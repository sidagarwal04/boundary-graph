<template>
  <div class="fixed inset-0 flex items-center justify-center bg-gradient-to-br from-amber-50 to-orange-50 z-50">
    <div class="text-center max-w-md px-4">
      <!-- Logo/Icon -->
      <div class="mb-6">
        <div class="inline-flex items-center justify-center w-20 h-20 rounded-full bg-gradient-to-br from-amber-100 to-orange-100 animate-pulse">
          <svg class="w-10 h-10 text-amber-600 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
        </div>
      </div>

      <!-- Main Title -->
      <h1 class="text-3xl font-bold text-gray-900 mb-3">
        Waking up the service
      </h1>

      <!-- Subtitle -->
      <p class="text-lg text-gray-600 mb-8">
        Kindly wait...
      </p>

      <!-- Progress Dots -->
      <div class="flex justify-center gap-2 mb-8">
        <div class="w-3 h-3 rounded-full bg-amber-400 animate-bounce" style="animation-delay: 0s"></div>
        <div class="w-3 h-3 rounded-full bg-amber-400 animate-bounce" style="animation-delay: 0.2s"></div>
        <div class="w-3 h-3 rounded-full bg-amber-400 animate-bounce" style="animation-delay: 0.4s"></div>
      </div>

      <!-- Status Message -->
      <p class="text-sm text-gray-500 mb-6">
        This usually takes 30-60 seconds on first load
      </p>

      <!-- Decorative Elements -->
      <div class="space-y-2 text-sm text-gray-400">
        <p>🏏 Initializing cricket analytics engine...</p>
        <p>📊 Loading database connections...</p>
        <p>⚡ Optimizing performance...</p>
      </div>

      <!-- Error message if applicable -->
      <div v-if="error" class="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg">
        <p class="text-red-600 text-sm">{{ error }}</p>
        <button
          @click="$router.go(0)"
          class="mt-3 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition text-sm font-medium"
        >
          Refresh Page
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  error?: string | null
}

withDefaults(defineProps<Props>(), {
  error: null
})
</script>
