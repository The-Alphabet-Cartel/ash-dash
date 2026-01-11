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
LoadingSpinner Component - Animated loading indicator
============================================================================
FILE VERSION: v5.0-11-11.2-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div 
    class="flex items-center justify-center"
    :class="containerClass"
    role="status"
    :aria-label="label"
  >
    <svg
      class="animate-spin text-purple-500"
      :class="sizeClass"
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
    >
      <circle
        class="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        stroke-width="4"
      />
      <path
        class="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
      />
    </svg>
    <span v-if="showText" class="ml-2 text-gray-600 dark:text-gray-400">
      {{ label }}
    </span>
    <span v-else class="sr-only">{{ label }}</span>
  </div>
</template>

<script setup>
/**
 * LoadingSpinner Component
 * 
 * Animated loading indicator with:
 * - Multiple size options (sm, md, lg)
 * - Optional visible text label
 * - Screen reader accessible
 * - Customizable container padding
 * 
 * Usage:
 *   <LoadingSpinner />
 *   <LoadingSpinner size="lg" label="Loading sessions..." show-text />
 *   <LoadingSpinner size="sm" class="py-2" />
 */

import { computed } from 'vue'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * Size of the spinner: 'sm', 'md', 'lg'
   */
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value),
  },
  
  /**
   * Accessibility label for screen readers
   */
  label: {
    type: String,
    default: 'Loading...',
  },
  
  /**
   * Show text label next to spinner
   */
  showText: {
    type: Boolean,
    default: false,
  },
  
  /**
   * Add padding to container (useful for full-page loaders)
   */
  padded: {
    type: Boolean,
    default: false,
  },
})

// =============================================================================
// Computed
// =============================================================================

const sizeClass = computed(() => {
  const sizes = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-10 h-10',
  }
  return sizes[props.size]
})

const containerClass = computed(() => {
  return props.padded ? 'py-12' : ''
})
</script>
