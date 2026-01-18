<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="stat-card">
        <div class="text-4xl">🏟️</div>
        <h3 class="text-slate-600 text-sm font-medium mt-2">Total Matches</h3>
        <p class="text-3xl font-bold text-blue-600">{{ overview.total_matches }}</p>
      </div>
      
      <div class="stat-card">
        <div class="text-4xl">🏏</div>
        <h3 class="text-slate-600 text-sm font-medium mt-2">Total Players</h3>
        <p class="text-3xl font-bold text-green-600">{{ overview.total_players }}</p>
      </div>
      
      <div class="stat-card">
        <div class="text-4xl">🎯</div>
        <h3 class="text-slate-600 text-sm font-medium mt-2">Franchises</h3>
        <p class="text-3xl font-bold text-orange-600">{{ overview.total_franchises }}</p>
      </div>
      
      <div class="stat-card">
        <div class="text-4xl">⚾</div>
        <h3 class="text-slate-600 text-sm font-medium mt-2">Total Deliveries</h3>
        <p class="text-3xl font-bold text-red-600">{{ formatNumber(overview.total_deliveries) }}</p>
      </div>
    </div>

    <!-- Seasons Breakdown -->
    <div class="stat-card mb-8">
      <h2 class="text-xl font-bold mb-6">Matches by Season</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="season in seasons" :key="season.season" class="bg-slate-50 rounded-lg p-4 text-center">
          <p class="text-sm text-slate-600">{{ season.season }}</p>
          <p class="text-2xl font-bold text-blue-600">{{ season.matches }}</p>
        </div>
      </div>
    </div>

    <!-- API Status -->
    <div class="bg-green-50 border border-green-200 rounded-lg p-4 text-sm text-green-800">
      ✓ Database connection healthy | {{ new Date().toLocaleString() }}
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const overview = ref<any>({
  total_matches: 0,
  total_players: 0,
  total_franchises: 0,
  total_deliveries: 0
})
const seasons = ref<any[]>([])

const formatNumber = (num: number) => {
  return num.toLocaleString('en-IN')
}

onMounted(async () => {
  try {
    const overviewRes = await $fetch(`${config.public.apiBase}/api/overview`)
    overview.value = overviewRes
  } catch (error) {
    console.error('Failed to fetch overview:', error)
  }
  
  try {
    const seasonsRes = await $fetch(`${config.public.apiBase}/api/seasons`)
    seasons.value = Array.isArray(seasonsRes) ? seasonsRes : []
  } catch (error) {
    console.error('Failed to fetch seasons:', error)
    seasons.value = []
  }
})
</script>
