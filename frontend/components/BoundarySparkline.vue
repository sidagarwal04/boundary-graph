<template>
  <div class="sparkline-wrapper">
    <div class="boundary-sparkline" :title="tooltipText">
      <canvas 
        ref="canvasRef" 
        :width="width" 
        :height="height" 
        class="sparkline-canvas"
        @mousemove="handleMouseMove"
        @mouseleave="hideTooltip"
      />
      <div v-if="showTrend" class="trend-info">
        <span :class="trendClasses">{{ trendIcon }}</span>
        <span class="text-xs font-medium" :class="trendTextColor">
          {{ metricValue.toFixed(1) }}{{ metricSuffix }}
        </span>
      </div>
    </div>
    
    <!-- Hover Tooltip -->
    <div v-if="hoveredPoint" class="hover-tooltip" :style="tooltipStyle">
      <div class="tooltip-season">{{ hoveredPoint.season }}</div>
      <div class="tooltip-value">{{ hoveredPoint.value.toFixed(1) }}{{ metricSuffix }}</div>
      <div v-if="type === 'boundary'" class="tooltip-details">
        {{ hoveredPoint.boundaries }} boundaries in {{ hoveredPoint.balls }} balls
      </div>
      <div v-else-if="type === 'economy'" class="tooltip-details">
        {{ hoveredPoint.runs }} runs in {{ Math.round(hoveredPoint.balls / 6) }} overs
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
/**
 * BoundarySparkline Component
 * 
 * A versatile sparkline component for visualizing player performance trends across seasons.
 * Supports multiple metric types for comprehensive player analysis.
 * 
 * Features:
 * - Interactive canvas-based sparkline with hover tooltips
 * - Multiple metric types: boundary rate, economy rate, wickets per innings
 * - Season labels for clear timeline visualization
 * - Trend analysis with visual indicators (improving/declining/stable)
 * - Responsive design with high-DPI support
 * - Customizable colors and dimensions
 * 
 * Usage:
 * - Boundary Rate: Shows (fours + sixes) / balls percentage for batsmen
 * - Economy Rate: Shows runs per over for bowlers (lower is better)
 * - Wickets Rate: Shows wickets per innings for bowlers/all-rounders
 */
import { ref, onMounted, watch, computed, nextTick } from 'vue'

interface SeasonStats {
  batting?: {
    fours: number
    sixes: number
    balls: number
    runs: number
  }
  bowling?: {
    wickets: number
    runs: number
    balls: number
    innings: number
    economy?: number
  }
}

interface Props {
  seasonData: Record<string, SeasonStats>
  type?: 'boundary' | 'economy' | 'wickets'
  width?: number
  height?: number
  showTrend?: boolean
  primaryColor?: string
  backgroundColor?: string
}

const props = withDefaults(defineProps<Props>(), {
  type: 'boundary',
  width: 120,
  height: 40,
  showTrend: true,
  primaryColor: '#6366f1',
  backgroundColor: '#f8fafc'
})

const canvasRef = ref<HTMLCanvasElement>()
const hoveredPoint = ref<any>(null)
const tooltipStyle = ref({})

// Calculate metric data for each season based on type
const metricData = computed(() => {
  const seasons = Object.keys(props.seasonData).sort()
  return seasons.map(season => {
    const batting = props.seasonData[season].batting
    const bowling = props.seasonData[season].bowling
    
    if (props.type === 'boundary') {
      const totalBalls = batting?.balls || 0
      const boundaries = (batting?.fours || 0) + (batting?.sixes || 0)
      const rate = totalBalls > 0 ? (boundaries / totalBalls) * 100 : 0
      return {
        season,
        value: rate,
        boundaries,
        balls: totalBalls,
        hasData: totalBalls > 0
      }
    } else if (props.type === 'economy') {
      const balls = bowling?.balls || 0
      const runs = bowling?.runs || 0
      const economy = balls > 0 ? (runs * 6) / balls : 0
      return {
        season,
        value: economy,
        runs,
        balls,
        hasData: balls > 0
      }
    } else if (props.type === 'wickets') {
      const innings = bowling?.innings || 0
      const wickets = bowling?.wickets || 0
      const rate = innings > 0 ? wickets / innings : 0
      return {
        season,
        value: rate,
        wickets,
        innings,
        hasData: innings > 0
      }
    }
    
    return { season, value: 0, hasData: false }
  }).filter(d => d.hasData)
})

// Calculate overall metric value and trend
const metricValue = computed(() => {
  if (metricData.value.length === 0) return 0
  
  if (props.type === 'boundary') {
    const totalBoundaries = metricData.value.reduce((sum, d) => sum + (d.boundaries || 0), 0)
    const totalBalls = metricData.value.reduce((sum, d) => sum + (d.balls || 0), 0)
    return totalBalls > 0 ? (totalBoundaries / totalBalls) * 100 : 0
  } else {
    return metricData.value.reduce((sum, d) => sum + d.value, 0) / metricData.value.length
  }
})

const metricSuffix = computed(() => {
  switch (props.type) {
    case 'boundary': return '%'
    case 'economy': return ' ER'
    case 'wickets': return ' WPI'
    default: return ''
  }
})

const trend = computed(() => {
  if (metricData.value.length < 2) return 'stable'
  
  const recent = metricData.value.slice(-3) // Last 3 seasons
  const earlier = metricData.value.slice(0, -3) // Earlier seasons
  
  if (recent.length === 0 || earlier.length === 0) return 'stable'
  
  const recentAvg = recent.reduce((sum, d) => sum + d.value, 0) / recent.length
  const earlierAvg = earlier.reduce((sum, d) => sum + d.value, 0) / earlier.length
  
  const changeThreshold = props.type === 'economy' ? 0.5 : 5 // Lower threshold for economy rate
  const change = Math.abs(recentAvg - earlierAvg)
  
  if (change < changeThreshold) return 'stable'
  
  // For economy rate, lower is better (reverse logic)
  if (props.type === 'economy') {
    return recentAvg < earlierAvg ? 'improving' : 'declining'
  }
  
  // For boundary rate and wickets per innings, higher is better
  return recentAvg > earlierAvg ? 'improving' : 'declining'
})

const trendIcon = computed(() => {
  switch (trend.value) {
    case 'improving': return '↗'
    case 'declining': return '↘'
    default: return '→'
  }
})

const trendClasses = computed(() => ({
  'text-green-500': trend.value === 'improving',
  'text-red-500': trend.value === 'declining',
  'text-gray-500': trend.value === 'stable',
  'text-sm font-bold': true
}))

const trendTextColor = computed(() => ({
  'text-green-700': trend.value === 'improving',
  'text-red-700': trend.value === 'declining',
  'text-gray-600': trend.value === 'stable'
}))

const tooltipText = computed(() => {
  if (metricData.value.length === 0) return 'No data available'
  
  const seasons = metricData.value.length
  const metricName = props.type === 'boundary' ? 'boundary rate' : 
                     props.type === 'economy' ? 'economy rate' : 
                     'wickets per innings'
  
  return `${seasons} seasons • ${metricName} • ${trend.value} trend`
})

const handleMouseMove = (event: MouseEvent) => {
  const canvas = canvasRef.value
  if (!canvas || metricData.value.length === 0) return
  
  const rect = canvas.getBoundingClientRect()
  const x = event.clientX - rect.left
  const padding = 4
  const width = rect.width - padding * 2
  
  // Find closest data point
  const dataIndex = Math.round(((x - padding) / width) * (metricData.value.length - 1))
  const clampedIndex = Math.max(0, Math.min(dataIndex, metricData.value.length - 1))
  
  const point = metricData.value[clampedIndex]
  if (point) {
    hoveredPoint.value = point
    tooltipStyle.value = {
      left: (event.clientX - rect.left) + 'px',
      top: (event.clientY - rect.top - 40) + 'px'
    }
  }
}

const hideTooltip = () => {
  hoveredPoint.value = null
}

const drawSparkline = () => {
  const canvas = canvasRef.value
  if (!canvas || metricData.value.length === 0) return
  
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  
  // Set high DPI for crisp lines
  const dpr = window.devicePixelRatio || 1
  const rect = canvas.getBoundingClientRect()
  
  // Use actual container width instead of fixed width
  const actualWidth = rect.width
  const actualHeight = rect.height
  
  canvas.width = actualWidth * dpr
  canvas.height = actualHeight * dpr
  ctx.scale(dpr, dpr)
  
  const width = actualWidth
  const height = actualHeight
  const padding = 4
  
  // Clear canvas
  ctx.fillStyle = props.backgroundColor
  ctx.fillRect(0, 0, width, height)
  
  if (metricData.value.length < 2) {
    // Draw a simple dot for single data point
    if (metricData.value.length === 1) {
      ctx.fillStyle = props.primaryColor
      ctx.beginPath()
      ctx.arc(width / 2, height / 2, 2, 0, Math.PI * 2)
      ctx.fill()
    }
    return
  }
  
  const data = metricData.value.map(d => d.value)
  const min = Math.min(...data)
  const max = Math.max(...data)
  const range = max - min || 1 // Prevent division by zero
  
  // Create points
  const points = data.map((value, index) => ({
    x: padding + (index * (width - padding * 2)) / (data.length - 1),
    y: padding + (height - padding * 2) - ((value - min) / range) * (height - padding * 2)
  }))
  
  // Draw area fill (subtle)
  ctx.fillStyle = `${props.primaryColor}20`
  ctx.beginPath()
  ctx.moveTo(points[0].x, height - padding)
  points.forEach(point => ctx.lineTo(point.x, point.y))
  ctx.lineTo(points[points.length - 1].x, height - padding)
  ctx.closePath()
  ctx.fill()
  
  // Draw line
  ctx.strokeStyle = props.primaryColor
  ctx.lineWidth = 2
  ctx.lineCap = 'round'
  ctx.lineJoin = 'round'
  ctx.beginPath()
  ctx.moveTo(points[0].x, points[0].y)
  points.slice(1).forEach(point => ctx.lineTo(point.x, point.y))
  ctx.stroke()
  
  // Draw dots
  ctx.fillStyle = props.primaryColor
  points.forEach(point => {
    ctx.beginPath()
    ctx.arc(point.x, point.y, 2.5, 0, Math.PI * 2)
    ctx.fill()
  })
}

onMounted(() => {
  drawSparkline()
})

watch([() => props.seasonData, () => props.width, () => props.height, () => props.type], () => {
  nextTick(() => drawSparkline())
})
</script>

<style scoped>
.sparkline-wrapper {
  position: relative;
}

.boundary-sparkline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.sparkline-canvas {
  border-radius: 0.5rem;
  background-color: #f8fafc;
  border: 1px solid #e2e8f0;
  cursor: crosshair;
  width: 100%;
  height: auto;
  min-width: 120px;
}

.trend-info {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  flex-shrink: 0;
}

.hover-tooltip {
  position: absolute;
  z-index: 10;
  background-color: #1e293b;
  color: white;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  pointer-events: none;
  transform: translateX(-50%);
  font-size: 12px;
  min-width: 120px;
}

.tooltip-season {
  font-weight: bold;
  color: #fde047;
}

.tooltip-value {
  font-weight: 600;
}

.tooltip-details {
  color: #cbd5e1;
  font-size: 0.75rem;
  margin-top: 0.25rem;
}
</style>