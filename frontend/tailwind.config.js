/**
 * ============================================================================
 * Ash-DASH: Discord Crisis Detection Dashboard
 * The Alphabet Cartel - https://discord.gg/alphabetcartel | alphabetcartel.org
 * ============================================================================
 *
 * TailwindCSS Configuration - Custom theme with severity colors
 * ----------------------------------------------------------------------------
 * FILE VERSION: v5.0-3-3.1-1
 * LAST MODIFIED: 2026-01-07
 * PHASE: Phase 3 - Frontend Foundation
 * Repository: https://github.com/the-alphabet-cartel/ash-dash
 * ============================================================================
 */

/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{vue,js,ts,jsx,tsx}',
  ],
  
  // Enable dark mode via class
  darkMode: 'class',
  
  theme: {
    extend: {
      colors: {
        // Severity colors for crisis levels
        severity: {
          critical: {
            DEFAULT: '#9333EA',
            light: '#A855F7',
            dark: '#7C3AED',
            bg: 'rgb(88 28 135 / 0.5)',
          },
          high: {
            DEFAULT: '#EF4444',
            light: '#F87171',
            dark: '#DC2626',
            bg: 'rgb(127 29 29 / 0.5)',
          },
          medium: {
            DEFAULT: '#F59E0B',
            light: '#FBBF24',
            dark: '#D97706',
            bg: 'rgb(120 53 15 / 0.5)',
          },
          low: {
            DEFAULT: '#22C55E',
            light: '#4ADE80',
            dark: '#16A34A',
            bg: 'rgb(20 83 45 / 0.5)',
          },
          safe: {
            DEFAULT: '#6B7280',
            light: '#9CA3AF',
            dark: '#4B5563',
            bg: 'rgb(55 65 81 / 0.5)',
          },
        },
        // Brand gradient colors
        brand: {
          purple: '#9333EA',
          pink: '#EC4899',
          orange: '#F97316',
        },
      },
      
      // Custom spacing for layout
      spacing: {
        'sidebar': '256px',
        'header': '64px',
      },
      
      // Custom border radius
      borderRadius: {
        'card': '12px',
      },
      
      // Custom font sizes
      fontSize: {
        'page-title': ['1.5rem', { lineHeight: '2rem', fontWeight: '700' }],
        'section-title': ['1.125rem', { lineHeight: '1.75rem', fontWeight: '600' }],
      },
      
      // Animation for pulse effect on status indicators
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      },
    },
  },
  
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
