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
            Deep dive into individual player careers with comprehensive analytics. Search any player to unlock batting and bowling insights.
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

      <!-- Debug Panel -->
      <div v-if="searchQuery.length >= 2" class="mt-2 p-3 bg-gray-100 rounded text-sm">
        <div>Query: "{{ searchQuery }}"</div>
        <div>Results count: {{ searchResults.length }}</div>
        <div>Show results: {{ showResults }}</div>
        <div>API Base: {{ config.public.apiBase }}</div>
        <div v-if="searchResults.length > 0">First result: {{ searchResults[0] }}</div>
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
        <div v-if="showResults && searchResults.length > 0" class="absolute z-50 mt-3 w-full bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden backdrop-blur-sm bg-white/95">
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
              {{ (playerStats.battingStats?.totalRuns > 0 && playerStats.bowlingStats?.totalWickets > 0) ? 'All Rounder' : 
                   (playerStats.battingStats?.totalRuns > 0 ? 'Batsman' : 'Bowler') }}
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
              <p class="text-2xl font-black text-slate-900">{{ playerStats.battingStats?.totalRuns || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Strike Rate</p>
              <p class="text-2xl font-black text-indigo-600">{{ playerStats.battingStats?.strikeRate || '0.00' }}<span class="text-sm font-medium ml-0.5">%</span></p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Average</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.average || '0.00' }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Highest Score</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.highestScore || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Fours (4s)</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.fours || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Sixes (6s)</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.sixes || 0 }}</p>
            </div>
            <div class="col-span-2 p-4 bg-indigo-600 rounded-xl flex justify-between items-center text-white shadow-md shadow-indigo-100">
               <div>
                 <p class="text-[10px] font-bold uppercase tracking-widest opacity-80 mb-0.5">Innings Played</p>
                 <p class="text-xl font-black">{{ playerStats.battingStats?.innings || 0 }}</p>
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
              <p class="text-2xl font-black text-slate-900">{{ playerStats.bowlingStats?.totalWickets || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Economy Rate</p>
              <p class="text-2xl font-black text-rose-600">{{ playerStats.bowlingStats?.economyRate || '0.00' }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Bowling Average</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.bowlingStats?.average || '0.00' }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Runs Conceded</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.bowlingStats?.runsConceded || 0 }}</p>
            </div>
            <div class="col-span-2 p-4 bg-rose-600 rounded-xl flex justify-between items-center text-white shadow-md shadow-rose-100">
               <div>
                 <p class="text-[10px] font-bold uppercase tracking-widest opacity-80 mb-0.5">Bowling Innings</p>
                 <p class="text-xl font-black">{{ playerStats.bowlingStats?.innings || 0 }}</p>
               </div>
               <FireIcon class="w-8 h-8 opacity-20" />
            </div>
          </div>
        </div>
      </div>

      <!-- Season-wise Performance -->
      <div v-if="Object.keys(playerStats.seasonWiseStats || {}).length > 0" class="col-span-1 lg:col-span-2">
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <PresentationChartLineIcon class="w-5 h-5 text-purple-500" />
              <h3 class="font-bold text-slate-800">Season-wise Performance</h3>
            </div>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Career Timeline</span>
          </div>
          <div class="p-6 space-y-4">
            <div v-for="(stats, season) in playerStats.seasonWiseStats" :key="season" class="border border-slate-200 rounded-lg overflow-hidden">
              <div class="bg-slate-50 px-4 py-3 border-b border-slate-200 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="font-bold text-slate-800 text-lg">{{ season }}</span>
                  <span v-if="stats.team" class="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-xs font-bold">{{ stats.team }}</span>
                </div>
                <div class="text-sm text-slate-600">
                  <span v-if="stats.batting?.innings">{{ stats.batting.innings }} bat</span>
                  <span v-if="stats.batting?.innings && stats.bowling?.innings"> • </span>
                  <span v-if="stats.bowling?.innings">{{ stats.bowling.innings }} bowl</span>
                </div>
              </div>
              <div class="p-4">
                <!-- Batting Performance -->
                <div v-if="stats.batting?.runs > 0" class="mb-4">
                  <h4 class="text-sm font-semibold text-indigo-600 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <CricketHelmetIcon class="w-4 h-4" />
                    Batting Performance
                  </h4>
                  <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                    <div class="text-center p-3 bg-indigo-50 rounded-lg">
                      <p class="text-lg font-bold text-indigo-800">{{ stats.batting.runs }}</p>
                      <p class="text-xs text-indigo-600 font-medium">Runs</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.batting.average }}</p>
                      <p class="text-xs text-slate-600 font-medium">Average</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.batting.strikeRate }}</p>
                      <p class="text-xs text-slate-600 font-medium">SR</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.batting.highest }}</p>
                      <p class="text-xs text-slate-600 font-medium">Highest</p>
                    </div>
                    <div class="text-center p-3 bg-green-50 rounded-lg">
                      <p class="text-lg font-bold text-green-800">{{ stats.batting.centuries }}</p>
                      <p class="text-xs text-green-600 font-medium">100s</p>
                    </div>
                    <div class="text-center p-3 bg-yellow-50 rounded-lg">
                      <p class="text-lg font-bold text-yellow-800">{{ stats.batting.fifties }}</p>
                      <p class="text-xs text-yellow-600 font-medium">50s</p>
                    </div>
                  </div>
                </div>
                
                <!-- Bowling Performance -->
                <div v-if="stats.bowling?.wickets > 0">
                  <h4 class="text-sm font-semibold text-rose-600 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <CricketBallIcon class="w-4 h-4" />
                    Bowling Performance
                  </h4>
                  <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <div class="text-center p-3 bg-rose-50 rounded-lg">
                      <p class="text-lg font-bold text-rose-800">{{ stats.bowling.wickets }}</p>
                      <p class="text-xs text-rose-600 font-medium">Wickets</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.average }}</p>
                      <p class="text-xs text-slate-600 font-medium">Average</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.economy }}</p>
                      <p class="text-xs text-slate-600 font-medium">Economy</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.runs }}</p>
                      <p class="text-xs text-slate-600 font-medium">Runs</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.bestBowling }}</p>
                      <p class="text-xs text-slate-600 font-medium">Best</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Graph View Expansion -->
      <!-- <div class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden">
        <div class="p-6 pb-4 border-b border-slate-100/60 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div class="flex flex-col">
            <h2 class="text-xl font-black text-slate-900">Graph Visualization</h2>
            <p class="text-slate-500 text-sm font-medium">Interactive relationship explorer for {{ searchQuery }}</p>
          </div>
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
               This <strong class="text-slate-900">interactive graph</strong> shows player connections and relationships. <strong class="text-indigo-600">Click</strong> nodes to view player stats. <strong class="text-indigo-600">Drag</strong> any node to move it around and explore the network layout.
             </p>
          </div>
        </div>
      </div> -->
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

type GraphData = {
  edges: Array<any>,
  nodes: Array<any>
}

const fetchPlayerGraph = async (playerName: string) => {
  try {
    loadingRivals.value = true
    const graphData = await $fetch<GraphData>(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/graph`)
    
    // Convert graph data to rivals format for compatibility
    if (graphData.edges && graphData.nodes) {
      playerRivals.value = graphData.edges.map((edge: any) => {
        const targetNode = graphData.nodes.find((n: any) => n.id === edge.target)
        return {
          name: targetNode?.name || edge.target,
          weight: edge.weight,
          score: edge.weight * 10,
          type: edge.relationship
        }
      })
    } else {
      // Fallback to old rivals endpoint
      playerRivals.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/rivals`)
    }
  } catch (error) {
    console.error('Failed to fetch graph data:', error)
    // Fallback to old endpoint
    try {
      playerRivals.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/rivals`)
    } catch (fallbackError) {
      console.error('Fallback fetch also failed:', fallbackError)
      playerRivals.value = []
    }
  } finally {
    loadingRivals.value = false
  }
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
      console.log('Searching for:', searchQuery.value)
      const url = `${config.public.apiBase}/api/players/search?query=${encodeURIComponent(searchQuery.value)}`
      console.log('API URL:', url)
      const data: any = await $fetch(url)
      console.log('API response:', data)
      searchResults.value = data || []
      showResults.value = searchResults.value.length > 0
      console.log('Search results set:', searchResults.value, 'showResults:', showResults.value)
    } catch (error) {
      console.error('Search failed:', error)
      searchResults.value = []
      showResults.value = false
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
    // Use the new comprehensive stats endpoint
    const playerSlug = playerName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
    playerStats.value = await $fetch(`${config.public.apiBase}/api/players/${playerSlug}/stats`)
    await fetchPlayerGraph(playerName)
  } catch (error) {
    console.error('Fetch failed:', error)
    playerStats.value = null
  }
}

onMounted(() => {
  if (route.query.name) selectPlayer(route.query.name as string)
})
</script>
