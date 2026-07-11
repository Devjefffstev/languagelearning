// Package config provides three-tier configuration resolution:
// defaults -> YAML file -> environment variables.
package config

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

// ModuleConfig holds per-module configuration.
type ModuleConfig struct {
	DB     DBConfig     `yaml:"db"`
	Broker BrokerConfig `yaml:"broker"`
}

// DBConfig holds database connection settings.
type DBConfig struct {
	Driver          string        `yaml:"driver"`
	DSN             string        `yaml:"dsn"`
	MaxOpenConns    int           `yaml:"max_open_conns"`
	MaxIdleConns    int           `yaml:"max_idle_conns"`
	ConnMaxLifetime time.Duration `yaml:"conn_max_lifetime"`
	AutoProvision   bool          `yaml:"auto_provision"`
}

// BrokerConfig holds message broker settings.
type BrokerConfig struct {
	URL string `yaml:"url"`
}

// appConfig represents the full YAML config file structure.
type appConfig struct {
	Modules map[string]ModuleConfig `yaml:"modules"`
}

// defaults returns a ModuleConfig with sensible defaults (SQLite, no broker).
func defaults() ModuleConfig {
	return ModuleConfig{
		DB: DBConfig{
			Driver:          "sqlite",
			DSN:             ":memory:",
			MaxOpenConns:    25,
			MaxIdleConns:    5,
			ConnMaxLifetime: 5 * time.Minute,
			AutoProvision:   false,
		},
		Broker: BrokerConfig{
			URL: "",
		},
	}
}

// Load resolves configuration for a module using three-tier resolution:
// 1. Hardcoded defaults (SQLite, no broker)
// 2. YAML file override (app-config.yaml, per-module sections)
// 3. Environment variable override (MODULE_SECTION_KEY format)
func Load(moduleName string, configPath string) ModuleConfig {
	cfg := defaults()

	if configPath != "" {
		loadYAML(configPath, moduleName, &cfg)
	}

	applyEnvOverrides(moduleName, &cfg)

	return cfg
}

func loadYAML(path string, moduleName string, cfg *ModuleConfig) {
	data, err := os.ReadFile(path)
	if err != nil {
		return
	}

	var app appConfig
	if err := yaml.Unmarshal(data, &app); err != nil {
		return
	}

	mod, ok := app.Modules[moduleName]
	if !ok {
		return
	}

	if mod.DB.Driver != "" {
		cfg.DB.Driver = mod.DB.Driver
	}
	if mod.DB.DSN != "" {
		cfg.DB.DSN = mod.DB.DSN
	}
	if mod.DB.MaxOpenConns != 0 {
		cfg.DB.MaxOpenConns = mod.DB.MaxOpenConns
	}
	if mod.DB.MaxIdleConns != 0 {
		cfg.DB.MaxIdleConns = mod.DB.MaxIdleConns
	}
	if mod.DB.ConnMaxLifetime != 0 {
		cfg.DB.ConnMaxLifetime = mod.DB.ConnMaxLifetime
	}
	if mod.DB.AutoProvision {
		cfg.DB.AutoProvision = true
	}
	if mod.Broker.URL != "" {
		cfg.Broker.URL = mod.Broker.URL
	}
}

func applyEnvOverrides(moduleName string, cfg *ModuleConfig) {
	prefix := strings.ToUpper(moduleName)

	if v := os.Getenv(fmt.Sprintf("%s_DB_DRIVER", prefix)); v != "" {
		cfg.DB.Driver = v
	}
	if v := os.Getenv(fmt.Sprintf("%s_DB_DSN", prefix)); v != "" {
		cfg.DB.DSN = v
	}
	if v := os.Getenv(fmt.Sprintf("%s_DB_MAX_OPEN_CONNS", prefix)); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			cfg.DB.MaxOpenConns = n
		}
	}
	if v := os.Getenv(fmt.Sprintf("%s_DB_MAX_IDLE_CONNS", prefix)); v != "" {
		if n, err := strconv.Atoi(v); err == nil {
			cfg.DB.MaxIdleConns = n
		}
	}
	if v := os.Getenv(fmt.Sprintf("%s_DB_CONN_MAX_LIFETIME", prefix)); v != "" {
		if d, err := time.ParseDuration(v); err == nil {
			cfg.DB.ConnMaxLifetime = d
		}
	}
	if v := os.Getenv(fmt.Sprintf("%s_DB_AUTO_PROVISION", prefix)); v != "" {
		cfg.DB.AutoProvision = v == "true" || v == "1"
	}
	if v := os.Getenv(fmt.Sprintf("%s_BROKER_URL", prefix)); v != "" {
		cfg.Broker.URL = v
	}
}
