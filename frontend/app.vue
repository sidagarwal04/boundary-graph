<script setup lang="ts">
import { onMounted } from 'vue'

const config = useRuntimeConfig()

onMounted(() => {
  // Initial "Wake up" call to Render backend
  const wakeUpBackend = () => {
    const apiBase = config.public.apiBase
    if (apiBase && apiBase.includes('render.com')) {
      console.log('💓 Sending heartbeat to Render backend...')
      $fetch(`${apiBase}/health`).catch(() => {})
    }
  }

  // Ping immediately on load
  wakeUpBackend()

  // Keep it awake every 10 minutes (Render timeout is 15 mins)
  const heartbeat = setInterval(wakeUpBackend, 10 * 60 * 1000)

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
