import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  base: './',
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: false,
  },
  server: {
    port: 5173,
    strictPort: true,
  },
  watch: {
    ignored: ['**/dist-electron/**', '**/dist/**', '**/node_modules/**'],
  },
})
