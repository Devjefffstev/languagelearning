// Package core defines the shared interfaces and types for the Go API Modules platform.
// All reusable API modules implement the Module interface to enable uniform
// composition, wiring, and discovery across applications.
package core

import "net/http"

// Module defines the contract for reusable API modules.
// Each module registers its own HTTP routes and event subscriptions,
// and identifies itself by name for logging and discovery.
type Module interface {
	RegisterRoutes(mux *http.ServeMux)
	RegisterEvents(broker MessageBroker)
	Name() string
}
