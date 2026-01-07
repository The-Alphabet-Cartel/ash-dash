<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Admin Page - Administration panel
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
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Administration</h2>
      <p class="text-gray-600 dark:text-gray-400">User management and system configuration</p>
    </div>

    <!-- Admin Tabs -->
    <div class="card mb-6">
      <div class="flex border-b border-gray-200 dark:border-gray-700">
        <button 
          class="px-6 py-3 text-sm font-medium border-b-2 border-purple-500 text-purple-600 dark:text-purple-400"
        >
          Users
        </button>
        <button 
          class="px-6 py-3 text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
        >
          System Health
        </button>
        <button 
          class="px-6 py-3 text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300"
        >
          Audit Log
        </button>
      </div>
    </div>

    <!-- User Management Section -->
    <div class="card">
      <div class="p-6 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">CRT Members</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400">Manage Crisis Response Team access</p>
          </div>
          <button class="btn-primary">
            <UserPlus class="w-4 h-4 mr-2" />
            Add User
          </button>
        </div>
      </div>
      
      <!-- Empty State -->
      <div class="flex flex-col items-center justify-center py-16 text-center">
        <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
          <Users class="w-8 h-8 text-gray-400 dark:text-gray-500" />
        </div>
        <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">User Management Coming Soon</h3>
        <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
          Admin panel will allow managing CRT members, viewing system health, and browsing audit logs.
        </p>
        <p class="mt-4 text-xs text-gray-400 dark:text-gray-500">
          Coming in Phase 10
        </p>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { MainLayout } from '@/components/layout'
import { Users, UserPlus } from 'lucide-vue-next'

// TODO: Phase 10 - Add:
// - User listing and management
// - System health dashboard
// - Audit log viewer
// - Role management
</script>
