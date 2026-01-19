<template>
  <div class="relative bg-slate-900 rounded-3xl p-8 overflow-hidden h-[400px] flex items-center justify-center border border-slate-800 shadow-2xl">
    <!-- Grid Pattern -->
    <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(#6366f1 0.5px, transparent 0.5px); background-size: 24px 24px;"></div>
    
    <div v-if="loading" class="flex flex-col items-center gap-4 animate-pulse">
      <div class="w-12 h-12 rounded-full border-4 border-brand-primary border-t-transparent animate-spin"></div>
      <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Traversing Graph...</p>
    </div>

    <svg v-else viewBox="0 0 500 400" class="w-full h-full relative z-10 transition-opacity duration-1000" :class="{ 'opacity-100': !loading, 'opacity-0': loading }">
      <!-- Connection Lines -->
      <g v-for="(rival, index) in rivals" :key="'line-' + index">
        <line 
          :x1="centerX" :y1="centerY" 
          :x2="rival.x" :y2="rival.y" 
          stroke="url(#lineGradient)" 
          stroke-width="1.5"
          class="connection-line"
        />
        <!-- Particle following the line -->
        <circle r="2" fill="#6366f1" class="line-particle">
          <animateMotion 
            :path="getLinePath(centerX, centerY, rival.x, rival.y)" 
            :dur="2 + Math.random() * 2 + 's'" 
            repeatCount="indefinite" 
          />
        </circle>
      </g>

      <!-- Rival Nodes -->
      <g v-for="(rival, index) in rivals" :key="'node-' + index" class="group cursor-pointer" 
         @click="$emit('select-rival', rival.name)"
         @dblclick="expandNode(rival.name)">
        <circle 
          :cx="rival.x" :cy="rival.y" 
          r="28" 
          class="fill-slate-800 stroke-slate-700 hover:stroke-brand-primary hover:fill-slate-700 transition-all duration-300" 
          stroke-width="2"
        />
        <!-- Hover effect ring -->
        <circle 
          :cx="rival.x" :cy="rival.y" 
          r="32" 
          class="fill-none stroke-brand-primary opacity-0 group-hover:opacity-20 transition-all duration-300" 
          stroke-width="3"
          stroke-dasharray="4 4"
        />
        <text 
          :x="rival.x" :y="rival.y + 45" 
          text-anchor="middle" 
          class="fill-slate-400 text-[10px] font-bold uppercase tracking-widest group-hover:fill-white transition-all duration-300"
        >
          {{ rival.name.split(' ').pop() }}
        </text>
        <text 
          :x="rival.x" :y="rival.y + 4" 
          text-anchor="middle" 
          class="fill-white text-[10px] font-black"
        >
          {{ rival.score }}{{ rival.type === 'bowler' ? 'w' : 'r' }}
        </text>
        <!-- Double-click hint -->
        <text 
          :x="rival.x" :y="rival.y - 40" 
          text-anchor="middle" 
          class="fill-brand-primary text-[8px] font-bold opacity-0 group-hover:opacity-100 transition-all duration-300"
        >
          2x CLICK
        </text>
      </g>

      <!-- Main Player Node (Center) -->
      <g class="animate-bounce-subtle cursor-pointer" @dblclick="expandCenter()">
        <circle 
          :cx="centerX" :cy="centerY" 
          r="35" 
          class="fill-brand-primary hover:fill-indigo-500 shadow-2xl transition-all duration-300"
        />
        <!-- Center node pulsing ring -->
        <circle 
          :cx="centerX" :cy="centerY" 
          r="40" 
          class="fill-none stroke-brand-primary opacity-30 animate-ping"
        />
        <text 
          :x="centerX" :y="centerY + 6" 
          text-anchor="middle" 
          class="fill-white text-lg font-black pointer-events-none"
        >
          {{ playerName.charAt(0) }}
        </text>
        <text 
          :x="centerX" :y="centerY + 55" 
          text-anchor="middle" 
          class="fill-white text-xs font-black uppercase tracking-widest pointer-events-none"
        >
          {{ playerName }}
        </text>
        <!-- Expand hint -->
        <text 
          :x="centerX" :y="centerY - 55" 
          text-anchor="middle" 
          class="fill-brand-primary text-[8px] font-bold animate-pulse"
        >
          2x CLICK TO EXPAND
        </text>
      </g>

      <!-- Gradients -->
      <defs>
        <linearGradient id="lineGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" stop-color="#FBBF24" stop-opacity="0.8" />
          <stop offset="100%" stop-color="#6366f1" stop-opacity="0.2" />
        </linearGradient>
      </defs>
    </svg>
    
    <div class="absolute bottom-4 left-6 flex items-center gap-2">
      <ShareIcon class="w-4 h-4 text-slate-500" />
      <span class="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Neo4j Relationship Explorer</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { watch } from 'vue'
import { ShareIcon } from '@heroicons/vue/24/outline'

const props = defineProps<{
  playerName: string
  rivals: any[]
  loading: boolean
}>()

const $emit = defineEmits(['select-rival', 'expand-node', 'expand-center'])

const expandNode = (rivalName: string) => {
  console.log(`Expanding node: ${rivalName}`)
  $emit('expand-node', rivalName)
}

const expandCenter = () => {
  console.log(`Expanding center node: ${props.playerName}`)
  $emit('expand-center', props.playerName)
}

const centerX = 250
const centerY = 180

const getLinePath = (x1: number, y1: number, x2: number, y2: number) => {
  return `M ${x1} ${y1} L ${x2} ${y2}`
}

watch(() => props.rivals, (newRivals) => {
  if (!newRivals) return
  const radius = 140
  newRivals.forEach((rival, index) => {
    const angle = (index / newRivals.length) * 2 * Math.PI - Math.PI / 2
    rival.x = centerX + radius * Math.cos(angle)
    rival.y = centerY + radius * Math.sin(angle)
  })
}, { immediate: true })
</script>

<style scoped>
@keyframes bounce-subtle {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
.animate-bounce-subtle {
  animation: bounce-subtle 3s ease-in-out infinite;
  transform-origin: center;
}

.connection-line {
  stroke-dasharray: 100;
  stroke-dashoffset: 100;
  animation: drawLine 2s ease-out forwards;
}

@keyframes drawLine {
  to { stroke-dashoffset: 0; }
}

.line-particle {
  filter: drop-shadow(0 0 4px #6366f1);
}
</style>
