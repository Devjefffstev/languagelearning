package config

import (
	"os"
	"path/filepath"
	"testing"
	"time"
)

func TestLoad_Defaults(t *testing.T) {
	cfg := Load("users", "")

	if cfg.DB.Driver != "sqlite" {
		t.Errorf("DB.Driver = %q, want sqlite", cfg.DB.Driver)
	}
	if cfg.DB.DSN != ":memory:" {
		t.Errorf("DB.DSN = %q, want :memory:", cfg.DB.DSN)
	}
	if cfg.DB.MaxOpenConns != 25 {
		t.Errorf("DB.MaxOpenConns = %d, want 25", cfg.DB.MaxOpenConns)
	}
	if cfg.DB.MaxIdleConns != 5 {
		t.Errorf("DB.MaxIdleConns = %d, want 5", cfg.DB.MaxIdleConns)
	}
	if cfg.DB.ConnMaxLifetime != 5*time.Minute {
		t.Errorf("DB.ConnMaxLifetime = %v, want 5m", cfg.DB.ConnMaxLifetime)
	}
	if cfg.Broker.URL != "" {
		t.Errorf("Broker.URL = %q, want empty", cfg.Broker.URL)
	}
}

func TestLoad_YAMLOverride(t *testing.T) {
	yamlContent := `
modules:
  users:
    db:
      driver: postgres
      dsn: "postgres://localhost:5432/users"
      max_open_conns: 50
    broker:
      url: "amqp://localhost:5672"
`
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "app-config.yaml")
	if err := os.WriteFile(configPath, []byte(yamlContent), 0o644); err != nil {
		t.Fatal(err)
	}

	cfg := Load("users", configPath)

	if cfg.DB.Driver != "postgres" {
		t.Errorf("DB.Driver = %q, want postgres", cfg.DB.Driver)
	}
	if cfg.DB.DSN != "postgres://localhost:5432/users" {
		t.Errorf("DB.DSN = %q, want postgres://localhost:5432/users", cfg.DB.DSN)
	}
	if cfg.DB.MaxOpenConns != 50 {
		t.Errorf("DB.MaxOpenConns = %d, want 50", cfg.DB.MaxOpenConns)
	}
	// MaxIdleConns should remain default since not in YAML
	if cfg.DB.MaxIdleConns != 5 {
		t.Errorf("DB.MaxIdleConns = %d, want 5 (default)", cfg.DB.MaxIdleConns)
	}
	if cfg.Broker.URL != "amqp://localhost:5672" {
		t.Errorf("Broker.URL = %q, want amqp://localhost:5672", cfg.Broker.URL)
	}
}

func TestLoad_EnvOverridesYAML(t *testing.T) {
	yamlContent := `
modules:
  users:
    db:
      driver: postgres
      dsn: "postgres://localhost:5432/users"
`
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "app-config.yaml")
	if err := os.WriteFile(configPath, []byte(yamlContent), 0o644); err != nil {
		t.Fatal(err)
	}

	t.Setenv("USERS_DB_DSN", "postgres://prod:5432/users_prod")
	t.Setenv("USERS_BROKER_URL", "amqp://prod:5672")

	cfg := Load("users", configPath)

	// Driver from YAML (no env override)
	if cfg.DB.Driver != "postgres" {
		t.Errorf("DB.Driver = %q, want postgres (from YAML)", cfg.DB.Driver)
	}
	// DSN from env override
	if cfg.DB.DSN != "postgres://prod:5432/users_prod" {
		t.Errorf("DB.DSN = %q, want postgres://prod:5432/users_prod (env override)", cfg.DB.DSN)
	}
	// Broker from env
	if cfg.Broker.URL != "amqp://prod:5672" {
		t.Errorf("Broker.URL = %q, want amqp://prod:5672 (env override)", cfg.Broker.URL)
	}
}

func TestLoad_EnvOverridesDefaults(t *testing.T) {
	t.Setenv("AUTH_DB_DRIVER", "postgres")
	t.Setenv("AUTH_DB_AUTO_PROVISION", "true")
	t.Setenv("AUTH_DB_MAX_OPEN_CONNS", "100")
	t.Setenv("AUTH_DB_CONN_MAX_LIFETIME", "10m")

	cfg := Load("auth", "")

	if cfg.DB.Driver != "postgres" {
		t.Errorf("DB.Driver = %q, want postgres", cfg.DB.Driver)
	}
	if !cfg.DB.AutoProvision {
		t.Error("DB.AutoProvision = false, want true")
	}
	if cfg.DB.MaxOpenConns != 100 {
		t.Errorf("DB.MaxOpenConns = %d, want 100", cfg.DB.MaxOpenConns)
	}
	if cfg.DB.ConnMaxLifetime != 10*time.Minute {
		t.Errorf("DB.ConnMaxLifetime = %v, want 10m", cfg.DB.ConnMaxLifetime)
	}
}

func TestLoad_MissingYAMLFile(t *testing.T) {
	cfg := Load("users", "/nonexistent/path/config.yaml")

	// Should fall back to defaults
	if cfg.DB.Driver != "sqlite" {
		t.Errorf("DB.Driver = %q, want sqlite (default)", cfg.DB.Driver)
	}
}

func TestLoad_ModuleNotInYAML(t *testing.T) {
	yamlContent := `
modules:
  users:
    db:
      driver: postgres
`
	tmpDir := t.TempDir()
	configPath := filepath.Join(tmpDir, "app-config.yaml")
	if err := os.WriteFile(configPath, []byte(yamlContent), 0o644); err != nil {
		t.Fatal(err)
	}

	// Load for "auth" which isn't in the YAML
	cfg := Load("auth", configPath)

	if cfg.DB.Driver != "sqlite" {
		t.Errorf("DB.Driver = %q, want sqlite (default — auth not in YAML)", cfg.DB.Driver)
	}
}
