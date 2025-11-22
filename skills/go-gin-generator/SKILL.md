---
name: go-gin-generator
description: Generate production-ready Go projects using the Gin framework with modern best practices, multiple templates, database integration, authentication, and comprehensive features for building scalable web applications and microservices.
license: MIT
---

# Go Gin Project Generator

This skill should be used when you need to create a new Go web application using the Gin framework. It generates complete, production-ready projects with proper structure, dependencies, configuration, and development tools.

## When to Use This Skill

Use this skill in these scenarios:

1. **Starting a new Go web project** - Generate a complete project structure with best practices
2. **Building REST APIs** - Create API-focused applications with proper routing and handlers
3. **Developing web applications** - Generate full-stack web apps with templates and static assets
4. **Creating microservices** - Build microservice-oriented applications with health checks and metrics
5. **Setting up gRPC services** - Generate gRPC services with HTTP gateway
6. **Rapid prototyping** - Quickly scaffold projects with common features pre-configured

## Quick Start

### Basic Project Generation

To generate a Go Gin project:

1. **Interactive Mode** (Recommended for beginners):
```bash
skill: "go-gin-generator" --interactive
```

2. **Command Line Mode** (For automation):
```bash
skill: "go-gin-generator" project-name -t api -m github.com/username/project
```

3. **Configuration File Mode** (For reproducible builds):
```bash
skill: "go-gin-generator" -c config.json
```

## Project Types

### 1. REST API (`api`)
- HTTP RESTful API with JSON responses
- JWT authentication support
- API documentation with Swagger
- Input validation and error handling
- Database integration (PostgreSQL, MySQL, SQLite)

**Use when**: Building backend APIs for mobile/web apps

### 2. Web Application (`web`)
- Full web application with HTML templates
- Static asset serving (CSS, JS, images)
- Session management
- Template rendering with Gin
- Frontend integration ready

**Use when**: Building traditional server-rendered web applications

### 3. Microservice (`microservice`)
- Health check endpoints
- Prometheus metrics
- Structured logging
- Container-ready configuration
- Service discovery friendly
- Graceful shutdown support

**Use when**: Building microservice architecture components

### 4. gRPC Service (`grpc`)
- gRPC server implementation
- HTTP/JSON gateway
- Protocol buffer definitions
- Service-to-service communication
- High-performance APIs

**Use when**: Building high-performance service-to-service APIs

## Core Capabilities

### 1. Project Structure Generation

The skill creates a professional project structure following Go best practices:

```
project-name/
├── cmd/server/              # Application entry point
├── internal/                # Private application code
│   ├── config/             # Configuration management
│   ├── handler/            # HTTP request handlers
│   ├── middleware/         # HTTP middleware
│   ├── model/              # Data models and structures
│   ├── repository/         # Data access layer
│   └── service/            # Business logic layer
├── pkg/                     # Public library code
├── api/                     # API definitions (OpenAPI/Swagger)
├── web/                     # Web application assets
├── configs/                 # Configuration files
├── scripts/                 # Build and deployment scripts
├── docs/                    # Documentation
├── go.mod                   # Go module definition
├── Dockerfile               # Docker configuration
├── Makefile                 # Build automation
└── README.md                # Project documentation
```

### 2. Dynamic Version Management

The skill automatically queries and uses the latest stable versions:

- **Gin Framework**: Queries GitHub API for latest release
- **Dependencies**: Fetches latest versions from Go proxy
- **Go Version**: Uses latest stable Go version
- **No Hardcoded Versions**: Always up-to-date with security patches

### 3. Smart Dependency Management

Manages Go dependencies using proper `go mod` commands:

- **Never edits go.mod directly** - Uses `go get`, `go mod tidy`
- **Version Pinning**: Locks to specific versions for stability
- **Dependency Resolution**: Handles transitive dependencies
- **Security Updates**: Automatic vulnerability checking

### 4. Database Integration

Support for multiple database systems:

- **PostgreSQL**: Production-ready with connection pooling
- **MySQL**: Full-featured MySQL support
- **SQLite**: Lightweight file-based database
- **GORM Integration**: Object-relational mapping
- **Migration Support**: Database schema management

### 5. Authentication & Security

Built-in security features:

- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt for password security
- **CORS Support**: Cross-origin resource sharing
- **Input Validation**: Request validation and sanitization
- **Security Headers**: Common security best practices

### 6. Development Tools Integration

Comprehensive development toolchain:

- **Air Live Reload**: Automatic server restart on code changes
- **Testing Framework**: Unit and integration tests
- **Linting**: golangci-lint for code quality
- **Documentation**: Swagger/OpenAPI auto-generation
- **Docker Support**: Multi-stage Docker builds

## Usage Examples

### Example 1: Basic REST API

```bash
skill: "go-gin-generator" myapi -t api -m github.com/user/myapi
```

This creates:
- REST API with JWT authentication
- PostgreSQL database integration
- Swagger documentation
- Docker configuration
- Comprehensive testing setup

### Example 2: Web Application

```bash
skill: "go-gin-generator" blog -t web -m github.com/user/blog
```

This creates:
- Full-stack web application
- HTML template rendering
- Static asset serving
- User authentication system
- Session management

### Example 3: Microservice

```bash
skill: "go-gin-generator" user-service -t microservice -m github.com/user/user-service
```

This creates:
- Microservice with health checks
- Prometheus metrics
- Structured logging
- Docker multi-stage build
- Graceful shutdown

## Configuration Options

### Database Configuration

```json
{
  "database": {
    "enabled": true,
    "type": "postgres",
    "connection_string": "postgres://user:pass@localhost/db"
  }
}
```

### Authentication Configuration

```json
{
  "auth": {
    "enabled": true,
    "type": "jwt",
    "secret": "your-secret-key"
  }
}
```

### Logging Configuration

```json
{
  "logging": {
    "library": "logrus",
    "level": "info",
    "format": "json"
  }
}
```

## Generated Features

### 1. Middleware Stack

- **Logger**: Structured request logging
- **Recovery**: Panic recovery with proper error handling
- **CORS**: Configurable CORS support
- **Rate Limiting**: Request rate limiting (optional)
- **Metrics**: Prometheus metrics collection (microservices)

### 2. API Documentation

Automatic Swagger/OpenAPI generation:

- **Route Documentation**: Auto-generated from handler comments
- **Model Schemas**: JSON schema definitions
- **Interactive UI**: Swagger UI for API testing
- **Code Generation**: Client SDK generation support

### 3. Testing Setup

Comprehensive testing configuration:

- **Unit Tests**: Handler and service layer tests
- **Integration Tests**: Database and API integration tests
- **Test Utilities**: Helper functions for testing
- **Mock Generation**: Automated mock creation
- **Coverage Reports**: Code coverage analysis

### 4. Development Environment

Ready-to-use development setup:

- **Environment Variables**: `.env` file support
- **Configuration Files**: YAML-based configuration
- **Live Reload**: Automatic server restart on changes
- **Debug Support**: Debug configuration and logging
- **IDE Integration**: VS Code and GoLand support

## Scripts and Automation

### Available Scripts

The skill generates several automation scripts in the `scripts/` directory:

1. **`scripts/query_versions.py`**: Queries latest package versions
2. **`scripts/create_structure.py`**: Creates project directory structure
3. **`scripts/setup_dependencies.py`**: Manages Go module dependencies
4. **`scripts/init_project.py`**: Main project initialization orchestration

### Build Targets

Generated Makefile includes these targets:

```makefile
make help          # Show all available commands
make build         # Build the application
make run           # Run the application
make test          # Run tests
make test-coverage # Run tests with coverage
make lint          # Run linter
make docker-build  # Build Docker image
make clean         # Clean build artifacts
```

## Reference Materials

The skill includes comprehensive reference documentation:

### `references/go_project_standards.md`
- Go project structure best practices
- Naming conventions and code organization
- Error handling patterns
- Testing strategies
- Performance optimization

### `references/gin_best_practices.md`
- Gin framework usage patterns
- Middleware implementation
- Handler organization
- Security best practices
- Performance optimization

### `references/package_registry.md`
- Comprehensive list of Go packages
- Usage examples and import paths
- Version recommendations
- Alternative package options
- Installation instructions

## Advanced Usage

### Custom Templates

For projects requiring custom templates:

1. Create custom template files in `assets/templates/`
2. Modify the structure creation script
3. Add template-specific logic to handlers

### Additional Packages

To include additional Go packages:

1. Add package to `package_registry.md`
2. Update dependency configuration
3. Add version query logic
4. Include in project templates

### Integration Examples

**Database Integration**:
```bash
# Project with PostgreSQL and Redis
skill: "go-gin-generator" myproject -t api --database=postgres --cache=redis
```

**Full-Stack Application**:
```bash
# Web app with frontend assets
skill: "go-gin-generator" myapp -t web --frontend=react --auth=jwt
```

**Microservice Suite**:
```bash
# Multiple related services
skill: "go-gin-generator" user-service -t microservice
skill: "go-gin-generator" order-service -t microservice
skill: "go-gin-generator" notification-service -t microservice
```

## Troubleshooting

### Common Issues

1. **Go Version Compatibility**: Ensure Go 1.21+ is installed
2. **Network Issues**: Check internet connection for version queries
3. **Permission Errors**: Ensure write permissions for project directory
4. **Module Conflicts**: Clean module cache with `go clean -modcache`

### Getting Help

1. **Check Logs**: Review generated application logs
2. **Version Information**: Check Go and Gin versions with `go version`
3. **Documentation**: Reference included documentation files
4. **Community**: Check Gin framework GitHub discussions

## Best Practices

### For Generated Projects

1. **Customize Configuration**: Update configuration files for your environment
2. **Security**: Update JWT secrets and database credentials
3. **Testing**: Add comprehensive tests for business logic
4. **Documentation**: Update API documentation as you add endpoints
5. **Monitoring**: Add application-specific metrics and logging

### For Production Deployment

1. **Environment Variables**: Use environment variables for sensitive data
2. **Database Security**: Use connection pooling and proper indexing
3. **Load Balancing**: Configure health checks and load balancers
4. **Monitoring**: Set up logging and monitoring
5. **Security**: Regular dependency updates and security scanning


This skill provides a complete foundation for professional Go web development using the Gin framework, enabling rapid development while maintaining high code quality and best practices.