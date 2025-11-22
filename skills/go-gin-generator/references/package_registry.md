# Go Package Registry

This document contains a comprehensive registry of commonly used Go packages for Gin web applications, organized by category.

## Web Framework

### Core Framework
- **gin-gonic/gin** - HTTP web framework written in Go
  - Import: `github.com/gin-gonic/gin`
  - Latest: v1.9.1
  - Use: Main web framework

### Middleware
- **gin-contrib/cors** - CORS middleware for Gin
  - Import: `github.com/gin-contrib/cors`
  - Latest: v1.4.0
  - Use: Cross-Origin Resource Sharing

- **gin-contrib/recovery** - Recovery middleware for Gin
  - Import: `github.com/gin-contrib/recovery`
  - Latest: v1.0.0
  - Use: Panic recovery

- **gin-contrib/static** - Static file serving
  - Import: `github.com/gin-contrib/static`
  - Latest: v1.0.2
  - Use: Static file serving

- **gin-contrib/gzip** - Gzip compression middleware
  - Import: `github.com/gin-contrib/gzip`
  - Latest: v0.0.6
  - Use: Response compression

- **gin-contrib/size** - Request size limiting middleware
  - Import: `github.com/gin-contrib/size`
  - Latest: v0.0.2
  - Use: Request size limits

- **gin-contrib/sessions** - Session management middleware
  - Import: `github.com/gin-contrib/sessions`
  - Latest: v0.0.5
  - Use: Session storage

- **gin-contrib/cache** - Cache middleware
  - Import: `github.com/gin-contrib/cache`
  - Latest: v0.2.0
  - Use: Response caching

## Database

### ORM
- **gorm** - The fantastic ORM library for Golang
  - Import: `gorm.io/gorm`
  - Latest: v1.25.4
  - Use: Object-relational mapping

- **gorm/driver/postgres** - PostgreSQL driver for GORM
  - Import: `gorm.io/driver/postgres`
  - Latest: v1.5.2
  - Use: PostgreSQL database

- **gorm/driver/mysql** - MySQL driver for GORM
  - Import: `gorm.io/driver/mysql`
  - Latest: v1.5.1
  - Use: MySQL database

- **gorm/driver/sqlite** - SQLite driver for GORM
  - Import: `gorm.io/driver/sqlite`
  - Latest: v1.5.2
  - Use: SQLite database

- **gorm/driver/sqlserver** - SQL Server driver for GORM
  - Import: `gorm.io/driver/sqlserver`
  - Latest: v1.5.1
  - Use: SQL Server database

### Database Drivers (Direct)
- **lib/pq** - Pure Go Postgres driver for database/sql
  - Import: `github.com/lib/pq`
  - Latest: v1.10.9
  - Use: PostgreSQL (database/sql)

- **go-sql-driver/mysql** - MySQL Driver for Go's database/sql package
  - Import: `github.com/go-sql-driver/mysql`
  - Latest: v1.7.1
  - Use: MySQL (database/sql)

- **mattn/go-sqlite3** - SQLite3 driver for Go
  - Import: `github.com/mattn/go-sqlite3`
  - Latest: v1.14.17
  - Use: SQLite (database/sql)

### Database Tools
- **sqlx** - general purpose extensions to golang's database/sql
  - Import: `github.com/jmoiron/sqlx`
  - Latest: v1.3.5
  - Use: Extended SQL operations

- **pgx** - PostgreSQL driver and toolkit
  - Import: `github.com/jackc/pgx/v5`
  - Latest: v5.4.3
  - Use: Advanced PostgreSQL

- **mongo-driver** - Official MongoDB driver for Go
  - Import: `go.mongodb.org/mongo-driver`
  - Latest: v1.12.1
  - Use: MongoDB database

## Authentication & Authorization

### JWT
- **golang-jwt/jwt** - JSON Web Tokens for Go
  - Import: `github.com/golang-jwt/jwt/v5`
  - Latest: v5.0.0
  - Use: JWT token handling

- **dgrijalva/jwt-go** - Legacy JWT library (deprecated)
  - Import: `github.com/dgrijalva/jwt-go`
  - Latest: v3.2.0
  - Use: Legacy projects only

### OAuth2
- **oauth2** - Go OAuth2 library
  - Import: `golang.org/x/oauth2`
  - Latest: latest
  - Use: OAuth2 authentication

- **gologin** - Go authentication chain for Go
  - Import: `github.com/dgrijalva/jwt-go`
  - Latest: v1.0.0
  - Use: OAuth providers

### Password Security
- **bcrypt** - Go bcrypt password hashing
  - Import: `golang.org/x/crypto/bcrypt`
  - Latest: latest
  - Use: Password hashing

- **argon2** - Go Argon2 password hashing
  - Import: `golang.org/x/crypto/argon2`
  - Latest: latest
  - Use: Advanced password hashing

### RBAC
- **casbin** - An authorization library that supports access control models
  - Import: `github.com/casbin/casbin/v2`
  - Latest: v2.70.0
  - Use: Role-based access control

## Configuration

### Configuration Management
- **viper** - Go configuration with fangs
  - Import: `github.com/spf13/viper`
  - Latest: v1.16.0
  - Use: Configuration files and environment variables

- **envconfig** - Go library for managing configuration data from environment variables
  - Import: `github.com/kelseyhightower/envconfig`
  - Latest: v1.4.0
  - Use: Environment variable configuration

### Flag Parsing
- **cobra** - A Commander for modern Go CLI interactions
  - Import: `github.com/spf13/cobra`
  - Latest: v1.7.0
  - Use: CLI applications

- **pflag** - POSIX-compliant flag package
  - Import: `github.com/spf13/pflag`
  - Latest: v1.0.5
  - Use: Command-line flags

## Logging

### Structured Logging
- **logrus** - Structured, pluggable logging for Go
  - Import: `github.com/sirupsen/logrus`
  - Latest: v1.9.3
  - Use: Structured logging

- **zap** - Fast, structured, leveled logging in Go
  - Import: "go.uber.org/zap"
  - Latest: v1.25.0
  - Use: High-performance logging

- **zerolog** - Zero Allocation JSON Logger
  - Import: `github.com/rs/zerolog`
  - Latest: v1.30.0
  - Use: Zero-allocation logging

### Log Aggregation
- **logrus-sentry** - Sentry hook for logrus
  - Import: `github.com/sirupsen/logrus/hooks/sentry`
  - Latest: latest
  - Use: Sentry integration

## Validation

### Input Validation
- **validator** - Go Struct and Field validation
  - Import: `github.com/go-playground/validator/v10`
  - Latest: v10.15.3
  - Use: Struct validation

- **go-playground/mold** - A general data validation and modifier library
  - Import: `github.com/go-playground/mold/v4`
  - Latest: v4.2.1
  - Use: Data modification and validation

## HTTP Client & Utilities

### HTTP Clients
- **resty** - Simple HTTP and REST client library for Go
  - Import: `github.com/go-resty/resty/v2`
  - Latest: v2.7.0
  - Use: HTTP client operations

- **httpmock** - HTTP mocking for Golang
  - Import: `github.com/jarcoal/httpmock`
  - Latest: v1.3.0
  - Use: HTTP mocking in tests

### HTTP Utilities
- **httprouter** - A high performance HTTP request router
  - Import: `github.com/julienschmidt/httprouter`
  - Latest: v1.3.0
  - Use: HTTP routing (alternative to Gin)

- **chi** - lightweight, idiomatic and composable router
  - Import: `github.com/go-chi/chi/v5`
  - Latest: v5.0.8
  - Use: HTTP routing (alternative to Gin)

## Serialization

### JSON
- **json-iterator** - A high-performance 100% compatible drop-in replacement of "encoding/json"
  - Import: `github.com/json-iterator/go`
  - Latest: v1.1.12
  - Use: Fast JSON operations

- **easyjson** - Fast JSON serializer for Go
  - Import: `github.com/mailru/easyjson`
  - Latest: v0.7.7
  - Use: High-performance JSON

### YAML
- **yaml** - YAML support for the Go language
  - Import: `gopkg.in/yaml.v3`
  - Latest: v3.0.1
  - Use: YAML operations

- **gopkg.in/yaml.v2** - YAML v2 support
  - Import: `gopkg.in/yaml.v2`
  - Latest: v2.4.0
  - Use: YAML v2 operations

## Caching

### Memory Cache
- **golang-lru** - LRU cache implementation
  - Import: `github.com/hashicorp/golang-lru`
  - Latest: v0.5.4
  - Use: LRU caching

- **bigcache** - Efficient cache for gigabytes of data written in Go
  - Import: `github.com/allegro/bigcache/v2`
  - Latest: v2.2.1
  - Use: Large-scale caching

### Redis
- **go-redis** - Type-safe Redis client for Golang
  - Import: `github.com/redis/go-redis/v9`
  - Latest: v9.0.5
  - Use: Redis client

- **redigo** - Go client for Redis database
  - Import: `github.com/gomodule/redigo/redis`
  - Latest: v1.8.19
  - Use: Redis client (alternative)

## Message Queue

### RabbitMQ
- **streadway/amqp** - Go client for AMQP 0.9.1
  - Import: `github.com/streadway/amqp`
  - Latest: v1.1.0
  - Use: RabbitMQ client

### NATS
- **nats** - Golang client for NATS
  - Import: `github.com/nats-io/nats.go`
  - Latest: v1.28.0
  - Use: NATS messaging

- **nats-jetstream** - NATS JetStream client
  - Import: `github.com/nats-io/nats.go/jetstream`
  - Latest: latest
  - Use: JetStream messaging

### Apache Kafka
- **confluent-kafka-go** - Confluent's Apache Kafka Golang client
  - Import: `github.com/confluentinc/confluent-kafka-go/v2`
  - Latest: v2.1.1
  - Use: Apache Kafka

## Testing

### Testing Framework
- **testify** - A toolkit with common assertions and mocks
  - Import: `github.com/stretchr/testify`
  - Latest: v1.8.3
  - Use: Testing assertions and mocks

### HTTP Testing
- **httptest** - Go's built-in HTTP testing utilities
  - Import: `net/http/httptest`
  - Latest: standard library
  - Use: HTTP testing

### Mock Generation
- **gomock** - GoMock is a mocking framework for Golang
  - Import: `github.com/golang/mock/gomock`
  - Latest: v1.6.0
  - Use: Mock generation

- **mockgen** - Tool for generating mock implementations
  - Import: `github.com/golang/mock/mockgen`
  - Latest: v1.6.0
  - Use: Mock code generation

### Test Coverage
- **gocov** - Code coverage analysis tool for Go
  - Import: `github.com/axw/gocov/...`
  - Latest: latest
  - Use: Coverage analysis

- **gocovmerge** - Merge multiple gocov coverage profiles
  - Import: `github.com/wadey/gocovmerge`
  - Latest: latest
  - Use: Coverage merging

## Documentation

### API Documentation
- **swaggo** - Automatically generate RESTful API documentation with Swagger 2.0
  - Import: `github.com/swaggo/swag`
  - Latest: v1.16.1
  - Use: Swagger documentation

- **swaggo/gin-swagger** - gin middleware to automatically generate RESTful API documentation
  - Import: `github.com/swaggo/gin-swagger`
  - Latest: v1.6.0
  - Use: Swagger for Gin

- **swaggo/files** - embed swagger files
  - Import: `github.com/swaggo/files`
  - Latest: v1.0.1
  - Use: Swagger file embedding

### OpenAPI
- **kin-openapi** - OpenAPI 3.0 implementation for Go
  - Import: `github.com/getkin/kin-openapi`
  - Latest: v0.119.0
  - Use: OpenAPI operations

## Monitoring & Metrics

### Metrics Collection
- **prometheus** - Prometheus instrumentation library for Go applications
  - Import: `github.com/prometheus/client_golang`
  - Latest: v1.16.0
  - Use: Prometheus metrics

- **gin-prometheus** - Prometheus metrics exporter for Gin
  - Import: `github.com/zsais/go-gin-prometheus`
  - Latest: v1.0.0
  - Use: Gin Prometheus integration

### Tracing
- **opentracing-go** - OpenTracing API for Go
  - Import: `github.com/opentracing/opentracing-go`
  - Latest: v1.2.0
  - Use: Distributed tracing

- **jaeger-client-go** - Jaeger client libraries
  - Import: `github.com/uber/jaeger-client-go`
  - Latest: v2.30.0
  - Use: Jaeger tracing

## Rate Limiting

### Rate Limiting
- **golang.org/x/time/rate** - Go's rate limiting package
  - Import: `golang.org/x/time/rate`
  - Latest: latest
  - Use: Token bucket rate limiting

- ** Tollbooth** - Rate limit HTTP requests
  - Import: `github.com/didip/tollbooth/v6`
  - Latest: v6.1.0
  - Use: HTTP rate limiting

## Utilities

### UUID Generation
- **google/uuid** - Go package for UUIDs
  - Import: `github.com/google/uuid`
  - Latest: v1.3.0
  - Use: UUID generation

- **satori/go.uuid** - UUID library for Go
  - Import: `github.com/satori/go.uuid`
  - Latest: v1.2.0
  - Use: UUID generation (alternative)

### Time Utilities
- **now** - Now is a time toolkit for golang
  - Import: `github.com/jinzhu/now`
  - Latest: v1.1.5
  - Use: Time operations

### String Utilities
- **strings** - Go's built-in string package
  - Import: `strings`
  - Latest: standard library
  - Use: String operations

- **cast** - Go package to safely cast between types
  - Import: `github.com/spf13/cast`
  - Latest: v1.5.1
  - Use: Type casting

### HTTP Utilities
- **httpexpect** - End-to-end HTTP and REST API testing for Go
  - Import: `github.com/gavv/httpexpect/v2`
  - Latest: v2.14.0
  - Use: HTTP testing

### Environment Variables
- **godotenv** - Go port of Ruby's dotenv library
  - Import: `github.com/joho/godotenv`
  - Latest: v1.4.0
  - Use: Environment file loading

## Security

### Security Headers
- **secure** - HTTP middleware for Go that facilitates some quick security wins
  - Import: `github.com/unrolled/secure`
  - Latest: v1.0.9
  - Use: Security headers

### Encryption
- **golang.org/x/crypto** - Go cryptography package
  - Import: `golang.org/x/crypto`
  - Latest: latest
  - Use: Cryptographic operations

## Development Tools

### Hot Reload
- **air** - Live reload for Go apps
  - Import: N/A (CLI tool)
  - Latest: v1.45.0
  - Use: Development live reload

### Linting
- **golangci-lint** - Fast Go linters runner
  - Import: N/A (CLI tool)
  - Latest: v1.52.2
  - Use: Code linting

### Code Formatting
- **goimports** - Updates your Go import lines, adding missing ones and removing unreferenced ones
  - Import: N/A (CLI tool)
  - Latest: latest
  - Use: Import organization

## gRPC

### gRPC Framework
- **grpc** - Go gRPC
  - Import: `google.golang.org/grpc`
  - Latest: v1.56.2
  - Use: gRPC framework

- **grpc-gateway** - gRPC to HTTP proxy generator
  - Import: `github.com/grpc-ecosystem/grpc-gateway/v2`
  - Latest: v2.15.2
  - Use: gRPC HTTP gateway

### Protocol Buffers
- **protobuf** - Go support for Google's protocol buffers
  - Import: `google.golang.org/protobuf`
  - Latest: v1.30.0
  - Use: Protocol buffer operations

- **protoc-gen-go** - Protocol buffer compiler plugin for Go
  - Import: N/A (CLI tool)
  - Latest: v1.30.0
  - Use: Protocol buffer generation

## Email

### Email Clients
- **gomail** - A simple and powerful email package for Go
  - Import: `github.com/go-gomail/gomail`
  - Latest: v2.0.0-20160411212932-81ebce5c23df
  - Use: SMTP email sending

- **hermes** - Gomail-inspired, clean email generation for Go
  - Import: `github.com/matcornic/hermes/v2`
  - Latest: v2.1.0
  - Use: HTML email generation

## File Processing

### File Upload
- **multipart** - Go's built-in multipart package
  - Import: `mime/multipart`
  - Latest: standard library
  - Use: Multipart form handling

### Image Processing
- **imaging** - Simple image processing for Go
  - Import: `github.com/disintegration/imaging`
  - Latest: v1.6.2
  - Use: Image operations

### PDF Processing
- **unidoc/unipdf** - A PDF library for Go
  - Import: `github.com/unidoc/unipdf/v3`
  - Latest: v3.23.0
  - Use: PDF generation and processing

## Date & Time

### Time Parsing
- **now** - A time toolkit for golang
  - Import: `github.com/jinzhu/now`
  - Latest: v1.1.5
  - Use: Time utilities

### Timezones
- **timezone** - IANA Time Zone database for Go
  - Import: `github.com/evanoberholster/timezoneLookup`
  - Latest: latest
  - Use: Timezone handling

## Utility Libraries

### Collections
- **go-funk** - A modern Go utility library
  - Import: `github.com/thoas/go-funk`
  - Latest: v0.1.0
  - Use: Functional programming utilities

### Reflection
- **copier** - Go copier: copy value from struct to struct and more
  - Import: `github.com/jinzhu/copier`
  - Latest: v2.6.0
  - Use: Struct copying

### Maps
- **mapstructure** - Go library for decoding generic map values into native Go structures
  - Import: `github.com/mitchellh/mapstructure`
  - Latest: v1.5.0
  - Use: Map to struct conversion

## Template Engines

### HTML Templates
- **template** - Go's built-in template package
  - Import: `html/template`
  - Latest: standard library
  - Use: HTML template rendering

- **quicktemplate** - Fast, powerful, yet easy to use template engine for Go
  - Import: `github.com/valyala/quicktemplate`
  - Latest: v1.7.0
  - Use: High-performance templates

### Alternative Template Engines
- **pongo2** - Django-syntax like template-engine for Go
  - Import: `github.com/flosch/pongo2/v4`
  - Latest: v4.0.2
  - Use: Django-like templates

## Development Environment Setup

### Installation Commands
```bash
# Core dependencies
go get github.com/gin-gonic/gin
go get github.com/spf13/viper
go get github.com/sirupsen/logrus
go get github.com/go-playground/validator/v10

# Database
go get gorm.io/gorm
go get gorm.io/driver/postgres

# Authentication
go get github.com/golang-jwt/jwt/v5
go get golang.org/x/crypto/bcrypt

# Development tools
go install github.com/air-verse/air@latest
go install github.com/swaggo/swag/cmd/swag@latest
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
go install golang.org/x/tools/cmd/goimports@latest
```

### Version Management
Always pin to specific versions for production applications:

```go
// go.mod
require (
    github.com/gin-gonic/gin v1.9.1
    github.com/spf13/viper v1.16.0
    github.com/sirupsen/logrus v1.9.3
    gorm.io/gorm v1.25.4
    github.com/golang-jwt/jwt/v5 v5.0.0
)
```