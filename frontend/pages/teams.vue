<template>
  <div>
    <h1 class="text-3xl font-bold mb-8">🏟️ Teams & Franchises</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
      <!-- Franchise Selector -->
      <div class="stat-card">
        <h2 class="text-xl font-bold mb-4">Select Franchise</h2>
        <div class="grid grid-cols-2 gap-2">
          <button 
            v-for="franchise in franchises" 
            :key="franchise.franchise_id"
            @click="selectFranchise(franchise)"
            :class="[
              'px-4 py-2 rounded-lg transition text-sm font-medium',
              selectedFranchise?.franchise_id === franchise.franchise_id 
                ? 'bg-blue-600 text-white' 
                : 'bg-slate-100 text-slate-900 hover:bg-slate-200'
            ]"
          >
            {{ franchise.current_name }}
          </button>
        </div>
      </div>

      <!-- Team Stats -->
      <div v-if="selectedFranchise" class="stat-card">
        <h2 class="text-xl font-bold mb-4">{{ selectedFranchise.current_name }} Statistics</h2>
        <div class="space-y-4">
          <div>
            <p class="text-slate-600 text-sm">Total Matches</p>
            <p class="text-3xl font-bold text-blue-600">{{ teamStats.total_matches }}</p>
          </div>
          <div>
            <p class="text-slate-600 text-sm">Wins</p>
            <p class="text-3xl font-bold text-green-600">{{ teamStats.wins }}</p>
          </div>
          <div>
            <p class="text-slate-600 text-sm">Win Percentage</p>
            <p class="text-3xl font-bold text-orange-600">{{ teamStats.win_percentage }}%</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Squad -->
    <div v-if="selectedFranchise && squad.length > 0" class="stat-card mt-8">
      <h2 class="text-xl font-bold mb-4">{{ selectedFranchise.current_name }} Squad</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
        <button 
          v-for="player in squad" 
          :key="player"
          @click="goToPlayer(player)"
          class="px-3 py-2 bg-slate-100 hover:bg-blue-100 rounded text-sm font-medium transition"
        >
          {{ player }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const franchises = ref<any[]>([])
const selectedFranchise = ref<any>(null)
const teamStats = ref<any>({ total_matches: 0, wins: 0, win_percentage: 0 })
const squad = ref<any[]>([])

const selectFranchise = async (franchise: any) => {
  selectedFranchise.value = franchise
  teamStats.value = { total_matches: 0, wins: 0, win_percentage: 0 }
  squad.value = []
  
  try {
    const stats = await $fetch(`${config.public.apiBase}/api/team/${franchise.franchise_id}/stats`)
    teamStats.value = stats
  } catch (error) {
    console.error('Failed to fetch team stats:', error)
  }
  
  try {
    const squadData = await $fetch(`${config.public.apiBase}/api/team/${franchise.franchise_id}/squad`)
    squad.value = Array.isArray(squadData) ? squadData : []
  } catch (error) {
    console.error('Failed to fetch squad data:', error)
    squad.value = []
  }
}

const goToPlayer = (playerName: string) => {
  navigateTo(`/player-search?name=${encodeURIComponent(playerName)}`)
}

onMounted(async () => {
  try {
    franchises.value = await $fetch(`${config.public.apiBase}/api/franchises`)
    if (franchises.value.length > 0) {
      await selectFranchise(franchises.value[0])
    }
  } catch (error) {
    console.error('Failed to fetch franchises:', error)
  }
})
</script>
