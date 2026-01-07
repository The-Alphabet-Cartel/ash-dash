<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Sessions Page - Session list and history view
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Page Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Session History</h2>
      <p class="text-gray-600 dark:text-gray-400">Browse and search past crisis sessions</p>
    </div>

    <!-- Filters Bar -->
    <div class="card p-4 mb-6">
      <div class="flex flex-wrap items-center gap-4">
        <!-- Search -->
        <div class="flex-1 min-w-[200px]">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by Discord ID or username..."
              class="w-full pl-10 pr-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
        </div>
        
        <!-- Severity Filter -->
        <select class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent">
          <option value="">All Severities</option>
          <option value="critical">Critical</option>
          <option value="high">High</option>
          <option value="medium">Medium</option>
          <option value="low">Low</option>
        </select>

        <!-- Status Filter -->
        <select class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent">
          <option value="">All Status</option>
          <option value="active">Active</option>
          <option value="closed">Closed</option>
          <option value="archived">Archived</option>
        </select>
      </div>
    </div>

    <!-- Sessions Table -->
    <div class="card overflow-hidden">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">All Sessions</h3>
      </div>
      
      <!-- Empty State -->
      <div class="flex flex-col items-center justify-center py-16 text-center">
        <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
          <Inbox class="w-8 h-8 text-gray-400 dark:text-gray-500" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">No Sessions Found</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
          Session history will appear here once Ash-Bot begins detecting and logging crisis events.
        </p>
        <p class="mt-4 text-xs text-gray-400 dark:text-gray-500">
          Coming in Phase 5
        </p>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { MainLayout } from '@/components/layout'
import { Search, Inbox } from 'lucide-vue-next'

// TODO: Phase 5 - Add:
// - Real session data fetching
// - Search functionality
// - Pagination
// - Filtering
</script>
