# Awesome AI Coding Enhance

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/kuku0922/awesome-ai-coding-enhance.svg?style=social&label=Star)](https://github.com/kuku0922/awesome-ai-coding-enhance)
[![GitHub forks](https://img.shields.io/github/forks/kuku0922/awesome-ai-coding-enhance.svg?style=social&label=Fork)](https://github.com/kuku0922/awesome-ai-coding-enhance)
[![GitHub issues](https://img.shields.io/github/issues/kuku0922/awesome-ai-coding-enhance.svg)](https://github.com/kuku0922/awesome-ai-coding-enhance/issues)

[简体中文](README.md) | [English](README.en.md)

> 🚀 **高质量 AI Coding 增强库，助力开发工作流程大幅提升**


## ✨ 项目概述

**Awesome AI Coding Enhance** 提供 Claude Code 开发过程中的增强工具，包含 Prompts、Subagents、Skills、Hooks、Plugins 等。同时希望这些增强工具能够通过修改、完善、组合应用于更多的 AI Coding CLI 或 IDE 中，不断增强开发效率和准确性。

### 📁 项目结构

```
awesome-ai-coding-enhance/
├── prompts/                    # 高质量AI编码提示词库
│   └── claude-code-global/     # Claude Code全局提示词
│       ├── zh/                 # 中文版本（3个提示词）
│       │   ├── senior-fullstack-engineer-claude-zh.md
│       │   ├── vue-frontend-development-prompt-zh.md
│       │   └── go-backend-development-prompt-zh.md
│       └── en/                 # 英文版本（3个提示词）
│           ├── senior-fullstack-engineer-claude-en.md
│           ├── vue-frontend-development-prompt.md
│           └── go-backend-development-prompt.md
├── commands/                   # AI编码增强命令
│   ├── git-commit.md          # 智能Git提交，支持多种消息选项
│   ├── git-rollback.md        # 企业级Git回滚，多层安全模式
│   └── [更多命令即将推出]
├── hooks/                      # 开发工作流钩子
├── other-prompts/              # 其他AI提示词模板
├── skills/                     # 技能增强工具
│   └── go-gin-generator/       # Go Gin 项目生成器
├── README.md                   # 主要文档（中文）
├── README.en.md               # 英文文档
├── LICENSE                     # MIT许可证
└── .gitignore                 # Git忽略文件
```

### 📝 Prompts

Prompts 提供生产就绪的AI编码提示词，适用于AI驱动的各种开发工作流程。无论您从事前端、后端还是全栈开发，这个提示词库都能提供：

- 📚 **专业提示词** 适用于不同开发角色和技术栈
- 🌍 **双语支持**（中文和英文）服务全球开发团队
- 🏢 **企业级内容** 配合全面最佳实践
- 🔧 **即用型提示词** 可立即用于任何AI编码工具
- 🎯 **角色特定** 为不同开发场景量身定制的指导

#### 📚 可用提示词

##### 前端开发提示词

##### Vue前端开发
- **专注**：企业级Vue 3 TypeScript开发
- **覆盖**：组件架构、状态管理、测试、性能
- **Token数**：~8,000 tokens（全面企业指导）

##### 后端开发提示词

###### Go后端开发
- **专注**：专业Go后端开发
- **覆盖**：API设计、数据库集成、安全、微服务
- **Token数**：~7,500 tokens（生产就绪模式）

##### 全栈开发提示词

###### 资深全栈工程师
- **专注**：全面全栈开发指导
- **覆盖**：架构、技术选择、最佳实践、团队领导
- **Token数**：~9,000 tokens（完整全栈工作流程）

### ⚡ Commands

Commands为AI编码助手提供预构建的、生产就绪的斜杠命令。这些命令自动化常见开发任务并提升生产力：

- 🚀 **智能Git操作** 配合智能提交消息生成和安全回滚功能
- 🎯 **多层消息选项**：简洁版、详细版和极简版
- 🛡️ **企业级安全** 多层保护模式和协作影响分析
- 🌍 **智能分析** 代码变更以生成最佳提交消息
- 🔧 **自动选择模式** 适应不同工作流偏好
- 📋 **规范遵循** 遵循约定式提交标准
- 📊 **审计追踪** 完整的操作记录和备份策略

#### ⚡ 可用命令

##### 智能Git提交

**特性**:
- **三层消息选项**：在简洁版、详细版和极简版提交消息之间选择
- **智能分析**：自动分析变更以生成合适的提交消息
- **约定式提交**：遵循行业标准的提交消息格式
- **智能拆分**：建议将大型变更拆分为多个专注的提交
- **自动选择**：使用预定义消息类型绕过交互式选择

##### 企业级Git回滚

**特性**:
- **四种安全模式**：快速、安全预览、全面分析和标准模式
- **自动备份创建**：每次回滚都创建时间戳备份分支
- **协作影响检测**：扫描活跃贡献者并警告潜在冲突
- **CI/CD集成**：管道状态验证和依赖关系分析
- **审计追踪**：详细回滚日志和企业级合规支持
- **团队通知**：自动生成团队沟通模板和建议
- **双语支持**：提供中文和英文版本文档

### 🛠️ Skills

Skills 为 Claude Code 提供专业级的开发工具，通过智能生成器加速项目开发：

#### 🚀 Go Gin 项目生成器

**功能**：生产级 Go Gin 框架项目生成器，支持现代最佳实践

**特性**：
- 🏗️ **4 种项目类型**：REST API、Web应用、微服务、gRPC服务
- 📊 **动态版本管理**：自动查询框架最新稳定版本
- 🗄️ **多数据库支持**：PostgreSQL、MySQL、SQLite + GORM集成
- 🔐 **安全认证**：JWT认证、密码哈希、CORS支持
- 🔧 **开发工具集成**：Air热重载、测试框架、代码检查、Swagger文档
- 📋 **自动化脚本**：完整的Makefile、构建脚本、部署脚本
- 📚 **参考文档**：包含Go项目标准、Gin最佳实践、包注册表

#### 贡献方式

1. **🐛 报告问题**：发现错误或有建议？[提交问题](https://github.com/kuku0922/awesome-ai-coding-enhance/issues)


##### 贡献指南

- **质量**：提示词应该全面且生产就绪
- **双语**：尽可能同时提供中英文版本
- **测试**：提交前在不同AI工具中测试提示词
- **文档**：包含清晰的使用说明和示例

##### 开发设置

```bash
# Fork仓库
git clone https://github.com/kuku0922/awesome-ai-coding-enhance.git
cd awesome-ai-coding-enhance

# 创建功能分支
git checkout -b feature/new-prompt

# 添加您的新提示词
# 提交更改
git commit -m 'feature:xxxxx'

# 推送到分支
git push origin feature/new-prompt

# 打开Pull Request
```

## 📄 许可证

本项目在MIT许可证下授权 - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- **Claude Code团队** 提供了出色的AI编码助手

## 📞 支持

- **问题**：[GitHub Issues](https://github.com/kuku0922/awesome-ai-coding-enhance/issues)
---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给它一个星标！⭐**


</div>