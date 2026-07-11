# Build Stage
FROM golang:1.25-alpine AS builder

WORKDIR /app

# Copy dependency files
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the binary
# -o main: name the output file "main"
# ./cmd/api/main.go: the entry point
RUN go build -o main ./cmd/api/main.go

# Run Stage
FROM alpine:latest

WORKDIR /app

# Copy binary from builder
COPY --from=builder /app/main .

# Expose port (8000 for learningGo-api)
EXPOSE 8000

# Run the binary
CMD ["./main"]
