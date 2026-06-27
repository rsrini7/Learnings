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
```bash
find . -name "*.java" -type f | xargs sed -i '' 's/javax\./jakarta./g'
```

### Windows (PowerShell)
```powershell
Get-ChildItem -Path . -Filter *.java -Recurse | ForEach-Object {
    (Get-Content $_.FullName) -replace 'javax\.', 'jakarta.' | Set-Content $_.FullName
}
```

### Windows (Git Bash)
```bash
find . -name "*.java" -type f -exec sed -i 's/javax\./jakarta./g' {} +
```

### Using Maven Plugin
```bash
./mvnw org.openrewrite.maven:rewrite-maven-plugin:run \
  -Drewrite.recipeArtifactCoordinates=org.openrewrite.recipe:rewrite-spring:RELEASE \
  -Drewrite.activeRecipes=org.openrewrite.java.migrate.jakarta.AddCommonJakartaMigrations
```

## Verification

### Check for Remaining javax Imports
```bash
grep -r "import javax" --include="*.java" .
# Expected output: (empty - no results)

grep -r "import javax" --include="*.xml" .
grep -r "import javax" --include="*.properties" .
grep -r "import javax" --include="*.yml" .
# All should be empty
```

### Compile Check
```bash
./mvnw clean compile
# If any javax.* references remain, compilation will fail
# Error message will show the file and line number
```

## Common Cases Before/After

### Case 1: Servlet Imports
```java
// ❌ Before
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.Filter;

// ✅ After
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.Filter;
```

### Case 2: JPA/Persistence
```java
// ❌ Before
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Column;

// ✅ After
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Column;
```

### Case 3: Annotations
```java
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
```

### Case 4: Validation
```java
// ❌ Before
import javax.validation.Valid;
import javax.validation.constraints.NotNull;

// ✅ After
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
```

## Testing
After migration, run full test suite:
```bash
./mvnw clean test
# All tests should pass with zero javax.* references
```
