// Package users defines event contracts for the users module.
package users

import "time"

// UserCreated is published when a new user is created.
type UserCreated struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	CreatedAt time.Time `json:"created_at"`
}

// UserUpdated is published when a user's profile is updated.
type UserUpdated struct {
	ID        string    `json:"id"`
	Email     string    `json:"email"`
	UpdatedAt time.Time `json:"updated_at"`
}

// UserDeleted is published when a user is deleted.
type UserDeleted struct {
	ID        string    `json:"id"`
	DeletedAt time.Time `json:"deleted_at"`
}

// RoleAssigned is published when a role is assigned to a user.
type RoleAssigned struct {
	UserID    string    `json:"user_id"`
	RoleID    string    `json:"role_id"`
	RoleName  string    `json:"role_name"`
	Timestamp time.Time `json:"timestamp"`
}

// RoleRemoved is published when a role is removed from a user.
type RoleRemoved struct {
	UserID    string    `json:"user_id"`
	RoleID    string    `json:"role_id"`
	RoleName  string    `json:"role_name"`
	Timestamp time.Time `json:"timestamp"`
}
