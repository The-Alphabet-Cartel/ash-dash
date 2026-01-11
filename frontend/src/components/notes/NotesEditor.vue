<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
NotesEditor - TipTap WYSIWYG Markdown Editor for CRT session notes
============================================================================
FILE VERSION: v5.0-6-6.7-3
LAST MODIFIED: 2026-01-08
PHASE: Phase 6 - Notes System
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="notes-editor flex flex-col rounded-lg border border-gray-200 dark:border-gray-600 overflow-hidden">
    <!-- Toolbar -->
    <EditorToolbar
      v-if="editor"
      :editor="editor"
      :disabled="readonly"
      :saving="saving"
      :last-saved="lastSaved"
      :is-locked="readonly"
    />

    <!-- Editor Content -->
    <div 
      class="flex-1 overflow-y-auto bg-white dark:bg-gray-800"
      :class="{ 'opacity-60 cursor-not-allowed': readonly }"
    >
      <EditorContent 
        :editor="editor" 
        class="prose prose-sm dark:prose-invert max-w-none h-full"
      />
    </div>

    <!-- Character Count (optional) -->
    <div 
      v-if="showCharCount && editor"
      class="px-3 py-1 text-xs text-gray-400 dark:text-gray-500 border-t border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-800/50"
    >
      {{ characterCount }} characters
    </div>
  </div>
</template>

<script setup>
/**
 * NotesEditor Component
 * 
 * TipTap-powered WYSIWYG Markdown editor for CRT session notes.
 * Features auto-save with debounce, lock states, and full formatting support.
 */
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import { useEditor, EditorContent } from '@tiptap/vue-3'
import StarterKit from '@tiptap/starter-kit'
import TaskList from '@tiptap/extension-task-list'
import TaskItem from '@tiptap/extension-task-item'
import Link from '@tiptap/extension-link'
import Underline from '@tiptap/extension-underline'
import Placeholder from '@tiptap/extension-placeholder'
import { useDebounceFn } from '@vueuse/core'
import EditorToolbar from './EditorToolbar.vue'

// =============================================================================
// Props & Emits
// =============================================================================

const props = defineProps({
  /**
   * Initial content (HTML format)
   */
  modelValue: {
    type: String,
    default: ''
  },
  /**
   * Whether the editor is read-only (locked)
   */
  readonly: {
    type: Boolean,
    default: false
  },
  /**
   * Placeholder text when empty
   */
  placeholder: {
    type: String,
    default: 'Start typing your session notes...'
  },
  /**
   * Auto-save delay in milliseconds
   */
  autoSaveDelay: {
    type: Number,
    default: 2000
  },
  /**
   * Show character count
   */
  showCharCount: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'save',
  'focus',
  'blur'
])

// =============================================================================
// State
// =============================================================================

const saving = ref(false)
const lastSaved = ref(null)

// =============================================================================
// TipTap Editor Setup
// =============================================================================

const editor = useEditor({
  content: props.modelValue,
  editable: !props.readonly,
  extensions: [
    StarterKit.configure({
      // Configure StarterKit options
      heading: {
        levels: [1, 2, 3]
      },
      bulletList: {
        keepMarks: true,
        keepAttributes: false
      },
      orderedList: {
        keepMarks: true,
        keepAttributes: false
      }
    }),
    TaskList,
    TaskItem.configure({
      nested: true
    }),
    Link.configure({
      openOnClick: false,
      HTMLAttributes: {
        class: 'text-purple-500 hover:text-purple-600 underline'
      }
    }),
    Underline,
    Placeholder.configure({
      placeholder: props.placeholder
    })
  ],
  editorProps: {
    attributes: {
      class: 'min-h-[350px] max-h-[350px] p-4 focus:outline-none overflow-y-auto'
    }
  },
  onUpdate: ({ editor }) => {
    const html = editor.getHTML()
    emit('update:modelValue', html)
    
    // Trigger auto-save
    if (!props.readonly) {
      debouncedSave()
    }
  },
  onFocus: () => {
    emit('focus')
  },
  onBlur: () => {
    emit('blur')
  }
})

// =============================================================================
// Auto-Save
// =============================================================================

const debouncedSave = useDebounceFn(async () => {
  if (props.readonly || !editor.value) return
  
  saving.value = true
  try {
    const content = editor.value.getHTML()
    await emit('save', {
      content_html: content,
      content: getMarkdownContent()
    })
    lastSaved.value = new Date()
  } catch (error) {
    console.error('Auto-save failed:', error)
  } finally {
    saving.value = false
  }
}, props.autoSaveDelay)

/**
 * Convert HTML content to approximate Markdown
 * Note: For full accuracy, consider using a library like turndown
 */
function getMarkdownContent() {
  if (!editor.value) return ''
  
  // Get text content as a simple fallback
  // In production, consider using turndown for proper HTML-to-MD conversion
  return editor.value.getText()
}

// =============================================================================
// Computed
// =============================================================================

const characterCount = computed(() => {
  if (!editor.value) return 0
  return editor.value.storage.characterCount?.characters() || 
         editor.value.getText().length
})

// =============================================================================
// Watchers
// =============================================================================

// Watch for external content changes
watch(() => props.modelValue, (newContent) => {
  if (!editor.value) return
  
  const currentContent = editor.value.getHTML()
  if (newContent !== currentContent) {
    editor.value.commands.setContent(newContent, false)
  }
})

// Watch for readonly changes
watch(() => props.readonly, (newVal) => {
  if (editor.value) {
    editor.value.setEditable(!newVal)
  }
})

// =============================================================================
// Lifecycle
// =============================================================================

onUnmounted(() => {
  if (editor.value) {
    editor.value.destroy()
  }
})

// =============================================================================
// Public Methods (exposed for parent components)
// =============================================================================

/**
 * Force save the current content
 */
async function forceSave() {
  if (props.readonly || !editor.value) return false
  
  saving.value = true
  try {
    await emit('save', {
      content_html: editor.value.getHTML(),
      content: getMarkdownContent()
    })
    lastSaved.value = new Date()
    return true
  } catch (error) {
    console.error('Force save failed:', error)
    return false
  } finally {
    saving.value = false
  }
}

/**
 * Clear editor content
 */
function clear() {
  if (editor.value && !props.readonly) {
    editor.value.commands.clearContent()
  }
}

/**
 * Focus the editor
 */
function focus() {
  if (editor.value) {
    editor.value.commands.focus()
  }
}

// Expose public methods
defineExpose({
  forceSave,
  clear,
  focus,
  editor
})
</script>

<style>
/* TipTap Editor Base Styles */
.notes-editor .ProseMirror {
  min-height: 350px;
  max-height: 350px;
  overflow-y: auto;
  outline: none;
}

/* Compact list spacing */
.notes-editor .ProseMirror ul,
.notes-editor .ProseMirror ol {
  margin: 0.5rem 0;
  padding-left: 1.5rem;
}

.notes-editor .ProseMirror li {
  margin: 0.125rem 0;
}

.notes-editor .ProseMirror li p {
  margin: 0;
}

/* Placeholder styling */
.notes-editor .ProseMirror p.is-editor-empty:first-child::before {
  content: attr(data-placeholder);
  float: left;
  color: #9ca3af;
  pointer-events: none;
  height: 0;
}

/* Dark mode placeholder */
.dark .notes-editor .ProseMirror p.is-editor-empty:first-child::before {
  color: #6b7280;
}

/* Task list styling - compact */
.notes-editor .ProseMirror ul[data-type="taskList"] {
  list-style: none;
  padding: 0;
  margin: 0.5rem 0;
}

.notes-editor .ProseMirror ul[data-type="taskList"] li {
  display: flex;
  align-items: flex-start;
  gap: 0.5rem;
  margin: 0.125rem 0;
}

.notes-editor .ProseMirror ul[data-type="taskList"] li > label {
  flex: 0 0 auto;
  margin-top: 0.25rem;
}

.notes-editor .ProseMirror ul[data-type="taskList"] li > div {
  flex: 1 1 auto;
}

/* Checkbox styling */
.notes-editor .ProseMirror ul[data-type="taskList"] input[type="checkbox"] {
  cursor: pointer;
  accent-color: #a855f7;
}

/* Code block styling */
.notes-editor .ProseMirror pre {
  background: #1f2937;
  color: #e5e7eb;
  padding: 0.75rem 1rem;
  border-radius: 0.5rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.875rem;
  overflow-x: auto;
}

.notes-editor .ProseMirror code {
  background: #374151;
  color: #f3f4f6;
  padding: 0.125rem 0.25rem;
  border-radius: 0.25rem;
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
  font-size: 0.875em;
}

.notes-editor .ProseMirror pre code {
  background: transparent;
  padding: 0;
}

/* Horizontal rule */
.notes-editor .ProseMirror hr {
  border: none;
  border-top: 2px solid #e5e7eb;
  margin: 1.5rem 0;
}

.dark .notes-editor .ProseMirror hr {
  border-top-color: #4b5563;
}

/* Blockquote styling */
.notes-editor .ProseMirror blockquote {
  border-left: 4px solid #a855f7;
  padding-left: 1rem;
  margin-left: 0;
  color: #6b7280;
}

.dark .notes-editor .ProseMirror blockquote {
  color: #9ca3af;
}

/* Link styling */
.notes-editor .ProseMirror a {
  color: #a855f7;
  text-decoration: underline;
}

.notes-editor .ProseMirror a:hover {
  color: #9333ea;
}
</style>
