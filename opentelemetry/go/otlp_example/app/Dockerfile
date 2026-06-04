FROM golang:1.25-alpine AS builder

WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 go build -o /app/server .

FROM alpine:latest

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app/server /app/server

USER appuser

EXPOSE 9080

CMD ["/app/server"]
