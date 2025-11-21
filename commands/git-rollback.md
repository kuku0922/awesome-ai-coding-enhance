---
description: Enterprise-grade Git rollback with multi-tier safety modes, collaborative impact warnings, and comprehensive audit trails. Supports Quick, Safe Preview, Comprehensive Analysis, and Standard rollback modes with automatic backup creation.
allowed-tools: Read(**), Exec(git fetch, git branch, git tag, git log, git reflog, git checkout, git reset, git revert, git switch), Write(.git/rollback-*.log)
argument-hint: [--branch <branch>] [--target <rev>] [--mode quick|safe-preview|comprehensive|standard] [--depth <n>] [--dry-run] [--yes] [--backup] [--team-notify]
# examples:
#   - /git-rollback                              # Interactive mode with all options
#   - /git-rollback --mode quick                 # Emergency rollback with minimal prompts
#   - /git-rollback --mode safe-preview          # Visual diff preview before action
#   - /git-rollback --branch dev --target v1.2.0 --mode comprehensive --yes
#   - /git-rollback --backup --team-notify       # Create backup and notify team
---

# Claude Command: Enterprise Git Rollback with Multi-Tier Safety

🚨 **Production-Ready Safety**: Comprehensive rollback system with **four distinct safety modes**, automatic backup creation, collaborative impact warnings, and complete audit trails. **Dry-run enabled by default** for maximum safety.

---

## 🎯 Four-Tier Rollback Safety Modes

### 1. **Quick Rollback** ⚡ (Emergency Mode)
- **Use Case**: Production hotfixes, critical security issues
- **Features**: Minimal prompts, automatic backup, fast execution
- **Safety**: Essential checks only, designed for speed
- **Best For**: When time is critical and you know exactly what to rollback

### 2. **Safe Preview** 🔍 (Visual Mode)
- **Use Case**: Regular development, uncertain impact scope
- **Features**: Color-coded diff display, file change summary, impact visualization
- **Safety**: Comprehensive preview with visual confirmation
- **Best For**: When you need to see exactly what will change

### 3. **Comprehensive Analysis** 📋 (Detailed Mode)
- **Use Case**: Critical branches, complex rollbacks, team environments
- **Features**: Collaborative impact detection, CI/CD status check, dependency analysis
- **Safety**: Maximum validation with enterprise-grade warnings
- **Best For**: When rollback could affect team members or dependent systems

### 4. **Standard Mode** 🎯 (Balanced Mode)
- **Use Case**: Daily development workflow
- **Features**: Interactive selection with essential safety checks
- **Safety**: Balanced approach between speed and thoroughness
- **Best For**: Most rollback scenarios (default behavior)

---

## Usage

```bash
# Interactive mode with mode selection
/git-rollback                                    # Full interactive: select mode, branch, target, action

# Four-Tier Mode Selection
/git-rollback --mode quick                      # Emergency rollback with minimal prompts
/git-rollback --mode safe-preview               # Visual diff preview before action
/git-rollback --mode comprehensive              # Full analysis with team impact warnings
/git-rollback --mode standard                   # Balanced interactive mode (default)

# Branch and Target Specification
/git-rollback --branch feature/calculator       # Specify branch, interactive for rest
/git-rollback --target v1.2.0                   # Specify target, interactive for branch/mode

# Advanced Combinations
/git-rollback --branch main --target 1a2b3c4d --mode quick --yes --backup
/git-rollback --branch release/v2.1 --target v2.0.5 --mode comprehensive --team-notify
/git-rollback --mode safe-preview --depth 50    # Extended history with visual preview

# Enterprise Features
/git-rollback --backup --team-notify            # Create backup and suggest team notification
/git-rollback --mode comprehensive --yes        # Full analysis with auto-confirmation
```

### Quick Reference by Scenario

| Scenario | Recommended Command | Reason |
|----------|-------------------|--------|
| **🚨 Production Hotfix** | `/git-rollback --mode quick --branch main --target v1.2.1 --yes --backup` | Emergency speed with safety |
| **🔍 Development Review** | `/git-rollback --mode safe-preview --branch dev` | Visual confirmation needed |
| **👥 Team Branch** | `/git-rollback --mode comprehensive --branch feature --team-notify` | Team impact analysis |
| **⚡ Routine Fix** | `/git-rollback --mode standard` | Balanced approach |
| **📋 Critical System** | `/git-rollback --mode comprehensive --backup --yes` | Maximum safety + audit trail |

### Options

#### **Core Options**
| Option | Description |
|--------|-------------|
| `--branch <branch>` | Branch to rollback; interactively selected if omitted |
| `--target <rev>` | Target version (commit hash, tag, reflog); interactive selection if omitted |
| `--mode <type>` | **Four safety modes**: `quick`, `safe-preview`, `comprehensive`, `standard` (default) |
| `--depth <n>` | List recent n versions (default 20; higher for comprehensive analysis) |
| `--dry-run` | **Enabled by default** - preview only, no execution |

#### **Enterprise Features**
| Option | Description |
|--------|-------------|
| `--backup` | **Always create backup branch** before rollback with timestamp |
| `--team-notify` | Generate team notification template and check for active contributors |
| `--audit-log` | Create detailed rollback audit log in `.git/rollback-*.log` |
| `--ci-check` | Verify CI/CD pipeline status before rollback (comprehensive mode default) |

#### **Execution Control**
| Option | Description |
|--------|-------------|
| `--yes` | Skip confirmations and execute directly (use with caution) |
| `--action reset\|revert` | Override action: `reset` (destructive) vs `revert` (non-destructive) |
| `--force-backup` | Force backup creation even in quick mode |

#### **Advanced Options**
| Option | Description |
|--------|-------------|
| `--exclude <paths>` | Exclude specific paths from rollback (expert mode) |
| `--verify-after` | Run verification checks after successful rollback |
| `--template <name>` | Use predefined rollback template (hotfix, feature-revert, etc.) |

---

## 🔄 Enhanced Interactive Flow

### **Phase 1: Mode Selection** (New)
```
🎯 Select Rollback Mode:
┌─────────────────────────────────────────────────────────────┐
│  ⚡ Quick          - Emergency rollback (minimal prompts)    │
│  🔍 Safe Preview   - Visual diff before action               │
│  📋 Comprehensive - Full analysis + team impact warnings    │
│  🎯 Standard       - Balanced interactive mode (default)     │
└─────────────────────────────────────────────────────────────┘
```

### **Phase 2: Repository Analysis** (Enhanced)
1. **Remote Sync** → `git fetch --all --prune`
2. **Branch Discovery** → Enhanced listing with:
   - 🛡️ **Protected branch detection** (main/master/production)
   - 👥 **Active contributor analysis** (recent commits/branches)
   - 🚦 **CI/CD status integration** (pipeline checks in comprehensive mode)
3. **Smart Target Selection** → Interactive with:
   - **Recent commits** (git log --oneline)
   - **Available tags** (git tag --merged)
   - **Reflog entries** (git reflog)
   - **Frequent rollback points** (history-based suggestions)

### **Phase 3: Safety & Impact Analysis** (New)
```
🔒 Safety Analysis Summary:
┌─────────────────────────────────────────────┐
│  📁 Files Changed: 23 (875 lines)           │
│  👥 Active Contributors: 3                  │
│  🚦 CI/CD Status: ⚠️ Pipeline Running       │
│  🏷️  Tags Involved: v2.1.0, v2.1.1         │
│  🔗 Submodules: 2 affected                 │
└─────────────────────────────────────────────┘
```

### **Phase 4: Preview & Confirmation** (Enhanced)
- **Quick Mode**: Essential preview + backup confirmation
- **Safe Preview**: Visual diff with color-coded changes
- **Comprehensive**: Full impact analysis + team warnings
- **Standard**: Balanced preview with key highlights

### **Phase 5: Backup Creation** (Automatic in most modes)
```bash
# Automatic backup branch naming
git branch backup/feature-auth-2025-01-21-14-30-$(git rev-parse --short HEAD)
```

### **Phase 6: Execution** (Enhanced)
```bash
# Action Selection (prompt/auto):
reset  → git switch <branch> && git reset --hard <target>
revert → git switch <branch> && git revert --no-edit <target>..HEAD
```

### **Phase 7: Post-Rollback Actions** (New)
- **Verification checks** (build/test status)
- **Push recommendations** (force-with-lease vs regular)
- **Team notification templates** (Slack/Teams/Email)
- **Audit log creation** (.git/rollback-*.log)

### **Mode-Specific Workflows**

#### **Quick Mode Flow**
`Mode → Branch → Target → Backup Confirmation → Execute → Push Tip`

#### **Safe Preview Flow**
`Mode → Branch → Target → Visual Diff → Confirm → Execute → Verify`

#### **Comprehensive Flow**
`Mode → Branch → Target → Impact Analysis → Team Warnings → Backup → Execute → Audit → Notify`

#### **Standard Flow**
`Mode → Branch → Target → Basic Preview → Confirm → Execute → Summary`

---

## 🛡️ Enterprise Safety Guards

### **🚨 Critical Protection Layers**
- **🔒 Automatic Backup Creation**: Every rollback creates timestamped backup branch
- **🛡️ Protected Branch Warnings**: Extra confirmation for `main`/`master`/`production` branches
- **👥 Collaborative Impact Detection**: Scans for active contributors and warns about potential conflicts
- **🚦 CI/CD Integration Checks**: Prevents rollbacks during active pipeline executions (comprehensive mode)

### **🔍 Pre-Execution Validation**
- **📂 Repository State Analysis**: Detects uncommitted changes, merge conflicts, rebase states
- **🔗 Submodule/LFS Verification**: Ensures complex repository integrity before rollback
- **🏷️ Tag Dependency Checking**: Analyzes tag relationships and release dependencies
- **⚡ Remote Sync Validation**: Confirms remote status before destructive operations

### **🎯 Mode-Specific Safeguards**

#### **Quick Mode Safeguards**
- ✅ Essential backup creation (forced)
- ✅ Basic protected branch warnings
- ✅ Uncommitted changes detection
- ❌ Skip comprehensive analysis (for speed)

#### **Safe Preview Safeguards**
- ✅ Visual diff confirmation required
- ✅ File change impact summary
- ✅ Backup creation with detailed naming
- ✅ Collaborative conflict warnings

#### **Comprehensive Mode Safeguards**
- ✅ Full repository analysis
- ✅ Team impact assessment
- ✅ CI/CD pipeline status check
- ✅ Dependency relationship validation
- ✅ Audit trail generation
- ✅ Rollback reason logging

#### **Standard Mode Safeguards**
- ✅ Balanced protection set
- ✅ Essential warnings and confirmations
- ✅ Backup creation (recommended)
- ✅ Clear execution preview

### **🔄 Recovery Mechanisms**
- **📋 Audit Trail**: Detailed rollback logs stored in `.git/rollback-*.log`
- **🔙 One-Click Recovery**: Automated commands to restore from backup branches
- **📊 Impact Reports**: Post-rollback verification and impact analysis
- **🧪 Rollback Testing**: Automated verification after successful rollback

### **⚠️ Explicit Safety Requirements**
- **--dry-run enabled by default**: All operations previewed before execution
- **No --force allowed**: Requires manual `git push --force-with-lease` for transparency
- **Protected branch escalation**: Multiple confirmation layers for critical branches
- **Team notification prompts**: Suggests communication when team impact detected

---

## 📚 Real-World Use Case Examples

### **🚨 Production Emergency Scenarios**

#### Critical Hotfix Rollback (Quick Mode)
```bash
# Situation: Bug discovered in production, immediate rollback required
/git-rollback --mode quick --branch main --target v2.1.3 --yes --backup
```
**Result**: Emergency rollback with minimal prompts, automatic backup, fast execution

#### Security Vulnerability Response (Comprehensive Mode)
```bash
# Situation: Security issue found, need full audit trail and team coordination
/git-rollback --mode comprehensive --branch production --target v2.0.8 --team-notify --audit-log
```
**Result**: Maximum safety analysis, team impact assessment, complete audit trail

### **👥 Team Development Scenarios**

#### Feature Branch Regression (Safe Preview Mode)
```bash
# Situation: Feature regression after merge, need to verify impact
/git-rollback --mode safe-preview --branch develop --target 1a2b3c4d
```
**Result**: Visual diff preview, impact analysis, confirmation before execution

#### Collaborative Branch Cleanup (Standard Mode)
```bash
# Situation: Team member left unfinished changes, need to cleanup
/git-rollback --branch feature/user-auth --mode standard --team-notify
```
**Result**: Balanced approach with team notification suggestions

### **🔧 Maintenance & Operations**

#### Release Tag Rollback (Comprehensive Mode)
```bash
# Situation: Release tag has issues, need to rollback entire release
/git-rollback --mode comprehensive --target v1.5.2 --action revert --ci-check
```
**Result**: Full release analysis, CI/CD verification, non-destructive revert

#### Dependency Update Reversion (Quick Mode)
```bash
# Situation: Dependency update broke build, quick rollback needed
/git-rollback --mode quick --target HEAD~1 --yes --backup
```
**Result**: Fast rollback to previous working state

### **📊 Complex Repository Scenarios**

#### Multi-Module Repository (Comprehensive Mode)
```bash
# Situation: Monorepo with multiple affected modules
/git-rollback --mode comprehensive --branch main --target v3.0.0 --verify-after
```
**Result**: Full impact analysis across all modules, post-rollback verification

#### Submodule Rollback (Safe Preview Mode)
```bash
# Situation: Submodule update causing issues
/git-rollback --mode safe-preview --target HEAD~5 --exclude "docs/"
```
**Result**: Visual preview of submodule changes, selective exclusion options

### **🎯 Learning & Investigation**

#### Historical Bug Investigation (Standard Mode)
```bash
# Situation: Research when bug was introduced
/git-rollback --mode standard --dry-run --depth 100
```
**Result**: Interactive exploration through commit history, no execution

#### Code Review Training (Safe Preview Mode)
```bash
# Situation: Training new team members on rollback procedures
/git-rollback --mode safe-preview --dry-run --verbose
```
**Result**: Educational preview with detailed explanations

### **🏢 Enterprise Workflow Integration**

#### Release Preparation (Comprehensive Mode)
```bash
# Situation: Pre-release rollback capability test
/git-rollback --mode comprehensive --template release-prep --audit-log --team-notify
```
**Result**: Enterprise-grade rollback simulation with complete documentation

#### Compliance & Auditing (Comprehensive Mode)
```bash
# Situation: Regulatory requirement for rollback audit trail
/git-rollback --mode comprehensive --backup --audit-log --verify-after
```
**Result**: Full audit compliance with verification and documentation

### **⚡ Quick Reference Decision Tree**

```
🚨 Emergency?
   ├─ Yes → Quick Mode + --backup + --yes
   └─ No
        ├─ Team Impact?
        │  ├─ Yes → Comprehensive Mode + --team-notify
        │  └─ No
        │       ├─ Uncertain Impact?
        │       │  ├─ Yes → Safe Preview Mode
        │       │  └─ No → Standard Mode
```

---

## 📖 Important Notes & Best Practices

### **🔄 reset vs revert Strategy Guide**

#### **When to Use `reset`** ⚡
- **Private branches** where you're the sole contributor
- **Local development** before pushing to remote
- **Complete history rewrite** is desired
- **Accidental commits** that should never have existed
- **Branch cleanup** before merge

#### **When to Use `revert`** 🛡️
- **Shared/public branches** with multiple contributors
- **Released versions** that need to maintain history integrity
- **Production hotfixes** where audit trail is required
- **Compliance requirements** that mandate immutable history
- **Team collaboration** to avoid disrupting others' work

### **🏗️ Repository Type Considerations**

#### **Complex Repositories**
- **📦 Monorepos**: Use `--exclude` for unaffected modules
- **🔗 Submodules**: Verify submodule state before/after rollback
- **📁 Large Binary Files**: Ensure LFS pointer consistency
- **🌐 Multi-remote**: Verify all remote states before operations

#### **CI/CD Integration**
- **🚦 Pipeline Status**: Comprehensive mode checks running pipelines
- **🔧 Automated Testing**: Use `--verify-after` for post-rollback validation
- **📊 Release Automation**: Coordinate with release management systems
- **🚫 Protected Environments**: Additional confirmations for staging/production

### **👥 Team Collaboration Best Practices**

#### **Before Rollback**
- **📢 Communicate Intent**: Notify team about planned rollback
- **🔍 Check Active Work**: Scan for ongoing PRs and branches
- **⏰ Time Operations**: Avoid rollback during active development hours
- **📋 Document Reason**: Create clear audit trail for future reference

#### **After Rollback**
- **🎯 Verify Functionality**: Test critical workflows and features
- **📢 Update Team**: Share rollback completion and impact
- **🔧 Fix Root Cause**: Address underlying issue that caused rollback
- **📊 Review Process**: Analyze rollback for process improvements

### **🔒 Advanced Safety Practices**

#### **Backup Strategy**
```bash
# Automatic backup naming convention
backup/<branch-name>-<YYYY-MM-DD-HH-MM>-<short-hash>

# Manual backup before complex operations
git branch backup/pre-rollback-$(date +%Y%m%d-%H%M%S)
```

#### **Recovery Procedures**
```bash
# Quick restore from backup
git switch backup/feature-auth-2025-01-21-14-30-abc123

# Verify rollback success
git log --oneline -5
git status
git diff origin/<branch>
```

#### **Audit Trail Management**
- **📝 Log Location**: `.git/rollback-*.log` files
- **🔍 Review Regularly**: Periodic audit log analysis
- **📊 Metrics Tracking**: Rollback frequency and patterns
- **🗂️ Archive Strategy**: Long-term log retention policies

### **⚠️ Critical Warning Scenarios**

#### **🛑 Stop Immediately If:**
- **Active CI/CD pipelines** are running
- **Multiple contributors** have pushed recently
- **Production deployments** are in progress
- **Critical release** is pending or recently deployed

#### **⚡ Proceed with Caution When:**
- **Protected branches** are targeted (additional confirmations required)
- **Large diffs** are detected (>1000 lines, >50 files)
- **Submodule/LFS** changes are involved
- **Tags/releases** will be affected

### **🚀 Performance Optimization**

#### **Large Repository Handling**
- **📊 Shallow Analysis**: Use appropriate `--depth` for faster operation
- **🔍 Selective Diffing**: Focus on specific paths with `--exclude`
- **⚡ Quick Mode**: For emergency situations requiring speed
- **📋 Parallel Operations**: Background fetching for large repos

#### **Memory & Storage**
- **🗑️ Cleanup Old Backups**: Regular backup branch maintenance
- **📝 Log Rotation**: Manage audit log file sizes
- **💾 Cache Optimization**: Leverage git's built-in caching mechanisms

### **🎯 Mode Selection Guidelines**

#### **Emergency Scenarios** → **Quick Mode**
- Production downtime requiring immediate action
- Security vulnerabilities needing instant response
- Critical system failures with business impact

#### **Uncertain Impact** → **Safe Preview Mode**
- Complex changes with unclear scope
- First-time rollback on specific branch
- When visual confirmation provides confidence

#### **Team Collaboration** → **Comprehensive Mode**
- Shared branches with active contributors
- Production releases with compliance requirements
- Complex rollbacks requiring full analysis

#### **Daily Operations** → **Standard Mode**
- Regular development workflow
- Feature branch maintenance
- Routine cleanup operations

---
