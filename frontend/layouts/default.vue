<script setup lang="ts">
import { ref } from 'vue'
import { ExclamationTriangleIcon, Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

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
  <div class="min-h-screen bg-slate-50 font-sans flex flex-col">
    <!-- Header Navigation -->
    <header class="bg-white text-slate-900 border-b border-slate-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <NuxtLink to="/" class="flex items-center gap-3" @click="closeMenu">
          <!-- Logo Mark -->
          <div class="w-8 h-8 bg-brand-primary text-white rounded flex items-center justify-center font-bold text-lg">
            B
          </div>
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-900">Boundary Graph</h1>
            <p class="text-[10px] text-slate-500 font-medium uppercase tracking-wide">Deep Analytics for Gentlemen & Madmen</p>
          </div>
        </NuxtLink>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex gap-8 items-center">
          <NuxtLink to="/" class="nav-link">Overview</NuxtLink>
          <NuxtLink to="/batsmen" class="nav-link">Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="nav-link">Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="nav-link">Teams</NuxtLink>
          <NuxtLink to="/h2h" class="nav-link">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link">Search</NuxtLink>
          <NuxtLink to="/ask-bg" class="nav-link group flex items-center gap-1.5">
            <span>Ask BG</span>
            <div class="w-1.5 h-1.5 rounded-full bg-brand-primary animate-pulse"></div>
          </NuxtLink>
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
          <NuxtLink to="/h2h" class="nav-link-mobile" @click="closeMenu">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link-mobile" @click="closeMenu">Search</NuxtLink>
          <NuxtLink to="/ask-bg" class="nav-link-mobile flex items-center justify-between" @click="closeMenu">
            <span>Ask BG</span>
            <div class="w-2 h-2 rounded-full bg-brand-primary animate-pulse"></div>
          </NuxtLink>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl mx-auto px-4 py-8 w-full">
      <slot />
    </main>

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
            Built with ❤️ for cricket fans and data enthusiasts using 
            <span class="font-semibold text-slate-800">Neo4j</span>, 
            <span class="font-semibold text-slate-800">Antigravity</span> and 
            <span class="font-semibold text-slate-800">Gemini</span>
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


