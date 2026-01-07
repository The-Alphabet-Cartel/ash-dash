<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Documentation Page - Wiki and training materials
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
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Documentation</h2>
      <p class="text-gray-600 dark:text-gray-400">CRT training materials and reference guides</p>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Sidebar Navigation -->
      <div class="card p-4">
        <h3 class="text-sm font-semibold text-gray-900 dark:text-white mb-4 px-2">Categories</h3>
        <nav class="space-y-1">
          <a 
            href="#" 
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-900/30"
          >
            <BookOpen class="w-4 h-4" />
            Getting Started
          </a>
          <a 
            href="#" 
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <Shield class="w-4 h-4" />
            CRT Protocols
          </a>
          <a 
            href="#" 
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <AlertTriangle class="w-4 h-4" />
            Crisis Response
          </a>
          <a 
            href="#" 
            class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            <Settings class="w-4 h-4" />
            Technical Reference
          </a>
        </nav>
      </div>

      <!-- Content Area -->
      <div class="lg:col-span-3 card">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Getting Started</h3>
            <button class="inline-flex items-center gap-2 px-3 py-1.5 text-sm rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
              <Download class="w-4 h-4" />
              PDF
            </button>
          </div>
        </div>
        
        <!-- Empty State -->
        <div class="flex flex-col items-center justify-center py-16 text-center">
          <div class="w-16 h-16 rounded-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center mb-4">
            <FileText class="w-8 h-8 text-gray-400 dark:text-gray-500" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">Documentation Coming Soon</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">
            The wiki system will render Markdown files from the docs/ directory with navigation, search, and PDF export.
          </p>
          <p class="mt-4 text-xs text-gray-400 dark:text-gray-500">
            Coming in Phase 7
          </p>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { MainLayout } from '@/components/layout'
import { BookOpen, Shield, AlertTriangle, Settings, FileText, Download } from 'lucide-vue-next'

// TODO: Phase 7 - Add:
// - Markdown file scanning
// - Category navigation
// - Search functionality
// - PDF export
</script>
