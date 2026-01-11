<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Not Found Page - 404 error page
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.3-3
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="text-center max-w-md">
      <!-- 404 Badge -->
      <div class="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 font-medium mb-6">
        <AlertTriangle class="w-4 h-4" />
        404 Not Found
      </div>
      
      <!-- Title -->
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Page Not Found
      </h1>
      
      <!-- Description -->
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        The page you're looking for doesn't exist or has been moved.
        Let's get you back on track.
      </p>
      
      <!-- Actions -->
      <div class="flex flex-col sm:flex-row gap-3 justify-center">
        <router-link 
          to="/"
          class="btn-primary flex items-center justify-center gap-2"
        >
          <Home class="w-4 h-4" />
          Go to Dashboard
        </router-link>
        
        <button 
          @click="goBack"
          class="btn-secondary flex items-center justify-center gap-2"
        >
          <ArrowLeft class="w-4 h-4" />
          Go Back
        </button>
      </div>
      
      <!-- Current Path (for debugging) -->
      <p class="mt-8 text-xs text-gray-400 dark:text-gray-600 font-mono">
        Requested: {{ currentPath }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { AlertTriangle, Home, ArrowLeft } from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()

const currentPath = computed(() => route.fullPath)

function goBack() {
  // Go back in history or to dashboard if no history
  if (window.history.length > 2) {
    router.back()
  } else {
    router.push('/')
  }
}
</script>
