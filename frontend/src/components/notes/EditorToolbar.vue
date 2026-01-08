<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
EditorToolbar - Formatting toolbar for TipTap editor
============================================================================
FILE VERSION: v5.0-6-6.2-1
LAST MODIFIED: 2026-01-08
PHASE: Phase 6 - Notes System
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div 
    class="editor-toolbar flex flex-wrap items-center gap-1 p-2 bg-gray-50 dark:bg-gray-800/80 border-b border-gray-200 dark:border-gray-700"
    :class="{ 'opacity-50': disabled }"
  >
    <!-- Text Formatting Group -->
    <div class="flex items-center gap-0.5 pr-2 border-r border-gray-300 dark:border-gray-600">
      <ToolbarButton
        title="Bold (Ctrl+B)"
        :active="editor?.isActive('bold')"
        :disabled="disabled"
        @click="toggleBold"
      >
        <Bold class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Italic (Ctrl+I)"
        :active="editor?.isActive('italic')"
        :disabled="disabled"
        @click="toggleItalic"
      >
        <Italic class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Underline (Ctrl+U)"
        :active="editor?.isActive('underline')"
        :disabled="disabled"
        @click="toggleUnderline"
      >
        <UnderlineIcon class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Strikethrough"
        :active="editor?.isActive('strike')"
        :disabled="disabled"
        @click="toggleStrike"
      >
        <Strikethrough class="w-4 h-4" />
      </ToolbarButton>
    </div>

    <!-- Headers Group -->
    <div class="flex items-center gap-0.5 px-2 border-r border-gray-300 dark:border-gray-600">
      <ToolbarButton
        title="Heading 1"
        :active="editor?.isActive('heading', { level: 1 })"
        :disabled="disabled"
        @click="toggleHeading(1)"
      >
        <Heading1 class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Heading 2"
        :active="editor?.isActive('heading', { level: 2 })"
        :disabled="disabled"
        @click="toggleHeading(2)"
      >
        <Heading2 class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Heading 3"
        :active="editor?.isActive('heading', { level: 3 })"
        :disabled="disabled"
        @click="toggleHeading(3)"
      >
        <Heading3 class="w-4 h-4" />
      </ToolbarButton>
    </div>

    <!-- Lists Group -->
    <div class="flex items-center gap-0.5 px-2 border-r border-gray-300 dark:border-gray-600">
      <ToolbarButton
        title="Bullet List"
        :active="editor?.isActive('bulletList')"
        :disabled="disabled"
        @click="toggleBulletList"
      >
        <List class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Numbered List"
        :active="editor?.isActive('orderedList')"
        :disabled="disabled"
        @click="toggleOrderedList"
      >
        <ListOrdered class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Task List"
        :active="editor?.isActive('taskList')"
        :disabled="disabled"
        @click="toggleTaskList"
      >
        <CheckSquare class="w-4 h-4" />
      </ToolbarButton>
    </div>

    <!-- Blocks Group -->
    <div class="flex items-center gap-0.5 px-2 border-r border-gray-300 dark:border-gray-600">
      <ToolbarButton
        title="Code Block"
        :active="editor?.isActive('codeBlock')"
        :disabled="disabled"
        @click="toggleCodeBlock"
      >
        <Code class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Blockquote"
        :active="editor?.isActive('blockquote')"
        :disabled="disabled"
        @click="toggleBlockquote"
      >
        <Quote class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Horizontal Rule"
        :disabled="disabled"
        @click="insertHorizontalRule"
      >
        <Minus class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Link"
        :active="editor?.isActive('link')"
        :disabled="disabled"
        @click="toggleLink"
      >
        <LinkIcon class="w-4 h-4" />
      </ToolbarButton>
    </div>

    <!-- Undo/Redo Group -->
    <div class="flex items-center gap-0.5 px-2 border-r border-gray-300 dark:border-gray-600">
      <ToolbarButton
        title="Undo (Ctrl+Z)"
        :disabled="disabled || !canUndo"
        @click="undo"
      >
        <Undo class="w-4 h-4" />
      </ToolbarButton>
      
      <ToolbarButton
        title="Redo (Ctrl+Shift+Z)"
        :disabled="disabled || !canRedo"
        @click="redo"
      >
        <Redo class="w-4 h-4" />
      </ToolbarButton>
    </div>

    <!-- Spacer -->
    <div class="flex-1" />

    <!-- Save Status -->
    <div class="flex items-center gap-2 pl-2">
      <!-- Saving indicator -->
      <span v-if="saving" class="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1">
        <Loader2 class="w-3 h-3 animate-spin" />
        Saving...
      </span>
      
      <!-- Last saved -->
      <span 
        v-else-if="lastSaved" 
        class="text-sm text-gray-400 dark:text-gray-500 flex items-center gap-1"
      >
        <Check class="w-3 h-3 text-green-500" />
        Saved {{ formatTimeAgo(lastSaved) }}
      </span>

      <!-- Lock indicator -->
      <span 
        v-if="isLocked" 
        class="text-sm text-yellow-600 dark:text-yellow-500 flex items-center gap-1 ml-2"
      >
        <Lock class="w-3 h-3" />
        Locked
      </span>
    </div>
  </div>

  <!-- Link Modal -->
  <Teleport to="body">
    <div 
      v-if="showLinkModal" 
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/50"
      @click.self="closeLinkModal"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 w-full max-w-md mx-4">
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          {{ editor?.isActive('link') ? 'Edit Link' : 'Add Link' }}
        </h3>
        
        <input
          ref="linkInput"
          v-model="linkUrl"
          type="url"
          placeholder="https://example.com"
          class="w-full px-3 py-2 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-purple-500 focus:border-transparent"
          @keydown.enter="applyLink"
          @keydown.escape="closeLinkModal"
        />
        
        <div class="flex justify-end gap-2 mt-4">
          <button
            v-if="editor?.isActive('link')"
            @click="removeLink"
            class="px-4 py-2 text-sm font-medium text-red-600 hover:text-red-700 dark:text-red-400 dark:hover:text-red-300"
          >
            Remove
          </button>
          <button
            @click="closeLinkModal"
            class="px-4 py-2 text-sm font-medium text-gray-600 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-300"
          >
            Cancel
          </button>
          <button
            @click="applyLink"
            class="px-4 py-2 text-sm font-medium bg-purple-600 text-white rounded-lg hover:bg-purple-700"
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
/**
 * EditorToolbar Component
 * 
 * Formatting toolbar for the TipTap editor with all standard
 * text formatting, list, and block-level controls.
 */
import { ref, computed, nextTick } from 'vue'
import {
  Bold,
  Italic,
  Underline as UnderlineIcon,
  Strikethrough,
  Heading1,
  Heading2,
  Heading3,
  List,
  ListOrdered,
  CheckSquare,
  Code,
  Quote,
  Minus,
  Link as LinkIcon,
  Undo,
  Redo,
  Loader2,
  Check,
  Lock
} from 'lucide-vue-next'
import ToolbarButton from './ToolbarButton.vue'

// =============================================================================
// Props
// =============================================================================

const props = defineProps({
  editor: {
    type: Object,
    default: null
  },
  disabled: {
    type: Boolean,
    default: false
  },
  saving: {
    type: Boolean,
    default: false
  },
  lastSaved: {
    type: Date,
    default: null
  },
  isLocked: {
    type: Boolean,
    default: false
  }
})

// =============================================================================
// State
// =============================================================================

const showLinkModal = ref(false)
const linkUrl = ref('')
const linkInput = ref(null)

// =============================================================================
// Computed
// =============================================================================

const canUndo = computed(() => props.editor?.can().undo())
const canRedo = computed(() => props.editor?.can().redo())

// =============================================================================
// Formatting Commands
// =============================================================================

function toggleBold() {
  props.editor?.chain().focus().toggleBold().run()
}

function toggleItalic() {
  props.editor?.chain().focus().toggleItalic().run()
}

function toggleUnderline() {
  props.editor?.chain().focus().toggleUnderline().run()
}

function toggleStrike() {
  props.editor?.chain().focus().toggleStrike().run()
}

function toggleHeading(level) {
  props.editor?.chain().focus().toggleHeading({ level }).run()
}

function toggleBulletList() {
  props.editor?.chain().focus().toggleBulletList().run()
}

function toggleOrderedList() {
  props.editor?.chain().focus().toggleOrderedList().run()
}

function toggleTaskList() {
  props.editor?.chain().focus().toggleTaskList().run()
}

function toggleCodeBlock() {
  props.editor?.chain().focus().toggleCodeBlock().run()
}

function toggleBlockquote() {
  props.editor?.chain().focus().toggleBlockquote().run()
}

function insertHorizontalRule() {
  props.editor?.chain().focus().setHorizontalRule().run()
}

function undo() {
  props.editor?.chain().focus().undo().run()
}

function redo() {
  props.editor?.chain().focus().redo().run()
}

// =============================================================================
// Link Handling
// =============================================================================

function toggleLink() {
  // Get current link URL if editing existing link
  const previousUrl = props.editor?.getAttributes('link').href || ''
  linkUrl.value = previousUrl
  showLinkModal.value = true
  
  nextTick(() => {
    linkInput.value?.focus()
    linkInput.value?.select()
  })
}

function applyLink() {
  if (!linkUrl.value) {
    removeLink()
    return
  }
  
  // Add https:// if no protocol specified
  let url = linkUrl.value
  if (!/^https?:\/\//i.test(url)) {
    url = 'https://' + url
  }
  
  props.editor
    ?.chain()
    .focus()
    .extendMarkRange('link')
    .setLink({ href: url })
    .run()
  
  closeLinkModal()
}

function removeLink() {
  props.editor?.chain().focus().unsetLink().run()
  closeLinkModal()
}

function closeLinkModal() {
  showLinkModal.value = false
  linkUrl.value = ''
}

// =============================================================================
// Utilities
// =============================================================================

function formatTimeAgo(date) {
  if (!date) return ''
  
  const now = new Date()
  const diff = Math.floor((now - date) / 1000) // seconds
  
  if (diff < 5) return 'just now'
  if (diff < 60) return `${diff}s ago`
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`
  
  return date.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
}
</script>
