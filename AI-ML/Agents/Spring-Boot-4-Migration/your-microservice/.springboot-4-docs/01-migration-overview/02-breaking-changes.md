# Spring Boot 4 Breaking Changes

## Critical Breaking Changes

### 1. Java Version Requirement
- **Spring Boot 3**: Java 17 or 20
- **Spring Boot 4**: Java 21+ (MANDATORY)
- **Impact**: Must upgrade JDK before migration

### 2. Package Migration: javax.* → jakarta.*
- **Change**: ALL javax.* packages renamed to jakarta.*
- **Impact**: Every import statement must be updated
- **Scope**: Affects servlet, JPA, validation, annotations, etc.
- **No Backward Compatibility**: This is a hard breaking change

### 3. Configuration Namespace Changes
- **Old**: `spring.http.client.*` and `spring.http.reactiveclient.*`
- **New**: `spring.http.clients.*` (unified namespace)
- **Impact**: All HTTP client configurations must be updated

### 4. Null Annotations
- **Old**: `org.springframework.lang.Nullable`
- **New**: `org.jspecify.annotations.Nullable`
- **Impact**: Update all nullable annotations for better type safety

### 5. Observability Framework
- **Old**: Jaeger tracing
- **New**: OpenTelemetry (OTLP)
- **Impact**: Update tracing configuration and dependencies

## Deprecated and Removed APIs

### Removed in Spring Boot 4.0
- RestTemplate patterns (replaced by @HttpExchange)
- Manual API versioning (replaced by native @Version)
- Spring's Nullable annotations (replaced by JSpecify)
- Old HTTP client configuration namespaces

### Configuration Changes

#### HTTP Client Configuration
```yaml
# ❌ Spring Boot 3 (DEPRECATED)
spring:
  http:
    client:
      connect-timeout: 5s
    reactiveclient:
      read-timeout: 10s

# ✅ Spring Boot 4 (REQUIRED)
spring:
  http:
    clients:
      default:
        connect-timeout: 5s
        read-timeout: 10s
```

#### Observability Configuration
```yaml
# ❌ Spring Boot 3 (Jaeger)
management:
  tracing:
    jaeger:
      grpc:
        endpoint: http://localhost:14250

# ✅ Spring Boot 4 (OpenTelemetry)
management:
  otlp:
    tracing:
      endpoint: http://localhost:4318
```

## Dependency Changes

### Maven Parent Version
```xml
<!-- ❌ Spring Boot 3 -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<!-- ✅ Spring Boot 4 -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>4.0.0</version>
</parent>
```

### New Dependencies Required
- `spring-boot-starter-opentelemetry` (for observability)
- JSpecify annotations library (for null safety)

## Migration Impact Assessment

| Change Category | Impact Level | Effort Required |
|----------------|--------------|-----------------|
| Java 21 Upgrade | HIGH | 1-2 hours |
| javax → jakarta | CRITICAL | 2-4 hours |
| Configuration Updates | MEDIUM | 1-2 hours |
| Null Annotations | LOW | 1 hour |
| Observability | MEDIUM | 2-3 hours |

## Compatibility Notes

### Third-Party Libraries
- Ensure all third-party libraries support Jakarta EE 11
- Check for Spring Boot 4 compatible versions
- Update Hibernate to 6.4+ (included in Boot 4)
- Update Spring Security to 6.4+ (included in Boot 4)

### Database Drivers
- Most JDBC drivers are compatible
- Update to latest versions for best performance
- Test connection pooling configurations

### Cloud Platforms
- Verify cloud provider supports Java 21
- Update buildpacks if using Cloud Native Buildpacks
- Check container base images for Java 21 support
