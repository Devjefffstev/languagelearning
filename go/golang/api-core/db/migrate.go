package db

import (
	"database/sql"
	"fmt"
	"io/fs"
	"path/filepath"
	"sort"
)

// RunMigrations executes SQL migration files from an fs.FS in alphabetical order.
// It tracks applied migrations in a schema_migrations table to ensure idempotency.
func RunMigrations(db *sql.DB, migrationsFS fs.FS) error {
	if err := ensureMigrationsTable(db); err != nil {
		return fmt.Errorf("db: create migrations table: %w", err)
	}

	entries, err := fs.ReadDir(migrationsFS, ".")
	if err != nil {
		return fmt.Errorf("db: read migrations directory: %w", err)
	}

	var filenames []string
	for _, e := range entries {
		if e.IsDir() {
			continue
		}
		if filepath.Ext(e.Name()) == ".sql" {
			filenames = append(filenames, e.Name())
		}
	}
	sort.Strings(filenames)

	for _, filename := range filenames {
		applied, err := isMigrationApplied(db, filename)
		if err != nil {
			return fmt.Errorf("db: check migration %q: %w", filename, err)
		}
		if applied {
			continue
		}

		content, err := fs.ReadFile(migrationsFS, filename)
		if err != nil {
			return fmt.Errorf("db: read migration %q: %w", filename, err)
		}

		tx, err := db.Begin()
		if err != nil {
			return fmt.Errorf("db: begin transaction for %q: %w", filename, err)
		}

		if _, err := tx.Exec(string(content)); err != nil {
			tx.Rollback()
			return fmt.Errorf("db: execute migration %q: %w", filename, err)
		}

		if _, err := tx.Exec(
			"INSERT INTO schema_migrations (filename) VALUES (?)",
			filename,
		); err != nil {
			tx.Rollback()
			return fmt.Errorf("db: record migration %q: %w", filename, err)
		}

		if err := tx.Commit(); err != nil {
			return fmt.Errorf("db: commit migration %q: %w", filename, err)
		}
	}

	return nil
}

func ensureMigrationsTable(db *sql.DB) error {
	_, err := db.Exec(`
		CREATE TABLE IF NOT EXISTS schema_migrations (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			filename TEXT UNIQUE NOT NULL,
			applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	`)
	return err
}

func isMigrationApplied(db *sql.DB, filename string) (bool, error) {
	var count int
	err := db.QueryRow(
		"SELECT COUNT(*) FROM schema_migrations WHERE filename = ?",
		filename,
	).Scan(&count)
	if err != nil {
		return false, err
	}
	return count > 0, nil
}
