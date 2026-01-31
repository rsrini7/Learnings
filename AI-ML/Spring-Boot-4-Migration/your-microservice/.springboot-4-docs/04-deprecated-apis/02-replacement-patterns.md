# Deprecated API Replacements in Spring Boot 4

## HTTP Client Configuration

### ❌ Spring Boot 3 (Deprecated)
```yaml
spring:
  http:
    client:
      connect-timeout: 5s
      read-timeout: 10s
    reactiveclient:
      connect-timeout: 5s
      read-timeout: 10s
```

### ✅ Spring Boot 4 (Unified)
```yaml
spring:
  http:
    clients:
      default:
        connect-timeout: 5s
        read-timeout: 10s
        redirect-follow: true
        ssl-bundle: web
      custom:
        connect-timeout: 15s
        read-timeout: 30s
```

## Observability Configuration

### ❌ Spring Boot 3 (Jaeger)
```yaml
management:
  tracing:
    jaeger:
      grpc:
        endpoint: http://localhost:14250
```

### ✅ Spring Boot 4 (OpenTelemetry)
```yaml
management:
  otlp:
    tracing:
      endpoint: http://localhost:4318
  observations:
    key-values:
      application: my-service
      environment: production
```

#### Dependencies
```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

## Null Annotations

### ❌ Spring Boot 3 (Spring's Nullable)
```java
import org.springframework.lang.Nullable;

@RestController
public class MyController {
    @GetMapping("/user/{id}")
    public User getUser(@Nullable String email) {
        // email is optional
    }
}
```

### ✅ Spring Boot 4 (JSpecify)
```java
import org.jspecify.annotations.Nullable;
import jakarta.annotation.Nonnull;

@RestController
public class MyController {
    @GetMapping("/user/{id}")
    public User getUser(@Nullable String email) {
        // email is optional (same behavior, better standard)
    }
    
    @GetMapping("/product/{id}")
    public Product getProduct(@Nonnull String id) {
        // id is required (explicitly non-null)
    }
}
```

## HTTP Service Clients

### ❌ Spring Boot 3 (Manual REST templates)
```java
@Service
public class OrderService {
    @Autowired
    private RestTemplate restTemplate;
    
    public Order getOrder(String id) {
        return restTemplate.getForObject(
            "http://api.example.com/orders/" + id, 
            Order.class
        );
    }
}
```

### ✅ Spring Boot 4 (@HttpExchange)
```java
// Define service interface
@HttpExchange("/orders")
public interface OrderClient {
    
    @GetExchange("/{id}")
    Order getOrder(@PathVariable String id);
    
    @PostExchange
    Order createOrder(@RequestBody CreateOrderRequest request);
}

// Use in service
@Service
public class OrderService {
    private final OrderClient orderClient;
    
    public OrderService(OrderClient orderClient) {
        this.orderClient = orderClient;
    }
    
    public Order getOrder(String id) {
        return orderClient.getOrder(id);
    }
}

// Configuration
@Configuration
public class ClientConfiguration {
    @Bean
    OrderClient orderClient(HttpClientBuilder builder) {
        return HttpServiceProxyFactory
            .builder(builder.build())
            .baseUrl("http://api.example.com")
            .build()
            .createClient(OrderClient.class);
    }
}
```

## API Versioning

### ❌ Spring Boot 3 (Manual Controllers)
```java
@RestController
@RequestMapping("/api/v1/products")
public class ProductControllerV1 {
    @GetMapping
    public List<ProductV1> getProducts() { }
}

@RestController
@RequestMapping("/api/v2/products")
public class ProductControllerV2 {
    @GetMapping
    public List<ProductV2> getProducts() { }
}
```

### ✅ Spring Boot 4 (Native Versioning)
```java
@RestController
@RequestMapping("/api/products")
public class ProductController {
    
    @GetMapping
    @Version("1.0")
    public List<ProductV1> getProductsV1() { }
    
    @GetMapping
    @Version("2.0")
    public List<ProductV2> getProductsV2() { }
}
```

Configuration:
```yaml
spring:
  mvc:
    api-versioning:
      enabled: true
      strategies:
        - path
        - header
      default-version: "2.0"
```
