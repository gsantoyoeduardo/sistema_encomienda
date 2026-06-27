package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type EncomiendaGo struct {
	ID     int     `json:"id"`
	Codigo string  `json:"codigo"`
	Peso   float64 `json:"peso"`
}

type RespuestaSaludo struct {
	Mensaje   string `json:"mensaje"`
	Timestamp string `json:"timestamp"`
	Version   string `json:"version"`
}

func saludoHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	respuesta := RespuestaSaludo{
		Mensaje:   "Bienvenido al Taller de Lenguajes de Programación - Sesión 09: Introducción a Go",
		Timestamp: time.Now().Format("2006-01-02 15:04:05"),
		Version:   "go1.26.4",
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(respuesta)
}

func encomiendasHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	encomiendas := []EncomiendaGo{
		{ID: 1, Codigo: "ENC-000001-LM", Peso: 2.5},
		{ID: 2, Codigo: "ENC-000002-PA", Peso: 5.0},
		{ID: 3, Codigo: "ENC-000003-CU", Peso: 1.8},
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(encomiendas)
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	fmt.Fprintf(w, `{"status":"ok","service":"shipping_service_go","port":8081}`)
}

func main() {
	mux := http.NewServeMux()

	mux.HandleFunc("/api/go/saludo", saludoHandler)
	mux.HandleFunc("/api/go/encomiendas", encomiendasHandler)
	mux.HandleFunc("/health", healthHandler)

	fmt.Println("==============================================")
	fmt.Println("  Shipping Service Go - Microservicio Activo")
	fmt.Println("  Puerto: 8081")
	fmt.Println("  Endpoints:")
	fmt.Println("    - GET /api/go/saludo")
	fmt.Println("    - GET /api/go/encomiendas")
	fmt.Println("    - GET /health")
	fmt.Println("==============================================")

	server := &http.Server{
		Addr:         ":8081",
		Handler:      mux,
		ReadTimeout:  10 * time.Second,
		WriteTimeout: 10 * time.Second,
	}

	err := server.ListenAndServe()
	if err != nil {
		fmt.Printf("Error al iniciar el servidor: %v\n", err)
	}
}
