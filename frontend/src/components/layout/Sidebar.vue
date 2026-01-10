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
Sidebar Component - Main navigation sidebar with logo and nav items
============================================================================
FILE VERSION: v5.0-10-10.3-8
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <aside class="fixed left-0 top-0 z-40 h-screen w-64 flex flex-col bg-white dark:bg-gray-900 border-r border-gray-200 dark:border-gray-700 transition-colors">
    
    <!-- Logo Section -->
    <div class="flex items-center gap-3 p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="w-10 h-10 rounded-lg bg-gradient-to-br from-purple-500 via-pink-500 to-orange-400 flex items-center justify-center shadow-lg">
        <Shield class="w-6 h-6 text-white" />
      </div>
      <div>
        <h1 class="font-bold text-gray-900 dark:text-white">Ash-Dash</h1>
        <p class="text-xs text-gray-500 dark:text-gray-400">Crisis Response Dashboard</p>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-4 space-y-1 overflow-y-auto">
      <!-- Main Navigation Items -->
      <router-link
        v-for="item in mainNavItems"
        :key="item.path"
        :to="item.path"
        class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
        :class="[
          isActive(item.path)
            ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
            : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
        ]"
      >
        <component :is="item.icon" class="w-5 h-5" />
        <span>{{ item.label }}</span>
        <!-- Badge for critical items -->
        <span 
          v-if="item.badge" 
          class="ml-auto px-2 py-0.5 text-xs font-semibold rounded-full bg-red-100 dark:bg-red-900/50 text-red-700 dark:text-red-300"
        >
          {{ item.badge }}
        </span>
      </router-link>
      
      <!-- Admin Section (Lead+ only) -->
      <div v-if="authStore.isLead" class="pt-4 mt-4 border-t border-gray-200 dark:border-gray-700">
        <p class="px-3 mb-2 text-xs font-semibold text-gray-400 dark:text-gray-500 uppercase tracking-wider">
          Administration
        </p>
        <router-link
          to="/admin"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors"
          :class="[
            isActive('/admin')
              ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
              : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 hover:text-gray-900 dark:hover:text-white'
          ]"
        >
          <Settings class="w-5 h-5" />
          <span>Admin Panel</span>
        </router-link>
      </div>
    </nav>

    <!-- Footer Section -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 space-y-3">
      <!-- Theme Toggle -->
      <ThemeToggle />
      
      <!-- User Info -->
      <div class="flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-800">
        <!-- Avatar -->
        <div 
          class="w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium"
          :class="avatarClass"
        >
          {{ userInitials }}
        </div>
        <!-- Name & Role -->
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">
            {{ authStore.userName }}
          </p>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate capitalize">
            {{ authStore.userRole || 'CRT Member' }}
          </p>
        </div>
        <!-- Logout Button -->
        <button
          @click="handleLogout"
          class="p-1.5 rounded text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          title="Sign out"
        >
          <LogOut class="w-4 h-4" />
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
/**
 * Sidebar Component
 * 
 * Main navigation sidebar with:
 * - Logo and branding
 * - Main navigation items (Dashboard, Sessions, Archives, Wiki)
 * - Admin section (Lead+ only)
 * - Theme toggle
 * - User info with logout
 * 
 * Role-based visibility:
 * - Admin Panel link only shown for Lead and Admin roles
 * - User info displays actual authenticated user data
 */

import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { 
  Shield, 
  LayoutDashboard, 
  MessageSquareWarning,
  Archive,
  BookOpen, 
  Settings,
  LogOut,
} from 'lucide-vue-next'
import ThemeToggle from './ThemeToggle.vue'

// =============================================================================
// Composables
// =============================================================================

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

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
 * Handle logout
 */
async function handleLogout() {
  await authStore.logout()
  // Router will redirect via auth guard
}
</script>
