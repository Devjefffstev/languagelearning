package internal

import (
	"context"
	"encoding/json"
	"log"
	"time"

	"github.com/google/uuid"

	core "github.com/Devjefffstev/golang/api-core"
	userEvents "github.com/Devjefffstev/golang/api-contracts/users"
)

// Service handles user business logic.
type Service struct {
	repo   Repository
	broker core.MessageBroker
}

// NewService creates a new user service.
func NewService(repo Repository, broker core.MessageBroker) *Service {
	return &Service{repo: repo, broker: broker}
}

func (s *Service) Create(ctx context.Context, req CreateUserRequest) (*User, error) {
	now := time.Now().UTC()
	user := &User{
		ID:        uuid.New().String(),
		Email:     req.Email,
		Password:  req.Password,
		CreatedAt: now,
		UpdatedAt: now,
	}

	if err := s.repo.Create(ctx, user); err != nil {
		return nil, err
	}

	s.publishEvent(ctx, "user.created", userEvents.UserCreated{
		ID:        user.ID,
		Email:     user.Email,
		CreatedAt: user.CreatedAt,
	})

	return user, nil
}

func (s *Service) GetByID(ctx context.Context, id string) (*User, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *Service) Update(ctx context.Context, id string, req UpdateUserRequest) (*User, error) {
	user, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	if req.Email != "" {
		user.Email = req.Email
	}
	if req.Password != "" {
		user.Password = req.Password
	}

	if err := s.repo.Update(ctx, user); err != nil {
		return nil, err
	}

	s.publishEvent(ctx, "user.updated", userEvents.UserUpdated{
		ID:        user.ID,
		Email:     user.Email,
		UpdatedAt: user.UpdatedAt,
	})

	return user, nil
}

func (s *Service) Delete(ctx context.Context, id string) error {
	if err := s.repo.Delete(ctx, id); err != nil {
		return err
	}

	s.publishEvent(ctx, "user.deleted", userEvents.UserDeleted{
		ID:        id,
		DeletedAt: time.Now().UTC(),
	})

	return nil
}

func (s *Service) List(ctx context.Context, page, pageSize int) (*PaginatedResponse, error) {
	if page < 1 {
		page = 1
	}
	if pageSize < 1 || pageSize > 100 {
		pageSize = 10
	}

	users, total, err := s.repo.List(ctx, page, pageSize)
	if err != nil {
		return nil, err
	}

	if users == nil {
		users = []User{}
	}

	return &PaginatedResponse{
		Data:     users,
		Total:    total,
		Page:     page,
		PageSize: pageSize,
	}, nil
}

func (s *Service) publishEvent(ctx context.Context, eventType string, event any) {
	payload, err := json.Marshal(event)
	if err != nil {
		log.Printf("users: failed to marshal %s event: %v", eventType, err)
		return
	}
	if err := s.broker.Publish(ctx, eventType, payload); err != nil {
		log.Printf("users: failed to publish %s event: %v", eventType, err)
	}
}
