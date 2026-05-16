// Package tools provides the say_hello and say_goodbye greeting tools.
package tools

import (
	"fmt"

	"google.golang.org/adk/tool"
	"google.golang.org/adk/tool/functiontool"
)

// SayHelloArgs holds the optional input for the say_hello tool.
type SayHelloArgs struct {
	// Name is the person's name to include in the greeting.
	// If empty, a generic greeting is returned.
	Name string `json:"name,omitempty" jsonschema:"The name of the person to greet, extracted from what the user said. Leave empty if no name was mentioned."`
}

// SayGoodbyeArgs is an empty struct; say_goodbye requires no input.
type SayGoodbyeArgs struct{}

// sayHelloFunc provides a simple greeting.
// If a name is provided it will be used; otherwise a generic greeting is returned.
func sayHelloFunc(_ tool.Context, args SayHelloArgs) (string, error) {
	if args.Name != "" {
		fmt.Printf("--- Tool: say_hello called with name: %s ---\n", args.Name)
		return fmt.Sprintf("Hello, %s!", args.Name), nil
	}
	fmt.Println("--- Tool: say_hello called without a specific name ---")
	return "Hello there!", nil
}

// sayGoodbyeFunc provides a simple farewell message to conclude the conversation.
func sayGoodbyeFunc(_ tool.Context, _ SayGoodbyeArgs) (string, error) {
	fmt.Println("--- Tool: say_goodbye called ---")
	return "Goodbye! Have a great day.", nil
}

// NewSayHelloTool creates and returns the say_hello function tool.
func NewSayHelloTool() (tool.Tool, error) {
	return functiontool.New(functiontool.Config{
		Name:        "say_hello",
		Description: "Provides a simple greeting. If a name is provided, it will be used.",
	}, sayHelloFunc)
}

// NewSayGoodbyeTool creates and returns the say_goodbye function tool.
func NewSayGoodbyeTool() (tool.Tool, error) {
	return functiontool.New(functiontool.Config{
		Name:        "say_goodbye",
		Description: "Provides a simple farewell message to conclude the conversation.",
	}, sayGoodbyeFunc)
}
