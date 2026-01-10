<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
RoleBadge Component - Visual badge for user roles
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.3-5
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <span
    class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium"
    :class="roleClasses"
  >
    <component :is="roleIcon" class="w-3 h-3" />
    {{ roleLabel }}
  </span>
</template>

<script setup>
/**
 * RoleBadge Component
 * 
 * Displays a colored badge indicating user role:
 * - Admin: Purple with shield icon
 * - Lead: Blue with star icon
 * - Member: Gray with user icon
 */

import { computed } from 'vue'
import { Shield, Star, User } from 'lucide-vue-next'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  /**
   * User role: 'admin', 'lead', 'member', or null
   */
  role: {
    type: String,
    default: null,
  },
})

// =============================================================================
// Role Configuration
// =============================================================================

const roleConfig = {
  admin: {
    label: 'Admin',
    icon: Shield,
    classes: 'bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-300',
  },
  lead: {
    label: 'Lead',
    icon: Star,
    classes: 'bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-300',
  },
  member: {
    label: 'Member',
    icon: User,
    classes: 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300',
  },
}

// =============================================================================
// Computed Properties
// =============================================================================

const config = computed(() => {
  return roleConfig[props.role] || roleConfig.member
})

const roleLabel = computed(() => config.value.label)
const roleIcon = computed(() => config.value.icon)
const roleClasses = computed(() => config.value.classes)
</script>
