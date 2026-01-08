<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Session Detail Page - Comprehensive session view with analysis and history
============================================================================
FILE VERSION: v5.0-5-5.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Back Button & Actions Row -->
    <div class="flex items-center justify-between mb-6">
      <router-link 
        to="/sessions"
        class="inline-flex items-center gap-2 text-sm text-gray-600 dark:text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 transition-colors"
      >
        <ArrowLeft class="w-4 h-4" />
        Back to Sessions
      </router-link>

      <!-- Session Actions -->
      <div v-if="session" class="flex items-center gap-2">
        <!-- Close Session Button -->
        <button
          v-if="session.status === 'active'"
          @click="handleCloseSession"
          :disabled="isClosing"
          class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <XCircle class="w-4 h-4" />
          {{ isClosing ? 'Closing...' : 'Close Session' }}
        </button>

        <!-- Reopen Session Button (Admin) -->
        <button
          v-else-if="session.status === 'closed'"
          @click="handleReopenSession"
          :disabled="isReopening"
          class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-purple-600 dark:text-purple-400 border border-purple-600 dark:border-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RotateCcw class="w-4 h-4" />
          {{ isReopening ? 'Reopening...' : 'Reopen Session' }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="space-y-6">
      <div class="card p-6 animate-pulse">
        <div class="h-8 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4" />
        <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/4" />
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div class="space-y-6">
          <div class="card p-6 h-48 animate-pulse" />
          <div class="card p-6 h-48 animate-pulse" />
        </div>
        <div class="lg:col-span-2 card h-96 animate-pulse" />
      </div>
    </div>

    <!-- Error State -->
    <div 
      v-else-if="error" 
      class="card p-8 text-center"
    >
      <AlertCircle class="w-16 h-16 mx-auto mb-4 text-red-400" />
      <h3 class="text-xl font-semibold text-gray-900 dark:text-white mb-2">
        Failed to Load Session
      </h3>
      <p class="text-gray-600 dark:text-gray-400 mb-4">{{ error }}</p>
      <button 
        @click="loadSession"
        class="px-4 py-2 text-sm font-medium text-white bg-purple-600 hover:bg-purple-700 rounded-lg transition-colors"
      >
        Try Again
      </button>
    </div>

    <!-- Session Content -->
    <template v-else-if="session">
      <!-- Session Header -->
      <div class="card p-6 mb-6">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div>
            <div class="flex items-center gap-3 mb-2">
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ session.discord_username || 'Unknown User' }}
              </h2>
              <SeverityBadge :severity="session.severity" :pulse="session.status === 'active'" />
              <StatusBadge :status="session.status" />
            </div>
            <p class="text-gray-600 dark:text-gray-400">
              Session {{ session.id }}
            </p>
          </div>
          
          <!-- Quick Stats -->
          <div class="flex items-center gap-6">
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ formatScore(session.analysis?.crisis_score) }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400">Crisis Score</p>
            </div>
            <div class="text-center">
              <p class="text-2xl font-bold text-gray-900 dark:text-white">
                {{ session.duration_display || 'Ongoing' }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400">Duration</p>
            </div>
          </div>
        </div>

        <!-- Summary (if available) -->
        <div v-if="session.ash_summary" class="mt-4 p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <p class="text-sm text-gray-700 dark:text-gray-300">{{ session.ash_summary }}</p>
        </div>
      </div>

      <!-- Main Content Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left Column - Info Panels -->
        <div class="space-y-6">
          <!-- User Info -->
          <UserInfoPanel :session="session" />
          
          <!-- User History -->
          <UserHistoryPanel 
            :history="userHistory"
            :loading="isLoadingHistory"
            @view-session="viewHistoricalSession"
            @view-all-history="viewAllHistory"
          />
          
          <!-- Ash Analysis -->
          <AshAnalysisPanel :analysis="session.analysis" />
        </div>

        <!-- Right Column - Notes -->
        <div class="lg:col-span-2">
          <NotesPanel 
            :session="session"
            :notes="session.notes || []"
            :readonly="session.status !== 'active'"
          />
        </div>
      </div>
    </template>

    <!-- Close Session Confirmation Modal -->
    <Teleport to="body">
      <div 
        v-if="showCloseModal" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
        @click.self="showCloseModal = false"
      >
        <div class="w-full max-w-md p-6 rounded-xl bg-white dark:bg-gray-800 shadow-xl">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-2">
            Close Session?
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            This will mark the session as closed and lock all notes. This action can be undone by an administrator.
          </p>
          
          <!-- Optional Summary -->
          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Closing Summary (optional)
            </label>
            <textarea
              v-model="closingSummary"
              rows="3"
              placeholder="Add a brief summary of the session outcome..."
              class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
            />
          </div>
          
          <div class="flex justify-end gap-3">
            <button 
              @click="showCloseModal = false"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button 
              @click="confirmCloseSession"
              :disabled="isClosing"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50"
            >
              {{ isClosing ? 'Closing...' : 'Close Session' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { 
  ArrowLeft, 
  AlertCircle, 
  XCircle, 
  RotateCcw 
} from 'lucide-vue-next'
import { MainLayout } from '@/components/layout'
import { 
  SeverityBadge, 
  StatusBadge,
  UserInfoPanel, 
  AshAnalysisPanel, 
  UserHistoryPanel, 
  NotesPanel 
} from '@/components/sessions'
import { useSessionsStore } from '@/stores'

// Router and Store
const route = useRoute()
const router = useRouter()
const sessionsStore = useSessionsStore()

// Local State
const showCloseModal = ref(false)
const closingSummary = ref('')
const isClosing = ref(false)
const isReopening = ref(false)

// Computed from Store
const session = computed(() => sessionsStore.currentSession)
const userHistory = computed(() => sessionsStore.userHistory)
const isLoading = computed(() => sessionsStore.isLoadingDetail)
const isLoadingHistory = computed(() => sessionsStore.isLoadingHistory)
const error = computed(() => sessionsStore.error)

// Session ID from route
const sessionId = computed(() => route.params.id)

// =============================================================================
// Methods
// =============================================================================

/**
 * Load session data
 */
async function loadSession() {
  try {
    await sessionsStore.fetchSessionDetail(sessionId.value)
    
    // Load user history after session loads
    if (session.value?.discord_user_id) {
      await sessionsStore.fetchUserHistory(
        session.value.discord_user_id,
        sessionId.value // Exclude current session
      )
    }
  } catch (err) {
    console.error('Failed to load session:', err)
  }
}

/**
 * Handle close session button click
 */
function handleCloseSession() {
  closingSummary.value = ''
  showCloseModal.value = true
}

/**
 * Confirm and close session
 */
async function confirmCloseSession() {
  isClosing.value = true
  try {
    await sessionsStore.closeSession(sessionId.value, closingSummary.value || null)
    showCloseModal.value = false
  } catch (err) {
    console.error('Failed to close session:', err)
  } finally {
    isClosing.value = false
  }
}

/**
 * Reopen a closed session
 */
async function handleReopenSession() {
  isReopening.value = true
  try {
    await sessionsStore.reopenSession(sessionId.value)
  } catch (err) {
    console.error('Failed to reopen session:', err)
  } finally {
    isReopening.value = false
  }
}

/**
 * Navigate to a historical session
 */
function viewHistoricalSession(historicalSessionId) {
  router.push({ name: 'session-detail', params: { id: historicalSessionId } })
}

/**
 * View all history for user (could navigate to filtered sessions page)
 */
function viewAllHistory(discordUserId) {
  router.push({ 
    name: 'sessions', 
    query: { search: discordUserId.toString() } 
  })
}

/**
 * Format crisis score for display
 */
function formatScore(score) {
  if (score === null || score === undefined) return '—'
  return score.toFixed(2)
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  loadSession()
})

// Watch for route changes (navigating between sessions)
watch(sessionId, (newId, oldId) => {
  if (newId !== oldId) {
    sessionsStore.clearCurrentSession()
    loadSession()
  }
})
</script>
