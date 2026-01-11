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
ErrorMessage Component - User-friendly error display with retry option
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
    class="p-4 rounded-lg"
    :class="containerClass"
    role="alert"
    aria-live="polite"
  >
    <div class="flex items-start gap-3">
      <!-- Icon -->
      <component 
        :is="iconComponent" 
        class="w-5 h-5 flex-shrink-0 mt-0.5" 
        :class="iconClass"
        aria-hidden="true"
      />
      
      <!-- Content -->
      <div class="flex-1 min-w-0">
        <!-- Title -->
        <h4 class="font-medium" :class="titleClass">
          {{ title }}
        </h4>
        
        <!-- Message -->
        <p class="text-sm mt-1" :class="messageClass">
          {{ message }}
        </p>
        
        <!-- Details (collapsible for technical errors) -->
        <details v-if="details" class="mt-2">
          <summary class="text-xs cursor-pointer" :class="detailsClass">
            Technical details
          </summary>
          <pre class="mt-1 text-xs p-2 rounded bg-black/20 overflow-x-auto" :class="messageClass">{{ details }}</pre>
        </details>
        
        <!-- Actions -->
        <div v-if="showRetry || $slots.actions" class="mt-3 flex items-center gap-2">
          <button
            v-if="showRetry"
            @click="$emit('retry')"
            class="inline-flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium rounded-lg transition-colors"
            :class="buttonClass"
          >
            <RefreshCw class="w-4 h-4" aria-hidden="true" />
            Try again
          </button>
          <slot name="actions" />
        </div>
      </div>
      
      <!-- Dismiss button -->
      <button
        v-if="dismissible"
        @click="$emit('dismiss')"
        class="p-1 rounded hover:bg-black/10 dark:hover:bg-white/10 transition-colors"
        :class="iconClass"
        aria-label="Dismiss"
      >
        <X class="w-4 h-4" aria-hidden="true" />
      </button>
    </div>
  </div>
</template>

<script setup>
/**
 * ErrorMessage Component
 * 
 * User-friendly error display with:
 * - Multiple severity variants (error, warning, info)
 * - Optional retry button
 * - Collapsible technical details
 * - Dismissible option
 * - Custom action slot
 * 
 * Usage:
 *   <ErrorMessage 
 *     title="Failed to load sessions" 
 *     message="Please check your connection and try again."
 *     @retry="fetchSessions"
 *   />
 *   
 *   <ErrorMessage 
 *     variant="warning"
 *     title="Connection unstable"
 *     message="Some data may be outdated."
 *     :show-retry="false"
 *   />
 */

import { computed } from 'vue'
import { AlertCircle, AlertTriangle, Info, RefreshCw, X } from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * Error title
   */
  title: {
    type: String,
    default: 'Something went wrong',
  },
  
  /**
   * Error message (user-friendly)
   */
  message: {
    type: String,
    default: 'Please try again later.',
  },
  
  /**
   * Technical error details (shown in collapsible)
   */
  details: {
    type: String,
    default: null,
  },
  
  /**
   * Variant: 'error', 'warning', 'info'
   */
  variant: {
    type: String,
    default: 'error',
    validator: (value) => ['error', 'warning', 'info'].includes(value),
  },
  
  /**
   * Show retry button
   */
  showRetry: {
    type: Boolean,
    default: true,
  },
  
  /**
   * Allow dismissing the error
   */
  dismissible: {
    type: Boolean,
    default: false,
  },
})

// =============================================================================
// Emits
// =============================================================================

defineEmits(['retry', 'dismiss'])

// =============================================================================
// Computed - Variant Styling
// =============================================================================

const iconComponent = computed(() => {
  const icons = {
    error: AlertCircle,
    warning: AlertTriangle,
    info: Info,
  }
  return icons[props.variant]
})

const containerClass = computed(() => {
  const classes = {
    error: 'bg-red-900/30 border border-red-700',
    warning: 'bg-yellow-900/30 border border-yellow-700',
    info: 'bg-blue-900/30 border border-blue-700',
  }
  return classes[props.variant]
})

const iconClass = computed(() => {
  const classes = {
    error: 'text-red-400',
    warning: 'text-yellow-400',
    info: 'text-blue-400',
  }
  return classes[props.variant]
})

const titleClass = computed(() => {
  const classes = {
    error: 'text-red-300',
    warning: 'text-yellow-300',
    info: 'text-blue-300',
  }
  return classes[props.variant]
})

const messageClass = computed(() => {
  const classes = {
    error: 'text-red-200/80',
    warning: 'text-yellow-200/80',
    info: 'text-blue-200/80',
  }
  return classes[props.variant]
})

const detailsClass = computed(() => {
  const classes = {
    error: 'text-red-300/60 hover:text-red-300',
    warning: 'text-yellow-300/60 hover:text-yellow-300',
    info: 'text-blue-300/60 hover:text-blue-300',
  }
  return classes[props.variant]
})

const buttonClass = computed(() => {
  const classes = {
    error: 'text-red-300 bg-red-900/50 hover:bg-red-900/70',
    warning: 'text-yellow-300 bg-yellow-900/50 hover:bg-yellow-900/70',
    info: 'text-blue-300 bg-blue-900/50 hover:bg-blue-900/70',
  }
  return classes[props.variant]
})
</script>
