// https://nuxt.com/docs/guide/concepts/auto-imports
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  ssr: false,
  compatibilityDate: '2024-04-03',
  nitro: {
    preset: 'static',
    prerender: {
      crawlLinks: true
    },
    compressPublicAssets: true
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
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'https://boundary-graph.onrender.com',
    },
  },
  modules: [
    [
      '@nuxtjs/color-mode',
      {
        preference: 'light',
        fallback: 'light',
        classSuffix: '',
      }
    ],
  ],
  imports: {
    autoImport: true,
  },
  experimental: {
    payloadExtraction: false,
    viewTransition: true
  },
  routeRules: {
    '/': { prerender: true },
    '/batsmen': { prerender: true },
    '/bowlers': { prerender: true },
    '/teams': { prerender: true },
    '/venues': { prerender: true },
    '/h2h': { prerender: true },
    '/player-search': { prerender: true }
  },
  app: {
    head: {
      title: 'Boundary Graph',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=5, user-scalable=yes, viewport-fit=cover' },
        { name: 'description', content: 'IPL Analytics dashboard' },
        { name: 'theme-color', content: '#FBBF24' },
        { name: 'mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-capable', content: 'yes' },
        { name: 'apple-mobile-web-app-status-bar-style', content: 'default' },
        { name: 'format-detection', content: 'telephone=no' },
        // Open Graph meta tags for social media sharing
        { property: 'og:title', content: 'Boundary Graph - Cricket Analytics Dashboard' },
        { property: 'og:description', content: 'IPL Analytics dashboard with comprehensive player statistics, team insights, and match analysis' },
        { property: 'og:image', content: 'https://boundary-graph.netlify.app/bg-thumbnail.webp' },
        { property: 'og:image:width', content: '1200' },
        { property: 'og:image:height', content: '630' },
        { property: 'og:image:type', content: 'image/webp' },
        { property: 'og:url', content: 'https://boundary-graph.netlify.app' },
        { property: 'og:type', content: 'website' },
        { property: 'og:site_name', content: 'Boundary Graph' },
        // Twitter Card meta tags
        { name: 'twitter:card', content: 'summary_large_image' },
        { name: 'twitter:title', content: 'Boundary Graph - Cricket Analytics Dashboard' },
        { name: 'twitter:description', content: 'IPL Analytics dashboard with comprehensive player statistics, team insights, and match analysis' },
        { name: 'twitter:image', content: 'https://boundary-graph.netlify.app/bg-thumbnail.webp' },
        // Additional SEO meta tags
        { name: 'keywords', content: 'cricket, analytics, statistics, IPL, dashboard, boundary graph, sports data' },
        { name: 'author', content: 'Boundary Graph' },
      ],
      link: [
        { rel: 'manifest', href: '/manifest.json' },
        { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
        { rel: 'apple-touch-icon', href: '/bg-logo.png' },
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap' },
        { rel: 'preconnect', href: 'https://boundary-graph.onrender.com' },
      ],
      script: [
        {
          innerHTML: `
            // Prevent FOUC and handle loading
            document.documentElement.classList.add('loading');
            window.addEventListener('load', () => {
              document.documentElement.classList.remove('loading');
            });
            
            // Add basic mobile detection
            if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
              document.documentElement.classList.add('mobile-device');
            }
          `,
          type: 'text/javascript'
        }
      ],
    },
  },
})
