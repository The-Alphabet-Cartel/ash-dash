<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
SeverityBadge - Reusable severity indicator badge
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
    :aria-label="`Severity: ${severity}`"
  >
    <span 
      v-if="showDot"
      aria-hidden="true"
      :class="[
        'rounded-full',
        dotSizeClasses,
        dotColorClasses,
        pulse && isPulsing ? 'animate-pulse' : ''
      ]"
    />
    <span class="capitalize">{{ severity }}</span>
  </span>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  severity: {
    type: String,
    required: true,
    validator: (v) => ['critical', 'high', 'medium', 'low', 'safe'].includes(v)
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v)
  },
  showDot: {
    type: Boolean,
    default: true
  },
  pulse: {
    type: Boolean,
    default: false
  }
})

const isPulsing = computed(() => {
  return props.severity === 'critical' || props.severity === 'high'
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'px-2 py-0.5 text-xs'
    case 'lg': return 'px-4 py-1.5 text-base'
    default: return 'px-2.5 py-1 text-sm'
  }
})

const dotSizeClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'w-1.5 h-1.5'
    case 'lg': return 'w-3 h-3'
    default: return 'w-2 h-2'
  }
})

const colorClasses = computed(() => {
  switch (props.severity) {
    case 'critical':
      return 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300'
    case 'high':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    case 'medium':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    case 'low':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    case 'safe':
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700/30 dark:text-gray-300'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700/30 dark:text-gray-300'
  }
})

const dotColorClasses = computed(() => {
  switch (props.severity) {
    case 'critical': return 'bg-purple-500'
    case 'high': return 'bg-red-500'
    case 'medium': return 'bg-yellow-500'
    case 'low': return 'bg-green-500'
    case 'safe': return 'bg-gray-400'
    default: return 'bg-gray-400'
  }
})
</script>
