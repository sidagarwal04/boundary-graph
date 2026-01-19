<template>
  <div v-if="match" class="space-y-8 animate-in fade-in slide-in-from-bottom-2 duration-700 pb-12">
    <!-- Match Header -->
    <div class="bg-slate-900 rounded-3xl p-8 text-white relative overflow-hidden shadow-2xl">
      <div class="absolute top-0 right-0 p-8 opacity-10">
        <CricketStadiumIcon class="w-32 h-32" />
      </div>
      
      <div class="relative z-10 flex flex-col md:flex-row justify-between items-center gap-8">
        <div class="text-center md:text-left flex-1">
          <p class="text-[10px] font-black uppercase tracking-[0.2em] text-brand-primary mb-2">{{ match.date }} • {{ match.venue }}</p>
          <div class="flex items-center justify-center md:justify-start gap-4">
             <h1 class="text-2xl md:text-3xl font-black tracking-tighter">{{ match.team1 }}</h1>
             <span class="text-slate-500 font-bold">vs</span>
             <h1 class="text-2xl md:text-3xl font-black tracking-tighter">{{ match.team2 }}</h1>
          </div>
          <div class="mt-6 inline-flex items-center gap-3 px-4 py-2 bg-white/10 rounded-full border border-white/10">
            <TrophyIcon class="w-4 h-4 text-brand-primary" />
            <span class="text-sm font-bold">{{ match.winner }} won by {{ match.margin }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <!-- Manhattan Chart (Runs per Over) -->
      <div class="stat-card p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-black text-slate-800 uppercase tracking-widest text-xs">Manhattan Chart</h3>
          <span class="text-[10px] font-bold text-slate-400 uppercase">Runs per Over</span>
        </div>
        <div class="h-[300px]">
          <canvas ref="manhattanChartRef"></canvas>
        </div>
      </div>

      <!-- Worm Chart (Cumulative Runs) -->
      <div class="stat-card p-6">
        <div class="flex items-center justify-between mb-6">
          <h3 class="font-black text-slate-800 uppercase tracking-widest text-xs">The Worm</h3>
          <span class="text-[10px] font-bold text-slate-400 uppercase">Cumulative Progress</span>
        </div>
        <div class="h-[300px]">
          <canvas ref="wormChartRef"></canvas>
        </div>
      </div>
    </div>

    <!-- Match Summary Stats -->
    <div class="stat-card overflow-hidden">
       <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50">
          <h3 class="font-black text-slate-800 uppercase tracking-widest text-xs">Over-by-Over Breakdown</h3>
       </div>
       <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="text-[10px] font-black uppercase tracking-widest text-slate-400">
                <th class="px-6 py-4">Over</th>
                <th class="px-6 py-4">{{ match.team1 }}</th>
                <th class="px-6 py-4">{{ match.team2 }}</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-50">
              <tr v-for="i in 20" :key="i" class="hover:bg-slate-50/50 transition-colors">
                <td class="px-6 py-3 font-bold text-slate-400">Over {{ i }}</td>
                <td class="px-6 py-3 font-black text-slate-800">{{ match.innings1[i-1]?.runs }} runs <span v-if="match.innings1[i-1]?.wickets" class="ml-2 text-rose-500 text-[10px]">W</span></td>
                <td class="px-6 py-3 font-black text-slate-800">{{ match.innings2[i-1]?.runs }} runs <span v-if="match.innings2[i-1]?.wickets" class="ml-2 text-rose-500 text-[10px]">W</span></td>
              </tr>
            </tbody>
          </table>
       </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { TrophyIcon } from '@heroicons/vue/24/solid'
import CricketStadiumIcon from '~/components/icons/CricketStadiumIcon.vue'
import Chart from 'chart.js/auto'

const route = useRoute()
const config = useRuntimeConfig()
const match = ref<any>(null)
const manhattanChartRef = ref<HTMLCanvasElement | null>(null)
const wormChartRef = ref<HTMLCanvasElement | null>(null)

let manhattanChart: any = null
let wormChart: any = null

const fetchMatch = async () => {
  try {
    const data = await $fetch(`${config.public.apiBase}/api/match/${route.params.id}`)
    match.value = data
    nextTick(() => {
      initCharts()
    })
  } catch (e) {
    console.error("Match fetch failed", e)
  }
}

const initCharts = () => {
  if (!match.value || !manhattanChartRef.value || !wormChartRef.value) return

  const labels = match.value.innings1.map((o: any) => `Over ${o.over + 1}`)

  // Manhattan Chart
  manhattanChart = new Chart(manhattanChartRef.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        {
          label: match.value.team1,
          data: match.value.innings1.map((o: any) => o.runs),
          backgroundColor: '#6366f1',
          borderRadius: 4
        },
        {
          label: match.value.team2,
          data: match.value.innings2.map((o: any) => o.runs),
          backgroundColor: '#FBBF24',
          borderRadius: 4
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { display: false } },
        x: { grid: { display: false } }
      }
    }
  })

  // Worm Chart
  wormChart = new Chart(wormChartRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: match.value.team1,
          data: match.value.innings1.map((o: any) => o.cumulative_runs),
          borderColor: '#6366f1',
          borderWidth: 3,
          tension: 0.3,
          pointRadius: 0
        },
        {
          label: match.value.team2,
          data: match.value.innings2.map((o: any) => o.cumulative_runs),
          borderColor: '#FBBF24',
          borderWidth: 3,
          tension: 0.3,
          pointRadius: 0
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: true, grid: { color: '#f1f5f9' } },
        x: { grid: { display: false } }
      }
    }
  })
}

onMounted(fetchMatch)

useHead({
  title: 'Match Storyline | Boundary Graph'
})
</script>
