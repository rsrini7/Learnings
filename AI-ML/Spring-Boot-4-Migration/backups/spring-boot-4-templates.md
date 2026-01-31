# Spring Boot 4 Migration: Concrete Implementation Examples
## Template Files & Real Code Samples

---

## 📝 Template 1: SPRINGBOOT-AGENTS.md (Compressed Index)

Save this as **`SPRINGBOOT-AGENTS.md`** in your project root:

```markdown
# Spring Boot 4 Migration Assistant Context

[Spring Boot 4 Docs Index]|root: ./.springboot-4-docs|
CRITICAL_RULES:
  - Java 21 is MANDATORY minimum (LTS release) - no Java 20 or earlier
  - ALL javax.* imports MUST become jakarta.* - this is NOT optional
  - Use org.jspecify.annotations.Nullable NOT org.springframework.lang.Nullable
  - Configuration spring.http.client.* is DEPRECATED - must use spring.http.clients.*
  - Verify NO remaining javax.* with: grep -r "import javax" --include="*.java" .
|
IMPORTANT: Prefer retrieval-led reasoning over pre-training-led reasoning for Spring Boot tasks|
IMPORTANT: When generating code, ALWAYS verify:
  1. Java 21+ compatibility
  2. Zero javax.* imports (use jakarta.*)
  3. spring.http.clients.* config (if HTTP client related)
  4. JSpecify null annotations (if nullable params)
|
01-migration-overview:{01-java-baseline.md,02-breaking-changes.md,03-migration-checklist.md}|
02-package-migrations:{01-javax-to-jakarta.md,02-common-packages.md,03-import-mappings.md}|
03-new-features:{01-api-versioning.md,02-http-clients.md,03-observability.md,04-jspecify-nullability.md}|
04-deprecated-apis:{01-removed-in-4.0.md,02-replacement-patterns.md,03-configuration-updates.md}|
05-dependency-updates:{01-maven-bom-updates.md,02-gradle-dependencies.md,03-transitive-versions.md}|
06-common-patterns:{01-spring-security-6.4.md,02-spring-data-updates.md,03-testing-changes.md,04-actuator-updates.md}|

## When Agent Encounters a Task

### Task Type: Code Generation
→ Check: 03-new-features/ (new patterns)
→ Cross-check: 04-deprecated-apis/ (what NOT to use)
→ Verify: No javax.* imports, Java 21 compatible

### Task Type: Configuration Update
→ Check: 05-dependency-updates/ (version mappings)
→ Check: 06-common-patterns/ (common configs)
→ Verify: spring.http.clients.* if HTTP related

### Task Type: Package Import Migration
→ Check: 02-package-migrations/01-javax-to-jakarta.md (mapping table)
→ Execute: Find & replace javax.* → jakarta.*
→ Verify: grep -r "import javax" returns 0

### Task Type: Dependency Issues
→ Check: 05-dependency-updates/01-maven-bom-updates.md
→ Check: 05-dependency-updates/02-gradle-dependencies.md

---

## 🔧 Template 2: .springboot-4-docs Structure Files

### 2.1: .springboot-4-docs/01-migration-overview/01-java-baseline.md

```markdown
# Java Baseline Requirements - Spring Boot 4

## Requirement
**Spring Boot 4.0 requires Java 21 minimum** (LTS release)

## Why Java 21?
- Spring Framework 7 requires Java 21+
- Jakarta EE 11 baseline requires Java 21+
- Virtual threads & ZGC (JDK 21 features) optimal for Spring Boot 4
- Java 20 and earlier NOT supported

## Installation

### macOS (Homebrew)
\`\`\`bash
brew install openjdk@21
echo 'export PATH="/opt/homebrew/opt/openjdk@21/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
java -version  # Verify: openjdk 21.x.x
\`\`\`

### Linux (Ubuntu/Debian)
\`\`\`bash
sudo apt-get install openjdk-21-jdk
java -version  # Verify: openjdk 21.x.x
\`\`\`

### SDKMAN (All platforms)
\`\`\`bash
curl -s "https://get.sdkman.io" | bash
sdk list java | grep 21
sdk install java 21.0.1-tem
java -version
\`\`\`

## Update Maven/Gradle

### Maven (pom.xml)
\`\`\`xml
<properties>
    <java.version>21</java.version>
    <maven.compiler.source>21</maven.compiler.source>
    <maven.compiler.target>21</maven.compiler.target>
</properties>
\`\`\`

### Gradle (build.gradle)
\`\`\`gradle
java {
    sourceCompatibility = '21'
    targetCompatibility = '21'
}
\`\`\`

## Verification
\`\`\`bash
java -version
# Expected: openjdk 21.0.x (or similar)

./mvnw --version
# Expected: Maven 3.9.0+

./gradlew --version
# Expected: Gradle 8.4+
\`\`\`

## If You See Errors
- **"javac: invalid release version 21"** → Java 21 not installed
- **"Error: Could not find or load main class"** → Check JAVA_HOME env var
- **"Spring Boot 4 not found"** → Maven/Gradle cache issue, run `clean install`
```

### 2.2: .springboot-4-docs/02-package-migrations/01-javax-to-jakarta.md

```markdown
# Jakarta EE Package Migration: javax.* → jakarta.*

## Overview
Jakarta EE 11 renamed ALL `javax.*` packages to `jakarta.*`

This is a **breaking change** - no backward compatibility

## Complete Migration Table

| javax Package | jakarta Package |
|---|---|
| javax.annotation.* | jakarta.annotation.* |
| javax.servlet.* | jakarta.servlet.* |
| javax.persistence.* | jakarta.persistence.* |
| javax.transaction.* | jakarta.transaction.* |
| javax.validation.* | jakarta.validation.* |
| javax.inject.* | jakarta.inject.* |
| javax.el.* | jakarta.el.* |
| javax.xml.* | jakarta.xml.* |
| javax.mail.* | jakarta.mail.* |
| javax.naming.* | jakarta.naming.* |

## Method 1: IDE Refactoring (Recommended)

### IntelliJ IDEA
```
1. Edit → Find → Replace (Ctrl+H on Windows/Linux, Cmd+H on Mac)
2. Find:    javax\.
3. Replace: jakarta.
4. Scope:   Entire Project
5. Replace All
```

### VS Code with Extension
```
1. Install "Find and Replace" extension (if needed)
2. Ctrl+H (Find and Replace)
3. Find:    javax\.
4. Replace: jakarta.
5. Replace All
```

## Method 2: Command Line

### macOS/Linux
\`\`\`bash
find . -name "*.java" -type f | xargs sed -i '' 's/javax\./jakarta./g'
\`\`\`

### Windows (Git Bash)
\`\`\`bash
find . -name "*.java" -type f -exec sed -i 's/javax\./jakarta./g' {} +
\`\`\`

### Using Maven Plugin
\`\`\`bash
./mvnw org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:RELEASE \
  -Drewrite.activeRecipes=org.openrewrite.java.migrate.jakarta.AddCommonJakartaMigrations
\`\`\`

## Verification

### Check for Remaining javax Imports
\`\`\`bash
grep -r "import javax" --include="*.java" .
# Expected output: (empty - no results)

grep -r "import javax" --include="*.xml" .
grep -r "import javax" --include="*.properties" .
grep -r "import javax" --include="*.yml" .
# All should be empty
\`\`\`

### Compile Check
\`\`\`bash
./mvnw clean compile
# If any javax.* references remain, compilation will fail
# Error message will show the file and line number
\`\`\`

## Common Cases Before/After

### Case 1: Servlet Imports
\`\`\`java
// ❌ Before
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.Filter;

// ✅ After
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.Filter;
\`\`\`

### Case 2: JPA/Persistence
\`\`\`java
// ❌ Before
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Column;

// ✅ After
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
\`\`\`

### Case 3: Annotations
\`\`\`java
// ❌ Before
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import javax.inject.Named;
import javax.inject.Singleton;

// ✅ After
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
\`\`\`

### Case 4: Validation
\`\`\`java
// ❌ Before
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

// ✅ After
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
\`\`\`

## Testing
After migration, run full test suite:
\`\`\`bash
./mvnw clean test
# All tests should pass with zero javax.* references
\`\`\`
```

### 2.3: .springboot-4-docs/03-new-features/01-api-versioning.md

```markdown
# Spring Boot 4: Native API Versioning

## Problem Solved
Before Boot 4: Developers manually created V1/V2/V3 controller classes

\`\`\`java
// ❌ Old approach - messy and hard to maintain
@RestController
@RequestMapping("/api/v1/orders")
public class OrderControllerV1 { }

@RestController
@RequestMapping("/api/v2/orders")
public class OrderControllerV2 { }

// Duplicate code, inconsistent logic, maintenance nightmare
\`\`\`

## Solution: Native Versioning

Spring Boot 4 includes built-in API versioning support

### Basic Example

\`\`\`java
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
\`\`\`

### Configuration

**application.yml:**
\`\`\`yaml
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
\`\`\`

### Versioning Strategies

#### 1. Path-Based Versioning
\`\`\`
GET /api/v4.0/orders
GET /api/v4.1/orders
\`\`\`

#### 2. Header-Based Versioning
\`\`\`
GET /api/orders
Header: X-API-Version: 4.0
\`\`\`

#### 3. Media-Type Versioning
\`\`\`
GET /api/orders
Accept: application/json; version=4.0
\`\`\`

#### 4. Query Parameter Versioning
\`\`\`
GET /api/orders?apiVersion=4.0
\`\`\`

### Testing Version-Specific Endpoints

\`\`\`java
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
\`\`\`

## Benefits
✅ Single controller with multiple versions
✅ Eliminates code duplication
✅ Easy deprecation path
✅ Type-safe and testable
✅ Built-in deprecation warnings
```

### 2.4: .springboot-4-docs/04-deprecated-apis/02-replacement-patterns.md

```markdown
# Deprecated API Replacements in Spring Boot 4

## HTTP Client Configuration

### ❌ Spring Boot 3 (Deprecated)
\`\`\`yaml
spring:
  http:
    client:
      connect-timeout: 5s
      read-timeout: 10s
    reactiveclient:
      connect-timeout: 5s
      read-timeout: 10s
\`\`\`

### ✅ Spring Boot 4 (Unified)
\`\`\`yaml
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
\`\`\`

## Observability Configuration

### ❌ Spring Boot 3 (Jaeger)
\`\`\`yaml
management:
  tracing:
    jaeger:
      grpc:
        endpoint: http://localhost:14250
\`\`\`

### ✅ Spring Boot 4 (OpenTelemetry)
\`\`\`yaml
management:
  otlp:
    tracing:
      endpoint: http://localhost:4318
  observations:
    key-values:
      application: my-service
      environment: production
\`\`\`

#### Dependencies
\`\`\`xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-opentelemetry</artifactId>
</dependency>
\`\`\`

## Null Annotations

### ❌ Spring Boot 3 (Spring's Nullable)
\`\`\`java
import org.springframework.lang.Nullable;

@RestController
public class MyController {
    @GetMapping("/user/{id}")
    public User getUser(@Nullable String email) {
        // email is optional
    }
}
\`\`\`

### ✅ Spring Boot 4 (JSpecify)
\`\`\`java
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
\`\`\`

## HTTP Service Clients

### ❌ Spring Boot 3 (Manual REST templates)
\`\`\`java
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
\`\`\`

### ✅ Spring Boot 4 (@HttpExchange)
\`\`\`java
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
\`\`\`
```

---

## 📋 Template 3: agent-evals.yaml

```yaml
# tests/agent-evals.yaml
# Evaluation suite for Spring Boot 4 migration tasks
# Target: 95%+ pass rate with SPRINGBOOT-AGENTS.md

test_suite:
  metadata:
    framework: "Spring Boot"
    version: "4.0.0"
    date_created: "2026-01-31"
    baseline_pass_rate_without_docs: "45%"
    target_pass_rate_with_agents_md: "95%"

tests:
  - test_id: "01-java-baseline"
    title: "Java 21 Baseline Requirement"
    description: "Verify agent understands Java 21 is mandatory"
    prompt: |
      Create a pom.xml for a new Spring Boot 4 project. 
      What Java version should be configured?
      Show pom.xml properties section.
    expected_assertions:
      - "Contains <java.version>21</java.version>"
      - "No Java 20 or earlier mentioned"
      - "maven.compiler.source and target both 21"
    pass_criteria: "All assertions true"
    
  - test_id: "02-javax-to-jakarta-migration"
    title: "Package Migration: javax.* → jakarta.*"
    description: "Migrate Spring Boot 3 code to use jakarta packages"
    prompt: |
      Migrate this Spring Boot 3 code to Spring Boot 4:
      ```java
      import javax.servlet.http.HttpServletRequest;
      import javax.annotation.PostConstruct;
      import javax.persistence.Entity;
      import javax.persistence.Id;
      
      @Entity
      public class User {
          @Id
          private Long id;
          
          @PostConstruct
          public void init() { }
      }
      ```
    expected_assertions:
      - "No javax.* imports remain"
      - "All imports use jakarta.*"
      - "Compiles without errors"
      - "Pattern: import jakarta.servlet.http.HttpServletRequest"
    pass_criteria: "All assertions true"
    
  - test_id: "03-native-api-versioning"
    title: "Native API Versioning Implementation"
    description: "Implement Spring Boot 4 native API versioning"
    prompt: |
      Create a Spring Boot 4 REST controller with native API versioning.
      Implement /api/products endpoint with two versions:
      - v4.0: Returns { id, name, price }
      - v4.1: Returns { id, name, price, stock, lastUpdated }
      Use path-based versioning (/api/v4.0/products, /api/v4.1/products)
    expected_assertions:
      - "Uses @Version annotation"
      - "Declares versions 4.0 and 4.1"
      - "Uses jakarta.* imports"
      - "Single controller with multiple @PostMapping methods"
      - "Configuration for path-based versioning present"
      - "No javax.* imports"
    pass_criteria: "All assertions true"
    
  - test_id: "04-http-clients-configuration"
    title: "HTTP Clients Configuration Namespace Update"
    description: "Migrate from deprecated HTTP config to unified namespace"
    prompt: |
      Update this Spring Boot 3 application.yml to Spring Boot 4:
      ```yaml
      spring:
        http:
          client:
            connect-timeout: 5s
          reactiveclient:
            read-timeout: 10s
      ```
    expected_assertions:
      - "Uses spring.http.clients.* namespace"
      - "No spring.http.client.* or reactiveclient.* properties"
      - "Contains default or custom client configurations"
      - "YAML validates without errors"
    pass_criteria: "All assertions true"
    
  - test_id: "05-jspecify-null-annotations"
    title: "JSpecify Null Annotations Migration"
    description: "Migrate from Spring's Nullable to JSpecify"
    prompt: |
      Update this REST controller to use Spring Boot 4 null annotations:
      ```java
      import org.springframework.lang.Nullable;
      
      @RestController
      @RequestMapping("/api/users")
      public class UserController {
          @GetMapping("/{id}")
          public User getUser(@RequestParam @Nullable String email) {
              // email is optional
          }
      }
      ```
    expected_assertions:
      - "Uses org.jspecify.annotations.Nullable"
      - "No org.springframework.lang.Nullable imports"
      - "Uses jakarta.* for servlet/annotation imports"
      - "Code compiles and is functionally equivalent"
    pass_criteria: "All assertions true"
    
  - test_id: "06-opentelemetry-observability"
    title: "OpenTelemetry Observability Configuration"
    description: "Migrate observability from Jaeger to OpenTelemetry"
    prompt: |
      Update management configuration from Jaeger to OpenTelemetry:
      ```yaml
      management:
        tracing:
          jaeger:
            grpc:
              endpoint: http://localhost:14250
      ```
    expected_assertions:
      - "Uses management.otlp.tracing.endpoint"
      - "No jaeger configuration present"
      - "Includes spring-boot-starter-opentelemetry dependency"
      - "YAML is valid"
    pass_criteria: "All assertions true"
    
  - test_id: "07-http-exchange-service-client"
    title: "Spring Boot 4 HTTP Service Clients (@HttpExchange)"
    description: "Implement new HTTP service client pattern"
    prompt: |
      Create a Spring Boot 4 HTTP service client using @HttpExchange
      for a remote Orders API at http://api.example.com/orders
      Requirements:
      - Interface with @GetExchange and @PostExchange methods
      - Configuration bean to create client
      - Service class that uses the client
    expected_assertions:
      - "Defines @HttpExchange interface"
      - "@GetExchange and @PostExchange annotations present"
      - "HttpServiceProxyFactory used for client creation"
      - "Service injects the client via constructor"
      - "Uses jakarta.* imports"
      - "No RestTemplate/WebClient boilerplate"
    pass_criteria: "All assertions true"
    
  - test_id: "08-deprecated-api-identification"
    title: "Identify and Flag Deprecated APIs"
    description: "Recognize Spring Boot 3 deprecated patterns"
    prompt: |
      Review this Spring Boot 3 code and flag deprecated patterns 
      for Spring Boot 4 migration:
      [Show example with multiple deprecated APIs]
    expected_assertions:
      - "Identifies all javax.* imports"
      - "Flags spring.lang.Nullable annotations"
      - "Identifies deprecated HTTP config namespace"
      - "Provides replacement for each deprecated pattern"
    pass_criteria: "Identifies 90%+ of deprecated patterns"
    
  - test_id: "09-end-to-end-migration"
    title: "End-to-End Service Migration"
    description: "Migrate complete Spring Boot 3 service to Boot 4"
    prompt: |
      Migrate this complete Spring Boot 3 service to Spring Boot 4:
      - Update pom.xml (version, Java, dependencies)
      - Migrate all javax.* → jakarta.*
      - Update application.yml configurations
      - Replace deprecated APIs with Boot 4 equivalents
      - Ensure all tests pass
      [Provide full service code]
    expected_assertions:
      - "No javax.* imports"
      - "pom.xml declares Spring Boot 4.0.0+ and Java 21"
      - "application.yml uses new config namespaces"
      - "All deprecated patterns replaced"
      - "Code compiles without errors"
      - "Tests pass (if provided)"
    pass_criteria: "All assertions true"
    
  - test_id: "10-production-readiness-checklist"
    title: "Production Readiness Verification"
    description: "Verify Spring Boot 4 migration is production-ready"
    prompt: |
      A team is about to deploy a Spring Boot 4 migrated application.
      Provide a pre-deployment checklist.
    expected_assertions:
      - "Includes Java 21+ verification step"
      - "References test execution (unit + integration)"
      - "Includes verification for zero javax imports"
      - "Covers configuration validation"
      - "Includes native image build (if applicable)"
      - "Covers observability/monitoring verification"
      - "Includes staged rollout strategy"
    pass_criteria: "Checklist covers 80%+ of migration concerns"

evaluation_criteria:
  pass_rate_calculation: "Number of passing tests / Total tests"
  target_success_metrics:
    - baseline_without_docs: "45%"
    - with_agents_md_embedded: "95%"
    - minimum_acceptable: "80%"
  
  test_execution:
    - Each test should be executable/verifiable
    - Retry failed tests 2 times to account for model variance
    - Document failure reason if test fails consistently
    
  scoring:
  - All assertions true: "PASS"
  - 90%+ assertions true: "PASS_WITH_WARNINGS"
  - <90% assertions true: "FAIL"

success_criteria:
  overall_pass_rate: "≥95%"
  minimum_passing_tests: "9 out of 10"
  consistency: "Should not vary >5% across 3 runs"
```

---

## 🎯 Template 4: pom.xml for Spring Boot 4

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <!-- Spring Boot 4.0.0+ BOM -->
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>4.0.0</version>
        <relativePath/>
    </parent>

    <groupId>com.example</groupId>
    <artifactId>my-spring-boot-4-app</artifactId>
    <version>1.0.0</version>
    <name>My Spring Boot 4 Application</name>

    <properties>
        <!-- ✅ Java 21 is MANDATORY for Spring Boot 4 -->
        <java.version>21</java.version>
        <maven.compiler.source>21</maven.compiler.source>
        <maven.compiler.target>21</maven.compiler.target>
        <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    </properties>

    <dependencies>
        <!-- Web Starter (includes Tomcat, Spring MVC, Jackson) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>

        <!-- Data JPA (includes Hibernate, JPA) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>

        <!-- Spring Security 6.4 (latest for Boot 4) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>

        <!-- OpenTelemetry for observability (Boot 4 recommended) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-opentelemetry</artifactId>
        </dependency>

        <!-- Micrometer for metrics -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>

        <!-- Validation (uses jakarta.validation) -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>

        <!-- H2 Database (for dev/test) -->
        <dependency>
            <groupId>com.h2database</groupId>
            <artifactId>h2</artifactId>
            <scope>runtime</scope>
        </dependency>

        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>

        <dependency>
            <groupId>org.springframework.security</groupId>
            <artifactId>spring-security-test</artifactId>
            <scope>test</scope>
        </dependency>
    </dependencies>

    <build>
        <plugins>
            <!-- Spring Boot Maven Plugin -->
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <image>
                        <builder>paketobuildpacks/builder-jammy-base</builder>
                    </image>
                </configuration>
            </plugin>

            <!-- Compiler Plugin (Java 21) -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-compiler-plugin</artifactId>
                <version>3.11.0</version>
                <configuration>
                    <source>21</source>
                    <target>21</target>
                </configuration>
            </plugin>

            <!-- Surefire for Tests -->
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-surefire-plugin</artifactId>
                <version>3.0.0</version>
            </plugin>
        </plugins>
    </build>
</project>
```

---

## 📋 Summary

These templates provide:

1. ✅ **SPRINGBOOT-AGENTS.md** - Compressed index for agent context
2. ✅ **.springboot-4-docs/** - Organized documentation structure
3. ✅ **agent-evals.yaml** - Comprehensive test suite
4. ✅ **pom.xml** - Spring Boot 4 ready configuration

**Next Steps:**
1. Copy templates to your project
2. Customize documentation with your specific codebase patterns
3. Run evaluation suite against agents
4. Begin migration with AI assistance
