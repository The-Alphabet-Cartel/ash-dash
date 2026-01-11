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
SkeletonCard Component - Animated placeholder for metric/stat cards
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
    class="card p-6 animate-pulse"
    role="status"
    aria-label="Loading content"
  >
    <!-- Icon placeholder -->
    <div 
      v-if="showIcon"
      class="w-10 h-10 rounded-lg bg-gray-200 dark:bg-gray-700 mb-4"
    />
    
    <!-- Title placeholder -->
    <div class="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded mb-3" />
    
    <!-- Value placeholder -->
    <div class="h-8 w-16 bg-gray-200 dark:bg-gray-700 rounded mb-2" />
    
    <!-- Subtitle placeholder (optional) -->
    <div 
      v-if="showSubtitle"
      class="h-3 w-32 bg-gray-200 dark:bg-gray-700 rounded"
    />
    
    <span class="sr-only">Loading...</span>
  </div>
</template>

<script setup>
/**
 * SkeletonCard Component
 * 
 * Animated placeholder for metric/stat cards while loading.
 * Matches the layout of MetricCard component.
 * 
 * Usage:
 *   <SkeletonCard />
 *   <SkeletonCard :show-icon="false" />
 *   <SkeletonCard show-subtitle />
 */

// =============================================================================
// Props
// =============================================================================

defineProps({
  /**
   * Show icon placeholder
   */
  showIcon: {
    type: Boolean,
    default: true,
  },
  
  /**
   * Show subtitle placeholder
   */
  showSubtitle: {
    type: Boolean,
    default: false,
  },
})
</script>
