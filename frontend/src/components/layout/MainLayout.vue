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
MainLayout Component - Main application layout with collapsible sidebar support
============================================================================
FILE VERSION: v5.0-11-11.1-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors">
    <!-- Skip Link for Accessibility -->
    <a href="#main-content" class="skip-link">
      Skip to main content
    </a>
    
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content Area (offset by sidebar width, with smooth transition) -->
    <div 
      class="min-h-screen flex flex-col content-transition"
      :class="uiStore.sidebarCollapsed ? 'ml-16' : 'ml-64'"
    >
      <!-- Header -->
      <Header 
        :is-refreshing="isRefreshing"
        :is-connected="isConnected"
        :notification-count="notificationCount"
        @refresh="handleRefresh"
      />

      <!-- Page Content -->
      <main id="main-content" class="flex-1 p-6" role="main">
        <slot></slot>
      </main>

      <!-- Footer -->
      <footer class="px-6 py-4 border-t border-gray-200 dark:border-gray-800" role="contentinfo">
        <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <div class="flex items-center gap-2">
            <span>Ash-Dash v5.0</span>
            <span class="text-gray-300 dark:text-gray-600" aria-hidden="true">|</span>
            <a 
              href="https://discord.gg/alphabetcartel" 
              target="_blank" 
              rel="noopener noreferrer"
              class="hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
            >
              The Alphabet Cartel
            </a>
          </div>
          <div class="flex items-center gap-1">
            <span>Built with</span>
            <span class="text-red-500" aria-label="love">♥</span>
            <span>for chosen family</span>
            <span class="ml-1" aria-label="Pride flag">🏳️‍🌈</span>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
/**
 * MainLayout Component
 * 
 * Primary application layout wrapper providing:
 * - Skip link for keyboard/screen reader users
 * - Collapsible sidebar with responsive content margin
 * - Sticky header with actions
 * - Main content area
 * - Footer with branding
 * 
 * The layout responds to sidebar collapse state via the UI store,
 * smoothly transitioning the content margin when toggled.
 */

import { ref, onMounted } from 'vue'
import { useUiStore } from '@/stores/ui'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'

// =============================================================================
// Store
// =============================================================================

const uiStore = useUiStore()

// =============================================================================
// State
// =============================================================================

const isRefreshing = ref(false)
const isConnected = ref(true)
const notificationCount = ref(0)

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  // Initialize UI state (loads sidebar preference from localStorage)
  uiStore.initUiState()
})

// =============================================================================
// Methods
// =============================================================================

/**
 * Handle refresh action from header
 */
const handleRefresh = async () => {
  isRefreshing.value = true
  
  // Emit event for parent/page to handle actual refresh
  // For now, just simulate a refresh
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  isRefreshing.value = false
}
</script>
