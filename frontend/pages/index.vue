<template>
  <div>
    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
      <div class="stat-card flex justify-between items-start">
        <div class="flex flex-col">
          <h3 class="text-label text-slate-500 mb-1">Total Matches</h3>
          <p class="text-3xl font-bold text-slate-900 tracking-tight">{{ overview.total_matches }}</p>
          <div class="h-1 w-12 bg-blue-500 mt-4 rounded-full"></div>
        </div>
        <div class="p-3 bg-blue-50 rounded-lg">
           <CricketStadiumIcon class="w-8 h-8 text-blue-600" />
        </div>
      </div>
      
      <div class="stat-card flex justify-between items-start">
        <div class="flex flex-col">
          <h3 class="text-label text-slate-500 mb-1">Total Players</h3>
          <p class="text-3xl font-bold text-slate-900 tracking-tight">{{ overview.total_players }}</p>
          <div class="h-1 w-12 bg-green-500 mt-4 rounded-full"></div>
        </div>
        <div class="p-3 bg-green-50 rounded-lg">
           <CricketHelmetIcon class="w-8 h-8 text-green-600" />
        </div>
      </div>
      
      <div class="stat-card flex justify-between items-start">
        <div class="flex flex-col">
          <h3 class="text-label text-slate-500 mb-1">Teams</h3>
          <div class="flex items-baseline gap-2">
            <p class="text-3xl font-bold text-slate-900 tracking-tight">{{ overview.active_teams }}</p>
            <span class="text-xs text-slate-400 font-medium">({{ overview.defunct_teams }} defunct)</span>
          </div>
          <div class="h-1 w-12 bg-orange-500 mt-4 rounded-full"></div>
        </div>
        <div class="p-3 bg-orange-50 rounded-lg">
           <CricketJerseyIcon class="w-8 h-8 text-orange-600" />
        </div>
      </div>
      
      <div class="stat-card flex justify-between items-start">
        <div class="flex flex-col">
          <h3 class="text-label text-slate-500 mb-1">Total Deliveries</h3>
          <p class="text-3xl font-bold text-slate-900 tracking-tight">{{ formatNumber(overview.total_deliveries) }}</p>
          <div class="h-1 w-12 bg-red-500 mt-4 rounded-full"></div>
        </div>
        <div class="p-3 bg-red-50 rounded-lg">
           <CricketBallIcon class="w-8 h-8 text-red-600" />
        </div>
      </div>
    </div>

    <!-- Seasons Breakdown -->
    <div class="stat-card mb-8">
      <div class="flex items-center gap-2 mb-6 border-b border-slate-100 pb-4">
        <h2 class="text-lg font-bold text-slate-800">Season Analysis</h2>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div v-for="season in seasons" :key="season.season" class="bg-slate-50 rounded p-3 text-center border border-slate-100/50 hover:bg-white hover:shadow-sm transition-all duration-200">
          <p class="text-xs text-slate-400 font-medium font-mono mb-1">{{ season.season }}</p>
          <p class="text-lg font-bold text-slate-900">{{ season.matches }}</p>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'
import CricketJerseyIcon from '~/components/icons/CricketJerseyIcon.vue'
import CricketStadiumIcon from '~/components/icons/CricketStadiumIcon.vue'

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
