<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Session Detail Page - Individual session view with notes
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Back Button -->
    <div class="mb-6">
      <router-link 
        to="/sessions"
        class="inline-flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Sessions
      </router-link>
    </div>

    <!-- Session Header -->
    <div class="card p-6 mb-6">
      <div class="flex items-start justify-between">
        <div>
          <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-1">
            Session {{ sessionId }}
          </h2>
          <p class="text-gray-600 dark:text-gray-400">Session details and CRT notes</p>
        </div>
        <span class="px-3 py-1 rounded-full text-sm font-medium bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400">
          Placeholder
        </span>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Session Info (2/3) -->
      <div class="lg:col-span-2 space-y-6">
        <!-- User Info Card -->
        <div class="card p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">User Information</h3>
          <div class="text-center py-8 text-gray-500 dark:text-gray-400">
            User details will be displayed here
            <p class="text-xs mt-2">Coming in Phase 5</p>
          </div>
        </div>

        <!-- Analysis Data Card -->
        <div class="card p-6">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">Analysis Data</h3>
          <div class="text-center py-8 text-gray-500 dark:text-gray-400">
            Ash-NLP analysis results will be displayed here
            <p class="text-xs mt-2">Coming in Phase 5</p>
          </div>
        </div>
      </div>

      <!-- Notes Section (1/3) -->
      <div class="card">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">CRT Notes</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">Session documentation</p>
        </div>
        <div class="p-6">
          <div class="text-center py-8 text-gray-500 dark:text-gray-400">
            <FileText class="w-12 h-12 mx-auto mb-4 text-gray-300 dark:text-gray-600" />
            <p>Notes editor will be here</p>
            <p class="text-xs mt-2">Coming in Phase 6</p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { MainLayout } from '@/components/layout'
import { ArrowLeft, FileText } from 'lucide-vue-next'

const route = useRoute()
const sessionId = computed(() => route.params.id)

// TODO: Phase 5 - Add:
// - Fetch session data by ID
// - Display user info
// - Display analysis data
// - Phase 6: Notes editor
</script>
