# Awesome AI Coding Enhance

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/kuku0922/awesome-ai-coding-enhance.svg?style=social&label=Star)](https://github.com/kuku0922/awesome-ai-coding-enhance)
[![GitHub forks](https://img.shields.io/github/forks/kuku0922/awesome-ai-coding-enhance.svg?style=social&label=Fork)](https://github.com/kuku0922/awesome-ai-coding-enhance)
[![GitHub issues](https://img.shields.io/github/issues/kuku0922/awesome-ai-coding-enhance.svg)](https://github.com/kuku0922/awesome-ai-coding-enhance/issues)

[简体中文](README.md) | [English](README.en.md)

> 🚀 **高质量 AI Coding 增强库，助力开发工作流程大幅提升**


## ✨ 项目概述

**Awesome AI Coding Enhance** 提供 Claude Code 开发过程中的增强工具，包含 Prompts、Subagens、Skills、Hooks、Plugins 等。同时希望这些增强工具能够通过修改、完善、组合应用于更多的 AI Coding CLI 或 IDE 中，不断增强开发效率和准确性。

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
├── README.md                   # 主要文档（中文）
├── README.en.md               # 英文文档
├── LICENSE                     # MIT许可证
└── .gitignore                 # Git忽略文件
```

### Prompts

Prompts 提供生产就绪的AI编码提示词，适用于AI驱动的各种开发工作流程。无论您从事前端、后端还是全栈开发，这个提示词库都能提供：

- 📚 **专业提示词** 适用于不同开发角色和技术栈
- 🌍 **双语支持**（中文和英文）服务全球开发团队
- 🏢 **企业级内容** 配合全面最佳实践
- 🔧 **即用型提示词** 可立即用于任何AI编码工具
- 🎯 **角色特定** 为不同开发场景量身定制的指导

### 🎯 核心特性

#### 📝 综合提示词库
- **角色特定提示词**：全栈工程师、Vue开发者、Go后端开发者
- **双语内容**：完整的中英文版本
- **企业聚焦**：专为实际生产环境设计
- **详细指导**：每个提示词4,000-6,000 tokens，提供全面覆盖

#### 🎨 前端开发
- **Vue.js专家**：企业级Vue 3现代化模式开发
- **TypeScript集成**：类型安全的前端开发实践
- **组件架构**：可重用组件设计与实现
- **性能优化**：前端性能和用户体验最佳实践

#### 🚀 后端开发
- **Go后端专家**：专业Go开发配合企业模式
- **API设计**：RESTful API开发和微服务架构
- **数据库集成**：数据建模和数据库最佳实践
- **安全与性能**：后端安全和优化策略

#### 🏗️ 全栈解决方案
- **集成工作流程**：完整的全栈开发指导
- **技术栈**：现代开发技术栈推荐
- **最佳实践**：行业标准开发模式
- **团队协作**：团队开发指南

### 📚 可用提示词

#### 前端开发提示词

##### Vue前端开发
- **语言**：[中文](prompts/claude-code-global/zh/vue-frontend-development-prompt-zh.md) | English
- **专注**：企业级Vue 3 TypeScript开发
- **覆盖**：组件架构、状态管理、测试、性能
- **Token数**：~8,000 tokens（全面企业指导）

#### 后端开发提示词

##### Go后端开发
- **语言**：[中文](prompts/claude-code-global/zh/go-backend-development-prompt-zh.md) | English
- **专注**：专业Go后端开发
- **覆盖**：API设计、数据库集成、安全、微服务
- **Token数**：~7,500 tokens（生产就绪模式）

#### 全栈开发提示词

##### 资深全栈工程师
- **语言**：[中文](prompts/claude-code-global/zh/senior-fullstack-engineer-claude-zh.md) | English
- **专注**：全面全栈开发指导
- **覆盖**：架构、技术选择、最佳实践、团队领导
- **Token数**：~9,000 tokens（完整全栈工作流程）

### 🤝 贡献

我们欢迎为扩展提示词库做出贡献！

#### 贡献方式

1. **🐛 报告问题**：发现错误或有建议？[提交问题](https://github.com/kuku0922/awesome-ai-coding-enhance/issues)
2. **💡 新提示词**：有新提示词想法？[开始讨论](https://github.com/kuku0922/awesome-ai-coding-enhance/discussions)
3. **📝 改进文档**：帮助我们改进文档
4. **🔧 提交提示词**：贡献新的高质量提示词

### 贡献指南

- **质量**：提示词应该全面且生产就绪
- **双语**：尽可能同时提供中英文版本
- **测试**：提交前在不同AI工具中测试提示词
- **文档**：包含清晰的使用说明和示例

### 开发设置

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