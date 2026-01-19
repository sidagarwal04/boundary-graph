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
                <button class="px-3 py-1.5 bg-slate-900 text-white rounded-lg text-[10px] font-bold uppercase tracking-widest hover:bg-brand-primary transition-colors">
                  View Intelligence
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { MapPinIcon, BuildingLibraryIcon } from '@heroicons/vue/24/outline'

const config = useRuntimeConfig()
const venues = ref<any[]>([])

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
