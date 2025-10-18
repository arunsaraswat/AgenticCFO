# Claude Code Custom Agents

This directory contains custom slash commands that invoke specialized Claude Code subagents for code review and quality assurance.

## Available Agents

### 1. UX Review Agent (`/ux-review`)

**Purpose:** Reviews frontend code for UX/UI best practices, design system compliance, and accessibility.

**When to Use:**
- Before committing new frontend components
- After implementing dashboard features
- Before pull requests involving UI changes
- When unsure about design decisions
- To ensure consistency across the platform

**What It Reviews:**
- ✅ Visual design (color palette, typography, spacing)
- ✅ Component patterns (KPI cards, charts, tables, filters)
- ✅ Interaction design (hover, active, disabled states)
- ✅ Responsive design (mobile, tablet, desktop)
- ✅ Accessibility (WCAG 2.1 AA compliance)
- ✅ Performance (rendering, bundle size, lazy loading)
- ✅ Design system alignment (based on reference dashboards)

**Usage:**
```bash
# Review all frontend files
/ux-review

# Review specific component
/ux-review src/components/Dashboard.tsx

# Focus on accessibility
/ux-review --accessibility

# Focus on mobile responsiveness
/ux-review --mobile
```

**Example Output:**
- Overall assessment (Good / Needs Work / Poor)
- Categorized issues (Critical 🔴 / Major 🟡 / Minor 🟢)
- Specific fixes with code examples
- Best practices applied
- Suggested enhancements
- Prioritized next steps with time estimates

**Design System Reference:**
- **Guidelines:** `.claude/UX_DESIGN_GUIDELINES.md`
- **Sample Review:** `.claude/SAMPLE_UX_REVIEW.md`
- **Color Palette:** Blues (#1F4E78, #4472C4, #8AB4F8) + semantic colors
- **Typography:** 48/24/16/14/12/10px scale
- **Spacing:** 8px grid system

---

### 2. Architect Review Agent (`/architect-review`)

**Purpose:** Reviews code for architectural alignment, best practices, and design patterns.

**When to Use:**
- After implementing new API endpoints
- After creating new services or models
- After significant refactoring
- Before submitting pull requests
- When unsure about architectural decisions

**What It Reviews:**
- ✅ Adherence to Agentic CFO 5-layer architecture
- ✅ FastAPI best practices (dependency injection, status codes, error handling)
- ✅ Database patterns (SQLAlchemy, indexing, JSONB usage)
- ✅ Service layer separation and SOLID principles
- ✅ Security (authentication, authorization, input validation)
- ✅ Type safety and Pydantic schema validation
- ✅ Code quality (naming, documentation, error messages)

**Usage:**
```bash
# In Claude Code, invoke the command:
/architect-review

# The agent will analyze the current context and provide detailed feedback
```

**Example Output:**
- Summary of architectural compliance
- Strengths found in the code
- Recommendations with priority levels (P0-P3)
- Critical issues that must be fixed
- Specific feedback by file with code examples
- Prioritized action items

---

### 3. Tester Review Agent (`/tester-review`)

**Purpose:** Analyzes test coverage and identifies missing test cases for all code.

**When to Use:**
- After creating new API endpoints
- After implementing new services
- Before submitting pull requests
- When test coverage seems incomplete
- To get test implementation examples

**What It Reviews:**
- ✅ Test coverage for API endpoints (success, error, edge cases)
- ✅ Test quality (assertions, fixtures, isolation)
- ✅ Test patterns compliance (AAA pattern, proper fixtures)
- ✅ Edge cases and boundary conditions
- ✅ Authentication and authorization tests
- ✅ Integration test completeness

**Coverage Analysis:**
- Success cases (happy path, correct status codes)
- Error cases (401, 403, 404, 422, 400, 409)
- Edge cases (empty values, max length, special characters)
- Authentication scenarios (no token, invalid token, expired token)
- Service layer testing
- Database model testing

**Usage:**
```bash
# In Claude Code, invoke the command:
/tester-review

# The agent will analyze test coverage and provide missing test implementations
```

**Example Output:**
- Coverage score and assessment
- Test inventory (existing tests)
- Untested components
- Coverage gap analysis (P0-P3 priorities)
- Existing test quality issues
- Complete, ready-to-use test code for critical gaps
- Test organization recommendations

---

## How These Agents Work

These are **Claude Code slash commands** that provide specialized prompts to Claude. When you invoke them:

1. **Context Awareness:** The agent analyzes files in your current IDE context
2. **Deep Analysis:** Applies domain-specific expertise (FastAPI, testing, Agentic CFO architecture)
3. **Actionable Output:** Provides specific recommendations with file references and code examples
4. **Priority Levels:** Categorizes issues as P0 (Critical), P1 (High), P2 (Medium), P3 (Low)

## Workflow Integration

### Recommended Development Flow

**Backend Development:**
```bash
# 1. Implement new feature
# Edit files in backend/app/api/, backend/app/services/, etc.

# 2. Run architect review
/architect-review
# Fix any P0/P1 issues found

# 3. Run tester review
/tester-review
# Implement missing tests identified

# 4. Run tests
cd backend
./test.sh

# 5. Verify coverage
pytest --cov=app --cov-report=term-missing

# 6. Commit changes
git add .
git commit -m "Add new feature with comprehensive tests"
```

**Frontend Development:**
```bash
# 1. Implement new component
# Edit files in frontend/src/components/, etc.

# 2. Run UX review
/ux-review
# Fix any critical/major issues found

# 3. Test manually
# - Check mobile responsiveness
# - Test keyboard navigation
# - Verify color contrast

# 4. Run frontend tests
cd frontend
./test.sh

# 5. Commit changes
git add .
git commit -m "Add dashboard component with UX polish"
```

### Example: Adding a New API Endpoint

```bash
# Step 1: Create the endpoint
# - backend/app/api/new_feature.py
# - backend/app/services/new_feature_service.py
# - backend/app/schemas/new_feature.py

# Step 2: Review architecture
/architect-review
# Output: "⚠️ Missing authentication on endpoint, no database index on tenant_id"
# Fix issues

# Step 3: Review tests
/tester-review
# Output: "❌ No tests found for POST /api/new-feature"
# Agent provides complete test code

# Step 4: Implement tests
# Copy test code from agent output to backend/tests/test_new_feature.py

# Step 5: Verify
./test.sh
# All tests pass!
```

## Benefits

### For Development Velocity
- **Faster Reviews:** Instant feedback without waiting for PR reviews
- **Learn Patterns:** See correct implementations and patterns
- **Reduce Rework:** Catch issues before they reach CI/CD

### For Code Quality
- **Consistency:** Enforces Agentic CFO architectural patterns
- **Security:** Identifies auth, validation, and security gaps
- **Test Coverage:** Ensures 70%+ coverage target (per CLAUDE.md)
- **Best Practices:** Validates FastAPI, SQLAlchemy, pytest patterns

### For Team Alignment
- **Documentation:** Agents reference CLAUDE.md and docs/architecture.md
- **Standards:** Consistent code review criteria
- **Onboarding:** New developers learn patterns from agent feedback

## Customization

### Modifying Agent Prompts

Edit the markdown files to customize agent behavior:

- **`.claude/commands/architect-review.md`** - Architecture review criteria
- **`.claude/commands/tester-review.md`** - Test coverage criteria

### Adding New Agents

Create new slash commands for specialized reviews:

```bash
# Example: Create a security-focused agent
cat > .claude/commands/security-review.md << 'EOF'
# Security Review Agent

Review code for security vulnerabilities:
- SQL injection prevention
- Authentication bypass risks
- Authorization gaps
- Input validation weaknesses
- Secret exposure
...
EOF
```

Then use: `/security-review`

## Reference Documentation

These agents reference and enforce standards from:

- **`CLAUDE.md`** - Project structure, development commands, architecture overview
- **`docs/architecture.md`** - Comprehensive 5-layer architecture design
- **`backend/tests/conftest.py`** - Test fixtures and patterns
- **Existing code** - API routes, services, models as pattern examples

## Support

If the agents provide unclear feedback or miss important issues:

1. **Refine the prompt:** Edit the `.md` file to add more specific criteria
2. **Provide more context:** Include relevant files in your IDE selection
3. **Iterate:** Run the agent again after making changes
4. **Ask questions:** Request clarification on specific recommendations

## Version

- **Created:** October 2025
- **UX Review Agent:** v1.0 (2025-10-17)
- **Architect Agent:** v1.0
- **Tester Agent:** v1.0
- **Maintained by:** Agentic CFO Platform Team
