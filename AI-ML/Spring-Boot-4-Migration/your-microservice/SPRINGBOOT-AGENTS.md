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
