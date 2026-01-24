<script setup lang="ts">
import { onMounted, onUnmounted } from 'vue'

const config = useRuntimeConfig()

onMounted(async () => {
  // Register service worker for caching and offline support
  if ('serviceWorker' in navigator) {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js')
      console.log('✅ Service Worker registered:', registration)
      
      // Handle service worker updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              console.log('🔄 New service worker available. Refreshing...')
              // Auto-refresh for seamless updates
              window.location.reload()
            }
          })
        }
      })
    } catch (error) {
      console.log('❌ Service Worker registration failed:', error)
    }
  }

  // Initial "Wake up" call to Render backend
  const wakeUpBackend = () => {
    const apiBase = config.public.apiBase as string
    if (apiBase && apiBase.includes('render.com')) {
      console.log('💓 Sending heartbeat to Render backend...')
      $fetch(`${apiBase}/health`).catch(() => {})
    }
  }

  // Ping immediately on load
  wakeUpBackend()

  // Keep it awake every 10 minutes (Render timeout is 15 mins)
  const heartbeat = setInterval(wakeUpBackend, 10 * 60 * 1000)

  // Mobile-specific optimizations
  if ('requestIdleCallback' in window) {
    // Pre-cache critical API data during idle time
    requestIdleCallback(async () => {
      try {
        console.log('🔄 Pre-caching critical data...')
        await Promise.allSettled([
          $fetch(`${config.public.apiBase}/api/overview`),
          $fetch(`${config.public.apiBase}/api/batsmen/top?limit=20`),
          $fetch(`${config.public.apiBase}/api/bowlers/top?limit=20`)
        ])
        console.log('✅ Pre-caching completed')
      } catch (error) {
        console.log('⚠️ Pre-caching failed:', error)
      }
    })
  }

  // Handle mobile connection changes
  if ('connection' in navigator) {
    const connection = (navigator as any).connection
    
    const handleConnectionChange = () => {
      const { effectiveType, downlink } = connection
      console.log(`📶 Connection: ${effectiveType}, Speed: ${downlink}Mbps`)
      
      // Adjust behavior for slow connections
      if (effectiveType === '2g' || effectiveType === 'slow-2g') {
        document.documentElement.classList.add('slow-connection')
        console.log('⚠️ Slow connection detected - reducing animations')
      } else {
        document.documentElement.classList.remove('slow-connection')
      }
    }
    
    connection.addEventListener('change', handleConnectionChange)
    handleConnectionChange() // Initial check
  }

  // Clean up interval on unmount
  onUnmounted(() => {
    clearInterval(heartbeat)
  })
})
</script>

<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>
