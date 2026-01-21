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
          <div class="px-6 py-5 border-b border-slate-100 flex items-center justify-between">
            <div>
              <div class="flex items-center gap-3 mb-2">
                <TeamLogo :teamName="selectedTeam.name" size="lg" :showName="false" />
                <h2 class="text-2xl font-bold text-slate-900">{{ selectedTeam.name }}</h2>
              </div>
              <p class="text-xs font-medium text-slate-400 mt-1 uppercase tracking-wider">
                {{ selectedTeam.is_active ? 'Currently Active' : 'Defunct Franchise' }}
              </p>
            </div>
            <div v-if="!selectedTeam.is_active" class="px-2 py-1 bg-slate-100 text-slate-500 text-[10px] font-bold rounded uppercase">
              Historical
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

        <!-- Squad Section -->
        <div v-if="squad.length > 0" class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/30">
            <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider">Historical Squad Members</h2>
          </div>
          <div class="p-6">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
              <button 
                v-for="player in squad" 
                :key="player"
                @click="goToPlayer(player)"
                class="group text-left p-3 bg-white border border-slate-100 hover:border-brand-primary/30 hover:bg-slate-50 rounded-lg transition-all duration-200"
              >
                <p class="text-sm font-semibold text-slate-700 group-hover:text-brand-primary transition-colors">{{ player }}</p>
                <p class="text-[10px] text-slate-400 font-medium uppercase mt-0.5">Player</p>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { TrophyIcon } from '@heroicons/vue/24/outline'
import CricketTeamIcon from '~/components/icons/CricketTeamIcon.vue'
import TeamLogo from '~/components/TeamLogo.vue'

const config = useRuntimeConfig()
const allTeams = ref<any[]>([])
const selectedTeam = ref<any>(null)
const teamStats = ref<any>({ total_matches: 0, wins: 0, win_percentage: 0, trophies: [] })
const squad = ref<any[]>([])
const rivalries = ref<any[]>([])

const activeTeams = computed(() => allTeams.value.filter(t => t.is_active))
const defunctTeams = computed(() => allTeams.value.filter(t => !t.is_active))

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

const selectTeam = async (team: any) => {
  selectedTeam.value = team
  teamStats.value = { total_matches: 0, wins: 0, win_percentage: 0 }
  squad.value = []
  
  try {
    const stats = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/stats`)
    teamStats.value = stats
  } catch (error) {
    console.error('Failed to fetch team stats:', error)
  }
  
  try {
    const squadData = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/squad`)
    squad.value = Array.isArray(squadData) ? squadData : []
  } catch (error) {
    console.error('Failed to fetch squad data:', error)
    squad.value = []
  }

  try {
    const rivalData = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/rivalries`)
    rivalries.value = Array.isArray(rivalData) ? rivalData : []
  } catch (error) {
    console.error('Failed to fetch rivalry data:', error)
    rivalries.value = []
  }
}

const goToPlayer = (playerName: string) => {
  navigateTo(`/player-search?name=${encodeURIComponent(playerName)}`)
}

onMounted(async () => {
  try {
    const teamsData = await $fetch(`${config.public.apiBase}/api/teams`)
    allTeams.value = Array.isArray(teamsData) ? teamsData : []
    
    if (allTeams.value.length > 0) {
      // Find First active team to select by default
      const firstActive = allTeams.value.find(t => t.is_active) || allTeams.value[0]
      await selectTeam(firstActive)
    }
  } catch (error) {
    console.error('Failed to fetch teams:', error)
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
