<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Archives Page - Browse and manage encrypted session archives
============================================================================
FILE VERSION: v5.0-11-11.2-1
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Page Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Session Archives</h2>
      <p class="text-gray-600 dark:text-gray-400">Encrypted long-term storage of completed sessions</p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <!-- Total Archives -->
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-lg bg-amber-100 dark:bg-amber-900/30">
            <Archive class="w-5 h-5 text-amber-600 dark:text-amber-400" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ isLoadingStats ? '...' : statistics?.total_archives || 0 }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Total Archives</p>
          </div>
        </div>
      </div>

      <!-- Total Size -->
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-lg bg-blue-100 dark:bg-blue-900/30">
            <HardDrive class="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ isLoadingStats ? '...' : formatSize(statistics?.total_size_bytes) }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Storage Used</p>
          </div>
        </div>
      </div>

      <!-- Permanent Archives -->
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-lg bg-purple-100 dark:bg-purple-900/30">
            <Lock class="w-5 h-5 text-purple-600 dark:text-purple-400" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ isLoadingStats ? '...' : statistics?.by_retention_tier?.permanent?.count || 0 }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Permanent</p>
          </div>
        </div>
      </div>

      <!-- Expiring Soon -->
      <div class="card p-4">
        <div class="flex items-center gap-3">
          <div class="p-2 rounded-lg" :class="expiringCount > 0 ? 'bg-red-100 dark:bg-red-900/30' : 'bg-green-100 dark:bg-green-900/30'">
            <Clock class="w-5 h-5" :class="expiringCount > 0 ? 'text-red-600 dark:text-red-400' : 'text-green-600 dark:text-green-400'" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900 dark:text-white">
              {{ isLoadingExpiring ? '...' : expiringCount }}
            </p>
            <p class="text-xs text-gray-500 dark:text-gray-400">Expiring (30d)</p>
          </div>
        </div>
      </div>
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
              placeholder="Search by Discord ID or username..."
              class="w-full pl-10 pr-10 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent"
              @input="debouncedSearch"
            />
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
          @change="handleFilterChange"
          class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value="">All Severities</option>
          <option value="critical">🟣 Critical</option>
          <option value="high">🔴 High</option>
          <option value="medium">🟡 Medium</option>
          <option value="low">🟢 Low</option>
          <option value="safe">⚪ Safe</option>
        </select>

        <!-- Retention Tier Filter -->
        <select 
          v-model="retentionFilter"
          @change="handleFilterChange"
          class="px-4 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
        >
          <option value="">All Retention Tiers</option>
          <option value="standard">📅 Standard (1 year)</option>
          <option value="permanent">🔒 Permanent (7 years)</option>
        </select>

        <!-- Clear Filters Button -->
        <button
          v-if="hasActiveFilters"
          @click="clearAllFilters"
          class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
        >
          <FilterX class="w-4 h-4" />
          Clear Filters
        </button>

        <!-- Refresh Button -->
        <button
          @click="refresh"
          :disabled="isLoading"
          class="flex items-center gap-2 px-4 py-2 text-sm font-medium text-purple-600 dark:text-purple-400 hover:text-purple-800 dark:hover:text-purple-300 hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded-lg transition-colors disabled:opacity-50"
        >
          <RefreshCw :class="['w-4 h-4', isLoading ? 'animate-spin' : '']" />
          Refresh
        </button>
      </div>
    </div>

    <!-- Error Banner -->
    <ErrorMessage
      v-if="error"
      class="mb-6"
      title="Unable to load archives"
      :message="error"
      @retry="refresh"
    />

    <!-- Archives Table -->
    <div class="card overflow-hidden">
      <!-- Loading State -->
      <SkeletonList 
        v-if="isLoading && archives.length === 0"
        :rows="8"
        show-indicator
        show-action
        class="p-4"
      />

      <!-- Empty State -->
      <EmptyState
        v-else-if="archives.length === 0 && !error"
        :variant="hasActiveFilters ? 'filter' : 'archive'"
        :title="hasActiveFilters ? 'No archives match your filters' : 'No archives yet'"
        :message="hasActiveFilters 
          ? 'Try adjusting your search criteria.' 
          : 'Archived sessions will appear here. Close and archive sessions to preserve them.'"
        :action-label="hasActiveFilters ? 'Clear filters' : null"
        @action="clearAllFilters"
      />

      <!-- Table -->
      <table v-else-if="archives.length > 0" class="w-full">
        <thead class="bg-gray-50 dark:bg-gray-800/50">
          <tr>
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              User
            </th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              Session
            </th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              Severity
            </th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              Archived
            </th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              Retention
            </th>
            <th class="px-4 py-3 text-left text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              Size
            </th>
            <th class="px-4 py-3 text-right text-xs font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="archive in archives" 
            :key="archive.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
          >
            <!-- User -->
            <td class="px-4 py-3">
              <div>
                <p class="font-medium text-gray-900 dark:text-white">
                  {{ archive.discord_user_name || 'Unknown User' }}
                </p>
                <p class="text-xs text-gray-500 dark:text-gray-400 font-mono">
                  {{ archive.discord_user_id }}
                </p>
              </div>
            </td>

            <!-- Session ID -->
            <td class="px-4 py-3">
              <p class="text-sm text-gray-600 dark:text-gray-400 font-mono truncate max-w-[150px]" :title="archive.session_id">
                {{ archive.session_id }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                {{ archive.notes_count }} note{{ archive.notes_count !== 1 ? 's' : '' }}
              </p>
            </td>

            <!-- Severity -->
            <td class="px-4 py-3">
              <SeverityBadge :severity="archive.severity" size="sm" />
            </td>

            <!-- Archived Date -->
            <td class="px-4 py-3">
              <p class="text-sm text-gray-900 dark:text-white">
                {{ formatDate(archive.archived_at) }}
              </p>
              <p class="text-xs text-gray-500 dark:text-gray-400">
                by {{ archive.archived_by_name || 'System' }}
              </p>
            </td>

            <!-- Retention -->
            <td class="px-4 py-3">
              <span 
                class="inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded-full"
                :class="archive.is_permanent 
                  ? 'bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300'
                  : 'bg-gray-100 dark:bg-gray-700/50 text-gray-700 dark:text-gray-300'"
              >
                <Lock v-if="archive.is_permanent" class="w-3 h-3" />
                <Calendar v-else class="w-3 h-3" />
                {{ archive.is_permanent ? 'Permanent' : 'Standard' }}
              </span>
              <p v-if="!archive.is_permanent && archive.days_until_expiry !== null" class="text-xs mt-1" :class="archive.days_until_expiry <= 30 ? 'text-red-500' : 'text-gray-500 dark:text-gray-400'">
                {{ archive.days_until_expiry }}d remaining
              </p>
            </td>

            <!-- Size -->
            <td class="px-4 py-3">
              <p class="text-sm text-gray-600 dark:text-gray-400">
                {{ formatSize(archive.size_bytes) }}
              </p>
            </td>

            <!-- Actions -->
            <td class="px-4 py-3 text-right">
              <div class="flex items-center justify-end gap-2">
                <button
                  @click="viewArchive(archive)"
                  class="p-2 text-gray-500 hover:text-purple-600 dark:text-gray-400 dark:hover:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 rounded-lg transition-colors"
                  title="View Archive"
                >
                  <Eye class="w-4 h-4" />
                </button>
                <button
                  @click="downloadArchive(archive)"
                  :disabled="isDownloading === archive.id"
                  class="p-2 text-gray-500 hover:text-blue-600 dark:text-gray-400 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors disabled:opacity-50"
                  title="Download Archive"
                >
                  <Download v-if="isDownloading !== archive.id" class="w-4 h-4" />
                  <Loader2 v-else class="w-4 h-4 animate-spin" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Loading Overlay for Refresh -->
      <div v-if="isLoading && archives.length > 0" class="absolute inset-0 bg-white/50 dark:bg-gray-900/50 flex items-center justify-center">
        <Loader2 class="w-8 h-8 text-purple-500 animate-spin" />
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="total > 0" class="mt-6 flex items-center justify-between">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        Showing {{ skip + 1 }} - {{ Math.min(skip + limit, total) }} of {{ total }} archives
      </p>
      <div class="flex items-center gap-2">
        <button
          @click="prevPage"
          :disabled="skip === 0"
          class="px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <span class="px-3 py-1.5 text-sm text-gray-600 dark:text-gray-400">
          Page {{ currentPage }} of {{ totalPages }}
        </span>
        <button
          @click="nextPage"
          :disabled="skip + limit >= total"
          class="px-3 py-1.5 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Archive, 
  Search, 
  X, 
  RefreshCw, 
  FilterX,
  Loader2,
  HardDrive,
  Lock,
  Clock,
  Calendar,
  Eye,
  Download
} from 'lucide-vue-next'
import { MainLayout } from '@/components/layout'
import { ErrorMessage, EmptyState, SkeletonList } from '@/components/common'
import { SeverityBadge } from '@/components/sessions'
import { useArchivesStore } from '@/stores'

// Router and Store
const router = useRouter()
const archivesStore = useArchivesStore()

// Local filter state
const searchInput = ref('')
const severityFilter = ref('')
const retentionFilter = ref('')

// Loading states
const isDownloading = ref(null)

// Debounce timer
let searchTimeout = null

// =============================================================================
// Computed
// =============================================================================

const archives = computed(() => archivesStore.archives)
const total = computed(() => archivesStore.total)
const skip = computed(() => archivesStore.skip)
const limit = computed(() => archivesStore.limit)
const isLoading = computed(() => archivesStore.isLoading)
const isLoadingStats = computed(() => archivesStore.isLoadingStats)
const isLoadingExpiring = computed(() => archivesStore.isLoadingExpiring)
const error = computed(() => archivesStore.error)
const statistics = computed(() => archivesStore.statistics)
const expiringArchives = computed(() => archivesStore.expiringArchives)

const expiringCount = computed(() => expiringArchives.value?.length || 0)

const currentPage = computed(() => Math.floor(skip.value / limit.value) + 1)
const totalPages = computed(() => Math.ceil(total.value / limit.value) || 1)

const hasActiveFilters = computed(() => {
  return searchInput.value || severityFilter.value || retentionFilter.value
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
    applyFilters()
  }, 300)
}

/**
 * Clear search input
 */
function clearSearch() {
  searchInput.value = ''
  applyFilters()
}

/**
 * Handle filter change
 */
function handleFilterChange() {
  applyFilters()
}

/**
 * Apply all filters
 */
function applyFilters() {
  archivesStore.setFilters({
    discordUserId: searchInput.value ? parseInt(searchInput.value) || null : null,
    severity: severityFilter.value || null,
    retentionTier: retentionFilter.value || null,
  })
  archivesStore.fetchArchives()
}

/**
 * Clear all filters
 */
function clearAllFilters() {
  searchInput.value = ''
  severityFilter.value = ''
  retentionFilter.value = ''
  archivesStore.clearFilters()
  archivesStore.fetchArchives()
}

/**
 * Refresh all data
 */
function refresh() {
  archivesStore.fetchArchives()
  archivesStore.fetchStatistics()
  archivesStore.fetchExpiring(30)
}

/**
 * Navigate to archive viewer
 */
function viewArchive(archive) {
  router.push({ name: 'archive-detail', params: { id: archive.id } })
}

/**
 * Download archive as JSON
 */
async function downloadArchive(archive) {
  isDownloading.value = archive.id
  try {
    const packageData = await archivesStore.downloadArchive(archive.id)
    
    if (packageData) {
      // Create downloadable JSON
      const blob = new Blob([JSON.stringify(packageData, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `archive_${archive.session_id}_${new Date().toISOString().split('T')[0]}.json`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    }
  } catch (err) {
    console.error('Failed to download archive:', err)
  } finally {
    isDownloading.value = null
  }
}

/**
 * Previous page
 */
function prevPage() {
  if (skip.value > 0) {
    archivesStore.setPage(currentPage.value - 2)
    archivesStore.fetchArchives()
  }
}

/**
 * Next page
 */
function nextPage() {
  if (skip.value + limit.value < total.value) {
    archivesStore.setPage(currentPage.value)
    archivesStore.fetchArchives()
  }
}

/**
 * Format file size
 */
function formatSize(bytes) {
  if (!bytes) return '0 B'
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  return `${size.toFixed(unitIndex > 0 ? 1 : 0)} ${units[unitIndex]}`
}

/**
 * Format date
 */
function formatDate(dateString) {
  if (!dateString) return '—'
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  })
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  // Fetch all data
  archivesStore.fetchArchives()
  archivesStore.fetchStatistics()
  archivesStore.fetchExpiring(30)
})
</script>
