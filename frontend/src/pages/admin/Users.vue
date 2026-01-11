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
CRT Roster Page - View Crisis Response Team members
----------------------------------------------------------------------------
FILE VERSION: v5.0-10-10.3-5
LAST MODIFIED: 2026-01-10
PHASE: Phase 10 - Authentication & Authorization
CLEAN ARCHITECTURE: Compliant
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="crt-roster">
    <!-- Header -->
    <div class="flex justify-between items-center mb-6">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Crisis Response Team Roster
        </h3>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          {{ users.length }} team member{{ users.length !== 1 ? 's' : '' }}
        </p>
      </div>
      
      <button 
        @click="fetchUsers"
        :disabled="isLoading"
        class="btn-secondary flex items-center gap-2"
      >
        <RefreshCw class="w-4 h-4" :class="{ 'animate-spin': isLoading }" />
        Refresh
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading && users.length === 0" class="flex justify-center py-12">
      <Loader2 class="w-8 h-8 animate-spin text-purple-500" />
    </div>

    <!-- Error State -->
    <div 
      v-else-if="error" 
      class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4"
    >
      <div class="flex items-center gap-2 text-red-600 dark:text-red-400">
        <AlertCircle class="w-5 h-5" />
        <p>{{ error }}</p>
      </div>
      <button 
        @click="fetchUsers" 
        class="mt-2 text-sm text-red-600 dark:text-red-400 hover:underline"
      >
        Try again
      </button>
    </div>

    <!-- Users Table -->
    <div 
      v-else 
      class="card overflow-hidden"
    >
      <table class="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
        <thead class="bg-gray-50 dark:bg-gray-800">
          <tr>
            <th 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
            >
              Member
            </th>
            <th 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
            >
              Role
            </th>
            <th 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
            >
              Status
            </th>
            <th 
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider"
            >
              Last Active
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200 dark:divide-gray-700">
          <tr 
            v-for="user in users" 
            :key="user.id"
            class="hover:bg-gray-50 dark:hover:bg-gray-800/50 transition-colors"
          >
            <!-- Member Info -->
            <td class="px-6 py-4 whitespace-nowrap">
              <div class="flex items-center gap-3">
                <!-- Avatar -->
                <div 
                  class="w-10 h-10 rounded-full flex items-center justify-center font-medium"
                  :class="getAvatarClass(user.role)"
                >
                  {{ getInitials(user.display_name || user.email) }}
                </div>
                <!-- Name & Email -->
                <div>
                  <div class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ user.display_name || 'Unknown' }}
                  </div>
                  <div class="text-sm text-gray-500 dark:text-gray-400">
                    {{ user.email }}
                  </div>
                </div>
              </div>
            </td>
            
            <!-- Role Badge -->
            <td class="px-6 py-4 whitespace-nowrap">
              <RoleBadge :role="user.role" />
            </td>
            
            <!-- Status -->
            <td class="px-6 py-4 whitespace-nowrap">
              <span
                class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium"
                :class="user.is_active 
                  ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300'
                  : 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-400'"
              >
                <span 
                  class="w-1.5 h-1.5 rounded-full"
                  :class="user.is_active ? 'bg-green-500' : 'bg-gray-400'"
                />
                {{ user.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            
            <!-- Last Active -->
            <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
              {{ formatLastActive(user.last_login) }}
            </td>
          </tr>
          
          <!-- Empty State -->
          <tr v-if="users.length === 0">
            <td colspan="4" class="px-6 py-12 text-center">
              <Users class="w-12 h-12 mx-auto text-gray-300 dark:text-gray-600 mb-3" />
              <p class="text-gray-500 dark:text-gray-400">No team members found</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
/**
 * CRT Roster Page
 * 
 * Displays all Crisis Response Team members with:
 * - Name and email
 * - Role badge (Admin/Lead/Member)
 * - Active status
 * - Last login time
 * 
 * Authorization: Lead or Admin only (enforced by route guard)
 */

import { ref, onMounted } from 'vue'
import { Loader2, RefreshCw, AlertCircle, Users } from 'lucide-vue-next'
import { adminApi } from '@/services/api'
import { RoleBadge } from '@/components/admin'
import { formatDistanceToNow } from 'date-fns'

// =============================================================================
// State
// =============================================================================

const users = ref([])
const isLoading = ref(true)
const error = ref(null)

// =============================================================================
// API Methods
// =============================================================================

/**
 * Fetch CRT users from API
 */
async function fetchUsers() {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await adminApi.getUsers()
    users.value = response.data.users
  } catch (err) {
    console.error('Failed to fetch users:', err)
    error.value = err.response?.data?.detail || 'Failed to load team members'
  } finally {
    isLoading.value = false
  }
}

// =============================================================================
// Helpers
// =============================================================================

/**
 * Get initials from name or email
 */
function getInitials(name) {
  if (!name) return '?'
  
  // If email, use first letter before @
  if (name.includes('@')) {
    return name.charAt(0).toUpperCase()
  }
  
  // Otherwise use first letters of name parts
  return name
    .split(' ')
    .map(part => part.charAt(0))
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

/**
 * Get avatar background class based on role
 */
function getAvatarClass(role) {
  switch (role) {
    case 'admin':
      return 'bg-purple-100 text-purple-700 dark:bg-purple-900/50 dark:text-purple-300'
    case 'lead':
      return 'bg-blue-100 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300'
    default:
      return 'bg-gray-100 text-gray-700 dark:bg-gray-700 dark:text-gray-300'
  }
}

/**
 * Format last login time
 */
function formatLastActive(date) {
  if (!date) return 'Never'
  
  try {
    return formatDistanceToNow(new Date(date), { addSuffix: true })
  } catch {
    return 'Unknown'
  }
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(fetchUsers)
</script>
