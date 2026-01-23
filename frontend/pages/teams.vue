<template>
  <div class="space-y-8 pb-12">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-brand-primary/10 text-brand-primary rounded-full text-xs font-bold uppercase tracking-widest">
          <CricketTeamIcon class="w-3 h-3" />
          Team Intelligence
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">Teams & <span class="text-brand-primary">Statistics</span></h1>
        <p class="text-slate-500 max-w-xl">
          Explore the dynasties and rivalries that define the IPL. Track team's evolution, squad compositions, and head-to-head battle records across all seasons.
        </p>
      </div>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
      <!-- Team Selector -->
      <div class="lg:col-span-4 lg:sticky lg:top-24 h-fit">
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-5 py-4 border-b border-slate-100 bg-slate-50/50">
            <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider">Select Team</h2>
          </div>
          <div class="p-4 space-y-4 max-h-[calc(100vh-250px)] overflow-y-auto custom-scrollbar">
            <!-- Active Teams separator -->
            <div class="relative py-2">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-slate-200"></div>
              </div>
              <div class="relative flex justify-center">
                <span class="bg-white px-2 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Active Teams</span>
              </div>
            </div>
            
            <!-- Active Teams -->
            <div class="space-y-1">
              <div v-for="team in activeTeams" :key="team.name">
                <button 
                  @click="selectTeam(team)"
                  :class="[
                    'w-full text-left px-4 py-2.5 rounded-lg transition-all duration-200 text-sm font-medium border',
                    selectedTeam?.name === team.name 
                      ? 'bg-brand-primary text-white border-brand-primary shadow-md shadow-brand-primary/20' 
                      : 'bg-white text-slate-600 hover:bg-slate-50 border-transparent'
                  ]"
                >
                  <TeamLogo :teamName="team.name" size="sm" :showName="true" :textClass="selectedTeam?.name === team.name ? 'text-white' : 'text-slate-600'" />
                </button>
              </div>
            </div>

            <!-- Separator -->
            <div class="relative py-2">
              <div class="absolute inset-0 flex items-center" aria-hidden="true">
                <div class="w-full border-t border-slate-200"></div>
              </div>
              <div class="relative flex justify-center">
                <span class="bg-white px-2 text-[10px] font-bold text-slate-400 uppercase tracking-widest">Defunct Teams</span>
              </div>
            </div>

            <!-- Defunct Teams -->
            <div class="space-y-1">
              <div v-for="team in defunctTeams" :key="team.name">
                <button 
                  @click="selectTeam(team)"
                  :class="[
                    'w-full text-left px-4 py-2.5 rounded-lg transition-all duration-200 text-sm font-medium border opacity-75',
                    selectedTeam?.name === team.name 
                      ? 'bg-slate-800 text-white border-slate-800 shadow-md shadow-slate-800/20' 
                      : 'bg-white text-slate-500 hover:bg-slate-50 border-transparent'
                  ]"
                >
                  <div class="flex items-center justify-between w-full">
                    <TeamLogo :teamName="team.name" size="sm" :showName="true" :textClass="selectedTeam?.name === team.name ? 'text-white' : 'text-slate-500'" />
                    <span v-if="selectedTeam?.name === team.name" class="text-[10px] opacity-60">(Defunct)</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Stats Panel -->
      <div v-if="selectedTeam" class="lg:col-span-8 space-y-8">
        <!-- Main Stats -->
        <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-6 py-5 border-b border-slate-100 flex items-start justify-between">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-3 mb-2">
                <TeamLogo :teamName="selectedTeam.name" size="lg" :showName="false" />
                <h2 class="text-2xl font-extrabold text-slate-900">{{ selectedTeam.name }}</h2>
              </div>
              <p class="text-xs font-medium text-slate-400 mt-1 uppercase tracking-wider">
                {{ selectedTeam.is_active ? 'Currently Active' : 'Defunct Franchise' }}
              </p>
            </div>
            <div class="ml-6 flex-shrink-0">
              <div v-if="!selectedTeam.is_active" class="px-2 py-1 mb-2 bg-slate-100 text-slate-500 text-[10px] font-bold rounded uppercase text-center">
                Historical
              </div>
              <div class="bg-slate-50 border border-slate-100 rounded-lg px-4 py-3 shadow-sm w-64 min-w-[25rem] max-w-[25rem]">
                <div class="text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2 text-center">Team Information</div>
                <div class="grid grid-cols-2 gap-x-4 gap-y-2">
                  <div class="flex flex-col items-start">
                    <span class="flex items-center gap-1 text-[10px] text-slate-400 font-bold uppercase"><span class="w-2 h-2 rounded-full bg-brand-primary"></span>Captain</span>
                    <span class="text-sm font-semibold text-slate-900">{{ teamDetails?.captain || 'N/A' }}</span>
                  </div>
                  <div class="flex flex-col items-start">
                    <span class="flex items-center gap-1 text-[10px] text-slate-400 font-bold uppercase"><span class="w-2 h-2 rounded-full bg-green-500"></span>Coach</span>
                    <span class="text-sm font-semibold text-slate-900">{{ teamDetails?.coach || 'N/A' }}</span>
                  </div>
                  <div class="flex flex-col items-start">
                    <span class="flex items-center gap-1 text-[10px] text-slate-400 font-bold uppercase"><span class="w-2 h-2 rounded-full bg-yellow-500"></span>Owner</span>
                    <span class="text-sm font-semibold text-slate-900">{{ teamDetails?.owner || 'N/A' }}</span>
                  </div>
                  <div class="flex flex-col items-start">
                    <span class="flex items-center gap-1 text-[10px] text-slate-400 font-bold uppercase"><span class="w-2 h-2 rounded-full bg-purple-500"></span>Venue</span>
                    <span class="text-sm font-semibold text-slate-900">{{ teamDetails?.venue || 'N/A' }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="grid grid-cols-1 md:grid-cols-3 divide-y md:divide-y-0 md:divide-x divide-slate-100">
            <div class="p-6">
              <p class="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1">Total Matches</p>
              <p class="text-4xl font-black text-slate-900">{{ teamStats.total_matches }}</p>
            </div>
            <div class="p-6">
              <p class="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1">Total Wins</p>
              <p class="text-4xl font-black text-brand-primary">{{ teamStats.wins }}</p>
            </div>
            <div class="p-6">
              <p class="text-slate-500 text-xs font-bold uppercase tracking-wider mb-1">Win Rate</p>
              <div class="flex items-baseline gap-1">
                <p class="text-4xl font-black text-brand-accent">{{ teamStats.win_percentage }}</p>
                <span class="text-lg font-bold text-slate-400">%</span>
              </div>
            </div>
          </div>

          <!-- Trophies Row -->
          <div v-if="teamStats.trophies?.length" class="p-6 bg-yellow-50/50 border-t border-yellow-100 flex flex-wrap items-center gap-4">
            <span class="text-xs font-black text-yellow-700 uppercase tracking-widest">IPL Champions</span>
            <div class="flex flex-wrap gap-2">
              <div v-for="year in teamStats.trophies" :key="year" class="flex items-center gap-1.5 px-3 py-1 bg-white rounded-lg border border-yellow-200 text-yellow-700 shadow-sm">
                <TrophyIcon class="w-3.5 h-3.5 fill-yellow-400" />
                <span class="text-xs font-black">{{ year }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Rivalry Intelligence -->
        <div v-if="rivalries.length > 0" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/30 flex justify-between items-center">
             <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider">H2H Rivalry Intelligence</h2>
             <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Win % vs Opponents</span>
          </div>
          <div class="divide-y divide-slate-50">
            <div v-for="rival in rivalries" :key="rival.opponent" class="p-4 flex items-center justify-between hover:bg-slate-50/50 transition-colors">
              <div class="flex-1 min-w-0">
                <div class="flex items-center gap-2">
                  <TeamLogo :teamName="rival.opponent" size="md" :showName="true" textClass="font-bold text-slate-800 truncate" />
                  <span class="text-[10px] text-slate-400 font-medium uppercase">• {{ rival.matches }} Matches Played</span>
                </div>
              </div>
              <div class="flex items-center gap-6">
                <div class="text-right">
                  <p class="text-sm font-black text-slate-900">{{ rival.wins }}W - {{ rival.matches - rival.wins }}L</p>
                  <p class="text-[10px] font-bold text-slate-400">{{ rival.win_pct }}% Win Ratio</p>
                </div>
                <div class="w-24 h-1.5 bg-slate-100 rounded-full overflow-hidden">
                  <div class="h-full bg-brand-primary rounded-full transition-all duration-700" :style="{ width: rival.win_pct + '%' }"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Squad Section with Season Dropdown and Segmentation -->
        <div v-if="Object.keys(seasonSquads).length > 0" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/30 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider">Squad by Season & Role</h2>
            <div>
              <select v-model="selectedSeason" class="border border-slate-200 rounded px-2 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-brand-primary">
                <option v-for="season in availableSeasons" :key="season" :value="season">{{ season }}</option>
              </select>
            </div>
          </div>
          <div class="p-6">
            <div v-if="segmentedSquad.batters.length > 0" class="mb-6">
              <h3 class="text-xs font-bold text-brand-primary uppercase tracking-wider mb-2">Batters</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <button v-for="player in segmentedSquad.batters" :key="player.name" @click="goToPlayer(player.name)" class="group text-left p-3 bg-white border border-slate-100 hover:border-brand-primary/30 hover:bg-slate-50 rounded-lg transition-all duration-200">
                  <p class="text-sm font-semibold text-slate-700 group-hover:text-brand-primary transition-colors">{{ player.name }}</p>
                  <p class="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Batter</p>
                </button>
              </div>
            </div>
            <div v-if="segmentedSquad.bowlers.length > 0" class="mb-6">
              <h3 class="text-xs font-bold text-green-600 uppercase tracking-wider mb-2">Bowlers</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <button v-for="player in segmentedSquad.bowlers" :key="player.name" @click="goToPlayer(player.name)" class="group text-left p-3 bg-white border border-slate-100 hover:border-green-500/30 hover:bg-slate-50 rounded-lg transition-all duration-200">
                  <p class="text-sm font-semibold text-slate-700 group-hover:text-green-600 transition-colors">{{ player.name }}</p>
                  <p class="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Bowler</p>
                </button>
              </div>
            </div>
            <div v-if="segmentedSquad.wicketKeepers.length > 0" class="mb-6">
              <h3 class="text-xs font-bold text-purple-600 uppercase tracking-wider mb-2">Wicket-keepers</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <button v-for="player in segmentedSquad.wicketKeepers" :key="player.name" @click="goToPlayer(player.name)" class="group text-left p-3 bg-white border border-slate-100 hover:border-purple-500/30 hover:bg-slate-50 rounded-lg transition-all duration-200">
                  <p class="text-sm font-semibold text-slate-700 group-hover:text-purple-600 transition-colors">{{ player.name }}</p>
                  <p class="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Wicket-keeper</p>
                </button>
              </div>
            </div>
            <div v-if="segmentedSquad.allRounders.length > 0">
              <h3 class="text-xs font-bold text-yellow-600 uppercase tracking-wider mb-2">All Rounders</h3>
              <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                <button v-for="player in segmentedSquad.allRounders" :key="player.name" @click="goToPlayer(player.name)" class="group text-left p-3 bg-white border border-slate-100 hover:border-yellow-500/30 hover:bg-slate-50 rounded-lg transition-all duration-200">
                  <p class="text-sm font-semibold text-slate-700 group-hover:text-yellow-600 transition-colors">{{ player.name }}</p>
                  <p class="text-[10px] text-slate-400 font-medium uppercase mt-0.5">All Rounder</p>
                </button>
              </div>
            </div>
            <div v-if="segmentedSquad.batters.length === 0 && segmentedSquad.bowlers.length === 0 && segmentedSquad.allRounders.length === 0 && segmentedSquad.wicketKeepers.length === 0" class="text-slate-400 text-sm text-center py-8">No players found for this season.</div>
          </div>
        </div>

        <!-- Squad Loading State -->
        <div v-else-if="selectedTeam" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/30">
            <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider">Squad by Season & Role</h2>
          </div>
          <div class="p-6 text-center py-12">
            <div class="animate-pulse">
              <div class="w-8 h-8 bg-brand-primary/20 rounded-full mx-auto mb-3"></div>
              <p class="text-slate-500 text-sm">Loading squad data...</p>
              <p class="text-slate-400 text-xs mt-1">Fetching player database</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { TrophyIcon } from '@heroicons/vue/24/outline'
import CricketTeamIcon from '~/components/icons/CricketTeamIcon.vue'
import TeamLogo from '~/components/TeamLogo.vue'
import { getTeamDetails } from '~/utils/teamLogos'

const config = useRuntimeConfig()
const route = useRoute()
const allTeams = ref<any[]>([])
const selectedTeam = ref<any>(null)
const teamStats = ref<any>({ total_matches: 0, wins: 0, win_percentage: 0, trophies: [] })
const squad = ref<any[]>([])
const seasonSquads = ref<Record<string, any[]>>({}) // { season: [ { name, role } ] }
const availableSeasons = ref<string[]>([])
const selectedSeason = ref<string>('all')
const rivalries = ref<any[]>([])


const activeTeams = computed(() => allTeams.value.filter(t => t.is_active))
const defunctTeams = computed(() => allTeams.value.filter(t => !t.is_active))

// Function to select team by name from query parameter
const selectTeamFromQuery = async () => {
  if (allTeams.value.length === 0) return
  
  const preSelectedTeamName = route.query.team as string
  console.log('Route query team:', preSelectedTeamName)
  
  if (preSelectedTeamName) {
    const decodedTeamName = decodeURIComponent(preSelectedTeamName)
    console.log('Looking for team:', decodedTeamName)
    console.log('Available teams:', allTeams.value.map(t => t.name))
    
    const teamToSelect = allTeams.value.find(t => t.name === decodedTeamName)
    if (teamToSelect) {
      console.log('Found matching team:', teamToSelect.name)
      await selectTeam(teamToSelect)
      return
    } else {
      console.warn('Team not found:', decodedTeamName)
    }
  }
  
  // If no query param or team not found, select first active team by default
  if (!selectedTeam.value) {
    const defaultTeam = allTeams.value.find(t => t.is_active) || allTeams.value[0]
    await selectTeam(defaultTeam)
  }
}

// Watch for route changes
watch(() => route.query.team, () => {
  selectTeamFromQuery()
}, { immediate: false })
const teamDetails = computed(() => {
  return selectedTeam.value ? getTeamDetails(selectedTeam.value.name) : null
})

const segmentedSquad = computed(() => {
  const season = selectedSeason.value
  const players = seasonSquads.value[season] || []
  
  // Safety check: ensure players is an array
  if (!Array.isArray(players)) {
    console.warn(`Squad data for season ${season} is not an array:`, players)
    return {
      batters: [],
      bowlers: [],
      allRounders: [],
      wicketKeepers: []
    }
  }
  
  return {
    batters: players.filter((p: any) => p.role && (
      p.role.toLowerCase().includes('bat') && 
      !p.role.toLowerCase().includes('wicket') &&
      !p.role.toLowerCase().includes('keeper')
    )),
    bowlers: players.filter((p: any) => p.role && (
      p.role.toLowerCase().includes('bowl') ||
      p.role.toLowerCase().includes('fast') ||
      p.role.toLowerCase().includes('spin')
    )),
    allRounders: players.filter((p: any) => p.role && (
      p.role.toLowerCase().includes('all') ||
      p.role.toLowerCase().includes('round')
    )),
    wicketKeepers: players.filter((p: any) => p.role && (
      p.role.toLowerCase().includes('wicket') ||
      p.role.toLowerCase().includes('keeper')
    )),
  }
})

// Player Database Management
let PLAYER_DATABASE: Record<string, {name: string, role: string, teamHistory: Record<string, string>}> = {}
let DATABASE_LAST_UPDATED: string = ''

// Load player database from API
const loadPlayerDatabase = async () => {
  try {
    console.log('Fetching player database from API...')
    const data = await $fetch<{ players: Record<string, any>, lastUpdated?: string, totalPlayers?: number }>(`${config.public.apiBase}/api/players/all`)
    
    if (data && data.players) {
      PLAYER_DATABASE = data.players
      DATABASE_LAST_UPDATED = data.lastUpdated || ''
      console.log(`✅ Player database loaded: ${data.totalPlayers} players`)
      
      // Cache in localStorage for 1 hour to reduce API calls
      const cacheData = {
        data: data,
        timestamp: Date.now(),
        expires: Date.now() + (60 * 60 * 1000) // 1 hour
      }
      localStorage.setItem('playerDB_cache', JSON.stringify(cacheData))
      
      return true
    } else {
      console.error('Invalid response format from API')
      return false
    }
  } catch (error) {
    console.log('Player database API temporarily unavailable:', error.message || error)
    
    // Try to load from cache as fallback
    const cached = localStorage.getItem('playerDB_cache')
    if (cached) {
      try {
        const cacheData = JSON.parse(cached)
        if (cacheData.expires > Date.now()) {
          console.log('📦 Using cached player database')
          PLAYER_DATABASE = cacheData.data.players
          DATABASE_LAST_UPDATED = cacheData.data.lastUpdated
          return true
        }
      } catch (cacheError) {
        console.error('Cache parse error:', cacheError)
      }
    }
    
    return false
  }
}

// Check if cached data is still valid
const loadFromCacheIfValid = async () => {
  const cached = localStorage.getItem('playerDB_cache')
  if (cached) {
    try {
      const cacheData = JSON.parse(cached)
      if (cacheData.expires > Date.now()) {
        console.log('📦 Using valid cached player database')
        PLAYER_DATABASE = cacheData.data.players
        DATABASE_LAST_UPDATED = cacheData.data.lastUpdated
        return true
      }
    } catch (error) {
      console.error('Cache read error:', error)
    }
  }
  return false
}

// Weekly refresh function to update player database from API
const refreshPlayerDatabase = async () => {
  const lastUpdate = localStorage.getItem('playerDB_lastUpdate')
  const now = new Date().getTime()
  const weekInMs = 7 * 24 * 60 * 60 * 1000
  
  // Only refresh once a week
  if (lastUpdate && (now - parseInt(lastUpdate)) < weekInMs) {
    console.log('Player database refresh not due yet (last updated:', new Date(parseInt(lastUpdate)).toLocaleDateString(), ')')
    return
  }
  
  try {
    console.log('🔄 Refreshing player database (weekly update)...')
    await loadPlayerDatabase()
    localStorage.setItem('playerDB_lastUpdate', now.toString())
    console.log('✅ Player database refreshed successfully')
  } catch (error) {
    console.error('Failed to refresh player database:', error)
  }
}

// Helper function to get players for specific team and season from centralized database
const getPlayersForTeamSeason = (teamName: string, season: string): Array<{name: string, role: string, season: string}> => {
  const players: Array<{name: string, role: string, season: string}> = []
  
  // Check if database is loaded
  if (Object.keys(PLAYER_DATABASE).length === 0) {
    console.log('Player database not ready for', teamName, season)
    return players // Return empty array if database not loaded
  }
  
  for (const playerKey in PLAYER_DATABASE) {
    const player = PLAYER_DATABASE[playerKey]
    if (player.teamHistory[season] === teamName) {
      players.push({
        name: player.name,
        role: player.role,
        season: season
      })
    }
  }
  
  return players
}

// Helper function to populate season squads using centralized database
const populateSeasonSquads = (teamName: string): Record<string, any[]> => {
  const bySeason: Record<string, any[]> = {}
  
  // Generate all seasons
  const seasons = []
  for (let year = 2025; year >= 2008; year--) {
    seasons.push(year.toString())
  }
  
  // Initialize all seasons
  seasons.forEach(season => {
    bySeason[season] = getPlayersForTeamSeason(teamName, season)
  })
  
  // Create 'all' seasons view
  const allPlayersMap: Record<string, any> = {}
  for (const season in bySeason) {
    for (const player of bySeason[season]) {
      const playerKey = player.name.toLowerCase()
      if (!allPlayersMap[playerKey] || 
          (allPlayersMap[playerKey].role === 'Batter' && player.role !== 'Batter')) {
        allPlayersMap[playerKey] = { 
          name: player.name, 
          role: player.role,
          season: 'all'
        }
      }
    }
  }
  bySeason['all'] = Object.values(allPlayersMap)
  
  return bySeason
}

// Populate squads for all teams using the centralized database
const populateAllSeasonSquads = () => {
  // This function will be called after database is loaded
  console.log('Season squads populated from centralized database')
}

// Helper function to assign mock roles to players
const getPlayerRole = (playerName: string, index: number = 0): string => {
  const name = playerName.toLowerCase()
  
  // Specific player role assignments
  if (name.includes('dhoni') || name.includes('pant') || name.includes('karthik') || 
      name.includes('saha') || name.includes('samson') || name.includes('pooran') ||
      name.includes('kishan') || name.includes('buttler') || name.includes('de kock') ||
      name.includes('bairstow') || name.includes('rahul')) {
    return 'Wicket-keeper Batter'
  }
  
  // Common bowlers
  if (name.includes('bumrah') || name.includes('shami') || name.includes('siraj') ||
      name.includes('chahal') || name.includes('rashid') || name.includes('narine') ||
      name.includes('malinga') || name.includes('boult') || name.includes('rabada') ||
      name.includes('archer') || name.includes('bhuvi') || name.includes('ashwin') ||
      name.includes('kuldeep') || name.includes('tahir') || name.includes('umesh') ||
      name.includes('mohit') || name.includes('shardul') || name.includes('khaleel') ||
      name.includes('mustafiz') || name.includes('southee') || name.includes('hazlewood') ||
      name.includes('starc') || name.includes('ferguson') || name.includes('natarajan')) {
    return 'Bowler'
  }
  
  // Common all-rounders
  if (name.includes('pandya') || name.includes('jadeja') || name.includes('russell') ||
      name.includes('stoinis') || name.includes('cummins') || name.includes('maxwell') ||
      name.includes('curran') || name.includes('morris') || name.includes('holder') ||
      name.includes('woakes') || name.includes('dwayne') || name.includes('pollard') ||
      name.includes('shankar') || name.includes('gopal') || name.includes('axar') ||
      name.includes('washington') || name.includes('krunal') || name.includes('deepak')) {
    return 'All Rounder'
  }
  
  // Use index to create better distribution
  // This ensures roughly 50% batters, 30% bowlers, 20% all-rounders
  const roleIndex = (index + playerName.length) % 10
  
  if (roleIndex <= 1) return 'All Rounder'  // 20%
  if (roleIndex <= 4) return 'Bowler'       // 30% 
  return 'Batter'                           // 50%
}

const getTeamLabel = (team: any) => {
  let label = team.name
  
  if (team.is_active) {
    const olderNames = team.raw_names.filter((n: string) => n !== team.name)
    if (olderNames.length > 0) {
      label += ` (earlier known as ${olderNames.join(', ')})`
    }
  }
  
  return label
}

// Function to navigate to player intelligence page
const goToPlayer = (playerName: string) => {
  navigateTo(`/player-search?name=${encodeURIComponent(playerName)}`)
}

const selectTeam = async (team: any) => {
  selectedTeam.value = team
  teamStats.value = { total_matches: 0, wins: 0, win_percentage: 0 }
  squad.value = []
  
  // Skip refresh if database was recently loaded (non-blocking background refresh)
  setTimeout(() => refreshPlayerDatabase(), 100)
  
  try {
    const stats = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/stats`)
    teamStats.value = stats
  } catch (error) {
    console.error('Failed to fetch team stats:', error)
  }

  // Use centralized player database for squad data
  try {
    // First, try to get any additional players from API (for supplementing our database)
    let apiPlayers: any[] = []
    try {
      const squadData = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/squad`)
      apiPlayers = Array.isArray(squadData) ? squadData : []
    } catch (apiError) {
      console.log('No additional API squad data available, using centralized database')
    }
    
  // Use centralized database as primary source (if available)
  const bySeason = Object.keys(PLAYER_DATABASE).length > 0 
    ? populateSeasonSquads(team.name)
    : {} // Empty if database not loaded yet
  
  // If database not ready, show loading state and retry after delay
  if (Object.keys(PLAYER_DATABASE).length === 0) {
    console.log('Player database not ready yet, will supplement with API data and retry...')
    // Don't set empty data initially - wait for database to load
    seasonSquads.value = {} // Keep empty until data is ready
    availableSeasons.value = []
    selectedSeason.value = '2025'
    
    // Retry after database loads
    setTimeout(() => {
      if (Object.keys(PLAYER_DATABASE).length > 0 && selectedTeam.value?.name === team.name) {
        console.log('Retrying squad population with loaded database...')
        const updatedBySeason = populateSeasonSquads(team.name)
        seasonSquads.value = updatedBySeason
        availableSeasons.value = Object.keys(updatedBySeason).filter(s => s !== 'all').sort((a, b) => b.localeCompare(a))
        selectedSeason.value = availableSeasons.value[0] || '2025'
      }
    }, 2000) // Wait 2 seconds for database to load
    
    // Exit early - don't process empty data
    return
  }
    
    // Supplement with any additional API data if available
    if (apiPlayers.length > 0 && typeof apiPlayers[0] === 'string') {
      // If API returns additional players as strings, add them to recent seasons
      const recentSeasons = ['2025', '2024', '2023']
      recentSeasons.forEach((season, seasonIndex) => {
        // Ensure bySeason[season] exists and is an array
        if (!bySeason[season]) {
          bySeason[season] = []
        }
        
        const existingNames = new Set(bySeason[season].map(p => p.name.toLowerCase()))
        const newPlayers = apiPlayers
          .filter((name: string) => !existingNames.has(name.toLowerCase()))
          .slice(0, Math.max(5, 15 - bySeason[season].length)) // Add up to fill squad
        
        newPlayers.forEach((name: string, index: number) => {
          bySeason[season].push({
            name: name,
            role: getPlayerRole(name, index + seasonIndex),
            season: season
          })
        })
      })
    }

    seasonSquads.value = bySeason
    availableSeasons.value = Object.keys(bySeason).filter(s => s !== 'all').sort((a, b) => b.localeCompare(a))
    selectedSeason.value = availableSeasons.value[0] || '2025' // Default to latest season (2025)
    
    console.log('Squad data for', team.name, 'loaded from centralized database')
    console.log('Available seasons:', availableSeasons.value)
    console.log('Players for', selectedSeason.value, ':', bySeason[selectedSeason.value]?.length)
    
  } catch (error) {
    console.error('Failed to load squad data:', error)
    seasonSquads.value = {}
    availableSeasons.value = []
    selectedSeason.value = '2025'
  }

  try {
    const rivalData = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/rivalries`)
    rivalries.value = Array.isArray(rivalData) ? rivalData : []
  } catch (error) {
    console.error('Failed to fetch rivalry data:', error)
    rivalries.value = []
  }
}

onMounted(async () => {
  try {
    // Load teams data first (faster, smaller dataset)
    console.log('Loading teams...')
    const teamsData = await $fetch(`${config.public.apiBase}/api/teams`)
    allTeams.value = Array.isArray(teamsData) ? teamsData : []
    
    // After teams are loaded, check for query parameter
    await selectTeamFromQuery()

    // Load player database in the background (non-blocking)
    setTimeout(async () => {
      try {
        console.log('Loading player database in background...')
        let loaded = await loadFromCacheIfValid()
        
        if (!loaded) {
          // If no valid cache, fetch from API with timeout (5 seconds)
          loaded = await Promise.race([
            loadPlayerDatabase(),
            new Promise((_, reject) => setTimeout(() => reject(new Error('Database load timeout')), 5000))
          ]) as boolean
        }
        
        if (loaded) {
          console.log(`✅ Player database ready: ${Object.keys(PLAYER_DATABASE).length} players`)
          populateAllSeasonSquads()
          // Run weekly refresh check in background
          setTimeout(() => refreshPlayerDatabase(), 1000)
        } else {
          console.log('🔄 Player database not available - using fallback data')
        }
      } catch (dbError) {
        console.log('🔄 Player database temporarily unavailable, using fallback mode:', dbError.message || dbError)
      }
    }, 100) // Small delay to ensure teams load first
    
  } catch (error) {
    console.error('Error in onMounted:', error)
  }
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #e2e8f0;
  border-radius: 10px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #cbd5e1;
}
</style>
