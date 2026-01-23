<template>
  <div :class="[
    'flex items-center gap-2',
    size === 'sm' && 'text-xs',
    size === 'md' && 'text-sm',
    size === 'lg' && 'text-base',
    size === 'xl' && 'text-lg',
    size === '2xl' && 'text-xl'
  ]">
    <div 
      v-if="logoUrl" 
      :class="[
        'rounded-full flex items-center justify-center p-1',
        size === 'sm' && 'w-8 h-8',
        size === 'md' && 'w-10 h-10', 
        size === 'lg' && 'w-12 h-12',
        size === 'xl' && 'w-14 h-14',
        size === '2xl' && 'w-16 h-16'
      ]"
      :style="{ backgroundColor: teamColor }"
    >
      <img 
        :src="logoUrl" 
        :alt="`${teamName} logo`"
        :class="[
          'object-contain',
          size === 'sm' && 'w-5 h-5',
          size === 'md' && 'w-6 h-6', 
          size === 'lg' && 'w-8 h-8',
          size === 'xl' && 'w-10 h-10',
          size === '2xl' && 'w-12 h-12'
        ]"
      />
    </div>
    <span v-if="showName" :class="textClass">
      {{ displayName }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getTeamLogo, getTeamAbbreviation, getTeamColor } from '~/utils/teamLogos'

interface Props {
  teamName: string
  size?: 'sm' | 'md' | 'lg' | 'xl' | '2xl'
  showName?: boolean
  useAbbreviation?: boolean
  textClass?: string
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  showName: true,
  useAbbreviation: false,
  textClass: ''
})

const logoUrl = computed(() => {
  return getTeamLogo(props.teamName)
})

const teamColor = computed(() => {
  return getTeamColor(props.teamName)
})

const displayName = computed(() => {
  if (!props.showName) return ''
  return props.useAbbreviation ? getTeamAbbreviation(props.teamName) : props.teamName
})
</script>