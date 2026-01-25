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
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 font-sans flex flex-col">
    <!-- Header Navigation -->
    <header class="bg-gradient-to-r from-ipl-blue via-brand-primary to-ipl-blue-dark text-white border-b border-ipl-blue-dark/20 sticky top-0 z-50 safe-area-inset shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-2 sm:py-3 flex justify-between items-center min-h-[56px]">
        <div class="flex items-center gap-2 sm:gap-4 min-w-0 flex-1">
          <NuxtLink to="/" class="flex items-center gap-2 min-w-0" @click="closeMenu">
            <!-- Logo Mark -->
            <div class="w-8 h-8 sm:w-10 sm:h-10 rounded-full p-[0.125rem] shadow-md flex items-center justify-center flex-shrink-0">
              <img 
                src="/bg-logo.png" 
                alt="Boundary Graph Logo" 
                class="w-full h-full object-contain rounded-full"
              />
            </div>
            <div class="hidden xs:block min-w-0">
              <h1 class="text-base sm:text-lg font-bold tracking-tight text-white leading-tight truncate">Boundary Graph</h1>
              <p class="text-[8px] sm:text-[9px] text-ipl-orange font-bold uppercase tracking-wide mt-0.5 hidden sm:block leading-none">IPL Analytics for Gentlemen and Madmen</p>
            </div>
          </NuxtLink>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex gap-4 lg:gap-6 items-center">
          <NuxtLink to="/" class="nav-link">Overview</NuxtLink>
          <NuxtLink to="/points-table" class="nav-link">Points Table</NuxtLink>
          <NuxtLink to="/batsmen" class="nav-link">Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="nav-link">Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="nav-link">Teams</NuxtLink>
          <NuxtLink to="/venues" class="nav-link">Venues</NuxtLink>
          <NuxtLink to="/h2h" class="nav-link">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link">Search</NuxtLink>
          <NuxtLink to="/ask-bg" class="nav-link group flex items-center gap-1.5">
            <span>Ask BG</span>
            <div class="w-1.5 h-1.5 rounded-full bg-ipl-orange animate-pulse"></div>
          </NuxtLink>
          <div class="w-px h-5 bg-white/20 ml-1 mr-1"></div>
          <a 
            href="https://github.com/sidagarwal04/boundary-graph" 
            target="_blank" 
            class="p-1.5 text-white/70 hover:text-ipl-orange transition-colors"
            title="GitHub Repository"
          >
            <CodeBracketIcon class="w-4 h-4" />
          </a>
        </nav>

        <!-- Mobile Menu Toggle -->
        <button class="md:hidden p-2 -mr-2 text-white hover:text-ipl-orange transition-colors touch-target flex-shrink-0" @click="toggleMenu">
          <Bars3Icon v-if="!isMenuOpen" class="w-6 h-6" />
          <XMarkIcon v-else class="w-6 h-6" />
        </button>
      </div>

      <!-- Mobile Navigation Drawer -->
      <div 
        v-if="isMenuOpen" 
        class="md:hidden border-t border-ipl-blue-dark/20 bg-gradient-to-r from-ipl-blue to-ipl-blue-dark absolute top-full left-0 w-full shadow-xl animate-in slide-in-from-top-2 duration-200 max-h-[calc(100vh-80px)] overflow-y-auto safe-area-inset"
      >
        <nav class="flex flex-col p-4 space-y-1">
          <NuxtLink to="/" class="nav-link-mobile touch-target" @click="closeMenu">Overview</NuxtLink>
          <NuxtLink to="/points-table" class="nav-link-mobile touch-target" @click="closeMenu">Points Table</NuxtLink>
          <NuxtLink to="/batsmen" class="nav-link-mobile touch-target" @click="closeMenu">Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="nav-link-mobile touch-target" @click="closeMenu">Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="nav-link-mobile touch-target" @click="closeMenu">Teams</NuxtLink>
          <NuxtLink to="/venues" class="nav-link-mobile touch-target" @click="closeMenu">Venues</NuxtLink>
          <NuxtLink to="/h2h" class="nav-link-mobile touch-target" @click="closeMenu">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link-mobile touch-target" @click="closeMenu">Search</NuxtLink>
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
    <main class="flex-grow max-w-7xl mx-auto px-4 py-6 sm:py-8 w-full container-safe safe-area-inset">
      <slot />
    </main>

    <!-- Global Disclaimer Modal (Session-based) -->

    <!-- Global Disclaimer Modal (Session-based) -->
    <div v-if="showDisclaimer" class="fixed inset-0 z-[100] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-in fade-in duration-300">
      <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8 space-y-6 border border-slate-100 animate-in zoom-in-95 duration-300">
        <div class="flex flex-col items-center text-center space-y-4">
          <div class="w-16 h-16 bg-gradient-to-br from-yellow-100 to-orange-100 text-ipl-orange rounded-2xl flex items-center justify-center">
            <ExclamationTriangleIcon class="w-8 h-8" />
          </div>
          <div>
            <h2 class="text-2xl font-black text-ipl-blue">Legal Notice</h2>
            <p class="text-slate-600 text-sm mt-2">
              Before you proceed to Boundary Graph, please acknowledge our 
              <NuxtLink to="/disclaimer" @click="showDisclaimer = false" class="text-ipl-orange font-bold hover:text-ipl-blue transition-colors hover:underline">Legal Disclaimer</NuxtLink>.
            </p>
          </div>
        </div>
        
        <div class="bg-gradient-to-r from-blue-50 to-orange-50 p-4 rounded-2xl text-xs text-slate-600 leading-relaxed italic border-l-4 border-ipl-orange">
          "Boundary Graph is for educational & entertainment purposes only. Data is sourced from Cricsheet.org and processed via Neo4j. We are not liable for any losses or betting outcomes."
        </div>

        <button 
          @click="acceptDisclaimer"
          class="w-full py-4 bg-gradient-to-r from-ipl-blue to-ipl-blue-dark text-white rounded-2xl font-black hover:from-ipl-blue-dark hover:to-ipl-blue transition-all duration-300 shadow-lg hover:shadow-xl transform hover:scale-105"
        >
          I Understand & Agree
        </button>
      </div>
    </div>

    <!-- Footer -->
    <footer class="bg-gradient-to-r from-ipl-blue via-brand-primary to-ipl-blue-dark text-white border-t border-ipl-blue-dark/20">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-col items-center text-center">
          <p class="text-white/90 text-sm mb-2 font-medium">
            Built with ❤️ for cricket fans and data enthusiasts
          </p>
          <div class="flex items-center gap-4 text-white/70 text-[10px] sm:text-xs">
            <span>© 2026 Boundary Graph</span>
            <span class="text-white/40">•</span>
            <a href="https://meetsid.dev" target="_blank" class="text-ipl-orange hover:text-ipl-gold transition-colors font-medium italic">meetsid.dev</a>
            <span class="text-white/40">•</span>
            <NuxtLink to="/disclaimer" class="hover:text-ipl-orange transition-colors underline underline-offset-2">Legal Disclaimer</NuxtLink>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.nav-link {
  font-size: 0.8125rem; /* text-[13px] */
  font-weight: 600; /* font-semibold */
  color: rgba(255, 255, 255, 0.9); /* text-white/90 */
  transition-property: color, background-color;
  transition-duration: 200ms;
  padding: 0.375rem 0.75rem;
  border-radius: 0.375rem;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(249, 115, 22, 0.1), transparent);
  transition: left 0.3s ease;
}

.nav-link:hover {
  color: #F97316; /* hover:text-ipl-orange */
  background-color: rgba(249, 115, 22, 0.1);
}

.nav-link:hover::before {
  left: 100%;
}

.nav-link.router-link-active {
  color: #F97316; /* text-ipl-orange */
  font-weight: 700; /* font-bold */
  background-color: rgba(249, 115, 22, 0.15);
  box-shadow: inset 0 0 0 1px rgba(249, 115, 22, 0.3);
}

.nav-link-mobile {
  font-size: 1rem; /* text-base */
  font-weight: 600; /* font-semibold */
  color: rgba(255, 255, 255, 0.95); /* text-white/95 */
  display: block;
  padding: 0.875rem 1rem;
  border-radius: 0.5rem;
  transition-property: all;
  transition-duration: 200ms;
  margin-bottom: 0.25rem;
}

.nav-link-mobile:hover {
  background-color: rgba(249, 115, 22, 0.15);
  color: #F97316;
}

.nav-link-mobile.router-link-active {
  color: #F97316;
  background-color: rgba(249, 115, 22, 0.2);
  font-weight: 700;
}
</style>


