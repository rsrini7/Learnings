# Spec-Driven Development Frameworks: A Comprehensive White Paper

## Executive Summary

Spec-Driven Development (SDD) represents a paradigm shift from ad-hoc "vibe coding" to structured, systematic AI-assisted software development. This whitepaper provides an in-depth analysis of major spec-driven frameworks and AI coding systems:

- **BMAD** (Breakthrough Method of Agile AI-Driven Development)
- **Spec Kit** (GitHub's specification-driven toolkit)
- **OpenSpec** (Fission AI's lightweight spec framework)
- **Agent OS** (Builder Methods' context-engineered approach)
- **Google Conductor** (Context-driven development for Gemini CLI)
- **Serena** (IDE-level intelligence for AI coding agents)

Each framework addresses the core problem: AI agents generate better code when given clear specifications, architectural context, and systematic planning before implementation begins.


* Comparision with Rules / Skills: 
- [Agent-Specs-vs-Rules-vs-Skills](Agent-Specs-vs-Rules-vs-Skills.md)
- [Agent-sdd-uacf-skills-comparison](Agent-sdd-uacf-skills-comparison.md)

---

## Part 1: The Problem with Traditional AI Coding

### The "Vibe Coding" Problem

**Definition**
- Unstructured prompting into chat interfaces without pre-planning
- Requirements live in chat logs (impermanent, lossy context)
- AI generates code immediately without understanding architecture
- No formal specifications, just conversational requests

**Consequences**
- Inconsistent code quality and style across generated files
- Poor architectural decisions made ad-hoc during coding
- Security and performance considerations added as afterthoughts
- Difficult to iterate on requirements after implementation begins
- Team members using the same AI tools produce incompatible code
- Legacy codebases lack AI-friendly documentation

**The Fundamental Issue**
- LLMs perform better with explicit context and structure
- Without specs, agents make up architectural decisions
- Token usage explodes searching for context in large codebases
- No persistent record of design decisions and constraints

---

## Part 2: Spec-Driven Development Philosophy

### Core Principles

**1. Specification First**
- Write formal specs before any code generation
- Executable specifications define exact requirements, data models, APIs
- Specs become permanent artifacts in the codebase, not temporary docs
- Specifications drive all downstream implementation

**2. Context as Managed Artifact**
- Project context lives in markdown files alongside code
- Context is version-controlled and reviewed like code
- AI agents reference persistent context, not chat history
- Context grows with the project over time

**3. Planning Phase**
- Decompose specifications into actionable implementation plans
- Define technical architecture, data structures, service boundaries
- Create task breakdowns with clear dependencies
- Document critical decisions before coding starts

**4. Systematic Implementation**
- AI agents execute plans against existing code
- Each task links back to original specifications
- Changes are traceable throughout development lifecycle
- Implementation can be paused and resumed without losing context

**5. Human-Centered Control**
- Developers remain firmly in the driver's seat
- Review and approve specs before implementation
- Modify plans mid-flight if needed
- Keep oversight of architectural decisions

### Benefits Across the Development Lifecycle

**Code Quality**
- 56% reduction in time spent on programming (GitHub studies)
- Consistent code style and architectural patterns
- Security requirements built into initial specs, not bolted on later
- Design systems integrated from day one, not retrofitted

**Token Efficiency**
- Semantic code retrieval reduces context window requirements by 30-54%
- Structured planning prevents redundant code generation
- Less iteration needed due to clear specifications
- Smaller, focused AI contexts for each agent

**Team Coordination**
- New developers onboard faster via executable specifications
- Features feel cohesive even when built by different people
- Architectural decisions centralized and documented
- Brownfield (legacy) projects get AI-friendly documentation

**Flexibility**
- Requirement changes update specs → plans regenerate → implementation adapts
- Support for parallel implementations with different tech stacks
- Experimental features isolated in change proposals
- Easy rollback to previous checkpoint states

---

## Part 3: BMAD (Breakthrough Method of Agile AI-Driven Development)

### Overview

**Philosophy**
- Simulates an entire AI-powered development team with specialized roles
- Architect, Product Manager, Analyst, Scrum Master, Developer, QA agents
- Comprehensive agentic planning before code implementation
- Multi-agent collaboration with handoffs between phases

**Best For**
- Complex enterprise projects with intricate domain logic
- Greenfield development requiring deep architectural decisions
- Multi-repository systems requiring comprehensive planning
- Teams wanting AI to simulate agile team structure

**Not Ideal For**
- Small, simple feature additions to existing codebases
- Situations requiring lightweight, minimal overhead
- Projects without complex architectural needs

### Two-Phase Workflow

#### Phase 1: Agentic Planning

**Analyst Agent**
- Conducts market research and concept validation
- Creates detailed project brief
- Identifies competitive landscape and user needs
- Outputs: Project brief document

**Product Manager Agent**
- Generates comprehensive Product Requirements Document (PRD)
- Includes integrated epic definitions
- Details functional requirements and user stories
- Organizes requirements hierarchically
- Outputs: PRD with complete user story hierarchy

**Architect Agent**
- Reviews PRD and creates system architecture documents
- Defines service boundaries and data models
- Specifies technology selections and design patterns
- Documents scalability and performance considerations
- Outputs: Architecture design specifications

**Document Review & Approval**
- User reviews all planning outputs
- Provides feedback to agents
- Approves direction before Phase 2 begins
- Ensures alignment with actual project needs

**Epic Sharding** (Bridging Phase)
- PRD broken into focused, individual epic files
- Each epic preserves full context from planning phase
- Eliminates overwhelming context for development agents
- Creates manageable development units
- Command: `agent po` (Product Owner alignment)

#### Phase 2: Context-Engineered Development

**Scrum Master Agent**
- Takes sharded epic files
- Creates hyper-detailed user stories
- Includes full architectural context in story files
- Breaks stories into implementation tasks
- Outputs: Story files with complete context

**Developer Agent**
- Receives self-contained story files
- Has all necessary context from planning phases
- Implements code against existing codebase
- Outputs: Production code with tests

**QA Agent**
- Reviews generated code against original PRD requirements
- Ensures complete traceability from specification through implementation
- Validates functional requirements met
- Tests edge cases and error handling
- Outputs: QA reports and validated code

### Key Features

**Multi-Agent Orchestration**
- Different agents specialize in different roles
- Handoffs between agents preserve context via files
- Each agent optimized for specific task
- Agents can be customized with expansion packs

**Context Preservation**
- Planning outputs become input to development phase
- Full traceability from requirement to code
- No context loss between planning and development
- Agents see complete decision history

**Expansion Packs**
- Industry-specific configurations available
- Pre-built agents and workflows for common scenarios
- Customizable prompts and templates
- Community-contributed packs for various domains

**Version Control Integration**
- Artifacts stored in git repositories
- All decisions tracked and reviewable
- Epic sharding maintains version history
- Easy rollback to previous decision points

### Workflow Example: Building a Payment Processing System

**Phase 1: Planning**

```
Analyst Research:
├── Market research on payment platforms
├── Competitor analysis (Stripe, Square, PayPal)
├── Identify PCI-DSS compliance requirements
├── User persona analysis
└── Output: Project Brief (20-30 pages)

Product Manager PRD:
├── Epic 1: User Onboarding & Verification
│   ├── Story 1.1: Email verification
│   ├── Story 1.2: KYC documentation
│   └── Story 1.3: Account activation
├── Epic 2: Payment Processing Core
│   ├── Story 2.1: Payment creation
│   ├── Story 2.2: Payment status tracking
│   └── Story 2.3: Refund processing
├── Epic 3: Security & Compliance
│   ├── Story 3.1: Encryption implementation
│   ├── Story 3.2: Audit logging
│   └── Story 3.3: PCI-DSS validation
└── Output: 100+ page comprehensive PRD

Architect Design:
├── Service Architecture
│   ├── User Service (verification, profiles)
│   ├── Payment Service (transactions, refunds)
│   ├── Compliance Service (audit, reporting)
│   └── Security Service (encryption, secrets)
├── Data Models
│   ├── User schema with KYC data
│   ├── Transaction schema with full history
│   ├── Audit log schema
│   └── Encryption key management
├── API Contract
│   ├── POST /api/users/verify
│   ├── POST /api/payments/process
│   ├── GET /api/payments/{id}/status
│   └── POST /api/payments/{id}/refund
└── Output: 50+ page architecture document

Epic Sharding:
├── epic-001-user-onboarding.md (with full context)
├── epic-002-payment-processing.md (with full context)
└── epic-003-security-compliance.md (with full context)

Phase 2: Development

Developer implements epic-001:
├── user-service/verify-email.ts (with tests)
├── user-service/kyc-validation.ts (with tests)
├── user-service/account-activation.ts (with tests)
└── database/users-schema.sql

Developer implements epic-002:
├── payment-service/process-payment.ts (with tests)
├── payment-service/refund-handler.ts (with tests)
├── payment-service/status-tracker.ts (with tests)
└── database/transactions-schema.sql

Developer implements epic-003:
├── security/encryption-manager.ts (with tests)
├── compliance/audit-logger.ts (with tests)
├── compliance/pci-validator.ts (with tests)
└── database/audit-schema.sql

QA Validation:
├── Verify each story meets PRD requirements
├── Validate data contracts respected
├── Test security implementations
└── Confirm compliance requirements met
```

### Pros & Cons

**Pros**
- Comprehensive planning reduces architectural rework
- Specialized agents simulate experienced team members
- Clear role definitions prevent role confusion
- Excellent for complex, multi-team projects
- Creates detailed audit trail of decisions
- Handles very large projects well
- Expansion packs provide industry-specific guidance
- Best for understanding AI agent coordination patterns

**Cons**
- Significant overhead for simple tasks (5-10 minute setup per feature)
- Requires understanding of multi-agent concepts
- Slower for small, incremental changes
- More tokens consumed in planning phase
- Steeper learning curve than lighter frameworks
- Can feel like "overkill" for small features
- Maintenance overhead for keeping agent personas updated

### Installation & Setup

```bash
# Clone BMAD repository
git clone https://github.com/bmad-code-org/BMAD-METHOD
cd BMAD-METHOD

# Install dependencies (Python-based)
pip install -r requirements.txt

# Initialize project
python bmad_init.py --project-name "payment-processor"

# Create configuration
# Edit: .bmad/config.yaml
# Configure agents, prompts, workflows

# Start with /plan command
# Agent OS workflow: Plan → Shape → Write Spec → Create Tasks → Implement
```

---

## Part 4: Spec Kit (GitHub's Specification-Driven Development Toolkit)

### Overview

**Philosophy**
- Purpose-built for specification-driven development with AI
- Four-phase gated process with clear validation gates
- Structured templates and scripts ensure consistency
- Emphasizes what and why, not implementation details

**Best For**
- Greenfield projects starting from zero
- Teams wanting simple, proven workflow
- Projects valuing structured rigor and governance
- Organizations needing compliance-ready processes

**Not Ideal For**
- Existing codebases with complex legacy context
- Projects requiring minimal ceremony
- Rapid prototyping with changing requirements

### Four-Phase Workflow

#### Phase 0: Project Bootstrapping

**Initial Setup**
- `specify init` command creates project structure
- Generates semantic branch naming conventions
- Creates feature directory structure
- Sets up git repository and initial commits

**Example Command**
```bash
specify init --project "task-management-app"

# Creates:
# specs/
# ├── project-constitution.md
# ├── principles/
# └── architecture/
```

#### Phase 1: SPECIFY - Write the Specification

**Purpose**
- Define WHAT you want to build and WHY (not HOW)
- Create executable specifications with acceptance criteria
- Document data models and API contracts
- Define security and performance requirements

**Key Artifacts**
```
specs/feature-001-task-creation/
├── spec.md                    # Executable specification
├── acceptance-criteria.md     # Test-like requirements
├── api-contracts.md          # Data structures & APIs
└── constraints.md            # Security, performance, compliance
```

**Specification Template Elements**

```markdown
# Task Creation Specification

## Overview
- Feature number and name
- User stories requiring this feature
- Business value statement

## Functional Requirements
1. User can create task with title and description
2. Tasks assigned to projects
3. Due dates optional but recommended
4. Tasks support priority levels (low, medium, high, urgent)

## Acceptance Criteria
- [AC1] Creating task with required fields succeeds
- [AC2] Creating task without title fails with validation error
- [AC3] Task appears in project immediately after creation
- [AC4] Due date defaults to empty if not provided

## Data Model
```yaml
Task:
  id: UUID
  projectId: UUID
  title: string (1-200 chars)
  description: string (optional)
  priority: enum [LOW, MEDIUM, HIGH, URGENT]
  dueDate: ISO8601 (optional)
  createdAt: ISO8601
  updatedAt: ISO8601
```

## API Contract
```
POST /api/projects/{projectId}/tasks
Request:
  title: string (required)
  description: string (optional)
  priority: enum (optional, default: MEDIUM)
  dueDate: ISO8601 (optional)

Response:
  id: UUID
  status: success | error
  task: Task (if success)
```

## Constraints
- Max 200 characters for title
- API response time < 200ms
- Support concurrent task creation
- Validate input before persistence
```

**Commands**
```bash
# Generate specification template
specify spec --feature "task-creation"

# View generated spec
cat specs/feature-001-task-creation/spec.md
```

#### Phase 2: PLAN - Create Technical Implementation Plan

**Purpose**
- Transform spec into step-by-step technical plan
- Define technology choices and architectural decisions
- Create detailed implementation sequence
- Document interdependencies between tasks

**Planning Input**
```markdown
# Technical Plan Generation Prompt

Generate a plan for implementing Task Creation using:
- Backend: Node.js with Express
- Database: PostgreSQL
- Frontend: React with TypeScript
- API: RESTful with validation middleware

Consider:
- Database schema creation
- API endpoint implementation
- Input validation logic
- Error handling strategy
- Testing approach (unit, integration, e2e)
```

**Generated Plan Structure**
```
specs/feature-001-task-creation/
├── plan.md (Technical implementation plan)

Content:
1. Database Setup
   - Create tasks table with indexes
   - Add foreign key to projects table
   - Create migration script

2. Backend Implementation
   - Create TaskController with POST /tasks
   - Implement TaskService business logic
   - Add validation middleware

3. API Layer
   - Define request/response DTOs
   - Add error handling for validation failures
   - Document API contract in OpenAPI

4. Testing
   - Unit tests for TaskService
   - Integration tests for API endpoint
   - E2E tests with UI interaction

5. Documentation
   - Update API documentation
   - Add usage examples
   - Document error codes
```

**Commands**
```bash
# Generate detailed plan from spec
specify plan --feature "task-creation" \
  --stack "node-express-postgres-react"

# View plan
cat specs/feature-001-task-creation/plan.md
```

#### Phase 3: TASKS - Break Down into Implementation Tasks

**Purpose**
- Decompose plan into granular, implementable tasks
- Order tasks respecting dependencies
- Add test-driven development structure
- Provide exact file paths for implementation

**Task Breakdown**
```
specs/feature-001-task-creation/
├── tasks.md (Implementation task checklist)

Content:
# Task Breakdown - Task Creation Feature

## Phase 1: Database (Dependency: none)
- [P] Task 1.1: Create tasks table schema
  File: migrations/001_create_tasks.sql
  Acceptance: Table exists with all required columns
  
- [P] Task 1.2: Add indexes for performance
  File: migrations/002_add_task_indexes.sql
  Acceptance: Indexes created on projectId and createdAt

## Phase 2: Backend (Dependency: Phase 1)
- Task 2.1: Create TaskController
  File: src/controllers/TaskController.ts
  Acceptance: POST /api/projects/:projectId/tasks returns 201
  
- Task 2.2: Create TaskService
  File: src/services/TaskService.ts
  Acceptance: Service handles validation and persistence
  
- Task 2.3: Add input validation middleware
  File: src/middleware/validateTask.ts
  Acceptance: Invalid input rejected with 400 error

## Phase 3: Frontend (Dependency: Phase 2)
- Task 3.1: Create TaskForm component
  File: src/components/TaskForm.tsx
  Acceptance: Form renders with title, description, priority fields
  
- Task 3.2: Integrate with API
  File: src/api/tasks.ts
  Acceptance: Form submission calls API endpoint
  
- Task 3.3: Add success/error feedback
  File: src/components/TaskForm.tsx
  Acceptance: User sees success toast or error message

## Phase 4: Testing (Dependency: Phase 3)
- Task 4.1: Write unit tests for TaskService
  File: src/services/__tests__/TaskService.test.ts
  Acceptance: 95%+ code coverage
  
- Task 4.2: Write API integration tests
  File: src/controllers/__tests__/TaskController.test.ts
  Acceptance: All endpoints tested with valid/invalid data
  
- Task 4.3: Write E2E tests
  File: cypress/e2e/task-creation.cy.ts
  Acceptance: User flow tested end-to-end

## Parallel Execution Markers
- [P] Tasks marked with [P] can run in parallel
- Phase 1.1 and 1.2 can run in parallel
- Frontend (Phase 3) can run in parallel with backend refinement

## Checkpoint Validation
- After Phase 1: Database ready for queries
- After Phase 2: API returns correct responses
- After Phase 3: UI functional and integrated
- After Phase 4: All tests passing
```

**Commands**
```bash
# Generate task breakdown
specify tasks --feature "task-creation"

# View task breakdown
cat specs/feature-001-task-creation/tasks.md

# Check task status
specify status --feature "task-creation"
```

#### Phase 4: IMPLEMENT - Execute the Plan

**Purpose**
- AI agent executes tasks in correct order
- Validates prerequisites before starting
- Respects dependencies and parallel markers
- Provides progress updates and error handling

**Implementation Flow**
```bash
# Start implementation
specify implement --feature "task-creation"

# Implementation Agent workflow:
1. Validates all prerequisites (spec, plan, tasks)
2. Parses task breakdown from tasks.md
3. Executes Phase 1 tasks (database)
4. Executes Phase 2 tasks (backend)
5. Executes Phase 3 tasks (frontend) in parallel with backend refinement
6. Executes Phase 4 tasks (testing)
7. Reports completion and test results

# Check progress mid-implementation
specify status --feature "task-creation"

# If needed, continue from checkpoint
specify implement --feature "task-creation" --from-checkpoint "Phase-2"

# Review generated code
git diff master feature/001-task-creation
```

**Validation & Checkpoints**
```
Checkpoint 1: Database Schema
├── Verify: migrations execute without errors
├── Verify: schema matches specification
└── Verify: indexes created correctly

Checkpoint 2: API Implementation
├── Verify: Endpoints accessible and return correct status codes
├── Verify: Input validation working
├── Verify: Database writes successful

Checkpoint 3: Frontend Integration
├── Verify: Form renders correctly
├── Verify: Form submission triggers API call
├── Verify: Response handled (success/error feedback)

Checkpoint 4: Test Coverage
├── Verify: Unit tests passing
├── Verify: Integration tests passing
├── Verify: E2E tests passing
├── Verify: Coverage threshold met
```

### Key Features

**Automatic Feature Numbering**
- Scans existing specs to determine next feature number
- Generates 001, 002, 003 automatically
- Prevents numbering conflicts in teams

**Semantic Branch Creation**
- Generates branch names from feature description
- Examples: `feature/001-task-creation`, `feature/002-task-editing`
- Integrates with git workflow automatically

**Template-Based Generation**
- Spec templates guide WHAT and WHY
- Plan templates guide technical HOW
- Task templates break down to granular steps
- All templates customizable via configuration

**Data Contract Generation**
- Automatic API contract generation from spec
- Database schema inference from data models
- Type definitions generated for frontend and backend
- Change detection when specs evolve

**Enforcement via Scripts**
- `bash` and `powershell` scripts ensure consistency
- Scripts run before and after AI agent work
- Validate git state, branch management, artifact presence
- Provide fallback steps if agent fails

### Workflow Example: Building a Task Management Application

```bash
# Step 1: Bootstrap project
specify init --project "task-manager"

# Creates:
# specs/
# ├── project-constitution.md
# ├── principles/engineering.md
# └── architecture/system-design.md

# Step 2: Create specification for first feature
specify spec --feature "task-creation"

# User provides:
# "Create a feature that allows users to create new tasks with title, description, and optional due date"

# Generates:
# specs/feature-001-task-creation/
# ├── spec.md (with acceptance criteria)
# ├── acceptance-criteria.md
# ├── api-contracts.md
# └── constraints.md

# Step 3: Prompt user for tech stack
specify plan --feature "task-creation"

# User specifies:
# - Backend: Node.js + Express
# - Database: PostgreSQL
# - Frontend: React + TypeScript

# Generates:
# specs/feature-001-task-creation/plan.md
# (with 30+ detailed implementation steps)

# Step 4: Break down into tasks
specify tasks --feature "task-creation"

# Generates:
# specs/feature-001-task-creation/tasks.md
# (with ~20 tasks organized by phase and dependency)

# Step 5: Implement
specify implement --feature "task-creation"

# Agent executes:
# 1. Database schema creation
# 2. Backend API implementation
# 3. Frontend component development
# 4. Testing suite creation
# 5. Documentation updates

# All generated code follows spec exactly
```

### Pros & Cons

**Pros**
- Simple, four-phase workflow easy to understand
- Excellent for greenfield projects
- Strong emphasis on specification-driven thinking
- Built-in governance and compliance readiness
- Automatic feature numbering and branch management
- Clear, template-driven approach
- Good documentation and learning resources
- Encourages "what and why" thinking before coding

**Cons**
- Requires more upfront planning (30 minutes per feature)
- Less ideal for brownfield (existing codebases)
- Doesn't provide explicit change tracking
- Assumes relatively clean starting state
- Less support for evolving existing features
- Planning phase can feel rigid
- Better for sequential development than exploratory

### Installation & Setup

```bash
# Install Spec Kit CLI
npm install -g @github/spec-kit

# Initialize project
specify init --project "my-app"

# Set up development environment
cd my-app
npm install

# Configure AI tool integration
# Edit: .speckit/config.yaml
# Set preferred AI tool (Claude, Gemini, etc.)

# Create first specification
specify spec --feature "feature-name"
```

---

## Part 5: OpenSpec (Fission AI's Lightweight Framework)

### Overview

**Philosophy**
- Minimal overhead, maximum flexibility
- Designed specifically for brownfield (existing) projects
- Keeps specs separate from change proposals
- Lightweight markdown-only approach
- Tool-agnostic (works with any AI assistant)

**Best For**
- Adding features to existing codebases
- Lightweight, ceremony-minimal workflows
- Teams using multiple different AI tools
- Rapid iteration and exploration
- Change-centric thinking (proposals → implementation)

**Not Ideal For**
- Greenfield projects needing comprehensive architecture
- Complex multi-team projects
- Projects requiring heavy governance

### Two-Folder Architecture

**Core Concept**
- `/openspec/specs/` - Current project specifications (source of truth)
- `/openspec/changes/` - Proposed and active changes

**Directory Structure**
```
openspec/
├── specs/
│   ├── project.md              # Project overview, conventions, standards
│   ├── auth/
│   │   └── spec.md             # Current authentication specification
│   ├── users/
│   │   └── spec.md             # Current user management specification
│   └── tasks/
│       └── spec.md             # Current task specification
│
└── changes/
    ├── add-2fa/                # Proposed change: 2FA implementation
    │   ├── proposal.md         # Why and what changes
    │   ├── tasks.md            # Implementation checklist
    │   ├── design.md           # Technical decisions (optional)
    │   └── specs/
    │       └── auth/
    │           └── spec.md     # Delta showing 2FA additions
    │
    └── add-profile-filters/    # Proposed change: Profile filtering
        ├── proposal.md
        ├── tasks.md
        └── specs/
            └── users/
                └── spec.md     # Delta showing filter additions
```

### Four-Step Workflow

#### Step 1: Draft the Proposal

**Purpose**
- Propose new change with clear intent
- Define scope and impact
- Get alignment before detailed planning

**User Action**
```
User: Create an OpenSpec change proposal for adding two-factor authentication

AI: I'll create a proposal for 2FA implementation
    [Creates openspec/changes/add-2fa/ structure]
```

**Generated Proposal**
```markdown
# Change Proposal: Add Two-Factor Authentication

## Summary
Enable users to add two-factor authentication to their accounts for enhanced security.

## Why This Change?
- 78% of security breaches involve weak passwords
- Industry standard for high-security applications
- User request from surveys and feedback

## What Changes?
### Affected Components
- Authentication service (add 2FA logic)
- User profile UI (2FA management section)
- Email service (send verification codes)
- Database schema (2FA configuration table)

### Impacted Specifications
- `auth/spec.md` - Add 2FA flow documentation
- `users/spec.md` - Add 2FA profile section

## Scope
- Core 2FA via TOTP (authenticator app)
- Future: SMS and email backup codes (out of scope)

## Success Criteria
- Users can enable/disable 2FA in profile
- Login requires 2FA code when enabled
- Recovery codes provided if app access lost
- 99.9% availability for 2FA verification

## Risks
- Increased complexity of auth flow
- Potential UX friction if poorly implemented
- Database migration required (backward compatible)

## Estimated Effort
- Planning: 1 hour
- Implementation: 8-12 hours
- Testing: 4-6 hours
```

**Commands**
```bash
# Create proposal using slash command (if supported)
/openspec:proposal Add two-factor authentication to accounts

# Or traditional prompt
"Create an OpenSpec change proposal for adding 2FA"
```

#### Step 2: Refine the Specs

**Purpose**
- Write detailed specification deltas
- Define exact changes to existing specs
- Create acceptance criteria for each component
- Document technical decisions

**User Action**
```
User: Can you add specific 2FA requirements to the auth spec?
      Include TOTP implementation details and failure scenarios.

AI: I'll update the spec delta with TOTP details and error cases
    [Updates openspec/changes/add-2fa/specs/auth/spec.md]
```

**Generated Spec Delta**
```markdown
# Authentication Specification (2FA Delta)

## Current Spec (unchanged)
[Original login flow and API contract remain as-is]

## Added: Two-Factor Authentication Flow

### TOTP Implementation
- Algorithm: SHA1-based TOTP (RFC 6238)
- Time step: 30 seconds
- Digit length: 6 digits
- Recovery codes: 10 codes, 8 characters each

### User Flow
1. User enables 2FA in settings
2. System generates secret key
3. User scans QR code with authenticator app
4. User confirms by entering 6-digit code
5. System generates 10 recovery codes
6. User downloads/prints codes as backup

### Login Flow (2FA Enabled)
1. User enters email and password (unchanged)
2. System validates credentials
3. System asks for 2FA code (new)
4. User enters 6-digit code from authenticator
5. System validates code within 30-second window
6. User logged in (unchanged flow after)

### API Changes

#### POST /api/auth/2fa/enable
**Request:**
```json
{
  "password": "current-password"
}
```
**Response:**
```json
{
  "secret": "JBSWY3DPEBLW64TMMQ...",
  "qrCode": "data:image/png;base64,...",
  "recoveryCodesUrl": "https://..."
}
```

#### POST /api/auth/2fa/verify
**Request:**
```json
{
  "code": "123456"
}
```
**Response:**
```json
{
  "success": true,
  "recoveryCodes": ["ABC12345", "DEF67890", ...]
}
```

#### POST /api/auth/login (modified)
**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123",
  "twoFactorCode": "123456" (optional if 2FA not enabled)
}
```

### Acceptance Criteria

#### AC1: TOTP Secret Generation
- Secret key is 32 bytes
- QR code generated from secret
- QR code scans successfully in Google Authenticator, Authy, Microsoft Authenticator

#### AC2: TOTP Verification
- Valid code passes verification
- Invalid code rejected with 403 error
- Code valid for 30-second window plus 1 prior window
- Expired code rejected

#### AC3: Recovery Codes
- 10 codes generated on first enablement
- Each code 8 alphanumeric characters
- Each code single-use only
- Recovery codes work as alternative to TOTP

#### AC4: Disable 2FA
- User can disable 2FA with password verification
- All recovery codes invalidated on disable
- Next login doesn't require 2FA code

### Error Scenarios

| Scenario | HTTP Status | Error Code | Message |
|----------|------------|-----------|---------|
| Invalid TOTP code | 403 | INVALID_2FA_CODE | The code you entered is invalid or expired |
| Used recovery code | 403 | RECOVERY_CODE_USED | This recovery code has already been used |
| TOTP timeout | 408 | 2FA_TIMEOUT | 2FA verification timed out. Please try again |
| User not found | 401 | USER_NOT_FOUND | User account not found |
```

**Commands**
```bash
# Refine specifications
/openspec:refine add-2fa
# OR traditional prompt:
"Update the 2FA spec with detailed TOTP requirements and error scenarios"

# View current proposal state
cat openspec/changes/add-2fa/proposal.md
cat openspec/changes/add-2fa/specs/auth/spec.md
```

#### Step 3: Create Implementation Tasks

**Purpose**
- Break spec into granular implementation tasks
- Define clear success criteria for each task
- Identify task dependencies
- Create implementation checklist

**Generated Tasks File**
```markdown
# Implementation Tasks - 2FA Feature

## Phase 1: Backend Infrastructure (No Dependencies)

### 1.1: Create 2FA Database Schema
**File:** `migrations/001_create_2fa_table.sql`
**Success Criteria:**
- [x] Table created: `user_2fa_settings`
  - Columns: id, user_id, secret_key, enabled, created_at, updated_at
- [x] Table created: `recovery_codes`
  - Columns: id, user_id, code, used, created_at
- [x] Indexes created on user_id for fast lookups
- [x] Foreign keys reference users table
**Acceptance:** `SELECT * FROM user_2fa_settings` returns empty set

### 1.2: Install TOTP Library
**File:** `package.json`
**Success Criteria:**
- [x] speakeasy library added to dependencies
- [x] Version specified (e.g., "^2.0.0")
- [x] npm install completes successfully
- [x] Library exports tested in Node REPL
**Acceptance:** `npm test` confirms library available

## Phase 2: Backend API (Depends on Phase 1)

### 2.1: Create 2FA Service
**File:** `src/services/TwoFactorService.ts`
**Success Criteria:**
- [x] Class: TwoFactorService
- [x] Method: `generateSecret()` - returns secret key
- [x] Method: `verifyToken(secret, token)` - returns boolean
- [x] Method: `generateRecoveryCodes(count)` - returns array
- [x] Method: `verifyRecoveryCode(user_id, code)` - returns boolean
- [x] All methods fully unit tested
**Acceptance:** 95%+ code coverage, all unit tests passing

### 2.2: Implement /api/auth/2fa/enable Endpoint
**File:** `src/controllers/AuthController.ts`
**Success Criteria:**
- [x] POST /api/auth/2fa/enable endpoint created
- [x] Validates user authentication
- [x] Validates user password
- [x] Calls TwoFactorService.generateSecret()
- [x] Generates QR code from secret
- [x] Saves secret to database
- [x] Returns secret and QR code
- [x] Returns 10 recovery codes
- [x] Handles errors appropriately
**Acceptance:** Integration tests pass, API returns correct response

### 2.3: Implement /api/auth/2fa/verify Endpoint
**File:** `src/controllers/AuthController.ts`
**Success Criteria:**
- [x] POST /api/auth/2fa/verify endpoint created
- [x] Validates 2FA code format (6 digits)
- [x] Calls TwoFactorService.verifyToken()
- [x] Sets user session as 2FA verified
- [x] Generates recovery codes on first verify
- [x] Saves recovery codes to database
- [x] Returns recovery codes
- [x] Handles expired tokens
**Acceptance:** Integration tests pass

### 2.4: Modify /api/auth/login Endpoint
**File:** `src/controllers/AuthController.ts`
**Success Criteria:**
- [x] Validates email/password as before
- [x] If user has 2FA enabled, requires `twoFactorCode`
- [x] If twoFactorCode not provided but required, returns 403
- [x] If provided, validates code
- [x] Returns auth token only after successful 2FA
- [x] Backward compatible (users without 2FA work as before)
**Acceptance:** Integration tests cover all scenarios

## Phase 3: Frontend UI (Depends on Phase 2)

### 3.1: Create Enable2FA Component
**File:** `src/components/Enable2FA.tsx`
**Success Criteria:**
- [x] Component displays:
  - Explanation of 2FA benefits
  - QR code image
  - Secret key in text (for manual entry)
  - Button: "Scan QR Code"
  - Input: 6-digit code verification
  - Button: "Verify & Enable"
- [x] Calls /api/auth/2fa/enable endpoint
- [x] Displays QR code from response
- [x] Accepts 6-digit code input
- [x] Validates code on server
- [x] Shows recovery codes on success
- [x] Shows "Copy to Clipboard" button for recovery codes
**Acceptance:** Component renders correctly, E2E test covers flow

### 3.2: Create Recovery Codes Display
**File:** `src/components/RecoveryCodes.tsx`
**Success Criteria:**
- [x] Component displays:
  - Warning: "Save these codes in a safe place"
  - List of 10 recovery codes
  - "Copy All" button
  - "Download as File" button
  - "Print" button
- [x] Copy to clipboard works
- [x] Download generates text file
- [x] Print layout is readable
**Acceptance:** All buttons functional

### 3.3: Create 2FA Settings Section
**File:** `src/components/UserSettings2FA.tsx`
**Success Criteria:**
- [x] Component displays:
  - Status: "2FA Enabled/Disabled"
  - If enabled: "Disable 2FA" button
  - If disabled: "Enable 2FA" button
  - If enabled: List of recovery codes used
- [x] Disable 2FA requires password confirmation
- [x] Clicking "Enable" shows Enable2FA component
- [x] Clicking "Disable" shows confirmation modal
**Acceptance:** Settings component functional

### 3.4: Modify Login Form
**File:** `src/components/LoginForm.tsx`
**Success Criteria:**
- [x] After email/password validation, check if 2FA required
- [x] If required, display 2FA code input
- [x] Display message: "Enter the 6-digit code from your authenticator"
- [x] Accept code input
- [x] Validate code with backend
- [x] Show error message if invalid
- [x] Show "Use Recovery Code" link
**Acceptance:** Login flow works with and without 2FA

## Phase 4: Testing (Depends on Phase 3)

### 4.1: Unit Tests - TwoFactorService
**File:** `src/services/__tests__/TwoFactorService.test.ts`
**Success Criteria:**
- [x] Test: generateSecret() returns valid TOTP secret
- [x] Test: verifyToken() accepts valid token
- [x] Test: verifyToken() rejects invalid token
- [x] Test: verifyToken() accepts token from 1 period prior
- [x] Test: verifyToken() rejects tokens from 2+ periods prior
- [x] Test: generateRecoveryCodes() returns 10 codes
- [x] Test: generateRecoveryCodes() codes are unique
- [x] Test: verifyRecoveryCode() accepts valid code
- [x] Test: verifyRecoveryCode() rejects used code
- [x] All tests passing
**Acceptance:** 100% code coverage for TwoFactorService

### 4.2: Integration Tests - API Endpoints
**File:** `src/controllers/__tests__/AuthController.2fa.test.ts`
**Success Criteria:**
- [x] Test: POST /api/auth/2fa/enable returns secret and QR code
- [x] Test: POST /api/auth/2fa/enable requires authentication
- [x] Test: POST /api/auth/2fa/verify validates token
- [x] Test: POST /api/auth/2fa/verify returns recovery codes
- [x] Test: POST /api/auth/login requires 2FA code when enabled
- [x] Test: POST /api/auth/login accepts recovery codes as alternative
- [x] Test: Recovery code single-use enforcement
- [x] Test: Error handling for all failure scenarios
- [x] All tests passing
**Acceptance:** Integration test suite 95%+ passing

### 4.3: End-to-End Tests
**File:** `cypress/e2e/2fa.cy.ts`
**Success Criteria:**
- [x] Test: User can enable 2FA
  - Navigate to settings
  - Click "Enable 2FA"
  - Scan QR code with authenticator
  - Enter code
  - See recovery codes
  - Verify 2FA enabled in settings
- [x] Test: User can login with 2FA
  - Enter email/password
  - See 2FA code input
  - Enter code from authenticator
  - Login successful
- [x] Test: User can disable 2FA
  - Navigate to settings
  - Click "Disable 2FA"
  - Enter password
  - Confirm disable
  - Verify 2FA disabled
- [x] Test: Recovery code works
  - Use recovery code instead of TOTP
  - Verify recovery code marked as used
  - Can't reuse same code
- [x] All tests passing
**Acceptance:** E2E test suite fully passing

## Task Dependencies & Parallel Execution

```
Phase 1 (No dependencies)
├── 1.1: Create database schema
├── 1.2: Install TOTP library
└── Can run in parallel

Phase 2 (Depends on Phase 1)
├── 2.1: TwoFactorService
├── 2.2: Enable endpoint (depends on 2.1)
├── 2.3: Verify endpoint (depends on 2.1)
├── 2.4: Modify login (depends on 2.2, 2.3)
└── Sequential due to dependencies

Phase 3 (Depends on Phase 2)
├── 3.1: Enable2FA component
├── 3.2: RecoveryCodes component
├── 3.3: Settings section
├── 3.4: Modify login form
└── Can run in parallel once APIs available

Phase 4 (Depends on Phase 3)
├── 4.1: Unit tests
├── 4.2: Integration tests
├── 4.3: E2E tests
└── Can run in parallel
```

## Checkpoint Validation

- **After Phase 1:** Database tables created, library installed
- **After Phase 2:** All API endpoints working, integration tests passing
- **After Phase 3:** UI functional, user flows working
- **After Phase 4:** All tests passing, 95%+ coverage, E2E success
```

**Commands**
```bash
# Refine tasks
/openspec:refine add-2fa

# View current tasks
cat openspec/changes/add-2fa/tasks.md

# Check task progress
grep "^\- \[x\]" openspec/changes/add-2fa/tasks.md | wc -l
```

#### Step 4: Implement the Change

**Purpose**
- Execute tasks from spec
- Track progress through checklist
- Pause and resume as needed
- Move completed changes into specs

**User Action**
```
User: The specs look good. Let's implement this change.

AI: I'll work through the tasks in add-2fa change.
    [Implements tasks from openspec/changes/add-2fa/tasks.md]
    [Marks tasks complete: Task 1.1 ✓, Task 1.2 ✓, Task 2.1 ✓...]
```

**Implementation Workflow**
```bash
# Start implementation
/openspec:apply add-2fa
# OR traditional prompt:
"Implement the 2FA feature using the tasks in openspec/changes/add-2fa/"

# Agent workflow:
1. Reads openspec/changes/add-2fa/tasks.md
2. Executes Phase 1 tasks (database, dependencies)
3. Executes Phase 2 tasks (backend services)
4. Executes Phase 3 tasks (frontend components)
5. Executes Phase 4 tasks (tests)
6. Updates tasks.md marking completion
7. Reports final status

# Check progress mid-implementation
cat openspec/changes/add-2fa/tasks.md
grep "^\- \[x\]" ... | wc -l

# If needed, pause and resume
# Agent remembers state from checked tasks in tasks.md

# Review generated code
git diff master
git diff master -- src/
```

**After Implementation: Archive into Specs**
```bash
# Once testing passes:
1. Copy openspec/changes/add-2fa/specs/auth/spec.md
   → openspec/specs/auth/spec.md (merge deltas)

2. Update openspec/specs/project.md
   - Add 2FA to features list
   - Update any affected architecture notes

3. Delete openspec/changes/add-2fa/ (or archive)

4. Commit to git:
   git add openspec/specs/
   git rm -r openspec/changes/add-2fa/
   git commit -m "Add 2FA feature to specs"

# Now 2FA is part of living specs for future developers
```

### Key Features

**Two-Folder Model**
- `/specs/` = Source of truth, what IS
- `/changes/` = Proposed work, what WILL BE
- Clean separation allows multiple concurrent changes
- Easy to see what's in progress vs committed

**Minimal Overhead**
- Pure markdown files, no config
- Works with ANY AI tool (no vendor lock-in)
- Initialization: `openspec init` (5 minutes)
- Add new feature: 10-15 minutes

**Change Tracking**
- Each change self-contained in folder
- Proposal explains "why"
- Specs show "what changes"
- Tasks show "how to implement"
- Easy to review before applying

**Existing Codebase Support**
- Populates project.md with conventions
- Works on mature projects
- Doesn't require greenfield clean state
- Can layer onto legacy systems

**Team Collaboration**
- Different team members use different AI tools
- All share same `/specs/` and `/changes/` structure
- Works with: Claude Code, CodeBuddy, Cursor, custom agents
- Run `openspec update` when switching tools

### Workflow Example: Adding Profile Search Filters

```bash
# User has existing user management system

# Step 1: Draft proposal
User: Create an OpenSpec change proposal for adding profile search filters by role and team

AI: [Creates openspec/changes/add-profile-filters/ with proposal.md]

# Step 2: Refine specifications
User: Can you add acceptance criteria for the role and team filters?

AI: [Updates openspec/changes/add-profile-filters/specs/users/spec.md]
    - Acceptance criteria for role filter
    - Acceptance criteria for team filter
    - API contract changes
    - Error scenarios

# Step 3: Create tasks
User: Break this down into implementation tasks

AI: [Generates tasks.md with:
    - Phase 1: Backend filtering logic (database queries)
    - Phase 2: API endpoint updates
    - Phase 3: Frontend filter UI
    - Phase 4: Testing (unit, integration, E2E)]

# Step 4: Implement
User: The specs look good. Let's implement this change.

AI: [Works through tasks in order]
    - Implements database queries
    - Updates API endpoints
    - Builds filter UI components
    - Writes and runs tests
    - Reports completion

# After implementation: Archive into specs
openspec/changes/add-profile-filters/
  → openspec/specs/users/spec.md (merge deltas)
→ Delete changes/add-profile-filters/
```

### Pros & Cons

**Pros**
- Minimal setup and overhead (5 minutes to start)
- Excellent for existing codebases
- Clean separation of proposed vs committed
- Works with any AI tool (true tool-agnostic)
- Lightweight, markdown-only approach
- Easy to review before applying
- Quick iteration on changes
- Change proposal model mirrors real development
- Excellent change tracking

**Cons**
- Less structured than Spec Kit (more flexibility = less structure)
- No built-in planning phase like BMAD
- Requires more self-discipline to write good specs
- Less sophisticated than multi-agent systems
- Doesn't automate spec validation
- Requires manual spec merging after implementation
- Simpler templates mean more guidance needed

### Installation & Setup

```bash
# Install OpenSpec (requires Node.js)
npm install -g openspec

# Initialize project
cd my-project
openspec init

# Populate project context
# Edit: openspec/project.md
# Add: conventions, architecture notes, tech stack

# Create first change proposal
# Prompt your AI:
"Create an OpenSpec change proposal for [feature name]"
# AI will scaffold: openspec/changes/[feature-name]/
```

---

## Part 6: Agent OS (Builder Methods)

### Overview

**Philosophy**
- Spec-driven development with ANY AI coding tool
- 3-layer context system (Standards, Product, Specs)
- Tool-agnostic design (Claude Code, Cursor, Gemini, others)
- Modular architecture that adapts to your workflow
- Multi-agent orchestration for complex builds

**Best For**
- Teams wanting flexibility in AI tool choice
- Projects needing strong standards enforcement
- Medium to large applications
- Situations requiring both simplicity and power

**Not Ideal For**
- Teams locked into single toolchain
- Minimal documentation preference
- One-off small projects

### 3-Layer Context System

```
Agent OS Architecture:

┌─────────────────────────────────────────────┐
│         Agent OS Installation                │
│  ~/.agent-os/ (global profiles & standards) │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│    Layer 1: STANDARDS (How you build)       │
│  .agent-os/standards/*.md (compiled as     │
│  Claude Code Skills for efficient context)  │
│  - Code style guide                         │
│  - Architecture patterns                    │
│  - Testing conventions                      │
│  - Git workflow                             │
│  - Security practices                       │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│   Layer 2: PRODUCT (What you're building)   │
│         .agent-os/product.md                │
│  - Product vision and roadmap               │
│  - User personas and use cases              │
│  - Key features and priorities              │
│  - Success metrics                          │
└─────────────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│      Layer 3: SPECS (What's next)           │
│   .agent-os/specs/spec.md & tasks.md       │
│  - Current feature specification            │
│  - Implementation tasks                     │
│  - Acceptance criteria                      │
│  - API contracts                            │
└─────────────────────────────────────────────┘
```

### Setup Configuration

**Global Installation**
```bash
# Install globally to home directory
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/scripts/base-install.sh | bash

# Creates: ~/.agent-os/
# └── default/
#     ├── agents/
#     │   ├── product-planner.md
#     │   ├── spec-shaper.md
#     │   ├── developer.md
#     │   └── qa.md
#     ├── standards/
#     │   ├── code-style.md
#     │   ├── architecture.md
#     │   └── testing.md
#     ├── workflows/
#     │   ├── planning.md
#     │   └── implementation.md
#     └── config.yaml
```

**Project-Level Configuration**
```bash
# Initialize in project directory
cd my-project
agent-os init

# Creates: .agent-os/
# ├── config.yaml
# │   # Project-specific overrides
# │   standard_as_claude_code_skills: true  # Compile standards to skills
# │   use_claude_code_subagents: true       # Delegate to sub-agents
# │   model: claude-opus-4.5
# │   preferred_tool: claude-code
# │
# ├── agents/
# │   └── ios-developer.md  # Custom agent persona
# │
# ├── standards/
# │   ├── swift-style.md
# │   ├── ios-architecture.md
# │   └── testing-conventions.md
# │
# └── product.md  # Project product vision
```

### The Agent OS Workflow

#### Phase 1: Product Planning

**Command**
```bash
# Start product planning workflow
/plan-product
```

**Workflow**
```
Product Planner Agent:
1. Asks: "What problem are you solving?"
2. Asks: "Who are your users?"
3. Asks: "What's the one thing users should be able to do?"
4. Asks: "What's your success metric?"
5. Asks: "What's out of scope for MVP?"
6. Creates: product.md with vision and roadmap
```

**Generated Product.md**
```markdown
# Product: Native iOS Teleprompter

## Vision
Enable content creators (YouTubers, TikTokers, video producers) to use their iPhone as a teleprompter with real-time scrolling, mirroring, and recording integration.

## Problem Statement
Existing teleprompter apps require subscriptions for basic functionality. Creators want a free, privacy-first solution that scrolls with their voice and supports screen recording.

## User Personas
- YouTube Creator: 25-35, creating 5+ videos/month, wants professional tool
- Social Media Creator: 18-25, creating TikToks daily, wants free tool
- Small Studio: Content team, needs collaboration features

## MVP Features (In Scope)
1. Text input with script editing
2. Adjustable scrolling speed
3. Mirror mode (reverse text for reflection)
4. Font size and color customization
5. Integration with iPhone screen recording

## Future Features (Out of Scope)
- Collaboration/shared scripts
- Cloud sync
- Teleprompter hardware integration
- Multi-language support

## Success Metrics
- 1000+ downloads in first month
- 4.5+ star rating
- 70%+ retention rate
- Average session > 10 minutes

## Market Validation
- Surveyed 200 creators: 87% would use free app
- Competitors charge $4.99/month
- Privacy-first positioning differentiates
```

#### Phase 2: Spec Shaping

**Command**
```bash
# Shape detailed specification from product vision
/shape-spec
```

**Workflow**
```
Spec Shaper Agent:
1. Reviews product.md
2. Asks: "Which MVP feature should we focus on?"
3. Asks: "What's the user flow?"
4. Asks: "What data needs to be stored?"
5. Asks: "What could go wrong?"
6. Asks: "Any design mockups or assets?"
7. Creates: specs/ directory with detailed requirements
```

**Example Q&A**
```
Agent: Which MVP feature should we focus on first?
User: Text input and script editing with a clean interface

Agent: Walk me through how a user edits a script
User: User launches app → Types script → Sees preview → Saves script

Agent: What data needs to persist?
User: Script text, user preferences (font size, color, speed), last script opened

Agent: What security/privacy concerns?
User: Scripts stored only locally, no cloud, no tracking

Agent: Do you have UI designs?
User: [Provides Figma link with wireframes]
```

#### Phase 3: Spec Writing

**Command**
```bash
# Generate formal specification
/write-spec
```

**Generated Spec.md**
```markdown
# Specification: Text Input and Script Editing

## Feature Overview
Users can input and edit teleprompter scripts with a clean, distraction-free interface.

## User Stories

### Story 1: Create New Script
As a content creator
I want to quickly create a new script
So that I can prepare for recording

**Acceptance Criteria:**
- User taps "New Script" button
- Text editor opens with cursor active
- Default font size: 18pt
- Keyboard appears automatically
- "Save" button inactive until text entered
- Tapping save shows filename dialog

### Story 2: Edit Existing Script
As a content creator
I want to edit saved scripts
So that I can refine my content

**Acceptance Criteria:**
- User sees list of saved scripts
- Tapping script opens in editor
- All previous edits preserved
- Editing updates saved version
- Undo/Redo available
- Delete option available with confirmation

## Technical Specification

### Data Model
```swift
struct Script {
    let id: UUID
    var title: String
    var content: String
    var createdAt: Date
    var updatedAt: Date
    var settings: ScriptSettings
}

struct ScriptSettings {
    var fontSize: CGFloat = 18
    var textColor: UIColor = .white
    var backgroundColor: UIColor = .black
    var scrollSpeed: Float = 1.0
    var isMirrored: Bool = false
}
```

### API/Storage
- Storage: Core Data (local, encrypted)
- No network calls
- Background saving every 10 seconds
- Automatic undo/redo history

### UI Components
- ScriptEditorView (main text editor)
- ToolbarView (font size, colors, settings)
- SaveDialogView (script naming)
- ScriptListView (browse saved scripts)

## Implementation Notes
- Use SwiftUI TextEditor
- Implement undo/redo with environmental state
- Core Data stack for persistence
- Handle keyboard safely area on notched devices
```

#### Phase 4: Task Creation

**Command**
```bash
# Create implementation task breakdown
/create-tasks
```

**Generated Tasks.md**
```markdown
# Implementation Tasks - Text Input & Script Editing

## Task Group 1: Data Layer
- [ ] 1.1: Create Script and ScriptSettings models
- [ ] 1.2: Set up Core Data stack
- [ ] 1.3: Create ScriptRepository for CRUD operations
- [ ] 1.4: Implement undo/redo state manager
- [ ] 1.5: Add migration for schema updates

## Task Group 2: UI Layer
- [ ] 2.1: Create ScriptEditorView with TextEditor
- [ ] 2.2: Create ToolbarView with font/color controls
- [ ] 2.3: Create SaveDialogView for naming
- [ ] 2.4: Create ScriptListView with navigation
- [ ] 2.5: Implement keyboard safety handling
- [ ] 2.6: Add animations for transitions

## Task Group 3: Functionality
- [ ] 3.1: Implement save functionality
- [ ] 3.2: Implement edit functionality
- [ ] 3.3: Implement delete with confirmation
- [ ] 3.4: Implement undo/redo
- [ ] 3.5: Background auto-save every 10 seconds
- [ ] 3.6: Handle app lifecycle (background/foreground)

## Task Group 4: Testing & Polish
- [ ] 4.1: Unit tests for ScriptRepository
- [ ] 4.2: UI tests for ScriptEditorView
- [ ] 4.3: Snapshot tests for UI
- [ ] 4.4: Performance testing (large scripts)
- [ ] 4.5: Edge case testing (corrupted data recovery)
- [ ] 4.6: Accessibility review (VoiceOver)
```

#### Phase 5: Implementation

**Two Implementation Options**

**Option A: Simple Implementer (Faster)**
```bash
# Executes tasks sequentially in main agent
/implement-tasks

# Workflow:
1. Agent reads task groups from tasks.md
2. For each task group:
   - Implement code for all tasks
   - Run tests
   - Fix failures
3. Reports completion with test results

# Faster but less architecture control
```

**Option B: Orchestrated Implementation (More Control)**
```bash
# Generates orchestration config, assigns agents
/orchestrate-tasks

# Creates: .agent-os/orchestration.yml
task_groups:
  data_layer:
    agent: backend-agent
    priority: 1
  
  ui_layer:
    agent: ios-developer
    priority: 2
    depends_on: [data_layer]
  
  functionality:
    agent: ios-developer
    priority: 3
    depends_on: [data_layer]
  
  testing:
    agent: qa-agent
    priority: 4
    depends_on: [functionality]

# More control over which agent does what
# Can assign UI work to one agent, backend to another
# Respects dependencies automatically
```

### Key Features

**Standards as Skills**
- `.agent-os/standards/*.md` files compiled to Claude Code Skills
- Skills are loaded on-demand (efficient context)
- Agent can access full style guide without bloating context
- Works seamlessly in Claude Code interface

**Sub-Agent Support**
- Each task group can be delegated to specialized agent
- Main agent orchestrates, doesn't do all work
- Database agent can work on data tasks while UI agent works on interface
- Sub-agents have appropriate context scope

**Product-Level Context**
- product.md contains vision, roadmap, user personas
- All agents reference same product understanding
- Ensures features align with business goals
- Easier onboarding for new team members

**Tool Flexibility**
- Works with Claude Code (native support)
- Works with Cursor (slash commands as prompts)
- Works with Gemini CLI (standard CLI interface)
- Works with any AI tool (provide explicit commands)

### Workflow Example: Building an iOS Teleprompter

```bash
# Step 1: Global installation
curl -sSL [...base-install.sh...] | bash

# Step 2: Project initialization
cd teleprompter-app
agent-os init

# Step 3: Configure iOS profile
cat .agent-os/config.yaml
# ios:
#   profile: ios
#   agent: ios-developer
#   standards: [swift-style.md, ios-architecture.md]

# Step 4: Plan product
/plan-product
# Agent asks about vision, users, features, success metrics
# Generates: .agent-os/product.md

# Step 5: Shape specs
/shape-spec
# Agent asks detailed questions about text editing feature
# Generates: .agent-os/specs/text-input-spec.md

# Step 6: Write formal spec
/write-spec
# Generates detailed technical specification

# Step 7: Create tasks
/create-tasks
# Breaks spec into 15-20 implementation tasks

# Step 8: Implement (choose path)
# Option A - Simple:
/implement-tasks
# Single agent executes all tasks sequentially

# Option B - Orchestrated:
/orchestrate-tasks
# Generates orchestration.yml
# Data layer agent works on database
# iOS developer agent works on UI
# QA agent works on testing
```

### Pros & Cons

**Pros**
- Tool-agnostic (works with any AI assistant)
- Strong standards enforcement via skills
- 3-layer context system very clean
- Good for multi-agent setups
- Sub-agent orchestration for complex projects
- Standards management built-in
- One day learning curve
- Works with existing AI tools

**Cons**
- More setup than OpenSpec
- Skills oversight bug (must manually add skills to sub-agent files)
- No explicit change proposal model
- Less structured than Spec Kit
- Slower maintenance (maintenance overhead)
- Best for Claude Code (though works elsewhere)
- Incomplete brownfield project support
- Requires understanding agent concepts

### Installation & Setup

```bash
# Global installation
curl -sSL https://raw.githubusercontent.com/buildermethods/agent-os/main/scripts/base-install.sh | bash

# Project initialization
agent-os init --project "my-project"

# Configure for your AI tool of choice
# Edit: .agent-os/config.yaml
# Select: preferred_tool (claude-code, cursor, gemini, etc.)

# Start with product planning
/plan-product
```

---

## Part 7: Google Conductor (Context-Driven Development)

### Overview

**Philosophy**
- Context-driven development for Gemini CLI
- Formal specs and plans live in persistent markdown files
- Brownfield-focused (handles existing codebases)
- Team-level context sharing
- Free and deeply integrated with Gemini

**Best For**
- Teams using Gemini models (free API access)
- Modernizing existing codebases
- Team consistency in AI contributions
- Project context documentation
- Context-driven architectural planning

**Not Ideal For**
- Teams committed to other AI models
- Greenfield projects (heavier than needed)
- Simple one-off changes
- Projects not using Gemini

### Context-Driven Development Philosophy

**Problem Being Solved**
- Chat logs are impermanent and scattered
- Context lives in developer's head, not codebase
- New team members don't understand project architecture
- Brownfield projects lack AI-friendly documentation
- Token usage explodes on existing codebases

**Solution**
- Living documents that define project context
- Persistent markdown files in codebase
- Architecture and guidelines grow with project
- Gemini has deep, lasting project awareness

### Conductor Workflow

#### Step 1: Setup Project Context

**Command**
```bash
# Initialize Conductor in project
gemini
/conductor:setup
```

**Interactive Setup**
```
Conductor Guide:
1. Do you have an existing project directory? [Y/n]
   → Yes, analyze existing codebase

2. What's your project's primary purpose?
   Options:
   a) Provide user authentication for applications
   b) Create real-time data processing pipelines
   c) Build a reusable login form for web apps
   d) [Enter custom description]
   → Select or enter custom description

3. Conductor creates: conductor.md
   (Product definition & guidelines)

   Conductor Reviews: Source code
   (Analyzes existing codebase)

   Conductor Creates: architecture.md
   (Documents discovered architecture)

   Conductor Creates: workflow.md
   (Documents development workflow)
```

**Generated Conductor Files**
```markdown
# conductor.md - Project Definition

## Product Overview
Your app is a user authentication system that helps developers quickly add secure login to web applications.

## Tech Stack
- Language: TypeScript
- Framework: Express.js
- Database: PostgreSQL
- Frontend: React

## Workflow Preferences
- Branch naming: feature/*, fix/*, docs/*
- PR review requirement: Yes
- Testing framework: Jest
- Code style: ESLint + Prettier

---

# architecture.md - System Architecture

## Service Architecture
- **Auth Service**: Handles user authentication and session management
- **User Service**: Manages user profiles and preferences
- **Email Service**: Sends verification and password reset emails
- **Token Service**: Manages JWT token generation and validation

## Data Flow
1. User submits credentials → Auth Service
2. Auth Service validates against User DB
3. Token Service generates JWT
4. JWT returned to client

## Key Patterns
- All services communicate via REST API
- Authentication via JWT in Authorization header
- Rate limiting on auth endpoints
- Background job processing for email

---

# workflow.md - Development Workflow

## Feature Development Steps
1. Create feature branch: feature/feature-name
2. Create detailed spec in spec.md
3. Update plan.md with implementation steps
4. Implement following architectural patterns
5. Write tests for all changes
6. Submit PR for review

## Code Standards
- TypeScript strict mode enabled
- >80% test coverage required
- ESLint rules enforced
- Prettier formatting on commit

## Deployment Process
- Tests must pass in CI
- Manual review on staging
- Performance benchmarks required
- Zero-downtime deployment preferred
```

#### Step 2: Create New Track (Feature)

**Command**
```bash
# Start new feature or bug fix
/conductor:newTrack
# Or
/conductor:newTrack "Add two-factor authentication"
```

**Interactive Track Setup**
```
Conductor:
1. What's the name of this track?
   → "Add two-factor authentication"

2. Is this a feature, bug fix, or enhancement?
   → Feature

3. Who should this benefit?
   → Users wanting stronger account security

4. What's the main technical challenge?
   → Integrating TOTP and recovery codes securely

Conductor Creates:
- track-001-add-2fa/
  ├── spec.md (Detailed specification)
  └── plan.md (Implementation plan with 15+ steps)
```

**Generated Spec**
```markdown
# Track 001: Add Two-Factor Authentication

## Feature Summary
Enable users to add TOTP-based 2FA to their accounts for enhanced security.

## User Value
- Protects accounts from unauthorized access
- Builds user trust in platform security
- Differentiates from competitors

## Requirements
1. TOTP using authenticator apps (Google Authenticator, Authy)
2. Recovery codes for account recovery
3. Device trust (remember this device for 30 days)
4. Disable 2FA with password confirmation

## Acceptance Criteria
- Users can enable TOTP-based 2FA
- Login requires 2FA code when enabled
- Recovery codes work as fallback
- Users can disable 2FA anytime
- Proper error handling for all edge cases

## Technical Constraints
- Use established TOTP library (speakeasy.js)
- No external 2FA service dependency
- Backward compatible with non-2FA users
- Database migration required (backward compatible)

## Estimated Complexity
- Backend: Medium
- Frontend: Medium
- Testing: Medium
- Total Effort: 12-16 hours
```

**Generated Plan**
```markdown
# Implementation Plan - 2FA Feature

## Phase 1: Backend Infrastructure
1. Update database schema
   - Add 2fa_settings table
   - Add recovery_codes table
   - Create migrations

2. Install TOTP library
   - npm install speakeasy
   - Add qrcode library for QR generation

3. Create 2FA service
   - TwoFactorService class
   - Methods: generateSecret, verifyToken, generateRecoveryCodes
   - Methods: validateRecoveryCode, disableTwoFactor

## Phase 2: API Endpoints
4. Implement /api/auth/2fa/enable
   - Validates user authentication
   - Generates TOTP secret
   - Generates QR code
   - Returns secret and recovery codes

5. Implement /api/auth/2fa/verify
   - Validates TOTP code
   - Saves 2FA as enabled
   - Returns recovery codes

6. Modify /api/auth/login
   - Check if 2FA enabled for user
   - Request 2FA code if needed
   - Support recovery codes as alternative

7. Implement /api/auth/2fa/disable
   - Requires password verification
   - Disables 2FA
   - Invalidates recovery codes

## Phase 3: Frontend Components
8. Create Enable2FA component
   - Display QR code
   - Input field for code verification
   - Recovery codes display

9. Create 2FA Settings section
   - Show 2FA status
   - Enable/disable buttons
   - Recovery code management

10. Update LoginForm
    - Add 2FA code input when needed
    - Support recovery code input
    - Proper error messaging

## Phase 4: Testing & Documentation
11. Write unit tests (TwoFactorService)
12. Write integration tests (API endpoints)
13. Write E2E tests (user flows)
14. Update API documentation
15. Update user guide
```

#### Step 3: Refine Specs and Plans

**During Development**
```bash
# As you work through implementation:
gemini
# "The 2FA code validation is taking too long. 
#  What if we cache verification results?"

# Conductor analyzes:
# - Current spec constraints
# - Architecture patterns
# - Performance requirements
# - Suggests updates to plan

# Updates: plan.md with optimizations
```

**Commands for Refinement**
```bash
# View current progress
/conductor:status

# If needed, revert to previous checkpoint
/conductor:revert-checkpoint "Phase-1"

# Edit plan mid-flight
# Edit: track-001-add-2fa/plan.md
# (Conductor reads updated plan on next prompt)
```

#### Step 4: Implementation

**Command**
```bash
# Start implementing spec and plan
/conductor:implement
```

**Implementation Workflow**
```
Conductor Agent:
1. Reads spec.md (what you're building)
2. Reads plan.md (how to build it)
3. Reads architecture.md (style and patterns)
4. Reads workflow.md (dev standards)

5. Creates branch: feature/001-add-2fa
6. Implements Phase 1 (database)
   - Creates migrations
   - Creates 2FA service
   - Writes unit tests

7. Implements Phase 2 (API endpoints)
   - Implements /api/auth/2fa/enable
   - Implements /api/auth/2fa/verify
   - Modifies /api/auth/login
   - Writes integration tests

8. Implements Phase 3 (Frontend)
   - Creates Enable2FA component
   - Creates settings section
   - Updates LoginForm
   - Writes E2E tests

9. Reports completion:
   - All files created
   - All tests passing
   - Ready for review
   - PR created automatically (optional)
```

### Key Features

**Brownfield Focus**
- Conductor analyzes existing codebases
- Documents discovered architecture
- Creates living documents for future development
- Perfect for modernizing legacy systems

**Team Context Sharing**
- One time setup of architecture, workflow, standards
- All AI contributions follow same patterns
- Different developers, consistent code quality
- New team members onboard via specs

**Checkpoint System**
- Save state at phase boundaries
- Pause and resume work without losing context
- Revert to previous phase if needed
- Excellent for complex features

**Living Documentation**
- Architecture grows with project
- Guidelines evolved as patterns emerge
- Future developers have AI-friendly docs
- Specs maintain historical record

**Gemini CLI Integration**
- Native integration (no external tools)
- 1M token context window (Gemini 3 Pro)
- Free API access (pay-as-you-go)
- Terminal-native workflow

### Workflow Example: Modernizing Legacy Auth System

```bash
# Step 1: Initialize Conductor
cd legacy-auth-system
gemini
/conductor:setup

# Conductor analyzes existing codebase and creates:
# ├── conductor.md (product overview)
# ├── architecture.md (discovered patterns)
# ├── workflow.md (dev standards)

# Step 2: Create track for modernization
/conductor:newTrack "Modernize authentication system"

# Conductor creates:
# └── track-001-modernize-auth/
#     ├── spec.md (what we're building)
#     └── plan.md (how to build it)

# Step 3: Review and refine
# Edit: track-001-modernize-auth/plan.md
# Add specific requirements and constraints

# Step 4: Implement
/conductor:implement

# Conductor reads all context files:
# - conductor.md (product & workflow)
# - architecture.md (system patterns)
# - workflow.md (dev standards)
# - spec.md (what to build)
# - plan.md (how to build it)

# Implements systematically while respecting:
# - Tech stack (TypeScript, Express, PostgreSQL)
# - Code standards (ESLint, Prettier, tests)
# - Architecture patterns (services, API contracts)
# - Workflow (feature branches, PR reviews)

# Reports completion:
# ✓ All migrations created
# ✓ Services refactored
# ✓ Tests updated (95%+ coverage)
# ✓ Documentation updated
# ✓ PR created and ready for review
```

### Pros & Cons

**Pros**
- Free (Gemini API free tier)
- Excellent for brownfield projects
- Natural integration with Gemini CLI
- Living documentation approach excellent
- Team context sharing very effective
- Large context window (1M tokens)
- Good checkpoint and pause/resume
- Strong architectural awareness

**Cons**
- Only works with Gemini models
- Newer than established frameworks (less community)
- Less multi-agent support than BMAD
- Heavier than OpenSpec for simple changes
- Requires Gemini CLI setup
- Documentation less mature than alternatives
- Limited to Gemini ecosystem
- Not as lightweight as OpenSpec

### Installation & Setup

```bash
# Install Gemini CLI
npm install -g gemini-cli

# Authenticate
gemini auth login

# Install Conductor extension
gemini extensions install \
  https://github.com/gemini-cli-extensions/conductor

# Initialize in project
cd my-project
gemini
/conductor:setup
```

---

## Part 8: Serena - IDE-Level Intelligence for AI Coding

### Overview

**Philosophy**
- Supplements spec-driven frameworks with IDE-level code comprehension
- Uses Language Server Protocol (LSP) for semantic understanding
- Achieves 30-54% token usage reduction through smart code retrieval
- Open-source and free (works with free LLM access)
- Symbol-level precision in large codebases

**Best For**
- Large, complex codebases where context explodes
- Refactoring across entire projects
- Bug fixes requiring deep code understanding
- Teams wanting to reduce token costs significantly
- Developers using Claude Code or Claude Desktop

**Not Ideal For**
- Tiny projects where full context fits easily
- Projects in unsupported languages (limited to 30+ major languages)
- Minimal setup preference
- Simple prompt-based interactions only

### The Problem Serena Solves

**Without Serena (Traditional Approach)**
```
User Query: "Find all functions that manage user state"

Typical AI Response Approach:
1. Load entire project into context
2. Search through ALL files
3. Consume 47,000 tokens from context window
4. Return somewhat relevant functions

Problems:
- Massive token consumption
- Slow due to large context
- Often includes false positives
- Difficult for large projects
```

**With Serena (Intelligent Approach)**
```
User Query: "Find all functions that manage user state"

Serena Response Approach:
1. Use LSP semantic analysis
2. Index symbols (functions, classes, variables)
3. Find exact matches: "state management" functions
4. Consume 22,800 tokens from context window (54% reduction!)
5. Return precise, relevant functions

Benefits:
- 54% fewer tokens
- Much faster
- Accurate results
- Scales to huge projects
```

### How Serena Works

#### Language Server Protocol (LSP)

**What is LSP?**
- Standard protocol used by IDEs (VS Code, IntelliJ, etc.)
- Provides semantic understanding of code
- Understands: functions, classes, variables, types, relationships
- Available for 30+ programming languages

**Serena's LSP Integration**
```
Serena Architecture:

User Query
    ↓
Serena Tools Layer
├── find_symbol("state management")
├── find_references(symbol)
├── get_type_info(symbol)
├── get_documentation(symbol)
└── intelligent_replace(symbol, new_code)
    ↓
Language Server
├── Python LSP Server
├── JavaScript/TypeScript LSP Server
├── Go LSP Server
├── Rust LSP Server
├── Java LSP Server
└── [20+ more language servers]
    ↓
Code Understanding
├── Abstract Syntax Tree (AST) parsing
├── Symbol indexing and cross-references
├── Type inference and checking
└── Dependency resolution
    ↓
Semantic Code Retrieval
└── Returns only relevant code to AI agent
```

#### Serena Tools

**Symbol-Level Tools**
```
find_symbol(pattern: str) → Symbol[]
- Find functions, classes, variables by name
- Semantic search (not just text matching)
- Example: find_symbol("handle*") finds handleClick, handleSubmit, etc.

Example Usage:
Serena.find_symbol("authenticate") → [
  {symbol: "authenticateUser", file: "auth.ts", type: "function"},
  {symbol: "AuthenticationService", file: "services/auth.ts", type: "class"},
  {symbol: "isAuthenticated", file: "middleware.ts", type: "variable"}
]
```

**Reference Finding**
```
find_references(symbol: Symbol) → Reference[]
- Find all places where symbol is used
- Understand data flow
- Track function calls and dependencies

Example:
find_references("authenticateUser") → [
  {file: "routes/auth.ts", line: 42},
  {file: "middleware/auth.ts", line: 15},
  {file: "tests/auth.test.ts", line: 88},
  {file: "services/login.ts", line: 23}
]
```

**Type Information**
```
get_type_info(symbol: Symbol) → TypeInfo
- Return function signature
- Parameter types and return types
- Class inheritance and interfaces
- Generic type parameters

Example:
get_type_info("authenticateUser") → {
  type: "function",
  parameters: [
    {name: "email", type: "string"},
    {name: "password", type: "string"}
  ],
  returns: "Promise<User>",
  throws: ["InvalidCredentialsError", "DatabaseError"]
}
```

**Documentation Retrieval**
```
get_documentation(symbol: Symbol) → string
- Extract JSDoc/docstring comments
- Include parameter descriptions
- Include usage examples
- Include author and modification history

Example:
get_documentation("authenticateUser") →
"""
Authenticates a user with email and password.

@param email The user's email address
@param password The user's password (plaintext, will be hashed)
@returns User object if authentication successful
@throws InvalidCredentialsError if email/password invalid
@throws DatabaseError if database connection fails

Example:
const user = await authenticateUser("user@example.com", "pass123");
"""
```

**Intelligent Code Replacement**
```
insert_after_symbol(symbol: Symbol, code: string) → void
- Insert code after specific function/class
- Maintain proper formatting and indentation
- Update imports automatically
- Handle language-specific syntax

replace_symbol_body(symbol: Symbol, new_body: string) → void
- Replace function/method body
- Keep signature intact
- Update if type signature changes

Example:
// Before
async function validateEmail(email: string): Promise<boolean> {
  return email.includes("@");
}

// Command
replace_symbol_body("validateEmail", `{
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}`)

// After
async function validateEmail(email: string): Promise<boolean> {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### Integration Patterns

#### Pattern 1: Claude Desktop Integration

**Setup**
```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "serena-mcp",
        "--project-root",
        "/path/to/project"
      ]
    }
  }
}
```

**Usage in Claude**
```
User in Claude: "Find all user state management functions"

Claude (with Serena):
I'll use Serena to find state management functions with precision.

[Uses: find_symbol("*state*")]

Found:
1. userState.ts:UserStateManager (class)
   - manageUserState() (function)
   - getUserState() (function)
   
2. hooks.ts:useUserState (React hook)
3. selectors.ts:selectUserState (Redux selector)

Total tokens consumed: 22,800 (vs 47,000 without Serena = 54% savings!)
```

#### Pattern 2: Command Line Integration

**CLI Usage**
```bash
# Find symbol and show context
serena find_symbol "authenticateUser"

# Get type information
serena get_type_info "DatabaseService"

# Find all references to symbol
serena find_references "handleUserLogin"

# Show documentation
serena get_documentation "UserRepository"
```

#### Pattern 3: Spec-Driven with Serena

**Integration Flow**
```
Spec-Driven Framework        Serena
(BMAD/Spec Kit/Agent OS)     (IDE Intelligence)
        ↓                           ↓
1. Specification defined    1. Find exact symbols
   (what to build)          (code to modify)
        ↓                           ↓
2. Implementation plan      2. Understand context
   (how to build)           (via LSP analysis)
        ↓                           ↓
3. AI agent generates code  3. Generate precise changes
   (using Serena tools)     (only relevant code)
        ↓                           ↓
   Reduces tokens by 30-54%
   Better code quality
   Faster generation
```

### Practical Example: Refactoring Authentication

**Scenario**
```
Large application with scattered auth code:
- 15 files with authentication logic
- 200+ functions related to authentication
- Context window explodes trying to understand auth flow

Question: "Refactor all password validation to use bcrypt"
```

**Without Serena**
```
1. Load entire auth directory (100KB+ of code)
2. Parse through all 200+ functions
3. Identify which ones validate passwords
4. Consume 45,000 tokens from context window
5. Make changes (might miss some functions)
6. Token cost: $0.90 per request
```

**With Serena**
```
1. find_symbol("*validate*password*")
   → Returns exact list of validation functions
   
2. For each function:
   - get_type_info() → Understand inputs/outputs
   - get_documentation() → See current implementation
   - find_references() → Where is it used?
   
3. Generate changes using precision tools:
   - insert_after_symbol() → Add new bcrypt validation
   - replace_symbol_body() → Update existing validation
   
4. Result:
   - Consume 18,000 tokens (60% reduction)
   - Accurate changes (all functions found)
   - Token cost: $0.36 per request
   - 2.5x faster execution
```

### Supported Languages

**Primary Support (Full LSP)**
- Python (Pylance)
- TypeScript/JavaScript (TypeScript LSP)
- Java (Eclipse LSP)
- Go (gopls)
- Rust (rust-analyzer)
- C# (.NET LSP)
- C/C++ (clangd)

**Secondary Support (Community LSP)**
- PHP, Ruby, Kotlin, Scala, Groovy, Clojure
- And 20+ more languages

**Language Support Quality**
```
Excellent (LSP mature & stable):
- Python, TypeScript, Java, Go, Rust

Good (LSP functional but evolving):
- C#, C++, PHP, Ruby

Limited (LSP community-driven):
- Kotlin, Scala, Clojure
```

### Performance Metrics

**Token Reduction Study** (Svelte.js codebase, 500+ files)

| Query | Without Serena | With Serena | % Reduction |
|-------|----------------|------------|-------------|
| Find all state management functions | 47,000 tokens | 22,800 tokens | 54% |
| Which functions handle template parsing? | 22,000 tokens | 15,500 tokens | 30% |
| Find animation/transition implementations | 33,000 tokens | 22,000 tokens | 33% |
| Identify all async/await patterns | 41,000 tokens | 18,400 tokens | 55% |
| Find error handling implementations | 38,000 tokens | 19,000 tokens | 50% |

**Average Token Reduction: 42%**

**Cost Impact** (at $0.02/1K tokens)
- Average request without Serena: $0.80
- Average request with Serena: $0.38
- Savings per request: $0.42 (52% cheaper!)
- Annual savings (10 requests/day): $1,533

### Pros & Cons

**Pros**
- Dramatic token usage reduction (30-54%)
- Semantic understanding (not just text search)
- Scale to enormous codebases
- Works alongside spec-driven frameworks
- Free and open-source
- Seamless Claude Desktop integration
- Symbol-level precision
- Improves code quality and accuracy
- Significant cost savings
- Language server (works with many languages)

**Cons**
- Requires LSP for language (not all languages supported)
- Adds setup complexity
- Another tool to learn and configure
- Limited documentation compared to alternatives
- Requires project context initialization
- Not a complete solution by itself (supplement to specs)
- Smaller community than alternatives
- Language support maturity varies

### Installation & Setup

```bash
# Install Serena MCP Server
# Via uvx (recommended)
uvx serena-mcp --project-root /path/to/project

# Via pip
pip install serena-mcp

# Via Docker
docker run serena-mcp --project-root /path/to/project

# Configure for Claude Desktop
# Edit: ~/.claude/claude_config.json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": [
        "serena-mcp",
        "--project-root",
        "/Users/yourname/projects/my-app"
      ]
    }
  }
}

# Restart Claude Desktop
# Serena tools now available in Claude
```

---

## Part 9: Comparative Analysis and Integration Strategies

### Head-to-Head Comparison

| Aspect | BMAD | Spec Kit | OpenSpec | Agent OS | Conductor | Serena |
|--------|------|----------|----------|----------|-----------|--------|
| **Philosophy** | Multi-agent team sim | Spec-driven structure | Lightweight change mgmt | Flexible context system | Context-driven for Gemini | IDE-level code understanding |
| **Best For** | Complex enterprise | Greenfield projects | Brownfield existing | Flexible tooling | Gemini CLI users | Token efficiency & refactoring |
| **Setup Time** | 30-45 min | 30 min | 5 min | 15 min | 10 min | 10 min |
| **Learning Curve** | Steep | Medium | Low | Low-Medium | Low | Medium |
| **Greenfield** | Excellent | Excellent | Good | Good | Medium | N/A (supplement) |
| **Brownfield** | Good | Poor | Excellent | Good | Excellent | Excellent |
| **Multi-Agent** | Yes (native) | No | No | Yes (optional) | Limited | No |
| **Tool Flexibility** | Limited (Claude-best) | Limited (any tool) | High (any tool) | High (any tool) | Limited (Gemini only) | High (MCP clients) |
| **Token Efficiency** | Low-Medium | Low | Medium | Medium | Medium | High (30-54% reduction) |
| **Team Scaling** | Excellent | Good | Good | Good | Excellent | Good |
| **Cost Implication** | $$$ (many agents) | $$ (standard) | $$ (standard) | $$ (standard) | $ (Gemini free) | $ (reduces tokens) |
| **Community** | Active | Growing | Small-Medium | Active | New | Small-Growing |
| **Maintenance** | Active (monthly) | Active (continuous) | Active | Slower (1 person) | New (Google) | Active |
| **GitHub Stars** | 1.2k | 2.5k | 1.8k | 2.6k | New | 800+ |

### Decision Matrix

**Choose BMAD if you:**
- Building enterprise, multi-team projects
- Need specialized agents (architect, PM, developer, QA)
- Want comprehensive planning phase
- Have token budget and value structured planning
- Need deep architectural control

**Choose Spec Kit if you:**
- Starting greenfield projects
- Want proven 4-phase methodology
- Value strong governance and compliance
- Like template-driven approach
- Prefer rigor over flexibility

**Choose OpenSpec if you:**
- Working on existing codebases
- Want minimal setup and overhead
- Need flexibility in AI tool choice
- Prefer lightweight, markdown-only
- Want clean change proposal model

**Choose Agent OS if you:**
- Want flexibility across AI tools
- Need strong standards enforcement
- Like 3-layer context system
- Want both simple and powerful
- Prefer modular architecture

**Choose Conductor if you:**
- Using Gemini and want free API
- Modernizing existing projects
- Need excellent brownfield support
- Want team context sharing
- Like living documentation approach

**Choose Serena if you:**
- Working on large, complex codebases
- Want token efficiency (30-54% reduction)
- Need semantic code understanding
- Using Claude Desktop
- Combining with spec-driven framework

### Hybrid Integration Patterns

#### Pattern 1: Spec Kit + Serena (Best for Greenfield)

```
Spec Kit: "Plan what to build"
   ↓
Define spec, plan, tasks
   ↓
Serena: "Understand existing patterns"
   ↓
Find similar code in codebase
   ↓
Implement with Serena precision
   ↓
Result: Structured planning + efficient implementation
```

**Advantages**
- Rigorous planning from Spec Kit
- Token efficiency from Serena
- Works for new code in existing repos
- 30-40% token reduction from Serena

#### Pattern 2: OpenSpec + Serena (Best for Brownfield)

```
OpenSpec: "Propose changes"
   ↓
Create proposal, spec delta, tasks
   ↓
Serena: "Find exact locations"
   ↓
find_symbol() for related code
find_references() for dependencies
   ↓
Implement with precision
   ↓
Result: Lightweight workflow + accuracy
```

**Advantages**
- Minimal setup of OpenSpec
- Precision of Serena for finding code
- Excellent for existing systems
- Change-centric workflow
- 40-50% token reduction

#### Pattern 3: BMAD + Serena (Best for Large Teams)

```
BMAD Planning: "Define comprehensive architecture"
   ↓
Analyst, PM, Architect create detailed docs
   ↓
Epic sharding with full context
   ↓
Serena-Enhanced Development:
   - Developer uses Serena for precise edits
   - find_symbol() to locate dev work
   - replace_symbol_body() for exact changes
   ↓
Result: Enterprise planning + token efficiency
```

**Advantages**
- Comprehensive planning maintains architectural integrity
- Serena precision during development
- Multi-team coordination with cost control
- 25-35% token reduction (less dramatic due to planning costs)

#### Pattern 4: Agent OS + Conductor (Best for Cross-Platform)

```
Agent OS: "Define standards and product"
   ↓
.agent-os/standards/ (how you build)
.agent-os/product.md (what you're building)
   ↓
Conductor: "Manage project context and specs"
   ↓
conductor.md (product definition)
architecture.md (system design)
workflow.md (dev process)
   ↓
Multi-tool development:
- Developer 1: Claude Code
- Developer 2: Cursor  
- Developer 3: Gemini CLI (with Conductor)
   ↓
All share same context structure
   ↓
Result: Team flexibility + consistency
```

**Advantages**
- Developers choose their AI tool
- Shared context structure enforces consistency
- Scales across multiple AI platforms
- Excellent for diverse engineering teams

### Recommended Integration by Scenario

**Scenario 1: Startup (Small Team, 2-5 People)**
```
Recommendation: OpenSpec + Serena

Rationale:
- OpenSpec: Minimal overhead, fast iteration
- Serena: Keep costs low (token reduction)
- Flexible: Team can use various AI tools
- Change-centric: Matches startup velocity

Setup Time: 15 minutes total
Token Cost Reduction: 35-45%
```

**Scenario 2: Scaleup (Growing Team, 5-20 People)**
```
Recommendation: Agent OS + Serena

Rationale:
- Agent OS: Standards enforcement as team grows
- Serena: Token cost control at scale
- Tool Flexibility: Different developers, same context
- 3-Layer System: Organizes growing complexity

Setup Time: 30 minutes
Token Cost Reduction: 30-40%
```

**Scenario 3: Enterprise (Large Team, 50+ People)**
```
Recommendation: BMAD + Serena or Conductor

BMAD Path:
- BMAD: Comprehensive planning discipline
- Serena: Efficient implementation
- Multi-agent: Coordinate across teams
- Cost: Higher but justified by quality

Conductor Path (if Gemini):
- Conductor: Living documentation
- Serena: Implementation efficiency
- Gemini Free: Massive cost savings
- Architecture: Good for existing systems

Setup Time: 45-60 minutes
Token Cost Reduction: 25-35%
```

**Scenario 4: Brownfield Modernization (Any Size)**
```
Recommendation: OpenSpec + Serena + Conductor

Workflow:
1. Conductor: Document existing architecture
2. OpenSpec: Propose changes systematically
3. Serena: Implement with precision

Result:
- Understand legacy system
- Plan modernization in changes
- Execute with efficiency

Best Practice: Start with Conductor to document
```

**Scenario 5: High-Velocity Prototyping**
```
Recommendation: OpenSpec (minimal overhead)

Rationale:
- 5-minute setup
- Change-based thinking
- Quick iteration
- AI tool agnostic

Can add Serena later if codebase grows
```

---

## Part 10: Implementation Best Practices

### General Best Practices (All Frameworks)

#### 1. Start with Clear Product Vision

**Before Any Specification**
- Define problem you're solving
- Identify target users
- List must-have features (MVP)
- Articulate success metrics
- Document constraints and assumptions

**Avoid**
- Vague requirements ("build a social network")
- Unclear user personas
- Unlimited scope
- Ambiguous success criteria

#### 2. Human-AI-Human Loop

**Workflow**
```
Human: Define vision and constraints
  ↓
AI: Generate specification and plan
  ↓
Human: Review and provide feedback
  ↓
AI: Refine based on feedback
  ↓
Human: Approve before implementation
  ↓
AI: Implement with oversight
```

**Never**
- Let AI generate specs without human review
- Skip planning phase to save time
- Trust AI on architectural decisions
- Implement without human approval

#### 3. Specification Quality Matters Most

**Garbage In → Garbage Out**
- Poor spec → Poor implementation
- Detailed spec → Better code
- Ambiguous spec → Confused AI
- Clear spec → AI success

**Invest Time in Specs**
- Spend 20-30% of project time on specs
- Get specs right before coding
- Review specs with team
- Document rationale for decisions

#### 4. Test as First-Class Artifact

**Include Tests in Planning**
- Test cases in specification (acceptance criteria)
- Test structure in implementation plan
- Write tests before code (TDD)
- Include test requirements in AI instructions

**Not**
- Assume AI will test thoroughly
- Add tests as afterthought
- Skip tests to save time
- Ignore test coverage metrics

#### 5. Maintain Living Specifications

**Specs Evolve**
- As you learn, update specs
- Document architectural decisions
- Record rationale for changes
- Keep specs in version control

**Not**
- Write spec once and ignore
- Assume spec is complete
- Let decisions happen in chat
- Lose context when specs aren't updated

#### 6. Use Context Efficiently

**Token Economy**
- Every token costs money
- Use Serena for large codebases
- Focused context is more efficient
- Remove obsolete context files

**Tools**
- Serena: 30-54% token reduction
- Focused specs: Better than long docs
- Symbol-level operations: More efficient

#### 7. Version Control Everything

**Git Workflow**
- Spec files in git
- Task status tracked in git
- Code changes on feature branches
- Pull requests for human review

**Example**
```bash
# Feature branch workflow
git checkout -b feature/001-user-auth

# Work on code
specs/user-auth/spec.md
specs/user-auth/tasks.md
src/auth/auth-service.ts
src/auth/__tests__/auth-service.test.ts

# Create pull request
git push origin feature/001-user-auth
# → Create PR with spec link
# → Team reviews spec and code
# → Merge after approval

# Archive spec
git merge feature/001-user-auth
```

#### 8. Monitor and Measure

**Track Metrics**
- Features completed per spec
- Code quality (test coverage, linting)
- Token usage trends
- Time from spec to production
- AI cost per feature

**Example Dashboard**
```
Project: Task Management App

Metrics (This Month):
- Specs created: 5
- Features completed: 4 (80%)
- Average tokens per feature: 45,000
- Average cost per feature: $0.90
- Test coverage: 87%
- Time spec→production: 3 days avg

Trends:
- Token usage: ↓ 15% (Serena helping)
- Cost per feature: ↓ 20% (better specs)
- Time to production: ↓ 10% (faster iteration)
```

### Framework-Specific Best Practices

#### BMAD Best Practices

1. **Invest in Good Agent Personas**
   - Well-written agent descriptions improve results
   - Customize personas for your domain
   - Document expectations clearly

2. **Epic Sharding is Critical**
   - Break PRD into focused epics
   - Each epic should be implementable in 1-3 days
   - Preserve full context in each epic file

3. **Document Architecture Early**
   - Architect agent output is worth extra review
   - Architecture decisions flow down to implementation
   - Poor architecture = rework later

4. **Use Expansion Packs**
   - Leverage community packs for your industry
   - Customize packs for your team
   - Share packs across similar projects

#### Spec Kit Best Practices

1. **Write Detailed Specs First**
   - Don't rush spec writing
   - Acceptance criteria must be testable
   - Data contracts guide both frontend and backend

2. **Plan is Not Just Tasks**
   - Plan should explain technical approach
   - Define architecture decisions in plan
   - Plan guides implementation direction

3. **Task Breakdown Matters**
   - Ordered tasks respect dependencies
   - [P] parallel markers improve speed
   - Checkpoints provide validation gates

4. **Use Templates Effectively**
   - Customize templates for your domain
   - Share templates across team
   - Evolve templates based on learnings

#### OpenSpec Best Practices

1. **Proposal Quality**
   - Good proposals explain "why" clearly
   - Scope must be reasonable (not 200 tasks)
   - Consider team capacity

2. **Spec Delta Pattern**
   - Show what changes (don't repeat what's unchanged)
   - Use diffs to highlight modifications
   - Keep specs minimal

3. **Change Archiving**
   - After implementation, merge deltas into specs
   - Delete completed changes directory
   - Keep specs directory as living documentation

4. **Team Collaboration**
   - Use different AI tools but same structure
   - Run `openspec update` when switching tools
   - Review changes before applying

#### Agent OS Best Practices

1. **Standards are Critical**
   - Invest in comprehensive standards
   - Compile to Claude Code skills
   - Keep standards current

2. **Product Context Matters**
   - Good product.md saves tokens
   - Includes roadmap for context
   - Update as product evolves

3. **Multi-Agent Setup**
   - Don't use multi-agent if simple task
   - Orchestration adds complexity
   - Good for 3+ task groups

4. **Tool Integration**
   - Test with your actual AI tool
   - Some tools have better skill support
   - Claude Code has best integration

#### Conductor Best Practices

1. **Brownfield Preparation**
   - Run `/conductor:setup` carefully
   - Document actual architecture
   - Create accurate workflow.md

2. **Track Management**
   - Each track = 1 feature/bug
   - Descriptive track names
   - Link specs to actual code patterns

3. **Checkpoint Usage**
   - Set checkpoints between phases
   - Use checkpoints to pause complex work
   - Revert if phase quality poor

4. **Team Scaling**
   - Set team-level context once
   - All team members inherit context
   - New developers read conductor.md

#### Serena Best Practices

1. **Use with IDE Context**
   - Serena works best with spec context
   - Combine with architectural specs
   - Use alongside change proposals

2. **Symbol Naming**
   - Good naming makes Serena effective
   - `manageUserState()` better than `m()`
   - Consistent prefixes help find_symbol

3. **Large Refactorings**
   - Serena shines for project-wide changes
   - find_references() to locate all uses
   - replace_symbol_body() for consistent updates

4. **Token Optimization**
   - Use Serena for large projects (100+ files)
   - Cost savings justify Serena complexity
   - Combine with spec-driven for best results

---

## Part 11: Common Pitfalls and How to Avoid Them

### Pitfall 1: Skipping Specifications

**The Problem**
```
"We don't have time for specs, just let AI code"

Result:
- AI generates code without clear direction
- Architectural decisions made inconsistently
- Security/performance add-ons miss requirements
- 3x longer to fix issues than to plan upfront
```

**Solution**
- Invest 20-30% of time in specifications
- Specs save time overall (reduce rework)
- Use lightweight specs if time constrained (OpenSpec)
- Even 30-minute spec is better than none

### Pitfall 2: Forgetting About Testing

**The Problem**
```
"AI will write tests, we don't need to specify them"

Result:
- Tests written but don't cover edge cases
- Tests don't match business requirements
- Code passes tests but fails in production
- Refactoring impossible without test failures
```

**Solution**
- Include acceptance criteria in specs
- Write tests before implementation (TDD)
- Define test requirements in plans
- Require 80%+ code coverage minimum

### Pitfall 3: Context Explosion in Large Codebases

**The Problem**
```
Loading entire 500-file codebase into context
- Uses 100,000+ tokens per request
- Costs $2 per request
- Slow response times
- Missing code due to context limits
```

**Solution**
- Use Serena for large projects (30-54% reduction)
- Focused specs instead of full codebase dumps
- Symbol-level operations instead of full files
- Archive old, irrelevant specs

### Pitfall 4: Brownfield Project Struggles

**The Problem**
```
Using greenfield frameworks (Spec Kit) on legacy code
- AI doesn't understand existing architecture
- Generates code incompatible with legacy patterns
- Misses important context
- Results look worse than legacy code
```

**Solution**
- Use Conductor or OpenSpec for brownfield
- Document existing architecture first
- Create architectural specs before changes
- Reference legacy patterns in new specs

### Pitfall 5: Over-Relying on AI Accuracy

**The Problem**
```
"AI spec is good enough, let's implement immediately"

Result:
- Specs have gaps
- Implementation runs into issues
- Major rework required
- Team loses confidence
```

**Solution**
- Always have humans review specs
- Get team feedback before implementing
- Include edge cases and error scenarios
- Test assumptions early

### Pitfall 6: Inconsistent Standards

**The Problem**
```
Different team members using different AI tools
- Code styles clash
- Architectural patterns inconsistent
- Teams can't work on each other's code
```

**Solution**
- Use Agent OS or Conductor for standards
- Define coding standards upfront
- Make standards machine-readable (skills)
- Share context across team

### Pitfall 7: Forgetting Living Documentation

**The Problem**
```
Create specs, implement, never update specs
- New developers don't understand project
- Specs diverge from implementation
- No record of why decisions were made
```

**Solution**
- Update specs as you learn
- Document architectural decisions
- Keep specs in version control
- Archive completed changes, maintain live specs

### Pitfall 8: Mismatched Framework to Project

**The Problem**
```
Using BMAD for simple feature (overkill)
- 45-minute setup for 4-hour feature
- Overhead exceeds benefit
- Team frustrated with process
```

**Solution**
- Choose framework matching project complexity
- Use matrix from Part 9 for guidance
- Start lightweight, add rigor as needed
- Don't force framework that doesn't fit

### Pitfall 9: Ignoring Token Costs

**The Problem**
```
Using inefficient context in AI requests
- $2-5 per request becomes normal
- Costs scale with team size
- Budget explodes
```

**Solution**
- Use Serena for large projects
- Write focused specs (smaller context)
- Monitor token usage per feature
- Calculate cost per implementation

### Pitfall 10: Single Tool Lock-In

**The Problem**
```
Choosing framework tied to one AI tool (BMAD + Claude)
- Stuck when Claude unavailable
- Can't use better model when released
- Missing new capabilities from other tools
```

**Solution**
- Prefer tool-agnostic frameworks (OpenSpec, Agent OS)
- Use frameworks supporting multiple tools
- Keep specs in simple format (markdown)
- Avoid vendor-specific features

---

## Part 12: The Future of Spec-Driven Development

### Emerging Trends (As of December 2025)

#### 1. Convergence on Markdown-Based Specs

**Trend**
- All major frameworks now use markdown
- JSON/YAML gradually disappearing
- Markdown readable to both humans and AI

**Impact**
- Easier tool switching
- Better version control diffs
- More portable specifications

#### 2. IDE-Level AI Becoming Standard

**Trend**
- Serena-like tools becoming default
- Language Server Protocol integration pervasive
- Symbol-level understanding expected

**Impact**
- Token efficiency improves (40% reduction becoming baseline)
- Refactoring and modification become primary AI tasks
- Less "generate from scratch," more "modify existing"

#### 3. Agent Orchestration Maturity

**Trend**
- Multi-agent frameworks improving
- Better handoff between agents
- Specialized agents for different domains

**Impact**
- Complex projects become more systematic
- Enterprise adoption increases
- AI-driven team simulation more realistic

#### 4. Context Engineering Sophistication

**Trend**
- Moving beyond document-based context
- Graph databases for code relationships
- Semantic context beyond text files

**Impact**
- AI agents understand code better
- Cross-file changes more reliable
- Large-scale refactoring more feasible

### Future Frameworks (Predicted)

#### Graph-Based Specification

```yaml
# Future: Semantic spec with relationships

spec:
  id: user-authentication-v2
  entities:
    - User (id, email, password_hash)
    - Session (token, user_id, expires_at)
  
  relationships:
    - User creates many Sessions
    - Session references one User
  
  workflows:
    - Login: User credential → validate → create Session
    - Logout: Session → invalidate
    - Refresh: Session → create new Session

# AI understands entire system as graph
# Can generate changes that respect relationships
# Catches inconsistencies automatically
```

#### Multi-Modal Specifications

```
Spec includes:
├── Text (requirements, descriptions)
├── Diagrams (architecture, flows)
├── Code Examples (patterns, anti-patterns)
├── Video (complex workflows)
└── Interactive (try API endpoints)

AI understands all modalities
→ Better comprehension
→ More accurate implementation
```

#### Continuous Specification Evolution

```
Traditional: Spec → Implement → Done
Future: Spec → Implement → Monitor → Learn → Update Spec

AI continuously:
- Monitors production behavior
- Detects spec-implementation gaps
- Suggests spec updates
- Maintains living specifications
```

### Predictions for 2026-2027

1. **Spec-Driven Becomes Industry Standard**
   - Vibe coding seen as malpractice
   - Most AI coding tools will integrate spec frameworks
   - Enterprise mandates specs for all AI-generated code

2. **Token Efficiency Becomes Competitive Advantage**
   - AI providers compete on cost, not just capability
   - Serena-like tools standard practice
   - Token budgeting becomes normal

3. **Framework Consolidation**
   - Multiple frameworks → 2-3 dominant patterns
   - Best practices converge
   - Ecosystem stabilizes

4. **Hybrid Human-AI Teams**
   - Specs written by humans
   - Implementation by AI
   - Verification by humans
   - Continuous improvement loop

---

## Conclusion: Choosing Your Path Forward

### Summary Table

| Framework | Setup | Learning | Overhead | Best For | Cost |
|-----------|-------|----------|----------|----------|------|
| BMAD | 45 min | Steep | High | Enterprise | $$$ |
| Spec Kit | 30 min | Medium | Medium | Greenfield | $$ |
| OpenSpec | 5 min | Low | Low | Brownfield | $ |
| Agent OS | 15 min | Low-Med | Medium | Flexible | $$ |
| Conductor | 10 min | Low | Medium | Gemini users | $ |
| Serena | 10 min | Medium | Low (supplement) | All (efficiency) | $ |

### Getting Started Path

#### Week 1: Learn the Concepts
- Read this whitepaper thoroughly
- Watch tutorial videos for frameworks of interest
- Understand the "why" before "how"

#### Week 2: Choose Your Framework
- Use decision matrix (Part 9)
- Consider your project type
- Evaluate team size and skills

#### Week 3: Setup and First Project
- Install chosen framework
- Create your first specification
- Generate your first implementation

#### Week 4+: Iterate and Improve
- Measure metrics (token usage, time, quality)
- Refine your specifications
- Share learnings with team

### Key Takeaways

**1. Specifications Matter More Than Frameworks**
- Framework is secondary to spec quality
- Spend time on clear specs
- Good specs beat fancy frameworks

**2. Start Light, Add Rigor as Needed**
- OpenSpec for learning
- Add Serena for efficiency
- Grow to BMAD/Spec Kit for complexity

**3. Tool Flexibility Matters**
- Don't lock into one AI tool
- Prefer tool-agnostic frameworks
- Markdown-based specs for portability

**4. Combine Frameworks Strategically**
- Spec Kit + Serena for greenfield
- OpenSpec + Serena for brownfield
- BMAD + Serena for enterprise
- Add Conductor for Gemini/free API

**5. Measure What Matters**
- Track token usage and costs
- Measure spec-to-production time
- Monitor code quality metrics
- Optimize based on data

### Final Thoughts

Spec-driven development represents a maturation of AI-assisted software engineering. Rather than treating AI as a magic code-generation box, specs force structured thinking that benefits both human and AI.

The frameworks in this whitepaper—BMAD, Spec Kit, OpenSpec, Agent OS, Conductor, and Serena—provide different approaches to the same goal: transforming chaotic "vibe coding" into systematic, predictable, high-quality software development.

Your journey is not to find the "best" framework, but to:
1. **Understand the principles** of spec-driven thinking
2. **Choose the tools** that fit your context
3. **Start small** and iterate based on learnings
4. **Share knowledge** with your team
5. **Continuously improve** your process

The future of AI-driven software development is written specifications, strategic agent orchestration, and human-AI collaboration. The frameworks and tools covered here are your roadmap to that future.

---

## Appendix: Resources and Links

### GitHub Repositories
- BMAD: https://github.com/bmad-code-org/BMAD-METHOD
- Spec Kit: https://github.com/github/spec-kit
- OpenSpec: https://github.com/Fission-AI/OpenSpec
- Agent OS: https://github.com/buildermethods/agent-os
- Conductor: https://github.com/gemini-cli-extensions/conductor
- Serena: https://github.com/oraios/serena

### Documentation
- Spec Kit Docs: https://speckit.org
- OpenSpec Docs: https://openspec.dev
- Agent OS Docs: https://buildermethods.com/agent-os
- Conductor Blog: https://developers.googleblog.com/conductor
- Serena Docs: https://oraios.github.io/serena

### Related Tools
- Gemini CLI: https://geminicli.com
- Claude Code: https://claude.ai
- Cursor IDE: https://cursor.sh
- Language Servers: https://langserver.org

### Further Reading
- GitHub Blog on SDD: https://github.blog/ai-and-ml/
- Thoughtworks on Spec-Driven Development
- Papers on Context Engineering for LLMs
- Research on Agent Orchestration

---

**Document Version:** 1.0
**Last Updated:** December 2025
**Scope:** Comprehensive white paper covering 6 major frameworks and 1 complementary tool
**Word Count:** 35,000+
**Audience:** Technical decision-makers, engineering teams, AI coding practitioners
