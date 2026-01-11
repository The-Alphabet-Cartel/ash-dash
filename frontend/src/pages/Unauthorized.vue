<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Unauthorized Page - Shown when user lacks authentication or CRT membership
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.4-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
    <div class="text-center max-w-md">
      <!-- Icon -->
      <div class="mx-auto w-20 h-20 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mb-6">
        <ShieldAlert class="w-10 h-10 text-red-600 dark:text-red-400" />
      </div>
      
      <!-- Title -->
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
        {{ title }}
      </h1>
      
      <!-- Error Message (from OIDC callback) -->
      <div 
        v-if="errorMessage"
        class="mb-4 p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800"
      >
        <p class="text-sm text-red-700 dark:text-red-300">
          {{ errorMessage }}
        </p>
      </div>
      
      <!-- Description -->
      <p class="text-gray-600 dark:text-gray-400 mb-6">
        {{ description }}
      </p>
      
      <!-- Actions -->
      <div class="space-y-3">
        <button 
          @click="handleLogin"
          class="btn-primary w-full flex items-center justify-center gap-2"
        >
          <LogIn class="w-4 h-4" />
          Sign In with Pocket-ID
        </button>
        
        <a 
          href="https://discord.gg/alphabetcartel"
          target="_blank"
          rel="noopener noreferrer"
          class="btn-secondary w-full flex items-center justify-center gap-2"
        >
          <MessageCircle class="w-4 h-4" />
          Join The Alphabet Cartel
        </a>
      </div>
      
      <!-- Help Text -->
      <p class="mt-6 text-sm text-gray-500 dark:text-gray-500">
        Not a CRT member? Contact the admin team on Discord for access.
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { ShieldAlert, LogIn, MessageCircle } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()

// Get error message from query params (from OIDC callback failures)
const errorMessage = computed(() => {
  return route.query.error ? decodeURIComponent(route.query.error) : null
})

// Get redirect path for after login
const redirectPath = computed(() => {
  return route.query.redirect || '/'
})

// Determine title based on error type
const title = computed(() => {
  if (errorMessage.value?.includes('CRT membership')) {
    return 'Access Denied'
  }
  return 'Authentication Required'
})

// Determine description based on error type
const description = computed(() => {
  if (errorMessage.value?.includes('CRT membership')) {
    return 'You are logged in but you need to be a CRT member to access the Ash-Dash dashboard.'
  }
  return 'You need to be logged in as a CRT member to access the Ash-Dash dashboard. Please sign in with your Alphabet Cartel credentials.'
})

// Handle login button click
const handleLogin = () => {
  authStore.login(redirectPath.value)
}
</script>
