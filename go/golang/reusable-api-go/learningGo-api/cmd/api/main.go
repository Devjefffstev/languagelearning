package main

import (
	"fmt"
	"net/http"

	"github.com/Devjefffstev/reusable-api-go/learningGo-api/internal/basic"
	httpSwagger "github.com/swaggo/http-swagger"
	_ "github.com/Devjefffstev/reusable-api-go/learningGo-api/docs" // definitions created by swag init
)

// @title Learning Go API
// @version 1.0
// @description This is a sample API for learning Go.
// @host localhost:8000
// @BasePath /
func main() {
	fmt.Println("Learning Go!")

	// Define a simple router handler to redirect to Swagger
	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		http.Redirect(w, r, "/swagger/index.html", http.StatusMovedPermanently)
	})

	// Register routes
	registerBasicRoutes()

	// Start the server on port 8000
	if err := http.ListenAndServe(":8000", nil); err != nil {
		fmt.Println("Error starting server:", err)
	}
}

// registerBasicRoutes handles the setup of routes for the basic package
func registerBasicRoutes() {
	http.HandleFunc("/basic", basic.BasicGoExamples)
	http.HandleFunc("/swagger/", httpSwagger.WrapHandler)
}
