<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================

MISSION - NEVER TO BE VIOLATED:
    Reveal   → Surface crisis alerts and user escalation patterns in real-time
    Enable   → Equip Crisis Response Teams with tools for swift intervention
    Clarify  → Translate detection data into actionable intelligence
    Protect  → Safeguard our LGBTQIA+ community through vigilant oversight

============================================================================
Sidebar Component - Collapsible navigation sidebar with icons and tooltips
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-17
PHASE: Phase 3 - CRT-Accessible System Health
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <aside 
    class="fixed left-0 top-0 z-40 h-screen flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 transition-colors sidebar-transition overflow-hidden"
    :class="isCollapsed ? 'w-16' : 'w-64'"
    role="navigation"
    aria-label="Main navigation"
  >
    
    <!-- Logo Section -->
    <div 
      class="flex items-center gap-3 p-4 border-b border-gray-200 dark:border-gray-700"
      :class="isCollapsed ? 'justify-center' : ''"
    >
      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 via-pink-500 to-orange-400 flex items-center justify-center shadow-lg flex-shrink-0">
        <Shield class="w-6 h-6 text-white" aria-hidden="true" />
      </div>
      <div v-if="!isCollapsed" class="overflow-hidden">
        <h1 class="font-bold text-gray-900 dark:text-white">Ash-Dash</h1>
        <p class="text-xs text-gray-500 dark:text-gray-400">Crisis Response Dashboard</p>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-2 space-y-1 overflow-y-auto overflow-x-hidden" aria-label="Primary">
      <!-- Main Navigation Items -->
      <router-link
        v-for="item in mainNavItems"
        :key="item.path"
        :to="item.path"
        class="group relative flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
        :class="[
          isCollapsed ? 'justify-center' : '',
          isActive(item.path)
            ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
        ]"
        :aria-label="item.label"
        :aria-current="isActive(item.path) ? 'page' : undefined"
      >
        <component :is="item.icon" class="w-5 h-5 flex-shrink-0" aria-hidden="true" />
        
        <!-- Label (hidden when collapsed) -->
        <span v-if="!isCollapsed" class="truncate">{{ item.label }}</span>
        
        <!-- Badge for critical items (hidden when collapsed) -->
        <span 
          v-if="item.badge && !isCollapsed" 
          class="ml-auto px-2 py-0.5 text-xs font-semibold rounded-full bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300"
        >
          {{ item.badge }}
        </span>
        
        <!-- Tooltip (shown when collapsed) -->
        <span 
          v-if="isCollapsed" 
          class="tooltip-right"
          role="tooltip"
        >
          {{ item.label }}
          <span v-if="item.badge" class="ml-1 text-red-300">({{ item.badge }})</span>
        </span>
      </router-link>
      
      <!-- Admin Section (Lead+ only) -->
      <div v-if="authStore.isLead" class="pt-4 mt-4 border-t border-gray-200 dark:border-gray-700">
        <p 
          v-if="!isCollapsed"
          class="px-3 mb-2 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider"
        >
          Administration
        </p>
        <router-link
          to="/admin"
          class="group relative flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="[
            isCollapsed ? 'justify-center' : '',
            isActive('/admin')
              ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
          ]"
          aria-label="Admin Panel"
          :aria-current="isActive('/admin') ? 'page' : undefined"
        >
          <Settings class="w-5 h-5 flex-shrink-0" aria-hidden="true" />
          <span v-if="!isCollapsed">Admin Panel</span>
          
          <!-- Tooltip when collapsed -->
          <span v-if="isCollapsed" class="tooltip-right" role="tooltip">
            Admin Panel
          </span>
        </router-link>
      </div>
    </nav>

    <!-- Footer Section -->
    <div class="p-2 border-t border-gray-200 dark:border-gray-700 space-y-2 overflow-hidden">
      <!-- Theme Toggle -->
      <div :class="isCollapsed ? 'flex justify-center' : ''">
        <ThemeToggle :compact="isCollapsed" />
      </div>
      
      <!-- User Info (hidden when collapsed, show avatar only) -->
      <div 
        class="group relative flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-800"
        :class="isCollapsed ? 'justify-center px-2' : ''"
      >
        <!-- Avatar -->
        <div 
          class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0"
          :class="avatarClass"
          :aria-label="authStore.userName"
        >
          {{ userInitials }}
        </div>
        
        <!-- Name & Role (hidden when collapsed) -->
        <div v-if="!isCollapsed" class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ authStore.userName }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate capitalize">
            {{ authStore.userRole || 'CRT Member' }}
          </p>
        </div>
        
        <!-- Action Buttons (hidden when collapsed) -->
        <div v-if="!isCollapsed" class="flex items-center gap-1">
          <!-- Profile Link -->
          <a
            href="https://id.alphabetcartel.net"
            target="_blank"
            rel="noopener noreferrer"
            class="p-1.5 rounded text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            title="Edit profile on PocketID"
            aria-label="Edit profile on PocketID (opens in new tab)"
          >
            <ExternalLink class="w-4 h-4" aria-hidden="true" />
          </a>
          
          <!-- Logout Button -->
          <button
            @click="handleLogout"
            class="p-1.5 rounded text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
            title="Sign out"
            aria-label="Sign out"
          >
            <LogOut class="w-4 h-4" aria-hidden="true" />
          </button>
        </div>
        
        <!-- Tooltip with user info and actions when collapsed -->
        <div 
          v-if="isCollapsed" 
          class="tooltip-right flex flex-col gap-1"
          role="tooltip"
        >
          <span class="font-medium">{{ authStore.userName }}</span>
          <span class="text-gray-300 text-xs capitalize">{{ authStore.userRole || 'CRT Member' }}</span>
          <div class="mt-1 pt-1 border-t border-gray-600 flex flex-col gap-1">
            <a
              href="https://id.alphabetcartel.net"
              target="_blank"
              rel="noopener noreferrer"
              class="text-xs text-purple-300 hover:text-purple-200 underline text-left"
            >
              Edit profile ↗
            </a>
            <button
              @click="handleLogout"
              class="text-xs text-red-300 hover:text-red-200 underline text-left"
            >
              Sign out
            </button>
          </div>
        </div>
      </div>
      
      <!-- Collapse Toggle Button -->
      <button
        @click="toggleSidebar"
        class="w-full flex items-center justify-center gap-2 px-3 py-2 rounded-lg text-sm font-medium text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-700 dark:hover:text-white transition-colors"
        :title="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        :aria-label="isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'"
        :aria-expanded="!isCollapsed"
      >
        <component 
          :is="isCollapsed ? ChevronRight : ChevronLeft" 
          class="w-5 h-5" 
          aria-hidden="true" 
        />
        <span v-if="!isCollapsed">Collapse</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
/**
 * Sidebar Component
 * 
 * Collapsible navigation sidebar with:
 * - Logo and branding (compact when collapsed)
 * - Main navigation items with tooltips when collapsed
 * - Admin section (Lead+ only)
 * - Theme toggle (compact when collapsed)
 * - User info with logout
 * - Collapse/expand toggle button
 * 
 * State:
 * - Sidebar state stored in Pinia ui store
 * - Preference persisted to localStorage
 * 
 * Accessibility:
 * - ARIA labels on all interactive elements
 * - Keyboard navigation support
 * - Screen reader friendly tooltips
 */

import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useUiStore } from '@/stores/ui'
import { 
  Shield, 
  LayoutDashboard, 
  MessageSquareWarning,
  Archive,
  BookOpen, 
  Settings,
  LogOut,
  ChevronLeft,
  ChevronRight,
  ExternalLink,
  Activity,
} from 'lucide-vue-next'
import ThemeToggle from './ThemeToggle.vue'

// =============================================================================
// Composables
// =============================================================================

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const uiStore = useUiStore()

// =============================================================================
// Computed Properties
// =============================================================================

/**
 * Sidebar collapsed state from UI store
 */
const isCollapsed = computed(() => uiStore.sidebarCollapsed)

// =============================================================================
// Navigation Configuration
// =============================================================================

/**
 * Main navigation items (visible to all CRT members)
 */
const mainNavItems = [
  { 
    path: '/', 
    label: 'Dashboard', 
    icon: LayoutDashboard,
  },
  { 
    path: '/sessions', 
    label: 'Sessions', 
    icon: MessageSquareWarning,
    badge: null, // Could show active session count
  },
  { 
    path: '/archives', 
    label: 'Archives', 
    icon: Archive,
  },
  { 
    path: '/wiki', 
    label: 'Documentation', 
    icon: BookOpen,
  },
  { 
    path: '/system-health', 
    label: 'System Health', 
    icon: Activity,
  },
]

// =============================================================================
// Computed Properties
// =============================================================================

/**
 * User initials for avatar
 */
const userInitials = computed(() => {
  const name = authStore.userName
  if (!name || name === 'Unknown') return '?'
  
  // Handle email addresses
  if (name.includes('@')) {
    return name.charAt(0).toUpperCase()
  }
  
  // Get initials from name
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

/**
 * Avatar background class based on role
 */
const avatarClass = computed(() => {
  switch (authStore.userRole) {
    case 'admin':
      return 'bg-purple-500 text-white'
    case 'lead':
      return 'bg-blue-500 text-white'
    default:
      return 'bg-gradient-to-br from-purple-500 to-pink-500 text-white'
  }
})

// =============================================================================
// Methods
// =============================================================================

/**
 * Check if a nav item is active
 */
function isActive(path) {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}

/**
 * Toggle sidebar collapse state
 */
function toggleSidebar() {
  uiStore.toggleSidebar()
}

/**
 * Handle logout
 */
async function handleLogout() {
  await authStore.logout()
  // Router will redirect via auth guard
}
</script>
