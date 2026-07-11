package core

import "context"

// MessageBroker abstracts event publish/subscribe communication.
// Modules code against this interface, enabling swappable implementations:
// in-memory for testing, RabbitMQ for production, Azure Event Hub for future use.
type MessageBroker interface {
	Publish(ctx context.Context, eventType string, payload []byte) error
	Subscribe(eventType string, handler func(ctx context.Context, payload []byte) error) error
}
