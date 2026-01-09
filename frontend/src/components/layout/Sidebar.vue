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
FILE VERSION: v5.0-7-7.8-2
LAST MODIFIED: 2026-01-09
PHASE: Phase 7 - Documentation Wiki
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
      <router-link
        v-for="item in navItems"
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
    </nav>

    <!-- Footer Section -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 space-y-3">
      <!-- Theme Toggle -->
      <ThemeToggle />
      
      <!-- User Info (placeholder for Phase 4) -->
      <div class="flex items-center gap-3 px-3 py-2 rounded-lg bg-gray-50 dark:bg-gray-800">
        <div class="w-8 h-8 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center">
          <User class="w-4 h-4 text-white" />
        </div>
        <div class="flex-1 min-w-0">
          <p class="text-sm font-medium text-gray-900 dark:text-white truncate">CRT Member</p>
          <p class="text-xs text-gray-500 dark:text-gray-400 truncate">Logged in</p>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  Shield, 
  LayoutDashboard, 
  MessageSquareWarning, 
  BookOpen, 
  Settings,
  User 
} from 'lucide-vue-next'
import ThemeToggle from './ThemeToggle.vue'

const route = useRoute()

// Navigation items
const navItems = [
  { 
    path: '/', 
    label: 'Dashboard', 
    icon: LayoutDashboard 
  },
  { 
    path: '/sessions', 
    label: 'Sessions', 
    icon: MessageSquareWarning,
    badge: null // Will show count of active sessions in Phase 4
  },
  { 
    path: '/wiki', 
    label: 'Documentation', 
    icon: BookOpen 
  },
  { 
    path: '/admin', 
    label: 'Administration', 
    icon: Settings 
  },
]

// Check if a nav item is active
const isActive = (path) => {
  if (path === '/') {
    return route.path === '/'
  }
  return route.path.startsWith(path)
}
</script>
