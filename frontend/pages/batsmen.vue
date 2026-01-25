<template>
  <div class="container mx-auto px-4 py-8">
    <div class="space-y-8 pb-4">
    <!-- Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-ipl-blue/15 text-ipl-blue rounded-full text-xs font-bold uppercase tracking-widest border border-ipl-blue/20">
          <CricketBatIcon class="w-3 h-3" />
          Batting Intelligence
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">The <span class="bg-gradient-to-r from-ipl-blue to-purple-600 bg-clip-text text-transparent">Elite Batsmen</span></h1>
        <p class="text-slate-500 max-w-xl">
          Meet the run-machine legends who've dominated IPL pitches. From explosive strike rates to consistent performances, these are the batsmen who redefined T20 cricket.
        </p>
      </div>
    </div>
    
    <div class="bg-gradient-to-br from-white via-ipl-blue/8 to-purple-50 rounded-3xl border border-ipl-blue/15 shadow-xl overflow-hidden relative">
      <!-- Decorative Elements -->
      <div class="absolute top-0 right-0 w-24 h-24 bg-gradient-to-br from-ipl-blue/25 to-purple-400/25 rounded-full -mr-12 -mt-12 animate-pulse-slow"></div>
      
      <div class="px-6 py-4 border-b border-ipl-blue/15 bg-gradient-to-r from-ipl-blue/8 to-purple-100 flex items-center justify-between relative z-10">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-ipl-blue/15 rounded-xl border border-ipl-blue/20">
            <CricketBatIcon class="w-4 h-4 text-ipl-blue" />
          </div>
          <h2 class="text-sm font-bold text-ipl-blue uppercase tracking-widest">🏏 Top Run Scorers (All Time)</h2>
        </div>
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span class="text-xs font-bold text-slate-600 uppercase bg-white px-3 py-1 rounded-full border border-slate-200 shadow-sm">Updated Final 2025</span>
        </div>
      </div>
      <div class="mobile-table-container">
        <table class="w-full text-left min-w-[600px]">
          <thead>
            <tr class="bg-gradient-to-r from-ipl-blue/8 to-purple-100 text-xs font-black text-slate-700 uppercase tracking-widest border-b border-ipl-blue/20">
              <th class="px-3 sm:px-6 py-4 text-ipl-blue">Rank</th>
              <th class="px-3 sm:px-6 py-4 min-w-[140px] text-purple-700">Player Profile</th>
              <th class="px-3 sm:px-6 py-4 text-center min-w-[80px] text-slate-600">Innings</th>
              <th class="px-3 sm:px-6 py-4 text-center min-w-[100px] text-green-700">Strike Rate</th>
              <th class="px-3 sm:px-6 py-4 text-right min-w-[100px] text-ipl-blue">Total Runs</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-slate-50">
            <tr v-for="(player, idx) in batsmen" :key="idx" class="hover:bg-gradient-to-r hover:from-ipl-blue/8 hover:to-purple-50 transition-all duration-200 group border-b border-slate-100/50">
              <td class="px-3 sm:px-6 py-3 sm:py-4">
                <div class="flex items-center justify-center">
                  <span :class="[
                    'w-8 h-8 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center text-xs font-black border-2 shadow-md transition-transform group-hover:scale-110',
                    idx === 0 ? 'bg-gradient-to-br from-yellow-400 to-yellow-500 border-yellow-600 text-white shadow-yellow-200' : 
                    idx === 1 ? 'bg-gradient-to-br from-slate-300 to-slate-400 border-slate-500 text-white shadow-slate-200' :
                    idx === 2 ? 'bg-gradient-to-br from-orange-400 to-orange-500 border-orange-600 text-white shadow-orange-200' :
                    'bg-gradient-to-br from-white to-slate-50 border-slate-200 text-slate-600 shadow-slate-100'
                  ]">
                    {{ (idx as number) + 1 }}
                  </span>
                </div>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4">
                <NuxtLink 
                  :to="`/player-search?name=${encodeURIComponent(player.name)}`" 
                  class="inline-flex items-center gap-2 text-sm font-bold text-ipl-blue hover:text-purple-600 transition-colors group/link"
                >
                  <div class="w-2 h-2 bg-ipl-blue rounded-full group-hover/link:bg-purple-600 transition-colors"></div>
                  <span class="whitespace-nowrap">{{ player.name }}</span>
                </NuxtLink>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4 text-center">
                <span class="px-3 py-1.5 bg-blue-50 text-blue-700 text-sm font-bold rounded-xl border border-blue-200">{{ player.matches }}</span>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4 text-center">
                <span class="px-3 py-1.5 bg-gradient-to-r from-green-100 to-emerald-100 text-green-800 text-sm font-black rounded-xl border border-green-200 shadow-sm whitespace-nowrap">
                  ⚡ {{ player.strike_rate }} SR
                </span>
              </td>
              <td class="px-3 sm:px-6 py-3 sm:py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <span class="text-xl sm:text-2xl font-black bg-gradient-to-r from-ipl-blue to-purple-600 bg-clip-text text-transparent whitespace-nowrap">{{ player.runs }}</span>
                  <div class="w-1.5 h-6 bg-gradient-to-b from-ipl-blue to-purple-600 rounded-full"></div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="flex justify-center">
      <NuxtLink 
        to="/player-search"
        class="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-ipl-blue to-purple-600 hover:from-purple-600 hover:to-ipl-blue text-white rounded-2xl font-bold hover:scale-[1.02] active:scale-[0.98] transition-all duration-300 shadow-xl shadow-ipl-blue/25 group border border-ipl-blue/20"
      >
        <MagnifyingGlassIcon class="w-5 h-5 group-hover:rotate-12 transition-transform duration-300" />
        <span>🔍 Search All Players</span>
        <div class="w-2 h-2 bg-white/30 rounded-full group-hover:scale-150 transition-transform"></div>
      </NuxtLink>
    </div>
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
