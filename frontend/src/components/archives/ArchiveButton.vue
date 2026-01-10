<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
ArchiveButton - Button to archive a session with confirmation dialog
============================================================================
FILE VERSION: v5.0-9-9.5-1
LAST MODIFIED: 2026-01-09
PHASE: Phase 9 - Archive System Implementation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div>
    <!-- Archive Button -->
    <button
      @click="handleClick"
      :disabled="!canArchive || isArchiving || isAlreadyArchived"
      :class="[
        'inline-flex items-center gap-2 font-medium rounded-lg transition-colors',
        sizeClasses,
        canArchive && !isAlreadyArchived
          ? 'bg-amber-600 hover:bg-amber-700 text-white'
          : 'bg-gray-600 text-gray-400 cursor-not-allowed',
      ]"
      :title="buttonTitle"
    >
      <Archive v-if="!isArchiving" :class="iconSizeClasses" />
      <Loader2 v-else :class="[iconSizeClasses, 'animate-spin']" />
      <span v-if="!iconOnly">{{ buttonText }}</span>
    </button>

    <!-- Confirmation Dialog -->
    <Teleport to="body">
      <div 
        v-if="showDialog" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
        @click.self="showDialog = false"
      >
        <div class="w-full max-w-md rounded-xl bg-white dark:bg-gray-800 shadow-xl overflow-hidden">
          <!-- Header -->
          <div class="px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center gap-3">
              <div class="flex-shrink-0 p-2 rounded-full bg-amber-100 dark:bg-amber-900/30">
                <Archive class="w-5 h-5 text-amber-600 dark:text-amber-400" />
              </div>
              <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                Archive Session
              </h3>
            </div>
          </div>

          <!-- Body -->
          <div class="px-6 py-4 space-y-4">
            <p class="text-sm text-gray-600 dark:text-gray-400">
              This will securely encrypt and archive session 
              <code class="px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-sm font-mono">
                {{ sessionId }}
              </code>
              for long-term storage.
            </p>

            <!-- Retention Tier Selection -->
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Retention Period
              </label>
              <div class="space-y-2">
                <!-- Standard Option -->
                <label 
                  class="flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors"
                  :class="retentionTier === 'standard' 
                    ? 'border-amber-500 bg-amber-50 dark:bg-amber-900/20' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                >
                  <input 
                    type="radio" 
                    v-model="retentionTier" 
                    value="standard"
                    class="mt-1 text-amber-600 focus:ring-amber-500"
                  />
                  <div>
                    <span class="block font-medium text-gray-900 dark:text-white">
                      Standard
                    </span>
                    <span class="block text-sm text-gray-500 dark:text-gray-400">
                      Retained for 1 year, then automatically deleted
                    </span>
                  </div>
                </label>

                <!-- Permanent Option -->
                <label 
                  class="flex items-start gap-3 p-3 rounded-lg border cursor-pointer transition-colors"
                  :class="retentionTier === 'permanent' 
                    ? 'border-amber-500 bg-amber-50 dark:bg-amber-900/20' 
                    : 'border-gray-200 dark:border-gray-700 hover:border-gray-300 dark:hover:border-gray-600'"
                >
                  <input 
                    type="radio" 
                    v-model="retentionTier" 
                    value="permanent"
                    class="mt-1 text-amber-600 focus:ring-amber-500"
                  />
                  <div>
                    <span class="block font-medium text-gray-900 dark:text-white">
                      Permanent
                    </span>
                    <span class="block text-sm text-gray-500 dark:text-gray-400">
                      Retained for 7 years, requires manual deletion
                    </span>
                  </div>
                </label>
              </div>
            </div>

            <!-- Warning -->
            <div class="flex items-start gap-3 p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
              <Info class="w-5 h-5 text-blue-600 dark:text-blue-400 flex-shrink-0 mt-0.5" />
              <p class="text-sm text-blue-700 dark:text-blue-300">
                The session data and all notes will be encrypted before storage. 
                The archive can be retrieved and decrypted later if needed.
              </p>
            </div>

            <!-- Error Message -->
            <div 
              v-if="archiveError" 
              class="flex items-start gap-3 p-3 rounded-lg bg-red-50 dark:bg-red-900/20"
            >
              <AlertCircle class="w-5 h-5 text-red-600 dark:text-red-400 flex-shrink-0 mt-0.5" />
              <p class="text-sm text-red-700 dark:text-red-300">
                {{ archiveError }}
              </p>
            </div>
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 bg-gray-50 dark:bg-gray-900/50 flex justify-end gap-3">
            <button 
              @click="showDialog = false"
              :disabled="isArchiving"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50"
            >
              Cancel
            </button>
            <button 
              @click="confirmArchive"
              :disabled="isArchiving"
              class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-amber-600 hover:bg-amber-700 rounded-lg transition-colors disabled:opacity-50"
            >
              <Loader2 v-if="isArchiving" class="w-4 h-4 animate-spin" />
              <Archive v-else class="w-4 h-4" />
              {{ isArchiving ? 'Archiving...' : 'Archive Session' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Archive, Loader2, Info, AlertCircle } from 'lucide-vue-next'
import { useArchivesStore } from '@/stores'

const props = defineProps({
  sessionId: {
    type: String,
    required: true,
  },
  sessionStatus: {
    type: String,
    required: true,
  },
  size: {
    type: String,
    default: 'md',
    validator: (v) => ['sm', 'md', 'lg'].includes(v),
  },
  iconOnly: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['archived'])

// Store
const archivesStore = useArchivesStore()

// Local state
const showDialog = ref(false)
const retentionTier = ref('standard')
const archiveError = ref(null)
const isAlreadyArchived = ref(false)

// Computed
const isArchiving = computed(() => archivesStore.isArchiving)

const canArchive = computed(() => {
  // Can only archive closed sessions
  return props.sessionStatus === 'closed'
})

const buttonTitle = computed(() => {
  if (isAlreadyArchived.value) {
    return 'Session already archived'
  }
  if (props.sessionStatus === 'active') {
    return 'Close the session before archiving'
  }
  if (props.sessionStatus === 'archived') {
    return 'Session is already archived'
  }
  return 'Archive this session'
})

const buttonText = computed(() => {
  if (isArchiving.value) return 'Archiving...'
  if (isAlreadyArchived.value) return 'Archived'
  return 'Archive'
})

const sizeClasses = computed(() => {
  if (props.iconOnly) {
    switch (props.size) {
      case 'sm': return 'p-1.5'
      case 'lg': return 'p-3'
      default: return 'p-2'
    }
  }
  switch (props.size) {
    case 'sm': return 'px-3 py-1.5 text-sm'
    case 'lg': return 'px-5 py-2.5 text-base'
    default: return 'px-4 py-2 text-sm'
  }
})

const iconSizeClasses = computed(() => {
  switch (props.size) {
    case 'sm': return 'w-3.5 h-3.5'
    case 'lg': return 'w-5 h-5'
    default: return 'w-4 h-4'
  }
})

// Methods
function handleClick() {
  if (!canArchive.value || isAlreadyArchived.value) return
  archiveError.value = null
  retentionTier.value = 'standard'
  showDialog.value = true
}

async function confirmArchive() {
  archiveError.value = null
  
  try {
    const result = await archivesStore.archiveSession(
      props.sessionId,
      retentionTier.value
    )
    
    showDialog.value = false
    isAlreadyArchived.value = true
    emit('archived', result)
  } catch (err) {
    archiveError.value = err.response?.data?.detail || 'Failed to archive session'
  }
}

async function checkArchiveStatus() {
  try {
    const status = await archivesStore.checkSessionArchived(props.sessionId)
    isAlreadyArchived.value = status.is_archived
  } catch (err) {
    // Silently fail - assume not archived
    isAlreadyArchived.value = false
  }
}

// Check status on mount
onMounted(() => {
  checkArchiveStatus()
})
</script>
