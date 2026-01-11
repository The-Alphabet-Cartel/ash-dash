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
ThemeToggle Component - Dark/Light mode toggle with compact mode support
============================================================================
FILE VERSION: v5.0-11-11.1-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <button
    @click="toggleTheme"
    class="group relative flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors
           text-gray-600 dark:text-gray-400 
           hover:bg-gray-100 dark:hover:bg-gray-800
           hover:text-gray-900 dark:hover:text-white"
    :class="compact ? 'justify-center w-full' : ''"
    :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
    :aria-pressed="isDark"
  >
    <!-- Sun icon (shown in dark mode) -->
    <Sun v-if="isDark" class="w-5 h-5 flex-shrink-0" aria-hidden="true" />
    <!-- Moon icon (shown in light mode) -->
    <Moon v-else class="w-5 h-5 flex-shrink-0" aria-hidden="true" />
    
    <!-- Label (hidden in compact mode) -->
    <span v-if="!compact" class="hidden sm:inline">{{ isDark ? 'Light' : 'Dark' }}</span>
    
    <!-- Tooltip (shown in compact mode) -->
    <span 
      v-if="compact" 
      class="tooltip-right"
      role="tooltip"
    >
      {{ isDark ? 'Light mode' : 'Dark mode' }}
    </span>
  </button>
</template>

<script setup>
/**
 * ThemeToggle Component
 * 
 * Toggle button for dark/light mode with:
 * - Icon changes based on current theme
 * - Compact mode for collapsed sidebar (icon only + tooltip)
 * - Full accessibility support
 * 
 * Props:
 * - compact: Boolean - When true, shows icon only with tooltip
 */

import { computed } from 'vue'
import { Sun, Moon } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'

// =============================================================================
// Props
// =============================================================================

defineProps({
  /**
   * Compact mode - shows icon only with tooltip (for collapsed sidebar)
   */
  compact: {
    type: Boolean,
    default: false,
  },
})

// =============================================================================
// Store
// =============================================================================

const themeStore = useThemeStore()

// =============================================================================
// Computed
// =============================================================================

const isDark = computed(() => themeStore.isDark)

// =============================================================================
// Methods
// =============================================================================

const toggleTheme = () => themeStore.toggleTheme()
</script>
