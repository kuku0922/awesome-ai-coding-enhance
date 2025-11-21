---
description: Auto-generate git commits with three message options: concise (recommended), detailed, or minimalist. Analyzes changes and creates conventional commits with optional emoji and smart split suggestions.
allowed-tools: Read(**), Exec(git status, git diff, git add, git restore --staged, git commit, git rev-parse, git config), Write(.git/COMMIT_EDITMSG)
argument-hint: [--no-verify] [--all] [--amend] [--signoff] [--emoji] [--scope <scope>] [--type <type>] [--auto-select <concise|detailed|minimalist>]
# examples:
#   - /git-commit                           # Analyze changes, show three message options
#   - /git-commit --all                     # Stage all changes and show options
#   - /git-commit --auto-select concise     # Auto-select concise version
#   - /git-commit --auto-select minimalist  # Auto-select one-line summary
#   - /git-commit --emoji                   # Include emoji in all message options
#   - /git-commit --scope ui --type feat    # Pre-define scope and type
#   - /git-commit --amend --signoff         # Amend last commit with new options
---

# Claude Command: Smart Git Commit with Message Options

This command works **without any package manager/build tools**, using only **Git** to automatically analyze changes and generate optimized commit messages with **three distinct options**:

## 🎯 Three Commit Message Options

1. **Concise Version** (Recommended) 🌟
   - Brief, clear summary of changes
   - Includes essential context and motivation
   - Perfect for daily development workflow

2. **Detailed Version** 📋
   - Comprehensive technical description
   - Includes implementation details and rationale
   - Ideal for complex features or critical fixes

3. **Minimalist Version** ⚡
   - Single-line summary for quick submission
   - Perfect for routine changes or hotfixes
   - Maintains clarity while maximizing speed

The command will:
- Read changes (staged/unstaged)
- Determine if changes should be **split into multiple commits**
- Generate all three message options for user selection
- Support auto-selection with `--auto-select` flag
- Execute `git add` and `git commit` as needed (runs local Git hooks by default; use `--no-verify` to skip)

---

## Usage

```bash
# Interactive mode - shows all three options
/git-commit
/git-commit --all                     # Stage all changes first
/git-commit --emoji                   # Include emoji in all options
/git-commit --no-verify               # Skip Git hooks

# Auto-selection modes
/git-commit --auto-select concise     # Auto-select concise version
/git-commit --auto-select detailed    # Auto-select detailed version
/git-commit --auto-select minimalist  # Auto-select one-line summary

# Advanced options
/git-commit --scope ui --type feat --emoji
/git-commit --amend --signoff
```

### Options

#### Core Options
- `--auto-select <type>`: Automatically select a message type without prompting
  - `concise`: Brief, clear summary (recommended)
  - `detailed`: Comprehensive technical description
  - `minimalist`: Single-line summary for speed
- `--no-verify`: Skip local Git hooks (`pre-commit`/`commit-msg` etc.).
- `--all`: When staging area is empty, automatically `git add -A` to include all changes.
- `--amend`: Amend the last commit without creating a new one.
- `--signoff`: Add `Signed-off-by` line (use when following DCO process).
- `--emoji`: Include emoji prefix in commit message (applies to all three options).
- `--scope <scope>`: Specify commit scope (e.g., `ui`, `docs`, `api`).
- `--type <type>`: Force commit type (e.g., `feat`, `fix`, `docs`).

#### Message Option Behavior
- **Interactive Mode** (default): Presents all three options with clear formatting for user selection
- **Auto-Select Mode**: Skips interaction and uses the specified message type immediately
- **Fallback**: If auto-selection fails, falls back to interactive mode

> Note: If the framework doesn't support interactive confirmation, enable `confirm: true` in front-matter to avoid mistakes.

---

## What This Command Does

1. **Repository/Branch Validation**
   - Check if in a Git repository using `git rev-parse --is-inside-work-tree`.
   - Read current branch/HEAD status; if in rebase/merge conflict state, prompt to resolve conflicts first.

2. **Change Detection**
   - Get staged and unstaged changes using `git status --porcelain` and `git diff`.
   - If staged files = 0:
     - If `--all` is passed → Execute `git add -A`.
     - Otherwise prompt choice: continue analyzing unstaged changes for **suggestions**, or cancel to manually group staging.

3. **Split Suggestions (Split Heuristics)**
   - Cluster by **concerns**, **file modes**, **change types** (e.g., source code vs docs/tests; different directories/packages; additions vs deletions).
   - If **multiple independent changesets** or large diff detected (e.g., > 300 lines / across multiple top-level directories), suggest splitting commits with pathspecs for each group (for subsequent `git add <paths>`).

4. **Three-Tier Message Generation** 🎯
   - Auto-infer `type` (`feat`/`fix`/`docs`/`refactor`/`test`/`chore`/`perf`/`style`/`ci`/`revert`...) and optional `scope`.
   - Generate conventional commit header: `[<emoji>] <type>(<scope>)?: <subject>` (≤ 72 chars, imperative mood).
   - Create **three distinct message options**:

     **Option 1: Concise Version** (Recommended) 🌟
     ```
     <header>

     • Brief motivation (1-2 sentences)
     • Key implementation highlights
     • Impact summary
     ```

     **Option 2: Detailed Version** 📋
     ```
     <header>

     • Comprehensive motivation and context
     • Detailed implementation approach
     • Technical considerations and trade-offs
     • Impact scope and testing notes
     • Future implications or next steps
     • BREAKING CHANGE details (if applicable)
     ```

     **Option 3: Minimalist Version** ⚡
     ```
     <header>
     ```
     (Single line - header only, perfect for quick commits)

   - Present options in interactive mode or auto-select based on `--auto-select` flag
   - Select message language based on Git history (analyze recent commits for Chinese vs English preference)
   - Write selected message to `.git/COMMIT_EDITMSG` for git commit execution

5. **Execute Commit**
   - Single commit scenario: `git commit [-S] [--no-verify] [-s] -F .git/COMMIT_EDITMSG`
   - Multiple commit scenario (if split accepted): Provide clear instructions for `git add <paths> && git commit ...` per group; execute sequentially if allowed.

6. **Safe Rollback**
   - If mistakenly staged, use `git restore --staged <paths>` to unstage (command provides instructions, doesn't modify file contents).

---

## Best Practices for Message Selection

### Choose Based on Context

**Use Concise Version** (Recommended) for:
- Daily development commits
- Feature additions and improvements
- Standard bug fixes
- When you want clarity without verbosity

**Use Detailed Version** for:
- Complex architectural changes
- Critical bug fixes with security implications
- Breaking changes or major refactors
- When documentation is crucial for team understanding

**Use Minimalist Version** for:
- Hotfixes in production
- Minor typo corrections
- Documentation link updates
- When speed is essential and context is obvious

### General Best Practices

- **Atomic commits**: One commit does one thing, easier to trace and review.
- **Group before committing**: Split by directory/module/feature.
- **Clear subject**: First line ≤ 72 chars, imperative mood (e.g., "add... / fix...").
- **Follow Conventional Commits**: `<type>(<scope>): <subject>`.
- **Match your team's style**: Consider what message length your team prefers for code reviews.

---

## Type to Emoji Mapping (When --emoji is Used)

- ✨ `feat`: New feature
- 🐛 `fix`: Bug fix (includes 🔥 remove code/files, 🚑️ hotfix, 👽️ adapt to external API changes, 🔒️ security fix, 🚨 fix warnings, 💚 fix CI)
- 📝 `docs`: Documentation and comments
- 🎨 `style`: Code style/formatting (no semantic changes)
- ♻️ `refactor`: Refactoring (no new features, no bug fixes)
- ⚡️ `perf`: Performance improvements
- ✅ `test`: Add/fix tests, snapshots
- 🔧 `chore`: Build/tools/misc tasks (merge branches, update configs, release tags, pin dependencies, .gitignore, etc.)
- 👷 `ci`: CI/CD configuration and scripts
- ⏪️ `revert`: Revert commits
- 💥 `feat`: Breaking changes (explained in `BREAKING CHANGE:` section)

> If `--type`/`--scope` is passed, it will **override** auto-detection.
> Emoji is only included when `--emoji` flag is specified.

---

## Guidelines for Splitting Commits

1. **Different concerns**: Unrelated feature/module changes should be split.
2. **Different types**: Don't mix `feat`, `fix`, `refactor` in the same commit.
3. **File modes**: Source code vs docs/tests/configs should be grouped separately.
4. **Size threshold**: Large diffs (e.g., >300 lines or across multiple top-level directories) should be split.
5. **Revertability**: Ensure each commit can be independently reverted.

---

## Examples

### Three Message Options for Same Change

**Scenario**: Added user authentication with JWT tokens

**Option 1: Concise Version** (Recommended) 🌟
```
✨ feat(auth): implement JWT-based user authentication

• Add login/register endpoints with JWT token generation
• Integrate authentication middleware for protected routes
• Update user model with password hashing and validation
• Implement token refresh mechanism for session management
```

**Option 2: Detailed Version** 📋
```
✨ feat(auth): implement JWT-based user authentication

• Comprehensive authentication system using JSON Web Tokens
  - Login endpoint with email/password validation
  - User registration with email verification
  - Password hashing using bcrypt with salt rounds

• Security middleware implementation
  - JWT token validation on protected endpoints
  - Role-based access control (admin/user roles)
  - CORS configuration for cross-origin requests

• Session management and security
  - Access tokens (15min expiry) + refresh tokens (7days)
  - Secure token storage with HttpOnly cookies
  - Automatic token refresh on access token expiry

• Database changes and testing
  - Extended User model with auth fields
  - Migration script for existing users
  - Unit tests covering all authentication flows
  - Integration tests for middleware protection
```

**Option 3: Minimalist Version** ⚡
```
✨ feat(auth): implement JWT-based user authentication
```

### Header-Only Examples

**With --emoji**
- ✨ feat(ui): add user authentication flow
- 🐛 fix(api): handle token refresh race condition
- 📝 docs: update API usage examples
- ♻️ refactor(core): extract retry logic into helper
- ✅ test: add unit tests for rate limiter
- 🔧 chore: update git hooks and repository settings
- ⏪️ revert: revert "feat(core): introduce streaming API"

**Without --emoji**
- feat(ui): add user authentication flow
- fix(api): handle token refresh race condition
- docs: update API usage examples
- refactor(core): extract retry logic into helper
- test: add unit tests for rate limiter
- chore: update git hooks and repository settings
- revert: revert "feat(core): introduce streaming API"

### Split Example

For large changes, the command suggests splitting:
- `feat(types): add new type defs for payment method`
- `docs: update API docs for new types`
- `test: add unit tests for payment types`
- `fix: address linter warnings in new files` ← (if your repo has hook errors)

---

## Important Notes

- **Git only**: No package manager/build commands (`pnpm`/`npm`/`yarn` etc.).
- **Respects hooks**: Executes local Git hooks by default; use `--no-verify` to skip.
- **No source code changes**: Command only reads/writes `.git/COMMIT_EDITMSG` and staging area; doesn't directly edit working directory files.
- **Safety prompts**: In rebase/merge conflicts, detached HEAD states, prompts to handle/confirm before continuing.
- **Auditable and controllable**: If `confirm: true` is enabled, each actual `git add`/`git commit` step requires confirmation.
