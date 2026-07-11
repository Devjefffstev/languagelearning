package basic

import (
	"net/http"
)

// BasicGoExamples is a standalone handler function.
// @Summary      Basic Example
// @Description  Returns a simple string to prove the API works
// @Tags         basic
// @Accept       json
// @Produce      plain
// @Success      200  {string}  string  "Basic Go Examples"
// @Router       /basic [post]
func BasicGoExamples(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Basic Go Examples"))
}
// SliceExamples is a standalone handler function.
// @Summary      Slice Example
// @Description  Returns a simple string to prove the API works
// @Tags         basic
// @Accept       json
// @Produce      plain
// @Success      200  {string}  string  "Slice Examples"
// @Router       /basic [post]
func SliceExamples(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Slice Examples"))
}
