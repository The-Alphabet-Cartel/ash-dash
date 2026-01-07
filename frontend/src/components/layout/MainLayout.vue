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
MainLayout Component - Main application layout wrapper
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-950 transition-colors">
    <!-- Sidebar -->
    <Sidebar />

    <!-- Main Content Area (offset by sidebar width) -->
    <div class="ml-64 min-h-screen flex flex-col">
      <!-- Header -->
      <Header 
        :is-refreshing="isRefreshing"
        :is-connected="isConnected"
        :notification-count="notificationCount"
        @refresh="handleRefresh"
      />

      <!-- Page Content -->
      <main class="flex-1 p-6">
        <slot></slot>
      </main>

      <!-- Footer -->
      <footer class="px-6 py-4 border-t border-gray-200 dark:border-gray-800">
        <div class="flex items-center justify-between text-sm text-gray-500 dark:text-gray-400">
          <div class="flex items-center gap-2">
            <span>Ash-Dash v5.0</span>
            <span class="text-gray-300 dark:text-gray-600">|</span>
            <a 
              href="https://discord.gg/alphabetcartel" 
              target="_blank" 
              rel="noopener noreferrer"
              class="hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
            >
              The Alphabet Cartel
            </a>
          </div>
          <div class="flex items-center gap-1">
            <span>Built with</span>
            <span class="text-red-500">♥</span>
            <span>for chosen family</span>
            <span class="ml-1">🏳️‍🌈</span>
          </div>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Sidebar from './Sidebar.vue'
import Header from './Header.vue'

// State
const isRefreshing = ref(false)
const isConnected = ref(true)
const notificationCount = ref(0)

// Handle refresh action from header
const handleRefresh = async () => {
  isRefreshing.value = true
  
  // Emit event for parent/page to handle actual refresh
  // For now, just simulate a refresh
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  isRefreshing.value = false
}

// TODO: In Phase 4, add:
// - Health check polling to update isConnected
// - WebSocket or polling for notificationCount
// - Global refresh mechanism
</script>
