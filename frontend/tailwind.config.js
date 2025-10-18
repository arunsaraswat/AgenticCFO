/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Legacy primary colors (keeping for backwards compatibility)
        primary: {
          50: '#eff6ff',
          100: '#dbeafe',
          200: '#bfdbfe',
          300: '#93c5fd',
          400: '#60a5fa',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#1e3a8a',
        },
        // Agentic CFO Design System Colors
        // Primary Blues (Data Visualization)
        'cfo-blue': {
          deep: '#1F4E78',      // Primary brand, headers, high values
          medium: '#4472C4',    // Standard data bars, primary actions
          light: '#8AB4F8',     // Secondary elements, low values
          sky: '#B4D4FF',       // Backgrounds, hover states
        },
        // Semantic Colors
        'cfo-red': '#C00000',       // Warnings, negative values, over-limit
        'cfo-orange': '#FF7043',    // Alerts, medium priority
        'cfo-green': '#375623',     // Success, positive trends, recommendations
        'cfo-grey': '#44546A',      // Neutral information, secondary text
        // Neutrals
        'cfo-neutral': {
          dark: '#2C2C2C',      // Primary text
          medium: '#6B6B6B',    // Secondary text
          light: '#E0E0E0',     // Borders, dividers
          'off-white': '#F5F5F5', // Backgrounds, panels
        },
      },
      fontSize: {
        // Typography Scale: 48/24/16/14/12/10px
        'hero': ['48px', { lineHeight: '56px', fontWeight: '700' }],     // Hero Numbers
        'title': ['24px', { lineHeight: '32px', fontWeight: '400' }],    // Page Title
        'section': ['16px', { lineHeight: '24px', fontWeight: '600' }],  // Section Headers
        'body': ['14px', { lineHeight: '20px', fontWeight: '400' }],     // Body Text
        'small': ['12px', { lineHeight: '16px', fontWeight: '400' }],    // Small Text
        'micro': ['10px', { lineHeight: '14px', fontWeight: '400' }],    // Micro Text
      },
      borderRadius: {
        'card': '8px',    // Cards
        'button': '4px',  // Buttons
      },
      boxShadow: {
        'card': '0 2px 8px rgba(0, 0, 0, 0.08)',  // Subtle elevation
      },
      transitionTimingFunction: {
        'cfo': 'cubic-bezier(0.4, 0.0, 0.2, 1)',  // Material Design standard
      },
    },
  },
  plugins: [],
}
