# Spring Boot 4 Migration Checklist

## Pre-Migration Preparation

### Environment Setup
- [ ] Install Java 21 (verify with `java -version`)
- [ ] Update Maven to 3.9.0+ or Gradle to 8.4+
- [ ] Backup current codebase (git commit/tag)
- [ ] Create feature branch for migration
- [ ] Review Spring Boot 4 release notes

### Dependency Audit
- [ ] List all third-party dependencies
- [ ] Check Spring Boot 4 compatibility for each
- [ ] Identify deprecated dependencies
- [ ] Plan dependency update strategy

## Phase 1: Dependencies (Day 1)

### Update Build Configuration
- [ ] Update Spring Boot version to 4.0.0+ in pom.xml/build.gradle
- [ ] Set Java version to 21
- [ ] Update Maven compiler plugin (if using Maven)
- [ ] Run `./mvnw clean compile` or `./gradlew clean build`
- [ ] Fix any compilation errors

### Verification Commands
```bash
# Verify Java version
java -version  # Must show Java 21+

# Verify Maven version
./mvnw --version  # Must show Maven 3.9.0+

# Verify Gradle version
./gradlew --version  # Must show Gradle 8.4+

# Clean build
./mvnw clean compile
```

## Phase 2: Package Migrations (Day 1-2)

### javax.* → jakarta.* Migration
- [ ] Run find & replace: `javax.` → `jakarta.`
- [ ] Verify all imports updated
- [ ] Check XML configuration files
- [ ] Update annotations in test files

### Verification Commands
```bash
# Check for remaining javax imports
grep -r "import javax" --include="*.java" src/
# Expected: 0 results

# Check XML files
grep -r "javax\." --include="*.xml" src/
# Expected: 0 results

# Compile to verify
./mvnw clean compile
```

### Common Package Migrations
- [ ] `javax.servlet.*` → `jakarta.servlet.*`
- [ ] `javax.persistence.*` → `jakarta.persistence.*`
- [ ] `javax.validation.*` → `jakarta.validation.*`
- [ ] `javax.annotation.*` → `jakarta.annotation.*`
- [ ] `javax.inject.*` → `jakarta.inject.*`

## Phase 3: Configuration Updates (Day 2-3)

### Application Configuration
- [ ] Update `application.yml` or `application.properties`
- [ ] Migrate HTTP client configuration to `spring.http.clients.*`
- [ ] Update observability configuration to OpenTelemetry
- [ ] Review and update actuator endpoints

### Configuration Migration Examples
```yaml
# Update HTTP client config
# OLD: spring.http.client.*
# NEW: spring.http.clients.default.*

# Update observability
# OLD: management.tracing.jaeger.*
# NEW: management.otlp.tracing.*
```

### Verification
- [ ] Run `./mvnw clean test`
- [ ] Check application startup logs
- [ ] Verify no deprecation warnings

## Phase 4: API & Feature Audit (Day 3-4)

### Null Annotations
- [ ] Replace `org.springframework.lang.Nullable` with `org.jspecify.annotations.Nullable`
- [ ] Add `@Nonnull` where appropriate
- [ ] Update method signatures

### New Features (Optional)
- [ ] Consider native API versioning with `@Version`
- [ ] Evaluate `@HttpExchange` for HTTP clients
- [ ] Review OpenTelemetry observability features

### Code Review
- [ ] Review all controllers
- [ ] Review all services
- [ ] Review all repositories
- [ ] Review all configuration classes

## Phase 5: Testing & Deployment (Day 4-5)

### Unit Testing
- [ ] Run all unit tests: `./mvnw test`
- [ ] Fix failing tests
- [ ] Update test dependencies if needed
- [ ] Verify test coverage maintained

### Integration Testing
- [ ] Run integration tests: `./mvnw verify`
- [ ] Test database connections
- [ ] Test external API integrations
- [ ] Test security configurations

### Performance Testing
- [ ] Run performance benchmarks
- [ ] Compare with Spring Boot 3 baseline
- [ ] Check memory usage
- [ ] Check startup time

### Deployment Preparation
- [ ] Update CI/CD pipelines for Java 21
- [ ] Update Docker base images
- [ ] Update deployment manifests
- [ ] Prepare rollback plan

### Staging Deployment
- [ ] Deploy to staging environment
- [ ] Run smoke tests
- [ ] Monitor logs for errors
- [ ] Validate all endpoints
- [ ] Check observability metrics

### Production Deployment
- [ ] Create deployment plan
- [ ] Schedule maintenance window
- [ ] Deploy to production (gradual rollout recommended)
- [ ] Monitor error rates
- [ ] Monitor performance metrics
- [ ] Verify observability data collection

## Post-Migration Validation

### Code Quality
- [ ] Zero `javax.*` imports: `grep -r "import javax" --include="*.java" src/`
- [ ] All tests passing: `./mvnw clean verify`
- [ ] No compilation warnings
- [ ] No deprecation warnings

### Runtime Validation
- [ ] Application starts successfully
- [ ] All endpoints responding
- [ ] Database connections working
- [ ] External integrations working
- [ ] Metrics being collected
- [ ] Logs being generated properly

### Documentation
- [ ] Update README with Java 21 requirement
- [ ] Update deployment documentation
- [ ] Document any breaking changes for API consumers
- [ ] Update team wiki/knowledge base

## Rollback Plan

### If Issues Occur
- [ ] Revert to previous Spring Boot 3 version
- [ ] Restore Java 17/20 configuration
- [ ] Deploy previous working version
- [ ] Document issues encountered
- [ ] Plan remediation strategy

## Success Criteria

✅ All tests passing (100%)
✅ Zero `javax.*` imports
✅ Application compiles without errors
✅ No runtime errors in staging
✅ Performance metrics acceptable
✅ Observability working correctly
✅ Team trained on new features
