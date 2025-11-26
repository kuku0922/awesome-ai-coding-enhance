---
description: Quick git branch creation with one-time question collection and AI translation. Simple pattern for fast branch operations with essential validation and bilingual support.
allowed-tools: Read(**), Bash(git status, git branch, git checkout, git push, git pull, git fetch, git log, git rev-parse, git remote, git check-ref-format)
argument-hint: [--name <branch-name>] [--base <branch>] [--push] [--no-translate]
# examples:
#   - /git-branch                                        # Interactive mode with all questions
#   - /git-branch --name "feature/user-auth"             # Direct creation with validation
#   - /git-branch --name "用户认证" --base main --translate  # Chinese input with translation
#   - /git-branch --name "hotfix/login" --base main --push  # Create and push immediately
---

# Claude Command: Quick Git Branch Creation

🚀 **Simple & Fast**: Create Git branches quickly with **one-time question collection**, **AI-powered translation**, and **essential validation**. Perfect for daily development workflow.

---

## Usage

```bash
# Interactive Mode (Recommended)
/git-branch                                        # Ask all questions at once

# Direct Mode with Parameters
/git-branch --name "feature/user-auth"             # Skip name input
/git-branch --name "用户认证" --translate            # Chinese input with AI translation
/git-branch --name "hotfix/bug-fix" --base main --push  # Full parameters

# Quick Creation
/git-branch --name "docs/readme-update" --push     # Create and push in one go
```

### Options

| Option | Description |
|--------|-------------|
| `--name <branch-name>` | Pre-specify branch name (skips name prompt) |
| `--base <branch>` | Pre-specify base branch (skips branch selection) |
| `--push` | Automatically push to remote after creation |
| `--no-translate` | Disable AI translation for Chinese input |

---

## 🔄 Simple Pattern Workflow

### **Context → Task**

**Step 1: Context Gathering** (One-time collection)
```bash
📋 Branch Creation Questions:
┌─────────────────────────────────────────┐
│  Branch Name: [________________________] │
│  Base Branch: [develop ▼]               │
│  Push to Remote: [Yes ▼]                │
│  Chinese Input: [Auto-translate ▼]     │
└─────────────────────────────────────────┘
```

**Step 2: Task Execution** (Single operation)
```bash
✅ Validation: Branch name available
✅ Translation: 用户认证 → feature/user-authentication
✅ Creation: git checkout -b feature/user-authentication
✅ Push: git push -u origin feature/user-authentication
```

---

## 🌐 AI Translation Features

### **Auto-Detection**
- **Chinese Input Detected**: Automatically enables translation
- **Context-Aware**: Translates based on development context
- **Multiple Options**: Provides several translation choices

### **Translation Examples**
```bash
用户登录系统     → feature/user-login-system, feat/user-auth
支付功能开发     → feature/payment-system, feat/payment-gateway
页面修复        → fix/page-layout, hotfix/ui-issue
文档更新        → docs/api-documentation, docs/update-readme
代码重构        → refactor/code-optimization, refactor/improve-structure
```

### **Translation Selection**
```bash
📋 Translation Options for "用户认证功能":
┌─────────────────────────────────────────┐
│  ● feature/user-authentication         │
│  ○ feat/user-auth                      │
│  ○ user-auth-system                    │
│  ○ Custom: [________________________]  │
└─────────────────────────────────────────┘
```

---

## ⚡ Quick Creation Patterns

### **Feature Development**
```bash
/git-branch --name "feature/user-profile" --base develop --push
```
- Creates feature branch from develop
- Automatically pushes to remote
- Sets up tracking branch

### **Bug Fixes**
```bash
/git-branch --name "fix/login-validation" --base main
```
- Creates fix branch from main
- Local only (no push by default for fixes)
- Ready for immediate development

### **Documentation**
```bash
/git-branch --name "docs/api-guide" --no-translate
```
- Creates documentation branch
- Skips translation for English input
- Perfect for doc updates

### **Hotfixes**
```bash
/git-branch --name "hotfix/critical-bug" --base main --push
```
- Creates hotfix from production branch
- Immediate push for team coordination
- Critical issue resolution

---

## ✅ Validation & Safety

### **Branch Name Validation**
- ✅ **Git Compliance**: Follows Git branch naming rules
- ✅ **Character Check**: Allows alphanumerics, hyphens, slashes, underscores
- ✅ **Conflict Detection**: Checks existing local and remote branches
- ✅ **Reserved Names**: Prevents use of HEAD, master, main conflicts

### **Repository State Check**
- ✅ **Git Repository**: Verifies we're in a Git repository
- ✅ **Remote Access**: Checks remote connectivity (if pushing)
- ✅ **Clean State**: Warns about uncommitted changes
- ✅ **Branch Sync**: Updates remote information

### **Base Branch Validation**
- ✅ **Existence**: Verifies base branch exists locally/remotely
- ✅ **Protected Warnings**: Alerts for main/master/production branches
- ✅ **Remote Sync**: Ensures remote is up-to-date before branching

---

## 🎯 Best Practices

### **Branch Naming**
- **Use kebab-case**: `feature/user-auth`, not `feature/userAuth`
- **Be descriptive**: `fix/payment-timeout`, not `fix/payment-bug`
- **Use prefixes**: `feature/`, `fix/`, `docs/`, `hotfix/`, `refactor/`

### **When to Push**
```bash
# ✅ Push immediately for:
- Feature branches (team collaboration)
- Hotfixes (urgent coordination)
- Shared development branches

# ❌ Don't push for:
- Local experiments
- Personal drafts
- Temporary debugging branches
```

### **Translation Tips**
- **Review AI suggestions**: Always check translation accuracy
- **Use custom when needed**: Don't hesitate to use your own translation
- **Team consistency**: Match existing branch naming patterns

---

## 🚨 Error Handling

### **Common Issues & Solutions**

#### **Branch Name Exists**
```bash
❌ Branch 'feature/user-auth' already exists
Options: [Switch to Existing] [Create with Suffix] [Choose New Name]
```

#### **Invalid Branch Name**
```bash
❌ Invalid branch name 'user auth!'
Issues: Contains spaces
Suggestion: 'user-auth' or 'user_auth'
```

#### **Remote Connection Failed**
```bash
❌ Cannot reach remote 'origin'
Options: [Create Local Only] [Retry Connection] [Cancel]
```

#### **Uncommitted Changes**
```bash
⚠️  You have uncommitted changes
Options: [Stash Changes] [Commit Changes] [Continue Anyway]
```

---

## 📊 Quick Reference

### **Command Matrix**

| Scenario | Command | Result |
|----------|---------|--------|
| **Quick Feature** | `/git-branch --name "feature/new-ui" --push` | Feature branch + push |
| **Chinese Input** | `/git-branch --name "支付功能" --translate` | Translated feature branch |
| **Bug Fix** | `/git-branch --name "fix/login-bug" --base main` | Fix branch from main |
| **Documentation** | `/git-branch --name "docs/readme"` | Documentation branch |
| **Hotfix** | `/git-branch --name "hotfix/critical" --base main --push` | Urgent fix + push |

### **Translation Quick Guide**

| Chinese | English Options | Recommended |
|---------|----------------|-------------|
| 用户登录 | feature/user-login, feat/user-auth | `feature/user-login` |
| 支付功能 | feature/payment, feat/payment-gateway | `feature/payment-system` |
| 页面修复 | fix/page, hotfix/ui-issue | `fix/page-layout` |
| 文档更新 | docs/update, docs/documentation | `docs/api-documentation` |
| 性能优化 | refactor/performance, perf/improvement | `perf/speed-optimization` |

---

## 🔧 Technical Implementation

### **Git Commands Used**
```bash
# Repository validation
git rev-parse --is-inside-work-tree
git remote -v

# Branch operations
git branch --list <name>
git checkout -b <new-branch> <base-branch>
git push -u origin <branch>

# Remote sync
git fetch --all --prune
git log --oneline -5 <base-branch>
```

### **Safety Checks**
- **Pre-flight validation** before any Git operations
- **Rollback capability** if creation fails
- **State preservation** - working directory unchanged
- **Atomic operations** - either succeeds completely or fails safely

---

## 🚀 Implementation

Let me create a new Git branch for you! I'll collect all the information needed upfront and then execute the branch creation.

# Step 1: Collect Branch Information

Please provide the following information for branch creation:

**Branch Name**: [Enter your desired branch name]
**Base Branch**: [Current branch will be used as default]
**Push to Remote**: [Yes/No - whether to push to remote after creation]
**Translation Option**: [Auto-translate Chinese names or keep as-is]

# Step 2: AI Translation (if needed)

If Chinese characters are detected in your branch name, I'll provide intelligent translation options:

## Chinese Character Detection
I'll automatically detect Chinese characters in your input using pattern matching:
```javascript
// Detection logic
const hasChinese = /[\u4e00-\u9fff]/.test(branchName);
```

## Translation Process
1. **Analyze Context**: Determine if it's a feature, fix, documentation, etc.
2. **Generate Options**: Create multiple translation variations
3. **Present Choices**: Show recommended and alternative translations
4. **Custom Option**: Allow user to provide their own translation

## Translation Examples
**Original**: "用户认证功能"
**Translation Options**:
1. `feature/user-authentication` *(Recommended - feature-specific)*
2. `feat/user-auth` *(Simplified - conventional commit style)*
3. `user-auth-system` *(Generic - clear and simple)*
4. `custom: [________________________]` *(Your own translation)*

**Common Translation Patterns**:
- 用户登录 → `feature/user-login`, `feat/login-system`
- 支付功能 → `feature/payment`, `feat/payment-gateway`
- 页面修复 → `fix/page-layout`, `hotfix/ui-issue`
- 文档更新 → `docs/update`, `docs/documentation`
- 性能优化 → `refactor/performance`, `perf/speed-optimization`

# Step 3: Safety Validation

Before creating the branch, I'll perform comprehensive safety checks:

## Repository State Validation
```bash
# Git repository verification
git rev-parse --is-inside-work-tree

# Remote connectivity (if pushing)
git remote -v
git ls-remote origin
```

## Branch Name Validation
```bash
# Check for existing local branches
git branch --list <branch-name>

# Check for existing remote branches
git branch -r --list origin/<branch-name>

# Validate branch name format
git check-ref-format --branch <branch-name>
```

## Base Branch Verification
```bash
# Verify base branch exists
git rev-parse --verify <base-branch>

# Check if base branch is up-to-date with remote
git fetch origin <base-branch>
git log HEAD..origin/<base-branch> --oneline
```

## Working Directory Analysis
```bash
# Check for uncommitted changes
git status --porcelain

# Check for staged changes
git diff --cached --name-only

# Warn about dirty working directory
```

## Pre-Creation Safety Checklist
- ✅ **Git Repository**: Confirmed we're in a valid Git repository
- ✅ **Remote Access**: Verified connectivity to remote (if pushing)
- ✅ **Branch Name**: Confirmed no naming conflicts
- ✅ **Base Branch**: Verified target branch exists
- ✅ **Clean State**: Warned about uncommitted changes
- ✅ **Permissions**: Confirmed write access to repository

## Error Recovery Strategies
- **Branch Exists**: Offer to switch to existing branch or create with suffix
- **Remote Offline**: Create local branch only, offer retry for push
- **Dirty Working Directory**: Offer to stash changes or continue anyway
- **Invalid Base**: Suggest alternative base branches from available options

# Step 4: Branch Creation

Once all information is collected and validated, I'll execute:
```bash
git checkout -b <your-branch-name> <base-branch>
git push -u origin <your-branch-name>  # if push requested
```

---

This command provides a fast, reliable way to create Git branches with intelligent translation and essential safety features, following the Simple Pattern for maximum efficiency in daily development workflows.