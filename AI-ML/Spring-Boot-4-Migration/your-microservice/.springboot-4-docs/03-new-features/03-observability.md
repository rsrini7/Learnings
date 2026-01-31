# Spring Boot 4: OpenTelemetry Observability

## Overview
Spring Boot 4 replaces Jaeger with OpenTelemetry (OTLP) as the standard for distributed tracing and observability.

## Migration from Jaeger

### Old Configuration (Spring Boot 3)

```yaml
# ❌ Spring Boot 3 - Jaeger
management:
  tracing:
    jaeger:
      grpc:
        endpoint: http://localhost:14250
```

```xml
<!-- ❌ Old dependency -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-tracing-bridge-brave</artifactId>
</dependency>
<dependency>
    <groupId>io.zipkin.reporter2</groupId>
    <artifactId>zipkin-reporter-brave</artifactId>
</dependency>
```

### New Configuration (Spring Boot 4)

```yaml
# ✅ Spring Boot 4 - OpenTelemetry
management:
  otlp:
    tracing:
      endpoint: http://localhost:4318
  observations:
    key-values:
      application: my-service
      environment: production
      version: 1.0.0
```

```xml
<!-- ✅ New dependency -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
```

## Complete Setup

### 1. Add Dependencies

```xml
<dependencies>
    <!-- OpenTelemetry -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-opentelemetry</artifactId>
    </dependency>
    
    <!-- Actuator for metrics -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
</dependencies>
```

### 2. Configure application.yml

```yaml
spring:
  application:
    name: order-service

management:
  # OpenTelemetry tracing
  otlp:
    tracing:
      endpoint: http://localhost:4318
      compression: gzip
      timeout: 10s
  
  # Observations configuration
  observations:
    key-values:
      application: ${spring.application.name}
      environment: ${ENVIRONMENT:dev}
      version: ${APP_VERSION:1.0.0}
  
  # Metrics export
  metrics:
    export:
      otlp:
        enabled: true
        endpoint: http://localhost:4318
        step: 10s
  
  # Actuator endpoints
  endpoints:
    web:
      exposure:
        include: health,metrics,prometheus,info
```

### 3. Custom Instrumentation

```java
import io.micrometer.observation.Observation;
import io.micrometer.observation.ObservationRegistry;
import org.springframework.stereotype.Service;

@Service
public class OrderService {
    private final ObservationRegistry observationRegistry;
    
    public OrderService(ObservationRegistry observationRegistry) {
        this.observationRegistry = observationRegistry;
    }
    
    public Order createOrder(CreateOrderRequest request) {
        return Observation
            .createNotStarted("order.create", observationRegistry)
            .lowCardinalityKeyValue("order.type", request.getType())
            .observe(() -> {
                // Business logic here
                return processOrder(request);
            });
    }
}
```

### 4. Span Annotations

```java
import io.micrometer.observation.annotation.Observed;
import org.springframework.stereotype.Service;

@Service
public class PaymentService {
    
    @Observed(name = "payment.process", contextualName = "process-payment")
    public PaymentResult processPayment(PaymentRequest request) {
        // Payment processing logic
        return new PaymentResult();
    }
}
```

## Docker Compose Setup

```yaml
version: '3.8'

services:
  # OpenTelemetry Collector
  otel-collector:
    image: otel/opentelemetry-collector:latest
    command: ["--config=/etc/otel-collector-config.yaml"]
    volumes:
      - ./otel-collector-config.yaml:/etc/otel-collector-config.yaml
    ports:
      - "4318:4318"   # OTLP HTTP receiver
      - "4317:4317"   # OTLP gRPC receiver
      - "8888:8888"   # Prometheus metrics
  
  # Jaeger (for visualization)
  jaeger:
    image: jaegertracing/all-in-one:latest
    ports:
      - "16686:16686" # Jaeger UI
      - "14250:14250" # gRPC
  
  # Prometheus
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
  
  # Grafana
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
```

### OpenTelemetry Collector Config

```yaml
# otel-collector-config.yaml
receivers:
  otlp:
    protocols:
      grpc:
        endpoint: 0.0.0.0:4317
      http:
        endpoint: 0.0.0.0:4318

processors:
  batch:
    timeout: 10s

exporters:
  jaeger:
    endpoint: jaeger:14250
    tls:
      insecure: true
  
  prometheus:
    endpoint: "0.0.0.0:8888"
  
  logging:
    loglevel: debug

service:
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [jaeger, logging]
    
    metrics:
      receivers: [otlp]
      processors: [batch]
      exporters: [prometheus, logging]
```

## Custom Metrics

```java
import io.micrometer.core.instrument.Counter;
import io.micrometer.core.instrument.MeterRegistry;
import io.micrometer.core.instrument.Timer;
import org.springframework.stereotype.Service;

@Service
public class MetricsService {
    private final Counter orderCounter;
    private final Timer orderProcessingTimer;
    
    public MetricsService(MeterRegistry meterRegistry) {
        this.orderCounter = Counter.builder("orders.created")
            .description("Total orders created")
            .tag("service", "order-service")
            .register(meterRegistry);
        
        this.orderProcessingTimer = Timer.builder("orders.processing.time")
            .description("Order processing time")
            .tag("service", "order-service")
            .register(meterRegistry);
    }
    
    public void recordOrderCreated() {
        orderCounter.increment();
    }
    
    public void recordProcessingTime(Runnable task) {
        orderProcessingTimer.record(task);
    }
}
```

## Distributed Tracing Example

```java
import io.micrometer.tracing.Tracer;
import io.micrometer.tracing.Span;
import org.springframework.stereotype.Service;

@Service
public class DistributedService {
    private final Tracer tracer;
    private final OrderClient orderClient;
    
    public DistributedService(Tracer tracer, OrderClient orderClient) {
        this.tracer = tracer;
        this.orderClient = orderClient;
    }
    
    public void processDistributedOrder(String orderId) {
        Span span = tracer.nextSpan().name("process-distributed-order");
        
        try (Tracer.SpanInScope ws = tracer.withSpan(span.start())) {
            span.tag("order.id", orderId);
            
            // Call external service - trace propagates automatically
            Order order = orderClient.getOrder(orderId);
            
            // Add event to span
            span.event("order-fetched");
            
            // Process order
            processOrder(order);
            
        } finally {
            span.end();
        }
    }
}
```

## Verification

### Check Metrics Endpoint
```bash
curl http://localhost:8080/actuator/metrics
curl http://localhost:8080/actuator/prometheus
```

### View Traces in Jaeger
```
http://localhost:16686
```

### View Metrics in Prometheus
```
http://localhost:9090
```

### View Dashboards in Grafana
```
http://localhost:3000
```

## Benefits

✅ **Industry Standard**: OpenTelemetry is vendor-neutral
✅ **Unified Observability**: Traces, metrics, and logs in one place
✅ **Better Performance**: More efficient than Jaeger
✅ **Cloud Native**: Works with all major cloud providers
✅ **Automatic Instrumentation**: Spring Boot auto-configures most components
