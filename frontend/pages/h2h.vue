<template>
  <div>
    <h1 class="text-3xl font-bold mb-8">⚔️ Head-to-Head</h1>
    
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <!-- Team Selector -->
      <div class="stat-card">
        <label class="block text-sm font-semibold mb-2">Team 1</label>
        <select 
          v-model="team1"
          class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">Select Team...</option>
          <option v-for="team in teams" :key="team" :value="team">
            {{ team }}
          </option>
        </select>
      </div>
      
      <div class="stat-card">
        <label class="block text-sm font-semibold mb-2">Team 2</label>
        <select 
          v-model="team2"
          class="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
        >
          <option value="">Select Team...</option>
          <option v-for="team in teams" :key="team" :value="team">
            {{ team }}
          </option>
        </select>
      </div>
    </div>

    <button @click="loadH2H" class="btn-primary mb-8">
      Load Head-to-Head
    </button>

    <!-- H2H Stats -->
    <div v-if="h2hStats.total_matches > 0" class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="stat-card text-center">
        <p class="text-slate-600 mb-2">Total Matches</p>
        <p class="text-4xl font-bold text-blue-600">{{ h2hStats.total_matches }}</p>
      </div>
      
      <div class="stat-card text-center">
        <p class="text-slate-600 mb-2">{{ team1 }} Wins</p>
        <p class="text-4xl font-bold text-green-600">{{ h2hStats.team1_wins }}</p>
      </div>
      
      <div class="stat-card text-center">
        <p class="text-slate-600 mb-2">{{ team2 }} Wins</p>
        <p class="text-4xl font-bold text-orange-600">{{ h2hStats.team2_wins }}</p>
      </div>
    </div>

    <!-- Recent Matches -->
    <div v-if="matches.length > 0" class="stat-card">
      <h2 class="text-xl font-bold mb-4">Recent Matches</h2>
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-slate-100">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-semibold">Date</th>
              <th class="px-4 py-3 text-left text-sm font-semibold">Season</th>
              <th class="px-4 py-3 text-left text-sm font-semibold">Winner</th>
              <th class="px-4 py-3 text-left text-sm font-semibold">Venue</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="match in matches" :key="match.date" class="border-b hover:bg-slate-50">
              <td class="px-4 py-3 text-sm">{{ formatDate(match.date) }}</td>
              <td class="px-4 py-3 text-sm font-medium">{{ match.season }}</td>
              <td class="px-4 py-3 text-sm font-bold text-green-600">{{ match.winner }}</td>
              <td class="px-4 py-3 text-sm">{{ match.venue }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const team1 = ref('')
const team2 = ref('')
const teams = ref<any[]>([])
const h2hStats = ref<any>({ total_matches: 0, team1_wins: 0, team2_wins: 0 })
const matches = ref<any[]>([])

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-IN')
}

const loadTeams = async () => {
  try {
    const response = await $fetch(`${config.public.apiBase}/api/teams`)
    // response is an array of objects with name property
    teams.value = Array.isArray(response) ? response.map((t: any) => t.name) : []
    console.log('Teams loaded:', teams.value)
  } catch (error) {
    console.error('Error loading teams:', error)
  }
}

onMounted(() => {
  loadTeams()
})

const loadH2H = async () => {
  if (!team1.value || !team2.value) {
    alert('Please enter both team names')
    return
  }
  
  try {
    const stats = await $fetch(`${config.public.apiBase}/api/h2h/${encodeURIComponent(team1.value)}/${encodeURIComponent(team2.value)}`)
    h2hStats.value = stats
    
    try {
      const matchesData = await $fetch(`${config.public.apiBase}/api/h2h/${encodeURIComponent(team1.value)}/${encodeURIComponent(team2.value)}/matches`)
      matches.value = Array.isArray(matchesData) ? matchesData : []
    } catch (matchError) {
      console.error('Could not fetch matches:', matchError)
      matches.value = []
    }
  } catch (error) {
    console.error('Failed to fetch H2H data:', error)
    alert(`Error: Could not find data for these teams. Make sure team names are exact (e.g., "Mumbai Indians", "Royal Challengers Bangalore")`)
  }
}
</script>
