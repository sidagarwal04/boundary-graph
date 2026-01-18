// https://nuxt.com/docs/guide/concepts/auto-imports
export default defineNuxtConfig({
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
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
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
      title: 'IPL Cricket Dashboard',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Professional IPL cricket analytics dashboard' },
      ],
    },
  },
})
