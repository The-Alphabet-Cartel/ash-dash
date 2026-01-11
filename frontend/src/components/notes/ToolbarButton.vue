<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
ToolbarButton - Reusable formatting button for editor toolbar
============================================================================
FILE VERSION: v5.0-11-11.3-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <button
    type="button"
    :title="title"
    :aria-label="title"
    :aria-pressed="active"
    :disabled="disabled"
    class="toolbar-button p-1.5 rounded transition-colors"
    :class="[
      active 
        ? 'bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300' 
        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700',
      disabled 
        ? 'opacity-50 cursor-not-allowed' 
        : 'hover:text-gray-900 dark:hover:text-white'
    ]"
    @click="$emit('click')"
  >
    <span aria-hidden="true">
      <slot />
    </span>
  </button>
</template>

<script setup>
/**
 * ToolbarButton Component
 * 
 * Simple button for the editor toolbar with active and disabled states.
 */
defineProps({
  title: {
    type: String,
    default: ''
  },
  active: {
    type: Boolean,
    default: false
  },
  disabled: {
    type: Boolean,
    default: false
  }
})

defineEmits(['click'])
</script>

<style scoped>
.toolbar-button:focus {
  outline: none;
  ring: 2px;
  ring-color: #a855f7;
}

.toolbar-button:focus-visible {
  outline: 2px solid #a855f7;
  outline-offset: 1px;
}
</style>
