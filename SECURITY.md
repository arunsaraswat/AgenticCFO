# Security Guidelines

## Environment Variables and Secrets

### ⚠️ CRITICAL: Never Commit Secrets

**NEVER commit the following files:**
- `.env` files (backend/.env, frontend/.env, etc.)
- API keys, tokens, passwords
- Private keys (.pem, .key files)
- Service account credentials
- Database connection strings with actual credentials

### ✅ Safe Practices

1. **Use .env.example files:**
   - Commit `.env.example` files with placeholder values
   - Document all required environment variables
   - Never include actual secrets

2. **Check .gitignore:**
   - Verify `.env` is in `.gitignore` (already configured)
   - Root-level `.gitignore` provides additional protection
   - Backend and frontend have their own `.gitignore` files

3. **Before committing:**
   ```bash
   # Always verify what you're committing
   git status
   git diff --staged

   # Look for accidentally included secrets
   git diff --staged | grep -i "password\|secret\|key\|token"
   ```

4. **If you accidentally commit secrets:**
   ```bash
   # IMMEDIATELY rotate/revoke the exposed credentials
   # Then remove from git history:
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch backend/.env" \
     --prune-empty --tag-name-filter cat -- --all

   # Force push (coordinate with team first!)
   git push origin --force --all
   ```

### Current Secrets Configuration

**Backend (.env):**
- `DATABASE_URL` - Supabase PostgreSQL connection string
- `SECRET_KEY` - JWT signing key
- `OPENROUTER_API_KEY` - OpenRouter API key for LLM access

**Frontend (.env):**
- `VITE_API_BASE_URL` - Backend API URL (safe to commit if public)

### Setup for New Developers

```bash
# 1. Copy example files
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. Fill in actual values (get from team lead or 1Password)
# Edit backend/.env with real:
#   - DATABASE_URL
#   - SECRET_KEY
#   - OPENROUTER_API_KEY

# 3. Verify .env is not tracked
git status  # Should NOT show .env files
```

### Production Deployment

- **Never** store secrets in code repositories
- Use environment variable management:
  - Vercel: Environment Variables in project settings
  - Docker: `.env` files or Docker secrets
  - Kubernetes: Secrets or sealed-secrets
  - AWS: Systems Manager Parameter Store or Secrets Manager

### OpenRouter API Key Security

Your OpenRouter key provides access to multiple LLM providers and incurs costs:

1. **Protect the key:**
   - Never commit to git
   - Rotate if exposed
   - Monitor usage at openrouter.ai/dashboard

2. **Production best practices:**
   - Use separate keys for dev/staging/prod
   - Set spending limits in OpenRouter dashboard
   - Enable usage alerts
   - Rotate keys quarterly

3. **If key is exposed:**
   - Go to https://openrouter.ai/keys
   - Revoke the exposed key immediately
   - Generate a new key
   - Update all deployments

### Verification Checklist

Before every commit:
- [ ] Run `git status` - no `.env` files listed
- [ ] Run `git diff --staged | grep -i "sk-or-v1"` - no API keys
- [ ] Run `git diff --staged | grep -i "password"` - no passwords
- [ ] Check for database URLs with actual credentials
- [ ] Verify only `.env.example` files are staged, not `.env`

### Automated Protection

Consider adding a pre-commit hook:

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for .env files
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "ERROR: Attempting to commit .env file!"
    echo "Please remove it from staging: git reset HEAD backend/.env"
    exit 1
fi

# Check for API keys
if git diff --cached | grep -q "sk-or-v1-[a-zA-Z0-9]"; then
    echo "ERROR: Potential API key detected in commit!"
    exit 1
fi
```

### Current Status: ✅ SECURE

- `.env` files are properly gitignored
- No secrets currently in repository
- `.env.example` files provide safe templates
- Root-level `.gitignore` adds extra protection

**Last Security Audit:** October 17, 2025
**Audited By:** Claude Code
**Status:** No secrets detected in repository
