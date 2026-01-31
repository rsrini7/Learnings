# Common Package Migrations

## Servlet API

### HTTP Servlet
```java
// ❌ Spring Boot 3
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import javax.servlet.http.Cookie;

// ✅ Spring Boot 4
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.http.HttpSession;
import jakarta.servlet.http.Cookie;
```

### Filters and Listeners
```java
// ❌ Spring Boot 3
import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.ServletContextListener;

// ✅ Spring Boot 4
import jakarta.servlet.Filter;
import jakarta.servlet.FilterChain;
import jakarta.servlet.ServletException;
import jakarta.servlet.ServletContextListener;
```

## JPA/Persistence API

### Entity Annotations
```java
// ❌ Spring Boot 3
import javax.persistence.Entity;
import javax.persistence.Table;
import javax.persistence.Id;
import javax.persistence.GeneratedValue;
import javax.persistence.Column;
import javax.persistence.ManyToOne;
import javax.persistence.OneToMany;

// ✅ Spring Boot 4
import jakarta.persistence.Entity;
import jakarta.persistence.Table;
import jakarta.persistence.Id;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Column;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
```

### Entity Manager
```java
// ❌ Spring Boot 3
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.persistence.Query;

// ✅ Spring Boot 4
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.persistence.Query;
```

## Validation API

### Constraint Annotations
```java
// ❌ Spring Boot 3
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.Size;
import javax.validation.constraints.Email;
import javax.validation.constraints.Min;
import javax.validation.constraints.Max;

// ✅ Spring Boot 4
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.Size;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.Max;
```

### Validator
```java
// ❌ Spring Boot 3
import javax.validation.Validator;
import javax.validation.ConstraintViolation;

// ✅ Spring Boot 4
import jakarta.validation.Validator;
import jakarta.validation.ConstraintViolation;
```

## Annotation API

### Lifecycle Annotations
```java
// ❌ Spring Boot 3
import javax.annotation.PostConstruct;
import javax.annotation.PreDestroy;
import javax.annotation.Resource;

// ✅ Spring Boot 4
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import jakarta.annotation.Resource;
```

### Null Safety (Note: Use JSpecify instead)
```java
// ❌ Spring Boot 3
import javax.annotation.Nullable;
import javax.annotation.Nonnull;

// ⚠️ Spring Boot 4 (jakarta, but JSpecify is preferred)
import jakarta.annotation.Nullable;
import jakarta.annotation.Nonnull;

// ✅ Spring Boot 4 (RECOMMENDED)
import org.jspecify.annotations.Nullable;
import org.jspecify.annotations.NullMarked;
```

## Dependency Injection

### Inject Annotations
```java
// ❌ Spring Boot 3
import javax.inject.Inject;
import javax.inject.Named;
import javax.inject.Singleton;

// ✅ Spring Boot 4
import jakarta.inject.Inject;
import jakarta.inject.Named;
import jakarta.inject.Singleton;
```

## Transaction API

### Transaction Management
```java
// ❌ Spring Boot 3
import javax.transaction.Transactional;
import javax.transaction.TransactionManager;

// ✅ Spring Boot 4
import jakarta.transaction.Transactional;
import jakarta.transaction.TransactionManager;
```

## Complete Example: REST Controller

### Before (Spring Boot 3)
```java
package com.example.controller;

import javax.servlet.http.HttpServletRequest;
import javax.validation.Valid;
import javax.validation.constraints.NotNull;
import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.annotation.PostConstruct;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @PostConstruct
    public void init() {
        // Initialization logic
    }
    
    @PostMapping
    public User createUser(@Valid @RequestBody UserRequest request, 
                          HttpServletRequest servletRequest) {
        // Implementation
    }
}
```

### After (Spring Boot 4)
```java
package com.example.controller;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import jakarta.persistence.EntityManager;
import jakarta.persistence.PersistenceContext;
import jakarta.annotation.PostConstruct;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    
    @PersistenceContext
    private EntityManager entityManager;
    
    @PostConstruct
    public void init() {
        // Initialization logic
    }
    
    @PostMapping
    public User createUser(@Valid @RequestBody UserRequest request, 
                          HttpServletRequest servletRequest) {
        // Implementation
    }
}
```

## Verification Checklist

After migration, verify:
- [ ] All `javax.servlet.*` → `jakarta.servlet.*`
- [ ] All `javax.persistence.*` → `jakarta.persistence.*`
- [ ] All `javax.validation.*` → `jakarta.validation.*`
- [ ] All `javax.annotation.*` → `jakarta.annotation.*`
- [ ] All `javax.inject.*` → `jakarta.inject.*`
- [ ] All `javax.transaction.*` → `jakarta.transaction.*`
- [ ] Run: `grep -r "import javax" --include="*.java" .` → 0 results
- [ ] Compile: `./mvnw clean compile` → Success
