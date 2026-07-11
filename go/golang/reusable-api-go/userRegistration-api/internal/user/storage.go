package user

import (
	"context"
	"errors"
	"sync"
)

var (
	ErrUserNotFound = errors.New("user not found")
	ErrEmailTaken   = errors.New("email already taken")
)

// Repository defines the interface for user storage.
type Repository interface {
	Create(ctx context.Context, user User) error
	FindByEmail(ctx context.Context, email string) (User, error)
}

// InMemoryRepository is a simple in-memory implementation of Repository.
// It is thread-safe.
type InMemoryRepository struct {
	mu    sync.RWMutex
	users map[string]User
}

// NewInMemoryRepository creates a new InMemoryRepository.
func NewInMemoryRepository() *InMemoryRepository {
	return &InMemoryRepository{
		users: make(map[string]User),
	}
}

// Create saves a new user to the in-memory store.
func (r *InMemoryRepository) Create(ctx context.Context, user User) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.users[user.Email]; exists {
		return ErrEmailTaken
	}

	r.users[user.Email] = user
	return nil
}

// FindByEmail retrieves a user by their email address.
func (r *InMemoryRepository) FindByEmail(ctx context.Context, email string) (User, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	user, exists := r.users[email]
	if !exists {
		return User{}, ErrUserNotFound
	}
	return user, nil
}
