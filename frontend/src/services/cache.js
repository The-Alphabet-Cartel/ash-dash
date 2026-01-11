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
 * API Cache - Simple in-memory cache for semi-static API responses
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-11-11.3-1
 * LAST MODIFIED: 2026-01-10
 * PHASE: Phase 11 - Polish & Documentation
 * CLEAN ARCHITECTURE: Compliant
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 * 
 * PURPOSE:
 *   Provides simple TTL-based caching for API responses that don't change
 *   frequently, reducing server load and improving perceived performance.
 * 
 * USAGE:
 *   import { cachedRequest, clearCache } from '@/services/cache'
 *   
 *   // Cache wiki navigation for 5 minutes
 *   const nav = await cachedRequest('wiki-nav', () => wikiApi.getNavigation(), 300)
 *   
 *   // Clear specific cache
 *   clearCache('wiki-nav')
 *   
 *   // Clear all cache
 *   clearCache()
 * ============================================================================
 */

// =============================================================================
// Cache Storage
// =============================================================================

/**
 * In-memory cache store
 * Key -> { data, timestamp, ttl }
 */
const cache = new Map()

// =============================================================================
// Default TTL Values (in seconds)
// =============================================================================

export const CacheTTL = {
  /** Short-lived cache (1 minute) - for moderately dynamic data */
  SHORT: 60,
  
  /** Medium cache (5 minutes) - for semi-static data */
  MEDIUM: 300,
  
  /** Long cache (15 minutes) - for rarely changing data */
  LONG: 900,
  
  /** Extended cache (1 hour) - for static reference data */
  EXTENDED: 3600,
}

// =============================================================================
// Cache Functions
// =============================================================================

/**
 * Execute an API request with caching
 * 
 * @param {string} key - Unique cache key
 * @param {Function} fetchFn - Async function that returns the data (called if cache miss)
 * @param {number} ttl - Time-to-live in seconds (default: 5 minutes)
 * @returns {Promise<any>} - Cached or fresh data
 * 
 * @example
 * const nav = await cachedRequest('wiki-nav', () => wikiApi.getNavigation(), CacheTTL.MEDIUM)
 */
export async function cachedRequest(key, fetchFn, ttl = CacheTTL.MEDIUM) {
  const now = Date.now()
  const cached = cache.get(key)
  
  // Check if we have valid cached data
  if (cached && (now - cached.timestamp) < (cached.ttl * 1000)) {
    return cached.data
  }
  
  // Cache miss or expired - fetch fresh data
  try {
    const response = await fetchFn()
    const data = response.data !== undefined ? response.data : response
    
    // Store in cache
    cache.set(key, {
      data,
      timestamp: now,
      ttl,
    })
    
    return data
  } catch (error) {
    // On error, return stale cache if available (stale-while-error)
    if (cached) {
      console.warn(`[Cache] Returning stale data for "${key}" due to fetch error`)
      return cached.data
    }
    throw error
  }
}

/**
 * Clear cache entries
 * 
 * @param {string} key - Specific key to clear, or undefined to clear all
 * 
 * @example
 * clearCache('wiki-nav')  // Clear specific entry
 * clearCache()            // Clear all entries
 */
export function clearCache(key = null) {
  if (key) {
    cache.delete(key)
  } else {
    cache.clear()
  }
}

/**
 * Clear cache entries matching a prefix
 * 
 * @param {string} prefix - Key prefix to match
 * 
 * @example
 * clearCachePrefix('wiki-')  // Clears wiki-nav, wiki-categories, etc.
 */
export function clearCachePrefix(prefix) {
  for (const key of cache.keys()) {
    if (key.startsWith(prefix)) {
      cache.delete(key)
    }
  }
}

/**
 * Get cache statistics (for debugging)
 * 
 * @returns {Object} - Cache stats
 */
export function getCacheStats() {
  const now = Date.now()
  let validCount = 0
  let staleCount = 0
  
  for (const [key, entry] of cache.entries()) {
    if ((now - entry.timestamp) < (entry.ttl * 1000)) {
      validCount++
    } else {
      staleCount++
    }
  }
  
  return {
    totalEntries: cache.size,
    validEntries: validCount,
    staleEntries: staleCount,
    keys: Array.from(cache.keys()),
  }
}

/**
 * Preload cache with data (useful for SSR or initial data)
 * 
 * @param {string} key - Cache key
 * @param {any} data - Data to cache
 * @param {number} ttl - Time-to-live in seconds
 */
export function preloadCache(key, data, ttl = CacheTTL.MEDIUM) {
  cache.set(key, {
    data,
    timestamp: Date.now(),
    ttl,
  })
}

// =============================================================================
// Cache Keys (centralized for consistency)
// =============================================================================

export const CacheKeys = {
  // Wiki
  WIKI_NAVIGATION: 'wiki-navigation',
  WIKI_CATEGORIES: 'wiki-categories',
  WIKI_TAGS: 'wiki-tags',
  WIKI_STYLES: 'wiki-styles',
  
  // Admin
  ADMIN_USERS: 'admin-users',
  
  // Archives
  ARCHIVE_STATS: 'archive-statistics',
}
