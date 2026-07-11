package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/Devjefffstev/reusable-api-go/userRegistration-api/internal/user"
)

func main() {
	fmt.Println("Starting User Registration API...")

	// 1. Initialize Storage
	repo := user.NewInMemoryRepository()

	// 2. Initialize Service
	svc := user.NewService(repo)

	// 3. Initialize Handler
	h := user.NewHandler(svc)

	// 4. Setup Routes
	http.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte("OK"))
	})

	http.HandleFunc("/users", h.RegisterUser)

	log.Println("Server listening on port 8080")
	if err := http.ListenAndServe(":8080", nil); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
