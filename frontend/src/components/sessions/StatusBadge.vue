<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
StatusBadge - Session status indicator badge
============================================================================
FILE VERSION: v5.0-11-11.3-2
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation (ARIA)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <span 
    :class="[
      'inline-flex items-center gap-1 font-medium rounded-full',
      sizeClasses,
      colorClasses
    ]"
    role="status"
    :aria-label="`Status: ${status}`"
  >
    <component :is="icon" v-if="showIcon" :class="iconSizeClasses" aria-hidden="true" />
    <span class="capitalize">{{ status }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue'
import { Activity, CheckCircle, Archive } from 'lucide-vue-next'

const props = defineProps({
  status: {
    type: String,
    required: true,
    validator: (v) => ['active', 'closed', 'archived'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  showIcon: {
    type: Boolean,
    default: true
  }
})

const icon = computed(() => {
  switch (props.status) {
    case 'active': return Activity
    case 'closed': return CheckCircle
    case 'archived': return Archive
    default: return null
  }
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'px-2 py-0.5 text-xs'
    case 'lg': return 'px-4 py-1.5 text-base'
    default: return 'px-2.5 py-1 text-sm'
  }
})

const iconSizeClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'w-3 h-3'
    case 'lg': return 'w-5 h-5'
    default: return 'w-4 h-4'
  }
})

const colorClasses = computed(() => {
  switch (props.status) {
    case 'active':
      return 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
    case 'closed':
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700/30 dark:text-gray-300'
    case 'archived':
      return 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700/30 dark:text-gray-300'
  }
})
</script>
