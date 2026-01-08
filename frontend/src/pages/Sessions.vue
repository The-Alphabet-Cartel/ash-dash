<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Sessions Page - Session list with search, filters, and pagination
============================================================================
FILE VERSION: v5.0-5-5.4-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Page Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Session History</h2>
      <p class="text-gray-600 dark:text-gray-400">Browse and search crisis sessions</p>
    </div>

    <!-- Filters Card -->
    <div class="card p-4 mb-6">
      <div class="flex flex-wrap items-center gap-4">
        <!-- Search Input -->
        <div class="flex-1 min-w-[250px]">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              v-model="searchInput"
              type="text"
              placeholder="Search by Discord ID, username, or session ID..."
              class="w-full pl-10 pr-10 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              @input="debouncedSearch"
            />
            <!-- Clear search button -->
            <button
              v-if="searchInput"
              @click="clearSearch"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
            >
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>
        
        <!-- Severity Filter -->
        <select 
          v-model="severityFilter"
          @change="handleSeverityChange"
          class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value="">All Severities</option>
          <option value="critical">🟣 Critical</option>
          <option value="high">🔴 High</option>
          <option value="medium">🟡 Medium</option>
          <option value="low">🟢 Low</option>
          <option value="safe">⚪ Safe</option>
        </select>

        <!-- Status Filter -->
        <select 
          v-model="statusFilter"
          @change="handleStatusChange"
          class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="closed">Closed</option>
          <option value="archived">Archived</option>
        </select>

        <!-- Date From -->
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600 dark:text-gray-400 whitespace-nowrap">From:</label>
          <input
            v-model="dateFrom"
            type="date"
            @change="handleDateChange"
            class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        <!-- Date To -->
        <div class="flex items-center gap-2">
          <label class="text-sm text-gray-600 dark:text-gray-400 whitespace-nowrap">To:</label>
          <input
            v-model="dateTo"
            type="date"
            @change="handleDateChange"
            class="px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          />
        </div>

        <!-- Clear Filters Button -->
        <button
          v-if="sessionsStore.hasFilters"
          @click="clearAllFilters"
          class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <FilterX class="w-4 h-4" />
          Clear Filters
        </button>

        <!-- Refresh Button -->
        <button
          @click="refresh"
          :disabled="sessionsStore.isLoading"
          class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300 hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded-lg transition-colors disabled:opacity-50"
        >
          <RefreshCw :class="['w-4 h-4', sessionsStore.isLoading ? 'animate-spin' : '']" />
          Refresh
        </button>
      </div>

      <!-- Active Filters Summary -->
      <div v-if="sessionsStore.filterSummary" class="mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
        <p class="text-sm text-gray-500 dark:text-gray-400">
          <span class="font-medium">Active filters:</span> {{ sessionsStore.filterSummary }}
        </p>
      </div>
    </div>

    <!-- Error Banner -->
    <div 
      v-if="sessionsStore.error" 
      class="mb-6 p-4 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800"
    >
      <div class="flex items-center gap-3">
        <AlertCircle class="w-5 h-5 text-red-500 flex-shrink-0" />
        <p class="text-sm text-red-700 dark:text-red-300">{{ sessionsStore.error }}</p>
        <button 
          @click="refresh" 
          class="ml-auto text-sm font-medium text-red-600 dark:text-red-400 hover:underline"
        >
          Retry
        </button>
      </div>
    </div>

    <!-- Sessions Table -->
    <SessionsTable
      :sessions="sessionsStore.sessions"
      :total="sessionsStore.total"
      :loading="sessionsStore.isLoading"
      :empty-message="emptyMessage"
      @row-click="viewSession"
    />

    <!-- Pagination -->
    <div v-if="sessionsStore.total > 0" class="mt-6">
      <Pagination
        :current-page="sessionsStore.currentPage"
        :total-pages="sessionsStore.totalPages"
        :total="sessionsStore.total"
        :page-size="sessionsStore.pageSize"
        @page-change="handlePageChange"
        @page-size-change="handlePageSizeChange"
      />
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Search, X, RefreshCw, FilterX, AlertCircle } from 'lucide-vue-next'
import { MainLayout } from '@/components/layout'
import { SessionsTable, Pagination } from '@/components/sessions'
import { useSessionsStore } from '@/stores'

// Router and Store
const router = useRouter()
const route = useRoute()
const sessionsStore = useSessionsStore()

// Local filter state (for inputs)
const searchInput = ref('')
const severityFilter = ref('')
const statusFilter = ref('')
const dateFrom = ref('')
const dateTo = ref('')

// Debounce timer
let searchTimeout = null

// =============================================================================
// Computed
// =============================================================================

const emptyMessage = computed(() => {
  if (sessionsStore.hasFilters) {
    return 'No sessions match your current filters. Try adjusting your search criteria.'
  }
  return 'No sessions have been recorded yet. Sessions will appear here once Ash-Bot begins detecting crisis events.'
})

// =============================================================================
// Methods
// =============================================================================

/**
 * Debounced search handler
 */
function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    sessionsStore.setSearch(searchInput.value)
    sessionsStore.fetchSessions()
  }, 300)
}

/**
 * Clear search input
 */
function clearSearch() {
  searchInput.value = ''
  sessionsStore.setSearch('')
  sessionsStore.fetchSessions()
}

/**
 * Handle severity filter change
 */
function handleSeverityChange() {
  sessionsStore.setSeverity(severityFilter.value)
}

/**
 * Handle status filter change
 */
function handleStatusChange() {
  sessionsStore.setStatus(statusFilter.value)
}

/**
 * Handle date range change
 */
function handleDateChange() {
  const from = dateFrom.value ? new Date(dateFrom.value).toISOString() : null
  const to = dateTo.value ? new Date(dateTo.value + 'T23:59:59').toISOString() : null
  sessionsStore.setDateRange(from, to)
}

/**
 * Clear all filters
 */
function clearAllFilters() {
  searchInput.value = ''
  severityFilter.value = ''
  statusFilter.value = ''
  dateFrom.value = ''
  dateTo.value = ''
  sessionsStore.clearFilters()
}

/**
 * Refresh sessions
 */
function refresh() {
  sessionsStore.fetchSessions()
}

/**
 * Handle page change
 */
function handlePageChange(page) {
  sessionsStore.setPage(page)
}

/**
 * Handle page size change
 */
function handlePageSizeChange(size) {
  sessionsStore.setPageSize(size)
}

/**
 * Navigate to session detail
 */
function viewSession(session) {
  router.push({ name: 'session-detail', params: { id: session.id } })
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  // Check for search query parameter
  if (route.query.search) {
    searchInput.value = route.query.search
    sessionsStore.setSearch(route.query.search)
  } else {
    // Sync local state with store
    searchInput.value = sessionsStore.filters.search
  }
  
  severityFilter.value = sessionsStore.filters.severity
  statusFilter.value = sessionsStore.filters.status
  
  // Fetch sessions on mount
  sessionsStore.fetchSessions()
})
</script>
