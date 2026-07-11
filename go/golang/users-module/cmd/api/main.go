package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	core "github.com/Devjefffstev/golang/api-core"
	"github.com/Devjefffstev/golang/api-core/config"
	"github.com/Devjefffstev/golang/api-core/db"
	users "github.com/Devjefffstev/golang/users-module"
)

func main() {
	cfg := config.Load("users", "app-config.yaml")

	conn, err := db.New(&db.Config{
		Driver:          cfg.DB.Driver,
		DSN:             cfg.DB.DSN,
		MaxOpenConns:    cfg.DB.MaxOpenConns,
		MaxIdleConns:    cfg.DB.MaxIdleConns,
		ConnMaxLifetime: cfg.DB.ConnMaxLifetime,
		AutoProvision:   cfg.DB.AutoProvision,
	})
	if err != nil {
		log.Fatalf("failed to connect to database: %v", err)
	}

	broker := core.NewMemoryBroker()

	mod, err := users.New(users.Config{
		DB:     conn,
		Broker: broker,
	})
	if err != nil {
		log.Fatalf("failed to create users module: %v", err)
	}

	mux := http.NewServeMux()
	mod.RegisterRoutes(mux)

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Users module listening on :%s", port)
	fmt.Printf("Endpoints:\n")
	fmt.Printf("  POST   http://localhost:%s/users\n", port)
	fmt.Printf("  GET    http://localhost:%s/users\n", port)
	fmt.Printf("  GET    http://localhost:%s/users/{id}\n", port)
	fmt.Printf("  PUT    http://localhost:%s/users/{id}\n", port)
	fmt.Printf("  DELETE http://localhost:%s/users/{id}\n", port)

	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatalf("server error: %v", err)
	}
}
