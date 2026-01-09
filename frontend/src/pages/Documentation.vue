<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
Documentation Page - Wiki and training materials
============================================================================
FILE VERSION: v5.0-7-7.8-2
LAST MODIFIED: 2026-01-09
PHASE: Phase 7 - Documentation Wiki
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <MainLayout>
    <!-- Page Header -->
    <div class="mb-6">
      <h2 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">Documentation</h2>
      <p class="text-gray-600 dark:text-gray-400">CRT training materials and reference guides</p>
    </div>

    <!-- Two Column Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Sidebar Navigation -->
      <div class="card p-4">
        <!-- Search -->
        <div class="mb-4">
          <div class="relative">
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-400" />
            <input
              v-model="searchQuery"
              type="text"
              placeholder="Search docs..."
              class="w-full pl-9 pr-3 py-2 text-sm rounded-lg bg-gray-100 dark:bg-gray-800 border-0 focus:ring-2 focus:ring-purple-500 text-gray-900 dark:text-white placeholder-gray-500"
              @input="debouncedSearch"
            />
            <button 
              v-if="searchQuery"
              @click="clearSearch"
              class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X class="w-4 h-4" />
            </button>
          </div>
        </div>

        <!-- Search Results -->
        <div v-if="isSearching" class="mb-4">
          <div class="flex items-center justify-center py-4">
            <Loader2 class="w-5 h-5 animate-spin text-purple-500" />
          </div>
        </div>

        <div v-else-if="searchResults.length > 0" class="mb-4">
          <h4 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 px-2">
            Search Results ({{ searchResults.length }})
          </h4>
          <nav class="space-y-1">
            <button
              v-for="result in searchResults"
              :key="result.document.slug"
              @click="loadDocument(result.document.slug)"
              class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors"
              :class="currentSlug === result.document.slug
                ? 'text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-900/30'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'"
            >
              <div class="font-medium">{{ result.document.title }}</div>
              <div class="text-xs text-gray-500 truncate">{{ result.document.category }}</div>
            </button>
          </nav>
          <button 
            @click="clearSearch" 
            class="mt-2 w-full text-xs text-purple-600 dark:text-purple-400 hover:underline"
          >
            Clear search
          </button>
        </div>

        <!-- Category Navigation -->
        <template v-else>
          <div v-if="loadingNav" class="flex items-center justify-center py-8">
            <Loader2 class="w-5 h-5 animate-spin text-purple-500" />
          </div>

          <nav v-else class="space-y-4">
            <!-- Home Link -->
            <button
              @click="goToIndex"
              class="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-sm transition-colors"
              :class="!currentSlug
                ? 'text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-900/30'
                : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'"
            >
              <Home class="w-4 h-4" />
              All Documents
            </button>

            <div v-for="category in navigation.categories" :key="category.slug">
              <button
                @click="toggleCategory(category.slug)"
                class="flex items-center justify-between w-full px-2 py-1 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider hover:text-gray-700 dark:hover:text-gray-300"
              >
                <span class="flex items-center gap-2">
                  <component :is="getCategoryIcon(category.icon)" class="w-4 h-4" />
                  {{ category.name }}
                </span>
                <ChevronDown 
                  class="w-4 h-4 transition-transform" 
                  :class="{ 'rotate-180': !collapsedCategories.has(category.slug) }"
                />
              </button>
              
              <div v-show="!collapsedCategories.has(category.slug)" class="mt-1 space-y-1">
                <button
                  v-for="doc in category.documents"
                  :key="doc.slug"
                  @click="loadDocument(doc.slug)"
                  class="w-full text-left px-3 py-2 rounded-lg text-sm transition-colors"
                  :class="currentSlug === doc.slug
                    ? 'text-purple-700 dark:text-purple-300 bg-purple-100 dark:bg-purple-900/30'
                    : 'text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800'"
                >
                  {{ doc.title }}
                </button>
              </div>
            </div>
          </nav>

          <!-- Document Count -->
          <div v-if="navigation.total_documents" class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
            <p class="text-xs text-gray-500 dark:text-gray-400 px-2">
              {{ navigation.total_documents }} documents
            </p>
          </div>
        </template>
      </div>

      <!-- Content Area -->
      <div class="lg:col-span-3 card">
        <!-- Loading State -->
        <div v-if="loadingDoc" class="flex items-center justify-center py-16">
          <Loader2 class="w-8 h-8 animate-spin text-purple-500" />
        </div>

        <!-- Error State -->
        <div v-else-if="error" class="flex flex-col items-center justify-center py-16 text-center">
          <div class="w-16 h-16 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center mb-4">
            <AlertCircle class="w-8 h-8 text-red-500" />
          </div>
          <h3 class="text-lg font-medium text-gray-900 dark:text-white mb-1">Error Loading Document</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400 max-w-sm">{{ error }}</p>
          <button 
            @click="retryLoad"
            class="mt-4 px-4 py-2 text-sm rounded-lg bg-purple-600 text-white hover:bg-purple-700"
          >
            Try Again
          </button>
        </div>

        <!-- Document Content -->
        <template v-else-if="currentDocument">
          <div class="p-6 border-b border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between flex-wrap gap-4">
              <div>
                <h3 class="text-xl font-semibold text-gray-900 dark:text-white">
                  {{ currentDocument.title }}
                </h3>
                <p v-if="currentDocument.description" class="mt-1 text-sm text-gray-500 dark:text-gray-400">
                  {{ currentDocument.description }}
                </p>
              </div>
              <button 
                @click="downloadPDF"
                :disabled="downloadingPDF"
                class="inline-flex items-center gap-2 px-4 py-2 text-sm rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors disabled:opacity-50"
              >
                <Loader2 v-if="downloadingPDF" class="w-4 h-4 animate-spin" />
                <Download v-else class="w-4 h-4" />
                {{ downloadingPDF ? 'Generating...' : 'Download PDF' }}
              </button>
            </div>
            
            <!-- Tags -->
            <div class="flex flex-wrap items-center gap-2 mt-4">
              <span class="px-2 py-1 rounded bg-purple-100 dark:bg-purple-900/30 text-purple-700 dark:text-purple-300 text-xs font-medium">
                {{ currentDocument.category }}
              </span>
              <span 
                v-for="tag in currentDocument.tags" 
                :key="tag"
                class="px-2 py-1 rounded bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
          
          <!-- Rendered Content -->
          <div class="p-6">
            <article 
              class="wiki-content prose prose-gray dark:prose-invert max-w-none"
              v-html="currentDocument.content_html"
            />
          </div>

          <!-- Footer -->
          <div class="px-6 py-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
            <div class="flex flex-wrap items-center justify-between gap-4 text-sm text-gray-500 dark:text-gray-400">
              <div class="flex items-center gap-4">
                <span v-if="currentDocument.author">
                  <User class="w-4 h-4 inline mr-1" />
                  {{ currentDocument.author }}
                </span>
                <span v-if="currentDocument.last_updated">
                  <Calendar class="w-4 h-4 inline mr-1" />
                  Updated: {{ currentDocument.last_updated }}
                </span>
              </div>
              <span v-if="currentDocument.version" class="text-xs">
                v{{ currentDocument.version }}
              </span>
            </div>
          </div>
        </template>

        <!-- Table of Contents (Index View) -->
        <div v-else class="p-6">
          <!-- Index Header -->
          <div class="text-center mb-8 pb-6 border-b border-gray-200 dark:border-gray-700">
            <div class="w-16 h-16 rounded-full bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center mx-auto mb-4">
              <BookOpen class="w-8 h-8 text-white" />
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-2">
              Ash-Dash Documentation
            </h3>
            <p class="text-gray-500 dark:text-gray-400 max-w-lg mx-auto">
              Training materials, reference guides, and resources for CRT members and administrators.
            </p>
          </div>

          <!-- Loading Index -->
          <div v-if="loadingNav" class="flex items-center justify-center py-8">
            <Loader2 class="w-6 h-6 animate-spin text-purple-500" />
          </div>

          <!-- Categories Grid -->
          <div v-else class="space-y-8">
            <div 
              v-for="category in navigation.categories" 
              :key="category.slug"
              class="bg-gray-50 dark:bg-gray-800/50 rounded-xl p-6"
            >
              <!-- Category Header -->
              <div class="flex items-center gap-3 mb-4">
                <div class="w-10 h-10 rounded-lg bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                  <component :is="getCategoryIcon(category.icon)" class="w-5 h-5 text-purple-600 dark:text-purple-400" />
                </div>
                <div>
                  <h4 class="font-semibold text-gray-900 dark:text-white">{{ category.name }}</h4>
                  <p class="text-xs text-gray-500 dark:text-gray-400">
                    {{ category.documents.length }} document{{ category.documents.length !== 1 ? 's' : '' }}
                  </p>
                </div>
              </div>

              <!-- Documents List -->
              <div class="grid gap-3 sm:grid-cols-2">
                <button
                  v-for="doc in category.documents"
                  :key="doc.slug"
                  @click="loadDocument(doc.slug)"
                  class="text-left p-4 rounded-lg bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 hover:border-purple-500 dark:hover:border-purple-500 hover:shadow-md transition-all group"
                >
                  <div class="flex items-start gap-3">
                    <FileText class="w-5 h-5 text-gray-400 group-hover:text-purple-500 mt-0.5 flex-shrink-0" />
                    <div class="min-w-0">
                      <h5 class="font-medium text-gray-900 dark:text-white group-hover:text-purple-600 dark:group-hover:text-purple-400 truncate">
                        {{ doc.title }}
                      </h5>
                      <p v-if="doc.description" class="text-sm text-gray-500 dark:text-gray-400 mt-1 line-clamp-2">
                        {{ doc.description }}
                      </p>
                      <div v-if="doc.tags && doc.tags.length > 0" class="flex flex-wrap gap-1 mt-2">
                        <span 
                          v-for="tag in doc.tags.slice(0, 3)" 
                          :key="tag"
                          class="text-xs px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-500 dark:text-gray-400"
                        >
                          {{ tag }}
                        </span>
                        <span v-if="doc.tags.length > 3" class="text-xs text-gray-400">
                          +{{ doc.tags.length - 3 }}
                        </span>
                      </div>
                    </div>
                  </div>
                </button>
              </div>
            </div>

            <!-- Empty State -->
            <div v-if="navigation.categories.length === 0" class="text-center py-8">
              <FileText class="w-12 h-12 text-gray-400 mx-auto mb-3" />
              <p class="text-gray-500 dark:text-gray-400">No documents found.</p>
            </div>
          </div>

          <!-- Footer -->
          <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700 text-center">
            <p class="text-sm text-gray-500 dark:text-gray-400">
              🏳️‍🌈 Built with care for chosen family
            </p>
            <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
              <a href="https://discord.gg/alphabetcartel" class="hover:text-purple-500" target="_blank">discord.gg/alphabetcartel</a>
              &nbsp;•&nbsp;
              <a href="https://alphabetcartel.org" class="hover:text-purple-500" target="_blank">alphabetcartel.org</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { MainLayout } from '@/components/layout'
import { wikiApi } from '@/services/api'
import { 
  BookOpen, 
  Shield, 
  Settings, 
  FileText, 
  Download,
  Search,
  X,
  ChevronDown,
  Loader2,
  AlertCircle,
  User,
  Calendar,
  GraduationCap,
  HelpCircle,
  Home
} from 'lucide-vue-next'

// =============================================================================
// Router
// =============================================================================

const route = useRoute()
const router = useRouter()

// =============================================================================
// State
// =============================================================================

// Navigation state
const navigation = ref({ categories: [], total_documents: 0 })
const loadingNav = ref(true)
const collapsedCategories = reactive(new Set())

// Document state
const currentDocument = ref(null)
const currentSlug = ref(null)
const loadingDoc = ref(false)
const error = ref(null)

// Search state
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)
let searchTimeout = null

// PDF download state
const downloadingPDF = ref(false)

// =============================================================================
// Category Icons
// =============================================================================

const categoryIcons = {
  'settings': Settings,
  'shield': Shield,
  'book-open': BookOpen,
  'graduation-cap': GraduationCap,
  'file-text': FileText,
  'help-circle': HelpCircle,
}

function getCategoryIcon(iconName) {
  return categoryIcons[iconName] || FileText
}

// =============================================================================
// Navigation
// =============================================================================

async function loadNavigation() {
  loadingNav.value = true
  try {
    const response = await wikiApi.getNavigation()
    navigation.value = response.data
  } catch (err) {
    console.error('Failed to load navigation:', err)
  } finally {
    loadingNav.value = false
  }
}

function toggleCategory(slug) {
  if (collapsedCategories.has(slug)) {
    collapsedCategories.delete(slug)
  } else {
    collapsedCategories.add(slug)
  }
}

function goToIndex() {
  currentDocument.value = null
  currentSlug.value = null
  router.push({ query: {} })
}

// =============================================================================
// Document Loading
// =============================================================================

async function loadDocument(slug) {
  if (!slug || slug === currentSlug.value) return
  
  loadingDoc.value = true
  error.value = null
  currentSlug.value = slug
  
  // Update URL
  router.push({ query: { doc: slug } })
  
  try {
    const response = await wikiApi.getDocument(slug)
    currentDocument.value = response.data
  } catch (err) {
    console.error('Failed to load document:', err)
    error.value = err.response?.data?.detail || 'Failed to load document'
    currentDocument.value = null
  } finally {
    loadingDoc.value = false
  }
}

function retryLoad() {
  if (currentSlug.value) {
    loadDocument(currentSlug.value)
  }
}

// =============================================================================
// Search
// =============================================================================

function debouncedSearch() {
  clearTimeout(searchTimeout)
  
  if (!searchQuery.value.trim()) {
    searchResults.value = []
    return
  }
  
  searchTimeout = setTimeout(async () => {
    isSearching.value = true
    try {
      const response = await wikiApi.search(searchQuery.value)
      searchResults.value = response.data.results
    } catch (err) {
      console.error('Search failed:', err)
      searchResults.value = []
    } finally {
      isSearching.value = false
    }
  }, 300) // 300ms debounce
}

function clearSearch() {
  searchQuery.value = ''
  searchResults.value = []
}

// =============================================================================
// PDF Download
// =============================================================================

async function downloadPDF() {
  if (!currentSlug.value || downloadingPDF.value) return
  
  downloadingPDF.value = true
  try {
    const response = await wikiApi.downloadPDF(currentSlug.value)
    
    // Create download link
    const blob = new Blob([response.data], { type: 'application/pdf' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${currentSlug.value.split('/').pop()}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
  } catch (err) {
    console.error('PDF download failed:', err)
    alert('Failed to download PDF. Please try again.')
  } finally {
    downloadingPDF.value = false
  }
}

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(async () => {
  await loadNavigation()
  
  // Load document from URL query param
  const docSlug = route.query.doc
  if (docSlug) {
    loadDocument(docSlug)
  }
})

// Watch for route changes
watch(() => route.query.doc, (newSlug) => {
  if (newSlug && newSlug !== currentSlug.value) {
    loadDocument(newSlug)
  } else if (!newSlug) {
    // Return to index
    currentDocument.value = null
    currentSlug.value = null
  }
})
</script>

<style>
/* Wiki content styles - imported from backend */
.wiki-content {
  line-height: 1.7;
}

.wiki-content h1,
.wiki-content h2,
.wiki-content h3,
.wiki-content h4 {
  scroll-margin-top: 80px;
}

.wiki-content h2 {
  border-bottom: 1px solid rgba(128, 128, 128, 0.3);
  padding-bottom: 0.3em;
}

/* Hide TOC anchor links by default, show on hover */
.wiki-content .toc-link {
  opacity: 0;
  margin-left: 0.5em;
  text-decoration: none;
  color: #9333EA;
  transition: opacity 0.2s;
}

.wiki-content h1:hover .toc-link,
.wiki-content h2:hover .toc-link,
.wiki-content h3:hover .toc-link,
.wiki-content h4:hover .toc-link,
.wiki-content h5:hover .toc-link,
.wiki-content h6:hover .toc-link {
  opacity: 1;
}

.wiki-content a {
  color: #A855F7;
}

.wiki-content a:hover {
  text-decoration: underline;
}

.wiki-content code {
  background: rgba(128, 128, 128, 0.15);
  padding: 0.2em 0.4em;
  border-radius: 4px;
  font-size: 0.9em;
}

.wiki-content pre {
  background: #1f2937;
  border-radius: 8px;
  padding: 1em;
  overflow-x: auto;
}

.wiki-content pre code {
  background: transparent;
  padding: 0;
}

.wiki-content table {
  width: 100%;
  border-collapse: collapse;
}

.wiki-content th,
.wiki-content td {
  padding: 0.75em 1em;
  text-align: left;
  border: 1px solid rgba(128, 128, 128, 0.3);
}

.wiki-content th {
  background: rgba(147, 51, 234, 0.1);
}

.wiki-content blockquote {
  border-left: 4px solid #9333EA;
  margin: 1.5em 0;
  padding: 0.5em 1em;
  background: rgba(147, 51, 234, 0.05);
  font-style: italic;
}

.wiki-content .task-item {
  list-style: none;
  margin-left: -1.5em;
}

.wiki-content .task-item input[type="checkbox"] {
  margin-right: 0.5em;
  accent-color: #9333EA;
}

/* Syntax highlighting */
.wiki-content .highlight {
  background: #1f2937;
  border-radius: 8px;
  padding: 1em;
  overflow-x: auto;
  margin: 1.5em 0;
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
