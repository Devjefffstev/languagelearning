package user

import (
	"context"
	"time"

	"github.com/google/uuid"
)

// Service contains the business logic for user operations.
type Service struct {
	repo Repository
}

// NewService creates a new Service.
func NewService(repo Repository) *Service {
	return &Service{
		repo: repo,
	}
}

// Register creates a new user.
func (s *Service) Register(ctx context.Context, req NewUserRequest) (User, error) {
	// TODO: Hash the password here! Storing plain text is bad.
	// For now, we are skipping hashing to keep the initial setup simple.

	now := time.Now()
	newUser := User{
		ID:        uuid.New().String(),
		Email:     req.Email,
		Password:  req.Password, // WARNING: Plain text for now
		CreatedAt: now,
		UpdatedAt: now,
	}

	if err := s.repo.Create(ctx, newUser); err != nil {
		return User{}, err
	}

	return newUser, nil
}
