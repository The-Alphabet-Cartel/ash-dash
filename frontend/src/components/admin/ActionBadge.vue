<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
ActionBadge Component - Visual badge for audit log actions
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.3-5
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <span
    class="inline-flex items-center gap-1 px-2 py-0.5 rounded text-xs font-medium"
    :class="actionClasses"
  >
    <component :is="actionIcon" class="w-3 h-3" />
    {{ actionLabel }}
  </span>
</template>

<script setup>
/**
 * ActionBadge Component
 * 
 * Displays a colored badge for audit log actions:
 * - Create actions: Green
 * - Update actions: Blue
 * - Delete actions: Red
 * - System actions: Purple
 */

import { computed } from 'vue'
import { 
  Plus, 
  Pencil, 
  Trash2, 
  Archive, 
  RotateCcw, 
  Lock, 
  Unlock,
  XCircle,
  Settings,
  User,
} from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * Action type string (e.g., 'note.create', 'session.close')
   */
  action: {
    type: String,
    required: true,
  },
})

// =============================================================================
// Action Configuration
// =============================================================================

const actionConfig = {
  // Note actions
  'note.create': {
    label: 'Note Created',
    icon: Plus,
    classes: 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
  },
  'note.update': {
    label: 'Note Updated',
    icon: Pencil,
    classes: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
  },
  'note.delete': {
    label: 'Note Deleted',
    icon: Trash2,
    classes: 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300',
  },
  'note.lock': {
    label: 'Note Locked',
    icon: Lock,
    classes: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300',
  },
  'note.unlock': {
    label: 'Note Unlocked',
    icon: Unlock,
    classes: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300',
  },
  
  // Session actions
  'session.close': {
    label: 'Session Closed',
    icon: XCircle,
    classes: 'bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300',
  },
  'session.reopen': {
    label: 'Session Reopened',
    icon: RotateCcw,
    classes: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
  },
  'session.assign': {
    label: 'Session Assigned',
    icon: User,
    classes: 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
  },
  'session.unassign': {
    label: 'Session Unassigned',
    icon: User,
    classes: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
  },
  
  // Archive actions
  'archive.create': {
    label: 'Archived',
    icon: Archive,
    classes: 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300',
  },
  'archive.delete': {
    label: 'Archive Deleted',
    icon: Trash2,
    classes: 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300',
  },
  'archive.cleanup': {
    label: 'Cleanup Executed',
    icon: Settings,
    classes: 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300',
  },
  'archive.retention_update': {
    label: 'Retention Updated',
    icon: Pencil,
    classes: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
  },
  
  // User actions
  'user.create': {
    label: 'User Created',
    icon: Plus,
    classes: 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300',
  },
  'user.update': {
    label: 'User Updated',
    icon: Pencil,
    classes: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
  },
  'user.login': {
    label: 'User Login',
    icon: User,
    classes: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
  },
}

// Default for unknown actions
const defaultConfig = {
  label: 'Unknown',
  icon: Settings,
  classes: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
}

// =============================================================================
// Computed Properties
// =============================================================================

const config = computed(() => {
  return actionConfig[props.action] || {
    ...defaultConfig,
    label: formatActionName(props.action),
  }
})

const actionLabel = computed(() => config.value.label)
const actionIcon = computed(() => config.value.icon)
const actionClasses = computed(() => config.value.classes)

// =============================================================================
// Helpers
// =============================================================================

/**
 * Format unknown action names for display.
 * Converts 'entity.action' to 'Entity Action'
 */
function formatActionName(action) {
  return action
    .split('.')
    .map(part => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ')
}
</script>
