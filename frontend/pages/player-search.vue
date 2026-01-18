<template>
  <div>
    <h1 class="text-3xl font-bold mb-8">🔍 Player Search & Stats</h1>
    
    <div class="stat-card mb-8">
      <div class="flex gap-3">
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Search players..."
          class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          @input="searchPlayers"
        />
      </div>
      
      <!-- Autocomplete Results -->
      <div v-if="searchResults.length > 0 && showResults" class="mt-2 bg-white border border-slate-200 rounded-lg shadow-lg max-h-48 overflow-y-auto">
        <button 
          v-for="player in searchResults" 
          :key="player"
          @click="selectPlayer(player)"
          class="w-full text-left px-4 py-2 hover:bg-blue-50 border-b last:border-b-0"
        >
          {{ player }}
        </button>
      </div>
    </div>

    <!-- Player Stats -->
    <div v-if="playerStats" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Batting Stats -->
        <div class="stat-card">
          <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
            <span>🏏</span> Batting Statistics
          </h2>
          <div class="space-y-4">
            <div class="flex justify-between">
              <span class="text-slate-600">Matches</span>
              <span class="font-bold text-blue-600">{{ playerStats.batting_matches || '-' }}</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Runs</span>
              <span class="font-bold text-green-600">{{ playerStats.total_runs || '-' }}</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Strike Rate</span>
              <span class="font-bold text-orange-600">{{ playerStats.strike_rate || '-' }}%</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Fours</span>
              <span class="font-bold">{{ playerStats.total_fours || '-' }}</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Sixes</span>
              <span class="font-bold">{{ playerStats.total_sixes || '-' }}</span>
            </div>
          </div>
        </div>

        <!-- Bowling Stats -->
        <div class="stat-card">
          <h2 class="text-xl font-bold mb-6 flex items-center gap-2">
            <span>🎯</span> Bowling Statistics
          </h2>
          <div class="space-y-4">
            <div class="flex justify-between">
              <span class="text-slate-600">Matches</span>
              <span class="font-bold text-blue-600">{{ playerStats.bowling_matches || '-' }}</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Wickets</span>
              <span class="font-bold text-red-600">{{ playerStats.total_wickets || '-' }}</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Economy</span>
              <span class="font-bold text-orange-600">{{ playerStats.economy || '-' }}</span>
            </div>
            <div class="flex justify-between border-t pt-3">
              <span class="text-slate-600">Runs Conceded</span>
              <span class="font-bold">{{ playerStats.runs_conceded || '-' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- No Player Selected -->
    <div v-else class="stat-card text-center text-slate-600 py-12">
      <p class="text-lg">Search for a player to view detailed statistics</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

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
