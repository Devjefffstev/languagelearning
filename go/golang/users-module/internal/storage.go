package internal

import (
	"context"
	"database/sql"
	"errors"
	"strings"
	"time"
)

// ErrUserNotFound is returned when a user cannot be found.
var ErrUserNotFound = errors.New("user not found")

// ErrDuplicateEmail is returned when a user with the same email already exists.
var ErrDuplicateEmail = errors.New("email already exists")

// Repository defines the data access interface for users.
type Repository interface {
	Create(ctx context.Context, user *User) error
	GetByID(ctx context.Context, id string) (*User, error)
	GetByEmail(ctx context.Context, email string) (*User, error)
	Update(ctx context.Context, user *User) error
	Delete(ctx context.Context, id string) error
	List(ctx context.Context, page, pageSize int) ([]User, int, error)
}

// SQLiteRepository is the default SQLite implementation of Repository.
type SQLiteRepository struct {
	db *sql.DB
}

// NewSQLiteRepository creates a new SQLite-backed repository.
func NewSQLiteRepository(db *sql.DB) *SQLiteRepository {
	return &SQLiteRepository{db: db}
}

func (r *SQLiteRepository) Create(ctx context.Context, user *User) error {
	_, err := r.db.ExecContext(ctx,
		"INSERT INTO users (id, email, password, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
		user.ID, user.Email, user.Password, user.CreatedAt, user.UpdatedAt,
	)
	if err != nil && strings.Contains(err.Error(), "UNIQUE constraint failed") {
		return ErrDuplicateEmail
	}
	return err
}

func (r *SQLiteRepository) GetByID(ctx context.Context, id string) (*User, error) {
	var u User
	err := r.db.QueryRowContext(ctx,
		"SELECT id, email, password, created_at, updated_at FROM users WHERE id = ?", id,
	).Scan(&u.ID, &u.Email, &u.Password, &u.CreatedAt, &u.UpdatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrUserNotFound
	}
	return &u, err
}

func (r *SQLiteRepository) GetByEmail(ctx context.Context, email string) (*User, error) {
	var u User
	err := r.db.QueryRowContext(ctx,
		"SELECT id, email, password, created_at, updated_at FROM users WHERE email = ?", email,
	).Scan(&u.ID, &u.Email, &u.Password, &u.CreatedAt, &u.UpdatedAt)
	if errors.Is(err, sql.ErrNoRows) {
		return nil, ErrUserNotFound
	}
	return &u, err
}

func (r *SQLiteRepository) Update(ctx context.Context, user *User) error {
	user.UpdatedAt = time.Now().UTC()
	result, err := r.db.ExecContext(ctx,
		"UPDATE users SET email = ?, password = ?, updated_at = ? WHERE id = ?",
		user.Email, user.Password, user.UpdatedAt, user.ID,
	)
	if err != nil {
		return err
	}
	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrUserNotFound
	}
	return nil
}

func (r *SQLiteRepository) Delete(ctx context.Context, id string) error {
	result, err := r.db.ExecContext(ctx, "DELETE FROM users WHERE id = ?", id)
	if err != nil {
		return err
	}
	rows, err := result.RowsAffected()
	if err != nil {
		return err
	}
	if rows == 0 {
		return ErrUserNotFound
	}
	return nil
}

func (r *SQLiteRepository) List(ctx context.Context, page, pageSize int) ([]User, int, error) {
	var total int
	if err := r.db.QueryRowContext(ctx, "SELECT COUNT(*) FROM users").Scan(&total); err != nil {
		return nil, 0, err
	}

	offset := (page - 1) * pageSize
	rows, err := r.db.QueryContext(ctx,
		"SELECT id, email, password, created_at, updated_at FROM users ORDER BY created_at DESC LIMIT ? OFFSET ?",
		pageSize, offset,
	)
	if err != nil {
		return nil, 0, err
	}
	defer rows.Close()

	var users []User
	for rows.Next() {
		var u User
		if err := rows.Scan(&u.ID, &u.Email, &u.Password, &u.CreatedAt, &u.UpdatedAt); err != nil {
			return nil, 0, err
		}
		users = append(users, u)
	}
	return users, total, rows.Err()
}
