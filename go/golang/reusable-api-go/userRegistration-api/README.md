# User Registration API

This is a reusable Go microservice for managing user registration. It follows a Clean Architecture approach.

## Prerequisites

- **Go**: Version 1.22 or higher. [Download Go](https://go.dev/dl/)

## Getting Started

### 1. Run the API

You can run the API directly using `go run`:

```bash
# Navigate to the service directory
cd reusable-api-go/userRegistration-api

# Run the server
go run ./cmd/api/main.go
```

The server will start on port `8080`.

The server will start on port `8080`.

### 2. Run via Docker

Alternatively, you can run the API in a container:

```bash
# Build the image
docker build -t user-reg-api .

# Run the container (background, name: user-reg-api, port: 8080->8080)
docker run -d -p 8080:8080 --name user-reg-api user-reg-api

# Stop the container
docker stop user-reg-api

# Remove the container
docker rm user-reg-api
```

### 3. Test the Endpoint

You can use `curl` to register a new user:

```bash
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "securepassword"}'
```

**Response:**
```json
{
  "id": "some-uuid",
  "email": "user@example.com",
  "created_at": "...",
  "updated_at": "..."
}
```

## Project Structure

- `cmd/api/main.go`: Entry point. Wires up dependencies and starts the server.
- `internal/user`: Contains the domain logic (Model, Service, Repository, Handler).
- `internal/platform/database`: (To be added) Database connections.

## Troubleshooting

### Port 8080 already in use
If you see the error `listen tcp :8080: bind: address already in use`, it means the server is already running in the background or another process is using that port.

**To resolve this:**

1. Find the process ID (PID) using port 8080:
   ```bash
   lsof -i :8080
   ```
2. Kill the process:
   ```bash
   kill -9 <PID>
   ```

