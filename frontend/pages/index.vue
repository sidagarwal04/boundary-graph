<template>
  <div>
    <!-- Project Intro -->
    <div class="mb-8 p-6 bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden relative animate-in fade-in slide-in-from-top-4 duration-700">
      <div class="absolute top-0 right-0 w-32 h-32 bg-brand-primary/5 rounded-full -mr-16 -mt-16"></div>
      <div class="relative flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div class="space-y-4">
          <div class="space-y-1">
            <h2 class="text-2xl font-black text-slate-900 tracking-tight">The Indian Premier League <span class="text-brand-primary">Graph</span></h2>
            <p class="text-slate-500 max-w-2xl leading-relaxed text-sm md:text-base">
              Welcome to the ultimate digital twin of the <strong class="text-slate-900">IPL</strong>. This platform processes every ball, wicket, and boundary since 2008 using high-performance graph technology. Dive deep into player trajectories and franchise rivalries powered by 17+ seasons of T20 data.
            </p>
            <div class="mt-3 p-3 bg-amber-50 border border-amber-100 rounded-xl">
              <p class="text-xs text-amber-800 leading-relaxed">
              <strong class="text-amber-900">Why not other leagues?</strong> While many leagues offer rich data, the IPL stands out for its scale, diversity, and continuous evolution—featuring global stars, frequent team changes, and high-stakes matches in a compressed window. This creates a uniquely complex, ever-changing network that’s ideal for graph analytics, letting us uncover dynamic relationships and trends that static datasets or less volatile leagues can’t reveal.
              </p>
            </div>
          </div>
          
          <!-- Tech Stack Pill -->
          <div class="flex flex-wrap items-center gap-4 pt-2">
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Engineered With</span>
            <div class="flex gap-3">
              <div class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 rounded-lg border border-slate-100" title="Graph Database">
                <CircleStackIcon class="w-3.5 h-3.5 text-blue-600" />
                <span class="text-[10px] font-bold text-slate-700">Neo4j</span>
              </div>
              <div class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 rounded-lg border border-slate-100" title="Frontend Framework">
                <SparklesIcon class="w-3.5 h-3.5 text-emerald-600" />
                <span class="text-[10px] font-bold text-slate-700">Nuxt 3</span>
              </div>
              <div class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 rounded-lg border border-slate-100" title="API Backend">
                <BoltIcon class="w-3.5 h-3.5 text-orange-600" />
                <span class="text-[10px] font-bold text-slate-700">FastAPI</span>
              </div>
              <div class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 rounded-lg border border-slate-100" title="AI Coding Assistant">
                <CpuChipIcon class="w-3.5 h-3.5 text-indigo-600" />
                <span class="text-[10px] font-bold text-slate-700">Antigravity</span>
              </div>
              <div class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 rounded-lg border border-slate-100" title="LLM Technology">
                <SparklesIcon class="w-3.5 h-3.5 text-purple-600" />
                <span class="text-[10px] font-bold text-slate-700">Gemini</span>
              </div>
            </div>
          </div>
        </div>
        <div class="flex items-center gap-3 shrink-0">
          <div class="px-4 py-2 bg-slate-900 text-white rounded-xl text-[10px] font-bold uppercase tracking-widest shadow-lg shadow-slate-200">
            IPL 2008 - 2025
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-8">
      <NuxtLink to="/h2h" class="stat-card flex flex-col justify-between hover:scale-[1.02] transition-transform group min-h-[140px]">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-500 mb-2 group-hover:text-blue-600 transition-colors">Total Matches</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-slate-900 tracking-tight leading-none whitespace-nowrap">{{ overview.total_matches }}</p>
            </div>
          </div>
          <div class="p-2 bg-blue-50 rounded-lg shrink-0">
             <CricketStadiumIcon class="w-7 h-7 sm:w-8 sm:h-8 text-blue-600" />
          </div>
        </div>
        <div class="h-1 w-12 bg-blue-500 mt-4 rounded-full"></div>
      </NuxtLink>
      
      <NuxtLink to="/player-search" class="stat-card flex flex-col justify-between hover:scale-[1.02] transition-transform group min-h-[140px]">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-500 mb-2 group-hover:text-green-600 transition-colors">Total Players</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-slate-900 tracking-tight leading-none whitespace-nowrap">{{ overview.total_players }}</p>
            </div>
          </div>
          <div class="p-2 bg-green-50 rounded-lg shrink-0">
             <CricketHelmetIcon class="w-7 h-7 sm:w-8 sm:h-8 text-green-600" />
          </div>
        </div>
        <div class="h-1 w-12 bg-green-500 mt-4 rounded-full"></div>
      </NuxtLink>
      
      <NuxtLink to="/teams" class="stat-card flex flex-col justify-between hover:scale-[1.02] transition-transform group min-h-[140px]">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-500 mb-2 group-hover:text-orange-600 transition-colors">Total Teams</h3>
            <div class="h-12 flex flex-col justify-center">
              <p class="text-2xl xl:text-3xl font-bold text-slate-900 tracking-tight leading-none whitespace-nowrap">{{ overview.active_teams }} <span class="text-[10px] text-slate-400 font-medium leading-tight mt-0.5">({{ overview.defunct_teams }} defunct)</span></p>
            </div>
          </div>
          <div class="p-2 bg-orange-50 rounded-lg shrink-0">
             <CricketJerseyIcon class="w-7 h-7 sm:w-8 sm:h-8 text-orange-600" />
          </div>
        </div>
        <div class="h-1 w-12 bg-orange-500 mt-4 rounded-full"></div>
      </NuxtLink>

      <NuxtLink to="/batsmen" class="stat-card flex flex-col justify-between hover:scale-[1.02] transition-transform group min-h-[140px]">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-500 mb-2 group-hover:text-yellow-600 transition-colors">Total Runs Scored</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-slate-900 tracking-tight leading-none whitespace-nowrap text-ellipsis">{{ formatNumber(overview.total_runs) }}</p>
            </div>
          </div>
          <div class="p-2 bg-yellow-50 rounded-lg shrink-0">
             <CricketBatIcon class="w-7 h-7 sm:w-8 sm:h-8 text-yellow-600" />
          </div>
        </div>
        <div class="h-1 w-12 bg-yellow-500 mt-4 rounded-full"></div>
      </NuxtLink>
      
      <NuxtLink to="/bowlers" class="stat-card flex flex-col justify-between hover:scale-[1.02] transition-transform group min-h-[140px]">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-500 mb-2 group-hover:text-red-600 transition-colors">Total Deliveries</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-slate-900 tracking-tight leading-none whitespace-nowrap text-ellipsis">{{ formatNumber(overview.total_deliveries) }}</p>
            </div>
          </div>
          <div class="p-2 bg-red-50 rounded-lg shrink-0">
             <CricketBallIcon class="w-7 h-7 sm:w-8 sm:h-8 text-red-600" />
          </div>
        </div>
        <div class="h-1 w-12 bg-red-500 mt-4 rounded-full"></div>
      </NuxtLink>
      <NuxtLink to="/venues" class="stat-card flex flex-col justify-between hover:scale-[1.02] transition-transform group min-h-[140px]">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-500 mb-2 group-hover:text-purple-600 transition-colors">Total Venues</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-slate-900 tracking-tight leading-none whitespace-nowrap">36+</p>
            </div>
          </div>
          <div class="p-2 bg-purple-50 rounded-lg shrink-0">
             <MapPinIcon class="w-7 h-7 sm:w-8 sm:h-8 text-purple-600" />
          </div>
        </div>
        <div class="h-1 w-12 bg-purple-500 mt-4 rounded-full"></div>
      </NuxtLink>
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

    <!-- Active Teams -->
    <div class="stat-card mb-8">
      <div class="flex items-center justify-between mb-6 border-b border-slate-100 pb-4">
        <h2 class="text-lg font-bold text-slate-800">Active Teams</h2>
        <span class="text-xs font-bold text-slate-400 uppercase tracking-widest">{{ activeTeams.length }} Teams</span>
      </div>
      <div class="flex flex-wrap gap-4 justify-center">
        <NuxtLink 
          v-for="team in activeTeams" 
          :key="team.name" 
          :to="'/teams'"
          class="group bg-white border border-slate-200 rounded-lg p-4 hover:border-brand-primary/30 hover:shadow-md hover:bg-slate-50 transition-all duration-200 cursor-pointer w-full sm:w-[calc(50%-0.5rem)] md:w-[calc(33.333%-0.67rem)] lg:w-[calc(25%-0.75rem)]"
        >
          <div class="flex flex-col items-center text-center space-y-3">
            <TeamLogo :teamName="team.name" size="2xl" :showName="false" />
            <div>
              <h3 class="font-bold text-slate-800 group-hover:text-brand-primary transition-colors text-sm">{{ team.name }}</h3>
            </div>
          </div>
        </NuxtLink>
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
          <NuxtLink 
            v-if="selectedSeasonDetails.final_match_id"
            :to="'/match/' + selectedSeasonDetails.final_match_id"
            class="flex flex-col items-center justify-center mb-8 bg-gradient-to-br from-yellow-50 to-orange-50 p-6 rounded-lg border border-yellow-100 hover:scale-[1.01] transition-transform cursor-pointer group"
          >
             <span class="text-xs font-bold text-yellow-600 uppercase tracking-widest mb-2">Season Winner</span>
             <div class="flex items-center gap-3 group-hover:text-yellow-700 transition-colors">
               <TrophyIcon class="w-8 h-8 text-yellow-500" />
               <TeamLogo :teamName="selectedSeasonDetails.winner" size="lg" :showName="false" />
               <h2 class="text-3xl font-extrabold text-slate-900">{{ selectedSeasonDetails.winner }}</h2>
             </div>
             <p class="text-sm text-slate-500 mt-2 font-medium">Won by {{ selectedSeasonDetails.margin }} • <span class="text-yellow-600">View Final Storyline</span></p>
          </NuxtLink>

          <div v-else class="flex flex-col items-center justify-center mb-8 bg-gradient-to-br from-yellow-50 to-orange-50 p-6 rounded-lg border border-yellow-100">
             <span class="text-xs font-bold text-yellow-600 uppercase tracking-widest mb-2">Winner</span>
             <div class="flex items-center gap-3">
               <TrophyIcon class="w-8 h-8 text-yellow-500" />
               <TeamLogo :teamName="selectedSeasonDetails.winner" size="lg" :showName="false" />
               <h2 class="text-3xl font-extrabold text-slate-900">{{ selectedSeasonDetails.winner }}</h2>
             </div>
             <p class="text-sm text-slate-500 mt-2 font-medium">Won by {{ selectedSeasonDetails.margin }}</p>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
             <!-- Runner Up -->
             <div class="p-4 bg-slate-50 rounded-lg border border-slate-100 min-h-[90px] flex flex-col justify-center">
                <p class="text-xs text-slate-400 font-medium mb-1">Runner Up</p>
                <div class="flex items-center gap-2">
                  <TeamLogo :teamName="selectedSeasonDetails.runner_up" size="sm" :showName="false" />
                  <p class="text-lg font-bold text-slate-800 leading-tight">{{ selectedSeasonDetails.runner_up }}</p>
                </div>
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
import { ref, onMounted, onUnmounted, computed } from 'vue'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'
import CricketJerseyIcon from '~/components/icons/CricketJerseyIcon.vue'
import CricketStadiumIcon from '~/components/icons/CricketStadiumIcon.vue'
import CricketBatIcon from '~/components/icons/CricketBatIcon.vue'
import TeamLogo from '~/components/TeamLogo.vue'
import { 
  TrophyIcon, 
  ShieldCheckIcon, 
  UserIcon, 
  CircleStackIcon, 
  SparklesIcon, 
  BoltIcon,
  CpuChipIcon,
  MapPinIcon
} from '@heroicons/vue/24/outline'

const config = useRuntimeConfig()
const overview = ref<any>({
  total_matches: 0,
  total_players: 0,
  total_runs: 0,
  active_teams: 0,
  defunct_teams: 0,
  total_deliveries: 0
})
const seasons = ref<any[]>([])
const allTeams = ref<any[]>([])

// Modal State
const isModalOpen = ref(false)
const loadingDetails = ref(false)
const selectedSeasonDetails = ref<any>(null)

// Computed properties
const activeTeams = computed(() => allTeams.value.filter(t => t.is_active))

const formatNumber = (num: number) => {
  if (!num) return 0
  
  // For very large numbers, use abbreviations
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1).replace(/\.0$/, '') + 'B'
  }
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  }
  
  return num.toLocaleString('en-IN')
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

  try {
    const teamsRes = await $fetch(`${config.public.apiBase}/api/teams`)
    allTeams.value = Array.isArray(teamsRes) ? teamsRes : []
  } catch (error) {
    console.error('Failed to fetch teams:', error)
    allTeams.value = []
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>
