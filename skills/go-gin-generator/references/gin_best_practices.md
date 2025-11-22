# Gin Framework Best Practices

This document outlines best practices and patterns for building web applications with the Gin framework in Go.

## Core Concepts

### Router Setup
```go
// Good: Create router with proper middleware
r := gin.New()  // Use gin.New() instead of gin.Default() for custom middleware

// Add essential middleware
r.Use(gin.Recovery())
r.Use(middleware.Logger())
r.Use(middleware.CORS())

// Add middleware only to specific routes
api := r.Group("/api/v1")
api.Use(middleware.Auth())
{
    api.GET("/users", userHandler.GetUsers)
    api.POST("/users", userHandler.CreateUser)
}
```

### Handler Organization
```go
// Good: Struct-based handlers with dependency injection
type UserHandler struct {
    userService UserService
    logger      *logrus.Logger
}

func NewUserHandler(userService UserService, logger *logrus.Logger) *UserHandler {
    return &UserHandler{
        userService: userService,
        logger:      logger,
    }
}

func (h *UserHandler) GetUser(c *gin.Context) {
    id, err := strconv.ParseInt(c.Param("id"), 10, 64)
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid user ID"})
        return
    }

    user, err := h.userService.GetUser(c.Request.Context(), id)
    if err != nil {
        if errors.Is(err, ErrUserNotFound) {
            c.JSON(http.StatusNotFound, gin.H{"error": "User not found"})
            return
        }

        h.logger.WithError(err).Error("Failed to get user")
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Internal server error"})
        return
    }

    c.JSON(http.StatusOK, gin.H{"data": user})
}
```

## Middleware Patterns

### Custom Middleware
```go
// Request ID Middleware
func RequestID() gin.HandlerFunc {
    return func(c *gin.Context) {
        requestID := c.GetHeader("X-Request-ID")
        if requestID == "" {
            requestID = generateUUID()
        }

        c.Set("request_id", requestID)
        c.Header("X-Request-ID", requestID)
        c.Next()
    }
}

// Rate Limiting Middleware
func RateLimiting(limit int, window time.Duration) gin.HandlerFunc {
    limiter := rate.NewLimiter(rate.Every(window/time.Duration(limit)), limit)

    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.JSON(http.StatusTooManyRequests, gin.H{
                "error": "Rate limit exceeded",
            })
            c.Abort()
            return
        }
        c.Next()
    }
}
```

### Authentication Middleware
```go
func AuthMiddleware(secretKey string) gin.HandlerFunc {
    return func(c *gin.Context) {
        authHeader := c.GetHeader("Authorization")
        if authHeader == "" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Authorization header required"})
            c.Abort()
            return
        }

        // Extract token from "Bearer <token>"
        tokenParts := strings.Split(authHeader, " ")
        if len(tokenParts) != 2 || tokenParts[0] != "Bearer" {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid authorization format"})
            c.Abort()
            return
        }

        token, err := jwt.Parse(tokenParts[1], func(token *jwt.Token) (interface{}, error) {
            if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
                return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
            }
            return []byte(secretKey), nil
        })

        if err != nil || !token.Valid {
            c.JSON(http.StatusUnauthorized, gin.H{"error": "Invalid token"})
            c.Abort()
            return
        }

        // Extract claims and set in context
        if claims, ok := token.Claims.(jwt.MapClaims); ok {
            c.Set("user_id", int64(claims["user_id"].(float64)))
            c.Set("username", claims["username"].(string))
        }

        c.Next()
    }
}
```

## Error Handling

### Consistent Error Responses
```go
// Standard error response structure
type ErrorResponse struct {
    Error   string `json:"error"`
    Code    int    `json:"code"`
    Details string `json:"details,omitempty"`
}

// Custom error types
type APIError struct {
    StatusCode int
    Message    string
    Details    string
}

func (e APIError) Error() string {
    return e.Message
}

// Error handling middleware
func ErrorMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()

        // Handle any errors that occurred during request processing
        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err

            var apiErr APIError
            if errors.As(err, &apiErr) {
                c.JSON(apiErr.StatusCode, ErrorResponse{
                    Error:   apiErr.Message,
                    Code:    apiErr.StatusCode,
                    Details: apiErr.Details,
                })
            } else {
                c.JSON(http.StatusInternalServerError, ErrorResponse{
                    Error:   "Internal server error",
                    Code:    http.StatusInternalServerError,
                })
            }
        }
    }
}
```

### Validation Errors
```go
// Custom validation response
func HandleValidationError(c *gin.Context, err error) {
    var validationErrors []string

    if validatorErrs, ok := err.(validator.ValidationErrors); ok {
        for _, e := range validatorErrs {
            validationErrors = append(validationErrors, fmt.Sprintf(
                "%s is required or invalid",
                e.Field(),
            ))
        }
    }

    c.JSON(http.StatusBadRequest, ErrorResponse{
        Error:   "Validation failed",
        Code:    http.StatusBadRequest,
        Details: strings.Join(validationErrors, ", "),
    })
}
```

## Request/Response Patterns

### Request Binding
```go
type CreateUserRequest struct {
    Name     string `json:"name" binding:"required,min=2,max=100"`
    Email    string `json:"email" binding:"required,email"`
    Password string `json:"password" binding:"required,min=8"`
    Age      int    `json:"age" binding:"min=0,max=120"`
}

func (h *UserHandler) CreateUser(c *gin.Context) {
    var req CreateUserRequest

    // Bind request body with validation
    if err := c.ShouldBindJSON(&req); err != nil {
        HandleValidationError(c, err)
        return
    }

    // Process request
    user, err := h.userService.CreateUser(c.Request.Context(), req)
    if err != nil {
        HandleError(c, err)
        return
    }

    c.JSON(http.StatusCreated, gin.H{"data": user})
}
```

### Response Consistency
```go
type APIResponse struct {
    Data    interface{} `json:"data,omitempty"`
    Message string      `json:"message,omitempty"`
    Meta    *Meta       `json:"meta,omitempty"`
}

type Meta struct {
    Page       int `json:"page"`
    Limit      int `json:"limit"`
    Total      int `json:"total"`
    TotalPages int `json:"total_pages"`
}

func SendJSON(c *gin.Context, statusCode int, data interface{}) {
    c.JSON(statusCode, APIResponse{Data: data})
}

func SendPaginatedJSON(c *gin.Context, data interface{}, meta Meta) {
    c.JSON(http.StatusOK, APIResponse{
        Data: data,
        Meta: &meta,
    })
}
```

## Database Integration

### GORM with Gin
```go
// Database middleware
func DatabaseMiddleware(db *gorm.DB) gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Set("db", db)
        c.Next()
    }
}

// Usage in handler
func (h *UserHandler) GetUsers(c *gin.Context) {
    db, exists := c.Get("db")
    if !exists {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Database not available"})
        return
    }

    var users []User
    if err := db.Find(&users).Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to fetch users"})
        return
    }

    c.JSON(http.StatusOK, gin.H{"data": users})
}
```

### Transaction Support
```go
func (h *OrderHandler) CreateOrder(c *gin.Context) {
    db, _ := c.Get("db")
    gormDB := db.(*gorm.DB)

    // Start transaction
    tx := gormDB.Begin()

    // Create order
    order := Order{ /* ... */ }
    if err := tx.Create(&order).Error; err != nil {
        tx.Rollback()
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to create order"})
        return
    }

    // Update inventory
    if err := tx.Model(&Product{}).Where("id = ?", productID).
       Update("quantity", gorm.Expr("quantity - ?", quantity)).Error; err != nil {
        tx.Rollback()
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to update inventory"})
        return
    }

    // Commit transaction
    if err := tx.Commit().Error; err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to commit transaction"})
        return
    }

    c.JSON(http.StatusCreated, gin.H{"data": order})
}
```

## File Upload Handling

### Single File Upload
```go
func (h *FileHandler) UploadFile(c *gin.Context) {
    file, err := c.FormFile("file")
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "No file uploaded"})
        return
    }

    // Validate file size (max 10MB)
    if file.Size > 10<<20 {
        c.JSON(http.StatusBadRequest, gin.H{"error": "File too large"})
        return
    }

    // Validate file type
    if !isValidFileType(file.Header.Get("Content-Type")) {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid file type"})
        return
    }

    // Generate unique filename
    filename := generateUniqueFilename(file.Filename)
    filepath := filepath.Join("uploads", filename)

    // Save file
    if err := c.SaveUploadedFile(file, filepath); err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save file"})
        return
    }

    c.JSON(http.StatusOK, gin.H{
        "filename": filename,
        "size":     file.Size,
        "url":      "/uploads/" + filename,
    })
}
```

### Multiple File Upload
```go
func (h *FileHandler) UploadMultipleFiles(c *gin.Context) {
    form, err := c.MultipartForm()
    if err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to parse multipart form"})
        return
    }

    files := form.File["files"]
    if len(files) == 0 {
        c.JSON(http.StatusBadRequest, gin.H{"error": "No files uploaded"})
        return
    }

    var uploadedFiles []map[string]interface{}

    for _, file := range files {
        filename := generateUniqueFilename(file.Filename)
        filepath := filepath.Join("uploads", filename)

        if err := c.SaveUploadedFile(file, filepath); err != nil {
            c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to save file: " + file.Filename})
            return
        }

        uploadedFiles = append(uploadedFiles, map[string]interface{}{
            "filename": filename,
            "size":     file.Size,
            "url":      "/uploads/" + filename,
        })
    }

    c.JSON(http.StatusOK, gin.H{"files": uploadedFiles})
}
```

## Caching Strategies

### Memory Cache
```go
// Simple in-memory cache
type Cache struct {
    store map[string]interface{}
    mu    sync.RWMutex
}

func NewCache() *Cache {
    return &Cache{
        store: make(map[string]interface{}),
    }
}

func (c *Cache) Set(key string, value interface{}, duration time.Duration) {
    c.mu.Lock()
    defer c.mu.Unlock()

    c.store[key] = value

    // Auto-expire
    time.AfterFunc(duration, func() {
        c.Delete(key)
    })
}

func (c *Cache) Get(key string) (interface{}, bool) {
    c.mu.RLock()
    defer c.mu.RUnlock()

    value, exists := c.store[key]
    return value, exists
}

// Cache middleware
func CacheMiddleware(cache *Cache, duration time.Duration) gin.HandlerFunc {
    return func(c *gin.Context) {
        // Only cache GET requests
        if c.Request.Method != "GET" {
            c.Next()
            return
        }

        cacheKey := c.Request.URL.String()

        // Try to get from cache
        if cached, exists := cache.Get(cacheKey); exists {
            c.JSON(http.StatusOK, cached)
            c.Abort()
            return
        }

        // Store response writer to capture response
        writer := &responseWriter{ResponseWriter: c.Writer, body: &bytes.Buffer{}}
        c.Writer = writer

        c.Next()

        // Cache successful responses
        if c.Writer.Status() == http.StatusOK {
            var response interface{}
            json.Unmarshal(writer.body.Bytes(), &response)
            cache.Set(cacheKey, response, duration)
        }
    }
}
```

## WebSocket Support

### WebSocket Handler
```go
func (h *WebSocketHandler) HandleWebSocket(c *gin.Context) {
    upgrader := websocket.Upgrader{
        CheckOrigin: func(r *http.Request) bool {
            return true // Configure for production
        },
    }

    conn, err := upgrader.Upgrade(c.Writer, c.Request, nil)
    if err != nil {
        c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to upgrade connection"})
        return
    }
    defer conn.Close()

    // Handle WebSocket connection
    for {
        messageType, p, err := conn.ReadMessage()
        if err != nil {
            break
        }

        // Process message
        response := h.processMessage(p)

        // Send response
        if err := conn.WriteMessage(messageType, response); err != nil {
            break
        }
    }
}
```

## Testing Gin Applications

### Unit Testing Handlers
```go
func TestUserHandler_GetUser(t *testing.T) {
    // Setup
    gin.SetMode(gin.TestMode)

    mockUserService := &MockUserService{}
    logger := logrus.New()
    handler := NewUserHandler(mockUserService, logger)

    router := gin.New()
    router.GET("/users/:id", handler.GetUser)

    // Test case: User found
    mockUserService.On("GetUser", mock.Anything, int64(1)).Return(
        &User{ID: 1, Name: "John Doe"}, nil,
    )

    req, _ := http.NewRequest("GET", "/users/1", nil)
    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)

    var response map[string]interface{}
    json.Unmarshal(w.Body.Bytes(), &response)
    assert.Equal(t, float64(1), response["data"].(map[string]interface{})["id"])

    mockUserService.AssertExpectations(t)
}

func TestUserHandler_GetUser_NotFound(t *testing.T) {
    gin.SetMode(gin.TestMode)

    mockUserService := &MockUserService{}
    logger := logrus.New()
    handler := NewUserHandler(mockUserService, logger)

    router := gin.New()
    router.GET("/users/:id", handler.GetUser)

    mockUserService.On("GetUser", mock.Anything, int64(999)).Return(
        nil, ErrUserNotFound,
    )

    req, _ := http.NewRequest("GET", "/users/999", nil)
    w := httptest.NewRecorder()
    router.ServeHTTP(w, req)

    assert.Equal(t, http.StatusNotFound, w.Code)

    mockUserService.AssertExpectations(t)
}
```

### Integration Testing
```go
func TestAPI_Integration(t *testing.T) {
    // Setup test database
    db := setupTestDatabase(t)
    defer db.Close()

    // Setup application
    app := setupApplication(db)

    // Test user creation and retrieval
    // Create user
    createReq := CreateUserRequest{
        Name:  "Test User",
        Email: "test@example.com",
    }

    reqBody, _ := json.Marshal(createReq)
    req, _ := http.NewRequest("POST", "/api/v1/users", bytes.NewBuffer(reqBody))
    req.Header.Set("Content-Type", "application/json")

    w := httptest.NewRecorder()
    app.ServeHTTP(w, req)

    assert.Equal(t, http.StatusCreated, w.Code)

    // Get user
    var response map[string]interface{}
    json.Unmarshal(w.Body.Bytes(), &response)
    userID := int64(response["data"].(map[string]interface{})["id"].(float64))

    req, _ = http.NewRequest("GET", fmt.Sprintf("/api/v1/users/%d", userID), nil)
    w = httptest.NewRecorder()
    app.ServeHTTP(w, req)

    assert.Equal(t, http.StatusOK, w.Code)
}
```

## Performance Optimization

### Response Compression
```go
func CompressionMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        // Check if client accepts gzip
        if strings.Contains(c.GetHeader("Accept-Encoding"), "gzip") {
            c.Header("Content-Encoding", "gzip")
        }
        c.Next()
    }
}

// Apply to router
r.Use(gin.WrapMiddleware(http.DefaultServeMux))
```

### Connection Pooling
```go
// Database connection pool settings
func setupDatabase() *gorm.DB {
    dsn := "user:password@tcp(localhost:3306)/dbname?charset=utf8mb4&parseTime=True&loc=Local"
    db, err := gorm.Open(mysql.Open(dsn), &gorm.Config{})
    if err != nil {
        panic("Failed to connect to database")
    }

    sqlDB, err := db.DB()
    if err != nil {
        panic("Failed to get database instance")
    }

    // Set connection pool parameters
    sqlDB.SetMaxOpenConns(100)     // Maximum number of open connections
    sqlDB.SetMaxIdleConns(10)      // Maximum number of idle connections
    sqlDB.SetConnMaxLifetime(time.Hour) // Maximum lifetime of a connection

    return db
}
```

## Security Best Practices

### Input Sanitization
```go
func sanitizeInput(input string) string {
    // Remove HTML tags
    html.EscapeString(input)

    // Trim whitespace
    strings.TrimSpace(input)

    return input
}
```

### Rate Limiting
```go
func RateLimitMiddleware() gin.HandlerFunc {
    limiter := rate.NewLimiter(rate.Limit(100), 200) // 100 requests per second, burst of 200

    return func(c *gin.Context) {
        if !limiter.Allow() {
            c.JSON(http.StatusTooManyRequests, gin.H{
                "error": "Rate limit exceeded",
            })
            c.Abort()
            return
        }
        c.Next()
    }
}
```

### CORS Configuration
```go
func CORSMiddleware() gin.HandlerFunc {
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
```

## Resources

### Official Documentation
- [Gin Framework Documentation](https://gin-gonic.com/docs/)
- [Gin GitHub Repository](https://github.com/gin-gonic/gin)
- [Gin Examples](https://github.com/gin-gonic/examples)

### Community Resources
- [Go Web Development with Gin](https://blog.golang.org/build-web-applications-with-go)
- [Gin Best Practices](https://github.com/gin-gonic/gin/wiki)
- [Gin CookBook](https://gin-gonic.com/en/docs/cookbook/)