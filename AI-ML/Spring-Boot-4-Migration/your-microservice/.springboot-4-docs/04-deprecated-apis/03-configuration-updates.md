# Configuration Updates for Spring Boot 4

## HTTP Client Configuration

### Old Namespace (Deprecated)
```yaml
spring:
  http:
    client:
      connect-timeout: 5000
      read-timeout: 10000
    reactiveclient:
      connect-timeout: 5000
      read-timeout: 10000
```

### New Unified Namespace
```yaml
spring:
  http:
    clients:
      default:
        connect-timeout: 5s
        read-timeout: 10s
        redirect-follow: true
      api-client:
        connect-timeout: 15s
        read-timeout: 30s
        max-connections: 100
```

## Observability and Tracing

### Old Configuration
```yaml
management:
  tracing:
    jaeger:
      grpc:
        endpoint: http://localhost:14250
      sampling:
        probability: 1.0
```

### New Configuration
```yaml
management:
  otlp:
    tracing:
      endpoint: http://localhost:4318
      compression: gzip
      timeout: 10s
  observations:
    key-values:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:dev}
```

## Actuator Endpoints

### Old Configuration
```yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"
  endpoint:
    health:
      show-details: always
```

### New Configuration (Same, but verify)
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus,info
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true
```

## Server Configuration

### Old Configuration
```yaml
server:
  port: 8080
  servlet:
    context-path: /api
```

### New Configuration (No change needed)
```yaml
server:
  port: 8080
  servlet:
    context-path: /api
```

## Data Source Configuration

### Old Configuration
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: user
    password: pass
    driver-class-name: org.postgresql.Driver
```

### New Configuration (No change needed)
```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: user
    password: pass
    driver-class-name: org.postgresql.Driver
```

## Complete application.yml Example

```yaml
spring:
  application:
    name: order-service
  
  # HTTP Clients (UPDATED)
  http:
    clients:
      default:
        connect-timeout: 5s
        read-timeout: 10s
  
  # Data Source (No change)
  datasource:
    url: jdbc:postgresql://localhost:5432/orders
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  
  # JPA (No change)
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: false
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect

# Management & Observability (UPDATED)
management:
  # OpenTelemetry
  otlp:
    tracing:
      endpoint: http://localhost:4318
  
  # Observations
  observations:
    key-values:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:production}
  
  # Endpoints
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus,info
  
  endpoint:
    health:
      show-details: when-authorized
      probes:
        enabled: true

# Server (No change)
server:
  port: 8080
```

## Migration Checklist

- [ ] Update `spring.http.client.*` to `spring.http.clients.*`
- [ ] Update `management.tracing.jaeger.*` to `management.otlp.tracing.*`
- [ ] Add `management.observations.key-values` for metadata
- [ ] Verify actuator endpoint exposure settings
- [ ] Test configuration with `./mvnw spring-boot:run`
