---
name: vue3-generator
description: Generate production-ready Vue 3 frontend projects with TypeScript, Vite, Vue Router, and Pinia using modern best practices and the latest stable versions.
license: MIT
---

# Vue 3 Project Generator

This skill should be used when you need to create a new Vue 3 frontend application with modern tooling and best practices. It generates complete, production-ready projects with proper structure, dependencies, configuration, and development tools.

## When to Use This Skill

Use this skill in these scenarios:

1. **Starting a new Vue 3 project** - Generate a complete project structure with modern tooling
2. **Building SPAs** - Create single-page applications with Vue Router
3. **Developing TypeScript frontends** - Generate projects with full TypeScript support
4. **Setting up component libraries** - Create projects ready for component development
5. **Rapid prototyping** - Quickly scaffold projects with common features pre-configured
6. **Modern frontend development** - Use Vite for fast development and building

## Quick Start

### Basic Project Generation

To generate a Vue 3 project:

1. **Interactive Mode** (Recommended for beginners):
```bash
skill: "vue3-generator" --interactive
```

2. **Direct Mode** (For experienced users):
```bash
skill: "vue3-generator" --project-name "my-app" --project-type "spa"
```

### Project Types

The generator supports these project types:

- **spa**: Single Page Application with Vue Router
- **pwa**: Progressive Web App with service worker
- **component-lib**: Component library with Vite library mode
- **admin-dashboard**: Admin dashboard with common UI patterns

## Workflow

### Step 1: Environment Setup

The skill first checks and sets up the Node.js environment:

1. **Node Version Check**: Priority order: fnm → nvm → direct node
2. **Version Validation**: Ensure Node.js version meets Vue 3 requirements
3. **Tool Installation**: Verify pnpm is installed and available

### Step 2: Version Querying

The skill queries the latest stable versions:

- **Vue 3**: Latest stable version from npm registry
- **TypeScript**: Latest stable version compatible with Vue 3
- **Vite**: Latest stable version
- **Vue Router**: Latest version compatible with Vue 3
- **Pinia**: Latest version compatible with Vue 3
- **Build Tools**: Latest versions of development dependencies

### Step 3: Project Creation

The skill uses the official Vue 3 create tools:

1. **Use `create-vue`**: The official project scaffolding tool
2. **Apply Configuration**: Based on selected project type and features
3. **Install Dependencies**: Using pnpm for efficient package management
4. **Configure Development Tools**: ESLint, Prettier, TypeScript settings

## Features

### Modern Development Stack

- **Vue 3**: Latest stable version with Composition API
- **TypeScript**: Full type safety and IDE support
- **Vite**: Fast development server and optimized builds
- **Vue Router**: Official routing solution
- **Pinia**: Modern state management
- **pnpm**: Fast, disk space efficient package manager

### Development Tools

- **ESLint**: Code linting with Vue 3 specific rules
- **Prettier**: Code formatting with consistent style
- **Husky**: Git hooks for code quality
- **Commitizen**: Conventional commit messages
- **Vitest**: Fast unit testing framework

### Production Optimizations

- **Tree Shaking**: Automatic dead code elimination
- **Code Splitting**: Optimize bundle sizes
- **Asset Optimization**: Image and font optimization
- **PWA Support**: Service worker and manifest generation
- **SEO Meta**: Proper meta tags and social sharing

## Project Structure

Generated projects follow Vue 3 best practices:

```
my-project/
├── public/                  # Static assets
├── src/
│   ├── assets/             # Project assets
│   ├── components/         # Vue components
│   ├── views/              # Route components
│   ├── stores/             # Pinia stores
│   ├── router/             # Vue Router configuration
│   ├── types/              # TypeScript type definitions
│   ├── utils/              # Utility functions
│   ├── App.vue             # Root component
│   └── main.ts             # Application entry point
├── tests/                  # Test files
├── .env                    # Environment variables
├── .eslintrc.cjs           # ESLint configuration
├── .prettierrc             # Prettier configuration
├── tsconfig.json           # TypeScript configuration
├── vite.config.ts          # Vite configuration
├── package.json            # Project metadata
└── README.md               # Project documentation
```

## Usage Examples

### Example 1: Basic SPA
**Request**: "Create a Vue 3 SPA with TypeScript for a task management application"

**Result**: Complete Vue 3 project with:
- Vue Router for navigation
- Pinia for state management
- TypeScript for type safety
- Pre-built components for task management

### Example 2: PWA Application
**Request**: "Generate a Vue 3 PWA with offline support for a weather app"

**Result**: PWA-ready project with:
- Service worker configuration
- Offline functionality
- App manifest generation
- Responsive design

### Example 3: Component Library
**Request**: "I need to create a Vue 3 component library with TypeScript and Storybook"

**Result**: Library project with:
- Vite library mode configuration
- Storybook integration
- TypeScript declaration files
- Component documentation

## Advanced Configuration

### Customizing the Generator

You can customize the generation process by:

1. **Feature Selection**: Choose specific features during setup
2. **Style Options**: Select CSS framework (Tailwind, Bootstrap, etc.)
3. **Testing Setup**: Configure testing framework and coverage
4. **Build Targets**: Set specific build targets and optimizations

### Environment Variables

The generator sets up these environment variables:
- `VITE_APP_TITLE`: Application title
- `VITE_API_BASE_URL`: API base URL
- `VITE_APP_VERSION`: Application version

## Scripts and Automation

The skill includes these automation scripts:

- **`query_versions.py`**: Queries latest package versions from npm
- **`check_environment.py`**: Validates Node.js and tool setup
- **`init_project.py`**: Main project initialization script
- **`setup_dependencies.py`**: Manages pnpm dependencies

## Best Practices Included

1. **Performance**: Lazy loading, code splitting, and optimization
2. **Accessibility**: ARIA labels and keyboard navigation support
3. **SEO**: Meta tags and semantic HTML structure
4. **Security**: Content Security Policy and XSS prevention
5. **Testing**: Unit tests and integration test setup
6. **Documentation**: README with setup and deployment instructions

## Resources

### scripts/
Executable scripts for project generation and dependency management.

### references/
Documentation for Vue 3 best practices, TypeScript configuration, and modern frontend development patterns.

### assets/
Configuration templates and boilerplate files for different project types.