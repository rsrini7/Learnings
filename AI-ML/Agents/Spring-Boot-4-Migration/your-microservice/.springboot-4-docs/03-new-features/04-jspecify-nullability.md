# Spring Boot 4: JSpecify Null Annotations

## Overview
Spring Boot 4 adopts JSpecify as the standard for null-safety annotations, replacing Spring's proprietary `@Nullable` annotations.

## Migration

### Old Pattern (Spring Boot 3)

```java
// ❌ Spring Boot 3 - Spring's proprietary annotations
import org.springframework.lang.Nullable;
import org.springframework.lang.NonNull;

@RestController
public class UserController {
    
    @GetMapping("/user/{id}")
    public User getUser(@Nullable String email) {
        // email is optional
    }
    
    @PostMapping("/user")
    public User createUser(@NonNull CreateUserRequest request) {
        // request is required
    }
}
```

### New Pattern (Spring Boot 4)

```java
// ✅ Spring Boot 4 - JSpecify standard annotations
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NullMarked;

@RestController
@NullMarked  // All parameters/returns are non-null by default
public class UserController {
    
    @GetMapping("/user/{id}")
    public User getUser(@Nullable String email) {
        // email is explicitly nullable
    }
    
    @PostMapping("/user")
    public User createUser(CreateUserRequest request) {
        // request is non-null by default (due to @NullMarked)
    }
}
```

## Setup

### Add Dependency

```xml
<dependency>
    <groupId>org.jspecify</groupId>
    <artifactId>jspecify</artifactId>
    <version>1.0.0</version>
</dependency>
```

### Gradle
```gradle
implementation 'org.jspecify:jspecify:1.0.0'
```

## Key Annotations

### @NullMarked
Marks a package, class, or method where all types are non-null by default.

```java
@NullMarked
package com.example.service;

// All parameters and return types in this package are non-null by default
```

```java
@NullMarked
public class OrderService {
    // All methods in this class have non-null parameters/returns by default
    
    public Order getOrder(String id) {
        // id is non-null
        // return value is non-null
    }
}
```

### @Nullable
Explicitly marks a type as nullable.

```java
import org.jspecify.annotations.Nullable;

public class UserService {
    
    public @Nullable User findUserByEmail(String email) {
        // May return null if user not found
    }
    
    public void updateUser(String id, @Nullable String newEmail) {
        // newEmail can be null
    }
}
```

### @NullUnmarked
Opts out of null-safety checking for a specific scope.

```java
import org.jspecify.annotations.NullUnmarked;

@NullUnmarked
public class LegacyService {
    // Null-safety not enforced here
}
```

## Common Patterns

### Optional Parameters

```java
@NullMarked
@RestController
public class ProductController {
    
    @GetMapping("/products")
    public List<Product> searchProducts(
        @RequestParam String category,
        @RequestParam @Nullable String brand,
        @RequestParam @Nullable Integer minPrice
    ) {
        // category is required
        // brand and minPrice are optional
    }
}
```

### Nullable Return Values

```java
@NullMarked
@Service
public class CacheService {
    
    public @Nullable Order getCachedOrder(String id) {
        // Returns null if not in cache
        return cache.get(id);
    }
    
    public Order getOrFetchOrder(String id) {
        Order cached = getCachedOrder(id);
        if (cached != null) {
            return cached;
        }
        return fetchFromDatabase(id);
    }
}
```

### Collections

```java
@NullMarked
public class OrderService {
    
    // List itself is non-null, but may contain null elements
    public List<@Nullable Order> getPendingOrders() {
        // Some orders might be null
    }
    
    // List is non-null and contains only non-null elements
    public List<Order> getCompletedOrders() {
        // All orders are guaranteed non-null
    }
    
    // List itself might be null
    public @Nullable List<Order> getArchivedOrders() {
        // Might return null if no archived orders
    }
}
```

### Generic Types

```java
@NullMarked
public class Repository<T> {
    
    public @Nullable T findById(String id) {
        // May return null if not found
    }
    
    public List<T> findAll() {
        // List is non-null, elements are non-null
    }
    
    public List<@Nullable T> findAllWithDeleted() {
        // List is non-null, but may contain null elements
    }
}
```

## Integration with IDE

### IntelliJ IDEA
1. Settings → Build, Execution, Deployment → Compiler
2. Enable "Add runtime assertions for notnull-annotated methods and parameters"
3. Configure JSpecify as the null-safety framework

### VS Code
1. Install "Java Extension Pack"
2. Configure null-safety checking in settings.json:
```json
{
  "java.compile.nullAnalysis.mode": "automatic",
  "java.compile.nullAnalysis.nonnull": [
    "org.jspecify.annotations.NonNull"
  ],
  "java.compile.nullAnalysis.nullable": [
    "org.jspecify.annotations.Nullable"
  ]
}
```

## Static Analysis

### SpotBugs Configuration

```xml
<plugin>
    <groupId>com.github.spotbugs</groupId>
    <artifactId>spotbugs-maven-plugin</artifactId>
    <version>4.7.3.0</version>
    <configuration>
        <effort>Max</effort>
        <threshold>Low</threshold>
        <plugins>
            <plugin>
                <groupId>com.h3xstream.findsecbugs</groupId>
                <artifactId>findsecbugs-plugin</artifactId>
                <version>1.12.0</version>
            </plugin>
        </plugins>
    </configuration>
</plugin>
```

### NullAway (Uber's null-checker)

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-compiler-plugin</artifactId>
    <version>3.11.0</version>
    <configuration>
        <compilerArgs>
            <arg>-Xplugin:NullAway -XepOpt:NullAway:AnnotatedPackages=com.example</arg>
        </compilerArgs>
    </configuration>
</plugin>
```

## Testing

```java
import org.junit.jupiter.api.Test;
import static org.assertj.core.api.Assertions.*;

@NullMarked
class UserServiceTest {
    
    @Test
    void testNullableReturn() {
        UserService service = new UserService();
        
        // May return null
        User user = service.findUserByEmail("unknown@example.com");
        
        // Safe null check
        if (user != null) {
            assertThat(user.getEmail()).isNotNull();
        }
    }
    
    @Test
    void testNonNullParameter() {
        UserService service = new UserService();
        
        // This should fail at compile time with proper IDE setup
        // service.getUser(null);  // Compile error
        
        // This is safe
        User user = service.getUser("123");
        assertThat(user).isNotNull();
    }
}
```

## Benefits

✅ **Industry Standard**: JSpecify is vendor-neutral
✅ **Better IDE Support**: Works with all major IDEs
✅ **Compile-Time Safety**: Catch null pointer errors before runtime
✅ **Documentation**: Makes API contracts explicit
✅ **Interoperability**: Works with Kotlin, other JVM languages
✅ **Gradual Adoption**: Can be applied incrementally

## Migration Checklist

- [ ] Add JSpecify dependency
- [ ] Replace `org.springframework.lang.Nullable` with `org.jspecify.annotations.Nullable`
- [ ] Replace `org.springframework.lang.NonNull` with default non-null (via `@NullMarked`)
- [ ] Add `@NullMarked` to packages or classes
- [ ] Configure IDE for null-safety checking
- [ ] Run static analysis tools
- [ ] Update tests to verify null-safety
