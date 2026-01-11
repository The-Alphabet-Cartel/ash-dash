<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
NotesPanel - Full session notes editor with TipTap integration
============================================================================
FILE VERSION: v5.0-11-11.3-3
LAST MODIFIED: 2026-01-10
PHASE: Phase 11 - Polish & Documentation (ARIA)
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="card flex flex-col">
    <!-- Header -->
    <div class="p-4 border-b border-gray-200 dark:border-gray-700">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <FileText class="w-5 h-5 text-purple-500" aria-hidden="true" />
            CRT Notes
          </h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ totalNotes }} note{{ totalNotes !== 1 ? 's' : '' }}
            <span v-if="isSessionLocked" class="text-yellow-500">
              • Session {{ session?.status }}
            </span>
          </p>
        </div>
        
        <!-- Session Lock Status -->
        <div v-if="isSessionLocked" class="flex items-center gap-1 text-yellow-600 dark:text-yellow-500">
          <Lock class="w-4 h-4" aria-hidden="true" />
          <span class="text-sm">Locked</span>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex flex-col overflow-hidden p-4 gap-4">
      <!-- Loading State -->
      <div v-if="loading" class="flex items-center justify-center py-8">
        <div class="flex flex-col items-center gap-3">
          <Loader2 class="w-8 h-8 animate-spin text-purple-500" aria-hidden="true" />
          <p class="text-sm text-gray-500 dark:text-gray-400">Loading notes...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="flex items-center justify-center py-8">
        <div class="text-center">
          <AlertCircle class="w-12 h-12 mx-auto mb-4 text-red-500" aria-hidden="true" />
          <p class="text-red-500 mb-2">{{ error }}</p>
          <button 
            @click="loadNotes" 
            class="text-purple-500 hover:text-purple-600 text-sm"
          >
            Try again
          </button>
        </div>
      </div>

      <!-- Notes Content -->
      <template v-else>
        <!-- Current Note Editor (when active) -->
        <div v-if="showEditor" class="flex flex-col">
          <NotesEditor
            ref="editorRef"
            v-model="currentNoteContent"
            :readonly="isNoteReadonly"
            :placeholder="editorPlaceholder"
            :auto-save-delay="2000"
            @save="handleAutoSave"
          />
        </div>

        <!-- Previous Notes (Clickable to view) -->
        <div 
          v-if="previousNotes.length > 0" 
          class="border-t border-gray-200 dark:border-gray-700 pt-4"
          :class="showEditor ? 'max-h-48 overflow-y-auto' : 'max-h-64 overflow-y-auto'"
        >
          <h4 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3 flex items-center gap-2">
            <History class="w-4 h-4" aria-hidden="true" />
            {{ showEditor ? 'Previous Notes' : 'All Notes' }}
            <span class="text-xs text-gray-400">(click to view)</span>
          </h4>
          <div class="space-y-3">
            <div 
              v-for="note in previousNotes" 
              :key="note.id"
              class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50 border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 hover:border-purple-300 dark:hover:border-purple-600 transition-colors"
            >
              <!-- Note Header -->
              <div class="flex items-center justify-between mb-2">
                <div 
                  class="flex items-center gap-2 cursor-pointer flex-1"
                  @click="viewNote(note)"
                >
                  <div class="w-6 h-6 rounded-full bg-purple-100 dark:bg-purple-900/30 flex items-center justify-center">
                    <span class="text-xs font-medium text-purple-600 dark:text-purple-400">
                      {{ getInitials(getAuthorName(note)) }}
                    </span>
                  </div>
                  <span class="text-sm font-medium text-gray-900 dark:text-white">
                    {{ getAuthorName(note) }}
                  </span>
                  <span v-if="note.version > 1" class="text-xs text-gray-400">
                    v{{ note.version }}
                  </span>
                </div>
                
                <!-- Note Actions -->
                <div class="flex items-center gap-2">
                  <!-- Edit Button (own notes or admin) -->
                  <button
                    v-if="canEditNote(note) && !isSessionLocked"
                    @click.stop="editNote(note)"
                    class="p-1 rounded text-gray-400 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-purple-50 dark:hover:bg-purple-900/20 transition-colors"
                    title="Edit note"
                    aria-label="Edit note"
                  >
                    <Pencil class="w-3.5 h-3.5" aria-hidden="true" />
                  </button>
                  
                  <!-- Delete Button (admin only) -->
                  <button
                    v-if="authStore.isAdmin && !isSessionLocked"
                    @click.stop="confirmDeleteNote(note)"
                    class="p-1 rounded text-gray-400 hover:text-red-600 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                    title="Delete note"
                    aria-label="Delete note"
                  >
                    <Trash2 class="w-3.5 h-3.5" aria-hidden="true" />
                  </button>
                  
                  <Lock v-if="note.is_locked" class="w-3 h-3 text-gray-400" aria-hidden="true" />
                  <span class="text-xs text-gray-500 dark:text-gray-400">
                    {{ formatDate(note.created_at) }}
                  </span>
                </div>
              </div>

              <!-- Note Content Preview (clickable) -->
              <p 
                class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap cursor-pointer"
                @click="viewNote(note)"
              >
                {{ note.content_preview }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty State (no notes and no editor) -->
        <div 
          v-if="!showEditor && previousNotes.length === 0" 
          class="flex items-center justify-center py-8"
        >
          <div class="text-center">
            <FileText class="w-12 h-12 mx-auto mb-4 text-gray-300 dark:text-gray-600" aria-hidden="true" />
            <p class="text-gray-500 dark:text-gray-400 mb-2">No notes yet</p>
            <p v-if="!isSessionLocked" class="text-xs text-gray-400 dark:text-gray-500">
              Click "Add Note" to start documenting
            </p>
          </div>
        </div>
      </template>
    </div>

    <!-- Footer Actions -->
    <div class="p-4 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50">
      <div class="flex items-center justify-between gap-2">
        <!-- Left: Save/Add buttons -->
        <div class="flex items-center gap-2">
          <!-- Save Button (when editing, not when just viewing) -->
          <button 
            v-if="showEditor && currentNoteId && !viewingExistingNote"
            @click="saveNote"
            :disabled="isNoteReadonly || saving"
            class="px-4 py-2 rounded-lg text-sm font-medium bg-purple-600 text-white hover:bg-purple-700 disabled:bg-gray-300 dark:disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <Save v-if="!saving" class="w-4 h-4" aria-hidden="true" />
            <Loader2 v-else class="w-4 h-4 animate-spin" aria-hidden="true" />
            {{ saving ? 'Saving...' : 'Save' }}
          </button>

          <!-- Close Button (when viewing existing note) -->
          <button 
            v-if="showEditor && viewingExistingNote"
            @click="cancelNewNote"
            class="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors flex items-center gap-2"
          >
            <X class="w-4 h-4" aria-hidden="true" />
            Close
          </button>

          <!-- Add Note Button -->
          <button 
            v-if="!showEditor || viewingExistingNote"
            @click="startNewNote"
            :disabled="isSessionLocked"
            class="px-4 py-2 rounded-lg text-sm font-medium bg-purple-600 text-white hover:bg-purple-700 disabled:bg-gray-300 dark:disabled:bg-gray-700 disabled:text-gray-500 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
          >
            <Plus class="w-4 h-4" />
            Add Note
          </button>

          <!-- Cancel Button (when creating new) -->
          <button 
            v-if="showEditor && !currentNoteId && !viewingExistingNote"
            @click="cancelNewNote"
            class="px-4 py-2 rounded-lg text-sm font-medium text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
          >
            Cancel
          </button>
        </div>

        <!-- Right: Status info -->
        <div class="text-xs text-gray-400 dark:text-gray-500">
          <span v-if="isSessionLocked">
            Notes are locked (session {{ session?.status }})
          </span>
          <span v-else-if="viewingExistingNote">
            Viewing note • Click "Add Note" to create new
          </span>
          <span v-else-if="lastSaved">
            Last saved {{ formatTimeAgo(lastSaved) }}
          </span>
          <span v-else-if="showEditor">
            Auto-saves every 2 seconds
          </span>
        </div>
      </div>
    </div>
    
    <!-- Delete Confirmation Modal -->
    <Teleport to="body">
      <div 
        v-if="noteToDelete" 
        class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
        role="dialog"
        aria-modal="true"
        aria-labelledby="delete-note-title"
        @click.self="noteToDelete = null"
      >
        <div class="w-full max-w-md p-6 rounded-xl bg-white dark:bg-gray-800 shadow-xl">
          <div class="flex items-center gap-3 mb-4">
            <div class="w-10 h-10 rounded-full bg-red-100 dark:bg-red-900/30 flex items-center justify-center">
              <Trash2 class="w-5 h-5 text-red-600 dark:text-red-400" aria-hidden="true" />
            </div>
            <div>
              <h3 id="delete-note-title" class="text-lg font-semibold text-gray-900 dark:text-white">
                Delete Note?
              </h3>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                This action cannot be undone.
              </p>
            </div>
          </div>
          
          <p class="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Are you sure you want to permanently delete this note by 
            <strong>{{ getAuthorName(noteToDelete) }}</strong>?
          </p>
          
          <div class="flex justify-end gap-3">
            <button 
              @click="noteToDelete = null"
              class="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              Cancel
            </button>
            <button 
              @click="deleteNote"
              :disabled="deleting"
              class="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              <Loader2 v-if="deleting" class="w-4 h-4 animate-spin" aria-hidden="true" />
              {{ deleting ? 'Deleting...' : 'Delete Note' }}
            </button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
/**
 * NotesPanel Component
 * 
 * Full session notes management panel with TipTap editor integration.
 * Features auto-save, note versioning, and lock state handling.
 * 
 * Role-based permissions (Phase 10):
 * - Create note: Any CRT member
 * - Edit own note: Any CRT member
 * - Edit other's note: Admin only
 * - Delete note: Admin only
 */
import { ref, computed, watch, onMounted } from 'vue'
import { 
  FileText, 
  Lock, 
  Plus, 
  Save, 
  History,
  Loader2,
  AlertCircle,
  X,
  Pencil,
  Trash2,
} from 'lucide-vue-next'
import { notesApi } from '@/services/api'
import { NotesEditor } from '@/components/notes'
import { useAuthStore } from '@/stores'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  session: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

// =============================================================================
// Emits
// =============================================================================

const emit = defineEmits(['notes-updated'])

// =============================================================================
// Composables
// =============================================================================

const authStore = useAuthStore()

// =============================================================================
// State
// =============================================================================

const editorRef = ref(null)
const notes = ref([])
const isSessionLocked = ref(false)
const loadingNotes = ref(false)
const error = ref(null)
const saving = ref(false)
const lastSaved = ref(null)

// Current note being edited
const showEditor = ref(false)
const currentNoteId = ref(null)
const currentNoteContent = ref('')
const originalContent = ref('')
const viewingExistingNote = ref(false)

// Delete confirmation
const noteToDelete = ref(null)
const deleting = ref(false)

// =============================================================================
// Computed
// =============================================================================

const totalNotes = computed(() => notes.value.length)

const previousNotes = computed(() => {
  // If editing an existing note, exclude it from the list
  if (currentNoteId.value) {
    return notes.value.filter(n => n.id !== currentNoteId.value)
  }
  return notes.value
})

const isNoteReadonly = computed(() => {
  // Read-only if session is locked
  if (isSessionLocked.value) return true
  
  // Read-only if viewing/editing a note that is individually locked
  if (currentNoteId.value) {
    const note = notes.value.find(n => n.id === currentNoteId.value)
    if (note?.is_locked) return true
    
    // Read-only if viewing someone else's note and not admin
    if (viewingExistingNote.value && !canEditNote(note)) return true
  }
  
  return false
})

const hasUnsavedChanges = computed(() => {
  return currentNoteContent.value !== originalContent.value
})

const editorPlaceholder = computed(() => {
  if (isSessionLocked.value) {
    return 'This session is closed. Notes are read-only.'
  }
  return 'Document your observations, actions taken, and follow-up plans...'
})

// Combined loading state
const loading = computed(() => props.loading || loadingNotes.value)

// =============================================================================
// Methods
// =============================================================================

/**
 * Check if current user can edit a note.
 * Users can edit their own notes; admins can edit any note.
 */
function canEditNote(note) {
  if (!note) return false
  
  // Admin can edit any note
  if (authStore.isAdmin) return true
  
  // Users can edit their own notes
  return note.author_id === authStore.userId
}

async function loadNotes() {
  if (!props.session?.id) return
  
  loadingNotes.value = true
  error.value = null
  
  try {
    const response = await notesApi.list(props.session.id)
    notes.value = response.data.notes || []
    isSessionLocked.value = response.data.is_session_locked || false
    
    emit('notes-updated', notes.value)
  } catch (err) {
    console.error('Failed to load notes:', err)
    error.value = 'Failed to load notes. Please try again.'
  } finally {
    loadingNotes.value = false
  }
}

function startNewNote() {
  if (isSessionLocked.value) return
  
  showEditor.value = true
  currentNoteId.value = null
  currentNoteContent.value = ''
  originalContent.value = ''
  viewingExistingNote.value = false
}

function cancelNewNote() {
  showEditor.value = false
  currentNoteId.value = null
  currentNoteContent.value = ''
  originalContent.value = ''
  viewingExistingNote.value = false
}

async function viewNote(note) {
  // Fetch the full note content
  try {
    const response = await notesApi.get(note.id)
    const fullNote = response.data
    
    // Load into editor (read-only mode)
    showEditor.value = true
    currentNoteId.value = fullNote.id
    currentNoteContent.value = fullNote.content_html || fullNote.content || ''
    originalContent.value = currentNoteContent.value
    viewingExistingNote.value = true
  } catch (err) {
    console.error('Failed to load note:', err)
    error.value = 'Failed to load note. Please try again.'
  }
}

async function editNote(note) {
  if (!canEditNote(note)) return
  
  // Fetch the full note content for editing
  try {
    const response = await notesApi.get(note.id)
    const fullNote = response.data
    
    // Load into editor (edit mode)
    showEditor.value = true
    currentNoteId.value = fullNote.id
    currentNoteContent.value = fullNote.content_html || fullNote.content || ''
    originalContent.value = currentNoteContent.value
    viewingExistingNote.value = false // Not just viewing, actually editing
  } catch (err) {
    console.error('Failed to load note for editing:', err)
    error.value = 'Failed to load note. Please try again.'
  }
}

function confirmDeleteNote(note) {
  noteToDelete.value = note
}

async function deleteNote() {
  if (!noteToDelete.value || !authStore.isAdmin) return
  
  deleting.value = true
  
  try {
    await notesApi.delete(noteToDelete.value.id)
    noteToDelete.value = null
    
    // Reload notes to reflect deletion
    await loadNotes()
  } catch (err) {
    console.error('Failed to delete note:', err)
    error.value = 'Failed to delete note. Please try again.'
  } finally {
    deleting.value = false
  }
}

async function handleAutoSave(data) {
  if (!props.session?.id || isNoteReadonly.value) return
  
  saving.value = true
  
  try {
    if (currentNoteId.value) {
      // Update existing note
      await notesApi.update(currentNoteId.value, {
        content: data.content || data.content_html,
        content_html: data.content_html,
      })
    } else {
      // Create new note
      const response = await notesApi.create(props.session.id, {
        content: data.content || data.content_html,
        content_html: data.content_html,
      })
      currentNoteId.value = response.data.id
    }
    
    lastSaved.value = new Date()
    originalContent.value = currentNoteContent.value
    
    // Don't reload notes during auto-save - it causes focus loss
    // Notes will be reloaded when user navigates away or on explicit save
  } catch (err) {
    console.error('Auto-save failed:', err)
    // Don't show error for auto-save, just log it
  } finally {
    saving.value = false
  }
}

async function saveNote() {
  if (!props.session?.id || isNoteReadonly.value) return
  
  // Force save via editor
  if (editorRef.value?.forceSave) {
    await editorRef.value.forceSave()
  } else {
    // Manual save
    await handleAutoSave({
      content: currentNoteContent.value,
      content_html: currentNoteContent.value,
    })
  }
  
  // Reload notes on explicit save to update the list
  await loadNotes()
}

function getAuthorName(note) {
  // If author_name exists, use it
  return note.author_name || 'CRT Member'
}

function getInitials(name) {
  if (!name) return 'CM'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

function formatDate(dateString) {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

function formatTimeAgo(date) {
  if (!date) return ''
  
  const now = new Date()
  const diff = Math.floor((now - date) / 1000)
  
  if (diff < 5) return 'just now'
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}

// =============================================================================
// Watchers
// =============================================================================

// Watch for session changes
watch(() => props.session?.id, (newId) => {
  if (newId) {
    loadNotes()
  }
}, { immediate: true })

// Watch for session status changes (lock state)
watch(() => props.session?.status, (newStatus) => {
  isSessionLocked.value = newStatus === 'closed' || newStatus === 'archived'
})

// =============================================================================
// Lifecycle
// =============================================================================

onMounted(() => {
  if (props.session?.id) {
    loadNotes()
  }
})
</script>
