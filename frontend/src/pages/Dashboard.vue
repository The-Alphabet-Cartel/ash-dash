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
Dashboard Page - Main dashboard view with metrics overview
============================================================================
FILE VERSION: v5.0-3-3.3-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 3 - Frontend Foundation
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Metrics Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-6">
      <!-- Active Sessions Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Active Sessions</span>
          <div class="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30">
            <MessageSquareWarning class="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">0</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">sessions</span>
        </div>
        <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
          No active crisis sessions
        </p>
      </div>

      <!-- Critical Sessions Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">Critical</span>
          <div class="p-2 rounded-lg bg-red-100 dark:bg-red-900/30">
            <AlertTriangle class="w-5 h-5 text-red-600 dark:text-red-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">0</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">critical</span>
        </div>
        <p class="mt-2 text-xs text-green-600 dark:text-green-400">
          All clear
        </p>
      </div>

      <!-- Weekly Total Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">This Week</span>
          <div class="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30">
            <TrendingUp class="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">0</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">total</span>
        </div>
        <p class="mt-2 text-xs text-gray-500 dark:text-gray-400">
          No sessions this week
        </p>
      </div>

      <!-- CRT Online Card -->
      <div class="card p-6">
        <div class="flex items-center justify-between mb-4">
          <span class="text-sm font-medium text-gray-500 dark:text-gray-400">CRT Online</span>
          <div class="p-2 rounded-lg bg-green-100 dark:bg-green-900/30">
            <Users class="w-5 h-5 text-green-600 dark:text-green-400" />
          </div>
        </div>
        <div class="flex items-end gap-2">
          <span class="text-3xl font-bold text-gray-900 dark:text-white">1</span>
          <span class="text-sm text-gray-500 dark:text-gray-400 mb-1">members</span>
        </div>
        <p class="mt-2 text-xs text-green-600 dark:text-green-400">
          You are online
        </p>
      </div>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Active Sessions List (2/3 width) -->
      <div class="lg:col-span-2 card">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Active Sessions</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">Real-time crisis session monitoring</p>
        </div>
        <div class="p-6">
          <!-- Empty State -->
          <div class="flex flex-col items-center justify-center py-12 text-center">
            <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
              <Shield class="w-8 h-8 text-gray-400 dark:text-gray-500" />
            </div>
            <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">No Active Sessions</h3>
            <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
              When Ash-Bot detects a crisis, active sessions will appear here for CRT response.
            </p>
          </div>
        </div>
      </div>

      <!-- Quick Stats (1/3 width) -->
      <div class="card">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">System Status</h2>
          <p class="text-sm text-gray-500 dark:text-gray-400">Service health overview</p>
        </div>
        <div class="p-6 space-y-4">
          <!-- Ash-Bot Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Ash-Bot</span>
            </div>
            <span class="text-xs text-green-600 dark:text-green-400">Online</span>
          </div>
          
          <!-- Ash-NLP Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Ash-NLP</span>
            </div>
            <span class="text-xs text-green-600 dark:text-green-400">Online</span>
          </div>
          
          <!-- Redis Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Redis</span>
            </div>
            <span class="text-xs text-green-600 dark:text-green-400">Connected</span>
          </div>
          
          <!-- Database Status -->
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-3">
              <div class="w-2 h-2 rounded-full bg-green-500"></div>
              <span class="text-sm text-gray-700 dark:text-gray-300">Database</span>
            </div>
            <span class="text-xs text-green-600 dark:text-green-400">Connected</span>
          </div>

          <!-- Divider -->
          <hr class="border-gray-200 dark:border-gray-700" />

          <!-- Last Sync -->
          <div class="text-center">
            <p class="text-xs text-gray-500 dark:text-gray-400">Last sync</p>
            <p class="text-sm font-medium text-gray-700 dark:text-gray-300">Just now</p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { MainLayout } from '@/components/layout'
import { 
  MessageSquareWarning, 
  AlertTriangle, 
  TrendingUp, 
  Users,
  Shield 
} from 'lucide-vue-next'

// TODO: Phase 4 - Add real data fetching
// - Fetch active sessions from API
// - Poll for updates
// - Fetch system health status
</script>
