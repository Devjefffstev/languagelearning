package tools

import (
	"encoding/json"
	"fmt"
	"net/http"
	"net/url"
	"strings"
	"time"

	"google.golang.org/adk/model"
	"google.golang.org/adk/tool"
	"google.golang.org/genai"
)

type SearchInternet struct{}

func (s SearchInternet) Name() string        { return "searchInternet" }
func (s SearchInternet) Description() string { return "Search the internet for current information, prices, news, and facts." }
func (s SearchInternet) IsLongRunning() bool { return false }

func (s SearchInternet) ProcessRequest(_ tool.Context, req *model.LLMRequest) error {
	if req.Tools == nil {
		req.Tools = make(map[string]any)
	}
	if _, ok := req.Tools[s.Name()]; ok {
		return fmt.Errorf("duplicate tool: %q", s.Name())
	}
	req.Tools[s.Name()] = s

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
			FunctionDeclarations: []*genai.FunctionDeclaration{s.Declaration()},
		})
	} else {
		funcTool.FunctionDeclarations = append(funcTool.FunctionDeclarations, s.Declaration())
	}
	return nil
}

func (s SearchInternet) Declaration() *genai.FunctionDeclaration {
	return &genai.FunctionDeclaration{
		Name:        "searchInternet",
		Description: "Search the internet for current information, prices, news, and facts.",
		Parameters: &genai.Schema{
			Type: genai.TypeObject,
			Properties: map[string]*genai.Schema{
				"query": {
					Type:        genai.TypeString,
					Description: "The search query to look up on the internet.",
				},
			},
			Required: []string{"query"},
		},
	}
}

func (s SearchInternet) Run(ctx tool.Context, args any) (map[string]any, error) {
	argsMap, ok := args.(map[string]any)
	if !ok {
		return nil, fmt.Errorf("invalid arguments: expected map[string]any")
	}
	query, ok := argsMap["query"].(string)
	if !ok || strings.TrimSpace(query) == "" {
		return nil, fmt.Errorf("query must be a non-empty string")
	}

	result, err := searchDDG(query)
	if err != nil {
		return nil, fmt.Errorf("search failed: %w", err)
	}

	return map[string]any{"result": result}, nil
}

type ddgResponse struct {
	AbstractText  string          `json:"AbstractText"`
	AbstractURL   string          `json:"AbstractURL"`
	AbstractSource string         `json:"AbstractSource"`
	Type          string          `json:"Type"`
	Results       []ddgResult     `json:"Results"`
	RelatedTopics []ddgRelated    `json:"RelatedTopics"`
}

type ddgResult struct {
	Text string `json:"Text"`
	URL  string `json:"FirstURL"`
}

type ddgRelated struct {
	Text   string        `json:"Text"`
	URL    string        `json:"FirstURL"`
	Topics []ddgRelated  `json:"Topics"`
	Name   string        `json:"Name"`
}

func searchDDG(query string) (string, error) {
	client := &http.Client{Timeout: 10 * time.Second}

	req, _ := http.NewRequest("GET", "https://api.duckduckgo.com/?"+url.Values{
		"q":          {query},
		"format":     {"json"},
		"no_html":    {"1"},
		"skip_disambig": {"1"},
	}.Encode(), nil)
	req.Header.Set("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

	resp, err := client.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	var data ddgResponse
	if err := json.NewDecoder(resp.Body).Decode(&data); err != nil {
		return "", err
	}

	var parts []string

	if data.AbstractText != "" {
		parts = append(parts, fmt.Sprintf("Summary: %s\nSource: %s\nURL: %s\n",
			data.AbstractText, data.AbstractSource, data.AbstractURL))
	}

	for _, r := range data.Results {
		parts = append(parts, fmt.Sprintf("- %s (%s)", r.Text, r.URL))
	}

	var count int
	for _, rt := range data.RelatedTopics {
		if count >= 5 {
			break
		}
		if rt.Text != "" {
			parts = append(parts, fmt.Sprintf("- %s", rt.Text))
			if rt.URL != "" {
				parts[count] += fmt.Sprintf(" (%s)", rt.URL)
			}
			count++
		}
		if rt.Topics != nil {
			for _, t := range rt.Topics {
				if count >= 5 {
					break
				}
				if t.Text != "" {
					parts = append(parts, fmt.Sprintf("- %s", t.Text))
					count++
				}
			}
		}
	}

	if len(parts) == 0 {
		return "No results found.", nil
	}

	var sb strings.Builder
	sb.WriteString(fmt.Sprintf("Results for %q:\n\n", query))
	sb.WriteString(strings.Join(parts, "\n"))
	sb.WriteString("\n\n(Results from DuckDuckGo)")

	return sb.String(), nil
}
