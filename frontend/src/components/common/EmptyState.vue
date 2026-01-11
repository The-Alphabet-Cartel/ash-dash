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
EmptyState Component - Placeholder for empty lists/content areas
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
    class="flex flex-col items-center justify-center py-12 px-4 text-center"
    role="status"
  >
    <!-- Icon -->
    <div 
      class="w-16 h-16 rounded-full flex items-center justify-center mb-4"
      :class="iconContainerClass"
    >
      <component 
        :is="iconComponent" 
        class="w-8 h-8" 
        :class="iconClass"
        aria-hidden="true"
      />
    </div>
    
    <!-- Title -->
    <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">
      {{ title }}
    </h3>
    
    <!-- Message -->
    <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm mb-4">
      {{ message }}
    </p>
    
    <!-- Action Button -->
    <button
      v-if="actionLabel"
      @click="$emit('action')"
      class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium rounded-lg transition-colors"
      :class="buttonClass"
    >
      <component 
        v-if="actionIcon" 
        :is="actionIcon" 
        class="w-4 h-4" 
        aria-hidden="true"
      />
      {{ actionLabel }}
    </button>
    
    <!-- Custom slot for additional content -->
    <slot />
  </div>
</template>

<script setup>
/**
 * EmptyState Component
 * 
 * Placeholder for empty content areas with:
 * - Multiple preset variants (default, search, filter, success)
 * - Custom icon support
 * - Optional action button
 * - Slot for additional content
 * 
 * Usage:
 *   <EmptyState 
 *     title="No sessions found"
 *     message="There are no active sessions at this time."
 *   />
 *   
 *   <EmptyState
 *     variant="search"
 *     title="No results"
 *     message="Try adjusting your search terms."
 *     action-label="Clear search"
 *     @action="clearSearch"
 *   />
 */

import { computed } from 'vue'
import { 
  Inbox, 
  Search, 
  Filter, 
  CheckCircle,
  Archive,
  FileText,
  RefreshCw,
} from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * Title text
   */
  title: {
    type: String,
    default: 'No data',
  },
  
  /**
   * Message text
   */
  message: {
    type: String,
    default: 'There is nothing to display.',
  },
  
  /**
   * Preset variant: 'default', 'search', 'filter', 'success', 'archive', 'document'
   */
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'search', 'filter', 'success', 'archive', 'document'].includes(value),
  },
  
  /**
   * Custom icon component (overrides variant icon)
   */
  icon: {
    type: Object,
    default: null,
  },
  
  /**
   * Action button label (if provided, button is shown)
   */
  actionLabel: {
    type: String,
    default: null,
  },
  
  /**
   * Action button icon component
   */
  actionIcon: {
    type: Object,
    default: null,
  },
})

// =============================================================================
// Emits
// =============================================================================

defineEmits(['action'])

// =============================================================================
// Computed
// =============================================================================

const iconComponent = computed(() => {
  if (props.icon) return props.icon
  
  const icons = {
    default: Inbox,
    search: Search,
    filter: Filter,
    success: CheckCircle,
    archive: Archive,
    document: FileText,
  }
  return icons[props.variant]
})

const iconContainerClass = computed(() => {
  const classes = {
    default: 'bg-gray-100 dark:bg-gray-800',
    search: 'bg-blue-100 dark:bg-blue-900/30',
    filter: 'bg-purple-100 dark:bg-purple-900/30',
    success: 'bg-green-100 dark:bg-green-900/30',
    archive: 'bg-orange-100 dark:bg-orange-900/30',
    document: 'bg-gray-100 dark:bg-gray-800',
  }
  return classes[props.variant]
})

const iconClass = computed(() => {
  const classes = {
    default: 'text-gray-400 dark:text-gray-500',
    search: 'text-blue-500 dark:text-blue-400',
    filter: 'text-purple-500 dark:text-purple-400',
    success: 'text-green-500 dark:text-green-400',
    archive: 'text-orange-500 dark:text-orange-400',
    document: 'text-gray-400 dark:text-gray-500',
  }
  return classes[props.variant]
})

const buttonClass = computed(() => {
  const classes = {
    default: 'text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700',
    search: 'text-blue-700 dark:text-blue-200 bg-blue-100 dark:bg-blue-900/50 hover:bg-blue-200 dark:hover:bg-blue-900/70',
    filter: 'text-purple-700 dark:text-purple-200 bg-purple-100 dark:bg-purple-900/50 hover:bg-purple-200 dark:hover:bg-purple-900/70',
    success: 'text-green-700 dark:text-green-200 bg-green-100 dark:bg-green-900/50 hover:bg-green-200 dark:hover:bg-green-900/70',
    archive: 'text-orange-700 dark:text-orange-200 bg-orange-100 dark:bg-orange-900/50 hover:bg-orange-200 dark:hover:bg-orange-900/70',
    document: 'text-gray-700 dark:text-gray-200 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700',
  }
  return classes[props.variant]
})
</script>
