<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
NotesPanel - Session notes display and editor (Phase 6 placeholder)
============================================================================
FILE VERSION: v5.0-5-5.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management (Editor in Phase 6)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="card h-full flex flex-col">
    <!-- Header -->
    <div class="p-6 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <FileText class="w-5 h-5 text-purple-500" />
            CRT Notes
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ noteCount }} note{{ noteCount !== 1 ? 's' : '' }}
          </p>
        </div>
        
        <!-- Lock Status -->
        <div v-if="readonly" class="flex items-center gap-1 text-gray-400 dark:text-gray-500">
          <Lock class="w-4 h-4" />
          <span class="text-xs">Locked</span>
        </div>
      </div>
    </div>

    <!-- Notes List -->
    <div class="flex-1 overflow-y-auto p-6">
      <!-- Loading -->
      <div v-if="loading" class="space-y-4 animate-pulse">
        <div class="h-20 bg-gray-200 dark:bg-gray-700 rounded" />
        <div class="h-20 bg-gray-200 dark:bg-gray-700 rounded" />
      </div>

      <!-- Empty State -->
      <div v-else-if="notes.length === 0" class="text-center py-12">
        <FileText class="w-12 h-12 mx-auto mb-4 text-gray-300 dark:text-gray-600" />
        <p class="text-gray-500 dark:text-gray-400 mb-2">No notes yet</p>
        <p class="text-xs text-gray-400 dark:text-gray-500">
          Notes editor coming in Phase 6
        </p>
      </div>

      <!-- Notes -->
      <div v-else class="space-y-4">
        <div 
          v-for="note in notes" 
          :key="note.id"
          class="p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600"
        >
          <!-- Note Header -->
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <div class="w-6 h-6 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                <span class="text-xs font-medium text-purple-600 dark:text-purple-400">
                  {{ getInitials(note.author_name) }}
                </span>
              </div>
              <span class="text-sm font-medium text-gray-900 dark:text-white">
                {{ note.author_name || 'Unknown' }}
              </span>
            </div>
            <div class="flex items-center gap-2">
              <Lock v-if="note.is_locked" class="w-3 h-3 text-gray-400" />
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatDate(note.created_at) }}
              </span>
            </div>
          </div>

          <!-- Note Content -->
          <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
            {{ note.content_preview }}
          </p>
        </div>
      </div>
    </div>

    <!-- Add Note Button (Phase 6) -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700">
      <button 
        :disabled="readonly"
        class="w-full py-2 px-4 rounded-lg text-sm font-medium bg-purple-600 text-white hover:bg-purple-700 disabled:bg-gray-300 dark:disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors"
      >
        <span class="flex items-center justify-center gap-2">
          <Plus class="w-4 h-4" />
          Add Note
        </span>
      </button>
      <p v-if="readonly" class="text-xs text-center text-gray-400 dark:text-gray-500 mt-2">
        Session is {{ session?.status }} - notes are locked
      </p>
      <p v-else class="text-xs text-center text-gray-400 dark:text-gray-500 mt-2">
        Full editor coming in Phase 6
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { FileText, Lock, Plus } from 'lucide-vue-next'

const props = defineProps({
  session: {
    type: Object,
    default: null
  },
  notes: {
    type: Array,
    default: () => []
  },
  loading: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  }
})

const noteCount = computed(() => props.notes?.length || 0)

function getInitials(name) {
  if (!name) return '?'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}
</script>
