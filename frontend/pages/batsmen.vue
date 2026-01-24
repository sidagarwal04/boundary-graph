<template>
  <div class="space-y-8 pb-12">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-brand-primary/10 text-brand-primary rounded-full text-xs font-bold uppercase tracking-widest">
          <CricketBatIcon class="w-3 h-3" />
          Batting Intelligence
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">The <span class="text-brand-primary">Elite Batsmen</span></h1>
        <p class="text-slate-500 max-w-xl">
          Meet the run-machine legends who've dominated IPL pitches. From explosive strike rates to consistent performances, these are the batsmen who redefined T20 cricket.
        </p>
      </div>
    </div>
    
    <div class="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
      <div class="px-6 py-4 border-b border-slate-50 bg-slate-50/50 flex items-center justify-between">
        <h2 class="text-xs font-bold text-slate-400 uppercase tracking-widest">Top Run Scorers (All Time)</h2>
        <span class="text-[10px] font-bold text-slate-400 uppercase bg-white px-2 py-1 rounded border border-slate-100 shadow-sm">Updated Final 2025</span>
      </div>
      <div class="mobile-table-container">
        <table class="w-full text-left min-w-[600px]">
          <thead>
            <tr class="bg-slate-50/20 text-[10px] font-bold text-slate-400 uppercase tracking-widest border-b border-slate-50">
              <th class="px-3 sm:px-6 py-4">Rank</th>
              <th class="px-3 sm:px-6 py-4 min-w-[140px]">Player Profile</th>
              <th class="px-3 sm:px-6 py-4 text-center min-w-[80px]">Innings</th>
              <th class="px-3 sm:px-6 py-4 text-center min-w-[100px]">Strike Rate</th>
              <th class="px-3 sm:px-6 py-4 text-right min-w-[100px]">Total Runs</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="(player, idx) in batsmen" :key="idx" class="hover:bg-slate-50/50 transition-colors group">
              <td class="px-3 sm:px-6 py-3 sm:py-4">
                <span :class="[
                  'w-7 h-7 sm:w-8 sm:h-8 rounded-lg flex items-center justify-center text-xs font-black border',
                  idx === 0 ? 'bg-yellow-400 border-yellow-500 text-white' : 
                  idx === 1 ? 'bg-slate-300 border-slate-400 text-white' :
                  idx === 2 ? 'bg-orange-300 border-orange-400 text-white' :
                  'bg-white border-slate-100 text-slate-400'
                ]">
                  {{ (idx as number) + 1 }}
                </span>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4">
                <NuxtLink 
                  :to="`/player-search?name=${encodeURIComponent(player.name)}`" 
                  class="text-sm font-bold text-slate-900 hover:text-brand-primary transition-colors block whitespace-nowrap"
                >
                  {{ player.name }}
                </NuxtLink>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4 text-center text-sm font-semibold text-slate-600">{{ player.matches }}</td>
              <td class="px-3 sm:px-6 py-3 sm:py-4 text-center">
                <span class="px-2 py-1 bg-brand-primary/5 text-brand-primary text-[10px] font-black rounded uppercase tracking-tighter whitespace-nowrap">
                  {{ player.strike_rate }} SR
                </span>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4 text-right">
                <span class="text-lg sm:text-xl font-black text-slate-900 whitespace-nowrap">{{ player.runs }}</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="flex justify-center">
      <NuxtLink 
        to="/player-search"
        class="inline-flex items-center gap-2 px-8 py-4 bg-brand-primary text-white rounded-2xl font-bold hover:scale-[1.02] active:scale-[0.98] transition-all shadow-xl shadow-brand-primary/20 group"
      >
        <MagnifyingGlassIcon class="w-5 h-5 group-hover:rotate-12 transition-transform" />
        <span>Search all players</span>
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { MagnifyingGlassIcon } from '@heroicons/vue/24/outline'
import CricketBatIcon from '~/components/icons/CricketBatIcon.vue'

const config = useRuntimeConfig()
const batsmen = ref<any[]>([])

onMounted(async () => {
  try {
    batsmen.value = await $fetch(`${config.public.apiBase}/api/batsmen/top?limit=50`)
  } catch (error) {
    console.error('Failed to fetch batsmen:', error)
  }
})
</script>
