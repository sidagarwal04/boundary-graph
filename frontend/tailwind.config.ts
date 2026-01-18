/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      colors: {
        cricket: {
          navy: '#0f172a',
          orange: '#ea580c',
          red: '#dc2626',
          gold: '#fbbf24',
        }
      }
    },
  },
  plugins: [],
}
