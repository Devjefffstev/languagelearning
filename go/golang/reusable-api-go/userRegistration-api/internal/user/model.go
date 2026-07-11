package user

import (
	"time"
)

// User represents a user in the system.
type User struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	Password  string    `json:"-"` // Never expose password in JSON
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// NewUserRequest represents the data required to register a new user.
type NewUserRequest struct {
	Email    string `json:"email"`
	Password string `json:"password"`
}
