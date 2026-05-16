// Package tools provides the get_weather tool for the weather agent.
package tools

import (
	"fmt"
	"strings"

	"google.golang.org/adk/tool"
	"google.golang.org/adk/tool/functiontool"
)

// WeatherArgs holds the input parameters for the get_weather tool.
type WeatherArgs struct {
	// City is the name of the city to retrieve weather for (e.g. "New York").
	City string `json:"city"`
}

// WeatherResult holds the output of a get_weather call.
type WeatherResult struct {
	// Status is "success" or "error".
	Status string `json:"status"`
	// Report contains the weather description when Status is "success".
	Report string `json:"report,omitempty"`
	// ErrorMessage describes the failure when Status is "error".
	ErrorMessage string `json:"error_message,omitempty"`
}

// mockWeatherDB is a simple in-memory weather lookup table used for demo purposes.
// A real implementation would call an external weather API.
var mockWeatherDB = map[string]string{
	"newyork": "The weather in New York is sunny with a temperature of 25°C.",
	"london":  "It's cloudy in London with a temperature of 15°C.",
	"tokyo":   "Tokyo is experiencing light rain and a temperature of 18°C.",
	"paris":   "Paris is partly cloudy with a temperature of 20°C.",
	"sydney":  "Sydney is clear and warm at 28°C.",
}

// getWeatherFunc retrieves the current weather report for a specified city.
// It returns a mock weather report from a pre-defined database.
// If the city is not found, an error result is returned.
func getWeatherFunc(_ tool.Context, args WeatherArgs) (WeatherResult, error) {
	fmt.Printf("--- Tool: get_weather called for city: %s ---\n", args.City)
	key := strings.ToLower(strings.ReplaceAll(args.City, " ", ""))
	if report, ok := mockWeatherDB[key]; ok {
		return WeatherResult{Status: "success", Report: report}, nil
	}
	return WeatherResult{
		Status:       "error",
		ErrorMessage: fmt.Sprintf("Sorry, I don't have weather information for '%s'.", args.City),
	}, nil
}

// NewGetWeatherTool creates and returns the get_weather function tool.
func NewGetWeatherTool() (tool.Tool, error) {
	return functiontool.New(functiontool.Config{
		Name:        "get_weather",
		Description: "Retrieves the current weather report for a specified city.",
	}, getWeatherFunc)
}
