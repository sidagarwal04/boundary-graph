<template>
  <div class="container mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl sm:text-4xl font-black text-slate-900 mb-4">
        IPL Points Table
      </h1>
      <p class="text-slate-600 text-lg">
        Live standings and team performance across IPL seasons
      </p>
    </div>

    <!-- Season Filter -->
    <div class="mb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
      <div class="flex items-center gap-4">
        <label for="season-select" class="text-sm font-semibold text-slate-700">
          Select Season:
        </label>
        <select 
          id="season-select"
          v-model="selectedSeason" 
          @change="fetchPointsTable"
          class="px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-white"
        >
          <option v-for="season in availableSeasons" :key="season" :value="season">
            IPL {{ season }}
          </option>
        </select>
      </div>
      
      <!-- Live indicator for current season -->
      <div v-if="selectedSeason === '2026' && pointsTable" class="flex items-center gap-2">
        <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
        <span class="text-sm text-slate-600">Live Updates</span>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-16">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-16">
      <div class="text-red-500 text-lg font-semibold mb-2">{{ error }}</div>
      <button 
        @click="fetchPointsTable" 
        class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
      >
        Retry
      </button>
    </div>

    <!-- Points Table -->
    <div v-else-if="pointsTable" class="bg-white rounded-xl shadow-sm border border-slate-200">
      <!-- Table Header -->
      <div class="px-6 py-4 border-b border-slate-200 flex justify-between items-center">
        <h2 class="text-xl font-bold text-slate-900">
          IPL {{ selectedSeason }} Standings
        </h2>
        <div class="text-sm text-slate-500">
          Last updated: {{ formatDate(pointsTable.last_updated) }}
        </div>
      </div>

      <!-- Table Content -->
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-slate-50">
            <tr class="text-left">
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider">Pos</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider">Team</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">P</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">W</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">L</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">NR</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">Pts</th>
              <th class="px-6 py-3 text-xs font-bold text-slate-600 uppercase tracking-wider text-center">NRR</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-200">
            <tr 
              v-for="team in pointsTable.teams" 
              :key="team.position"
              class="hover:bg-slate-50 transition-colors"
              :class="getTeamRowClass(team.position, team.status)"
            >
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <span class="font-bold text-slate-900">{{ team.position }}</span>
                  <span v-if="team.status" class="ml-2 text-xs font-semibold px-1.5 py-0.5 rounded" :class="getStatusBadgeClass(team.status)">
                    {{ team.status }}
                  </span>
                </div>
              </td>
              <td class="px-6 py-4">
                <div class="flex items-center">
                  <TeamLogo :teamName="getFullTeamName(team.team)" size="sm" :showName="false" />
                  <span class="ml-3 font-semibold text-slate-900">{{ getFullTeamName(team.team) }}</span>
                </div>
              </td>
              <td class="px-6 py-4 text-center text-slate-700">{{ team.played }}</td>
              <td class="px-6 py-4 text-center font-semibold text-green-600">{{ team.won }}</td>
              <td class="px-6 py-4 text-center font-semibold text-red-600">{{ team.lost }}</td>
              <td class="px-6 py-4 text-center text-slate-500">{{ team.no_result }}</td>
              <td class="px-6 py-4 text-center font-bold text-slate-900">{{ team.points }}</td>
              <td class="px-6 py-4 text-center font-mono" :class="getNRRClass(team.nrr)">
                {{ formatNRR(team.nrr) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Legend -->
      <div class="px-6 py-4 border-t border-slate-200 bg-slate-50">
        <div class="flex flex-wrap gap-6 text-xs text-slate-600">
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 bg-green-100 border border-green-300 rounded"></span>
            <span>Qualified (Q)</span>
          </div>
          <div class="flex items-center gap-2">
            <span class="w-3 h-3 bg-red-100 border border-red-300 rounded"></span>
            <span>Eliminated (E)</span>
          </div>
          <div class="text-slate-500">
            P: Played • W: Won • L: Lost • NR: No Result • Pts: Points • NRR: Net Run Rate
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import TeamLogo from '~/components/TeamLogo.vue'

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
  'LSG': 'Lucknow Super Giants'
}

// Methods
const fetchAvailableSeasons = async () => {
  try {
    const response = await fetch(`${config.public.apiUrl}/api/points-table/seasons`)
    if (response.ok) {
      const data = await response.json()
      availableSeasons.value = data.seasons.sort((a: string, b: string) => b.localeCompare(a))
    }
  } catch (err) {
    console.error('Failed to fetch available seasons:', err)
    // Fallback to default seasons
    availableSeasons.value = ['2026', '2025', '2024', '2023']
  }
}

const fetchPointsTable = async () => {
  loading.value = true
  error.value = null
  
  try {
    const response = await fetch(`${config.public.apiUrl}/api/points-table/${selectedSeason.value}`)
    
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
  if (status === 'Q') return 'bg-green-50 border-l-4 border-green-500'
  if (status === 'E') return 'bg-red-50 border-l-4 border-red-500'
  if (position <= 4) return 'bg-blue-50 border-l-4 border-blue-500'
  return ''
}

const getStatusBadgeClass = (status: string): string => {
  if (status === 'Q') return 'bg-green-100 text-green-800'
  if (status === 'E') return 'bg-red-100 text-red-800'
  return 'bg-slate-100 text-slate-800'
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