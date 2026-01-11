/**
 * ============================================================================
 * Ash-DASH: Discord Crisis Detection Dashboard
 * The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
 * ============================================================================
 *
 * MISSION - NEVER TO BE VIOLATED:
 *     Reveal   → Surface crisis alerts and user escalation patterns in real-time
 *     Enable   → Equip Crisis Response Teams with tools for swift intervention
 *     Clarify  → Translate detection data into actionable intelligence
 *     Protect  → Safeguard our LGBTQIA+ community through vigilant oversight
 *
 * ============================================================================
 * Archives Store - Pinia store for archive operations
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-9-9.5-1
 * LAST MODIFIED: 2026-01-09
 * PHASE: Phase 9 - Archive System Implementation
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { archivesApi } from '@/services'

export const useArchivesStore = defineStore('archives', () => {
  // ==========================================================================
  // State
  // ==========================================================================
  
  // Archive list
  const archives = ref([])
  const total = ref(0)
  const skip = ref(0)
  const limit = ref(50)
  
  // Filters
  const filters = ref({
    discordUserId: null,
    severity: '',
    retentionTier: '',
  })
  
  // Loading states
  const isLoading = ref(false)
  const isArchiving = ref(false)
  const isLoadingStats = ref(false)
  const isLoadingExpiring = ref(false)
  
  // Error state
  const error = ref(null)
  
  // Statistics
  const statistics = ref(null)
  
  // Expiring archives
  const expiringArchives = ref([])
  
  // Current archive detail
  const currentArchive = ref(null)
  const currentArchivePackage = ref(null)
  
  // Session archive status cache
  const sessionArchiveCache = ref({})

  // ==========================================================================
  // Computed
  // ==========================================================================
  
  const hasFilters = computed(() => {
    return filters.value.discordUserId || 
           filters.value.severity || 
           filters.value.retentionTier
  })
  
  const totalSizeMB = computed(() => {
    return statistics.value?.total_size_mb || 0
  })
  
  const totalArchives = computed(() => {
    return statistics.value?.total_archives || 0
  })

  // ==========================================================================
  // Actions
  // ==========================================================================
  
  /**
   * Archive a session
   * @param {string} sessionId - Session ID to archive
   * @param {string} retentionTier - 'standard' or 'permanent'
   */
  async function archiveSession(sessionId, retentionTier = 'standard') {
    isArchiving.value = true
    error.value = null
    
    try {
      const response = await archivesApi.archiveSession(sessionId, {
        retention_tier: retentionTier,
      })
      
      // Update cache
      sessionArchiveCache.value[sessionId] = {
        is_archived: true,
        archive: response.data,
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to archive session:', err)
      error.value = err.response?.data?.detail || 'Failed to archive session'
      throw err
    } finally {
      isArchiving.value = false
    }
  }
  
  /**
   * Check if a session is archived
   * @param {string} sessionId - Session ID
   * @param {boolean} force - Force refresh even if cached
   */
  async function checkSessionArchived(sessionId, force = false) {
    // Return cached value if available
    if (!force && sessionArchiveCache.value[sessionId] !== undefined) {
      return sessionArchiveCache.value[sessionId]
    }
    
    try {
      const response = await archivesApi.checkSession(sessionId)
      sessionArchiveCache.value[sessionId] = response.data
      return response.data
    } catch (err) {
      console.error('Failed to check session archive status:', err)
      return { is_archived: false, archive: null }
    }
  }
  
  /**
   * Fetch archives list with filters
   */
  async function fetchArchives() {
    isLoading.value = true
    error.value = null
    
    try {
      const params = {
        skip: skip.value,
        limit: limit.value,
      }
      
      if (filters.value.discordUserId) {
        params.discord_user_id = filters.value.discordUserId
      }
      if (filters.value.severity) {
        params.severity = filters.value.severity
      }
      if (filters.value.retentionTier) {
        params.retention_tier = filters.value.retentionTier
      }
      
      const response = await archivesApi.list(params)
      archives.value = response.data.archives
      total.value = response.data.total
      
      return response.data
    } catch (err) {
      console.error('Failed to fetch archives:', err)
      error.value = err.response?.data?.detail || 'Failed to load archives'
      archives.value = []
      throw err
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Fetch archive statistics
   */
  async function fetchStatistics() {
    isLoadingStats.value = true
    
    try {
      const response = await archivesApi.getStatistics()
      statistics.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch archive statistics:', err)
      statistics.value = null
      throw err
    } finally {
      isLoadingStats.value = false
    }
  }
  
  /**
   * Fetch archives expiring soon
   * @param {number} days - Days until expiration
   */
  async function fetchExpiring(days = 30) {
    isLoadingExpiring.value = true
    
    try {
      const response = await archivesApi.getExpiring(days)
      expiringArchives.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch expiring archives:', err)
      expiringArchives.value = []
      throw err
    } finally {
      isLoadingExpiring.value = false
    }
  }
  
  /**
   * Get archive metadata
   * @param {string} archiveId - Archive UUID
   */
  async function fetchArchive(archiveId) {
    try {
      const response = await archivesApi.get(archiveId)
      currentArchive.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to fetch archive:', err)
      currentArchive.value = null
      throw err
    }
  }
  
  /**
   * Download and decrypt archive
   * @param {string} archiveId - Archive UUID
   */
  async function downloadArchive(archiveId) {
    try {
      const response = await archivesApi.download(archiveId)
      currentArchivePackage.value = response.data
      return response.data
    } catch (err) {
      console.error('Failed to download archive:', err)
      currentArchivePackage.value = null
      throw err
    }
  }
  
  /**
   * Update retention tier
   * @param {string} archiveId - Archive UUID
   * @param {string} newTier - 'standard' or 'permanent'
   */
  async function updateRetentionTier(archiveId, newTier) {
    try {
      const response = await archivesApi.updateRetention(archiveId, newTier)
      
      // Update in list if present
      const index = archives.value.findIndex(a => a.id === archiveId)
      if (index !== -1) {
        archives.value[index] = response.data
      }
      
      // Update current if viewing
      if (currentArchive.value?.id === archiveId) {
        currentArchive.value = response.data
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to update retention tier:', err)
      throw err
    }
  }
  
  /**
   * Extend retention
   * @param {string} archiveId - Archive UUID
   * @param {number} days - Days to extend
   */
  async function extendRetention(archiveId, days) {
    try {
      const response = await archivesApi.extendRetention(archiveId, days)
      
      // Update in list if present
      const index = archives.value.findIndex(a => a.id === archiveId)
      if (index !== -1) {
        archives.value[index] = response.data
      }
      
      return response.data
    } catch (err) {
      console.error('Failed to extend retention:', err)
      throw err
    }
  }
  
  /**
   * Delete an archive
   * @param {string} archiveId - Archive UUID
   */
  async function deleteArchive(archiveId) {
    try {
      await archivesApi.delete(archiveId)
      
      // Remove from list
      archives.value = archives.value.filter(a => a.id !== archiveId)
      total.value = Math.max(0, total.value - 1)
      
      // Clear current if viewing
      if (currentArchive.value?.id === archiveId) {
        currentArchive.value = null
        currentArchivePackage.value = null
      }
    } catch (err) {
      console.error('Failed to delete archive:', err)
      throw err
    }
  }
  
  /**
   * Set filters
   */
  function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    skip.value = 0 // Reset pagination
  }
  
  /**
   * Clear filters
   */
  function clearFilters() {
    filters.value = {
      discordUserId: null,
      severity: '',
      retentionTier: '',
    }
    skip.value = 0
  }
  
  /**
   * Set pagination
   */
  function setPage(page) {
    skip.value = page * limit.value
  }
  
  /**
   * Clear current archive
   */
  function clearCurrent() {
    currentArchive.value = null
    currentArchivePackage.value = null
  }
  
  /**
   * Clear session archive cache
   */
  function clearCache() {
    sessionArchiveCache.value = {}
  }

  // ==========================================================================
  // Return
  // ==========================================================================
  
  return {
    // State
    archives,
    total,
    skip,
    limit,
    filters,
    isLoading,
    isArchiving,
    isLoadingStats,
    isLoadingExpiring,
    error,
    statistics,
    expiringArchives,
    currentArchive,
    currentArchivePackage,
    sessionArchiveCache,
    
    // Computed
    hasFilters,
    totalSizeMB,
    totalArchives,
    
    // Actions
    archiveSession,
    checkSessionArchived,
    fetchArchives,
    fetchStatistics,
    fetchExpiring,
    fetchArchive,
    downloadArchive,
    updateRetentionTier,
    extendRetention,
    deleteArchive,
    setFilters,
    clearFilters,
    setPage,
    clearCurrent,
    clearCache,
  }
})

export default useArchivesStore
