# APIs Removed in Spring Boot 4.0

## Deprecated and Removed Components

### 1. RestTemplate (Soft Deprecated)
**Status**: Soft deprecated, still works but not recommended
**Replacement**: `@HttpExchange` declarative clients

```java
// ❌ Deprecated (still works)
@Service
public class OldService {
    @Autowired
    private RestTemplate restTemplate;
}

// ✅ Recommended
@HttpExchange("/api")
public interface NewClient {
    @GetExchange("/data")
    Data getData();
}
```

### 2. Manual API Versioning
**Status**: Replaced by native versioning
**Replacement**: `@Version` annotation

```java
// ❌ Old approach
@RestController
@RequestMapping("/api/v1/users")
public class UserControllerV1 { }

// ✅ New approach
@RestController
@RequestMapping("/api/users")
public class UserController {
    @GetMapping
    @Version("1.0")
    public List<User> getUsers() { }
}
```

### 3. Spring's Nullable Annotations
**Status**: Replaced
**Replacement**: JSpecify annotations

```java
// ❌ Removed
import org.springframework.lang.Nullable;
import org.springframework.lang.NonNull;

// ✅ Use instead
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NullMarked;
```

### 4. Old HTTP Client Configuration
**Status**: Removed
**Replacement**: Unified `spring.http.clients.*` namespace

```yaml
# ❌ Removed
spring:
  http:
    client:
      connect-timeout: 5s
    reactiveclient:
      read-timeout: 10s

# ✅ Use instead
spring:
  http:
    clients:
      default:
        connect-timeout: 5s
        read-timeout: 10s
```

### 5. Jaeger Tracing
**Status**: Removed
**Replacement**: OpenTelemetry

```yaml
# ❌ Removed
management:
  tracing:
    jaeger:
      grpc:
        endpoint: http://localhost:14250

# ✅ Use instead
management:
  otlp:
    tracing:
      endpoint: http://localhost:4318
```

## Deprecation Timeline

| Component | Deprecated In | Removed In | Replacement |
|-----------|--------------|------------|-------------|
| javax.* packages | N/A | 4.0 | jakarta.* |
| RestTemplate | 3.2 | Not removed | @HttpExchange |
| Manual versioning | N/A | 4.0 | @Version |
| Spring Nullable | 3.3 | 4.0 | JSpecify |
| Old HTTP config | 3.3 | 4.0 | spring.http.clients.* |
| Jaeger | 3.3 | 4.0 | OpenTelemetry |

## Migration Priority

### Critical (Must Fix)
1. javax.* → jakarta.* (breaks compilation)
2. HTTP client configuration namespace
3. Observability configuration

### High (Recommended)
4. Null annotations to JSpecify
5. Manual versioning to @Version
6. RestTemplate to @HttpExchange

### Medium (Optional)
7. Legacy actuator endpoints
8. Old metrics formats
