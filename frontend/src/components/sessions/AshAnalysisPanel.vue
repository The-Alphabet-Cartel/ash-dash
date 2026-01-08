<!--
============================================================================
Ash-DASH: Discord Crisis Detection Dashboard
The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
============================================================================
AshAnalysisPanel - Display Ash-NLP analysis data for a session
============================================================================
FILE VERSION: v5.0-5-5.5-1
LAST MODIFIED: 2026-01-07
PHASE: Phase 5 - Session Management
Repository: https://github.com/the-alphabet-cartel/ash-dash
============================================================================
-->

<template>
  <div class="card p-6">
    <h3 class="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
      <Activity class="w-5 h-5 text-purple-500" />
      Ash Analysis
    </h3>

    <!-- Loading State -->
    <div v-if="loading" class="space-y-3 animate-pulse">
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-2/3" />
      <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2" />
      <div class="h-20 bg-gray-200 dark:bg-gray-700 rounded" />
    </div>

    <!-- No Analysis Data -->
    <div v-else-if="!analysis" class="text-center py-8 text-gray-500 dark:text-gray-400">
      <AlertCircle class="w-12 h-12 mx-auto mb-3 text-gray-300 dark:text-gray-600" />
      <p>No analysis data available</p>
    </div>

    <!-- Content -->
    <div v-else class="space-y-4">
      <!-- Scores -->
      <div class="grid grid-cols-2 gap-4">
        <!-- Crisis Score -->
        <div class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Crisis Score</p>
          <p :class="['text-2xl font-bold', crisisScoreClass]">
            {{ formatScore(analysis.crisis_score) }}
          </p>
        </div>

        <!-- Confidence -->
        <div class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Confidence</p>
          <p class="text-2xl font-bold text-gray-900 dark:text-white">
            {{ formatPercent(analysis.confidence) }}
          </p>
        </div>
      </div>

      <!-- Severity -->
      <div class="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
        <span class="text-sm text-gray-500 dark:text-gray-400">Severity Level</span>
        <SeverityBadge :severity="analysis.severity" />
      </div>

      <!-- Conflict Warning -->
      <div 
        v-if="analysis.conflict_analysis?.has_conflicts"
        class="p-3 rounded-lg bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800"
      >
        <div class="flex items-start gap-2">
          <AlertTriangle class="w-5 h-5 text-yellow-600 dark:text-yellow-400 flex-shrink-0 mt-0.5" />
          <div>
            <p class="text-sm font-medium text-yellow-800 dark:text-yellow-200">
              Model Disagreement Detected
            </p>
            <p class="text-xs text-yellow-700 dark:text-yellow-300 mt-1">
              {{ analysis.conflict_analysis.summary || 'Models have conflicting assessments. Review signals carefully.' }}
            </p>
          </div>
        </div>
      </div>

      <!-- Signals -->
      <div v-if="hasSignals" class="space-y-2">
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">Key Signals</p>
        <div class="flex flex-wrap gap-2">
          <span 
            v-for="(signal, key) in analysis.signals" 
            :key="key"
            :class="[
              'px-2 py-1 rounded text-xs font-medium',
              getSignalClass(signal)
            ]"
          >
            {{ signal.label || key }}
          </span>
        </div>
      </div>

      <!-- Explanation Summary -->
      <div v-if="hasExplanation" class="space-y-2">
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">Analysis Summary</p>
        <div class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50 text-sm text-gray-600 dark:text-gray-400">
          <p v-if="analysis.explanation.summary">{{ analysis.explanation.summary }}</p>
          <p v-else-if="analysis.explanation.primary_concern">
            Primary concern: {{ analysis.explanation.primary_concern }}
          </p>
        </div>
      </div>

      <!-- Consensus (if available) -->
      <div v-if="analysis.consensus" class="space-y-2">
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300">Model Consensus</p>
        <div class="p-3 rounded-lg bg-gray-50 dark:bg-gray-700/50">
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-500 dark:text-gray-400">Agreement</span>
            <span class="font-medium text-gray-900 dark:text-white">
              {{ formatPercent(analysis.consensus.agreement_score) }}
            </span>
          </div>
          <div v-if="analysis.consensus.method" class="flex items-center justify-between text-sm mt-1">
            <span class="text-gray-500 dark:text-gray-400">Method</span>
            <span class="text-gray-700 dark:text-gray-300 capitalize">
              {{ analysis.consensus.method }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { Activity, AlertCircle, AlertTriangle } from 'lucide-vue-next'
import { SeverityBadge } from '@/components/sessions'

const props = defineProps({
  analysis: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  }
})

const crisisScoreClass = computed(() => {
  if (!props.analysis?.crisis_score) return 'text-gray-500'
  const score = props.analysis.crisis_score
  if (score >= 0.7) return 'text-purple-600 dark:text-purple-400'
  if (score >= 0.5) return 'text-red-600 dark:text-red-400'
  if (score >= 0.3) return 'text-yellow-600 dark:text-yellow-400'
  return 'text-green-600 dark:text-green-400'
})

const hasSignals = computed(() => {
  return props.analysis?.signals && Object.keys(props.analysis.signals).length > 0
})

const hasExplanation = computed(() => {
  return props.analysis?.explanation && 
    (props.analysis.explanation.summary || props.analysis.explanation.primary_concern)
})

function formatScore(score) {
  if (score === null || score === undefined) return '—'
  return score.toFixed(2)
}

function formatPercent(value) {
  if (value === null || value === undefined) return '—'
  return `${Math.round(value * 100)}%`
}

function getSignalClass(signal) {
  const severity = signal?.severity || signal?.level || 'neutral'
  switch (severity) {
    case 'critical':
    case 'high':
      return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
    case 'medium':
    case 'warning':
      return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    case 'low':
    case 'positive':
      return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    default:
      return 'bg-gray-100 text-gray-800 dark:bg-gray-700/30 dark:text-gray-300'
  }
}
</script>
