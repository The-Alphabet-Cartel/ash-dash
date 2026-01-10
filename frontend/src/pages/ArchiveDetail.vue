<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Archive Detail Page - View decrypted archive contents
============================================================================
FILE VERSION: v5.0-9-9.7-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Back Button -->
    <div class="mb-6">
      <router-link 
        to="/archives"
        class="inline-flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Archives
      </router-link>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="card p-8 text-center">
      <Loader2 class="w-8 h-8 mx-auto mb-3 text-purple-500 animate-spin" />
      <p class="text-gray-500 dark:text-gray-400">Loading and decrypting archive...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="card p-8 text-center">
      <AlertCircle class="w-12 h-12 mx-auto mb-3 text-red-400" />
      <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-2">Failed to Load Archive</h3>
      <p class="text-gray-500 dark:text-gray-400 mb-4">{{ error }}</p>
      <button 
        @click="loadArchive"
        class="px-4 py-2 text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
      >
        Try Again
      </button>
    </div>

    <!-- Archive Content -->
    <template v-else-if="archiveData">
      <!-- Header Card -->
      <div class="card p-6 mb-6">
        <div class="flex items-start justify-between">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <Archive class="w-6 h-6 text-amber-500" />
              <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                {{ archiveData.session?.user_name || 'Unknown User' }}
              </h2>
              <SeverityBadge v-if="archiveData.session?.severity" :severity="archiveData.session.severity" />
            </div>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              Archived on {{ formatDate(archiveData.archived_at) }}
            </p>
          </div>
          <div class="text-right">
            <p class="text-sm text-gray-500 dark:text-gray-400">Archive Version</p>
            <p class="font-mono text-gray-900 dark:text-white">{{ archiveData.version }}</p>
          </div>
        </div>
      </div>

      <!-- Session Details -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div class="card p-4">
          <h3 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-3">Session Info</h3>
          <dl class="space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Session ID</dt>
              <dd class="font-mono text-gray-900 dark:text-white truncate max-w-[150px]">{{ archiveData.session?.session_id }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Discord ID</dt>
              <dd class="font-mono text-gray-900 dark:text-white">{{ archiveData.session?.user_id }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Crisis Score</dt>
              <dd class="text-gray-900 dark:text-white">{{ archiveData.session?.crisis_score?.toFixed(2) || '—' }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Messages</dt>
              <dd class="text-gray-900 dark:text-white">{{ archiveData.session?.message_count || 0 }}</dd>
            </div>
          </dl>
        </div>

        <div class="card p-4">
          <h3 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-3">Timeline</h3>
          <dl class="space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Started</dt>
              <dd class="text-gray-900 dark:text-white">{{ formatDateTime(archiveData.session?.started_at) }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Ended</dt>
              <dd class="text-gray-900 dark:text-white">{{ formatDateTime(archiveData.session?.ended_at) }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Duration</dt>
              <dd class="text-gray-900 dark:text-white">{{ formatDuration(archiveData.session?.duration_seconds) }}</dd>
            </div>
          </dl>
        </div>

        <div class="card p-4">
          <h3 class="text-sm font-semibold text-gray-600 dark:text-gray-400 mb-3">Archive Metadata</h3>
          <dl class="space-y-2 text-sm">
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Archived By</dt>
              <dd class="text-gray-900 dark:text-white">{{ archiveData.metadata?.archived_by_name || 'System' }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Retention</dt>
              <dd class="text-gray-900 dark:text-white capitalize">{{ archiveData.metadata?.retention_tier }}</dd>
            </div>
            <div class="flex justify-between">
              <dt class="text-gray-500 dark:text-gray-400">Notes Count</dt>
              <dd class="text-gray-900 dark:text-white">{{ archiveData.notes?.length || 0 }}</dd>
            </div>
          </dl>
        </div>
      </div>

      <!-- Notes Section -->
      <div class="card">
        <div class="p-4 border-b border-gray-200 dark:border-gray-700">
          <h3 class="font-semibold text-gray-900 dark:text-white">Archived Notes</h3>
        </div>
        
        <div v-if="archiveData.notes?.length === 0" class="p-8 text-center">
          <FileText class="w-12 h-12 mx-auto mb-3 text-gray-400" />
          <p class="text-gray-500 dark:text-gray-400">No notes were archived with this session.</p>
        </div>

        <div v-else class="divide-y divide-gray-200 dark:divide-gray-700">
          <div 
            v-for="note in archiveData.notes" 
            :key="note.id"
            class="p-4"
          >
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm font-medium text-gray-900 dark:text-white">
                Note from {{ formatDateTime(note.created_at) }}
              </span>
              <span v-if="note.is_locked" class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
                <Lock class="w-3 h-3" />
                Locked
              </span>
            </div>
            <div 
              v-if="note.content_html"
              class="prose prose-sm dark:prose-invert max-w-none"
              v-html="note.content_html"
            />
            <p v-else class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
              {{ note.content }}
            </p>
          </div>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ArrowLeft, Archive, Loader2, AlertCircle, Lock, FileText } from 'lucide-vue-next'
import { MainLayout } from '@/components/layout'
import { SeverityBadge } from '@/components/sessions'
import { useArchivesStore } from '@/stores'

const route = useRoute()
const archivesStore = useArchivesStore()

// State
const isLoading = ref(false)
const error = ref(null)

// Computed
const archiveId = computed(() => route.params.id)
const archiveData = computed(() => archivesStore.currentArchivePackage)

// Methods
async function loadArchive() {
  isLoading.value = true
  error.value = null
  
  try {
    await archivesStore.downloadArchive(archiveId.value)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load archive'
  } finally {
    isLoading.value = false
  }
}

function formatDate(dateString) {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'long',
    day: 'numeric',
    year: 'numeric',
  })
}

function formatDateTime(dateString) {
  if (!dateString) return '—'
  return new Date(dateString).toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
  })
}

function formatDuration(seconds) {
  if (!seconds) return '—'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  if (hours > 0) {
    return `${hours}h ${minutes}m`
  }
  return `${minutes}m`
}

// Lifecycle
onMounted(() => {
  loadArchive()
})
</script>
