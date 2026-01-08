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
MetricCard Component - Reusable dashboard metric display card
============================================================================
FILE VERSION: v5.0-4-4.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 4 - Dashboard & Metrics
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================

USAGE:
  <MetricCard
    label="Active Sessions"
    :value="42"
    :sub-value="+5 from last week"
    sub-value-type="positive"
    :icon="ActivityIcon"
    icon-color="purple"
  />

PROPS:
  - label: Card title/label
  - value: Main numeric or string value
  - subValue: Secondary text below value (optional)
  - subValueType: 'positive', 'negative', 'neutral', 'warning' (optional)
  - icon: Lucide icon component
  - iconColor: 'purple', 'red', 'yellow', 'green', 'blue', 'gray'
  - loading: Show skeleton state
-->

<template>
  <div class="card p-6">
    <!-- Loading Skeleton -->
    <div v-if="loading" class="animate-pulse">
      <div class="flex items-center justify-between mb-4">
        <div class="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded"></div>
        <div class="h-10 w-10 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
      </div>
      <div class="h-8 w-16 bg-gray-200 dark:bg-gray-700 rounded mb-2"></div>
      <div class="h-3 w-32 bg-gray-200 dark:bg-gray-700 rounded"></div>
    </div>

    <!-- Content -->
    <div v-else>
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm font-medium text-gray-500 dark:text-gray-400">
          {{ label }}
        </span>
        <div class="p-2 rounded-lg" :class="iconBgClass">
          <component :is="icon" class="w-5 h-5" :class="iconClass" />
        </div>
      </div>
      
      <div class="flex items-end gap-2">
        <span class="text-3xl font-bold text-gray-900 dark:text-white">
          {{ formattedValue }}
        </span>
        <span v-if="valueSuffix" class="text-sm text-gray-500 dark:text-gray-400 mb-1">
          {{ valueSuffix }}
        </span>
      </div>
      
      <p v-if="subValue" class="mt-2 text-sm" :class="subValueClass">
        {{ subValue }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /** Card label/title */
  label: {
    type: String,
    required: true,
  },
  /** Main value to display */
  value: {
    type: [Number, String],
    required: true,
  },
  /** Optional suffix for the value (e.g., "sessions", "min") */
  valueSuffix: {
    type: String,
    default: '',
  },
  /** Secondary text below the value */
  subValue: {
    type: String,
    default: '',
  },
  /** Type of sub-value for styling */
  subValueType: {
    type: String,
    default: 'neutral',
    validator: (v) => ['positive', 'negative', 'neutral', 'warning'].includes(v),
  },
  /** Lucide icon component */
  icon: {
    type: [Object, Function],
    required: true,
  },
  /** Color theme for the icon */
  iconColor: {
    type: String,
    default: 'gray',
    validator: (v) => ['purple', 'red', 'yellow', 'green', 'blue', 'gray'].includes(v),
  },
  /** Show loading skeleton */
  loading: {
    type: Boolean,
    default: false,
  },
})

// =============================================================================
// Computed
// =============================================================================

/** Format value for display (handle large numbers) */
const formattedValue = computed(() => {
  if (typeof props.value === 'number') {
    // Format large numbers with commas
    if (props.value >= 1000) {
      return props.value.toLocaleString()
    }
    // Format decimals to 1 place
    if (!Number.isInteger(props.value)) {
      return props.value.toFixed(1)
    }
  }
  return props.value
})

/** Icon background color classes */
const iconBgClass = computed(() => {
  const colors = {
    purple: 'bg-purple-100 dark:bg-purple-900/30',
    red: 'bg-red-100 dark:bg-red-900/30',
    yellow: 'bg-yellow-100 dark:bg-yellow-900/30',
    green: 'bg-green-100 dark:bg-green-900/30',
    blue: 'bg-blue-100 dark:bg-blue-900/30',
    gray: 'bg-gray-100 dark:bg-gray-700',
  }
  return colors[props.iconColor] || colors.gray
})

/** Icon color classes */
const iconClass = computed(() => {
  const colors = {
    purple: 'text-purple-600 dark:text-purple-400',
    red: 'text-red-600 dark:text-red-400',
    yellow: 'text-yellow-600 dark:text-yellow-400',
    green: 'text-green-600 dark:text-green-400',
    blue: 'text-blue-600 dark:text-blue-400',
    gray: 'text-gray-600 dark:text-gray-400',
  }
  return colors[props.iconColor] || colors.gray
})

/** Sub-value text color classes */
const subValueClass = computed(() => {
  const types = {
    positive: 'text-green-600 dark:text-green-400',
    negative: 'text-red-600 dark:text-red-400',
    warning: 'text-yellow-600 dark:text-yellow-400',
    neutral: 'text-gray-500 dark:text-gray-400',
  }
  return types[props.subValueType] || types.neutral
})
</script>
