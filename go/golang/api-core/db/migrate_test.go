package db

import (
	"embed"
	"io/fs"
	"testing"
)

//go:embed testdata/migrations
var testMigrations embed.FS

func testMigrationsFS(t *testing.T) fs.FS {
	t.Helper()
	sub, err := fs.Sub(testMigrations, "testdata/migrations")
	if err != nil {
		t.Fatalf("failed to create sub FS: %v", err)
	}
	return sub
}

func TestRunMigrations_ExecutesInOrder(t *testing.T) {
	conn, err := New(nil)
	if err != nil {
		t.Fatalf("New(nil) returned error: %v", err)
	}
	defer conn.Close()

	if err := RunMigrations(conn, testMigrationsFS(t)); err != nil {
		t.Fatalf("RunMigrations returned error: %v", err)
	}

	// Verify table exists with both columns (001 + 002)
	_, err = conn.Exec("INSERT INTO test_items (name, description) VALUES ('test', 'desc')")
	if err != nil {
		t.Fatalf("insert into test_items failed (table or columns missing): %v", err)
	}

	var name, desc string
	err = conn.QueryRow("SELECT name, description FROM test_items WHERE name = 'test'").Scan(&name, &desc)
	if err != nil {
		t.Fatalf("query test_items failed: %v", err)
	}
	if name != "test" || desc != "desc" {
		t.Errorf("got name=%q desc=%q, want name=test desc=desc", name, desc)
	}
}

func TestRunMigrations_Idempotent(t *testing.T) {
	conn, err := New(nil)
	if err != nil {
		t.Fatalf("New(nil) returned error: %v", err)
	}
	defer conn.Close()

	migrationsFS := testMigrationsFS(t)

	// Run once
	if err := RunMigrations(conn, migrationsFS); err != nil {
		t.Fatalf("first RunMigrations returned error: %v", err)
	}

	// Run again — should not error
	if err := RunMigrations(conn, migrationsFS); err != nil {
		t.Fatalf("second RunMigrations returned error: %v", err)
	}

	// Verify no duplicate tracking rows
	var count int
	err = conn.QueryRow("SELECT COUNT(*) FROM schema_migrations").Scan(&count)
	if err != nil {
		t.Fatalf("count schema_migrations failed: %v", err)
	}
	if count != 2 {
		t.Errorf("schema_migrations count = %d, want 2 (one per migration file)", count)
	}
}

func TestRunMigrations_TracksAppliedMigrations(t *testing.T) {
	conn, err := New(nil)
	if err != nil {
		t.Fatalf("New(nil) returned error: %v", err)
	}
	defer conn.Close()

	if err := RunMigrations(conn, testMigrationsFS(t)); err != nil {
		t.Fatalf("RunMigrations returned error: %v", err)
	}

	// Verify both migrations are tracked in order
	rows, err := conn.Query("SELECT filename FROM schema_migrations ORDER BY id")
	if err != nil {
		t.Fatalf("query schema_migrations failed: %v", err)
	}
	defer rows.Close()

	expected := []string{
		"001_create_test_table.sql",
		"002_add_test_column.sql",
	}

	var i int
	for rows.Next() {
		var filename string
		if err := rows.Scan(&filename); err != nil {
			t.Fatalf("scan failed: %v", err)
		}
		if i >= len(expected) {
			t.Fatalf("unexpected extra migration: %s", filename)
		}
		if filename != expected[i] {
			t.Errorf("migration[%d] = %q, want %q", i, filename, expected[i])
		}
		i++
	}
	if i != len(expected) {
		t.Errorf("got %d migrations, want %d", i, len(expected))
	}
}
