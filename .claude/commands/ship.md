---
description: Stage, commit, and push all changes to the repository
---

# Ship Command

Stage all changes, create a commit with a meaningful message, and push to the remote repository.

## Instructions

1. **Update README Status**: Before committing, analyze the current state of the project and update the README.md status line
   - Read PROGRESS.md to understand current completion state
   - Check git status to see what changed
   - Update the "Current Status" line in README.md to reflect progress
   - Example statuses:
     - `🟡 MVP Phase - Database foundation complete, building file upload system`
     - `🟡 MVP Phase - File intake system complete, implementing agents`
     - `🟢 MVP Complete - Cash Commander demo ready`
     - `🔴 In Development - Refactoring [component]`
   - Keep it concise (under 100 characters) and accurate
   - Update "Last Updated" date in PROGRESS.md if making significant progress

2. **Check Git Status**: Run `git status` to see all changes

3. **Review Changes**: Run `git diff` to see unstaged changes and `git diff --staged` to see staged changes

4. **Review Recent Commits**: Run `git log --online -5` to see recent commit message style

5. **Stage All Changes**: Add all changes using `git add .`

6. **Create Commit Message**:
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
7. **Commit Changes**: Create the commit with the message using HEREDOC format
8. **Push to Remote**: Push the changes to the remote repository with `git push`
9. **Confirm Success**: Run `git status` to verify the push was successful

## Important Notes

- **Always update README.md status** before committing to keep it current
- **Do NOT push force** unless explicitly requested
- **Do NOT skip hooks** (--no-verify)
- **Do NOT amend** unless explicitly requested or adding pre-commit hook edits
- If there are no changes to commit, inform the user
- If push fails due to remote changes, inform the user and suggest pulling first
- Always use HEREDOC format for commit messages to ensure proper formatting
- The README status should be factual and reflect actual progress, not aspirational goals

## Workflow Details

### README Status Update Process

1. **Analyze Progress:**
   - Read PROGRESS.md to see completion percentages
   - Review git status/diff to understand what was built
   - Identify the current phase and milestone

2. **Determine Status Emoji:**
   - 🟢 = Complete/working demo
   - 🟡 = In progress/active development
   - 🔴 = Blocked/refactoring/major issues

3. **Write Status Message:**
   - Format: `[Emoji] [Phase] - [What's complete], [What's next]`
   - Be specific about component names
   - Keep under 100 characters

4. **Update README.md:**
   - Find line 22: `**Current Status:**`
   - Replace with new status
   - Save the file

5. **Optional: Update PROGRESS.md:**
   - If significant milestone reached, update "Last Updated" date
   - Update completion percentages if applicable

### Example Status Updates

**After completing database models:**
```
🟡 MVP Phase - Database foundation complete, building file upload system
```

**After adding file upload and intake:**
```
🟡 MVP Phase - File intake infrastructure complete, implementing agents
```

**After completing Cash Commander:**
```
🟡 MVP Phase - Cash Commander agent working, building orchestration layer
```

**After MVP demo ready:**
```
🟢 MVP Complete - Cash Commander demo ready, starting full build
```

## Example Commit Message Format

```bash
git commit -m "$(cat <<'EOF'
Add custom ship command for streamlined git workflow

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```
