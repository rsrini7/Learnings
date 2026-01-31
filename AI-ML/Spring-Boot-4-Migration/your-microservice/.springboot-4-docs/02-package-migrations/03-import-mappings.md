# Import Mappings Quick Reference

## Quick Lookup Table

| Old Import (javax.*) | New Import (jakarta.*) |
|---------------------|------------------------|
| `import javax.servlet.http.HttpServletRequest;` | `import jakarta.servlet.http.HttpServletRequest;` |
| `import javax.servlet.http.HttpServletResponse;` | `import jakarta.servlet.http.HttpServletResponse;` |
| `import javax.servlet.Filter;` | `import jakarta.servlet.Filter;` |
| `import javax.persistence.Entity;` | `import jakarta.persistence.Entity;` |
| `import javax.persistence.Id;` | `import jakarta.persistence.Id;` |
| `import javax.persistence.EntityManager;` | `import jakarta.persistence.EntityManager;` |
| `import javax.validation.Valid;` | `import jakarta.validation.Valid;` |
| `import javax.validation.constraints.NotNull;` | `import jakarta.validation.constraints.NotNull;` |
| `import javax.annotation.PostConstruct;` | `import jakarta.annotation.PostConstruct;` |
| `import javax.annotation.PreDestroy;` | `import jakarta.annotation.PreDestroy;` |
| `import javax.inject.Inject;` | `import jakarta.inject.Inject;` |
| `import javax.inject.Named;` | `import jakarta.inject.Named;` |
| `import javax.transaction.Transactional;` | `import jakarta.transaction.Transactional;` |

## Automated Migration Scripts

### PowerShell Script (Windows)
```powershell
# migrate-to-jakarta.ps1
$files = Get-ChildItem -Path . -Filter *.java -Recurse

foreach ($file in $files) {
    $content = Get-Content $file.FullName
    $updated = $content -replace 'import javax\.', 'import jakarta.'
    $updated | Set-Content $file.FullName
}

Write-Host "Migration complete. Files updated: $($files.Count)"
```

### Bash Script (macOS/Linux)
```bash
#!/bin/bash
# migrate-to-jakarta.sh

find . -name "*.java" -type f -print0 | while IFS= read -r -d '' file; do
    sed -i '' 's/import javax\./import jakarta./g' "$file"
done

echo "Migration complete"
```

### Python Script (Cross-platform)
```python
#!/usr/bin/env python3
# migrate_to_jakarta.py

import os
import re

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    updated = re.sub(r'import javax\.', 'import jakarta.', content)
    
    if content != updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return True
    return False

count = 0
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.java'):
            filepath = os.path.join(root, file)
            if migrate_file(filepath):
                count += 1

print(f"Migration complete. Files updated: {count}")
```

## Maven OpenRewrite Configuration

Add to your `pom.xml`:

```xml
<build>
    <plugins>
        <plugin>
            <groupId>org.openrewrite.maven</groupId>
            <artifactId>rewrite-maven-plugin</artifactId>
            <version>5.3.0</version>
            <configuration>
                <activeRecipes>
                    <recipe>org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta</recipe>
                </activeRecipes>
            </configuration>
            <dependencies>
                <dependency>
                    <groupId>org.openrewrite.recipe</groupId>
                    <artifactId>rewrite-migrate-java</artifactId>
                    <version>2.0.0</version>
                </dependency>
            </dependencies>
        </plugin>
    </plugins>
</build>
```

Run migration:
```bash
./mvnw rewrite:run
```

## Gradle OpenRewrite Configuration

Add to your `build.gradle`:

```gradle
plugins {
    id 'org.openrewrite.rewrite' version '6.1.0'
}

rewrite {
    activeRecipe('org.openrewrite.java.migrate.jakarta.JavaxMigrationToJakarta')
}

dependencies {
    rewrite('org.openrewrite.recipe:rewrite-migrate-java:2.0.0')
}
```

Run migration:
```bash
./gradlew rewriteRun
```

## Post-Migration Verification

### Verification Script (PowerShell)
```powershell
# verify-migration.ps1
$javaxImports = Get-ChildItem -Path . -Filter *.java -Recurse | 
    Select-String -Pattern "import javax\." | 
    Select-Object -ExpandProperty Line

if ($javaxImports.Count -eq 0) {
    Write-Host "✅ SUCCESS: No javax.* imports found" -ForegroundColor Green
} else {
    Write-Host "❌ FAILED: Found $($javaxImports.Count) javax.* imports" -ForegroundColor Red
    $javaxImports | ForEach-Object { Write-Host $_ }
}
```

### Verification Script (Bash)
```bash
#!/bin/bash
# verify-migration.sh

count=$(grep -r "import javax\." --include="*.java" . | wc -l)

if [ $count -eq 0 ]; then
    echo "✅ SUCCESS: No javax.* imports found"
    exit 0
else
    echo "❌ FAILED: Found $count javax.* imports"
    grep -r "import javax\." --include="*.java" .
    exit 1
fi
```

## CI/CD Integration

### GitHub Actions
```yaml
name: Verify Jakarta Migration

on: [push, pull_request]

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for javax imports
        run: |
          if grep -r "import javax\." --include="*.java" .; then
            echo "❌ Found javax.* imports"
            exit 1
          else
            echo "✅ No javax.* imports found"
          fi
```

### GitLab CI
```yaml
verify-jakarta:
  stage: test
  script:
    - |
      if grep -r "import javax\." --include="*.java" .; then
        echo "❌ Found javax.* imports"
        exit 1
      else
        echo "✅ No javax.* imports found"
      fi
```

## Common Issues and Solutions

### Issue: Compilation Errors After Migration
**Solution**: Ensure all dependencies are updated to Jakarta-compatible versions

### Issue: Mixed javax/jakarta Imports
**Solution**: Run verification script and fix remaining javax imports

### Issue: Third-party Libraries Still Using javax
**Solution**: Update library versions or find Jakarta-compatible alternatives

### Issue: Test Files Not Migrated
**Solution**: Ensure migration scripts include `src/test/java` directory
