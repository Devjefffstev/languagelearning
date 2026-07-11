// Package db provides database connection management and migration utilities.
package db

import (
	"database/sql"
	"fmt"
	"os"
	"path/filepath"
	"time"

	_ "modernc.org/sqlite"
)

// Config holds database connection configuration.
type Config struct {
	Driver          string        // "sqlite" or "postgres" — defaults to "sqlite"
	DSN             string        // Data source name — defaults to ":memory:"
	MaxOpenConns    int           // Connection pool max open — defaults to 25
	MaxIdleConns    int           // Connection pool max idle — defaults to 5
	ConnMaxLifetime time.Duration // Connection max lifetime — defaults to 5 minutes
	AutoProvision   bool          // Create database file/dirs if not exists
}

// New creates a new database connection using the provided configuration.
// If cfg is nil or Driver is empty, it defaults to an in-memory SQLite database.
func New(cfg *Config) (*sql.DB, error) {
	if cfg == nil {
		cfg = &Config{}
	}

	driver := cfg.Driver
	dsn := cfg.DSN

	if driver == "" {
		driver = "sqlite"
	}

	if dsn == "" {
		dsn = ":memory:"
	}

	if driver == "sqlite" && cfg.AutoProvision && dsn != ":memory:" {
		dir := filepath.Dir(dsn)
		if err := os.MkdirAll(dir, 0o755); err != nil {
			return nil, fmt.Errorf("db: auto-provision directory %q: %w", dir, err)
		}
	}

	conn, err := sql.Open(driver, dsn)
	if err != nil {
		return nil, fmt.Errorf("db: open %s: %w", driver, err)
	}

	maxOpen := cfg.MaxOpenConns
	if maxOpen == 0 {
		maxOpen = 25
	}

	maxIdle := cfg.MaxIdleConns
	if maxIdle == 0 {
		maxIdle = 5
	}

	maxLifetime := cfg.ConnMaxLifetime
	if maxLifetime == 0 {
		maxLifetime = 5 * time.Minute
	}

	conn.SetMaxOpenConns(maxOpen)
	conn.SetMaxIdleConns(maxIdle)
	conn.SetConnMaxLifetime(maxLifetime)

	if err := conn.Ping(); err != nil {
		conn.Close()
		return nil, fmt.Errorf("db: ping %s: %w", driver, err)
	}

	return conn, nil
}
