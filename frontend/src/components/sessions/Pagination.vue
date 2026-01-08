<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Pagination - Reusable pagination controls
============================================================================
FILE VERSION: v5.0-5-5.4-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="flex flex-col sm:flex-row items-center justify-between gap-4 px-4 py-3 bg-white dark:bg-gray-800 rounded-xl shadow-sm">
    <!-- Page Info -->
    <div class="text-sm text-gray-600 dark:text-gray-400">
      Showing 
      <span class="font-medium text-gray-900 dark:text-white">{{ startItem }}</span>
      to
      <span class="font-medium text-gray-900 dark:text-white">{{ endItem }}</span>
      of
      <span class="font-medium text-gray-900 dark:text-white">{{ total.toLocaleString() }}</span>
      results
    </div>

    <!-- Page Controls -->
    <div class="flex items-center gap-2">
      <!-- First Page -->
      <button
        @click="goToPage(1)"
        :disabled="currentPage === 1"
        class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        title="First page"
      >
        <ChevronsLeft class="w-4 h-4" />
      </button>

      <!-- Previous Page -->
      <button
        @click="goToPage(currentPage - 1)"
        :disabled="currentPage === 1"
        class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        title="Previous page"
      >
        <ChevronLeft class="w-4 h-4" />
      </button>

      <!-- Page Numbers -->
      <div class="flex items-center gap-1">
        <template v-for="page in visiblePages" :key="page">
          <button
            v-if="page !== '...'"
            @click="goToPage(page)"
            :class="[
              'min-w-[36px] h-9 px-2 rounded-lg text-sm font-medium transition-colors',
              page === currentPage
                ? 'bg-purple-600 text-white'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700'
            ]"
          >
            {{ page }}
          </button>
          <span v-else class="px-2 text-gray-400 dark:text-gray-500">...</span>
        </template>
      </div>

      <!-- Next Page -->
      <button
        @click="goToPage(currentPage + 1)"
        :disabled="currentPage === totalPages"
        class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        title="Next page"
      >
        <ChevronRight class="w-4 h-4" />
      </button>

      <!-- Last Page -->
      <button
        @click="goToPage(totalPages)"
        :disabled="currentPage === totalPages"
        class="p-2 rounded-lg text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        title="Last page"
      >
        <ChevronsRight class="w-4 h-4" />
      </button>
    </div>

    <!-- Page Size Selector -->
    <div class="flex items-center gap-2">
      <label class="text-sm text-gray-600 dark:text-gray-400">Per page:</label>
      <select
        :value="pageSize"
        @change="$emit('page-size-change', Number($event.target.value))"
        class="px-2 py-1 text-sm rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
      >
        <option v-for="size in pageSizeOptions" :key="size" :value="size">
          {{ size }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-vue-next'

const props = defineProps({
  currentPage: {
    type: Number,
    required: true
  },
  totalPages: {
    type: Number,
    required: true
  },
  total: {
    type: Number,
    required: true
  },
  pageSize: {
    type: Number,
    default: 20
  },
  pageSizeOptions: {
    type: Array,
    default: () => [10, 20, 50, 100]
  }
})

const emit = defineEmits(['page-change', 'page-size-change'])

// Calculate item range being shown
const startItem = computed(() => {
  if (props.total === 0) return 0
  return (props.currentPage - 1) * props.pageSize + 1
})

const endItem = computed(() => {
  return Math.min(props.currentPage * props.pageSize, props.total)
})

// Generate array of visible page numbers
const visiblePages = computed(() => {
  const pages = []
  const total = props.totalPages
  const current = props.currentPage
  
  if (total <= 7) {
    // Show all pages if 7 or fewer
    for (let i = 1; i <= total; i++) {
      pages.push(i)
    }
  } else {
    // Always show first page
    pages.push(1)
    
    if (current > 3) {
      pages.push('...')
    }
    
    // Show pages around current
    const start = Math.max(2, current - 1)
    const end = Math.min(total - 1, current + 1)
    
    for (let i = start; i <= end; i++) {
      pages.push(i)
    }
    
    if (current < total - 2) {
      pages.push('...')
    }
    
    // Always show last page
    pages.push(total)
  }
  
  return pages
})

function goToPage(page) {
  if (page >= 1 && page <= props.totalPages && page !== props.currentPage) {
    emit('page-change', page)
  }
}
</script>
