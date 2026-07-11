package core

import (
	"context"
	"sync"
)

// MemoryBroker is a thread-safe in-memory implementation of MessageBroker
// for testing and local development without requiring RabbitMQ.
type MemoryBroker struct {
	mu          sync.RWMutex
	subscribers map[string][]func(ctx context.Context, payload []byte) error
}

// NewMemoryBroker creates a new in-memory message broker.
func NewMemoryBroker() *MemoryBroker {
	return &MemoryBroker{
		subscribers: make(map[string][]func(ctx context.Context, payload []byte) error),
	}
}

// Publish sends an event to all subscribers of the given event type.
// Publishing to an event type with no subscribers does not error.
func (b *MemoryBroker) Publish(ctx context.Context, eventType string, payload []byte) error {
	b.mu.RLock()
	handlers := b.subscribers[eventType]
	b.mu.RUnlock()

	for _, handler := range handlers {
		if err := handler(ctx, payload); err != nil {
			return err
		}
	}
	return nil
}

// Subscribe registers a handler for the given event type.
// Multiple subscribers to the same event type all receive the event.
func (b *MemoryBroker) Subscribe(eventType string, handler func(ctx context.Context, payload []byte) error) error {
	b.mu.Lock()
	defer b.mu.Unlock()
	b.subscribers[eventType] = append(b.subscribers[eventType], handler)
	return nil
}
