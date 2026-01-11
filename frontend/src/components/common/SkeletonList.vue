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
SkeletonList Component - Animated placeholder for list/table content
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
    class="space-y-3"
    role="status"
    aria-label="Loading list"
  >
    <div 
      v-for="i in rows" 
      :key="i" 
      class="card p-4 animate-pulse"
    >
      <div class="flex items-center gap-4">
        <!-- Status indicator placeholder -->
        <div 
          v-if="showIndicator"
          class="w-3 h-3 rounded-full bg-gray-200 dark:bg-gray-700 flex-shrink-0" 
        />
        
        <!-- Avatar placeholder -->
        <div 
          v-if="showAvatar"
          class="w-10 h-10 rounded-full bg-gray-200 dark:bg-gray-700 flex-shrink-0"
        />
        
        <!-- Content placeholders -->
        <div class="flex-1 space-y-2">
          <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded" :class="titleWidth" />
          <div 
            v-if="showSubtitle"
            class="h-3 bg-gray-200 dark:bg-gray-700 rounded" 
            :class="subtitleWidth"
          />
        </div>
        
        <!-- Action placeholder -->
        <div 
          v-if="showAction"
          class="h-8 w-20 bg-gray-200 dark:bg-gray-700 rounded flex-shrink-0"
        />
      </div>
    </div>
    
    <span class="sr-only">Loading list...</span>
  </div>
</template>

<script setup>
/**
 * SkeletonList Component
 * 
 * Animated placeholder for list/table content while loading.
 * Configurable to match different list layouts.
 * 
 * Usage:
 *   <SkeletonList />
 *   <SkeletonList :rows="3" />
 *   <SkeletonList :rows="5" show-avatar show-action />
 */

import { computed } from 'vue'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * Number of skeleton rows to show
   */
  rows: {
    type: Number,
    default: 5,
  },
  
  /**
   * Show status indicator dot
   */
  showIndicator: {
    type: Boolean,
    default: true,
  },
  
  /**
   * Show avatar circle
   */
  showAvatar: {
    type: Boolean,
    default: false,
  },
  
  /**
   * Show subtitle line
   */
  showSubtitle: {
    type: Boolean,
    default: true,
  },
  
  /**
   * Show action button placeholder
   */
  showAction: {
    type: Boolean,
    default: true,
  },
  
  /**
   * Width variant for title: 'sm', 'md', 'lg', 'random'
   */
  titleVariant: {
    type: String,
    default: 'random',
  },
})

// =============================================================================
// Computed
// =============================================================================

const titleWidth = computed(() => {
  if (props.titleVariant === 'random') {
    const widths = ['w-1/3', 'w-2/5', 'w-1/2', 'w-3/5']
    return widths[Math.floor(Math.random() * widths.length)]
  }
  const widthMap = { sm: 'w-1/4', md: 'w-1/3', lg: 'w-1/2' }
  return widthMap[props.titleVariant] || 'w-1/3'
})

const subtitleWidth = computed(() => {
  const widths = ['w-1/4', 'w-1/3', 'w-2/5']
  return widths[Math.floor(Math.random() * widths.length)]
})
</script>
