---
description: Interactive GitHub branch creation with intelligent Chinese-to-English translation, base branch selection, and comprehensive safety validation. Enterprise-grade workflow with bilingual support and multi-tier safety modes.
allowed-tools: Read(**), Exec(git branch, git checkout, git push, git pull, git fetch, git log, git status, git rev-parse, git remote, git check-ref-format), Write(.git/branch-creation-*.log)
argument-hint: [--name <name>] [--base <branch>] [--translate] [--no-push] [--safe] [--dry-run] [--mode quick|standard|comprehensive]
# examples:
#   - /git-branch-create                                    # Full interactive mode with translation and safety
#   - /git-branch-create --name "用户认证" --base main --translate
#   - /git-branch-create --name "feature-payment" --no-push --safe
#   - /git-branch-create --mode comprehensive --dry-run     # Full analysis preview
#   - /git-branch-create --name "hotfix/登录修复" --translate --base main
---

# Claude Command: Enterprise GitHub Branch Creation

🚀 **Production-Ready Branch Creation**: Interactive workflow with **AI-powered translation**, **intelligent base branch selection**, **multi-tier safety validation**, and **comprehensive audit trails**. **Bilingual support** with enterprise-grade error handling and team collaboration features.

---

## 🎯 Core Features

### **1. Interactive Branch Creation**
- **Multi-language Input**: Support for Chinese and English branch names
- **AI-Powered Translation**: Context-aware translation for technical terms
- **Smart Validation**: Real-time branch name validation and conflict detection
- **Intuitive Interface**: Step-by-step guided workflow

### **2. Intelligent Base Branch Selection**
- **Interactive Branch Browser**: Visual branch selection with metadata
- **Protected Branch Warnings**: Safety alerts for production branches
- **Activity Indicators**: Recent commit information and branch health
- **Remote Sync Status**: Automatic remote synchronization check

### **3. Multi-Tier Safety Modes**
- **Quick Mode** ⚡: Essential validations for fast operation
- **Standard Mode** 🎯: Comprehensive validation (default)
- **Comprehensive Mode** 🛡️: Maximum safety with team impact analysis

### **4. Enterprise Safety Features**
- **Repository Validation**: Complete repository state analysis
- **Conflict Detection**: Advanced merge conflict prediction
- **Team Impact Assessment**: Active contributor detection
- **Audit Trail**: Complete operation logging for compliance

---

## Usage

```bash
# Interactive Mode (Recommended)
/git-branch-create                                    # Full interactive workflow
/git-branch-create --translate                        # Enable translation
/git-branch-create --safe                             # Use comprehensive safety

# Direct Mode with Parameters
/git-branch-create --name "用户认证" --base main --translate
/git-branch-create --name "feature/payment" --no-push --safe
/git-branch-create --name "hotfix/修复" --base production --translate

# Mode Selection
/git-branch-create --mode quick                      # Fast mode with essential safety
/git-branch-create --mode comprehensive --dry-run     # Full analysis preview
/git-branch-create --mode standard                   # Balanced safety (default)

# Enterprise Features
/git-branch-create --safe --no-push                  # Local-only creation with full safety
/git-branch-create --dry-run --mode comprehensive    # Preview with full analysis
```

### Options

#### **Core Options**
| Option | Description |
|--------|-------------|
| `--name <name>` | Pre-specify branch name (bypasses interactive input) |
| `--base <branch>` | Pre-specify base branch (bypasses branch selection) |
| `--mode <type>` | Safety mode: `quick`, `standard` (default), `comprehensive` |
| `--translate` | Enable AI translation for Chinese input (auto-enabled when Chinese detected) |

#### **Control Options**
| Option | Description |
|--------|-------------|
| `--no-push` | Create branch locally only, skip remote push |
| `--dry-run` | Preview operations without execution (enabled by default in comprehensive mode) |
| `--safe` | Equivalent to `--mode comprehensive` with additional safety checks |

#### **Advanced Options**
| Option | Description |
|--------|-------------|
| `--audit-log` | Force detailed audit log creation |
| `--template <type>` | Use branch template: `feat`, `fix`, `docs`, `test`, `refactor`, `hotfix` |

---

## 🔄 Interactive Workflow

### **Phase 1: Repository Validation**
```bash
# System Checks
✅ Git Repository: Valid
✅ Remote Access: Connected
✅ Working Directory: Clean
⚠️  Remote Sync: Fetching latest changes...
```

### **Phase 2: Branch Name Input**
```bash
📝 Enter branch name: [用户认证功能开发]
🌐 Language detected: Chinese
🔤 Translation: Enabled
```

### **Phase 3: Translation Selection** (if Chinese input)
```bash
📋 Translation Options for "用户认证功能开发":
┌─────────────────────────────────────────┐
│  ● feature/user-authentication         │
│  ○ feat/user-auth                      │
│  ○ user-auth-system                    │
│  ○ Custom: [________________________]  │
└─────────────────────────────────────────┘
```

### **Phase 4: Base Branch Selection**
```bash
🌿 Select Base Branch:
┌─────────────────────────────────────────┐
│  🛡️  main (Production) - 2 hours ago   │
│  🚀 develop (Development) - 30 min ago  │
│  🧪 staging (Testing) - 1 hour ago     │
│  📝 docs - 3 days ago                  │
└─────────────────────────────────────────┘

⚠️  Warning: Creating from protected branch 'main'
👥 Active contributors: 2 in last 24 hours
```

### **Phase 5: Safety Validation**
```bash
🔒 Safety Analysis Summary:
┌─────────────────────────────────────────┐
│  ✅ Repository State: Clean             │
│  ✅ Branch Name: Available              │
│  ✅ Base Branch: Synced with remote     │
│  ⚠️  Protected Branch: main             │
│  ✅ Team Impact: Low                    │
└─────────────────────────────────────────┘
```

### **Phase 6: Creation Confirmation**
```bash
🚀 Ready to create new branch:
   📁 Branch Name: feature/user-authentication
   🌿 Base Branch: main (Protected)
   🚀 Push to Remote: Yes (ask for confirmation)
   🔒 Safe Mode: Standard

   [Confirm Creation] [Modify] [Cancel]
```

---

## 🛡️ Enterprise Safety Features

### **Multi-Tier Safety Modes**

#### **Quick Mode** ⚡ (Emergency)
- **Use Case**: Fast branch creation for trusted scenarios
- **Features**: Essential validations only, minimal prompts
- **Safety**: Basic repository and name validation
- **Performance**: Optimized for speed

#### **Standard Mode** 🎯 (Default)
- **Use Case**: Daily development workflow
- **Features**: Comprehensive validation with balanced prompts
- **Safety**: Full repository analysis, conflict detection
- **Performance**: Balanced approach

#### **Comprehensive Mode** 🛡️ (Enterprise)
- **Use Case**: Critical operations, team environments
- **Features**: Maximum validation, team impact analysis
- **Safety**: All safety checks, audit trails, team notifications
- **Performance**: Thorough analysis priority

### **Safety Validation Layers**

#### **Repository State Analysis**
```bash
# Pre-flight checks
git rev-parse --is-inside-work-tree          # Git repository validation
git status --porcelain                       # Working directory state
git fetch --all --prune                      # Remote synchronization
git remote -v                                # Remote connectivity
```

#### **Branch Name Validation**
```bash
# Name safety checks
git branch --list <branch-name>              # Existing branch check
git check-ref-format <branch-name>           # Git naming compliance
# Character validation: alphanumeric, /, -, _ only
# Length validation: Git branch name limits
# Reserved name check: HEAD, master, main protections
```

#### **Base Branch Analysis**
```bash
# Branch safety validation
git merge-base HEAD <base-branch>            # Common ancestor check
git log --oneline -10 <base-branch>          # Recent activity analysis
git rev-parse --verify origin/<base-branch>  # Remote branch verification
# Protected branch detection: main, master, production
# Team activity analysis: recent contributors
```

### **Enterprise Security Guards**

#### **🚨 Critical Protection**
- **Protected Branch Warnings**: Multiple confirmations for production branches
- **Team Impact Detection**: Scan for active contributors and conflicts
- **Remote Sync Validation**: Ensure remote connectivity before operations
- **Audit Trail Creation**: Complete operation logging in `.git/branch-creation-*.log`

#### **🔍 Pre-Execution Validation**
- **Repository Health Check**: Verify repository integrity and state
- **Branch Conflict Analysis**: Predict potential merge conflicts
- **Network Connectivity**: Verify remote repository access
- **Permission Validation**: Check branch creation permissions

---

## 🌐 AI-Powered Translation System

### **Translation Categories & Patterns**

#### **Feature Development**
```bash
用户登录系统      → feature/user-login-system, feat/user-auth
支付功能开发      → feature/payment-system, feat/payment-gateway
数据报表功能      → feature/data-reporting, feat/analytics-dashboard
权限管理系统      → feature/permission-system, feat/rbac-system
```

#### **Bug Fixes & Hotfixes**
```bash
登录页面修复      → fix/login-page, hotfix/auth-bug
支付接口问题      → fix/payment-api, hotfix/payment-gateway
性能优化问题      → fix/performance-issue, hotfix/slow-loading
数据导出错误      → fix/data-export, hotfix/export-bug
```

#### **Documentation & Testing**
```bash
API文档更新      → docs/api-documentation, docs/update-api
测试用例补充      → test/unit-tests, test/integration-tests
用户手册编写      → docs/user-guide, docs/manual
代码注释完善      → docs/code-comments, refactor/improve-comments
```

#### **Refactoring & Optimization**
```bash
代码重构优化      → refactor/code-optimization, refactor/improve-structure
数据库设计改进    → refactor/database-schema, refactor/db-design
配置文件整理      → refactor/configuration, refactor/config-management
依赖包升级        → refactor/dependency-update, chore/update-dependencies
```

### **Translation Intelligence Features**

#### **Context-Aware Translation**
- **Technical Term Recognition**: Identify development-specific terminology
- **Project Context Analysis**: Consider existing branch patterns in repository
- **Semantic Preservation**: Maintain meaning while following conventions
- **Multiple Options**: Provide several translation choices for user selection

#### **Pattern Learning**
- **Repository Pattern Analysis**: Learn from existing branch naming conventions
- **Team Preference Memory**: Remember translation choices for consistency
- **Industry Standard Alignment**: Follow GitFlow and common branching strategies
- **Custom Dictionary Support**: Support for project-specific terminology

---

## ⚙️ Advanced Features

### **Intelligent Branch Suggestions**

#### **Based on Current Changes**
```bash
# Analyze git status for intelligent suggestions
📁 Based on your changes, suggest:
   • feature/user-authentication (Modified: auth/, login/, user/)
   • fix/payment-validation (Fixed: payment/, validation/)
   • docs/api-endpoints (Added: api/, docs/)
```

#### **Team Pattern Recognition**
```bash
🕐 Recent branch patterns in your repository:
   • feature/ (Used 12 times, last: 2 days ago)
   • fix/ (Used 8 times, last: 5 hours ago)
   • hotfix/ (Used 3 times, last: 1 day ago)
   • docs/ (Used 5 times, last: 3 days ago)
```

### **Template System**
```bash
# Predefined branch templates
[feat] New Feature:     feature/<description>
[fix] Bug Fix:         fix/<description>
[docs] Documentation:  docs/<description>
[test] Testing:         test/<description>
[refactor] Code Improvement: refactor/<description>
[hotfix] Production Fix: hotfix/<description>
[chore] Maintenance:   chore/<description>
```

### **Audit Trail & Logging**
```bash
# Automatic audit log creation
.git/branch-creation-2025-01-26-14-30.log

# Log contents
[2025-01-26 14:30:15] Branch creation initiated
[2025-01-26 14:30:20] Repository validation: PASSED
[2025-01-26 14:30:25] Branch name: feature/user-authentication
[2025-01-26 14:30:30] Base branch: main
[2025-01-26 14:30:35] Safety checks: PASSED
[2025-01-26 14:30:40] Branch created: SUCCESS
[2025-01-26 14:30:45] Remote push: SUCCESS
```

---

## 🚨 Error Handling & Recovery

### **Comprehensive Error Categories**

#### **Repository State Errors**
```bash
❌ Not in a Git repository
   Solution: Initialize with 'git init' or navigate to a Git repository

❌ Detached HEAD state detected
   Solution: Checkout a branch first or create from current commit

❌ Uncommitted changes present
   Options: [Stash Changes] [Commit Changes] [Continue Anyway] [Cancel]
```

#### **Branch Naming Errors**
```bash
❌ Invalid branch name 'user auth!'
   Issues: Contains spaces, contains special character '!'
   Suggestion: 'user-auth' or 'user_auth'
   Options: [Use Suggestion] [Enter New Name] [Cancel]

❌ Branch 'feature/user-auth' already exists
   Location: Local and Remote
   Last updated: 2 hours ago
   Options: [Switch to Existing] [Create with Suffix] [Choose New Name]
```

#### **Network & Remote Errors**
```bash
❌ Cannot reach remote 'origin'
   Issue: Network connection failed
   Options: [Create Local Only] [Retry Connection] [Cancel]

❌ Authentication failed for remote
   Issue: Invalid credentials or permissions
   Solution: Check SSH keys or access tokens
```

#### **Permission & Access Errors**
```bash
❌ Cannot create branch on protected 'main'
   Issue: Branch protection rules active
   Solution: Create feature branch instead

❌ Insufficient permissions for remote operations
   Issue: Repository access restrictions
   Solution: Contact repository administrator
```

### **Recovery Strategies**

#### **Automatic Recovery**
- **Smart Retry**: Automatic retry with exponential backoff
- **Graceful Degradation**: Fallback to local-only operation when remote unavailable
- **State Restoration**: Automatic cleanup on failed operations

#### **Manual Recovery Options**
- **Suggested Fixes**: Context-aware fix suggestions
- **Alternative Workflows**: Alternative approaches to achieve goals
- **Rollback Capabilities**: Safe rollback of partial operations

---

## 📊 Enterprise Integration Features

### **Team Collaboration**
```bash
👥 Team Impact Assessment:
   • Active contributors: 3 (last 24 hours)
   • Recent branches: 5 (last 48 hours)
   • Merge conflicts: 0 detected

📢 Notification Suggestions:
   • Slack: #development-changes
   • Email: team@company.com
   • Project Board: Update with new branch
```

### **CI/CD Integration**
```bash
🚦 Pipeline Status Check:
   • Build Status: ✅ Passing
   • Deploy Status: ✅ Ready
   • Tests: ✅ All green

⚠️  Warnings:
   • Branch protection: main requires PR review
   • Required checks: 2/2 passing
```

### **Compliance & Auditing**
```bash
📋 Compliance Features:
   • Audit Trail: Complete operation logging
   • Change Tracking: Branch creation reason documentation
   • Approval Workflow: Optional approval requirement
   • Retention Policy: Configurable log retention

🔒 Security Features:
   • Access Control: Role-based permissions
   • Sensitive Data: No sensitive data in logs
   • Encryption: Secure log storage
```

---

## 🎯 Best Practices

### **Branch Naming Conventions**
- **Use kebab-case**: `feature/user-authentication`, not `feature/userAuthentication`
- **Be descriptive**: `fix/payment-gateway-timeout`, not `fix/payment-bug`
- **Include scope**: `feat(api/user-endpoints)`, not `feat/api`
- **Use prefixes**: Consistent use of `feature/`, `fix/`, `docs/`, etc.

### **When to Use Different Modes**

#### **Quick Mode** ⚡
- Trusted development environments
- Local feature branches
- Emergency branch creation
- When you know exactly what you're doing

#### **Standard Mode** 🎯 (Recommended)
- Daily development workflow
- Team collaboration scenarios
- Feature branch creation
- Most common use cases

#### **Comprehensive Mode** 🛡️
- Production branch operations
- Critical system changes
- Team-wide impact scenarios
- Compliance requirements

### **Translation Best Practices**
- **Review Translations**: Always review AI-generated translations
- **Team Consistency**: Use consistent terminology across branches
- **Context Matters**: Consider the specific technical context
- **Custom Override**: Don't hesitate to use custom translations

---

## 📖 Important Notes

### **System Requirements**
- **Git Version**: 2.20+ for full feature support
- **Repository**: Must be a valid Git repository
- **Permissions**: Write access to repository for branch creation
- **Network**: Internet connection for remote operations (optional for local-only)

### **Limitations**
- **No GitHub CLI**: Uses standard Git commands only (as requested)
- **Translation Quality**: AI translation quality may vary with context
- **Remote Dependencies**: Remote operations require network access
- **Branch Protection**: Cannot override repository protection rules

### **Performance Considerations**
- **Large Repositories**: May take longer for initial analysis
- **Network Latency**: Remote operations affected by network speed
- **Translation Processing**: AI translation adds minimal processing time
- **Log File Size**: Audit logs grow with usage, implement rotation

---

## 🔧 Troubleshooting

### **Common Issues & Solutions**

#### **Translation Not Working**
```bash
Issue: Translation not triggered for Chinese input
Solution: Ensure --translate flag or enable auto-detection
Check: Verify Chinese characters are properly encoded
```

#### **Branch Creation Fails**
```bash
Issue: Branch creation fails with permission error
Solution: Check repository write permissions
Alternative: Use --no-push for local-only creation
```

#### **Remote Sync Issues**
```bash
Issue: Remote synchronization timeout
Solution: Check network connectivity
Alternative: Continue with local branch, push later
```

#### **Safety Mode Too Strict**
```bash
Issue: Comprehensive mode too slow for daily use
Solution: Use --mode standard or --mode quick
Customization: Adjust validation levels in workflow
```

### **Debug Mode**
```bash
# Enable verbose logging
/git-branch-create --debug --mode comprehensive

# Check specific validation steps
/git-branch-create --dry-run --verbose --debug
```

---

This command provides a production-ready, enterprise-grade solution for GitHub branch creation with advanced features including AI-powered translation, comprehensive safety validation, and seamless integration with existing Git workflows.