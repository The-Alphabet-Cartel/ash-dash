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
ThemeToggle Component - Dark/Light mode toggle button
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <button
    @click="toggleTheme"
    class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors
           text-gray-600 dark:text-gray-400 
           hover:bg-gray-100 dark:hover:bg-gray-800
           hover:text-gray-900 dark:hover:text-white"
    :title="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    <!-- Sun icon (shown in dark mode) -->
    <Sun v-if="isDark" class="w-5 h-5" />
    <!-- Moon icon (shown in light mode) -->
    <Moon v-else class="w-5 h-5" />
    <span class="hidden sm:inline">{{ isDark ? 'Light' : 'Dark' }}</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'
import { Sun, Moon } from 'lucide-vue-next'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
const isDark = computed(() => themeStore.isDark)
const toggleTheme = () => themeStore.toggleTheme()
</script>
