---
description: Stage, commit, and push all changes to the repository
---

# Ship Command

Stage all changes, create a commit with a meaningful message, and push to the remote repository.

## Instructions

1. **Check Git Status**: Run `git status` to see all changes
2. **Review Changes**: Run `git diff` to see unstaged changes and `git diff --staged` to see staged changes
3. **Review Recent Commits**: Run `git log --oneline -5` to see recent commit message style
4. **Stage All Changes**: Add all changes using `git add .`
5. **Create Commit Message**:
   - Analyze all changes (both staged and unstaged)
   - Write a clear, concise commit message that:
     - Starts with a verb (Add, Update, Fix, Refactor, Remove, etc.)
     - Summarizes the "why" not just the "what"
     - Follows the existing commit message style from git log
     - Is 1-2 sentences maximum
     - Ends with the standard footer:
       ```

       🤖 Generated with [Claude Code](https://claude.com/claude-code)

       Co-Authored-By: Claude <noreply@anthropic.com>
       ```
6. **Commit Changes**: Create the commit with the message using HEREDOC format
7. **Push to Remote**: Push the changes to the remote repository with `git push`
8. **Confirm Success**: Run `git status` to verify the push was successful

## Important Notes

- **Do NOT push force** unless explicitly requested
- **Do NOT skip hooks** (--no-verify)
- **Do NOT amend** unless explicitly requested or adding pre-commit hook edits
- If there are no changes to commit, inform the user
- If push fails due to remote changes, inform the user and suggest pulling first
- Always use HEREDOC format for commit messages to ensure proper formatting

## Example Commit Message Format

```bash
git commit -m "$(cat <<'EOF'
Add custom ship command for streamlined git workflow

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```
