// Package users provides a self-contained users module implementing the Module interface.
package users

import (
	"database/sql"
	"embed"
	"fmt"
	"io/fs"
	"net/http"

	core "github.com/Devjefffstev/golang/api-core"
	"github.com/Devjefffstev/golang/api-core/db"
	"github.com/Devjefffstev/golang/users-module/internal"
)

//go:embed internal/migrations
var migrationsFS embed.FS

// Config holds users module configuration.
type Config struct {
	DB     *sql.DB
	Broker core.MessageBroker
	Repo   internal.Repository // optional: inject custom repository
}

// Module is the users module implementing core.Module.
type Module struct {
	handler *internal.Handler
}

// New creates and initializes the users module.
func New(cfg Config) (*Module, error) {
	if cfg.DB == nil {
		conn, err := db.New(nil)
		if err != nil {
			return nil, fmt.Errorf("users: default db: %w", err)
		}
		cfg.DB = conn
	}

	if cfg.Broker == nil {
		cfg.Broker = core.NewMemoryBroker()
	}

	sub, err := fs.Sub(migrationsFS, "internal/migrations")
	if err != nil {
		return nil, fmt.Errorf("users: migrations fs: %w", err)
	}
	if err := db.RunMigrations(cfg.DB, sub); err != nil {
		return nil, fmt.Errorf("users: run migrations: %w", err)
	}

	repo := cfg.Repo
	if repo == nil {
		repo = internal.NewSQLiteRepository(cfg.DB)
	}

	svc := internal.NewService(repo, cfg.Broker)
	handler := internal.NewHandler(svc)

	return &Module{handler: handler}, nil
}

// RegisterRoutes registers user HTTP routes on the mux.
func (m *Module) RegisterRoutes(mux *http.ServeMux) {
	m.handler.RegisterRoutes(mux)
}

// RegisterEvents sets up event subscriptions (no-op for users module).
func (m *Module) RegisterEvents(broker core.MessageBroker) {}

// Name returns the module name.
func (m *Module) Name() string {
	return "users"
}
