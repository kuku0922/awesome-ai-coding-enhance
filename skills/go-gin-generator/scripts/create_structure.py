#!/usr/bin/env python3
"""
Go project structure creation utilities.

This module provides functions to create standard Go project directories
and files following golang-standards/project-layout conventions.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional


class GoProjectStructure:
    """Creates and manages Go project directory structure."""

    def __init__(self, project_name: str, project_path: str):
        """
        Initialize project structure creator.

        Args:
            project_name: Name of the project
            project_path: Base path where project will be created
        """
        self.project_name = project_name
        self.project_path = Path(project_path) / project_name
        self.module_path = f"github.com/username/{project_name}"  # Default, can be customized

    def set_module_path(self, module_path: str):
        """Set the Go module path for the project."""
        self.module_path = module_path

    def create_directory_structure(self, project_type: str = "api") -> None:
        """
        Create the standard Go project directory structure.

        Args:
            project_type: Type of project ("api", "web", "microservice", "grpc")
        """
        # Standard directories for all project types
        base_dirs = [
            "cmd/server",
            "internal/config",
            "internal/handler",
            "internal/middleware",
            "internal/model",
            "internal/repository",
            "internal/service",
            "pkg",
            "api",
            "scripts",
            "configs",
            "docs",
            "web",
            "build",
            "deployments",
            "init"
        ]

        # Additional directories for specific project types
        if project_type in ["api", "web"]:
            base_dirs.extend([
                "internal/validator",
                "internal/response",
                "test/e2e",
                "test/integration"
            ])

        if project_type == "web":
            base_dirs.extend([
                "internal/template",
                "internal/static",
                "web/templates",
                "web/static/css",
                "web/static/js",
                "web/static/images"
            ])

        if project_type == "microservice":
            base_dirs.extend([
                "internal/health",
                "internal/metrics",
                "internal/grpc",
                "proto"
            ])

        if project_type == "grpc":
            base_dirs.extend([
                "internal/grpc",
                "internal/proto",
                "proto",
                "third_party/proto"
            ])

        # Create all directories
        for dir_path in base_dirs:
            full_path = self.project_path / dir_path
            full_path.mkdir(parents=True, exist_ok=True)

        # Create .gitkeep files in empty directories
        for dir_path in base_dirs:
            self._create_gitkeep(dir_path)

    def _create_gitkeep(self, dir_path: str) -> None:
        """Create .gitkeep file in specified directory."""
        gitkeep_path = self.project_path / dir_path / ".gitkeep"
        if not any(gitkeep_path.parent.iterdir()):
            gitkeep_path.touch()

    def create_main_file(self, project_type: str = "api") -> None:
        """
        Create the main.go file with basic setup.

        Args:
            project_type: Type of project being created
        """
        main_file = self.project_path / "cmd/server/main.go"

        if project_type == "api":
            content = self._get_api_main_template()
        elif project_type == "web":
            content = self._get_web_main_template()
        elif project_type == "microservice":
            content = self._get_microservice_main_template()
        elif project_type == "grpc":
            content = self._get_grpc_main_template()
        else:
            content = self._get_api_main_template()  # Default to API template

        main_file.write_text(content)

    def _get_api_main_template(self) -> str:
        """Get main.go template for REST API projects."""
        return f'''package main

import (
	"log"
	"os"

	"{self.module_path}/internal/config"
	"{self.module_path}/internal/handler"
	"{self.module_path}/internal/middleware"

	"github.com/gin-gonic/gin"
)

func main() {{
	// Initialize configuration
	cfg := config.Load()

	// Set Gin mode
	if cfg.Server.Mode == "release" {{
		gin.SetMode(gin.ReleaseMode)
	}}

	// Create Gin engine
	r := gin.Default()

	// Add middleware
	r.Use(middleware.Logger())
	r.Use(middleware.Recovery())
	r.Use(middleware.CORS())

	// Initialize handlers
	api := r.Group("/api/v1")
	{{
		handler.NewHealthHandler(api)
		handler.NewExampleHandler(api)
	}}

	// Start server
	port := os.Getenv("PORT")
	if port == "" {{
		port = cfg.Server.Port
	}}

	log.Printf("Server starting on port %s", port)
	if err := r.Run(":" + port); err != nil {{
		log.Fatal("Failed to start server:", err)
	}}
}}
'''

    def _get_web_main_template(self) -> str:
        """Get main.go template for web applications."""
        return f'''package main

import (
	"log"
	"os"

	"{self.module_path}/internal/config"
	"{self.module_path}/internal/handler"
	"{self.module_path}/internal/middleware"

	"github.com/gin-gonic/gin"
)

func main() {{
	// Initialize configuration
	cfg := config.Load()

	// Set Gin mode
	if cfg.Server.Mode == "release" {{
		gin.SetMode(gin.ReleaseMode)
	}}

	// Create Gin engine
	r := gin.Default()

	// Load templates
	r.LoadHTMLGlob("web/templates/*")
	r.Static("/static", "./web/static")

	// Add middleware
	r.Use(middleware.Logger())
	r.Use(middleware.Recovery())
	r.Use(middleware.CORS())

	// Initialize handlers
	api := r.Group("/api/v1")
	{{
		handler.NewHealthHandler(api)
		handler.NewAPIHandler(api)
	}}

	// Web routes
	r.GET("/", handler.NewWebHandler().Home)
	r.GET("/about", handler.NewWebHandler().About)

	// Start server
	port := os.Getenv("PORT")
	if port == "" {{
		port = cfg.Server.Port
	}}

	log.Printf("Server starting on port %s", port)
	if err := r.Run(":" + port); err != nil {{
		log.Fatal("Failed to start server:", err)
	}}
}}
'''

    def _get_microservice_main_template(self) -> str:
        """Get main.go template for microservices."""
        return f'''package main

import (
	"context"
	"log"
	"os"
	"os/signal"
	"syscall"
	"time"

	"{self.module_path}/internal/config"
	"{self.module_path}/internal/health"
	"{self.module_path}/internal/handler"
	"{self.module_path}/internal/middleware"
	"{self.module_path}/internal/metrics"

	"github.com/gin-gonic/gin"
)

func main() {{
	// Initialize configuration
	cfg := config.Load()

	// Set Gin mode
	if cfg.Server.Mode == "release" {{
		gin.SetMode(gin.ReleaseMode)
	}}

	// Create Gin engine
	r := gin.Default()

	// Add middleware
	r.Use(middleware.Logger())
	r.Use(middleware.Recovery())
	r.Use(middleware.CORS())
	r.Use(metrics.PrometheusMiddleware())

	// Initialize health check
	healthCheck := health.NewChecker()

	// Initialize handlers
	api := r.Group("/api/v1")
	{{
		handler.NewHealthHandler(api, healthCheck)
		handler.NewServiceHandler(api)
	}}

	// Metrics endpoint
	r.GET("/metrics", metrics.PrometheusHandler())

	// Graceful shutdown
	server := &http.Server{{
		Addr:    ":" + cfg.Server.Port,
		Handler: r,
	}}

	go func() {{
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {{
			log.Fatal("Failed to start server:", err)
		}}
	}}()

	// Wait for interrupt signal to gracefully shutdown
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Println("Shutting down server...")

	ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {{
		log.Fatal("Server forced to shutdown:", err)
	}}

	log.Println("Server exited")
}}
'''

    def _get_grpc_main_template(self) -> str:
        """Get main.go template for gRPC gateway projects."""
        return f'''package main

import (
	"context"
	"log"
	"net"
	"net/http"

	"{self.module_path}/internal/config"
	"{self.module_path}/internal/grpc"
	grpcHandler "{self.module_path}/internal/handler"

	"github.com/gin-gonic/gin"
	"google.golang.org/grpc"
)

func main() {{
	// Initialize configuration
	cfg := config.Load()

	// Start gRPC server
	grpcServer := grpc.NewServer()
	grpcService := grpc.NewService()
	grpcService.Register(grpcServer)

	// Start gRPC server in a goroutine
	go func() {{
		lis, err := net.Listen("tcp", ":"+cfg.GRPC.Port)
		if err != nil {{
			log.Fatal("Failed to listen for gRPC:", err)
		}}

		log.Printf("gRPC server starting on port %s", cfg.GRPC.Port)
		if err := grpcServer.Serve(lis); err != nil {{
			log.Fatal("Failed to start gRPC server:", err)
		}}
	}}()

	// Create Gin gateway
	r := gin.Default()

	// Initialize gRPC gateway handlers
	gateway := grpcHandler.NewGateway(cfg.GRPC.Address)
	gateway.RegisterRoutes(r)

	// Start HTTP gateway
	log.Printf("HTTP gateway starting on port %s", cfg.Server.Port)
	if err := r.Run(":" + cfg.Server.Port); err != nil {{
		log.Fatal("Failed to start HTTP gateway:", err)
	}}
}}
'''

    def create_config_files(self, project_type: str = "api") -> None:
        """
        Create configuration files for the project.

        Args:
            project_type: Type of project being created
        """
        # Create config struct
        config_file = self.project_path / "internal/config/config.go"
        config_file.write_text(self._get_config_template(project_type))

        # Create config files
        config_dir = self.project_path / "configs"

        # Development config
        dev_config = config_dir / "config.dev.yaml"
        dev_config.write_text(self._get_dev_config_template())

        # Production config
        prod_config = config_dir / "config.prod.yaml"
        prod_config.write_text(self._get_prod_config_template())

    def _get_config_template(self, project_type: str) -> str:
        """Get config.go template."""
        return f'''package config

import (
	"fmt"
	"os"

	"github.com/spf13/viper"
)

type Config struct {{
	Server   ServerConfig   `mapstructure:"server"`
	Database DatabaseConfig `mapstructure:"database"`
	Redis    RedisConfig    `mapstructure:"redis"`
	JWT      JWTConfig      `mapstructure:"jwt"`
	Log      LogConfig      `mapstructure:"log"`
	{self._get_additional_config(project_type)}
}}

type ServerConfig struct {{
	Port string `mapstructure:"port"`
	Mode string `mapstructure:"mode"`
}}

type DatabaseConfig struct {{
	Host     string `mapstructure:"host"`
	Port     string `mapstructure:"port"`
	User     string `mapstructure:"user"`
	Password string `mapstructure:"password"`
	DBName   string `mapstructure:"dbname"`
	SSLMode  string `mapstructure:"sslmode"`
}}

type RedisConfig struct {{
	Host     string `mapstructure:"host"`
	Port     string `mapstructure:"port"`
	Password string `mapstructure:"password"`
	DB       int    `mapstructure:"db"`
}}

type JWTConfig struct {{
	Secret     string `mapstructure:"secret"`
	Expiration int    `mapstructure:"expiration"`
}}

type LogConfig struct {{
	Level  string `mapstructure:"level"`
	Format string `mapstructure:"format"`
}}

{self._get_additional_config_structs(project_type)}

func Load() *Config {{
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	viper.AddConfigPath("./configs")
	viper.AddConfigPath(".")

	// Set environment variables
	viper.AutomaticEnv()

	// Set default values
	setDefaults()

	// Read config file
	if err := viper.ReadInConfig(); err != nil {{
		fmt.Printf("Config file not found, using defaults: %v\n", err)
	}}

	var config Config
	if err := viper.Unmarshal(&config); err != nil {{
		fmt.Printf("Error unmarshaling config: %v\n", err)
		os.Exit(1)
	}}

	return &config
}}

func setDefaults() {{
	viper.SetDefault("server.port", "8080")
	viper.SetDefault("server.mode", "debug")
	viper.SetDefault("log.level", "info")
	viper.SetDefault("log.format", "json")
	viper.SetDefault("jwt.expiration", 24) // hours
}}

{self._get_additional_config_functions(project_type)}
'''

    def _get_additional_config(self, project_type: str) -> str:
        """Get additional config fields based on project type."""
        if project_type == "microservice":
            return "Metrics MetricsConfig `mapstructure:\"metrics\"`"
        elif project_type == "grpc":
            return "GRPC GRPCConfig `mapstructure:\"grpc\"`"
        return ""

    def _get_additional_config_structs(self, project_type: str) -> str:
        """Get additional config structs based on project type."""
        if project_type == "microservice":
            return '''
type MetricsConfig struct {
	Enabled bool   `mapstructure:"enabled"`
	Port    string `mapstructure:"port"`
	Path    string `mapstructure:"path"`
}'''
        elif project_type == "grpc":
            return '''
type GRPCConfig struct {
	Port    string `mapstructure:"port"`
	Address string `mapstructure:"address"`
}'''
        return ""

    def _get_additional_config_functions(self, project_type: str) -> str:
        """Get additional config functions based on project type."""
        if project_type == "microservice":
            return '''
func (c *Config) GetMetricsPort() string {
	if c.Metrics.Port != "" {
		return c.Metrics.Port
	}
	return "9090"
}'''
        return ""

    def _get_dev_config_template(self) -> str:
        """Get development config template."""
        return '''server:
  port: "8080"
  mode: "debug"

database:
  host: "localhost"
  port: "5432"
  user: "postgres"
  password: "postgres"
  dbname: "myapp_dev"
  sslmode: "disable"

redis:
  host: "localhost"
  port: "6379"
  password: ""
  db: 0

jwt:
  secret: "your-secret-key-change-in-production"
  expiration: 24

log:
  level: "debug"
  format: "console"
'''

    def _get_prod_config_template(self) -> str:
        """Get production config template."""
        return '''server:
  port: "8080"
  mode: "release"

database:
  host: "${DB_HOST}"
  port: "${DB_PORT}"
  user: "${DB_USER}"
  password: "${DB_PASSWORD}"
  dbname: "${DB_NAME}"
  sslmode: "require"

redis:
  host: "${REDIS_HOST}"
  port: "${REDIS_PORT}"
  password: "${REDIS_PASSWORD}"
  db: 0

jwt:
  secret: "${JWT_SECRET}"
  expiration: 24

log:
  level: "info"
  format: "json"
'''

    def create_docker_files(self, project_type: str = "api") -> None:
        """
        Create Docker-related files.

        Args:
            project_type: Type of project being created
        """
        # Dockerfile
        dockerfile = self.project_path / "Dockerfile"
        dockerfile.write_text(self._get_dockerfile_template())

        # docker-compose.yml
        compose_file = self.project_path / "docker-compose.yml"
        compose_file.write_text(self._get_docker_compose_template(project_type))

        # .dockerignore
        dockerignore = self.project_path / ".dockerignore"
        dockerignore.write_text(self._get_dockerignore_template())

    def _get_dockerfile_template(self) -> str:
        """Get Dockerfile template."""
        return '''# Build stage
FROM golang:1.21-alpine AS builder

WORKDIR /app

# Install dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy source code
COPY . .

# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main cmd/server/main.go

# Final stage
FROM alpine:latest

RUN apk --no-cache add ca-certificates tzdata

WORKDIR /root/

# Copy the binary from builder stage
COPY --from=builder /app/main .

# Copy config files
COPY --from=builder /app/configs ./configs

# Expose port
EXPOSE 8080

# Run the binary
CMD ["./main"]
'''

    def _get_docker_compose_template(self, project_type: str) -> str:
        """Get docker-compose.yml template."""
        base_compose = '''version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - GIN_MODE=release
    depends_on:
      - postgres
      - redis
    volumes:
      - ./configs:/root/configs

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
'''

        if project_type == "microservice":
            base_compose += '''
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    volumes:
      - grafana_data:/var/lib/grafana

volumes:
  grafana_data:
'''

        return base_compose

    def _get_dockerignore_template(self) -> str:
        """Get .dockerignore template."""
        return '''# Git
.git
.gitignore

# Documentation
README.md
docs/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Test files
*_test.go
test/

# Build artifacts
*.exe
main
/vendor/

# Config files (sensitive data)
.env
config.prod.yaml
'''

    def create_gitignore(self) -> None:
        """Create .gitignore file."""
        gitignore_file = self.project_path / ".gitignore"
        gitignore_content = '''# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with `go test -c`
*.test

# Output of the go coverage tool
*.out

# Go workspace file
go.work

# Dependency directories
vendor/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Environment files
.env
.env.local
.env.*.local

# Config files
config.prod.yaml

# Logs
*.log
logs/

# Build output
/build/
/dist/
/bin/

# Database
*.db
*.sqlite

# Temporary files
*.tmp
*.temp

# Coverage
coverage.txt
coverage.out

# Air (live reload)
tmp/
'''
        gitignore_file.write_text(gitignore_content)

    def create_readme(self, project_type: str = "api") -> None:
        """
        Create README.md file.

        Args:
            project_type: Type of project being created
        """
        readme_file = self.project_path / "README.md"
        readme_file.write_text(self._get_readme_template(project_type))

    def _get_readme_template(self, project_type: str) -> str:
        """Get README.md template."""
        base_readme = f'''# {self.project_name}

A modern Go web application built with the Gin framework.

## Features

- ⚡ High-performance HTTP router
- 🏗️ Clean architecture with separation of concerns
- 🔧 Configuration management with Viper
- 📝 Structured logging
- 🐳 Docker support
- 🧪 Unit and integration tests
- 📊 API documentation with Swagger
- 🔒 JWT authentication
- 📈 Metrics and monitoring
'''

        if project_type == "api":
            base_readme += '''- 🔄 RESTful API design
- ✅ Input validation
- 🌐 CORS support
'''
        elif project_type == "web":
            base_readme += '''- 🎨 HTML template rendering
- 📁 Static file serving
- 🌐 Web interface
'''
        elif project_type == "microservice":
            base_readme += '''- 🏥 Health checks
- 📊 Prometheus metrics
- 🔄 Graceful shutdown
- 📋 Service discovery ready
'''
        elif project_type == "grpc":
            base_readme += '''- 🚀 gRPC server
- 🌐 HTTP/JSON gateway
- 📡 Protocol Buffers
'''

        base_readme += f'''

## Quick Start

### Prerequisites

- Go 1.21 or later
- Docker and Docker Compose
- PostgreSQL (for full functionality)
- Redis (for caching)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd {self.project_name}
```

2. Install dependencies:
```bash
go mod download
```

3. Set up environment variables:
```bash
cp configs/config.dev.yaml configs/config.yaml
# Edit configs/config.yaml with your settings
```

4. Run with Docker Compose (recommended):
```bash
docker-compose up -d
```

5. Or run locally:
```bash
go run cmd/server/main.go
```

### Development

#### Running Tests
```bash
# Run all tests
go test ./...

# Run tests with coverage
go test -cover ./...

# Generate coverage report
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out
```

#### Live Reload
```bash
# Install air
go install github.com/air-verse/air@latest

# Run with live reload
air
```

## API Documentation

Once the server is running, visit:

- Swagger UI: http://localhost:8080/swagger/index.html
- Health Check: http://localhost:8080/api/v1/health

## Configuration

The application uses YAML configuration files located in the `configs/` directory:

- `config.dev.yaml` - Development environment
- `config.prod.yaml` - Production environment

Configuration can also be set via environment variables.

## Project Structure

```
{self.project_name}/
├── cmd/server/          # Application entry point
├── internal/            # Private application code
│   ├── config/         # Configuration
│   ├── handler/        # HTTP handlers
│   ├── middleware/     # HTTP middleware
│   ├── model/          # Data models
│   ├── repository/     # Data access layer
│   └── service/        # Business logic
├── pkg/                # Public library code
├── api/                # API definitions
├── web/                # Web assets
├── configs/            # Configuration files
├── scripts/            # Build and deployment scripts
└── docs/               # Documentation
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
'''

        return base_readme

    def create_makefile(self) -> None:
        """Create Makefile for common tasks."""
        makefile = self.project_path / "Makefile"
        makefile_content = f'''.PHONY: help build run test clean docker-build docker-run docker-stop lint format

# Variables
APP_NAME := {self.project_name}
VERSION := $$(shell git describe --tags --always --dirty)
BUILD_TIME := $$(shell date +%Y-%m-%dT%H:%M:%S%z)
LDFLAGS := -ldflags "-X main.version=$$(VERSION) -X main.buildTime=$$(BUILD_TIME)"

# Help
help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {{FS = ":.*?## "}} /^[a-zA-Z_-]+:.*?## / {{printf "  %-15s %s\n", $$1, $$2}}' $$(MAKEFILE_LIST)

# Build
build: ## Build the application
	go build $$(LDFLAGS) -o bin/$$(APP_NAME) cmd/server/main.go

run: ## Run the application
	go run cmd/server/main.go

# Testing
test: ## Run tests
	go test -v ./...

test-coverage: ## Run tests with coverage
	go test -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

test-integration: ## Run integration tests
	go test -tags=integration ./test/integration/...

# Code Quality
lint: ## Run linter
	golangci-lint run

format: ## Format code
	go fmt ./...
	goimports -w .

# Docker
docker-build: ## Build Docker image
	docker build -t $$(APP_NAME):$$(VERSION) .
	docker tag $$(APP_NAME):$$(VERSION) $$(APP_NAME):latest

docker-run: ## Run with Docker Compose
	docker-compose up -d

docker-stop: ## Stop Docker Compose
	docker-compose down

docker-logs: ## Show Docker logs
	docker-compose logs -f

# Development
dev: ## Run in development mode with hot reload
	air

install-deps: ## Install development dependencies
	go install github.com/air-verse/air@latest
	go install golang.org/x/tools/cmd/goimports@latest
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

# Database
migrate-up: ## Run database migrations
	go run cmd/migrate/main.go up

migrate-down: ## Rollback database migrations
	go run cmd/migrate/main.go down

migrate-create: ## Create new migration (use name=migration_name)
	@if [ -z "$$(name)" ]; then echo "Usage: make migrate-create name=migration_name"; exit 1; fi
	migrate create -ext sql -dir migrations $$(name)

# Clean
clean: ## Clean build artifacts
	rm -rf bin/
	rm -f coverage.out coverage.html
	go clean -cache

# Install
install: build ## Install the application
	cp bin/$$(APP_NAME) $$(GOPATH)/bin/

# Release
release: clean test lint build ## Prepare a release
	@echo "Release ready: $$(APP_NAME):$$(VERSION)"
'''
        makefile.write_text(makefile_content)

    def create_basic_handlers(self, project_type: str = "api") -> None:
        """
        Create basic handler files.

        Args:
            project_type: Type of project being created
        """
        # Health handler
        health_file = self.project_path / "internal/handler/health.go"
        health_file.write_text(self._get_health_handler_template())

        # Example handler
        example_file = self.project_path / "internal/handler/example.go"
        example_file.write_text(self._get_example_handler_template())

        if project_type == "web":
            # Web handler
            web_file = self.project_path / "internal/handler/web.go"
            web_file.write_text(self._get_web_handler_template())

    def _get_health_handler_template(self) -> str:
        """Get health handler template."""
        return '''package handler

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
)

type HealthHandler struct {
	startTime time.Time
}

func NewHealthHandler(router *gin.RouterGroup) *HealthHandler {
	h := &HealthHandler{
		startTime: time.Now(),
	}

	health := router.Group("/health")
	{
		health.GET("/", h.Check)
		health.GET("/detailed", h.DetailedCheck)
	}

	return h
}

type HealthResponse struct {
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
	Uptime    string    `json:"uptime"`
	Version   string    `json:"version"`
}

func (h *HealthHandler) Check(c *gin.Context) {
	c.JSON(http.StatusOK, HealthResponse{
		Status:    "ok",
		Timestamp: time.Now(),
		Uptime:    time.Since(h.startTime).String(),
		Version:   "1.0.0",
	})
}

func (h *HealthHandler) DetailedCheck(c *gin.Context) {
	// Add more detailed health checks here
	// Database connection, external services, etc.

	c.JSON(http.StatusOK, gin.H{
		"status": "ok",
		"timestamp": time.Now(),
		"uptime": time.Since(h.startTime).String(),
		"version": "1.0.0",
		"checks": gin.H{
			"database": "ok",
			"redis": "ok",
		},
	})
}
'''

    def _get_example_handler_template(self) -> str:
        """Get example handler template."""
        return '''package handler

import (
	"net/http"
	"strconv"

	"github.com/gin-gonic/gin"
)

type ExampleHandler struct {
	// Add dependencies here (services, repositories, etc.)
}

func NewExampleHandler(router *gin.RouterGroup) *ExampleHandler {
	h := &ExampleHandler{}

	examples := router.Group("/examples")
	{
		examples.GET("/", h.GetExamples)
		examples.GET("/:id", h.GetExample)
		examples.POST("/", h.CreateExample)
		examples.PUT("/:id", h.UpdateExample)
		examples.DELETE("/:id", h.DeleteExample)
	}

	return h
}

type Example struct {
	ID    int    `json:"id"`
	Name  string `json:"name"`
	Value string `json:"value"`
}

func (h *ExampleHandler) GetExamples(c *gin.Context) {
	// Example data - replace with actual data access
	examples := []Example{
		{ID: 1, Name: "Example 1", Value: "Value 1"},
		{ID: 2, Name: "Example 2", Value: "Value 2"},
	}

	c.JSON(http.StatusOK, gin.H{
		"data": examples,
		"total": len(examples),
	})
}

func (h *ExampleHandler) GetExample(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	// Example data - replace with actual data access
	example := Example{
		ID:    id,
		Name:  "Example " + strconv.Itoa(id),
		Value: "Value " + strconv.Itoa(id),
	}

	c.JSON(http.StatusOK, gin.H{
		"data": example,
	})
}

func (h *ExampleHandler) CreateExample(c *gin.Context) {
	var req struct {
		Name  string `json:"name" binding:"required"`
		Value string `json:"value" binding:"required"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Create example - replace with actual data access
	example := Example{
		ID:    3, // Should be generated by database
		Name:  req.Name,
		Value: req.Value,
	}

	c.JSON(http.StatusCreated, gin.H{
		"data": example,
	})
}

func (h *ExampleHandler) UpdateExample(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	var req struct {
		Name  string `json:"name"`
		Value string `json:"value"`
	}

	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Update example - replace with actual data access
	example := Example{
		ID:    id,
		Name:  req.Name,
		Value: req.Value,
	}

	c.JSON(http.StatusOK, gin.H{
		"data": example,
	})
}

func (h *ExampleHandler) DeleteExample(c *gin.Context) {
	id, err := strconv.Atoi(c.Param("id"))
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid ID"})
		return
	}

	// Delete example - replace with actual data access

	c.JSON(http.StatusOK, gin.H{
		"message": "Example deleted successfully",
		"id": id,
	})
}
'''

    def _get_web_handler_template(self) -> str:
        """Get web handler template."""
        return '''package handler

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

type WebHandler struct {
	// Add dependencies here
}

func NewWebHandler() *WebHandler {
	return &WebHandler{}
}

func (h *WebHandler) Home(c *gin.Context) {
	c.HTML(http.StatusOK, "index.html", gin.H{
		"title": "Welcome to " + c.Request.Host,
	})
}

func (h *WebHandler) About(c *gin.Context) {
	c.HTML(http.StatusOK, "about.html", gin.H{
		"title": "About Us",
	})
}
'''

    def create_basic_middleware(self) -> None:
        """Create basic middleware files."""
        # Logger middleware
        logger_file = self.project_path / "internal/middleware/logger.go"
        logger_file.write_text(self._get_logger_middleware_template())

        # Recovery middleware
        recovery_file = self.project_path / "internal/middleware/recovery.go"
        recovery_file.write_text(self._get_recovery_middleware_template())

        # CORS middleware
        cors_file = self.project_path / "internal/middleware/cors.go"
        cors_file.write_text(self._get_cors_middleware_template())

    def _get_logger_middleware_template(self) -> str:
        """Get logger middleware template."""
        return '''package middleware

import (
	"fmt"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func Logger() gin.HandlerFunc {
	logger := logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})

	return func(c *gin.Context) {
		start := time.Now()
		path := c.Request.URL.Path
		raw := c.Request.URL.RawQuery

		// Process request
		c.Next()

		// Log request
		latency := time.Since(start)
		clientIP := c.ClientIP()
		method := c.Request.Method
		statusCode := c.Writer.Status()

		if raw != "" {
			path = path + "?" + raw
		}

		logger.WithFields(logrus.Fields{
			"method":     method,
			"path":       path,
			"status":     statusCode,
			"latency":    latency,
			"client_ip":  clientIP,
			"user_agent": c.Request.UserAgent(),
		}).Info("Request processed")
	}
}
'''

    def _get_recovery_middleware_template(self) -> str:
        """Get recovery middleware template."""
        return '''package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

func Recovery() gin.HandlerFunc {
	logger := logrus.New()

	return gin.CustomRecovery(func(c *gin.Context, recovered interface{}) {
		logger.WithFields(logrus.Fields{
			"error":  recovered,
			"method": c.Request.Method,
			"path":   c.Request.URL.Path,
		}).Error("Panic recovered")

		c.JSON(http.StatusInternalServerError, gin.H{
			"error": "Internal server error",
		})
	})
}
'''

    def _get_cors_middleware_template(self) -> str:
        """Get CORS middleware template."""
        return '''package middleware

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func CORS() gin.HandlerFunc {
	return func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Origin, Content-Type, Authorization")
		c.Header("Access-Control-Allow-Credentials", "true")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(http.StatusNoContent)
			return
		}

		c.Next()
	}
}
'''


def main():
    """Example usage of Go project structure creator."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python create_structure.py <project_name> [project_type]")
        sys.exit(1)

    project_name = sys.argv[1]
    project_type = sys.argv[2] if len(sys.argv) > 2 else "api"
    project_path = "."  # Current directory

    creator = GoProjectStructure(project_name, project_path)
    creator.create_directory_structure(project_type)
    creator.create_main_file(project_type)
    creator.create_config_files(project_type)
    creator.create_basic_handlers(project_type)
    creator.create_basic_middleware()
    creator.create_docker_files(project_type)
    creator.create_gitignore()
    creator.create_makefile()
    creator.create_readme(project_type)

    print(f"✅ Go project '{project_name}' created successfully!")
    print(f"📁 Location: {creator.project_path}")
    print(f"🏗️  Type: {project_type}")
    print("\nNext steps:")
    print(f"1. cd {project_name}")
    print("2. Customize configuration in configs/")
    print("3. Run: go mod tidy")
    print("4. Run: go run cmd/server/main.go")
    print("   or: docker-compose up -d")


if __name__ == "__main__":
    main()