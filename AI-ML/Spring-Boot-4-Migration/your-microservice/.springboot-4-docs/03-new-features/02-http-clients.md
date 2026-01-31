# Spring Boot 4: HTTP Service Clients (@HttpExchange)

## Overview
Spring Boot 4 introduces declarative HTTP clients using `@HttpExchange`, replacing the verbose RestTemplate pattern.

## Old Pattern (RestTemplate)

```java
// ❌ Spring Boot 3 - Verbose and error-prone
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
    
    public Order createOrder(CreateOrderRequest request) {
        return restTemplate.postForObject(
            "http://api.example.com/orders",
            request,
            Order.class
        );
    }
}
```

## New Pattern (@HttpExchange)

### Step 1: Define Service Interface

```java
import org.springframework.web.service.annotation.HttpExchange;
import org.springframework.web.service.annotation.GetExchange;
import org.springframework.web.service.annotation.PostExchange;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;

@HttpExchange("/orders")
public interface OrderClient {
    
    @GetExchange("/{id}")
    Order getOrder(@PathVariable String id);
    
    @PostExchange
    Order createOrder(@RequestBody CreateOrderRequest request);
    
    @GetExchange
    List<Order> getAllOrders();
    
    @DeleteExchange("/{id}")
    void deleteOrder(@PathVariable String id);
}
```

### Step 2: Configure Client Bean

```java
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.function.client.WebClient;
import org.springframework.web.reactive.function.client.support.WebClientAdapter;
import org.springframework.web.service.invoker.HttpServiceProxyFactory;

@Configuration
public class ClientConfiguration {
    
    @Bean
    public OrderClient orderClient() {
        WebClient webClient = WebClient.builder()
            .baseUrl("http://api.example.com")
            .build();
        
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
            .builder(WebClientAdapter.forClient(webClient))
            .build();
        
        return factory.createClient(OrderClient.class);
    }
}
```

### Step 3: Use in Service

```java
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final OrderClient orderClient;
    
    public OrderService(OrderClient orderClient) {
        this.orderClient = orderClient;
    }
    
    public Order getOrder(String id) {
        return orderClient.getOrder(id);
    }
    
    public Order createOrder(CreateOrderRequest request) {
        return orderClient.createOrder(request);
    }
}
```

## Advanced Features

### Custom Headers

```java
@HttpExchange("/orders")
public interface OrderClient {
    
    @GetExchange("/{id}")
    Order getOrder(
        @PathVariable String id,
        @RequestHeader("X-API-Key") String apiKey
    );
}
```

### Query Parameters

```java
@HttpExchange("/orders")
public interface OrderClient {
    
    @GetExchange
    List<Order> searchOrders(
        @RequestParam("status") String status,
        @RequestParam("limit") int limit
    );
}
```

### Response Handling

```java
@HttpExchange("/orders")
public interface OrderClient {
    
    @GetExchange("/{id}")
    ResponseEntity<Order> getOrderWithHeaders(@PathVariable String id);
    
    @GetExchange
    Mono<List<Order>> getAllOrdersAsync();  // Reactive support
}
```

### Error Handling

```java
@Configuration
public class ClientConfiguration {
    
    @Bean
    public OrderClient orderClient() {
        WebClient webClient = WebClient.builder()
            .baseUrl("http://api.example.com")
            .defaultStatusHandler(
                HttpStatusCode::is4xxClientError,
                response -> Mono.error(new ClientException("Client error"))
            )
            .defaultStatusHandler(
                HttpStatusCode::is5xxServerError,
                response -> Mono.error(new ServerException("Server error"))
            )
            .build();
        
        HttpServiceProxyFactory factory = HttpServiceProxyFactory
            .builder(WebClientAdapter.forClient(webClient))
            .build();
        
        return factory.createClient(OrderClient.class);
    }
}
```

## Configuration Options

### Timeouts

```yaml
spring:
  http:
    clients:
      order-client:
        connect-timeout: 5s
        read-timeout: 10s
```

### Authentication

```java
@Bean
public OrderClient orderClient() {
    WebClient webClient = WebClient.builder()
        .baseUrl("http://api.example.com")
        .defaultHeader("Authorization", "Bearer " + getToken())
        .build();
    
    // ... rest of configuration
}
```

## Testing

```java
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;

import static org.mockito.Mockito.*;
import static org.assertj.core.api.Assertions.*;

@SpringBootTest
class OrderServiceTest {
    
    @MockBean
    private OrderClient orderClient;
    
    @Autowired
    private OrderService orderService;
    
    @Test
    void testGetOrder() {
        Order mockOrder = new Order("123", "Test Order");
        when(orderClient.getOrder("123")).thenReturn(mockOrder);
        
        Order result = orderService.getOrder("123");
        
        assertThat(result).isEqualTo(mockOrder);
        verify(orderClient).getOrder("123");
    }
}
```

## Benefits

✅ **Declarative**: Define API as interface
✅ **Type-safe**: Compile-time checking
✅ **Less boilerplate**: No manual URL construction
✅ **Testable**: Easy to mock
✅ **Reactive support**: Works with WebFlux
✅ **Consistent**: Same pattern across all HTTP clients
