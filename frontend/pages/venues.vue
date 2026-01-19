<template>
  <div class="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-700">
    <!-- Header Area -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-brand-primary/10 text-brand-primary rounded-full text-xs font-bold uppercase tracking-widest">
          <MapPinIcon class="w-3 h-3" />
          Venue Intelligence
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">The <span class="text-brand-primary">Home Grounds</span></h1>
        <p class="text-slate-500 max-w-xl">
          Analyze pitch behavior across India's iconic stadiums. Discover where the coin toss matters most and where the boundaries flow.
        </p>
      </div>
      
      <div class="flex gap-4">
        <div class="stat-card py-2 px-4 flex items-center gap-3">
          <div class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
          <span class="text-xs font-bold text-slate-600 uppercase tracking-tighter">{{ venues.length }} Primary Venues Indexing</span>
        </div>
      </div>
    </div>

    <!-- Venues Table -->
    <div class="stat-card overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full text-left">
          <thead>
            <tr class="bg-slate-50/50 border-b border-slate-100">
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-slate-400">Venue Name</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-slate-400 text-center">Matches</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-slate-400 text-center">Avg 1st Innings</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-slate-400 text-center">Defend %</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-slate-400 text-center">Chase %</th>
              <th class="px-6 py-4 text-[10px] font-black uppercase tracking-widest text-slate-400 text-right">Action</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="venue in venues" :key="venue.name" class="hover:bg-slate-50/50 transition-colors group">
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 bg-slate-100 rounded-xl flex items-center justify-center text-slate-400 group-hover:bg-brand-primary group-hover:text-white transition-colors">
                    <BuildingLibraryIcon class="w-5 h-5" />
                  </div>
                  <div>
                    <p class="font-bold text-slate-900 leading-none mb-1">{{ venue.name }}</p>
                    <p class="text-xs text-slate-400 font-medium">Premier League Venue</p>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-lg text-xs font-bold tracking-tight">
                  {{ venue.total_matches }}
                </span>
              </td>
              <td class="px-6 py-4 text-center">
                <span class="text-sm font-bold text-slate-700">{{ venue.avg_first_innings }}</span>
              </td>
              <td class="px-6 py-4 text-center">
                <div class="flex flex-col items-center gap-1">
                  <span class="text-sm font-bold text-slate-700">{{ venue.bat_first_win_pct }}%</span>
                  <div class="w-12 h-1 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-blue-500 rounded-full" :style="{ width: venue.bat_first_win_pct + '%' }"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-center">
                <div class="flex flex-col items-center gap-1">
                  <span class="text-sm font-bold text-slate-700">{{ venue.chase_win_pct }}%</span>
                  <div class="w-12 h-1 bg-slate-100 rounded-full overflow-hidden">
                    <div class="h-full bg-green-500 rounded-full" :style="{ width: venue.chase_win_pct + '%' }"></div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 text-right">
                <button 
                  @click="showVenueDetails(venue)"
                  class="px-3 py-1.5 bg-slate-900 text-white rounded-lg text-[10px] font-bold uppercase tracking-widest hover:bg-brand-primary transition-colors"
                >
                  View Intelligence
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Venue Details Modal -->
    <Teleport to="body">
      <div v-if="selectedVenue" class="fixed inset-0 z-[9999] flex items-start justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-300" @click.self="closeModal">
        <div class="bg-white rounded-3xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden animate-in zoom-in-95 duration-300 mt-8">
        <!-- Header -->
        <div class="bg-white px-6 py-4 border-b border-slate-200 flex justify-between items-center sticky top-0 z-10">
          <div>
            <h3 class="text-xl font-bold text-slate-900">{{ selectedVenue.name }}</h3>
            <p class="text-sm text-slate-500">Venue Intelligence Report</p>
          </div>
          <button @click="closeModal" class="text-slate-400 hover:text-slate-600 p-2">
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
            </svg>
          </button>
        </div>

        <!-- Content -->
        <div class="p-6 space-y-6 overflow-y-auto max-h-[calc(90vh-80px)]">
          <!-- Venue Personality Card -->
          <div class="bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50 p-6 rounded-2xl border border-purple-100">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                <span class="text-white text-xl">🏟️</span>
              </div>
              <div>
                <h4 class="text-lg font-bold text-slate-900">Venue Personality</h4>
                <p class="text-xs text-purple-600 font-medium">AI-Generated Insights</p>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="space-y-2">
                <p class="text-xs text-purple-600 font-bold uppercase tracking-widest">Batting Paradise Score</p>
                <div class="flex items-center gap-2">
                  <div class="flex-1 h-2 bg-purple-100 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-purple-400 to-pink-500 rounded-full transition-all duration-1000" 
                         :style="{ width: Math.min(100, (selectedVenue.avg_first_innings / 200) * 100) + '%' }"></div>
                  </div>
                  <span class="text-sm font-bold text-purple-700">{{ Math.round((selectedVenue.avg_first_innings / 200) * 100) }}/100</span>
                </div>
              </div>
              <div class="space-y-2">
                <p class="text-xs text-indigo-600 font-bold uppercase tracking-widest">Thriller Factor</p>
                <div class="flex items-center gap-2">
                  <div class="flex-1 h-2 bg-indigo-100 rounded-full overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-indigo-400 to-blue-500 rounded-full transition-all duration-1000" 
                         :style="{ width: Math.abs(50 - Math.abs(selectedVenue.chase_win_pct - selectedVenue.bat_first_win_pct)) + 50 + '%' }"></div>
                  </div>
                  <span class="text-sm font-bold text-indigo-700">{{ Math.round(Math.abs(50 - Math.abs(selectedVenue.chase_win_pct - selectedVenue.bat_first_win_pct)) + 50) }}/100</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Venue Superpowers -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="bg-gradient-to-br from-yellow-50 to-orange-100 p-4 rounded-xl border border-yellow-200">
              <div class="text-center">
                <div class="text-2xl mb-2">⚡</div>
                <p class="text-xs text-orange-600 font-bold uppercase tracking-widest mb-1">Power Hitting</p>
                <p class="text-xl font-black text-orange-800">{{ selectedVenue.avg_first_innings > 180 ? 'EXTREME' : selectedVenue.avg_first_innings > 160 ? 'HIGH' : selectedVenue.avg_first_innings > 140 ? 'MEDIUM' : 'LOW' }}</p>
              </div>
            </div>
            
            <div class="bg-gradient-to-br from-green-50 to-emerald-100 p-4 rounded-xl border border-green-200">
              <div class="text-center">
                <div class="text-2xl mb-2">🎯</div>
                <p class="text-xs text-green-600 font-bold uppercase tracking-widest mb-1">Chase Mastery</p>
                <p class="text-xl font-black text-green-800">{{ selectedVenue.chase_win_pct > 60 ? 'LEGENDARY' : selectedVenue.chase_win_pct > 50 ? 'STRONG' : selectedVenue.chase_win_pct > 40 ? 'BALANCED' : 'TOUGH' }}</p>
              </div>
            </div>
            
            <div class="bg-gradient-to-br from-blue-50 to-cyan-100 p-4 rounded-xl border border-blue-200">
              <div class="text-center">
                <div class="text-2xl mb-2">🛡️</div>
                <p class="text-xs text-blue-600 font-bold uppercase tracking-widest mb-1">Defend Mode</p>
                <p class="text-xl font-black text-blue-800">{{ selectedVenue.bat_first_win_pct > 60 ? 'FORTRESS' : selectedVenue.bat_first_win_pct > 50 ? 'SOLID' : selectedVenue.bat_first_win_pct > 40 ? 'FAIR' : 'RISKY' }}</p>
              </div>
            </div>
          </div>

          <!-- Crazy Predictions -->
          <div class="bg-gradient-to-r from-slate-900 via-purple-900 to-slate-900 p-6 rounded-2xl text-white">
            <div class="flex items-center gap-3 mb-4">
              <div class="w-8 h-8 bg-purple-500 rounded-lg flex items-center justify-center">
                <span class="text-lg">🔮</span>
              </div>
              <h4 class="text-lg font-bold text-white">AI Venue Oracle</h4>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div class="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20">
                <p class="text-xs text-white font-bold uppercase tracking-widest mb-2">Next Match Prediction</p>
                <p class="text-sm leading-relaxed text-white">
                  <span v-if="selectedVenue.chase_win_pct > 45 && selectedVenue.chase_win_pct > selectedVenue.bat_first_win_pct + 10">
                    🎯 <strong>CHASE MASTERS!</strong> {{ selectedVenue.chase_win_pct }}% chase success rate means captains should bowl first and hunt!
                  </span>
                  <span v-else-if="selectedVenue.bat_first_win_pct > 45 && selectedVenue.bat_first_win_pct > selectedVenue.chase_win_pct + 10">
                    🛡️ <strong>FORTRESS MODE!</strong> {{ selectedVenue.bat_first_win_pct }}% defend rate - always bat first and build pressure!
                  </span>
                  <span v-else-if="selectedVenue.chase_win_pct > 35 && selectedVenue.avg_first_innings > 165">
                    ⚡ <strong>SHOOTOUT ZONE!</strong> High scores ({{ selectedVenue.avg_first_innings }}) + decent chasing ({{ selectedVenue.chase_win_pct }}%) = fireworks expected!
                  </span>
                  <span v-else-if="selectedVenue.bat_first_win_pct < 25 && selectedVenue.chase_win_pct < 35">
                    🎲 <strong>CHAOS CRICKET!</strong> Neither strategy works well here - expect wild, unpredictable matches!
                  </span>
                  <span v-else-if="Math.abs(selectedVenue.chase_win_pct - selectedVenue.bat_first_win_pct) < 8">
                    ⚖️ <strong>TOSS IRRELEVANT!</strong> {{ selectedVenue.chase_win_pct }}% vs {{ selectedVenue.bat_first_win_pct }}% - pure skill will decide!
                  </span>
                  <span v-else>
                    🤔 <strong>TACTICAL PUZZLE!</strong> {{ selectedVenue.chase_win_pct }}% chase rate suggests careful planning required.
                  </span>
                </p>
              </div>
              
              <div class="bg-white/10 p-4 rounded-xl backdrop-blur-sm border border-white/20">
                <p class="text-xs text-white font-bold uppercase tracking-widest mb-2">Strategic Wisdom</p>
                <p class="text-sm leading-relaxed text-white">
                  <span v-if="selectedVenue.avg_first_innings > 168 && selectedVenue.chase_win_pct > 40">
                    🚀 <strong>RUN FEST GUARANTEED!</strong> {{ selectedVenue.avg_first_innings }} avg + {{ selectedVenue.chase_win_pct }}% chases = boundaries galore!
                  </span>
                  <span v-else-if="selectedVenue.avg_first_innings < 150 && selectedVenue.bat_first_win_pct > 35">
                    🏏 <strong>GRIND IT OUT!</strong> Low scores ({{ selectedVenue.avg_first_innings }}) favor patient batting and clever bowling.
                  </span>
                  <span v-else-if="selectedVenue.avg_first_innings > 165 && selectedVenue.chase_win_pct < 30">
                    😱 <strong>PRESSURE COOKER!</strong> High scores ({{ selectedVenue.avg_first_innings }}) but tough chasing - mental game crucial!
                  </span>
                  <span v-else-if="selectedVenue.total_matches > 60 && Math.abs(selectedVenue.chase_win_pct - selectedVenue.bat_first_win_pct) < 5">
                    🎯 <strong>PURE CRICKET THEATER!</strong> {{ selectedVenue.total_matches }} matches prove this venue tests every skill equally!
                  </span>
                  <span v-else-if="selectedVenue.avg_first_innings > 155 && selectedVenue.avg_first_innings < 165">
                    ⚖️ <strong>GOLDILOCKS GROUND!</strong> Not too high, not too low - {{ selectedVenue.avg_first_innings }} is just right for T20!
                  </span>
                  <span v-else-if="selectedVenue.chase_win_pct < 25">
                    🛡️ <strong>DEFEND OR DIE!</strong> Only {{ selectedVenue.chase_win_pct }}% chases succeed - set big totals early!
                  </span>
                  <span v-else>
                    🎪 <strong>WILDCARD VENUE!</strong> This ground writes its own rules - expect the unexpected every time!
                  </span>
                </p>
              </div>
            </div>
          </div>

          <!-- Venue vs League Comparison -->
          <div class="bg-white border border-slate-200 rounded-2xl p-6">
            <h4 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
              <span class="text-lg">📊</span> How This Venue Stacks Up
            </h4>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div class="text-center">
                <div class="relative w-16 h-16 mx-auto mb-2">
                  <svg class="w-16 h-16 transform -rotate-90" viewBox="0 0 36 36">
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                          fill="none" stroke="#e5e7eb" stroke-width="3"/>
                    <path d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" 
                          fill="none" stroke="#3b82f6" stroke-width="3" 
                          :stroke-dasharray="`${(selectedVenue.avg_first_innings / 200) * 100}, 100`"/>
                  </svg>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <span class="text-xs font-bold text-blue-600">{{ Math.round((selectedVenue.avg_first_innings / 200) * 100) }}%</span>
                  </div>
                </div>
                <p class="text-xs text-slate-500 font-medium">vs League Avg</p>
              </div>
              
              <div class="text-center">
                <p class="text-2xl font-black text-slate-900 mb-1">{{ selectedVenue.total_matches }}</p>
                <p class="text-xs text-slate-500 font-medium">Epic Battles</p>
              </div>
              
              <div class="text-center">
                <p class="text-2xl font-black text-emerald-600 mb-1">{{ selectedVenue.chase_win_pct }}%</p>
                <p class="text-xs text-slate-500 font-medium">Chase Success</p>
              </div>
              
              <div class="text-center">
                <p class="text-2xl font-black text-purple-600 mb-1">{{ selectedVenue.bat_first_win_pct }}%</p>
                <p class="text-xs text-slate-500 font-medium">Defend Success</p>
              </div>
            </div>
          </div>

          <!-- Fun Venue Facts -->
          <div class="bg-gradient-to-r from-amber-50 to-yellow-100 p-6 rounded-2xl border border-amber-200">
            <h4 class="text-lg font-bold text-amber-900 mb-4 flex items-center gap-2">
              <span class="text-lg">🎪</span> Venue Secrets & Fun Facts
            </h4>
            <div class="space-y-3">
              <div class="flex items-start gap-3">
                <span class="text-lg flex-shrink-0">🏆</span>
                <p class="text-sm text-amber-800 leading-relaxed">
                  <strong>Stadium Superpower:</strong> 
                  <span v-if="selectedVenue.chase_win_pct > 50 && selectedVenue.avg_first_innings > 165">
                    CHASE MASTER'S HEAVEN! High scores ({{ selectedVenue.avg_first_innings }}) + {{ selectedVenue.chase_win_pct }}% chase success = second innings magic!
                  </span>
                  <span v-else-if="selectedVenue.bat_first_win_pct > 40 && selectedVenue.avg_first_innings < 155">
                    BOWLER'S SANCTUARY! Low totals ({{ selectedVenue.avg_first_innings }}) + {{ selectedVenue.bat_first_win_pct }}% defend rate = spin twins' paradise!
                  </span>
                  <span v-else-if="selectedVenue.total_matches > 70">
                    LEGENDARY COLOSSEUM! {{ selectedVenue.total_matches }} epic battles have made this hallowed ground of cricket history!
                  </span>
                  <span v-else-if="selectedVenue.chase_win_pct < 25">
                    PRESSURE FORTRESS! Only {{ selectedVenue.chase_win_pct }}% chases succeed - where dreams come to die!
                  </span>
                  <span v-else-if="Math.abs(selectedVenue.chase_win_pct - selectedVenue.bat_first_win_pct) < 5">
                    PURE SKILL ARENA! {{ selectedVenue.chase_win_pct }}% vs {{ selectedVenue.bat_first_win_pct }}% - toss is meaningless, talent decides!
                  </span>
                  <span v-else>
                    MYSTERY GROUND! This venue has its own personality that defies conventional cricket wisdom!
                  </span>
                </p>
              </div>
              
              <div class="flex items-start gap-3">
                <span class="text-lg flex-shrink-0">⚡</span>
                <p class="text-sm text-amber-800 leading-relaxed">
                  <strong>Batting Mood:</strong> 
                  <span v-if="selectedVenue.avg_first_innings > 168">
                    FIREWORKS GUARANTEED! {{ selectedVenue.avg_first_innings }} average means sixes rain like monsoon!
                  </span>
                  <span v-else-if="selectedVenue.avg_first_innings < 145">
                    GRIND FEST! {{ selectedVenue.avg_first_innings }} average - every boundary is earned through blood and sweat!
                  </span>
                  <span v-else-if="selectedVenue.avg_first_innings > 155 && selectedVenue.avg_first_innings < 165">
                    TEXTBOOK T20! {{ selectedVenue.avg_first_innings }} average is cricket perfection - not too easy, not too tough!
                  </span>
                  <span v-else-if="selectedVenue.chase_win_pct < 30 && selectedVenue.avg_first_innings > 160">
                    SCOREBOARD PRESSURE! High totals ({{ selectedVenue.avg_first_innings }}) but tough chasing creates mind games!
                  </span>
                  <span v-else>
                    WILDCARD WICKET! This pitch writes its own rules - expect anything from 120 to 200!
                  </span>
                </p>
              </div>
              
              <div class="flex items-start gap-3">
                <span class="text-lg flex-shrink-0">🎯</span>
                <p class="text-sm text-amber-800 leading-relaxed">
                  <strong>Captain&apos;s Dilemma:</strong> 
                  <span v-if="selectedVenue.chase_win_pct > selectedVenue.bat_first_win_pct + 15">
                    BOWL FIRST OR GO HOME! {{ selectedVenue.chase_win_pct }}% vs {{ selectedVenue.bat_first_win_pct }}% - chasing is the only way!
                  </span>
                  <span v-else-if="selectedVenue.bat_first_win_pct > selectedVenue.chase_win_pct + 15">
                    BAT FIRST AND DOMINATE! {{ selectedVenue.bat_first_win_pct }}% vs {{ selectedVenue.chase_win_pct }}% - set the target, win the game!
                  </span>
                  <span v-else-if="selectedVenue.chase_win_pct < 25 && selectedVenue.bat_first_win_pct < 25">
                    TOSS IS CURSED! Neither strategy works - coin flip decides your doom!
                  </span>
                  <span v-else-if="selectedVenue.total_matches < 20">
                    UNCHARTED TERRITORY! Too few matches to predict - pure gamble awaits!
                  </span>
                  <span v-else-if="Math.abs(selectedVenue.chase_win_pct - selectedVenue.bat_first_win_pct) < 8">
                    FLIP A COIN! {{ selectedVenue.chase_win_pct }}% vs {{ selectedVenue.bat_first_win_pct }}% - even the stats are confused!
                  </span>
                  <span v-else>
                    TRUST YOUR INSTINCT! Numbers suggest {{ selectedVenue.chase_win_pct > selectedVenue.bat_first_win_pct ? 'chasing' : 'defending' }} but gut feeling matters here!
                  </span>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, Teleport } from 'vue'
import { MapPinIcon, BuildingLibraryIcon } from '@heroicons/vue/24/outline'
import { useHead } from 'nuxt/app'

const config = useRuntimeConfig()
const venues = ref<any[]>([])
const selectedVenue = ref<any>(null)

const showVenueDetails = (venue: any) => {
  selectedVenue.value = venue
}

const closeModal = () => {
  selectedVenue.value = null
}

const fetchVenues = async () => {
  try {
    const data = await $fetch(`${config.public.apiBase}/api/venues`)
    venues.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error("Failed to fetch venues", e)
  }
}

onMounted(() => {
  fetchVenues()
})

useHead({
  title: 'Venue Intelligence | Boundary Graph'
})
</script>
