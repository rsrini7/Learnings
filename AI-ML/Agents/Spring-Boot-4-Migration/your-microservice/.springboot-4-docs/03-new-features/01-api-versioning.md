# Spring Boot 4: Native API Versioning

## Problem Solved
Before Boot 4: Developers manually created V1/V2/V3 controller classes

```java
// ❌ Old approach - messy and hard to maintain
@RestController
@RequestMapping("/api/v1/orders")
public class OrderControllerV1 { }

@RestController
@RequestMapping("/api/v2/orders")
public class OrderControllerV2 { }

// Duplicate code, inconsistent logic, maintenance nightmare
```

## Solution: Native Versioning

Spring Boot 4 includes built-in API versioning support

### Basic Example

```java
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.http.HttpStatus;
import org.springframework.web.servlet.mvc.method.annotation.HttpHeaders;
// ✅ Use jakarta.*, not javax.*
import jakarta.annotation.Nonnull;

@RestController
@RequestMapping("/api/orders")
public class OrderController {
    
    // Version 4.0: Basic order creation
    @PostMapping
    @Version("4.0")
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<OrderResponse> createOrder(@Nonnull @RequestBody CreateOrderRequest request) {
        // Returns: { id, name, price, timestamp }
        return ResponseEntity.ok(new OrderResponse(/* ... */));
    }
    
    // Version 4.1: Enhanced with tracking
    @PostMapping
    @Version("4.1")
    @ResponseStatus(HttpStatus.CREATED)
    public ResponseEntity<OrderResponseV2> createOrderWithTracking(@Nonnull @RequestBody CreateOrderRequest request) {
        // Returns: { id, name, price, timestamp, trackingId, estimatedDelivery }
        return ResponseEntity.ok(new OrderResponseV2(/* ... */));
    }
}
```

### Configuration

**application.yml:**
```yaml
spring:
  mvc:
    api-versioning:
      enabled: true
      strategies:
        - path        # /api/v4.0/...
        - header      # X-API-Version: 4.0
        - media-type  # application/json; version=4.0
        - parameter   # ?apiVersion=4.0
      default-version: "4.0"
      version-header-name: X-API-Version
```

### Versioning Strategies

#### 1. Path-Based Versioning
```
GET /api/v4.0/orders
GET /api/v4.1/orders
```

#### 2. Header-Based Versioning
```
GET /api/orders
Header: X-API-Version: 4.0
```

#### 3. Media-Type Versioning
```
GET /api/orders
Accept: application/json; version=4.0
```

#### 4. Query Parameter Versioning
```
GET /api/orders?apiVersion=4.0
```

### Testing Version-Specific Endpoints

```java
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.web.servlet.MockMvc;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
class OrderControllerVersioningTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Test
    void testVersion40() throws Exception {
        mockMvc.perform(post("/api/v4.0/orders")
                .contentType("application/json")
                .content(/* order JSON */))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.tracking").doesNotExist());  // v4.0 has no tracking
    }
    
    @Test
    void testVersion41() throws Exception {
        mockMvc.perform(post("/api/v4.1/orders")
                .contentType("application/json")
                .content(/* order JSON */))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.tracking").exists());  // v4.1 has tracking
    }
    
    @Test
    void testHeaderBasedVersioning() throws Exception {
        mockMvc.perform(post("/api/orders")
                .header("X-API-Version", "4.1")
                .contentType("application/json")
                .content(/* order JSON */))
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.tracking").exists());
    }
}
```

## Benefits
✅ Single controller with multiple versions
✅ Eliminates code duplication
✅ Easy deprecation path
✅ Type-safe and testable
✅ Built-in deprecation warnings
