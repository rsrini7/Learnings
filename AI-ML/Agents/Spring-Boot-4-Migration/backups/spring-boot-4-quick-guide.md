# Spring Boot 4 Migration: AI Agent-Driven Strategy
## Executive Summary & Quick Implementation Guide

---

## 🎯 Core Pattern: Why AGENTS.md > Skills

### The Vercel Discovery
```
Baseline (no docs):                 53% ✗
Skills (agents ignored):            53% ✗
Skills (with explicit prompts):     79% ⚠️ (fragile)
AGENTS.md (embedded index):        100% ✅ (reliable)
```

### Three Reasons Why
1. **No decision point** → Agent doesn't decide "should I load this?"
2. **Persistent context** → Available every turn
3. **Compressed efficiently** → 8KB index, not 40KB full docs

---

## 🚀 Quick Start (3-Step Implementation)

### Step 1: Create Documentation Structure (4 hours)
```bash
mkdir -p .springboot-4-docs/{01-migration-overview,02-package-migrations,03-new-features,04-deprecated-apis,05-dependency-updates,06-common-patterns}

# Key files to create:
# .springboot-4-docs/01-migration-overview/01-java-baseline.md
# .springboot-4-docs/02-package-migrations/01-javax-to-jakarta.md
# .springboot-4-docs/03-new-features/01-api-versioning.md
# .springboot-4-docs/04-deprecated-apis/02-replacement-patterns.md
# ... (see detailed guide for all)
```

### Step 2: Create Compressed Index (1 hour)
```markdown
# SPRINGBOOT-AGENTS.md (at project root)

[Spring Boot 4 Docs Index]|root: ./.springboot-4-docs|
CRITICAL: Java 21+ MANDATORY - javax.* → jakarta.*|
IMPORTANT: Prefer retrieval-led reasoning|
01-migration-overview:{...files...}|
02-package-migrations:{...files...}|
... (pipe-delimited, 8KB compressed format)
```

### Step 3: Create Evaluation Suite (2 hours)
```yaml
# tests/agent-evals.yaml
tests:
  - id: "api-versioning-basic"
    input: "Create Spring Boot 4 native versioning endpoint"
    assertions: ["@Version annotation present", "No javax imports", "Compiles"]
  
  - id: "package-migration"
    input: "Migrate javax.* to jakarta.*"
    assertions: ["No javax remains", "All jakarta.*", "Compiles"]
  
  - id: "http-clients-config"
    input: "Update to spring.http.clients.* namespace"
    assertions: ["Uses spring.http.clients.*", "No deprecated config"]
```

---

## 📋 Spring Boot 4 Migration Checklist

### Phase 1: Dependencies (Day 1)
- [ ] Java version: 17/20 → **Java 21+**
- [ ] Spring Boot: 3.x → **4.0.0+**
- [ ] Maven: → **3.9.0+** | Gradle: → **8.4+**
- [ ] Run: `./mvnw clean verify`

### Phase 2: Package Migrations (Day 1-2)
- [ ] Find & replace: `javax.*` → `jakarta.*`
- [ ] Verify: `grep -r "import javax" --include="*.java" .` → 0 results
- [ ] Annotations: `org.springframework.lang.Nullable` → `org.jspecify.annotations.Nullable`

### Phase 3: Configuration Updates (Day 2-3)
```yaml
# ❌ OLD (Spring Boot 3)
spring:
  http:
    client:
      connect-timeout: 5s

# ✅ NEW (Spring Boot 4)
spring:
  http:
    clients:
      default:
        connect-timeout: 5s
```

### Phase 4: API & Feature Audit (Day 3-4)
- [ ] Adopt native API versioning (if applicable)
- [ ] Update HTTP client patterns
- [ ] Review observability (OpenTelemetry)

### Phase 5: Testing & Deployment (Day 4-5)
- [ ] Unit & integration tests pass
- [ ] Native image builds (if applicable)
- [ ] Staging deployment
- [ ] Gradual production rollout

---

## 🔄 Critical Migrations

### #1: Package Migration
```java
// ❌ Before (Spring Boot 3)
import javax.servlet.http.HttpServletRequest;
import javax.annotation.PostConstruct;
import javax.inject.Named;

// ✅ After (Spring Boot 4)
import jakarta.servlet.http.HttpServletRequest;
import jakarta.annotation.PostConstruct;
import jakarta.inject.Named;
```

### #2: Native API Versioning
```java
// ❌ Before: Manual V1/V2 controllers
@RestController
@RequestMapping("/api/v1/orders")
public class OrderControllerV1 { }

// ✅ After: Single controller, native versioning
@RestController
@RequestMapping("/api/orders")
@Version("4.0")
public class OrderController {
    @PostMapping
    @Version("4.0")
    public ResponseEntity<Order> createOrder() { }
}
```

### #3: Configuration Namespace
```yaml
# ❌ Old (deprecated)
spring.http.client.connect-timeout

# ✅ New (unified)
spring.http.clients.default.connect-timeout
```

### #4: Null Annotations
```java
// ❌ Old
import org.springframework.lang.Nullable;
public void process(@Nullable String value) { }

// ✅ New (JSpecify)
import org.jspecify.annotations.Nullable;
public void process(@Nullable String value) { }
```

---

## 📊 Expected Results

| Metric | Without AGENTS.md | With AGENTS.md | Target |
|--------|---|---|---|
| **Agent Pass Rate** | 45% | 95% | ✅ 95%+ |
| **Manual Migration Time** | 5-7 days | 2-3 days | ✅ 2-3 days |
| **Documentation Coverage** | 60% | 100% | ✅ 100% |
| **Errors Caught** | 70% | 95% | ✅ 95%+ |

---

## 🛠️ Tools & Integration

### For Cursor / Claude Code
Add to `.cursor/config.json`:
```json
{
  "agentsConfig": {
    "contextFiles": ["SPRINGBOOT-AGENTS.md"],
    "retrievalPaths": [".springboot-4-docs/"]
  }
}
```

### For LangChain / Custom Agents
```python
# Load SPRINGBOOT-AGENTS.md as system context
with open("SPRINGBOOT-AGENTS.md") as f:
    context = f.read()

system_prompt = f"""
You are a Spring Boot 4 migration expert.

{context}

CRITICAL RULES:
1. Java 21+ only - no earlier versions
2. javax.* → jakarta.* always
3. Use spring.http.clients.* namespace
4. Use JSpecify @Nullable, not Spring's
"""
```

---

## 📁 Directory Structure

```
my-spring-boot-4-project/
├── SPRINGBOOT-AGENTS.md                    ← Compressed index
├── .springboot-4-docs/
│   ├── 01-migration-overview/
│   │   ├── 01-java-baseline.md
│   │   ├── 02-breaking-changes.md
│   │   └── 03-migration-checklist.md
│   ├── 02-package-migrations/
│   │   ├── 01-javax-to-jakarta.md
│   │   ├── 02-common-packages.md
│   │   └── 03-import-mappings.md
│   ├── 03-new-features/
│   │   ├── 01-api-versioning.md
│   │   ├── 02-http-clients.md
│   │   ├── 03-observability.md
│   │   └── 04-jspecify-nullability.md
│   ├── 04-deprecated-apis/
│   │   ├── 01-removed-in-4.0.md
│   │   ├── 02-replacement-patterns.md
│   │   └── 03-configuration-updates.md
│   ├── 05-dependency-updates/
│   │   ├── 01-maven-bom-updates.md
│   │   ├── 02-gradle-dependencies.md
│   │   └── 03-transitive-versions.md
│   └── 06-common-patterns/
│       ├── 01-spring-security-6.4.md
│       ├── 02-spring-data-updates.md
│       ├── 03-testing-changes.md
│       └── 04-actuator-updates.md
├── tests/
│   └── agent-evals.yaml                    ← Test suite
├── src/test/java/SpringBoot4MigrationTests.java
└── pom.xml (Spring Boot 4.0.0, Java 21)
```

---

## ⏱️ Implementation Timeline

| Week | Focus | Deliverables |
|------|-------|--------------|
| **Week 1** | Setup & Docs | `.springboot-4-docs/` (6 categories), `SPRINGBOOT-AGENTS.md` |
| **Week 2** | Testing | `agent-evals.yaml`, measure pass rates, refine docs |
| **Week 3** | Migration | Dependencies, packages, config, full test suite, deploy |

---

## 🎓 Key Takeaways

### From Vercel's Research
1. ✅ **Passive context beats active retrieval** - Embed docs, don't invoke skills
2. ✅ **Compression is critical** - 8KB works as well as 40KB
3. ✅ **No decision points** - Agent always has context available
4. ✅ **Retrieval-led reasoning** - Tell agent to consult docs

### For Spring Boot 4 Migration
1. ✅ **Create retrievable structure** - 6 categories, clear file hierarchy
2. ✅ **Compress efficiently** - Pipe-delimited index in root
3. ✅ **Embed critical rules** - Java 21+, javax→jakarta, config namespace
4. ✅ **Build eval suite** - Test against new APIs (api-versioning, http-clients, jspecify)
5. ✅ **Measure success** - Aim for 95%+ agent pass rate

---

## 🚦 Next Steps

1. **Today** - Read full strategy guide (`spring_boot_4_agent_migration_strategy.md`)
2. **Days 1-2** - Create `.springboot-4-docs/` with 6 categories
3. **Day 3** - Build `SPRINGBOOT-AGENTS.md` compressed index
4. **Days 4-5** - Create `agent-evals.yaml` and test with agents
5. **Week 2** - Begin actual Spring Boot 4 migration with AI assistance

---

**Questions?** Refer to detailed guide for:
- Complete file templates
- Exact migration commands
- Configuration examples
- Common pitfalls & solutions
