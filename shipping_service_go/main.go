package main

import (
	"encoding/json"
	"fmt"
	"net/http"
	"time"
)

type EncomiendaGo struct {
	ID      int     `json:"id"`
	Codigo  string  `json:"codigo"`
	PesoKg  float64 `json:"peso_kg"`
	Estado  string  `json:"estado"`
	Destino string  `json:"destino"`
}

type ResultadoProcesamiento struct {
	TotalProcesadas    int            `json:"total_procesadas"`
	ConteoPorEstado    map[string]int `json:"conteo_por_estado"`
	EncomiendasPesadas []EncomiendaGo `json:"encomiendas_pesadas"`
	TiempoEjecucion    string         `json:"tiempo_ejecucion"`
}

type RespuestaSaludo struct {
	Mensaje   string `json:"mensaje"`
	Timestamp string `json:"timestamp"`
	Version   string `json:"version"`
}

func ProcesarEncomiendas(encomiendas []EncomiendaGo) ResultadoProcesamiento {
	inicio := time.Now()

	conteoPorEstado := make(map[string]int)
	var encomiendasPesadas []EncomiendaGo

	var estadoActual string
	var pesoActual float64
	var codigoActual string

	for _, enc := range encomiendas {
		estadoActual = enc.Estado
		pesoActual = enc.PesoKg
		codigoActual = enc.Codigo

		switch estadoActual {
		case "Registrado":
			conteoPorEstado["Registrado"]++
		case "En Ruta":
			conteoPorEstado["En Ruta"]++
		case "En Sucursal":
			conteoPorEstado["En Sucursal"]++
		case "Entregado":
			conteoPorEstado["Entregado"]++
		case "Devuelto":
			conteoPorEstado["Devuelto"]++
		default:
			conteoPorEstado["Desconocido"]++
		}

		if peso := pesoActual; peso > 20.0 {
			encomiendaPesada := EncomiendaGo{
				ID:      enc.ID,
				Codigo:  codigoActual,
				PesoKg:  pesoActual,
				Estado:  estadoActual,
				Destino: enc.Destino,
			}
			encomiendasPesadas = append(encomiendasPesadas, encomiendaPesada)
		}
	}

	duracion := time.Since(inicio)

	return ResultadoProcesamiento{
		TotalProcesadas:    len(encomiendas),
		ConteoPorEstado:    conteoPorEstado,
		EncomiendasPesadas: encomiendasPesadas,
		TiempoEjecucion:    duracion.String(),
	}
}

func saludoHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	respuesta := RespuestaSaludo{
		Mensaje:   "Bienvenido al Taller de Lenguajes de Programación - Sesión 10: Estructuras de Control y Colecciones en Go",
		Timestamp: time.Now().Format("2006-01-02 15:04:05"),
		Version:   "go1.26.4",
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(respuesta)
}

func encomiendasHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	encomiendas := []EncomiendaGo{
		{ID: 1, Codigo: "ENC-000001-LM", PesoKg: 2.5, Estado: "Registrado", Destino: "Lima"},
		{ID: 2, Codigo: "ENC-000002-PA", PesoKg: 5.0, Estado: "En Ruta", Destino: "Arequipa"},
		{ID: 3, Codigo: "ENC-000003-CU", PesoKg: 1.8, Estado: "Entregado", Destino: "Cusco"},
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(encomiendas)
}

func procesarEncomiendasHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")

	encomiendas := []EncomiendaGo{
		{ID: 1, Codigo: "ENC-000001-LM", PesoKg: 2.5, Estado: "Registrado", Destino: "Lima"},
		{ID: 2, Codigo: "ENC-000002-PA", PesoKg: 25.0, Estado: "En Ruta", Destino: "Arequipa"},
		{ID: 3, Codigo: "ENC-000003-CU", PesoKg: 1.8, Estado: "Entregado", Destino: "Cusco"},
		{ID: 4, Codigo: "ENC-000004-TR", PesoKg: 30.5, Estado: "Registrado", Destino: "Trujillo"},
		{ID: 5, Codigo: "ENC-000005-PI", PesoKg: 15.0, Estado: "En Sucursal", Destino: "Piura"},
		{ID: 6, Codigo: "ENC-000006-CH", PesoKg: 8.2, Estado: "En Ruta", Destino: "Chiclayo"},
		{ID: 7, Codigo: "ENC-000007-HU", PesoKg: 45.0, Estado: "Devuelto", Destino: "Huancayo"},
		{ID: 8, Codigo: "ENC-000008-IC", PesoKg: 3.7, Estado: "Entregado", Destino: "Ica"},
		{ID: 9, Codigo: "ENC-000009-TA", PesoKg: 22.3, Estado: "Registrado", Destino: "Tacna"},
		{ID: 10, Codigo: "ENC-000010-PU", PesoKg: 12.0, Estado: "En Ruta", Destino: "Puno"},
	}

	resultado := ProcesarEncomiendas(encomiendas)

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(resultado)
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
	mux.HandleFunc("/api/go/encomiendas/procesar", procesarEncomiendasHandler)
	mux.HandleFunc("/health", healthHandler)

	fmt.Println("==============================================")
	fmt.Println("  Shipping Service Go - Microservicio Activo")
	fmt.Println("  Puerto: 8081")
	fmt.Println("  Endpoints:")
	fmt.Println("    - GET /api/go/saludo")
	fmt.Println("    - GET /api/go/encomiendas")
	fmt.Println("    - GET /api/go/encomiendas/procesar")
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
