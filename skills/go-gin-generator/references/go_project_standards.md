# Go Project Standards and Best Practices

This document outlines the standard practices and conventions for Go projects, specifically tailored for web applications using the Gin framework.

## Project Structure

Based on [golang-standards/project-layout](https://github.com/golang-standards/project-layout):

```
project-name/
├── cmd/                    # Main applications for this project
│   └── server/            # Server application entry point
│       └── main.go        # Main application file
├── internal/              # Private application code
│   ├── config/           # Configuration management
│   ├── handler/          # HTTP request handlers (controllers)
│   ├── middleware/       # HTTP middleware
│   ├── model/           # Data models and structures
│   ├── repository/      # Data access layer
│   ├── service/         # Business logic layer
│   └── validator/       # Input validation
├── pkg/                   # Public library code
│   └── logger/          # Shared logging utilities
├── api/                   # API definitions (OpenAPI/Swagger)
│   └── swagger/          # Swagger documentation
├── web/                   # Web application assets
│   ├── static/          # CSS, JavaScript, images
│   └── templates/       # HTML templates
├── configs/               # Configuration files
├── scripts/              # Build and deployment scripts
├── docs/                 # Documentation
├── build/                # Build output and CI configuration
├── deployments/          # Deployment configurations
├── init/                 # System init configurations
├── test/                 # Additional tests
│   ├── e2e/             # End-to-end tests
│   └── integration/     # Integration tests
├── go.mod                # Go module definition
├── go.sum                # Go module checksums
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose configuration
├── Makefile              # Build automation
├── README.md             # Project documentation
└── .gitignore           # Git ignore rules
```

## Naming Conventions

### Package Names
- Use short, lowercase, single-word names when possible
- Don't use underscores or camelCase
- Be descriptive but concise
- Example: `config`, `handler`, `service`

### File Names
- Use lowercase with underscores for multi-word files
- Match the package name for the main file
- Example: `user_service.go`, `config_manager.go`

### Struct and Interface Names
- Use PascalCase (CamelCase)
- Use descriptive names
- Interfaces should often end with `er` suffix
- Example: `UserService`, `DatabaseRepository`, `Handler`

### Function and Variable Names
- Use camelCase for local variables and functions
- Use camelCase for exported names
- Use short names for local variables, descriptive names for exported ones
- Example: `getUserByID`, `db`, `userService`

### Constants
- Use UPPER_SNAKE_CASE for constants
- Group related constants
- Example: `DEFAULT_TIMEOUT`, `MAX_CONNECTIONS`

## Code Organization

### Package Structure
- **cmd**: Main application entry points
- **internal**: Private application code that shouldn't be imported by other projects
- **pkg**: Public library code that can be imported by other projects
- **api**: API definitions, protocol buffer files
- **web**: Web application assets
- **configs**: Configuration files
- **scripts**: Build, install, analysis, etc. scripts
- **docs**: Design and user documentation
- **test**: Additional external test applications

### Layer Architecture
```
Handler Layer (Controllers)
    ↓
Service Layer (Business Logic)
    ↓
Repository Layer (Data Access)
    ↓
Database/External Services
```

### Dependency Direction
- Dependencies should point inward
- `cmd` → `internal` → `pkg`
- Never have circular dependencies
- `internal` packages can import other `internal` packages
- `pkg` packages should be independent

## Error Handling

### Error Types
```go
// Custom error type
type ValidationError struct {
    Field   string
    Message string
}

func (e ValidationError) Error() string {
    return fmt.Sprintf("validation error in field %s: %s", e.Field, e.Message)
}

// Error wrapping
if err != nil {
    return fmt.Errorf("failed to create user: %w", err)
}
```

### Error Return Patterns
- Always return errors as the last return value
- Use `error` type, not custom types for most cases
- Handle errors immediately or wrap with context

```go
// Good
user, err := userService.GetUser(id)
if err != nil {
    return nil, fmt.Errorf("failed to get user %d: %w", id, err)
}

// Bad - ignoring error
user, _ := userService.GetUser(id)
```

## Configuration Management

### Configuration Structure
```go
type Config struct {
    Server   ServerConfig   `mapstructure:"server"`
    Database DatabaseConfig `mapstructure:"database"`
    Redis    RedisConfig    `mapstructure:"redis"`
    JWT      JWTConfig      `mapstructure:"jwt"`
    Log      LogConfig      `mapstructure:"log"`
}

type ServerConfig struct {
    Port string `mapstructure:"port"`
    Mode string `mapstructure:"mode"`
    Host string `mapstructure:"host"`
}
```

### Environment Variables
- Use environment variables for sensitive data
- Use configuration files for non-sensitive defaults
- Support multiple environments (dev, staging, prod)

## Logging

### Logging Levels
- **Debug**: Detailed information for debugging
- **Info**: General information about application flow
- **Warn**: Unexpected behavior that doesn't stop the application
- **Error**: Error events that might still allow the application to continue
- **Fatal**: Very severe error events that will presumably lead the application to abort

### Structured Logging
```go
logger.WithFields(logrus.Fields{
    "user_id":  userID,
    "action":   "create_order",
    "duration": time.Since(start),
}).Info("Order created successfully")
```

## Testing

### Test Organization
- Unit tests: `*_test.go` files in the same package
- Integration tests: `test/integration/` directory
- End-to-end tests: `test/e2e/` directory
- Test utilities: `testutils/` package

### Test Naming
```go
func TestUserService_GetUser_Success(t *testing.T) { ... }
func TestUserService_GetUser_NotFound(t *testing.T) { ... }
func TestUserService_CreateUser_ValidationError(t *testing.T) { ... }
```

### Table-Driven Tests
```go
func TestUserService_ValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"invalid format", "invalid-email", true},
        {"empty", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := userService.ValidateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateEmail() error = %v, wantErr %v", err, tt.wantErr)
            }
        })
    }
}
```

## Database Practices

### Repository Pattern
```go
type UserRepository interface {
    Create(ctx context.Context, user *User) error
    GetByID(ctx context.Context, id int64) (*User, error)
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int64) error
    List(ctx context.Context, filter UserFilter) ([]*User, error)
}
```

### Database Transactions
```go
func (s *UserService) TransferMoney(fromID, toID int64, amount float64) error {
    return s.repo.WithTransaction(func(tx *sql.Tx) error {
        // Deduct from sender
        if err := s.repo.UpdateBalance(tx, fromID, -amount); err != nil {
            return err
        }

        // Add to receiver
        if err := s.repo.UpdateBalance(tx, toID, amount); err != nil {
            return err
        }

        return nil
    })
}
```

## HTTP Handler Best Practices

### Handler Structure
```go
func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    user, err := h.userService.CreateUser(c.Request.Context(), req)
    if err != nil {
        // Handle different error types
        if isValidationError(err) {
            c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
            return
        }

        c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
        return
    }

    c.JSON(http.StatusCreated, gin.H{"data": user})
}
```

### Request/Response Structures
```go
type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=2,max=100"`
    Email string `json:"email" binding:"required,email"`
}

type UserResponse struct {
    ID        int64     `json:"id"`
    Name      string    `json:"name"`
    Email     string    `json:"email"`
    CreatedAt time.Time `json:"created_at"`
    UpdatedAt time.Time `json:"updated_at"`
}
```

## Security Best Practices

### Input Validation
- Validate all user inputs
- Use parameterized queries for database operations
- Sanitize data before rendering in templates

### Authentication & Authorization
```go
// JWT Middleware
func AuthMiddleware(secretKey string) gin.HandlerFunc {
    return func(c *gin.Context) {
        tokenString := c.GetHeader("Authorization")
        if tokenString == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header required"})
            c.Abort()
            return
        }

        token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
            return []byte(secretKey), nil
        })

        if err != nil || !token.Valid {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
            c.Abort()
            return
        }

        c.Next()
    }
}
```

### CORS Configuration
- Configure CORS appropriately for your use case
- Avoid allowing all origins in production
- Use specific headers and methods

## Performance Optimization

### Database Optimization
- Use connection pooling
- Implement proper indexing
- Use prepared statements
- Consider caching for frequently accessed data

### Memory Management
- Reuse objects when possible
- Use object pools for frequently allocated objects
- Profile memory usage with `pprof`

### HTTP Performance
- Use middleware for gzip compression
- Implement proper HTTP caching
- Use streaming for large responses

## Deployment

### Docker Best Practices
- Use multi-stage builds
- Minimize image size
- Use specific versions, not `latest`
- Don't run as root user

### Environment Configuration
- Use environment variables for configuration
- Separate secrets from configuration
- Support multiple environments

## Monitoring and Observability

### Metrics
- Track request latency, error rates, and throughput
- Use Prometheus for metrics collection
- Implement custom business metrics

### Health Checks
- Implement health check endpoints
- Check dependencies (database, Redis, external APIs)
- Return appropriate HTTP status codes

### Logging
- Use structured logging
- Include correlation IDs for request tracing
- Log at appropriate levels

## Resources

### Official Go Documentation
- [Effective Go](https://golang.org/doc/effective_go.html)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Go Package Naming Conventions](https://blog.golang.org/package-names)

### Web Development
- [Gin Framework Documentation](https://gin-gonic.com/docs/)
- [Go Web Examples](https://github.com/golang/go/wiki/WebApp)

### Testing
- [Testing in Go](https://golang.org/pkg/testing/)
- [Testify](https://github.com/stretchr/testify)

### Security
- [Go Security Checklist](https://github.com/Checkmarx/Go-SCP)
- [OWASP Go Secure Coding Practices](https://owasp.org/www-project-go-secure-coding-practices/)