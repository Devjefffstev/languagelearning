package main

import (
	"context"
	"errors"
	"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp"
	"log/slog"
	"net"
	"net/http"
	"os"
	"os/signal"
	"time"
)

func  main() {
	if err := run(); err != nil {
		slog.Error("application failed", "error", err)
		os.Exit(1)
	}
}

func run() (err error){
	// Handle SIGINT (CTRL+C) gracefully.
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt)
	defer stop()

	// Set up OpenTelemetry.
	otelShutdown, err := setupOTelSDK(ctx)
	if err != nil {
		return err
	}
	// Handle shutdown properly so nothing leaks.
	defer func() {
		err = errors.Join(err, otelShutdown(context.Background()))
	}()
	// Start HTTP server.
	srv := &http.Server{
		Addr:         ":9080",
		BaseContext: func(net.Listener) context.Context { return ctx },
		ReadTimeout:  time.Second,
		WriteTimeout: 10 * time.Second,
		Handler:      newHTTPHandler(),
	}
	srvErr := make(chan error, 1)
	go func() {
		slog.InfoContext(ctx, "Running HTTP server...")
		srvErr <- srv.ListenAndServe()
	}()

	// Wait for interruption.
	select {
	case err = <-srvErr:
		// Error when starting HTTP server.
		return err
	case <-ctx.Done():
		// Wait for first CTRL+C.
		// Stop receiving signal notifications as soon as possible.
		stop()
	}
	// When Shutdown is called, ListenAndServe immediately returns ErrServerClosed.
	err = srv.Shutdown(context.Background())
	return err
}
func newHTTPHandler() http.Handler {
	mux := http.NewServeMux()

	// Register handlers.
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		logger.ErrorContext(r.Context(), "page not found", "path", r.URL.Path)
		w.WriteHeader(http.StatusNotFound)
		w.Write([]byte("not found — try /rolldice or /rolldice/{player}\n"))
	})
	mux.Handle("/rolldice", http.HandlerFunc(randomnumberstv))
	mux.Handle("/rolldice/{player}", http.HandlerFunc(randomnumberstv))

	// Add HTTP instrumentation for the whole server.
	handler := otelhttp.NewHandler(mux, "/")
	return handler
}