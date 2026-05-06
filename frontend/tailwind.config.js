/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        bg:           '#0f1117',
        surface:      '#1a1d27',
        surface2:     '#212535',
        border:       '#2a2f42',
        accent:       '#3b82f6',
        'accent-hover': '#60a5fa',
        success:      '#22c55e',
        error:        '#ef4444',
        warning:      '#f59e0b',
        text:         '#e2e8f6',
        'text-dim':   '#6b7a94',
        'text-muted': '#3a4560',
        'msg-ai':     '#1a1d27',
        'msg-user':   '#1e3a5f',
        'sql-bg':     '#0d1117',
      },
      fontFamily: {
        sans: ['DM Sans', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'Consolas', 'monospace'],
      },
      borderRadius: {
        card: '12px',
      },
    },
  },
  plugins: [],
}
