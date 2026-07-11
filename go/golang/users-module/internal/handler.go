package internal

import (
	"encoding/json"
	"errors"
	"net/http"
	"strconv"

	core "github.com/Devjefffstev/golang/api-core"
)

// Handler handles HTTP requests for users.
type Handler struct {
	svc *Service
}

// NewHandler creates a new user HTTP handler.
func NewHandler(svc *Service) *Handler {
	return &Handler{svc: svc}
}

// RegisterRoutes registers user routes on the given mux.
func (h *Handler) RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("POST /users", h.create)
	mux.HandleFunc("GET /users/{id}", h.getByID)
	mux.HandleFunc("PUT /users/{id}", h.update)
	mux.HandleFunc("DELETE /users/{id}", h.delete)
	mux.HandleFunc("GET /users", h.list)
}

func (h *Handler) create(w http.ResponseWriter, r *http.Request) {
	var req CreateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		core.WriteError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	if req.Email == "" || req.Password == "" {
		core.WriteError(w, http.StatusBadRequest, "email and password are required")
		return
	}

	user, err := h.svc.Create(r.Context(), req)
	if err != nil {
		if errors.Is(err, ErrDuplicateEmail) {
			core.WriteError(w, http.StatusConflict, "email already exists")
			return
		}
		core.WriteError(w, http.StatusInternalServerError, "failed to create user")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(user)
}

func (h *Handler) getByID(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	user, err := h.svc.GetByID(r.Context(), id)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			core.WriteError(w, http.StatusNotFound, "user not found")
			return
		}
		core.WriteError(w, http.StatusInternalServerError, "failed to get user")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(user)
}

func (h *Handler) update(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	var req UpdateUserRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		core.WriteError(w, http.StatusBadRequest, "invalid request body")
		return
	}

	user, err := h.svc.Update(r.Context(), id, req)
	if err != nil {
		if errors.Is(err, ErrUserNotFound) {
			core.WriteError(w, http.StatusNotFound, "user not found")
			return
		}
		core.WriteError(w, http.StatusInternalServerError, "failed to update user")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(user)
}

func (h *Handler) delete(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")

	if err := h.svc.Delete(r.Context(), id); err != nil {
		if errors.Is(err, ErrUserNotFound) {
			core.WriteError(w, http.StatusNotFound, "user not found")
			return
		}
		core.WriteError(w, http.StatusInternalServerError, "failed to delete user")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

func (h *Handler) list(w http.ResponseWriter, r *http.Request) {
	page, _ := strconv.Atoi(r.URL.Query().Get("page"))
	pageSize, _ := strconv.Atoi(r.URL.Query().Get("page_size"))

	result, err := h.svc.List(r.Context(), page, pageSize)
	if err != nil {
		core.WriteError(w, http.StatusInternalServerError, "failed to list users")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(result)
}
