<template>
  <div class="relative bg-slate-900 rounded-2xl sm:rounded-3xl p-4 sm:p-8 overflow-hidden h-[300px] sm:h-[400px] flex items-center justify-center border border-slate-800 shadow-2xl">
    <!-- Grid Pattern -->
    <div class="absolute inset-0 opacity-10 pointer-events-none" style="background-image: radial-gradient(#6366f1 0.5px, transparent 0.5px); background-size: 24px 24px;"></div>
    
    <div v-if="loading" class="flex flex-col items-center gap-4 animate-pulse">
      <div class="w-12 h-12 rounded-full border-4 border-brand-primary border-t-transparent animate-spin"></div>
      <p class="text-slate-400 text-xs font-bold uppercase tracking-widest">Traversing Graph...</p>
    </div>

    <svg v-else viewBox="0 0 500 400" class="w-full h-full relative z-10 transition-opacity duration-1000 touch-pan-y" :class="{ 'opacity-100': !loading, 'opacity-0': loading }">
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
      <g v-for="(rival, index) in rivals" :key="'node-' + index" class="group cursor-move" 
         @mousedown="startDrag(rival, $event)"
         @mouseup="handleMouseUp(rival, $event)">
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
          class="fill-slate-400 text-[10px] font-bold uppercase tracking-widest group-hover:fill-white transition-all duration-300 pointer-events-none"
        >
          {{ rival.name.split(' ').pop() }}
        </text>
        <text 
          :x="rival.x" :y="rival.y + 4" 
          text-anchor="middle" 
          class="fill-white text-[10px] font-black pointer-events-none"
        >
          {{ rival.score }}{{ rival.type === 'bowler' ? 'w' : 'r' }}
        </text>
      </g>

      <!-- Main Player Node (Center) -->
      <g class="animate-bounce-subtle cursor-move" @mousedown="startDrag(centerNode, $event)">
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
import { watch, ref, onMounted, onUnmounted } from 'vue'
import { ShareIcon } from '@heroicons/vue/24/outline'

const props = defineProps<{
  playerName: string
  rivals: any[]
  loading: boolean
}>()

const $emit = defineEmits(['select-rival'])

const centerX = ref(250)
const centerY = ref(180)
const centerNode = ref({ x: centerX.value, y: centerY.value, name: 'center' })
const isDragging = ref(false)
const dragNode = ref<any>(null)
const dragOffset = ref({ x: 0, y: 0 })
const dragStartPosition = ref({ x: 0, y: 0 })
const hasDragged = ref(false)

const getLinePath = (x1: number, y1: number, x2: number, y2: number) => {
  return `M ${x1} ${y1} L ${x2} ${y2}`
}

const startDrag = (node: any, event: MouseEvent) => {
  event.preventDefault()
  isDragging.value = true
  dragNode.value = node
  hasDragged.value = false
  
  const rect = (event.target as Element).closest('svg')?.getBoundingClientRect()
  if (rect) {
    const svgX = (event.clientX - rect.left) * (500 / rect.width)
    const svgY = (event.clientY - rect.top) * (400 / rect.height)
    dragOffset.value = {
      x: svgX - node.x,
      y: svgY - node.y
    }
    dragStartPosition.value = { x: svgX, y: svgY }
  }
}

const handleMouseUp = (node: any, event: MouseEvent) => {
  if (isDragging.value && !hasDragged.value && node.name) {
    // This was a click, not a drag
    $emit('select-rival', node.name)
  }
  isDragging.value = false
  dragNode.value = null
  hasDragged.value = false
}

const handleMouseMove = (event: MouseEvent) => {
  if (!isDragging.value || !dragNode.value) return
  
  const rect = document.querySelector('svg')?.getBoundingClientRect()
  if (rect) {
    const svgX = (event.clientX - rect.left) * (500 / rect.width)
    const svgY = (event.clientY - rect.top) * (400 / rect.height)
    
    // Check if we've moved enough to consider this a drag
    const dragDistance = Math.sqrt(
      Math.pow(svgX - dragStartPosition.value.x, 2) + 
      Math.pow(svgY - dragStartPosition.value.y, 2)
    )
    
    if (dragDistance > 3) {
      hasDragged.value = true
    }
    
    dragNode.value.x = Math.max(35, Math.min(465, svgX - dragOffset.value.x))
    dragNode.value.y = Math.max(35, Math.min(365, svgY - dragOffset.value.y))
    
    if (dragNode.value.name === 'center') {
      centerX.value = dragNode.value.x
      centerY.value = dragNode.value.y
    }
  }
}

const handleGlobalMouseUp = () => {
  isDragging.value = false
  dragNode.value = null
  hasDragged.value = false
}

onMounted(() => {
  document.addEventListener('mousemove', handleMouseMove)
  document.addEventListener('mouseup', handleGlobalMouseUp)
})

onUnmounted(() => {
  document.removeEventListener('mousemove', handleMouseMove)
  document.removeEventListener('mouseup', handleGlobalMouseUp)
})

watch(() => props.rivals, (newRivals) => {
  if (!newRivals) return
  const radius = 140
  newRivals.forEach((rival, index) => {
    const angle = (index / newRivals.length) * 2 * Math.PI - Math.PI / 2
    rival.x = centerX.value + radius * Math.cos(angle)
    rival.y = centerY.value + radius * Math.sin(angle)
  })
}, { immediate: true })

// Update rival positions when center moves
watch([centerX, centerY], ([newCenterX, newCenterY]) => {
  centerNode.value.x = newCenterX
  centerNode.value.y = newCenterY
})
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
