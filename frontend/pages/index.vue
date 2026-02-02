<template>
  <div class="container mx-auto px-4 py-8">
    <div class="pb-4">
    <!-- Project Intro -->
    <div class="mb-6 sm:mb-8 p-5 sm:p-6 bg-gradient-to-br from-white via-ipl-orange/5 to-ipl-blue/5 rounded-2xl sm:rounded-3xl border border-ipl-blue/10 shadow-xl overflow-hidden relative animate-in fade-in slide-in-from-top-4 duration-700">
      <!-- Decorative Elements -->
      <div class="absolute top-0 right-0 w-24 h-24 sm:w-32 sm:h-32 bg-gradient-to-br from-ipl-orange/20 to-ipl-blue/20 rounded-full -mr-12 -mt-12 sm:-mr-16 sm:-mt-16 animate-pulse-slow"></div>
      <div class="absolute bottom-0 left-0 w-20 h-20 sm:w-24 sm:h-24 bg-gradient-to-tr from-ipl-gold/20 to-transparent rounded-full -ml-10 -mb-10 sm:-ml-12 sm:-mb-12"></div>
      
      <div class="relative flex flex-col lg:flex-row lg:items-center justify-between gap-5 sm:gap-6">
        <div class="space-y-3 sm:space-y-4">
            <div class="space-y-2">
              <h2 class="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight text-responsive">
                <span class="bg-gradient-to-r from-ipl-blue to-ipl-orange bg-clip-text text-transparent">Boundary Graph</span> 
                <!-- <span class="text-ipl-blue">Analytics</span> -->
              </h2>
              <p class="text-slate-600 leading-relaxed text-base sm:text-lg">
                Welcome to <strong class="text-ipl-blue">Boundary Graph</strong>, the ultimate cricket analytics platform designed exclusively for the <strong class="text-ipl-orange">Indian Premier League (IPL)</strong>. This cutting-edge educational project leverages ball-by-ball IPL data through high-performance Neo4j graph technology. Dive deep into player trajectories, team dynamics, and venue insights from India's most electrifying T20 tournament spanning 2008-2025.
              </p>
            </div>
            <div class="mt-4 p-4 bg-gradient-to-r from-blue-50 to-orange-50 border-l-4 border-ipl-orange rounded-xl">
              <p class="text-sm text-slate-700 leading-relaxed">
              <strong class="text-ipl-blue">Educational Project:</strong> This is an independent, non-commercial project created for educational and technical demonstration purposes. Not affiliated with any cricket organization. <NuxtLink to="/disclaimer" class="text-ipl-orange underline font-semibold hover:text-ipl-blue transition-colors">View legal disclaimer</NuxtLink>.
              </p>
            </div>
            
            <!-- Tech Stack Pill -->
            <div class="flex flex-wrap items-start gap-3 sm:gap-4 pt-4">
              <span class="text-xs font-bold text-ipl-blue/70 uppercase tracking-widest shrink-0">Powered By</span>
              <div class="flex flex-wrap gap-2 sm:gap-3 min-w-0">
                <div class="flex items-center gap-2 px-3 sm:px-4 py-2 bg-gradient-to-r from-blue-100 to-blue-50 rounded-xl border border-blue-200 min-h-touch shadow-sm hover:shadow-md transition-all duration-200" title="Graph Database">
                  <CircleStackIcon class="w-4 h-4 text-blue-600 shrink-0" />
                  <span class="text-xs font-bold text-blue-800 whitespace-nowrap">Neo4j</span>
                </div>
                <div class="flex items-center gap-2 px-3 sm:px-4 py-2 bg-gradient-to-r from-emerald-100 to-emerald-50 rounded-xl border border-emerald-200 min-h-touch shadow-sm hover:shadow-md transition-all duration-200" title="Frontend Framework">
                  <SparklesIcon class="w-4 h-4 text-emerald-600 shrink-0" />
                  <span class="text-xs font-bold text-emerald-800 whitespace-nowrap">Nuxt 3</span>
                </div>
                <div class="flex items-center gap-2 px-3 sm:px-4 py-2 bg-gradient-to-r from-orange-100 to-orange-50 rounded-xl border border-orange-200 min-h-touch shadow-sm hover:shadow-md transition-all duration-200" title="API Backend">
                  <BoltIcon class="w-4 h-4 text-orange-600 shrink-0" />
                  <span class="text-xs font-bold text-orange-800 whitespace-nowrap">FastAPI</span>
                </div>
                <div class="flex items-center gap-2 px-3 sm:px-4 py-2 bg-gradient-to-r from-indigo-100 to-indigo-50 rounded-xl border border-indigo-200 min-h-touch shadow-sm hover:shadow-md transition-all duration-200" title="AI Coding Assistant">
                  <CpuChipIcon class="w-4 h-4 text-indigo-600 shrink-0" />
                  <span class="text-xs font-bold text-indigo-800 whitespace-nowrap">Antigravity</span>
                </div>
                <div class="flex items-center gap-2 px-3 sm:px-4 py-2 bg-gradient-to-r from-purple-100 to-purple-50 rounded-xl border border-purple-200 min-h-touch shadow-sm hover:shadow-md transition-all duration-200" title="LLM Technology">
                  <SparklesIcon class="w-4 h-4 text-purple-600 shrink-0" />
                  <span class="text-xs font-bold text-purple-800 whitespace-nowrap">Gemini</span>
                </div>
              </div>
            </div>
        </div>
        <div class="flex flex-col items-center gap-4 shrink-0">
          <div class="flex-shrink-0 relative">
            <div class="absolute inset-0 bg-gradient-to-r from-ipl-blue to-ipl-orange rounded-full blur-lg opacity-30 animate-pulse-slow"></div>
            <img 
              src="/bg-logo.png" 
              alt="Boundary Graph Logo" 
              class="w-36 h-36 object-contain relative z-10 drop-shadow-lg"
            />
          </div>
          <div class="px-6 py-3 bg-gradient-to-r from-ipl-blue to-ipl-orange text-white rounded-2xl text-xs font-black uppercase tracking-widest shadow-xl shadow-ipl-blue/25 relative overflow-hidden">
            <div class="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent animate-shimmer"></div>
            <span class="relative z-10">IPL 2008 - 2025</span>
          </div>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 xs:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 sm:gap-6 mb-8">
      <NuxtLink to="/h2h" class="stat-card bg-gradient-to-br from-ipl-blue/5 to-blue-100/50 border-ipl-blue/20 hover:border-ipl-blue/40 hover:from-ipl-blue/10 hover:to-blue-100 flex flex-col justify-between hover:scale-[1.02] transition-all duration-300 group min-h-[140px] shadow-lg hover:shadow-xl">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-600 mb-2 group-hover:text-ipl-blue transition-colors font-semibold">Total Matches</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-ipl-blue tracking-tight leading-none whitespace-nowrap">{{ overview.total_matches }}</p>
            </div>
          </div>
          <div class="p-3 bg-gradient-to-br from-ipl-blue/10 to-blue-100 rounded-xl shrink-0 group-hover:from-ipl-blue/20 group-hover:to-blue-200 transition-all duration-300">
             <CricketStadiumIcon class="w-7 h-7 sm:w-8 sm:h-8 text-ipl-blue" />
          </div>
        </div>
        <div class="h-1.5 w-12 bg-gradient-to-r from-ipl-blue to-blue-500 mt-4 rounded-full"></div>
      </NuxtLink>
      
      <NuxtLink to="/player-search" class="stat-card bg-gradient-to-br from-emerald-50 to-green-100/50 border-emerald-200/60 hover:border-emerald-300 hover:from-emerald-100 hover:to-green-100 flex flex-col justify-between hover:scale-[1.02] transition-all duration-300 group min-h-[140px] shadow-lg hover:shadow-xl">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-600 mb-2 group-hover:text-emerald-700 transition-colors font-semibold">Total Players</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-emerald-700 tracking-tight leading-none whitespace-nowrap">{{ overview.total_players }}</p>
            </div>
          </div>
          <div class="p-3 bg-gradient-to-br from-emerald-100 to-green-100 rounded-xl shrink-0 group-hover:from-emerald-200 group-hover:to-green-200 transition-all duration-300">
             <CricketHelmetIcon class="w-7 h-7 sm:w-8 sm:h-8 text-emerald-700" />
          </div>
        </div>
        <div class="h-1.5 w-12 bg-gradient-to-r from-emerald-500 to-green-500 mt-4 rounded-full"></div>
      </NuxtLink>
      
      <NuxtLink to="/teams" class="stat-card bg-gradient-to-br from-ipl-orange/10 to-orange-100/50 border-ipl-orange/30 hover:border-ipl-orange/50 hover:from-ipl-orange/20 hover:to-orange-100 flex flex-col justify-between hover:scale-[1.02] transition-all duration-300 group min-h-[140px] shadow-lg hover:shadow-xl">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-600 mb-2 group-hover:text-ipl-orange transition-colors font-semibold">Total Teams</h3>
            <div class="h-12 flex flex-col justify-center">
              <p class="text-2xl xl:text-3xl font-bold text-ipl-orange tracking-tight leading-none whitespace-nowrap">{{ overview.active_teams }} <span class="text-[10px] text-slate-500 font-medium leading-tight mt-0.5">({{ overview.defunct_teams }} defunct)</span></p>
            </div>
          </div>
          <div class="p-3 bg-gradient-to-br from-ipl-orange/10 to-orange-100 rounded-xl shrink-0 group-hover:from-ipl-orange/20 group-hover:to-orange-200 transition-all duration-300">
             <CricketJerseyIcon class="w-7 h-7 sm:w-8 sm:h-8 text-ipl-orange" />
          </div>
        </div>
        <div class="h-1.5 w-12 bg-gradient-to-r from-ipl-orange to-orange-500 mt-4 rounded-full"></div>
      </NuxtLink>

      <NuxtLink to="/batsmen" class="stat-card bg-gradient-to-br from-ipl-gold/10 to-yellow-100/50 border-ipl-gold/40 hover:border-ipl-gold/60 hover:from-ipl-gold/20 hover:to-yellow-100 flex flex-col justify-between hover:scale-[1.02] transition-all duration-300 group min-h-[140px] shadow-lg hover:shadow-xl">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-600 mb-2 group-hover:text-yellow-700 transition-colors font-semibold">Total Runs Scored</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-yellow-700 tracking-tight leading-none whitespace-nowrap text-ellipsis">{{ formatNumber(overview.total_runs) }}</p>
            </div>
          </div>
          <div class="p-3 bg-gradient-to-br from-ipl-gold/20 to-yellow-100 rounded-xl shrink-0 group-hover:from-ipl-gold/30 group-hover:to-yellow-200 transition-all duration-300">
             <CricketBatIcon class="w-7 h-7 sm:w-8 sm:h-8 text-yellow-700" />
          </div>
        </div>
        <div class="h-1.5 w-12 bg-gradient-to-r from-ipl-gold to-yellow-500 mt-4 rounded-full"></div>
      </NuxtLink>
      
      <NuxtLink to="/bowlers" class="stat-card bg-gradient-to-br from-red-50 to-red-100/50 border-red-200/60 hover:border-red-300 hover:from-red-100 hover:to-red-100 flex flex-col justify-between hover:scale-[1.02] transition-all duration-300 group min-h-[140px] shadow-lg hover:shadow-xl">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-600 mb-2 group-hover:text-red-700 transition-colors font-semibold">Total Deliveries</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-red-700 tracking-tight leading-none whitespace-nowrap text-ellipsis">{{ formatNumber(overview.total_deliveries) }}</p>
            </div>
          </div>
          <div class="p-3 bg-gradient-to-br from-red-100 to-red-100 rounded-xl shrink-0 group-hover:from-red-200 group-hover:to-red-200 transition-all duration-300">
             <CricketBallIcon class="w-7 h-7 sm:w-8 sm:h-8 text-red-700" />
          </div>
        </div>
        <div class="h-1.5 w-12 bg-gradient-to-r from-red-500 to-red-600 mt-4 rounded-full"></div>
      </NuxtLink>
      <NuxtLink to="/venues" class="stat-card bg-gradient-to-br from-ipl-purple/10 to-purple-100/50 border-ipl-purple/30 hover:border-ipl-purple/50 hover:from-ipl-purple/20 hover:to-purple-100 flex flex-col justify-between hover:scale-[1.02] transition-all duration-300 group min-h-[140px] shadow-lg hover:shadow-xl">
        <div class="flex justify-between items-start w-full gap-3">
          <div class="flex flex-col min-w-0 flex-1">
            <h3 class="text-label text-slate-600 mb-2 group-hover:text-ipl-purple transition-colors font-semibold">Total Venues</h3>
            <div class="h-12 flex items-center">
              <p class="text-2xl xl:text-3xl font-bold text-ipl-purple tracking-tight leading-none whitespace-nowrap">36+</p>
            </div>
          </div>
          <div class="p-3 bg-gradient-to-br from-ipl-purple/10 to-purple-100 rounded-xl shrink-0 group-hover:from-ipl-purple/20 group-hover:to-purple-200 transition-all duration-300">
             <MapPinIcon class="w-7 h-7 sm:w-8 sm:h-8 text-ipl-purple" />
          </div>
        </div>
        <div class="h-1.5 w-12 bg-gradient-to-r from-ipl-purple to-purple-500 mt-4 rounded-full"></div>
      </NuxtLink>
    </div>

    <!-- Seasons Breakdown -->
    <div class="stat-card mb-8 bg-gradient-to-br from-ipl-blue/5 to-purple-50 border-ipl-blue/20 shadow-lg">
      <div class="flex items-center gap-3 mb-6 border-b border-ipl-blue/20 pb-4">
        <div class="p-2 bg-gradient-to-br from-ipl-blue/10 to-purple-100 rounded-xl">
          <svg class="w-5 h-5 text-ipl-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
          </svg>
        </div>
        <h2 class="text-xl font-black text-ipl-blue">Season Analysis</h2>
      </div>
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
        <div 
          v-for="season in seasons" 
          :key="season.season" 
          @click="openSeasonModal(season)"
          class="bg-gradient-to-br from-white to-slate-50 rounded-xl p-4 text-center border border-ipl-blue/20 hover:from-ipl-blue/5 hover:to-purple-50 hover:shadow-lg hover:border-ipl-blue/40 hover:scale-105 transition-all duration-300 cursor-pointer group"
        >
          <p class="text-2xl text-ipl-blue font-black font-mono mb-2 group-hover:text-ipl-orange transition-colors">{{ season.season }}</p>
          <p class="text-xs font-semibold text-slate-600 uppercase tracking-wide">{{ season.matches }} Matches</p>
        </div>
      </div>
    </div>

    <!-- Active Teams -->
    <div class="stat-card mb-8 bg-gradient-to-br from-ipl-orange/5 to-yellow-50 border-ipl-orange/20 shadow-lg">
      <div class="flex items-center justify-between mb-6 border-b border-ipl-orange/20 pb-4">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-gradient-to-br from-ipl-orange/10 to-yellow-100 rounded-xl">
            <svg class="w-5 h-5 text-ipl-orange" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
            </svg>
          </div>
          <h2 class="text-xl font-black text-ipl-orange">Active Teams</h2>
        </div>
        <span class="text-xs font-bold text-ipl-orange/70 bg-ipl-orange/10 px-3 py-1 rounded-full uppercase tracking-widest">{{ activeTeams.length }} Teams</span>
      </div>
      <div class="flex flex-wrap gap-4 justify-center">
        <div 
          v-for="team in activeTeams" 
          :key="team.name" 
          @click="openTeamModal(team)"
          class="group bg-gradient-to-br from-white to-slate-50 border border-ipl-orange/20 rounded-2xl p-5 hover:from-ipl-orange/5 hover:to-yellow-50 hover:border-ipl-orange/40 hover:shadow-xl hover:scale-105 transition-all duration-300 cursor-pointer w-full sm:w-[calc(50%-0.5rem)] md:w-[calc(33.333%-0.67rem)] lg:w-[calc(25%-0.75rem)]"
        >
          <div class="flex flex-col items-center text-center space-y-3">
            <TeamLogo :teamName="team.name" size="2xl" :showName="false" />
            <div>
              <h3 class="font-bold text-slate-800 group-hover:text-ipl-orange transition-colors text-sm">{{ team.name }}</h3>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- Season Detail Modal -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-2xl w-full max-w-sm sm:max-w-lg md:max-w-2xl max-h-[90vh] overflow-y-auto animate-fade-in-up border border-ipl-blue/20">
        
        <!-- Header -->
        <div class="bg-gradient-to-r from-ipl-blue/10 to-purple-50 px-4 sm:px-6 py-4 sm:py-5 border-b border-ipl-blue/20 flex justify-between items-center sticky top-0 z-10">
          <div class="flex items-center gap-2 sm:gap-3 min-w-0">
            <div class="p-1.5 sm:p-2 bg-gradient-to-br from-ipl-blue/10 to-purple-100 rounded-lg sm:rounded-xl flex-shrink-0">
              <svg class="w-4 h-4 sm:w-5 sm:h-5 text-ipl-blue" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
            </div>
            <h3 class="text-lg sm:text-xl font-black text-ipl-blue truncate">IPL {{ selectedSeasonDetails?.season }} Season Details</h3>
          </div>
          <button @click="closeModal" class="text-slate-400 hover:text-ipl-orange transition-colors p-2 rounded-lg hover:bg-ipl-orange/10 flex-shrink-0 touch-manipulation">
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <!-- Content -->
        <div v-if="loadingDetails" class="p-4 sm:p-6 md:p-8 text-center text-slate-500">
           <div class="ipl-loader mx-auto mb-3 sm:mb-4"></div>
           <p class="text-ipl-blue font-semibold text-sm sm:text-base">Loading season stats...</p>
        </div>
        
        <div v-else-if="selectedSeasonDetails" class="p-3 sm:p-4 md:p-6">
          
          <!-- Winner Section -->
          <NuxtLink 
            v-if="selectedSeasonDetails.final_match_id"
            :to="'/match/' + selectedSeasonDetails.final_match_id"
            class="flex flex-col items-center justify-center mb-4 sm:mb-6 md:mb-8 bg-gradient-to-br from-ipl-gold/10 to-yellow-100 p-4 sm:p-5 md:p-6 rounded-xl sm:rounded-2xl border-2 border-ipl-gold/30 hover:scale-[1.02] hover:border-ipl-gold/50 transition-all duration-300 cursor-pointer group shadow-lg touch-manipulation"
          >
             <span class="text-xs font-bold text-slate-800 bg-ipl-gold/20 px-2 sm:px-3 py-1 rounded-full uppercase tracking-widest mb-2 sm:mb-3">🏆 Season Winner</span>
             <div class="flex items-center gap-2 sm:gap-3 md:gap-4 group-hover:scale-105 transition-transform duration-300">
               <TrophyIcon class="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 text-ipl-gold flex-shrink-0" />
               <TeamLogo :teamName="selectedSeasonDetails.winner" size="lg" :showName="false" />
               <h2 class="text-xl sm:text-2xl md:text-3xl font-black text-slate-800 group-hover:text-slate-900 transition-colors text-center">{{ selectedSeasonDetails.winner }}</h2>
             </div>
             <p class="text-xs sm:text-sm text-slate-600 mt-2 sm:mt-3 font-semibold text-center">Won by {{ selectedSeasonDetails.margin }} • <span class="text-ipl-orange">View Final Storyline →</span></p>
          </NuxtLink>

          <div v-else class="flex flex-col items-center justify-center mb-4 sm:mb-6 md:mb-8 bg-gradient-to-br from-ipl-gold/10 to-yellow-100 p-4 sm:p-5 md:p-6 rounded-xl sm:rounded-2xl border-2 border-ipl-gold/30 shadow-lg">
             <span class="text-xs font-bold text-slate-800 bg-ipl-gold/20 px-2 sm:px-3 py-1 rounded-full uppercase tracking-widest mb-2 sm:mb-3">🏆 Winner</span>
             <div class="flex items-center gap-2 sm:gap-3 md:gap-4">
               <TrophyIcon class="w-6 h-6 sm:w-8 sm:h-8 md:w-10 md:h-10 text-ipl-gold flex-shrink-0" />
               <TeamLogo :teamName="selectedSeasonDetails.winner" size="lg" :showName="false" />
               <h2 class="text-xl sm:text-2xl md:text-3xl font-black text-slate-800 text-center">{{ selectedSeasonDetails.winner }}</h2>
             </div>
             <p class="text-xs sm:text-sm text-slate-600 mt-2 sm:mt-3 font-semibold text-center">Won by {{ selectedSeasonDetails.margin }}</p>
          </div>

          <!-- Stats Grid -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4">
             <!-- Runner Up -->
             <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl sm:rounded-2xl border border-slate-200 min-h-[80px] sm:min-h-[100px] flex flex-col justify-center shadow-md hover:shadow-lg transition-shadow">
                <p class="text-xs text-ipl-blue font-bold mb-1 sm:mb-2 uppercase tracking-wide">🥈 Runner Up</p>
                <div class="flex items-center gap-2 sm:gap-3">
                  <TeamLogo :teamName="selectedSeasonDetails.runner_up" size="sm" :showName="false" />
                  <p class="text-sm sm:text-base md:text-lg font-black text-slate-800 leading-tight">{{ selectedSeasonDetails.runner_up }}</p>
                </div>
             </div>
             
             <!-- Venue -->
             <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-orange/5 to-orange-50 rounded-xl sm:rounded-2xl border border-ipl-orange/20 min-h-[80px] sm:min-h-[100px] flex flex-col justify-center shadow-md hover:shadow-lg transition-shadow">
                <p class="text-xs text-ipl-orange font-bold mb-1 sm:mb-2 uppercase tracking-wide">🏟️ Final Venue</p>
                <p class="text-sm sm:text-base md:text-lg font-black text-slate-800 leading-tight">{{ selectedSeasonDetails.venue }}</p>
             </div>
             
             <!-- Total Teams -->
             <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-blue/5 to-blue-50 rounded-xl sm:rounded-2xl border border-ipl-blue/20 flex items-center justify-between min-h-[80px] sm:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
                <div>
                  <p class="text-xs text-ipl-blue font-bold mb-1 sm:mb-2 uppercase tracking-wide">👥 Participating Teams</p>
                  <p class="text-xl sm:text-2xl font-black text-ipl-blue">{{ selectedSeasonDetails.total_teams }}</p>
                </div>
                <ShieldCheckIcon class="w-4 h-4 sm:w-5 sm:h-5 text-slate-300 flex-shrink-0" />
             </div>

             <!-- Total Matches -->
             <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-orange/5 to-orange-50 rounded-xl sm:rounded-2xl border border-ipl-orange/20 flex items-center justify-between min-h-[80px] sm:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
                <div>
                  <p class="text-xs text-ipl-orange font-bold mb-1 sm:mb-2 uppercase tracking-wide">🏏 Total Matches played</p>
                  <p class="text-xl sm:text-2xl font-black text-ipl-orange">{{ selectedSeasonDetails.total_matches }}</p>
                </div>
                 <CricketBallIcon class="w-4 h-4 sm:w-5 sm:h-5 text-slate-300 flex-shrink-0" />
             </div>
             
             <!-- Player of the Tournament -->
             <div v-if="selectedSeasonDetails.player_of_tournament" class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-yellow-100 to-yellow-200 rounded-xl sm:rounded-2xl border border-yellow-300/30 flex items-center justify-between min-h-[80px] sm:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
                <div class="min-w-0 pr-2">
                  <p class="text-xs text-yellow-800 font-bold mb-1 sm:mb-2 uppercase tracking-wide">🏆 Player of the Tournament</p>
                  <p class="text-sm sm:text-base md:text-lg font-black text-yellow-900 leading-tight truncate">{{ selectedSeasonDetails.player_of_tournament }}</p>
                </div>
                <CricketHelmetIcon class="w-4 h-4 sm:w-5 sm:h-5 text-slate-300 flex-shrink-0" />
             </div>
             
             <!-- Player of the Match (Final) -->
             <div v-if="selectedSeasonDetails.player_of_match" class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-green-100 to-emerald-100 rounded-xl sm:rounded-2xl border border-green-300/30 flex items-center justify-between min-h-[80px] sm:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
                <div class="min-w-0 pr-2">
                  <p class="text-xs text-green-800 font-bold mb-1 sm:mb-2 uppercase tracking-wide">🎯 Player of the Match (Final)</p>
                  <p class="text-sm sm:text-base md:text-lg font-black text-green-900 leading-tight truncate">{{ selectedSeasonDetails.player_of_match }}</p>
                </div>
                <TrophyIcon class="w-4 h-4 sm:w-5 sm:h-5 text-slate-300 flex-shrink-0" />
             </div>
          </div>
          
        </div>
      </div>
    </div>

    <!-- Team Detail Modal -->
    <div v-if="isTeamModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-2 sm:p-4 bg-slate-900/60 backdrop-blur-sm" @click.self="closeTeamModal">
      <div class="bg-white rounded-2xl sm:rounded-3xl shadow-2xl w-full max-w-sm sm:max-w-lg md:max-w-2xl max-h-[90vh] overflow-y-auto animate-fade-in-up border border-ipl-orange/20">
        
        <!-- Header -->
        <div class="bg-gradient-to-r from-ipl-orange/10 to-yellow-50 px-4 sm:px-6 py-4 sm:py-5 border-b border-ipl-orange/20 flex justify-between items-center sticky top-0 z-10">
          <div class="flex items-center gap-2 sm:gap-3 md:gap-4 min-w-0">
            <div class="p-1.5 sm:p-2 bg-gradient-to-br from-ipl-orange/10 to-yellow-100 rounded-lg sm:rounded-xl flex-shrink-0">
              <TeamLogo v-if="selectedTeam" :teamName="selectedTeam.name" size="sm" :showName="false" />
            </div>
            <h3 class="text-lg sm:text-xl font-black text-ipl-orange truncate">{{ selectedTeam?.name }}</h3>
          </div>
          <button @click="closeTeamModal" class="text-slate-400 hover:text-ipl-orange transition-colors p-2 rounded-lg hover:bg-ipl-orange/10 flex-shrink-0 touch-manipulation">
            <svg class="w-5 h-5 sm:w-6 sm:h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>

        <!-- Content -->
        <div v-if="loadingTeamDetails" class="p-4 sm:p-6 md:p-8 text-center text-slate-500">
           <div class="ipl-loader mx-auto mb-3 sm:mb-4"></div>
           <p class="text-ipl-orange font-semibold text-sm sm:text-base">Loading team stats...</p>
        </div>
        
        <div v-else-if="selectedTeamDetails" class="p-3 sm:p-4 md:p-6">
          
          <!-- Team Status -->
          <div class="mb-4 sm:mb-6 text-center p-3 sm:p-4 rounded-xl sm:rounded-2xl" :class="selectedTeam?.is_active ? 'bg-gradient-to-r from-green-50 to-emerald-50 border border-green-200' : 'bg-gradient-to-r from-red-50 to-pink-50 border border-red-200'">
            <div class="flex items-center justify-center gap-2 sm:gap-3 mb-2">
              <div :class="selectedTeam?.is_active ? 'w-3 h-3 sm:w-4 sm:h-4 bg-green-500 rounded-full animate-pulse' : 'w-3 h-3 sm:w-4 sm:h-4 bg-red-500 rounded-full'"></div>
              <span :class="selectedTeam?.is_active ? 'text-green-700 font-black text-base sm:text-lg' : 'text-red-700 font-black text-base sm:text-lg'">{{ selectedTeam?.is_active ? '✅ Active Team' : '❌ Inactive Team' }}</span>
            </div>
            <p class="text-xs sm:text-sm font-semibold" :class="selectedTeam?.is_active ? 'text-green-600' : 'text-red-600'">{{ selectedTeam?.is_active ? 'Currently participating in IPL' : 'No longer part of IPL' }}</p>
          </div>

          <!-- Team Details -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 mb-4 sm:mb-6">
            <!-- Captain -->
            <div v-if="selectedTeamDetails.captain" class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-blue/10 to-blue-100 rounded-xl sm:rounded-2xl border border-ipl-blue/30 shadow-md hover:shadow-lg transition-shadow">
              <div class="flex items-center justify-between">
                <div class="min-w-0 pr-2">
                  <p class="text-xs text-ipl-blue font-bold uppercase tracking-widest mb-1 sm:mb-2">👨‍✈️ Captain</p>
                  <p class="text-sm sm:text-base md:text-lg font-black text-slate-900 truncate">{{ selectedTeamDetails.captain }}</p>
                </div>
                <CricketHelmetIcon class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 text-ipl-blue flex-shrink-0" />
              </div>
            </div>
            
            <!-- Coach -->
            <div v-if="selectedTeamDetails.coach" class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-emerald-50 to-green-100 rounded-xl sm:rounded-2xl border border-emerald-300 shadow-md hover:shadow-lg transition-shadow">
              <div class="flex items-center justify-between">
                <div class="min-w-0 pr-2">
                  <p class="text-xs text-emerald-700 font-bold uppercase tracking-widest mb-1 sm:mb-2">🎯 Coach</p>
                  <p class="text-sm sm:text-base md:text-lg font-black text-slate-900 truncate">{{ selectedTeamDetails.coach }}</p>
                </div>
                <UserIcon class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 text-emerald-600 flex-shrink-0" />
              </div>
            </div>
            
            <!-- Home Ground -->
            <div v-if="selectedTeamDetails.home_ground" class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-orange/10 to-orange-100 rounded-xl sm:rounded-2xl border border-ipl-orange/30 shadow-md hover:shadow-lg transition-shadow">
              <div class="flex items-center justify-between">
                <div class="min-w-0 pr-2">
                  <p class="text-xs text-ipl-orange font-bold uppercase tracking-widest mb-1 sm:mb-2">🏟️ Home Ground</p>
                  <p class="text-sm sm:text-base md:text-lg font-black text-slate-900 truncate">{{ selectedTeamDetails.home_ground }}</p>
                </div>
                <CricketStadiumIcon class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 text-ipl-orange flex-shrink-0" />
              </div>
            </div>
            
            <!-- Owner -->
            <div v-if="selectedTeamDetails.owner" class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-purple/10 to-purple-100 rounded-xl sm:rounded-2xl border border-ipl-purple/30 shadow-md hover:shadow-lg transition-shadow">
              <div class="flex items-center justify-between">
                <div class="min-w-0 pr-2">
                  <p class="text-xs text-ipl-purple font-bold uppercase tracking-widest mb-1 sm:mb-2">👑 Owner</p>
                  <p class="text-sm sm:text-base md:text-lg font-black text-slate-900 truncate">{{ selectedTeamDetails.owner }}</p>
                </div>
                <ShieldCheckIcon class="w-6 h-6 sm:w-7 sm:h-7 md:w-8 md:h-8 text-ipl-purple flex-shrink-0" />
              </div>
            </div>
          </div>

          <!-- Quick Stats -->
          <div class="grid grid-cols-2 gap-2 sm:gap-3 md:gap-4 mb-4 sm:mb-6">
            <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-slate-100 to-slate-200 rounded-xl sm:rounded-2xl border border-slate-300/30 flex items-center justify-between min-h-[70px] sm:min-h-[80px] md:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
              <div>
                <p class="text-xs text-slate-700 font-bold mb-1 sm:mb-2 uppercase tracking-wide">📊 Total Matches</p>
                <p class="text-lg sm:text-xl md:text-2xl font-black text-slate-800">{{ selectedTeamDetails.total_matches || 'N/A' }}</p>
              </div>
            </div>
            <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-ipl-gold/10 to-yellow-200 rounded-xl sm:rounded-2xl border border-ipl-gold/30 flex items-center justify-between min-h-[70px] sm:min-h-[80px] md:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
              <div>
                <p class="text-xs text-yellow-800 font-bold mb-1 sm:mb-2 uppercase tracking-wide">🎯 Win Rate</p>
                <p class="text-lg sm:text-xl md:text-2xl font-black text-yellow-900">
                  {{ selectedTeamDetails.wins && selectedTeamDetails.total_matches ? 
                     Math.round((selectedTeamDetails.wins / selectedTeamDetails.total_matches) * 100) + '%' : 
                     'N/A' }}
                </p>
              </div>
            </div>
            <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-green-100 to-emerald-200 rounded-xl sm:rounded-2xl border border-green-300/30 flex items-center justify-between min-h-[70px] sm:min-h-[80px] md:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
              <div>
                <p class="text-xs text-green-800 font-bold mb-1 sm:mb-2 uppercase tracking-wide">✅ Wins</p>
                <p class="text-lg sm:text-xl md:text-2xl font-black text-green-900">{{ selectedTeamDetails.wins || 'N/A' }}</p>
              </div>
            </div>
            <div class="p-3 sm:p-4 md:p-5 bg-gradient-to-br from-red-100 to-pink-200 rounded-xl sm:rounded-2xl border border-red-300/30 flex items-center justify-between min-h-[70px] sm:min-h-[80px] md:min-h-[100px] shadow-md hover:shadow-lg transition-shadow">
              <div>
                <p class="text-xs text-red-800 font-bold mb-1 sm:mb-2 uppercase tracking-wide">❌ Losses</p>
                <p class="text-lg sm:text-xl md:text-2xl font-black text-red-900">{{ selectedTeamDetails.losses || 'N/A' }}</p>
              </div>
            </div>
          </div>

          <!-- Action Button -->
          <div class="text-center">
            <button 
              @click="goToTeamsPage"
              class="w-full bg-gradient-to-r from-ipl-orange to-orange-500 hover:from-orange-500 hover:to-ipl-orange text-white font-black py-3 sm:py-4 px-4 sm:px-8 rounded-xl sm:rounded-2xl transition-all duration-300 flex items-center justify-center gap-2 sm:gap-3 shadow-lg hover:shadow-xl transform hover:scale-105 touch-manipulation text-sm sm:text-base"
            >
              <span>🏏 Know More About This Team</span>
              <svg class="w-4 h-4 sm:w-5 sm:h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path></svg>
            </button>
          </div>
          
        </div>
      </div>
    </div>

    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'
import CricketJerseyIcon from '~/components/icons/CricketJerseyIcon.vue'
import CricketStadiumIcon from '~/components/icons/CricketStadiumIcon.vue'
import CricketBatIcon from '~/components/icons/CricketBatIcon.vue'
import TeamLogo from '~/components/TeamLogo.vue'
import { 
  TrophyIcon, 
  ShieldCheckIcon, 
  UserIcon, 
  CircleStackIcon, 
  SparklesIcon, 
  BoltIcon,
  CpuChipIcon,
  MapPinIcon
} from '@heroicons/vue/24/outline'

const config = useRuntimeConfig()
const overview = ref<any>({
  total_matches: 0,
  total_players: 0,
  total_runs: 0,
  active_teams: 0,
  defunct_teams: 0,
  total_deliveries: 0
})
const seasons = ref<any[]>([])
const allTeams = ref<any[]>([])

// Modal State
const isModalOpen = ref(false)
const loadingDetails = ref(false)
const selectedSeasonDetails = ref<any>(null)

// Team Modal State
const isTeamModalOpen = ref(false)
const loadingTeamDetails = ref(false)
const selectedTeam = ref<any>(null)
const selectedTeamDetails = ref<any>(null)

// Computed properties
const activeTeams = computed(() => allTeams.value.filter(t => t.is_active))

const formatNumber = (num: number) => {
  if (!num) return 0
  
  // For very large numbers, use abbreviations
  if (num >= 1000000000) {
    return (num / 1000000000).toFixed(1).replace(/\.0$/, '') + 'B'
  }
  if (num >= 1000000) {
    return (num / 1000000).toFixed(1).replace(/\.0$/, '') + 'M'
  }
  if (num >= 1000) {
    return (num / 1000).toFixed(1).replace(/\.0$/, '') + 'K'
  }
  
  return num.toLocaleString('en-IN')
}

const openSeasonModal = async (season: any) => {
  isModalOpen.value = true
  loadingDetails.value = true
  selectedSeasonDetails.value = { season: season.season } // Initial placeholder
  
  try {
     const details = await $fetch(`${config.public.apiBase}/api/seasons/${season.season}`)
     selectedSeasonDetails.value = details
  } catch (e) {
     console.error("Error fetching season details", e)
  } finally {
     loadingDetails.value = false
  }
}

const closeModal = () => {
  isModalOpen.value = false
  selectedSeasonDetails.value = null
}

const openTeamModal = async (team: any) => {
  isTeamModalOpen.value = true
  loadingTeamDetails.value = true
  selectedTeam.value = team
  selectedTeamDetails.value = null
  
  try {
    // Get team stats from API
    const stats = await $fetch(`${config.public.apiBase}/api/team/${encodeURIComponent(team.name)}/stats`)
    console.log('Raw API stats response:', stats) // Debug: see actual API response
    
    // Get team details from utility function (same as teams page)
    const { getTeamDetails } = await import('~/utils/teamLogos')
    const teamInfo = getTeamDetails(team.name)
    
    // Map the utility function properties to match our template
    const mappedTeamInfo = teamInfo ? {
      captain: teamInfo.captain,
      coach: teamInfo.coach,
      home_ground: teamInfo.venue, // venue -> home_ground
      owner: teamInfo.owner // Use owner from teamInfo
    } : {}
    
    // Type-safe handling of stats
    const safeStats = stats && typeof stats === 'object' ? stats as any : {}
    
    // Combine stats with team information
    selectedTeamDetails.value = {
      ...safeStats,
      ...mappedTeamInfo,
      name: team.name,
      is_active: team.is_active,
      // Calculate losses since API doesn't provide it
      losses: safeStats.total_matches && safeStats.wins ? safeStats.total_matches - safeStats.wins : 'N/A'
    }
    console.log('Final team details:', selectedTeamDetails.value) // Debug log
  } catch (e) {
    console.error("Error fetching team details", e)
    // Set minimal details when API fails - no fake stats
    selectedTeamDetails.value = {
      name: team.name,
      is_active: team.is_active,
      total_matches: 'N/A',
      wins: 'N/A',
      losses: 'N/A',
      win_percentage: 'N/A'
    }
  } finally {
    loadingTeamDetails.value = false
  }
}

const closeTeamModal = () => {
  isTeamModalOpen.value = false
  selectedTeam.value = null
  selectedTeamDetails.value = null
}

const goToTeamsPage = () => {
  const teamName = selectedTeam.value?.name
  console.log('Navigating with team:', teamName)
  closeTeamModal()
  if (teamName) {
    const encodedName = encodeURIComponent(teamName)
    const url = `/teams?team=${encodedName}`
    console.log('Navigation URL:', url)
    navigateTo(url)
  } else {
    navigateTo('/teams')
  }
}

const onKeydown = (e: KeyboardEvent) => {
  if (e.key === 'Escape') {
    if (isTeamModalOpen.value) {
      closeTeamModal()
    } else if (isModalOpen.value) {
      closeModal()
    }
  }
}

onMounted(async () => {
  window.addEventListener('keydown', onKeydown)
  
  try {
    const overviewRes = await $fetch(`${config.public.apiBase}/api/overview`)
    overview.value = overviewRes
  } catch (error) {
    console.error('Failed to fetch overview:', error)
  }
  
  try {
    const seasonsRes = await $fetch(`${config.public.apiBase}/api/seasons`)
    seasons.value = Array.isArray(seasonsRes) ? seasonsRes : []
  } catch (error) {
    console.error('Failed to fetch seasons:', error)
    seasons.value = []
  }

  try {
    const teamsRes = await $fetch(`${config.public.apiBase}/api/teams`)
    allTeams.value = Array.isArray(teamsRes) ? teamsRes : []
  } catch (error) {
    console.error('Failed to fetch teams:', error)
    allTeams.value = []
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', onKeydown)
})
</script>
