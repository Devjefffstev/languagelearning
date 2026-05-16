package tools

import (
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"golang.org/x/net/html"
	"google.golang.org/adk/model"
	"google.golang.org/adk/tool"
	"google.golang.org/genai"
)

type FetchPage struct{}

func (f FetchPage) Name() string        { return "fetchPage" }
func (f FetchPage) Description() string { return "Retrieve the full text content of a webpage by its URL. Use this to read articles, documentation, or any online page." }
func (f FetchPage) IsLongRunning() bool { return false }

func (f FetchPage) ProcessRequest(_ tool.Context, req *model.LLMRequest) error {
	if req.Tools == nil {
		req.Tools = make(map[string]any)
	}
	if _, ok := req.Tools[f.Name()]; ok {
		return fmt.Errorf("duplicate tool: %q", f.Name())
	}
	req.Tools[f.Name()] = f

	if req.Config == nil {
		req.Config = &genai.GenerateContentConfig{}
	}
	var funcTool *genai.Tool
	for _, t := range req.Config.Tools {
		if t != nil && t.FunctionDeclarations != nil {
			funcTool = t
			break
		}
	}
	if funcTool == nil {
		req.Config.Tools = append(req.Config.Tools, &genai.Tool{
			FunctionDeclarations: []*genai.FunctionDeclaration{f.Declaration()},
		})
	} else {
		funcTool.FunctionDeclarations = append(funcTool.FunctionDeclarations, f.Declaration())
	}
	return nil
}

func (f FetchPage) Declaration() *genai.FunctionDeclaration {
	return &genai.FunctionDeclaration{
		Name:        "fetchPage",
		Description: "Retrieve the full text content of a webpage by its URL. Good for reading articles, documentation, or extracting information from a specific page.",
		Parameters: &genai.Schema{
			Type: genai.TypeObject,
			Properties: map[string]*genai.Schema{
				"url": {
					Type:        genai.TypeString,
					Description: "The full URL of the webpage to fetch (e.g. https://example.com/page).",
				},
			},
			Required: []string{"url"},
		},
	}
}

func (f FetchPage) Run(ctx tool.Context, args any) (map[string]any, error) {
	argsMap, ok := args.(map[string]any)
	if !ok {
		return nil, fmt.Errorf("invalid arguments: expected map[string]any")
	}
	urlStr, ok := argsMap["url"].(string)
	if !ok || strings.TrimSpace(urlStr) == "" {
		return nil, fmt.Errorf("url must be a non-empty string")
	}

	client := &http.Client{Timeout: 15 * time.Second}
	req, err := http.NewRequest("GET", urlStr, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create request: %w", err)
	}
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
	req.Header.Set("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
	req.Header.Set("Accept-Language", "en-US,en;q=0.9")

	resp, err := client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to fetch URL: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return nil, fmt.Errorf("server returned status %d", resp.StatusCode)
	}

	// Limit to 1MB to avoid huge pages
	body, err := io.ReadAll(io.LimitReader(resp.Body, 1<<20))
	if err != nil {
		return nil, fmt.Errorf("failed to read response: %w", err)
	}

	contentType := resp.Header.Get("Content-Type")
	if !strings.HasPrefix(contentType, "text/html") && !strings.Contains(contentType, "html") {
		// Not HTML — return raw text (first 8000 chars)
		text := string(body)
		if len(text) > 8000 {
			text = text[:8000] + "\n\n[...content truncated at 8000 chars]"
		}
		return map[string]any{"result": text}, nil
	}

	text := extractText(string(body))
	if len(text) > 8000 {
		text = text[:8000] + "\n\n[...content truncated at 8000 chars]"
	}

	if strings.TrimSpace(text) == "" {
		return map[string]any{"result": "Page appears to have no readable text content."}, nil
	}

	return map[string]any{"result": text}, nil
}

func extractText(htmlContent string) string {
	z := html.NewTokenizer(strings.NewReader(htmlContent))
	var parts []string
	var inScript, inStyle bool

	for {
		tokenType := z.Next()
		if tokenType == html.ErrorToken {
			break
		}

		switch tokenType {
		case html.StartTagToken, html.EndTagToken:
			name, _ := z.TagName()
			tag := string(name)
			if tag == "script" {
				inScript = tokenType == html.StartTagToken
			}
			if tag == "style" {
				inStyle = tokenType == html.StartTagToken
			}
			if tag == "br" || tag == "p" || tag == "div" || tag == "tr" || tag == "li" || tag == "h1" || tag == "h2" || tag == "h3" || tag == "h4" || tag == "h5" || tag == "h6" {
				parts = append(parts, "\n")
			}

		case html.TextToken:
			if inScript || inStyle {
				continue
			}
			text := strings.TrimSpace(string(z.Text()))
			if text != "" {
				parts = append(parts, text)
			}
		}
	}

	return strings.Join(parts, " ")
}
