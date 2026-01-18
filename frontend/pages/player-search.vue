<template>
  <div class="space-y-8 animate-in fade-in duration-500">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
      <div class="flex items-center gap-4">
        <div class="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center text-indigo-600 shadow-sm border border-indigo-100">
          <MagnifyingGlassIcon class="w-6 h-6" />
        </div>
        <div>
          <h1 class="text-2xl font-bold text-slate-900 tracking-tight">Player Intelligence</h1>
          <p class="text-slate-500 text-sm font-medium">Search the database for deep performance metrics</p>
        </div>
      </div>
    </div>

    <!-- Search Section -->
    <div class="relative max-w-2xl">
      <div class="bg-white p-2 rounded-2xl border border-slate-200 shadow-sm focus-within:ring-4 focus-within:ring-brand-primary/10 focus-within:border-brand-primary transition-all flex items-center gap-3">
        <div class="pl-3 text-slate-400">
          <MagnifyingGlassIcon class="w-5 h-5" />
        </div>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Ex: Virat Kohli, Rashid Khan..."
          class="flex-1 bg-transparent py-3 pr-4 outline-none text-slate-900 font-medium placeholder:text-slate-400"
          @input="searchPlayers"
        />
        <div v-if="searchQuery" @click="searchQuery = ''; playerStats = null; showResults = false" class="pr-3 text-slate-400 hover:text-slate-600 cursor-pointer">
          <XMarkIcon class="w-5 h-5" />
        </div>
      </div>
      
      <!-- Autocomplete Dropdown -->
      <transition 
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div v-if="searchResults.length > 0 && showResults" class="absolute z-50 mt-3 w-full bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden backdrop-blur-sm bg-white/95">
          <div class="py-2">
            <button 
              v-for="player in searchResults" 
              :key="player"
              @click="selectPlayer(player)"
              class="w-full text-left px-5 py-3.5 hover:bg-slate-50 flex items-center gap-3 transition-colors group"
            >
              <div class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-slate-500 group-hover:bg-brand-primary/10 group-hover:text-brand-primary">
                <UserIcon class="w-4 h-4" />
              </div>
              <span class="font-semibold text-slate-700 group-hover:text-slate-900">{{ player }}</span>
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Stats Display -->
    <div v-if="playerStats" class="space-y-6">
      <!-- Player Header Card -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-6">
        <div class="w-16 h-16 rounded-full bg-slate-900 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-slate-200">
          {{ searchQuery.charAt(0) }}
        </div>
        <div>
          <h2 class="text-3xl font-bold text-slate-900 tracking-tight">{{ searchQuery }}</h2>
          <div class="flex gap-4 mt-2">
            <span class="px-2.5 py-1 bg-green-50 text-green-700 rounded-md text-xs font-bold uppercase tracking-wider border border-green-100">Pro Athlete</span>
            <span class="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-md text-xs font-bold uppercase tracking-wider border border-slate-200 italic">{{ playerStats.batting_matches > 0 ? (playerStats.bowling_matches > 0 ? 'All Rounder' : 'Batsman') : 'Bowler' }}</span>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Batting Analytics -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <CricketHelmetIcon class="w-5 h-5 text-indigo-500" />
              <h3 class="font-bold text-slate-800">Batting Analytics</h3>
            </div>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Career Profile</span>
          </div>
          <div class="p-6 grid grid-cols-2 gap-4 flex-grow">
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Total Runs</p>
              <p class="text-2xl font-black text-slate-900">{{ playerStats.total_runs || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Strike Rate</p>
              <p class="text-2xl font-black text-indigo-600">{{ playerStats.strike_rate || '0.00' }}<span class="text-sm font-medium ml-0.5">%</span></p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Fours (4s)</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.total_fours || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Sixes (6s)</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.total_sixes || 0 }}</p>
            </div>
            <div class="col-span-2 p-4 bg-indigo-600 rounded-xl flex justify-between items-center text-white shadow-md shadow-indigo-100">
               <div>
                 <p class="text-[10px] font-bold uppercase tracking-widest opacity-80 mb-0.5">Participating Matches</p>
                 <p class="text-xl font-black">{{ playerStats.batting_matches || 0 }}</p>
               </div>
               <PresentationChartLineIcon class="w-8 h-8 opacity-20" />
            </div>
          </div>
        </div>

        <!-- Bowling Analytics -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <CricketBallIcon class="w-5 h-5 text-rose-500" />
              <h3 class="font-bold text-slate-800">Bowling Analytics</h3>
            </div>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Career Profile</span>
          </div>
          <div class="p-6 grid grid-cols-2 gap-4 flex-grow">
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Total Wickets</p>
              <p class="text-2xl font-black text-slate-900">{{ playerStats.total_wickets || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Economy</p>
              <p class="text-2xl font-black text-rose-600">{{ playerStats.economy || '0.00' }}</p>
            </div>
            <div class="col-span-2 p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Runs Conceded</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.runs_conceded || 0 }}</p>
            </div>
            <div class="col-span-2 p-4 bg-rose-600 rounded-xl flex justify-between items-center text-white shadow-md shadow-rose-100">
               <div>
                 <p class="text-[10px] font-bold uppercase tracking-widest opacity-80 mb-0.5">Participating Matches</p>
                 <p class="text-xl font-black">{{ playerStats.bowling_matches || 0 }}</p>
               </div>
               <FireIcon class="w-8 h-8 opacity-20" />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Placeholder State -->
    <div v-else-if="!searchQuery" class="bg-white rounded-2xl border-2 border-dashed border-slate-200 py-20 text-center">
      <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-300">
        <UserPlusIcon class="w-10 h-10" />
      </div>
      <h3 class="text-xl font-bold text-slate-800">No Intelligence Selected</h3>
      <p class="text-slate-500 max-w-sm mx-auto mt-2 font-medium">Use the search box above to lookup any player's career statistics and performance metrics.</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { 
  MagnifyingGlassIcon, 
  XMarkIcon, 
  UserIcon, 
  UserPlusIcon,
  PresentationChartLineIcon,
  FireIcon
} from '@heroicons/vue/24/outline'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'

const config = useRuntimeConfig()
const route = useRoute()
const searchQuery = ref('')
const searchResults = ref<any[]>([])
const showResults = ref(false)
const playerStats = ref<any>(null)

const searchPlayers = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    showResults.value = false
    return
  }
  
  try {
    searchResults.value = await $fetch(`${config.public.apiBase}/api/players/search?query=${encodeURIComponent(searchQuery.value)}`)
    showResults.value = true
  } catch (error) {
    console.error('Search failed:', error)
  }
}

const selectPlayer = async (playerName: string) => {
  searchQuery.value = playerName
  showResults.value = false
  
  try {
    playerStats.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}`)
  } catch (error) {
    console.error('Failed to fetch player stats:', error)
    playerStats.value = null
  }
}

onMounted(() => {
  // Check if player name is in query params
  if (route.query.name) {
    selectPlayer(route.query.name as string)
  }
})
</script>
