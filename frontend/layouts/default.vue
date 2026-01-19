<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { 
  ExclamationTriangleIcon, 
  Bars3Icon, 
  XMarkIcon, 
  CodeBracketIcon, 
  MagnifyingGlassIcon,
  UserIcon,
  UserGroupIcon,
  MapPinIcon
} from '@heroicons/vue/24/outline'

const config = useRuntimeConfig()
const router = useRouter()

const showDisclaimer = ref(true)
const isMenuOpen = ref(false)

// Global Search State
const isSearchOpen = ref(false)
const searchQuery = ref('')
const searchResults = ref<any[]>([])
const selectedIndex = ref(0)
const isSearching = ref(false)
const searchInput = ref<HTMLInputElement | null>(null)

const toggleSearch = () => {
  isSearchOpen.value = !isSearchOpen.value
  if (isSearchOpen.value) {
    searchQuery.value = ""
    searchResults.value = []
    selectedIndex.value = 0
    setTimeout(() => searchInput.value?.focus(), 100)
  }
}

const handleSearch = async () => {
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    return
  }
  
  isSearching.value = true
  try {
    const data = await $fetch(`${config.public.apiBase}/api/search?q=${encodeURIComponent(searchQuery.value)}`)
    searchResults.value = Array.isArray(data) ? data : []
    selectedIndex.value = 0
  } catch (e) {
    console.error("Search failed", e)
  } finally {
    isSearching.value = false
  }
}

watch(searchQuery, () => {
  handleSearch()
})

const navigateToResult = (result: any) => {
  isSearchOpen.value = false
  if (result.type === 'player') {
    router.push(`/player-search?name=${encodeURIComponent(result.name)}`)
  } else if (result.type === 'team') {
    router.push(`/teams?name=${encodeURIComponent(result.name)}`)
  } else if (result.type === 'venue') {
    router.push(`/venues?name=${encodeURIComponent(result.name)}`)
  }
}

const handleKeyDown = (e: KeyboardEvent) => {
  if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
    e.preventDefault()
    toggleSearch()
  }

  if (!isSearchOpen.value) return

  if (e.key === 'Escape') {
    isSearchOpen.value = false
  } else if (e.key === 'ArrowDown') {
    e.preventDefault()
    selectedIndex.value = (selectedIndex.value + 1) % searchResults.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    selectedIndex.value = (selectedIndex.value - 1 + searchResults.value.length) % searchResults.value.length
  } else if (e.key === 'Enter') {
    if (searchResults.value[selectedIndex.value]) {
      navigateToResult(searchResults.value[selectedIndex.value])
    }
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeyDown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeyDown)
})

const acceptDisclaimer = () => {
  showDisclaimer.value = false
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}
</script>

<template>
  <div class="min-h-screen bg-slate-50 font-sans flex flex-col">
    <!-- Header Navigation -->
    <header class="bg-white text-slate-900 border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center gap-6">
          <NuxtLink to="/" class="flex items-center gap-3" @click="closeMenu">
            <!-- Logo Mark -->
            <div class="w-8 h-8 bg-brand-primary text-white rounded flex items-center justify-center font-bold text-lg">
              B
            </div>
            <div class="hidden sm:block">
              <h1 class="text-xl font-bold tracking-tight text-slate-900 leading-none">Boundary Graph</h1>
              <p class="text-[10px] text-slate-500 font-medium uppercase tracking-wide mt-1">IPL Graph Analytics</p>
            </div>
          </NuxtLink>

          <!-- Search Trigger -->
          <button 
            @click="toggleSearch"
            class="hidden md:flex items-center gap-3 px-3 py-1.5 bg-slate-50 border border-slate-200 rounded-lg text-slate-400 hover:border-slate-300 transition-colors group"
          >
            <MagnifyingGlassIcon class="w-4 h-4" />
            <span class="text-sm font-medium">Search anything...</span>
            <div class="flex items-center gap-1 ml-4 bg-white px-1.5 py-0.5 rounded border border-slate-200 text-[10px] font-bold">
              <span>⌘</span>
              <span>K</span>
            </div>
          </button>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex gap-8 items-center">
          <NuxtLink to="/" class="nav-link">Overview</NuxtLink>
          <NuxtLink to="/batsmen" class="nav-link">Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="nav-link">Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="nav-link">Teams</NuxtLink>
          <NuxtLink to="/venues" class="nav-link">Venues</NuxtLink>
          <NuxtLink to="/h2h" class="nav-link">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link">Search</NuxtLink>
          <NuxtLink to="/ask-bg" class="nav-link group flex items-center gap-1.5">
            <span>Ask BG</span>
            <div class="w-1.5 h-1.5 rounded-full bg-brand-primary animate-pulse"></div>
          </NuxtLink>
          <div class="w-px h-6 bg-slate-200 ml-2 mr-2"></div>
          <a 
            href="https://github.com/sidagarwal04/boundary-graph" 
            target="_blank" 
            class="p-2 text-slate-400 hover:text-slate-900 transition-colors"
            title="GitHub Repository"
          >
            <CodeBracketIcon class="w-5 h-5" />
          </a>
        </nav>

        <!-- Mobile Menu Toggle -->
        <button class="md:hidden p-2 -mr-2 text-slate-600" @click="toggleMenu">
          <Bars3Icon v-if="!isMenuOpen" class="w-6 h-6" />
          <XMarkIcon v-else class="w-6 h-6" />
        </button>
      </div>

      <!-- Mobile Navigation Drawer -->
      <div 
        v-if="isMenuOpen" 
        class="md:hidden border-t border-slate-100 bg-white absolute top-full left-0 w-full shadow-xl animate-in slide-in-from-top-2 duration-200"
      >
        <nav class="flex flex-col p-4 space-y-4">
          <NuxtLink to="/" class="nav-link-mobile" @click="closeMenu">Overview</NuxtLink>
          <NuxtLink to="/batsmen" class="nav-link-mobile" @click="closeMenu">Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="nav-link-mobile" @click="closeMenu">Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="nav-link-mobile" @click="closeMenu">Teams</NuxtLink>
          <NuxtLink to="/venues" class="nav-link-mobile" @click="closeMenu">Venues</NuxtLink>
          <NuxtLink to="/h2h" class="nav-link-mobile" @click="closeMenu">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link-mobile" @click="closeMenu">Search</NuxtLink>
          <NuxtLink to="/ask-bg" class="nav-link-mobile flex items-center justify-between" @click="closeMenu">
            <span>Ask BG</span>
            <div class="w-2 h-2 rounded-full bg-brand-primary animate-pulse"></div>
          </NuxtLink>
          <a 
            href="https://github.com/sidagarwal04/boundary-graph" 
            target="_blank" 
            class="nav-link-mobile flex items-center justify-between text-slate-500"
            @click="closeMenu"
          >
            <span>GitHub Repository</span>
            <CodeBracketIcon class="w-5 h-5" />
          </a>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl mx-auto px-4 py-8 w-full">
      <slot />
    </main>

    <!-- Command Palette / Global Search -->
    <div v-if="isSearchOpen" class="fixed inset-0 z-[110] flex items-start justify-center pt-[15vh] px-4 pointer-events-none">
      <div class="absolute inset-0 bg-slate-900/40 backdrop-blur-sm pointer-events-auto" @click="isSearchOpen = false"></div>
      
      <div class="bg-white w-full max-w-xl rounded-2xl shadow-2xl overflow-hidden border border-slate-100 animate-in zoom-in-95 duration-200 pointer-events-auto">
        <div class="p-4 border-b border-slate-100 flex items-center gap-3">
          <MagnifyingGlassIcon class="w-5 h-5 text-slate-400" />
          <input 
            ref="searchInput"
            v-model="searchQuery"
            type="text"
            placeholder="Search players, teams, or venues..."
            class="flex-1 bg-transparent outline-none text-slate-800 placeholder-slate-400 font-medium"
            @keydown="handleKeyDown"
          />
          <div class="text-[10px] font-bold text-slate-400 px-2 py-1 bg-slate-50 rounded uppercase tracking-widest leading-none">ESC to close</div>
        </div>

        <div class="max-h-[60vh] overflow-y-auto">
          <div v-if="searchQuery.length > 0 && searchResults.length === 0 && !isSearching" class="p-12 text-center text-slate-400 italic">
            No results found for "{{ searchQuery }}"
          </div>

          <div v-if="searchResults.length > 0" class="p-2">
            <div 
              v-for="(result, index) in searchResults" 
              :key="result.id"
              @mouseover="selectedIndex = index"
              @click="navigateToResult(result)"
              :class="[
                'flex items-center gap-4 p-3 rounded-xl cursor-pointer transition-colors group',
                selectedIndex === index ? 'bg-brand-primary/5' : ''
              ]"
            >
              <div :class="[
                'w-10 h-10 rounded-lg flex items-center justify-center transition-colors',
                selectedIndex === index ? 'bg-brand-primary text-white' : 'bg-slate-50 text-slate-400'
              ]">
                <UserIcon v-if="result.type === 'player'" class="w-6 h-6" />
                <UserGroupIcon v-if="result.type === 'team'" class="w-6 h-6" />
                <MapPinIcon v-if="result.type === 'venue'" class="w-6 h-6" />
              </div>
              <div class="flex-1">
                <p :class="[
                  'font-bold transition-colors',
                  selectedIndex === index ? 'text-slate-900' : 'text-slate-600'
                ]">{{ result.name }}</p>
                <p class="text-[10px] font-bold uppercase tracking-widest text-slate-400">{{ result.type }}</p>
              </div>
              <div v-if="selectedIndex === index" class="text-xs font-bold text-brand-primary animate-in fade-in slide-in-from-right-2">Enter ↵</div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Global Disclaimer Modal (Session-based) -->
    <div v-if="showDisclaimer" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-300">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8 space-y-6 border border-slate-100 animate-in zoom-in-95 duration-300">
        <div class="flex flex-col items-center text-center space-y-4">
          <div class="w-16 h-16 bg-red-50 text-red-600 rounded-2xl flex items-center justify-center">
            <ExclamationTriangleIcon class="w-8 h-8" />
          </div>
          <div>
            <h2 class="text-2xl font-black text-slate-900">Legal Notice</h2>
            <p class="text-slate-500 text-sm mt-2">
              Before you proceed to Boundary Graph, please acknowledge our 
              <NuxtLink to="/disclaimer" @click="showDisclaimer = false" class="text-brand-primary font-bold hover:underline">Legal Disclaimer</NuxtLink>.
            </p>
          </div>
        </div>
        
        <div class="bg-slate-50 p-4 rounded-xl text-xs text-slate-500 leading-relaxed italic">
          "Boundary Graph is for educational & entertainment purposes only. Data is sourced from Cricsheet.org and processed via Neo4j. We are not liable for any losses or betting outcomes."
        </div>

        <button 
          @click="acceptDisclaimer"
          class="w-full py-4 bg-slate-900 text-white rounded-2xl font-black hover:bg-black transition-colors shadow-lg shadow-slate-200"
        >
          I Understand & Agree
        </button>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-col items-center text-center">
          <p class="text-slate-600 text-sm mb-2">
            Built with ❤️ for cricket fans and data enthusiasts
          </p>
          <div class="flex items-center gap-4 text-slate-400 text-[10px] sm:text-xs">
            <span>© 2026 Boundary Graph</span>
            <span class="text-slate-300">•</span>
            <a href="https://meetsid.dev" target="_blank" class="text-brand-primary hover:underline font-medium italic">meetsid.dev</a>
            <span class="text-slate-300">•</span>
            <NuxtLink to="/disclaimer" class="hover:text-slate-600 underline underline-offset-2">Legal Disclaimer</NuxtLink>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.nav-link {
  @apply text-sm font-medium text-slate-600 hover:text-brand-primary transition-colors duration-200;
}

.nav-link.router-link-active {
  @apply text-brand-primary font-semibold;
}

.nav-link-mobile {
  @apply text-base font-bold text-slate-700 block py-2 border-b border-slate-50;
}

.nav-link-mobile.router-link-active {
  @apply text-brand-primary;
}
</style>


