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
Audit Logs Page - View system action history
----------------------------------------------------------------------------
FILE VERSION: v5.0-11-11.3-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation (ARIA)
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="audit-logs">
    <!-- Header with Filters -->
    <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Audit Logs
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          {{ total }} total entries
        </p>
      </div>
      
      <!-- Filters -->
      <div class="flex flex-wrap items-center gap-3">
        <!-- Action Filter -->
        <select
          v-model="filters.action"
          aria-label="Filter by action type"
          class="rounded-lg border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white text-sm"
        >
          <option value="">All Actions</option>
          <optgroup label="Notes">
            <option value="note.create">Note Created</option>
            <option value="note.update">Note Updated</option>
            <option value="note.delete">Note Deleted</option>
            <option value="note.lock">Note Locked</option>
          </optgroup>
          <optgroup label="Sessions">
            <option value="session.close">Session Closed</option>
            <option value="session.reopen">Session Reopened</option>
            <option value="session.assign">Session Assigned</option>
          </optgroup>
          <optgroup label="Archives">
            <option value="archive.create">Archive Created</option>
            <option value="archive.delete">Archive Deleted</option>
            <option value="archive.cleanup">Cleanup Executed</option>
          </optgroup>
          <optgroup label="Users">
            <option value="user.create">User Created</option>
            <option value="user.login">User Login</option>
          </optgroup>
        </select>
        
        <!-- Refresh Button -->
        <button
          @click="fetchLogs"
          :disabled="isLoading"
          aria-label="Refresh audit logs"
          class="btn-secondary flex items-center gap-2"
        >
          <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': isLoading }" aria-hidden="true" />
          Refresh
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && logs.length === 0" class="flex justify-center py-12" role="status" aria-label="Loading audit logs">
      <Loader2 class="w-8 h-8 animate-spin text-purple-500" aria-hidden="true" />
    </div>

    <!-- Error State -->
    <div 
      v-else-if="error" 
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
      role="alert"
    >
      <div class="flex items-center gap-2 text-red-600 dark:text-red-400">
        <AlertCircle class="w-5 h-5" aria-hidden="true" />
        <p>{{ error }}</p>
      </div>
    </div>

    <!-- Logs Table -->
    <div v-else class="card overflow-hidden">
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Timestamp
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              User
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Action
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Entity
            </th>
            <th scope="col" class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
              Details
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="log in logs" 
            :key="log.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
          >
            <!-- Timestamp -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
              <div>{{ formatDate(log.created_at) }}</div>
              <div class="text-xs text-gray-400 dark:text-gray-500">
                {{ formatTime(log.created_at) }}
              </div>
            </td>
            
            <!-- User -->
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span 
                v-if="log.user_name"
                class="text-gray-900 dark:text-white"
              >
                {{ log.user_name }}
              </span>
              <span 
                v-else 
                class="text-gray-400 dark:text-gray-500 italic"
              >
                System
              </span>
            </td>
            
            <!-- Action Badge -->
            <td class="px-6 py-4 whitespace-nowrap">
              <ActionBadge :action="log.action" />
            </td>
            
            <!-- Entity -->
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <span class="text-gray-700 dark:text-gray-300">
                {{ formatEntityType(log.entity_type) }}
              </span>
              <span 
                v-if="log.entity_id" 
                class="text-gray-400 dark:text-gray-500 ml-1"
              >
                #{{ log.entity_id.slice(0, 8) }}
              </span>
            </td>
            
            <!-- Details Button -->
            <td class="px-6 py-4 whitespace-nowrap text-sm">
              <button
                v-if="hasDetails(log)"
                @click="showDetails(log)"
                class="text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300 hover:underline"
              >
                View
              </button>
              <span v-else class="text-gray-400 dark:text-gray-500">—</span>
            </td>
          </tr>
          
          <!-- Empty State -->
          <tr v-if="logs.length === 0">
            <td colspan="5" class="px-6 py-12 text-center">
              <FileText class="w-12 h-12 mx-auto text-gray-300 dark:text-gray-600 mb-3" />
              <p class="text-gray-500 dark:text-gray-400">No audit logs found</p>
              <p v-if="filters.action" class="text-sm text-gray-400 dark:text-gray-500 mt-1">
                Try clearing the filter
              </p>
            </td>
          </tr>
        </tbody>
      </table>
      
      <!-- Pagination -->
      <div 
        v-if="totalPages > 1"
        class="flex items-center justify-between px-6 py-3 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800"
      >
        <div class="text-sm text-gray-500 dark:text-gray-400">
          Page {{ page }} of {{ totalPages }}
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="goToPage(page - 1)"
            :disabled="page <= 1"
            class="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <ChevronLeft class="w-4 h-4" />
          </button>
          <button
            @click="goToPage(page + 1)"
            :disabled="page >= totalPages"
            class="px-3 py-1 rounded border border-gray-300 dark:border-gray-600 text-sm disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            <ChevronRight class="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
    
    <!-- Details Modal -->
    <Teleport to="body">
      <div 
        v-if="selectedLog"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
      >
        <!-- Backdrop -->
        <div 
          class="absolute inset-0 bg-black/50"
          @click="selectedLog = null"
        />
        
        <!-- Modal -->
        <div class="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] overflow-hidden">
          <!-- Header -->
          <div class="flex items-center justify-between px-6 py-4 border-b border-gray-200 dark:border-gray-700">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
              Audit Log Details
            </h3>
            <button
              @click="selectedLog = null"
              class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
            >
              <X class="w-5 h-5" />
            </button>
          </div>
          
          <!-- Content -->
          <div class="p-6 overflow-y-auto max-h-[60vh] space-y-4">
            <!-- Summary -->
            <div class="grid grid-cols-2 gap-4 text-sm">
              <div>
                <dt class="text-gray-500 dark:text-gray-400">Action</dt>
                <dd class="mt-1">
                  <ActionBadge :action="selectedLog.action" />
                </dd>
              </div>
              <div>
                <dt class="text-gray-500 dark:text-gray-400">Timestamp</dt>
                <dd class="mt-1 text-gray-900 dark:text-white">
                  {{ formatDateTime(selectedLog.created_at) }}
                </dd>
              </div>
              <div>
                <dt class="text-gray-500 dark:text-gray-400">User</dt>
                <dd class="mt-1 text-gray-900 dark:text-white">
                  {{ selectedLog.user_name || 'System' }}
                </dd>
              </div>
              <div>
                <dt class="text-gray-500 dark:text-gray-400">Entity</dt>
                <dd class="mt-1 text-gray-900 dark:text-white">
                  {{ formatEntityType(selectedLog.entity_type) }}
                  <span v-if="selectedLog.entity_id" class="text-gray-500">
                    ({{ selectedLog.entity_id }})
                  </span>
                </dd>
              </div>
            </div>
            
            <!-- Old Values -->
            <div v-if="selectedLog.old_values && Object.keys(selectedLog.old_values).length > 0">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Previous Values
              </h4>
              <pre class="bg-gray-100 dark:bg-gray-900 rounded p-3 text-xs overflow-x-auto">{{ JSON.stringify(selectedLog.old_values, null, 2) }}</pre>
            </div>
            
            <!-- New Values -->
            <div v-if="selectedLog.new_values && Object.keys(selectedLog.new_values).length > 0">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                New Values
              </h4>
              <pre class="bg-gray-100 dark:bg-gray-900 rounded p-3 text-xs overflow-x-auto">{{ JSON.stringify(selectedLog.new_values, null, 2) }}</pre>
            </div>
            
            <!-- IP Address -->
            <div v-if="selectedLog.ip_address">
              <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                IP Address
              </h4>
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ selectedLog.ip_address }}
              </p>
            </div>
          </div>
          
          <!-- Footer -->
          <div class="flex justify-end px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
            <button
              @click="selectedLog = null"
              class="btn-secondary"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
/**
 * Audit Logs Page
 * 
 * Displays system audit logs with:
 * - Timestamp, user, action, entity
 * - Filtering by action type
 * - Pagination
 * - Details modal showing old/new values
 * 
 * Authorization: Lead or Admin only (enforced by route guard)
 */

import { ref, reactive, onMounted, watch } from 'vue'
import { 
  Loader2, 
  RefreshCw, 
  AlertCircle, 
  FileText,
  ChevronLeft,
  ChevronRight,
  X,
} from 'lucide-vue-next'
import { adminApi } from '@/services/api'
import { ActionBadge } from '@/components/admin'
import { format } from 'date-fns'

// =============================================================================
// State
// =============================================================================

const logs = ref([])
const isLoading = ref(true)
const error = ref(null)
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const totalPages = ref(1)
const selectedLog = ref(null)

const filters = reactive({
  action: '',
})

// =============================================================================
// API Methods
// =============================================================================

/**
 * Fetch audit logs from API
 */
async function fetchLogs() {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await adminApi.getAuditLogs({
      page: page.value,
      page_size: pageSize.value,
      action: filters.action || undefined,
    })
    
    logs.value = response.data.logs
    total.value = response.data.total
    totalPages.value = response.data.total_pages
  } catch (err) {
    console.error('Failed to fetch audit logs:', err)
    error.value = err.response?.data?.detail || 'Failed to load audit logs'
  } finally {
    isLoading.value = false
  }
}

// =============================================================================
// Pagination
// =============================================================================

function goToPage(newPage) {
  if (newPage < 1 || newPage > totalPages.value) return
  page.value = newPage
  fetchLogs()
}

// =============================================================================
// Watch Filters
// =============================================================================

watch(() => filters.action, () => {
  page.value = 1 // Reset to first page on filter change
  fetchLogs()
})

// =============================================================================
// Helpers
// =============================================================================

/**
 * Format date for display
 */
function formatDate(dateStr) {
  try {
    return format(new Date(dateStr), 'MMM d, yyyy')
  } catch {
    return 'Unknown'
  }
}

/**
 * Format time for display
 */
function formatTime(dateStr) {
  try {
    return format(new Date(dateStr), 'HH:mm:ss')
  } catch {
    return ''
  }
}

/**
 * Format full datetime for modal
 */
function formatDateTime(dateStr) {
  try {
    return format(new Date(dateStr), 'MMM d, yyyy HH:mm:ss')
  } catch {
    return 'Unknown'
  }
}

/**
 * Format entity type for display
 */
function formatEntityType(type) {
  if (!type) return 'System'
  return type.charAt(0).toUpperCase() + type.slice(1)
}

/**
 * Check if log has viewable details
 */
function hasDetails(log) {
  return (
    (log.old_values && Object.keys(log.old_values).length > 0) ||
    (log.new_values && Object.keys(log.new_values).length > 0) ||
    log.ip_address
  )
}

/**
 * Show details modal for a log entry
 */
function showDetails(log) {
  selectedLog.value = log
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(fetchLogs)
</script>
