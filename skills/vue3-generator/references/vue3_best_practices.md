# Vue 3 Best Practices and Development Standards

This document provides comprehensive guidelines for developing Vue 3 applications with modern best practices, TypeScript support, and production-ready patterns.

## Table of Contents

- [Project Structure](#project-structure)
- [Component Architecture](#component-architecture)
- [TypeScript Integration](#typescript-integration)
- [State Management with Pinia](#state-management-with-pinia)
- [Routing with Vue Router](#routing-with-vue-router)
- [Styling Guidelines](#styling-guidelines)
- [Performance Optimization](#performance-optimization)
- [Testing Strategy](#testing-strategy)
- [Code Quality and Linting](#code-quality-and-linting)
- [Build and Deployment](#build-and-deployment)
- [Security Best Practices](#security-best-practices)
- [Accessibility Guidelines](#accessibility-guidelines)

## Project Structure

### Recommended Directory Structure

```
src/
├── assets/                 # Static assets (images, fonts, icons)
│   ├── images/
│   ├── fonts/
│   └── icons/
├── components/             # Reusable Vue components
│   ├── common/            # Generic components (Button, Input, Modal)
│   ├── layout/            # Layout components (Header, Sidebar, Footer)
│   └── features/          # Feature-specific components
├── composables/           # Vue composition functions
│   ├── useAuth.ts
│   ├── useApi.ts
│   └── useUtils.ts
├── views/                 # Page-level components (route components)
│   ├── HomeView.vue
│   ├── AboutView.vue
│   └── auth/
├── router/                # Vue Router configuration
│   └── index.ts
├── stores/                # Pinia stores
│   ├── auth.ts
│   ├── user.ts
│   └── app.ts
├── services/              # API and external service integrations
│   ├── api.ts
│   ├── auth.ts
│   └── types.ts
├── utils/                 # Utility functions
│   ├── formatters.ts
│   ├── validators.ts
│   └── constants.ts
├── types/                 # TypeScript type definitions
│   ├── api.ts
│   ├── user.ts
│   └── common.ts
├── styles/                # Global styles and CSS modules
│   ├── main.css
│   ├── variables.css
│   └── components/
├── App.vue                # Root component
└── main.ts                # Application entry point
```

### File Naming Conventions

- **Components**: PascalCase (e.g., `UserProfile.vue`, `DataTable.vue`)
- **Views**: PascalCase with "View" suffix (e.g., `HomeView.vue`, `DashboardView.vue`)
- **Composables**: camelCase with "use" prefix (e.g., `useAuth.ts`, `useDataTable.ts`)
- **Stores**: camelCase (e.g., `userStore.ts`, `authStore.ts`)
- **Utilities**: camelCase (e.g., `formatters.ts`, `validators.ts`)
- **Types**: camelCase (e.g., `userTypes.ts`, `apiTypes.ts`)

## Component Architecture

### Single File Component (SFC) Structure

```vue
<template>
  <!-- Template with semantic HTML and Vue directives -->
  <div class="user-profile">
    <h2>{{ user.name }}</h2>
    <p v-if="user.email">{{ user.email }}</p>
    <button @click="updateProfile" :disabled="isLoading">
      {{ isLoading ? 'Updating...' : 'Update Profile' }}
    </button>
  </div>
</template>

<script setup lang="ts">
// Imports
import { ref, computed, onMounted } from 'vue'
import type { User } from '@/types/user'

// Props definition
interface Props {
  userId: string
  readonly?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false
})

// Emits definition
interface Emits {
  update: [user: User]
  error: [error: Error]
}

const emit = defineEmits<Emits>()

// Reactive state
const user = ref<User | null>(null)
const isLoading = ref(false)
const error = ref<Error | null>(null)

// Computed properties
const initials = computed(() => {
  return user.value?.name
    .split(' ')
    .map(name => name[0])
    .join('')
    .toUpperCase()
})

// Methods
const loadUser = async () => {
  try {
    isLoading.value = true
    error.value = null
    // API call to load user
  } catch (err) {
    error.value = err as Error
  } finally {
    isLoading.value = false
  }
}

const updateProfile = async () => {
  if (!user.value || props.readonly) return

  try {
    isLoading.value = true
    // API call to update user
    emit('update', user.value)
  } catch (err) {
    error.value = err as Error
    emit('error', err as Error)
  } finally {
    isLoading.value = false
  }
}

// Lifecycle hooks
onMounted(() => {
  loadUser()
})
</script>

<style scoped>
/* Component-specific styles using CSS modules or scoped CSS */
.user-profile {
  @apply p-4 border rounded-lg;
}

.user-profile h2 {
  @apply text-xl font-semibold mb-2;
}
</style>
```

### Component Design Principles

1. **Single Responsibility**: Each component should have one clear purpose
2. **Composition over Inheritance**: Use composables for reusable logic
3. **Props Down, Events Up**: Follow unidirectional data flow
4. **Smart vs Dumb Components**: Separate container components from presentational ones
5. **Accessibility First**: Include proper ARIA labels and keyboard navigation

## TypeScript Integration

### Type Definitions

```typescript
// types/user.ts
export interface User {
  id: string
  name: string
  email: string
  avatar?: string
  role: UserRole
  createdAt: Date
  updatedAt: Date
}

export interface UserRole {
  id: string
  name: string
  permissions: string[]
}

// API response types
export interface ApiResponse<T> {
  data: T
  message: string
  success: boolean
  errors?: string[]
}

// Form types
export interface UserFormData {
  name: string
  email: string
  password?: string
  confirmPassword?: string
}
```

### Component Props and Emits

```typescript
// Strongly typed props
interface Props {
  user: User
  readonly?: boolean
  theme?: 'light' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  readonly: false,
  theme: 'light'
})

// Strongly typed emits
interface Emits {
  update: [user: Partial<User>]
  delete: [id: string]
  'theme-change': [theme: 'light' | 'dark']
}

const emit = defineEmits<Emits>()
```

### Utility Types

```typescript
// utils/typeHelpers.ts
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>
export type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P]
}

// Usage examples
type UserUpdate = Optional<User, 'id' | 'createdAt' | 'updatedAt'>
type UserCreation = RequiredFields<User, 'name' | 'email'>
```

## State Management with Pinia

### Store Structure

```typescript
// stores/user.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/user'
import { userService } from '@/services/user'

export const useUserStore = defineStore('user', () => {
  // State
  const currentUser = ref<User | null>(null)
  const users = ref<User[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => !!currentUser.value)
  const userCount = computed(() => users.value.length)
  const getUserById = computed(() => {
    return (id: string) => users.value.find(user => user.id === id)
  })

  // Actions
  const setCurrentUser = (user: User | null) => {
    currentUser.value = user
  }

  const loadUsers = async () => {
    try {
      isLoading.value = true
      error.value = null
      users.value = await userService.getUsers()
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Unknown error'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const createUser = async (userData: Omit<User, 'id' | 'createdAt' | 'updatedAt'>) => {
    try {
      const newUser = await userService.createUser(userData)
      users.value.push(newUser)
      return newUser
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to create user'
      throw err
    }
  }

  const updateUser = async (id: string, updates: Partial<User>) => {
    try {
      const updatedUser = await userService.updateUser(id, updates)
      const index = users.value.findIndex(user => user.id === id)
      if (index !== -1) {
        users.value[index] = updatedUser
      }
      if (currentUser.value?.id === id) {
        currentUser.value = updatedUser
      }
      return updatedUser
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to update user'
      throw err
    }
  }

  const deleteUser = async (id: string) => {
    try {
      await userService.deleteUser(id)
      users.value = users.value.filter(user => user.id !== id)
      if (currentUser.value?.id === id) {
        currentUser.value = null
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Failed to delete user'
      throw err
    }
  }

  // Reset state
  const $reset = () => {
    currentUser.value = null
    users.value = []
    isLoading.value = false
    error.value = null
  }

  return {
    // State
    currentUser: readonly(currentUser),
    users: readonly(users),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Getters
    isAuthenticated,
    userCount,
    getUserById,

    // Actions
    setCurrentUser,
    loadUsers,
    createUser,
    updateUser,
    deleteUser,
    $reset
  }
})
```

### Composables for Store Integration

```typescript
// composables/useAuth.ts
import { computed } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

export const useAuth = () => {
  const userStore = useUserStore()
  const router = useRouter()

  const isAuthenticated = computed(() => userStore.isAuthenticated)
  const currentUser = computed(() => userStore.currentUser)

  const login = async (credentials: LoginCredentials) => {
    try {
      const user = await authService.login(credentials)
      userStore.setCurrentUser(user)
      await router.push('/dashboard')
      return user
    } catch (error) {
      throw error
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
      userStore.setCurrentUser(null)
      await router.push('/login')
    } catch (error) {
      console.error('Logout error:', error)
    }
  }

  const requireAuth = () => {
    if (!isAuthenticated.value) {
      router.push('/login')
    }
  }

  return {
    isAuthenticated,
    currentUser,
    login,
    logout,
    requireAuth
  }
}
```

## Routing with Vue Router

### Route Configuration

```typescript
// router/index.ts
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
    meta: {
      title: 'Home',
      requiresAuth: false
    }
  },
  {
    path: '/auth',
    component: () => import('@/layouts/AuthLayout.vue'),
    children: [
      {
        path: 'login',
        name: 'login',
        component: () => import('@/views/auth/LoginView.vue'),
        meta: {
          title: 'Login',
          requiresGuest: true
        }
      },
      {
        path: 'register',
        name: 'register',
        component: () => import('@/views/auth/RegisterView.vue'),
        meta: {
          title: 'Register',
          requiresGuest: true
        }
      }
    ]
  },
  {
    path: '/dashboard',
    component: () => import('@/layouts/DashboardLayout.vue'),
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'dashboard',
        component: () => import('@/views/DashboardView.vue'),
        meta: {
          title: 'Dashboard'
        }
      },
      {
        path: 'profile',
        name: 'profile',
        component: () => import('@/views/ProfileView.vue'),
        meta: {
          title: 'Profile'
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
    meta: {
      title: 'Page Not Found'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else if (to.hash) {
      return { el: to.hash }
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const { isAuthenticated } = useAuth()

  // Update page title
  if (to.meta.title) {
    document.title = `${to.meta.title} - MyApp`
  }

  // Authentication checks
  if (to.meta.requiresAuth && !isAuthenticated.value) {
    next('/auth/login')
    return
  }

  if (to.meta.requiresGuest && isAuthenticated.value) {
    next('/dashboard')
    return
  }

  next()
})

export default router
```

## Styling Guidelines

### CSS Architecture

```css
/* styles/main.css */
@import './variables.css';
@import './base.css';
@import './components.css';

/* CSS Variables for theming */
:root {
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;
  --color-secondary: #64748b;
  --color-success: #10b981;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
}

/* Dark theme */
[data-theme="dark"] {
  --color-primary: #60a5fa;
  --color-primary-hover: #3b82f6;
  --color-secondary: #94a3b8;
  --bg-primary: #0f172a;
  --bg-secondary: #1e293b;
  --text-primary: #f1f5f9;
  --text-secondary: #cbd5e1;
}
```

### Component Styling

```vue
<template>
  <button
    :class="buttonClasses"
    :disabled="disabled || isLoading"
    @click="handleClick"
  >
    <span v-if="isLoading" class="spinner"></span>
    <slot />
  </button>
</template>

<script setup lang="ts">
interface Props {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  isLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  size: 'md',
  disabled: false,
  isLoading: false
})

const buttonClasses = computed(() => [
  'btn',
  `btn--${props.variant}`,
  `btn--${props.size}`,
  {
    'btn--disabled': props.disabled,
    'btn--loading': props.isLoading
  }
])
</script>

<style scoped>
.btn {
  @apply inline-flex items-center justify-center font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2;
}

.btn--primary {
  @apply bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500;
}

.btn--secondary {
  @apply bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-500;
}

.btn--danger {
  @apply bg-red-600 text-white hover:bg-red-700 focus:ring-red-500;
}

.btn--sm {
  @apply px-3 py-1.5 text-sm;
}

.btn--md {
  @apply px-4 py-2 text-base;
}

.btn--lg {
  @apply px-6 py-3 text-lg;
}

.btn--disabled {
  @apply opacity-50 cursor-not-allowed;
}

.btn--loading {
  @apply cursor-wait;
}

.spinner {
  @apply animate-spin -ml-1 mr-2 h-4 w-4;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
}
</style>
```

## Performance Optimization

### Lazy Loading

```typescript
// Route-level lazy loading
const routes: RouteRecordRaw[] = [
  {
    path: '/admin',
    component: () => import('@/layouts/AdminLayout.vue'),
    children: [
      {
        path: 'users',
        component: () => import('@/views/admin/UsersView.vue')
      }
    ]
  }
]

// Component-level lazy loading
const AsyncComponent = defineAsyncComponent({
  loader: () => import('./HeavyComponent.vue'),
  loadingComponent: LoadingSpinner,
  errorComponent: ErrorMessage,
  delay: 200,
  timeout: 3000
})
```

### Image Optimization

```vue
<template>
  <img
    :src="imageSrc"
    :srcset="imageSrcset"
    :alt="alt"
    :loading="lazy ? 'lazy' : 'eager'"
    :sizes="sizes"
    @error="handleImageError"
  />
</template>

<script setup lang="ts">
interface Props {
  src: string
  alt: string
  lazy?: boolean
  sizes?: string
}

const props = withDefaults(defineProps<Props>(), {
  lazy: true,
  sizes: '(max-width: 768px) 100vw, 50vw'
})

const imageSrc = computed(() => {
  // Generate responsive image URLs
  return `${props.src}?format=webp&quality=80`
})

const imageSrcset = computed(() => {
  const sizes = [400, 800, 1200, 1600]
  return sizes
    .map(size => `${props.src}?w=${size}&format=webp&quality=80 ${size}w`)
    .join(', ')
})

const handleImageError = (event: Event) => {
  const img = event.target as HTMLImageElement
  img.src = '/images/placeholder.jpg'
}
</script>
```

### Virtual Scrolling

```vue
<template>
  <div class="virtual-list" :style="{ height: containerHeight + 'px' }" @scroll="handleScroll">
    <div :style="{ height: totalHeight + 'px', position: 'relative' }">
      <div
        v-for="item in visibleItems"
        :key="item.id"
        :style="{
          position: 'absolute',
          top: item.top + 'px',
          height: itemHeight + 'px',
          width: '100%'
        }"
      >
        <slot :item="item.data" :index="item.index" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  items: any[]
  itemHeight: number
  containerHeight: number
  overscan?: number
}

const props = withDefaults(defineProps<Props>(), {
  overscan: 5
})

const scrollTop = ref(0)

const totalHeight = computed(() => props.items.length * props.itemHeight)

const startIndex = computed(() => {
  return Math.max(0, Math.floor(scrollTop.value / props.itemHeight) - props.overscan)
})

const endIndex = computed(() => {
  return Math.min(
    props.items.length - 1,
    Math.ceil((scrollTop.value + props.containerHeight) / props.itemHeight) + props.overscan
  )
})

const visibleItems = computed(() => {
  return props.items.slice(startIndex.value, endIndex.value + 1).map((item, index) => ({
    id: item.id,
    data: item,
    index: startIndex.value + index,
    top: (startIndex.value + index) * props.itemHeight
  }))
})

const handleScroll = (event: Event) => {
  scrollTop.value = (event.target as HTMLElement).scrollTop
}
</script>
```

## Testing Strategy

### Component Testing with Vitest

```typescript
// tests/components/UserProfile.spec.ts
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'
import UserProfile from '@/components/UserProfile.vue'
import type { User } from '@/types/user'

describe('UserProfile', () => {
  const mockUser: User = {
    id: '1',
    name: 'John Doe',
    email: 'john@example.com',
    role: { id: '1', name: 'user', permissions: [] },
    createdAt: new Date(),
    updatedAt: new Date()
  }

  it('renders user information correctly', () => {
    const wrapper = mount(UserProfile, {
      props: { user: mockUser }
    })

    expect(wrapper.find('h2').text()).toBe('John Doe')
    expect(wrapper.find('p').text()).toBe('john@example.com')
  })

  it('emits update event when edit button is clicked', async () => {
    const wrapper = mount(UserProfile, {
      props: { user: mockUser }
    })

    await wrapper.find('button').trigger('click')
    await nextTick()

    expect(wrapper.emitted()).toHaveProperty('update')
    expect(wrapper.emitted('update')?.[0]).toEqual([mockUser])
  })

  it('displays loading state', async () => {
    const wrapper = mount(UserProfile, {
      props: { user: mockUser, isLoading: true }
    })

    const button = wrapper.find('button')
    expect(button.attributes('disabled')).toBeDefined()
    expect(button.text()).toContain('Updating...')
  })

  it('is readonly when readonly prop is true', () => {
    const wrapper = mount(UserProfile, {
      props: { user: mockUser, readonly: true }
    })

    const button = wrapper.find('button')
    expect(button.attributes('disabled')).toBeDefined()
  })
})
```

### Composables Testing

```typescript
// tests/composables/useAuth.spec.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useAuth } from '@/composables/useAuth'
import { createPinia, setActivePinia } from 'pinia'
import { useRouter } from 'vue-router'

// Mock dependencies
vi.mock('@/services/auth')
vi.mock('vue-router')

describe('useAuth', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('should initialize with authentication state', () => {
    const { isAuthenticated, currentUser } = useAuth()

    expect(isAuthenticated.value).toBe(false)
    expect(currentUser.value).toBeNull()
  })

  it('should login successfully', async () => {
    const mockRouter = { push: vi.fn() }
    ;(useRouter as any).mockReturnValue(mockRouter)

    const { login, isAuthenticated } = useAuth()

    const credentials = { email: 'test@example.com', password: 'password' }
    await login(credentials)

    expect(isAuthenticated.value).toBe(true)
    expect(mockRouter.push).toHaveBeenCalledWith('/dashboard')
  })
})
```

## Code Quality and Linting

### ESLint Configuration (.eslintrc.cjs)

```javascript
module.exports = {
  root: true,
  env: {
    node: true,
    browser: true,
    es2022: true
  },
  extends: [
    'eslint:recommended',
    '@vue/eslint-config-typescript',
    '@vue/eslint-config-prettier/skip-formatting',
    'plugin:vue/vue3-recommended'
  ],
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module'
  },
  rules: {
    // Vue specific rules
    'vue/multi-word-component-names': 'off',
    'vue/component-name-in-template-casing': ['error', 'PascalCase'],
    'vue/component-definition-name-casing': ['error', 'PascalCase'],
    'vue/custom-event-name-casing': ['error', 'camelCase'],
    'vue/define-macros-order': ['error', {
      order: ['defineProps', 'defineEmits']
    }],
    'vue/no-unused-vars': 'error',
    'vue/padding-line-between-blocks': ['error', 'always'],
    'vue/prefer-separate-static-class': 'error',

    // TypeScript rules
    '@typescript-eslint/no-unused-vars': 'error',
    '@typescript-eslint/no-explicit-any': 'warn',
    '@typescript-eslint/prefer-const': 'error',

    // General rules
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off',
    'prefer-const': 'error',
    'no-var': 'error'
  },
  overrides: [
    {
      files: ['**/__tests__/**/*', '**/*.{test,spec}.*'],
      rules: {
        'no-console': 'off'
      }
    }
  ]
}
```

### Prettier Configuration (.prettierrc)

```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "none",
  "printWidth": 100,
  "endOfLine": "lf",
  "arrowParens": "avoid",
  "vueIndentScriptAndStyle": true
}
```

## Build and Deployment

### Vite Configuration (vite.config.ts)

```typescript
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],

  resolve: {
    alias: {
      '@': resolve(__dirname, 'src'),
      '@components': resolve(__dirname, 'src/components'),
      '@views': resolve(__dirname, 'src/views'),
      '@stores': resolve(__dirname, 'src/stores'),
      '@utils': resolve(__dirname, 'src/utils'),
      '@types': resolve(__dirname, 'src/types')
    }
  },

  build: {
    target: 'es2020',
    outDir: 'dist',
    assetsDir: 'assets',
    sourcemap: true,
    minify: 'terser',
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    },
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['vue', 'vue-router', 'pinia'],
          ui: ['@headlessui/vue', '@heroicons/vue']
        }
      }
    },
    chunkSizeWarningLimit: 1000
  },

  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  },

  preview: {
    port: 4173,
    host: true
  },

  optimizeDeps: {
    include: ['vue', 'vue-router', 'pinia']
  }
})
```

### Environment Configuration

```typescript
// .env.development
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=MyApp (Development)
VITE_DEBUG=true

// .env.production
VITE_API_BASE_URL=https://api.myapp.com
VITE_APP_NAME=MyApp
VITE_DEBUG=false
```

## Security Best Practices

### Content Security Policy

```typescript
// main.ts
const cspScript = document.createElement('meta')
cspScript.httpEquiv = 'Content-Security-Policy'
cspScript.content = `
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://www.googletagmanager.com;
  style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
  font-src 'self' https://fonts.gstatic.com;
  img-src 'self' data: https:;
  connect-src 'self' https://api.myapp.com;
  frame-src 'none';
`.replace(/\s+/g, ' ').trim()

document.head.appendChild(cspScript)
```

### XSS Prevention

```vue
<template>
  <!-- Always use v-text for user content -->
  <div v-text="userContent"></div>

  <!-- Use v-html only with sanitized content -->
  <div v-html="sanitizedHtml"></div>

  <!-- Proper attribute binding -->
  <img :src="trustedImageUrl" :alt="imageDescription" />
</template>

<script setup lang="ts">
import DOMPurify from 'dompurify'

const userContent = ref('<script>alert("xss")</script>')
const sanitizedHtml = computed(() => DOMPurify.sanitize(userContent.value))
</script>
```

## Accessibility Guidelines

### ARIA Labels and Roles

```vue
<template>
  <!-- Semantic HTML -->
  <main role="main" aria-label="Main content">
    <h1>{{ pageTitle }}</h1>

    <!-- Form with proper labels -->
    <form @submit.prevent="handleSubmit">
      <label for="email">Email address</label>
      <input
        id="email"
        v-model="form.email"
        type="email"
        required
        aria-describedby="email-help"
        aria-invalid="!!errors.email"
      />
      <div id="email-help" class="sr-only">
        Enter your email address
      </div>
      <div v-if="errors.email" role="alert" class="error-message">
        {{ errors.email }}
      </div>

      <!-- Accessible button -->
      <button
        type="submit"
        :disabled="isLoading"
        :aria-label="isLoading ? 'Submitting form, please wait' : 'Submit form'"
      >
        <span v-if="isLoading" aria-hidden="true">Loading...</span>
        <span v-else>Submit</span>
      </button>
    </form>

    <!-- Accessible navigation -->
    <nav role="navigation" aria-label="Main navigation">
      <ul>
        <li v-for="item in navigation" :key="item.path">
          <router-link
            :to="item.path"
            :aria-current="isCurrentPath(item.path) ? 'page' : undefined"
          >
            {{ item.name }}
          </router-link>
        </li>
      </ul>
    </nav>
  </main>
</template>

<style scoped>
/* Screen reader only content */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Focus management */
button:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  .btn {
    border: 2px solid currentColor;
  }
}
</style>
```

This comprehensive guide provides the foundation for building modern, scalable, and maintainable Vue 3 applications with best practices for TypeScript integration, state management, testing, and accessibility.