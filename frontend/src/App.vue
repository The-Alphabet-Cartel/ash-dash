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
Root Application Component - Main app wrapper with router-view
============================================================================
FILE VERSION: v5.0-3-3.1-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div id="ash-dash" class="min-h-screen bg-gray-100 dark:bg-gray-900 transition-colors duration-200">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useThemeStore } from '@/stores/theme'

// Initialize theme on app mount
const themeStore = useThemeStore()

onMounted(() => {
  themeStore.initTheme()
})
</script>

<style>
/* Global transitions for theme switching */
#ash-dash {
  transition: background-color 0.2s ease-in-out, color 0.2s ease-in-out;
}
</style>
