<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-ipl-blue/15 text-ipl-blue rounded-full text-xs font-bold uppercase tracking-widest border border-ipl-blue/20">
          <TrophyIcon class="w-3 h-3" />
          Tournament Standings
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">IPL <span class="bg-gradient-to-r from-ipl-blue to-purple-600 bg-clip-text text-transparent">Points Table</span></h1>
        <p class="text-slate-500 max-w-xl">
          Live standings and team performance across IPL seasons
        </p>
      </div>
    </div>

    <!-- Season Filter -->
    <div class="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 p-5 bg-gradient-to-r from-ipl-blue/8 to-purple-100/50 rounded-2xl border border-ipl-blue/15 shadow-md">
      <div class="flex items-center gap-4">
        <label for="season-select" class="text-sm font-bold text-ipl-blue uppercase tracking-wide">
          🏏 Select Season:
        </label>
        <select 
          id="season-select"
          v-model="selectedSeason" 
          @change="fetchPointsTable"
          class="px-4 py-2 border-2 border-ipl-blue/30 rounded-xl focus:ring-2 focus:ring-purple-500 focus:border-purple-500 bg-white font-semibold text-ipl-blue transition-all duration-300 hover:border-purple-500/50"
        >
          <option v-for="season in availableSeasons" :key="season" :value="season">
            IPL {{ season }}
          </option>
        </select>
      </div>
      
      <!-- Live indicator for current season -->
      <div v-if="selectedSeason === '2026' && pointsTable" class="flex items-center gap-3 bg-green-100 px-4 py-2 rounded-full border-2 border-green-300">
        <div class="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
        <span class="text-sm font-bold text-green-700">🔴 Live Updates</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex flex-col justify-center items-center py-16 bg-gradient-to-br from-white to-slate-50 rounded-2xl border border-slate-200 shadow-lg">
      <div class="ipl-loader mb-4"></div>
      <p class="text-ipl-blue font-bold">Loading points table...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16 bg-gradient-to-br from-red-50 to-pink-50 rounded-2xl border-2 border-red-200 shadow-lg">
      <div class="text-red-600 text-lg font-bold mb-4">⚠️ {{ error }}</div>
      <button 
        @click="fetchPointsTable" 
        class="px-6 py-3 bg-gradient-to-r from-ipl-blue to-ipl-blue-dark text-white rounded-xl hover:from-ipl-blue-dark hover:to-ipl-blue font-bold transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
      >
        🔄 Retry
      </button>
    </div>

    <!-- Points Table -->
    <div v-else-if="pointsTable" class="bg-white rounded-3xl shadow-xl border border-ipl-blue/10">
      <!-- Table Header -->
      <div class="px-6 py-5 border-b border-ipl-blue/20 bg-gradient-to-r from-ipl-blue/5 to-purple-50 rounded-t-3xl">
        <div class="flex justify-between items-start">
          <div class="flex items-start gap-3">
            <div class="p-2 bg-gradient-to-br from-ipl-blue/10 to-purple-100 rounded-xl">
              <svg class="w-6 h-6 text-ipl-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
              </svg>
            </div>
            <div>
              <h2 class="text-xl font-black text-ipl-blue">
                🏆 IPL {{ selectedSeason }} Standings
              </h2>
              <div v-if="selectedSeason === '2026'" class="mt-1 flex items-center gap-2 text-sm">
                <span class="font-semibold text-ipl-blue">📅 Playoffs: 26 March – 31 May 2026</span>
              </div>
            </div>
          </div>
          <div class="flex flex-col items-end gap-2">
            <div class="text-sm font-semibold text-slate-600 bg-slate-100 px-3 py-1 rounded-full">
              Last updated: {{ formatDate(pointsTable.last_updated) }}
            </div>
            <div v-if="selectedSeason === '2026'" class="flex items-center gap-2 text-xs text-slate-500 bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
              <svg class="w-4 h-4 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
              </svg>
              <span class="font-medium">Table updated daily at end of day</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Table Content -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gradient-to-r from-ipl-blue/10 to-purple-50">
            <tr class="text-left">
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider">📍 Pos</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider">🏏 Team</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider text-center">P</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider text-center">W</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider text-center">L</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider text-center">NR</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider text-center">Pts</th>
              <th class="px-6 py-4 text-xs font-black text-ipl-blue uppercase tracking-wider text-center">NRR</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            <tr 
              v-for="team in pointsTable.teams" 
              :key="team.position"
              class="hover:bg-gradient-to-r hover:from-ipl-blue/5 hover:to-purple-50 transition-all duration-300"
              :class="getTeamRowClass(team.position, team.status)"
            >
              <td class="px-6 py-5">
                <div class="flex items-center">
                  <span class="font-black text-ipl-blue text-lg">{{ team.position }}</span>
                  <span v-if="team.status" class="ml-3 text-xs font-bold px-2 py-1 rounded-full" :class="getStatusBadgeClass(team.status)">
                    {{ team.status }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-5">
                <div class="flex items-center gap-3 hover:scale-105 transition-transform duration-200">
                  <TeamLogo :teamName="getFullTeamName(team.team)" size="md" :showName="false" />
                  <span class="font-bold text-slate-900 text-base">{{ getFullTeamName(team.team) }}</span>
                </div>
              </td>
              <td class="px-6 py-5 text-center font-bold text-slate-700">{{ team.played }}</td>
              <td class="px-6 py-5 text-center font-black text-green-700 text-lg">{{ team.won }}</td>
              <td class="px-6 py-5 text-center font-black text-red-700 text-lg">{{ team.lost }}</td>
              <td class="px-6 py-5 text-center font-semibold text-slate-500">{{ team.no_result }}</td>
              <td class="px-6 py-5 text-center font-black text-ipl-blue text-xl">{{ team.points }}</td>
              <td class="px-6 py-5 text-center font-mono font-bold text-base" :class="getNRRClass(team.nrr)">
                {{ formatNRR(team.nrr) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Legend -->
      <div class="px-6 py-5 border-t border-ipl-blue/20 bg-gradient-to-r from-slate-50 to-slate-100 rounded-b-3xl">
        <div class="flex flex-wrap gap-6 text-xs font-semibold text-slate-600">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-ipl-blue rounded-full"></div>
            <span>P: Played • W: Won • L: Lost • NR: No Result • Pts: Points • NRR: Net Run Rate</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import TeamLogo from '~/components/TeamLogo.vue'
import { useHead } from '#app'
import { TrophyIcon } from '@heroicons/vue/24/outline'

// Nuxt composables
const config = useRuntimeConfig()

// Define TypeScript interfaces
interface PointsTableTeam {
  position: number
  team: string
  played: number
  won: number
  lost: number
  no_result: number
  points: number
  nrr: number
  status?: string
}

interface PointsTable {
  season: string
  last_updated: string
  teams: PointsTableTeam[]
}

// Reactive data
const selectedSeason = ref('2026')
const availableSeasons = ref<string[]>([])
const pointsTable = ref<PointsTable | null>(null)
const loading = ref(false)
const error = ref<string | null>(null)
let refreshInterval: NodeJS.Timeout | null = null

// Team name mappings from codes to full names
const teamNameMap: Record<string, string> = {
  'CSK': 'Chennai Super Kings',
  'MI': 'Mumbai Indians',
  'RCB': 'Royal Challengers Bengaluru',
  'KKR': 'Kolkata Knight Riders',
  'DC': 'Delhi Capitals',
  'PBKS': 'Punjab Kings',
  'RR': 'Rajasthan Royals',
  'SRH': 'Sunrisers Hyderabad',
  'GT': 'Gujarat Titans',
  'LSG': 'Lucknow Super Giants',
  // Defunct teams
  'GL': 'Gujarat Lions',
  'KTK': 'Kochi Tuskers Kerala'
}

// Methods
const fetchAvailableSeasons = async () => {
  try {
    const response = await fetch(`${config.public.apiBase}/api/points-table/seasons`)
    if (response.ok) {
      const data = await response.json()
      availableSeasons.value = data.seasons.sort((a: string, b: string) => b.localeCompare(a))
    }
  } catch (err) {
    console.error('Failed to fetch available seasons:', err)
    // Fallback to all available seasons (2008-2026)
    availableSeasons.value = [
      '2026', '2025', '2024', '2023', '2022', '2021', '2020', '2019', 
      '2018', '2017', '2016', '2015', '2014', '2013', '2012', '2011', 
      '2010', '2009', '2008'
    ]
  }
}

const fetchPointsTable = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${config.public.apiBase}/api/points-table/${selectedSeason.value}`)
    
    if (!response.ok) {
      throw new Error(`Failed to fetch points table: ${response.statusText}`)
    }
    
    const data = await response.json()
    pointsTable.value = data
  } catch (err: any) {
    error.value = err.message || 'Failed to fetch points table'
    console.error('Error fetching points table:', err)
  } finally {
    loading.value = false
  }
}

const getFullTeamName = (code: string): string => {
  return teamNameMap[code] || code
}

const formatDate = (dateString: string): string => {
  return new Date(dateString).toLocaleString()
}

const formatNRR = (nrr: number): string => {
  return nrr >= 0 ? `+${nrr.toFixed(3)}` : nrr.toFixed(3)
}

const getNRRClass = (nrr: number): string => {
  if (nrr > 0) return 'text-green-600'
  if (nrr < 0) return 'text-red-600'
  return 'text-slate-600'
}

const getTeamRowClass = (position: number, status?: string): string => {
  if (status === 'Q') return 'bg-gradient-to-r from-green-50 to-emerald-50 border-l-4 border-green-500 shadow-md'
  if (status === 'E') return 'bg-gradient-to-r from-red-50 to-pink-50 border-l-4 border-red-500 shadow-md'
  if (position <= 4) return 'bg-gradient-to-r from-ipl-blue/5 to-blue-50 border-l-4 border-ipl-blue shadow-md'
  return ''
}

const getStatusBadgeClass = (status: string): string => {
  if (status === 'Q') return 'bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 border border-green-300'
  if (status === 'E') return 'bg-gradient-to-r from-red-100 to-pink-100 text-red-800 border border-red-300'
  return 'bg-gradient-to-r from-slate-100 to-slate-200 text-slate-800 border border-slate-300'
}

// Auto-refresh for live season
const setupAutoRefresh = () => {
  if (selectedSeason.value === '2026') {
    // Refresh every 30 minutes for live season
    refreshInterval = setInterval(() => {
      fetchPointsTable()
    }, 30 * 60 * 1000)
  } else if (refreshInterval) {
    clearInterval(refreshInterval)
    refreshInterval = null
  }
}

// Lifecycle
onMounted(async () => {
  await fetchAvailableSeasons()
  await fetchPointsTable()
  setupAutoRefresh()
})

onUnmounted(() => {
  if (refreshInterval) {
    clearInterval(refreshInterval)
  }
})

// Watch for season changes
watch(selectedSeason, () => {
  fetchPointsTable()
  setupAutoRefresh()
})

// SEO
useHead({
  title: 'IPL Points Table - Live Standings | Boundary Graph',
  meta: [
    {
      name: 'description',
      content: 'Live IPL points table with team standings, wins, losses, and net run rates across all seasons.'
    }
  ]
})
</script>

<style scoped>
.touch-target {
  min-height: 44px;
  min-width: 44px;
}
</style>