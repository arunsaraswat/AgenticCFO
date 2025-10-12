#!/bin/bash

# GitHub Setup Commands for AgenticCFO
# Run these commands after creating your repository on GitHub

echo "================================================"
echo "  GitHub Repository Setup Commands"
echo "================================================"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " github_username

# Get repository name (default: AgenticCFO)
read -p "Enter repository name [AgenticCFO]: " repo_name
repo_name=${repo_name:-AgenticCFO}

echo ""
echo "================================================"
echo "Step 1: Verify you've created the repository"
echo "================================================"
echo ""
echo "Go to: https://github.com/new"
echo "Repository name: $repo_name"
echo "Description: Production-ready full-stack application template with FastAPI + React + TypeScript"
echo "Visibility: Choose Public or Private"
echo "DO NOT initialize with README, .gitignore, or license"
echo ""
read -p "Press Enter when you've created the repository on GitHub..."

echo ""
echo "================================================"
echo "Step 2: Adding remote and pushing to GitHub"
echo "================================================"
echo ""

# Add remote
echo "Adding GitHub remote..."
git remote add origin "https://github.com/$github_username/$repo_name.git"

# Verify remote
echo ""
echo "Remote added. Verifying..."
git remote -v

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "================================================"
echo "  Success! ✅"
echo "================================================"
echo ""
echo "Your repository is now on GitHub at:"
echo "https://github.com/$github_username/$repo_name"
echo ""
echo "Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Add topics/tags: fastapi, react, typescript, full-stack"
echo "3. Add a license (recommended: MIT)"
echo "4. Consider making it a template repository"
echo ""
echo "Share your repository:"
echo "https://github.com/$github_username/$repo_name"
echo ""
