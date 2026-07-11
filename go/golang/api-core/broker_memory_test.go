package core

import (
	"context"
	"sync"
	"sync/atomic"
	"testing"
)

func TestMemoryBroker_PublishSubscribe(t *testing.T) {
	broker := NewMemoryBroker()
	var received []byte

	broker.Subscribe("user.created", func(ctx context.Context, payload []byte) error {
		received = payload
		return nil
	})

	broker.Publish(context.Background(), "user.created", []byte(`{"id":"123"}`))

	if string(received) != `{"id":"123"}` {
		t.Errorf("received = %q, want %q", string(received), `{"id":"123"}`)
	}
}

func TestMemoryBroker_MultipleSubscribers(t *testing.T) {
	broker := NewMemoryBroker()
	var count int

	broker.Subscribe("user.created", func(ctx context.Context, payload []byte) error {
		count++
		return nil
	})
	broker.Subscribe("user.created", func(ctx context.Context, payload []byte) error {
		count++
		return nil
	})

	broker.Publish(context.Background(), "user.created", []byte(`{}`))

	if count != 2 {
		t.Errorf("count = %d, want 2 (both subscribers called)", count)
	}
}

func TestMemoryBroker_NoSubscribers(t *testing.T) {
	broker := NewMemoryBroker()

	err := broker.Publish(context.Background(), "no.subscribers", []byte(`{}`))
	if err != nil {
		t.Errorf("Publish with no subscribers returned error: %v", err)
	}
}

func TestMemoryBroker_ConcurrentSafe(t *testing.T) {
	broker := NewMemoryBroker()
	var calls atomic.Int64

	var wg sync.WaitGroup
	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			broker.Subscribe("event", func(ctx context.Context, payload []byte) error {
				calls.Add(1)
				return nil
			})
		}()
	}
	wg.Wait()

	for i := 0; i < 10; i++ {
		wg.Add(1)
		go func() {
			defer wg.Done()
			broker.Publish(context.Background(), "event", []byte(`{}`))
		}()
	}
	wg.Wait()

	if calls.Load() == 0 {
		t.Error("expected some handler calls, got 0")
	}
}

func TestMemoryBroker_ImplementsInterface(t *testing.T) {
	var _ MessageBroker = (*MemoryBroker)(nil)
}
