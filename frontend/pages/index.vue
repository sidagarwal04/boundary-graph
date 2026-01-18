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
        <div 
          v-for="season in seasons" 
          :key="season.season" 
          @click="openSeasonModal(season)"
          class="bg-slate-50 rounded p-3 text-center border border-slate-100/50 hover:bg-white hover:shadow-sm hover:border-brand-primary/30 transition-all duration-200 cursor-pointer"
        >
          <p class="text-xs text-slate-400 font-medium font-mono mb-1">{{ season.season }}</p>
          <p class="text-lg font-bold text-slate-900">{{ season.matches }} Matches</p>
        </div>
      </div>
    </div>


    <!-- Season Detail Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/50 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-xl shadow-2xl w-full max-w-2xl overflow-hidden animate-fade-in-up">
        
        <!-- Header -->
        <div class="bg-slate-50 px-6 py-4 border-b border-slate-200 flex justify-between items-center">
          <h3 class="text-xl font-bold text-slate-900">IPL {{ selectedSeasonDetails?.season }} Season Details</h3>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <!-- Content -->
        <div v-if="loadingDetails" class="p-8 text-center text-slate-500">
           Loading stats...
        </div>
        
        <div v-else-if="selectedSeasonDetails" class="p-6">
          
          <!-- Winner Section -->
          <div class="flex flex-col items-center justify-center mb-8 bg-gradient-to-br from-yellow-50 to-orange-50 p-6 rounded-lg border border-yellow-100">
             <span class="text-xs font-bold text-yellow-600 uppercase tracking-widest mb-2">Winner</span>
             <h2 class="text-3xl font-extrabold text-slate-900 flex items-center gap-3">
               <TrophyIcon class="w-8 h-8 text-yellow-500" />
               {{ selectedSeasonDetails.winner }}
             </h2>
             <p class="text-sm text-slate-500 mt-2 font-medium">Won by {{ selectedSeasonDetails.margin }}</p>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <!-- Runner Up -->
             <div class="p-4 bg-slate-50 rounded-lg border border-slate-100 min-h-[90px] flex flex-col justify-center">
                <p class="text-xs text-slate-400 font-medium mb-1">Runner Up</p>
                <p class="text-lg font-bold text-slate-800 leading-tight">{{ selectedSeasonDetails.runner_up }}</p>
             </div>
             
             <!-- Venue -->
             <div class="p-4 bg-slate-50 rounded-lg border border-slate-100 min-h-[90px] flex flex-col justify-center">
                <p class="text-xs text-slate-400 font-medium mb-1">Final Venue</p>
                <p class="text-lg font-bold text-slate-800 leading-tight">{{ selectedSeasonDetails.venue }}</p>
             </div>
             
             <!-- Total Teams -->
             <div class="p-4 bg-slate-50 rounded-lg border border-slate-100 flex items-center justify-between min-h-[90px]">
                <div>
                  <p class="text-xs text-slate-400 font-medium mb-1">Participating Teams</p>
                  <p class="text-lg font-bold text-slate-800">{{ selectedSeasonDetails.total_teams }}</p>
                </div>
                <ShieldCheckIcon class="w-5 h-5 text-slate-300" />
             </div>

             <!-- Total Matches -->
             <div class="p-4 bg-slate-50 rounded-lg border border-slate-100 flex items-center justify-between min-h-[90px]">
                <div>
                  <p class="text-xs text-slate-400 font-medium mb-1">Total Matches played</p>
                  <p class="text-lg font-bold text-slate-800">{{ selectedSeasonDetails.total_matches }}</p>
                </div>
                 <CricketBallIcon class="w-5 h-5 text-slate-300" />
             </div>
             
             <!-- Player of the Tournament -->
             <div v-if="selectedSeasonDetails.player_of_tournament" class="p-4 bg-gradient-to-br from-blue-50 to-indigo-50 rounded-lg border border-blue-100 flex items-center justify-between">
                <div>
                  <p class="text-xs text-blue-600 font-bold uppercase tracking-widest mb-1">Player of the Tournament</p>
                  <p class="text-xl font-extrabold text-slate-900">{{ selectedSeasonDetails.player_of_tournament }}</p>
                </div>
                <CricketHelmetIcon class="w-6 h-6 text-blue-400" />
             </div>
             
             <!-- Player of the Match (Final) -->
             <div v-if="selectedSeasonDetails.player_of_match" class="p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg border border-green-100 flex items-center justify-between">
                <div>
                  <p class="text-xs text-green-600 font-bold uppercase tracking-widest mb-1">Player of the Match (Final)</p>
                  <p class="text-xl font-extrabold text-slate-900">{{ selectedSeasonDetails.player_of_match }}</p>
                </div>
                <TrophyIcon class="w-6 h-6 text-green-400" />
             </div>
          </div>
          
        </div>
      </div>
    </div>

  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'
import CricketJerseyIcon from '~/components/icons/CricketJerseyIcon.vue'
import CricketStadiumIcon from '~/components/icons/CricketStadiumIcon.vue'
import { TrophyIcon, ShieldCheckIcon, UserIcon } from '@heroicons/vue/24/outline'

const config = useRuntimeConfig()
const overview = ref<any>({
  total_matches: 0,
  total_players: 0,
  active_teams: 0,
  defunct_teams: 0,
  total_deliveries: 0
})
const seasons = ref<any[]>([])

// Modal State
const isModalOpen = ref(false)
const loadingDetails = ref(false)
const selectedSeasonDetails = ref<any>(null)

const formatNumber = (num: number) => {
  return num ? num.toLocaleString('en-IN') : 0
}

const openSeasonModal = async (season: any) => {
  isModalOpen.value = true
  loadingDetails.value = true
  selectedSeasonDetails.value = { season: season.season } // Initial placeholder
  
  try {
     const details = await $fetch(`${config.public.apiBase}/api/seasons/${season.season}`)
     selectedSeasonDetails.value = details
  } catch (e) {
     console.error("Error fetching season details", e)
  } finally {
     loadingDetails.value = false
  }
}

const closeModal = () => {
  isModalOpen.value = false
  selectedSeasonDetails.value = null
}

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape' && isModalOpen.value) {
    closeModal()
  }
}

onMounted(async () => {
  window.addEventListener('keydown', onKeydown)
  
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

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>
