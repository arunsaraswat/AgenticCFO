# GitHub Setup Guide

## Step 1: Create GitHub Repository

1. Go to [GitHub](https://github.com)
2. Click the "+" icon in the top right → "New repository"
3. Fill in repository details:
   - **Repository name**: `AgenticCFO` (or your preferred name)
   - **Description**: Production-ready full-stack application template with FastAPI + React + TypeScript
   - **Visibility**: Choose Public or Private
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
4. Click "Create repository"

## Step 2: Link Local Repository to GitHub

After creating the repository on GitHub, run these commands from your project root:

```bash
# Add all files to git
git add .

# Create initial commit
git commit -m "Initial commit: Complete full-stack application template

- FastAPI backend with JWT authentication
- React + TypeScript frontend with Tailwind CSS
- SQLAlchemy ORM with Alembic migrations
- Comprehensive test suites (70%+ coverage)
- Complete documentation
- Ready-to-run scripts"

# Add GitHub remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/AgenticCFO.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Verify Upload

1. Refresh your GitHub repository page
2. You should see all files uploaded
3. The README.md will be displayed automatically

## Quick Commands

### If you created the repository with a different name:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

### To check remote URL:
```bash
git remote -v
```

### To update remote URL:
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## What Will Be Pushed

The following will be included in your GitHub repository:
- ✅ Complete backend application (FastAPI)
- ✅ Complete frontend application (React + TypeScript)
- ✅ All documentation files
- ✅ Test suites
- ✅ Configuration files
- ✅ Shell scripts
- ✅ .gitignore files (excluding sensitive data)

**NOT included** (as per .gitignore):
- ❌ node_modules/
- ❌ venv/
- ❌ .env files (sensitive data)
- ❌ __pycache__/
- ❌ Build artifacts

## Repository Settings (Optional)

### Add Topics/Tags
Add these topics to your repository for better discoverability:
- `fastapi`
- `react`
- `typescript`
- `tailwindcss`
- `full-stack`
- `jwt-authentication`
- `sqlalchemy`
- `alembic`
- `template`
- `starter-kit`

### Set Repository Description
```
Production-ready full-stack application template with FastAPI backend, React+TypeScript frontend, JWT auth, and comprehensive testing
```

### Add a License (Recommended)
1. Go to your repository → "Add file" → "Create new file"
2. Name it `LICENSE`
3. Click "Choose a license template"
4. Select MIT License (or your preference)
5. Commit

## Using SSH Instead of HTTPS

If you prefer SSH:

```bash
# Add remote with SSH
git remote add origin git@github.com:YOUR_USERNAME/AgenticCFO.git

# Or change existing remote
git remote set-url origin git@github.com:YOUR_USERNAME/AgenticCFO.git
```

## Cloning the Repository

After pushing, anyone can clone your repository:

```bash
# Clone via HTTPS
git clone https://github.com/YOUR_USERNAME/AgenticCFO.git

# Clone via SSH
git clone git@github.com:YOUR_USERNAME/AgenticCFO.git
```

## GitHub Actions (CI/CD) - Optional

Consider adding GitHub Actions for automated testing:

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  backend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          cd backend
          pytest

  frontend-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd frontend
          npm install
      - name: Run tests
        run: |
          cd frontend
          npm test
```

## Protecting Secrets

**IMPORTANT**: Never commit sensitive data!

Files that are already excluded by .gitignore:
- `.env` files
- `venv/` directories
- `node_modules/`
- Database files

If you accidentally committed secrets:
1. Remove them from git history: `git filter-branch` or use BFG Repo-Cleaner
2. Rotate all compromised credentials immediately
3. Update .gitignore to prevent future commits

## Making Your Repository a Template

To allow others to use this as a template:

1. Go to repository Settings
2. Check "Template repository"
3. Users can now click "Use this template" to create their own copy

## Collaboration

### Adding Collaborators
1. Go to Settings → Collaborators
2. Add team members by username

### Branch Protection (Recommended for teams)
1. Go to Settings → Branches
2. Add rule for `main` branch
3. Enable:
   - Require pull request reviews
   - Require status checks to pass
   - Require branches to be up to date

## README Badges (Optional)

Add badges to your README:

```markdown
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)
![React](https://img.shields.io/badge/react-18+-blue.svg)
![TypeScript](https://img.shields.io/badge/typescript-5.3+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
```

## Next Steps After Pushing

1. ✅ Verify all files are on GitHub
2. ✅ Add repository description and topics
3. ✅ Add a license if you haven't
4. ✅ Consider making it a template repository
5. ✅ Share with the community!

## Troubleshooting

### "Repository not found" error
- Check repository name matches
- Verify you have access to the repository
- Try HTTPS instead of SSH (or vice versa)

### Large files rejected
- Check if any files exceed GitHub's 100MB limit
- Use Git LFS for large files if needed

### Authentication failed
- Ensure you're using a personal access token (not password)
- Generate token at: Settings → Developer settings → Personal access tokens

### Permission denied
- Verify you have write access to the repository
- Check SSH keys are set up correctly (if using SSH)

---

**You're all set!** Your repository is ready to share with the world. 🚀
