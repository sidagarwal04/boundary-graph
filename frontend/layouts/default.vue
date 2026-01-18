<template>
  <div class="min-h-screen bg-slate-50 font-sans flex flex-col">
    <!-- Header Navigation -->
    <header class="bg-white text-slate-900 border-b border-slate-200">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <!-- Logo Mark -->
          <div class="w-8 h-8 bg-brand-primary text-white rounded flex items-center justify-center font-bold text-lg">
            B
          </div>
          <div>
            <h1 class="text-xl font-bold tracking-tight text-slate-900">Boundary Graph</h1>
            <p class="text-xs text-slate-500 font-medium uppercase tracking-wide">Where Numbers Meet the Boundary</p>
          </div>
        </div>
        <nav class="hidden md:flex gap-8 items-center">
          <NuxtLink to="/" class="nav-link">Overview</NuxtLink>
          <NuxtLink to="/batsmen" class="nav-link">Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="nav-link">Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="nav-link">Teams</NuxtLink>
          <NuxtLink to="/h2h" class="nav-link">Compare</NuxtLink>
          <NuxtLink to="/player-search" class="nav-link">Search</NuxtLink>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="flex-grow max-w-7xl mx-auto px-4 py-8 w-full">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-white border-t border-slate-200">
      <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row justify-between items-center">
          <div class="mb-4 md:mb-0 text-center md:text-left">
            <h2 class="text-lg font-bold text-slate-800">Boundary Graph</h2>
            <p class="text-slate-500 text-sm mt-1">Deep Analytics for Gentlemen & Madmen</p>
          </div>
          <div class="flex gap-4">
             <span class="text-slate-400 text-sm">© 2026 Boundary Graph. All rights reserved.</span>
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
</style>


