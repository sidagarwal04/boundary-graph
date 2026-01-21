// https://nuxt.com/docs/guide/concepts/auto-imports
export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2024-04-03',
  nitro: {
    preset: 'static'
  },
  devtools: { enabled: true },
  css: ['~/assets/css/main.css'],
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 
        (process.env.NODE_ENV === 'production' 
          ? 'https://boundary-graph.onrender.com' 
          : 'http://localhost:8000'),
    },
  },
  modules: [
    '@nuxtjs/color-mode',
  ],
  colorMode: {
    preference: 'light',
    fallback: 'light',
    classSuffix: '',
  },
  imports: {
    autoImport: true,
  },
  app: {
    head: {
      title: 'Boundary Graph',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Professional cricket analytics dashboard' },
        { name: 'theme-color', content: '#FBBF24' },
      ],
      link: [
        { rel: 'manifest', href: '/manifest.json' },
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap' }
      ],
    },
  },
})
