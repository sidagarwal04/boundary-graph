<template>
  <div class="space-y-8 animate-in fade-in duration-500">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-indigo-600/10 text-indigo-600 rounded-full text-xs font-bold uppercase tracking-widest">
          <MagnifyingGlassIcon class="w-3 h-3" />
          Player Intelligence
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">The <span class="text-indigo-600">Search Engine</span></h1>
        <p class="text-slate-500 max-w-xl">
          Deep dive into individual player careers with comprehensive analytics. Search any player to unlock batting, bowling, and rivalry insights powered by graph technology.
        </p>
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
          placeholder="Ex: V Kohli, MS Dhoni, Rashid Khan..."
          class="flex-1 bg-transparent py-3 pr-4 outline-none text-slate-900 font-medium placeholder:text-slate-400"
          @input="searchPlayers"
          @keydown="handleKeydown"
        />
        <div v-if="searchQuery" @click="clearSearch" class="pr-3 text-slate-400 hover:text-slate-600 cursor-pointer">
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
              v-for="(player, index) in searchResults" 
              :key="player"
              @click="selectPlayer(player)"
              :class="[
                'w-full text-left px-5 py-3.5 flex items-center gap-3 transition-colors group',
                highlightedIndex === index ? 'bg-slate-100' : 'hover:bg-slate-50'
              ]"
            >
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center transition-colors',
                highlightedIndex === index ? 'bg-brand-primary/10 text-brand-primary' : 'bg-slate-100 text-slate-500 group-hover:bg-brand-primary/10 group-hover:text-brand-primary'
              ]">
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
            <span class="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-md text-xs font-bold uppercase tracking-wider border border-slate-200 italic">
              {{ playerStats.batting_matches > 0 ? (playerStats.bowling_matches > 0 ? 'All Rounder' : 'Batsman') : 'Bowler' }}
            </span>
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

      <!-- Graph View Expansion -->
      <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
          <div class="flex items-center gap-2">
            <ShareIcon class="w-5 h-5 text-indigo-500" />
            <h3 class="font-bold text-slate-800">Graph Relationship Explorer</h3>
          </div>
          <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Interactive Rivalry Network</span>
        </div>
        <div class="p-6">
          <GraphVisualization 
            :playerName="searchQuery" 
            :rivals="playerRivals" 
            :loading="loadingRivals"
            @select-rival="selectPlayer"
          />
          <div class="mt-4 p-4 bg-slate-50 rounded-xl flex items-start gap-3">
             <div class="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                <InformationCircleIcon class="w-4 h-4" />
             </div>
             <p class="text-[11px] text-slate-500 leading-relaxed font-medium mt-0.5">
               This <strong class="text-slate-900">interactive Neo4j graph</strong> shows player rivalries and relationships. <strong class="text-indigo-600">Single-click</strong> nodes to view player stats. <strong class="text-indigo-600">Double-click</strong> any node to expand and explore their network of rivals and connections.
             </p>
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
      <p class="text-slate-500 max-w-sm mx-auto mt-2 font-medium">Use the search box above to lookup any player's statistics.</p>
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
  FireIcon,
  ShareIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'
import GraphVisualization from '~/components/GraphVisualization.vue'

const config = useRuntimeConfig()
const route = useRoute()
const searchQuery = ref('')
const searchResults = ref<any[]>([])
const showResults = ref(false)
const playerStats = ref<any>(null)
const playerRivals = ref<any[]>([])
const loadingRivals = ref(false)
const highlightedIndex = ref(-1)
let searchTimeout: any = null

// Handle graph expansion events
onMounted(() => {
  document.addEventListener('expand-player', (event: any) => {
    const playerName = event.detail
    searchQuery.value = playerName
    selectPlayer(playerName)
  })
  
  document.addEventListener('expand-center', (event: any) => {
    console.log('Center expansion requested for:', event.detail)
    // Could fetch more relationships, show team connections, etc.
    fetchAdditionalRelationships(event.detail)
  })
})

const fetchAdditionalRelationships = async (playerName: string) => {
  // This could fetch team relationships, coach connections, etc.
  console.log(`Fetching additional relationships for ${playerName}`)
  // For now, just show a notification that it's expanding
  // You could add more complex graph expansion logic here
}

const clearSearch = () => {
  searchQuery.value = ''
  playerStats.value = null
  showResults.value = false
}

const searchPlayers = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    showResults.value = false
    return
  }
  searchTimeout = setTimeout(async () => {
    try {
      const data: any = await $fetch(`${config.public.apiBase}/api/players/search?query=${encodeURIComponent(searchQuery.value)}`)
      searchResults.value = data
      showResults.value = searchResults.value.length > 0
    } catch (error) {
      console.error('Search failed:', error)
    }
  }, 300)
}

const handleKeydown = (e: KeyboardEvent) => {
  if (!showResults.value || searchResults.value.length === 0) return
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    highlightedIndex.value = (highlightedIndex.value + 1) % searchResults.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    highlightedIndex.value = (highlightedIndex.value - 1 + searchResults.value.length) % searchResults.value.length
  } else if (e.key === 'Enter') {
    e.preventDefault()
    if (highlightedIndex.value >= 0) selectPlayer(searchResults.value[highlightedIndex.value])
  } else if (e.key === 'Escape') {
    showResults.value = false
  }
}

const selectPlayer = async (playerName: string) => {
  searchQuery.value = playerName
  showResults.value = false
  try {
    playerStats.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}`)
    loadingRivals.value = true
    playerRivals.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/rivals`)
  } catch (error) {
    console.error('Fetch failed:', error)
  } finally {
    loadingRivals.value = false
  }
}

onMounted(() => {
  if (route.query.name) selectPlayer(route.query.name as string)
})
</script>
