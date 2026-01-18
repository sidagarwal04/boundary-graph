<template>
  <div class="space-y-8 pb-12">
    <!-- Header -->
    <div class="flex items-center gap-3">
      <div class="w-10 h-10 bg-brand-primary/10 rounded-lg flex items-center justify-center">
        <span class="text-xl">⚔️</span>
      </div>
      <h1 class="text-3xl font-bold text-slate-900 tracking-tight">Head-to-Head Analysis</h1>
    </div>
    
    <!-- Team Selection -->
    <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-end">
      <div class="md:col-span-5 space-y-2">
        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">First Team</label>
        <select 
          v-model="team1"
          class="w-full px-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-brand-primary/20 focus:border-brand-primary outline-none transition-all text-slate-800 font-medium shadow-sm"
        >
          <option value="">Select Team...</option>
          <optgroup label="Active Teams">
            <option v-for="team in activeTeams" :key="team.name" :value="team.name">
              {{ getTeamLabel(team) }}
            </option>
          </optgroup>
          <optgroup label="Defunct Teams">
            <option v-for="team in defunctTeams" :key="team.name" :value="team.name">
              {{ team.name }} (defunct)
            </option>
          </optgroup>
        </select>
      </div>
      
      <div class="md:col-span-2 flex justify-center pb-2">
        <div class="w-10 h-10 rounded-full bg-slate-100 flex items-center justify-center text-slate-400 font-bold text-xs border border-slate-200">VS</div>
      </div>

      <div class="md:col-span-5 space-y-2">
        <label class="block text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Second Team</label>
        <select 
          v-model="team2"
          class="w-full px-4 py-3 bg-white border border-slate-200 rounded-xl focus:ring-2 focus:ring-brand-primary/20 focus:border-brand-primary outline-none transition-all text-slate-800 font-medium shadow-sm"
        >
          <option value="">Select Team...</option>
          <optgroup label="Active Teams">
            <option v-for="team in activeTeams" :key="team.name" :value="team.name">
              {{ getTeamLabel(team) }}
            </option>
          </optgroup>
          <optgroup label="Defunct Teams">
            <option v-for="team in defunctTeams" :key="team.name" :value="team.name">
              {{ team.name }} (defunct)
            </option>
          </optgroup>
        </select>
      </div>
    </div>

    <div class="flex justify-center">
      <button 
        @click="loadH2H" 
        :disabled="!team1 || !team2"
        class="px-8 py-3 bg-brand-primary text-white font-bold rounded-xl shadow-lg shadow-brand-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 disabled:grayscale disabled:hover:scale-100"
      >
        Compare Performance
      </button>
    </div>

    <!-- H2H Stats Cards -->
    <div v-if="h2hStats.total_matches > 0" class="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm text-center">
          <p class="text-slate-400 font-bold text-[10px] uppercase tracking-widest mb-2">Total Face-offs</p>
          <p class="text-5xl font-black text-slate-900">{{ h2hStats.total_matches }}</p>
        </div>
        
        <div class="bg-white p-6 rounded-2xl border-l-4 border-l-brand-primary border border-slate-100 shadow-sm text-center">
          <p class="text-brand-primary font-bold text-[10px] uppercase tracking-widest mb-1 line-clamp-1">{{ team1 }}</p>
          <p class="text-slate-400 text-[10px] font-medium uppercase mb-2">Victories</p>
          <p class="text-5xl font-black text-slate-900">{{ h2hStats.team1_wins }}</p>
        </div>
        
        <div class="bg-white p-6 rounded-2xl border-l-4 border-l-brand-accent border border-slate-100 shadow-sm text-center">
          <p class="text-brand-accent font-bold text-[10px] uppercase tracking-widest mb-1 line-clamp-1">{{ team2 }}</p>
          <p class="text-slate-400 text-[10px] font-medium uppercase mb-2">Victories</p>
          <p class="text-5xl font-black text-slate-900">{{ h2hStats.team2_wins }}</p>
        </div>
      </div>

      <!-- Recent Confrontations Table -->
      <div v-if="matches.length > 0" class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
        <div class="px-6 py-4 border-b border-slate-50 bg-slate-50/50">
          <h2 class="text-sm font-bold text-slate-800 uppercase tracking-wider">Recent Confrontations</h2>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="bg-slate-50/50 text-[10px] font-bold text-slate-400 uppercase tracking-widest">
                <th class="px-6 py-4">Date</th>
                <th class="px-6 py-4">Season</th>
                <th class="px-6 py-4">Winner</th>
                <th class="px-6 py-4">Venue</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="match in matches" :key="match.date" class="hover:bg-slate-50/50 transition-colors">
                <td class="px-6 py-4 text-sm text-slate-500 font-medium">{{ formatDate(match.date) }}</td>
                <td class="px-6 py-4">
                  <span class="px-2 py-1 bg-slate-100 text-slate-600 text-[10px] font-bold rounded uppercase">{{ match.season }}</span>
                </td>
                <td class="px-6 py-4">
                  <span 
                    :class="[
                      'text-sm font-bold',
                      match.winner === team1 ? 'text-brand-primary' : 'text-brand-accent'
                    ]"
                  >
                    {{ match.winner }}
                  </span>
                </td>
                <td class="px-6 py-4 text-sm text-slate-400 truncate max-w-xs" :title="match.venue">{{ match.venue }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const config = useRuntimeConfig()
const team1 = ref('')
const team2 = ref('')
const allTeamsInfo = ref<any[]>([])
const h2hStats = ref<any>({ total_matches: 0, team1_wins: 0, team2_wins: 0 })
const matches = ref<any[]>([])

const activeTeams = computed(() => allTeamsInfo.value.filter(t => t.is_active))
const defunctTeams = computed(() => allTeamsInfo.value.filter(t => !t.is_active))

const formatDate = (date: string) => {
  return new Date(date).toLocaleDateString('en-IN', {
    day: 'numeric',
    month: 'short',
    year: 'numeric'
  })
}

const loadTeams = async () => {
  try {
    const response = await $fetch(`${config.public.apiBase}/api/teams`)
    // response is an array of objects: {name, is_active, raw_names}
    allTeamsInfo.value = Array.isArray(response) ? response : []
  } catch (error) {
    console.error('Error loading teams:', error)
  }
}

const getTeamLabel = (team: any) => {
  let label = team.name
  
  // For active teams, show rebrand history
  if (team.is_active) {
    const olderNames = team.raw_names.filter((n: string) => n !== team.name)
    if (olderNames.length > 0) {
      label += ` (earlier known as ${olderNames.join(', ')})`
    }
  }
  
  return label
}

onMounted(() => {
  loadTeams()
})

const loadH2H = async () => {
  if (!team1.value || !team2.value) return
  
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
  }
}
</script>
