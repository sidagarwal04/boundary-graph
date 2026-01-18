<template>
  <div class="min-h-screen bg-slate-50">
    <!-- Header Navigation -->
    <header class="cricket-gradient text-white shadow-lg">
      <div class="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <span class="text-2xl">🏏</span>
          <h1 class="text-3xl font-bold">IPL Cricket Dashboard</h1>
        </div>
        <nav class="hidden md:flex gap-6">
          <NuxtLink to="/" class="hover:text-orange-200 transition">Overview</NuxtLink>
          <NuxtLink to="/batsmen" class="hover:text-orange-200 transition">Top Batsmen</NuxtLink>
          <NuxtLink to="/bowlers" class="hover:text-orange-200 transition">Top Bowlers</NuxtLink>
          <NuxtLink to="/teams" class="hover:text-orange-200 transition">Teams</NuxtLink>
          <NuxtLink to="/h2h" class="hover:text-orange-200 transition">H2H</NuxtLink>
          <NuxtLink to="/player-search" class="hover:text-orange-200 transition">Players</NuxtLink>
        </nav>
      </div>
    </header>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 py-8">
      <slot />
    </main>

    <!-- Footer -->
    <footer class="bg-slate-900 text-white text-center py-6 mt-12">
      <p>IPL Cricket Dashboard © 2026 | Professional Analytics Platform</p>
    </footer>
  </div>
</template>

<style scoped>
/* Navigation links styling */
</style>
