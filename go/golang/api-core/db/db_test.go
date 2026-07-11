package db

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestNew_NilConfig(t *testing.T) {
	conn, err := New(nil)
	if err != nil {
		t.Fatalf("New(nil) returned error: %v", err)
	}
	defer conn.Close()

	if err := conn.Ping(); err != nil {
		t.Fatalf("Ping failed: %v", err)
	}
}

func TestNew_EmptyConfig(t *testing.T) {
	conn, err := New(&Config{})
	if err != nil {
		t.Fatalf("New(&Config{}) returned error: %v", err)
	}
	defer conn.Close()

	if err := conn.Ping(); err != nil {
		t.Fatalf("Ping failed: %v", err)
	}
}

func TestNew_ExplicitSQLiteInMemory(t *testing.T) {
	conn, err := New(&Config{
		Driver: "sqlite",
		DSN:    ":memory:",
	})
	if err != nil {
		t.Fatalf("New with explicit sqlite config returned error: %v", err)
	}
	defer conn.Close()

	if err := conn.Ping(); err != nil {
		t.Fatalf("Ping failed: %v", err)
	}
}

func TestNew_PoolSettings(t *testing.T) {
	cfg := &Config{
		MaxOpenConns:    10,
		MaxIdleConns:    3,
		ConnMaxLifetime: 2 * time.Minute,
	}
	conn, err := New(cfg)
	if err != nil {
		t.Fatalf("New returned error: %v", err)
	}
	defer conn.Close()

	stats := conn.Stats()
	if stats.MaxOpenConnections != 10 {
		t.Errorf("MaxOpenConnections = %d, want 10", stats.MaxOpenConnections)
	}
}

func TestNew_DefaultPoolSettings(t *testing.T) {
	conn, err := New(nil)
	if err != nil {
		t.Fatalf("New(nil) returned error: %v", err)
	}
	defer conn.Close()

	stats := conn.Stats()
	if stats.MaxOpenConnections != 25 {
		t.Errorf("MaxOpenConnections = %d, want 25 (default)", stats.MaxOpenConnections)
	}
}

func TestNew_AutoProvision(t *testing.T) {
	tmpDir := t.TempDir()
	dbPath := filepath.Join(tmpDir, "subdir", "nested", "test.db")

	conn, err := New(&Config{
		Driver:        "sqlite",
		DSN:           dbPath,
		AutoProvision: true,
	})
	if err != nil {
		t.Fatalf("New with auto-provision returned error: %v", err)
	}
	defer conn.Close()

	if _, err := os.Stat(dbPath); err != nil {
		t.Errorf("database file not created: %v", err)
	}
}

func TestNew_AutoProvisionSkipsMemory(t *testing.T) {
	conn, err := New(&Config{
		Driver:        "sqlite",
		DSN:           ":memory:",
		AutoProvision: true,
	})
	if err != nil {
		t.Fatalf("New with auto-provision + :memory: returned error: %v", err)
	}
	defer conn.Close()
}
