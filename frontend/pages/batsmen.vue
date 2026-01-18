<template>
  <div>
    <h1 class="text-3xl font-bold mb-8">🏏 Top Batsmen</h1>
    
    <div class="stat-card">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-slate-100">
            <tr>
              <th class="px-4 py-3 text-left text-sm font-semibold">Rank</th>
              <th class="px-4 py-3 text-left text-sm font-semibold">Player</th>
              <th class="px-4 py-3 text-center text-sm font-semibold">Runs</th>
              <th class="px-4 py-3 text-center text-sm font-semibold">Matches</th>
              <th class="px-4 py-3 text-center text-sm font-semibold">Strike Rate</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(player, idx) in batsmen" :key="idx" class="border-b hover:bg-slate-50 transition">
              <td class="px-4 py-3 text-sm font-medium text-blue-600">{{ (idx as number) + 1 }}</td>
              <td class="px-4 py-3 text-sm font-medium text-slate-900">
                <NuxtLink :to="`/player-search?name=${encodeURIComponent(player.name)}`" class="hover:text-blue-600">
                  {{ player.name }}
                </NuxtLink>
              </td>
              <td class="px-4 py-3 text-sm text-center font-semibold text-green-600">{{ player.runs }}</td>
              <td class="px-4 py-3 text-sm text-center">{{ player.matches }}</td>
              <td class="px-4 py-3 text-sm text-center">
                <span class="badge">{{ player.strike_rate }}%</span>
              </td>
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
const batsmen = ref<any[]>([])

onMounted(async () => {
  try {
    batsmen.value = await $fetch(`${config.public.apiBase}/api/batsmen/top?limit=50`)
  } catch (error) {
    console.error('Failed to fetch batsmen:', error)
  }
})
</script>
