<template>
  <div class="container mx-auto px-4 py-8">
    <div class="space-y-8 animate-in fade-in duration-500 pb-4">
    <!-- Page Header -->
    <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8">
      <div class="space-y-2">
        <div class="inline-flex items-center gap-2 px-3 py-1 bg-ipl-blue/15 text-ipl-blue rounded-full text-xs font-bold uppercase tracking-widest border border-ipl-blue/20">
          <MagnifyingGlassIcon class="w-3 h-3" />
          Player Intelligence
        </div>
        <h1 class="text-4xl font-black text-slate-900 tracking-tight">The <span class="bg-gradient-to-r from-ipl-blue to-purple-600 bg-clip-text text-transparent">Search Engine</span></h1>
        <p class="text-slate-500 max-w-xl">
            Deep dive into individual player careers with comprehensive analytics. Search any player to unlock batting and bowling insights.
        </p>
      </div>
    </div>

    <!-- Search Section -->
    <div class="relative max-w-2xl">
      <div class="bg-white p-2 rounded-2xl border border-slate-200 shadow-sm focus-within:ring-4 focus-within:ring-ipl-blue/10 focus-within:border-ipl-blue transition-all flex items-center gap-3">
        <div class="pl-3 text-slate-400">
          <MagnifyingGlassIcon class="w-5 h-5" />
        </div>
        <input 
          v-model="searchQuery"
          type="text"
          placeholder="Ex: V Kohli, MS Dhoni, Rashid Khan..."
          class="flex-1 bg-transparent py-3 pr-4 outline-none text-slate-900 font-medium placeholder:text-slate-400"
          @input="searchPlayers"
          @keydown="handleKeydown"
        />
        <div v-if="searchQuery" @click="clearSearch" class="pr-3 text-slate-400 hover:text-slate-600 cursor-pointer">
          <XMarkIcon class="w-5 h-5" />
        </div>
      </div>
      
      <!-- Autocomplete Dropdown -->
      <transition 
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
        <div v-if="showResults && searchResults.length > 0" class="absolute z-50 mt-3 w-full bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden backdrop-blur-sm bg-white/95">
          <div class="py-2">
            <button 
              v-for="(player, index) in searchResults" 
              :key="player"
              @click="selectPlayer(player)"
              :class="[
                'w-full text-left px-5 py-3.5 flex items-center gap-3 transition-colors group',
                highlightedIndex === index ? 'bg-slate-100' : 'hover:bg-slate-50'
              ]"
            >
              <div :class="[
                'w-8 h-8 rounded-full flex items-center justify-center transition-colors',
                highlightedIndex === index ? 'bg-brand-primary/10 text-brand-primary' : 'bg-slate-100 text-slate-500 group-hover:bg-brand-primary/10 group-hover:text-brand-primary'
              ]">
                <UserIcon class="w-4 h-4" />
              </div>
              <span class="font-semibold text-slate-700 group-hover:text-slate-900">{{ player }}</span>
            </button>
          </div>
        </div>
      </transition>
    </div>

    <!-- Stats Display -->
    <div v-if="playerStats" class="space-y-6">
      <!-- Player Header Card -->
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div class="flex items-start gap-6">
          <div class="w-16 h-16 rounded-full bg-slate-900 flex items-center justify-center text-white text-2xl font-bold shadow-lg shadow-slate-200">
            {{ searchQuery.charAt(0) }}
          </div>
          <div class="flex-1">
            <h2 class="text-3xl font-bold text-slate-900 tracking-tight">{{ searchQuery }}</h2>
            
            <!-- Player Type and Career Stats -->
            <div class="flex flex-wrap gap-3 mt-3 mb-4">
              <span class="px-2.5 py-1 bg-green-50 text-green-700 rounded-md text-xs font-bold uppercase tracking-wider border border-green-100">Pro Athlete</span>
              <span class="px-2.5 py-1 bg-slate-100 text-slate-600 rounded-md text-xs font-bold uppercase tracking-wider border border-slate-200 italic">
                {{ (playerStats.battingStats?.totalRuns > 0 && playerStats.bowlingStats?.totalWickets > 0) ? 'All Rounder' : 
                     (playerStats.battingStats?.totalRuns > 0 ? 'Batsman' : 'Bowler') }}
              </span>
              <span v-if="consolidatedTeamInfo?.totalTeams" class="px-2.5 py-1 bg-blue-50 text-blue-700 rounded-md text-xs font-bold uppercase tracking-wider border border-blue-100">
                {{ consolidatedTeamInfo.totalTeams }} {{ consolidatedTeamInfo.totalTeams === 1 ? 'Team' : 'Teams' }}
              </span>
            </div>

            <!-- Team Information -->
            <div v-if="consolidatedTeamInfo" class="space-y-3">
              <!-- Debut Team -->
              <div v-if="consolidatedTeamInfo.debutTeam" class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider w-16">Debut:</span>
                <div class="flex items-center gap-2 px-3 py-1.5 bg-blue-50 text-blue-700 rounded-lg border border-blue-100">
                  <TeamLogo :teamName="consolidatedTeamInfo.debutTeam" size="sm" :showName="false" />
                  <span class="text-sm font-semibold">{{ consolidatedTeamInfo.debutTeam }}</span>
                </div>
              </div>

              <!-- Latest Team -->
              <div v-if="consolidatedTeamInfo.latestTeam" class="flex items-center gap-2">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider w-16">Current:</span>
                <div class="flex items-center gap-2 px-3 py-1.5 bg-purple-50 text-purple-700 rounded-lg border border-purple-100">
                  <TeamLogo :teamName="consolidatedTeamInfo.latestTeam" size="sm" :showName="false" />
                  <span class="text-sm font-semibold">{{ consolidatedTeamInfo.latestTeam }}</span>
                </div>
              </div>

              <!-- Other Teams -->
              <div v-if="consolidatedTeamInfo.otherTeams && consolidatedTeamInfo.otherTeams.length > 0" class="flex items-start gap-2">
                <span class="text-xs font-bold text-slate-400 uppercase tracking-wider w-16 mt-1">Other:</span>
                <div class="flex flex-wrap gap-2">
                  <div 
                    v-for="team in consolidatedTeamInfo.otherTeams" 
                    :key="team"
                    class="flex items-center gap-1.5 px-2.5 py-1 bg-slate-50 text-slate-700 rounded-md border border-slate-200"
                  >
                    <TeamLogo :teamName="team" size="sm" :showName="false" />
                    <span class="text-xs font-medium">{{ team }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Batting Analytics -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <CricketHelmetIcon class="w-5 h-5 text-ipl-blue" />
              <h3 class="font-bold text-slate-800">Batting Analytics</h3>              <div v-if="loadingStats" class="animate-spin h-4 w-4 border-2 border-indigo-500 border-t-transparent rounded-full"></div>            </div>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Career Profile</span>
          </div>
          <div class="p-6 grid grid-cols-2 gap-4 flex-grow">
            <template v-if="loadingStats">
              <div v-for="n in 8" :key="n" class="p-4 bg-slate-50 rounded-xl border border-slate-100 animate-pulse">
                <div class="h-3 bg-slate-200 rounded w-16 mb-2"></div>
                <div class="h-6 bg-slate-300 rounded w-12"></div>
              </div>
            </template>
            <template v-else>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Total Runs</p>
                <p class="text-2xl font-black text-slate-900">{{ playerStats.battingStats?.totalRuns || 0 }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Strike Rate</p>
                <p class="text-2xl font-black text-ipl-blue">{{ playerStats.battingStats?.strikeRate || '0.00' }}<span class="text-sm font-medium ml-0.5">%</span></p>
              </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Average</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.average || '0.00' }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Highest Score</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.highestScore || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Fours (4s)</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.fours || 0 }}</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
              <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Sixes (6s)</p>
              <p class="text-2xl font-black text-slate-800">{{ playerStats.battingStats?.sixes || 0 }}</p>
            </div>
            
            <!-- Boundary Trend Sparkline -->
            <div v-if="Object.keys(playerStats?.seasonWiseStats || {}).length > 1" class="col-span-1 md:col-span-2 p-4 bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl border border-blue-100">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-3 gap-2">
                <div>
                  <p class="text-xs text-blue-700 font-bold uppercase tracking-wide mb-1">Boundary Rate Trend</p>
                  <p class="text-sm text-blue-600">Season-wise boundaries per ball</p>
                </div>
                <div class="text-blue-500 self-start">
                  <ChartBarIcon class="w-5 h-5" />
                </div>
              </div>
              <BoundarySparkline 
                :seasonData="playerStats.seasonWiseStats"
                type="boundary"
                :width="240"
                :height="50"
                primaryColor="#1d4ed8"
                backgroundColor="transparent"
                class="w-full"
              />
            </div>
            
            <div class="col-span-2 p-4 bg-ipl-blue rounded-xl flex justify-between items-center text-white shadow-md shadow-blue-100">
               <div>
                 <p class="text-[10px] font-bold uppercase tracking-widest opacity-80 mb-0.5">Innings Played</p>
                 <p class="text-xl font-black">{{ playerStats.battingStats?.innings || 0 }}</p>
               </div>
               <PresentationChartLineIcon class="w-8 h-8 opacity-20" />
            </div>
            </template>
          </div>
        </div>

        <!-- Bowling Analytics -->
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden flex flex-col">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <CricketBallIcon class="w-5 h-5 text-purple-600" />
              <h3 class="font-bold text-slate-800">Bowling Analytics</h3>
              <div v-if="loadingStats" class="animate-spin h-4 w-4 border-2 border-rose-500 border-t-transparent rounded-full"></div>
            </div>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Career Profile</span>
          </div>
          <div class="p-6 grid grid-cols-2 gap-4 flex-grow">
            <template v-if="loadingStats">
              <div v-for="n in 4" :key="n" class="p-4 bg-slate-50 rounded-xl border border-slate-100 animate-pulse">
                <div class="h-3 bg-slate-200 rounded w-16 mb-2"></div>
                <div class="h-6 bg-slate-300 rounded w-12"></div>
              </div>
            </template>
            <template v-else>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Total Wickets</p>
                <p class="text-2xl font-black text-slate-900">{{ playerStats.bowlingStats?.totalWickets || 0 }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Economy Rate</p>
                <p class="text-2xl font-black text-purple-600">{{ playerStats.bowlingStats?.economyRate ?? 'N/A' }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Bowling Average</p>
                <p class="text-2xl font-black text-slate-800">{{ playerStats.bowlingStats?.average ?? 'N/A' }}</p>
              </div>
              <div class="p-4 bg-slate-50 rounded-xl border border-slate-100">
                <p class="text-xs text-slate-400 font-bold uppercase tracking-wide mb-1">Runs Conceded</p>
                <p class="text-2xl font-black text-slate-800">{{ playerStats.bowlingStats?.runsConceded || 0 }}</p>
              </div>
              
              <!-- Bowling Economy Trend Sparkline -->
              <div v-if="Object.keys(playerStats?.seasonWiseStats || {}).length > 1 && Object.values(playerStats?.seasonWiseStats || {}).some((s: any) => s.bowling?.balls > 0)" class="col-span-1 md:col-span-2 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl border border-purple-100">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-3 gap-2">
                  <div>
                    <p class="text-xs text-purple-700 font-bold uppercase tracking-wide mb-1">Economy Rate Trend</p>
                    <p class="text-sm text-purple-600">Season-wise runs per over</p>
                  </div>
                  <div class="text-purple-500 self-start">
                    <ChartBarIcon class="w-5 h-5" />
                  </div>
                </div>
                <BoundarySparkline 
                  :seasonData="playerStats.seasonWiseStats"
                  type="economy"
                  :width="240"
                  :height="50"
                  primaryColor="#9333ea"
                  backgroundColor="transparent"
                  class="w-full"
                />
              </div>
              
              <!-- Wickets Per Innings Trend (for all-rounders) -->
              <div v-if="Object.keys(playerStats?.seasonWiseStats || {}).length > 1 && Object.values(playerStats?.seasonWiseStats || {}).some((s: any) => s.bowling?.wickets > 0 && s.bowling?.innings > 0)" class="col-span-1 md:col-span-2 p-4 bg-gradient-to-r from-indigo-50 to-purple-50 rounded-xl border border-indigo-200">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between mb-3 gap-2">
                  <div>
                    <p class="text-xs text-indigo-700 font-bold uppercase tracking-wide mb-1">Wickets Trend</p>
                    <p class="text-sm text-indigo-600">Season-wise wickets per innings</p>
                  </div>
                  <div class="text-indigo-500 self-start">
                    <ChartBarIcon class="w-5 h-5" />
                  </div>
                </div>
                <BoundarySparkline 
                  :seasonData="playerStats.seasonWiseStats"
                  type="wickets"
                  :width="240"
                  :height="50"
                  primaryColor="#6366f1"
                  backgroundColor="transparent"
                  class="w-full"
                />
              </div>
              
              <div class="col-span-2 p-4 bg-purple-600 rounded-xl flex justify-between items-center text-white shadow-md shadow-purple-100">
                 <div>
                   <p class="text-[10px] font-bold uppercase tracking-widest opacity-80 mb-0.5">Bowling Innings</p>
                   <p class="text-xl font-black">{{ playerStats.bowlingStats?.innings || 0 }}</p>
                 </div>
                 <FireIcon class="w-8 h-8 opacity-20" />
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- Season-wise Performance -->
      <div v-if="loadingStats || Object.keys(playerStats?.seasonWiseStats || {}).length > 0" class="col-span-1 lg:col-span-2">
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
          <div class="px-6 py-4 border-b border-slate-100 bg-slate-50/50 flex justify-between items-center">
            <div class="flex items-center gap-2">
              <PresentationChartLineIcon class="w-5 h-5 text-ipl-blue" />
              <h3 class="font-bold text-slate-800">Season-wise Performance</h3>
              <div v-if="loadingStats" class="animate-spin h-4 w-4 border-2 border-purple-500 border-t-transparent rounded-full"></div>
            </div>
            <span class="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Career Timeline</span>
          </div>
          <div v-if="loadingStats" class="p-6 space-y-4">
            <!-- Loading skeleton for season-wise stats -->
            <div class="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg p-4 mb-6 border border-purple-100 animate-pulse">
              <div class="h-4 bg-purple-200 rounded w-48 mb-3"></div>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div class="h-20 bg-white rounded-lg border"></div>
                <div class="h-20 bg-white rounded-lg border"></div>
              </div>
            </div>
            <div class="space-y-3">
              <div v-for="n in 3" :key="n" class="bg-slate-50 rounded-lg p-4 animate-pulse">
                <div class="h-5 bg-slate-200 rounded w-24 mb-3"></div>
                <div class="grid grid-cols-3 gap-4">
                  <div class="h-16 bg-slate-200 rounded"></div>
                  <div class="h-16 bg-slate-200 rounded"></div>
                  <div class="h-16 bg-slate-200 rounded"></div>
                </div>
              </div>
            </div>
          </div>
          <div v-else class="p-6 space-y-4">
            <!-- Performance Trend Overview -->
            <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-lg p-4 mb-6 border border-blue-100">
              <h4 class="font-semibold text-ipl-blue mb-3 flex items-center gap-2">
                <PresentationChartLineIcon class="w-4 h-4" />
                Performance Trajectory Analysis
              </h4>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div v-if="Object.values(playerStats.seasonWiseStats).some((s: any) => s.batting?.runs > 0)" class="text-center p-3 bg-white rounded-lg border border-blue-100">
                  <div class="flex items-center justify-center gap-2 mb-1">
                    <CricketHelmetIcon class="w-4 h-4 text-ipl-blue" />
                    <span class="text-sm font-medium text-slate-600">Batting Trend</span>
                  </div>
                  <div class="flex items-center justify-center gap-2">
                    <span class="text-2xl" :class="{
                      'text-green-600': calculateBattingTrend(playerStats.seasonWiseStats).color === 'green',
                      'text-red-600': calculateBattingTrend(playerStats.seasonWiseStats).color === 'red',
                      'text-slate-600': calculateBattingTrend(playerStats.seasonWiseStats).color === 'slate'
                    }">
                      {{ calculateBattingTrend(playerStats.seasonWiseStats).icon }}
                    </span>
                    <div>
                      <p class="font-bold text-lg" :class="{
                        'text-green-700': calculateBattingTrend(playerStats.seasonWiseStats).color === 'green',
                        'text-red-700': calculateBattingTrend(playerStats.seasonWiseStats).color === 'red',
                        'text-slate-700': calculateBattingTrend(playerStats.seasonWiseStats).color === 'slate'
                      }">
                        {{ calculateBattingTrend(playerStats.seasonWiseStats).trend.toUpperCase() }}
                      </p>
                      <p class="text-xs text-slate-500" v-if="calculateBattingTrend(playerStats.seasonWiseStats).change !== 0">
                        {{ calculateBattingTrend(playerStats.seasonWiseStats).change }}% vs recent
                      </p>
                    </div>
                  </div>
                </div>
                
                <div v-if="Object.values(playerStats.seasonWiseStats).some((s: any) => s.bowling?.wickets > 0)" class="text-center p-3 bg-white rounded-lg border border-purple-100">
                  <div class="flex items-center justify-center gap-2 mb-1">
                    <CricketBallIcon class="w-4 h-4 text-purple-600" />
                    <span class="text-sm font-medium text-slate-600">Bowling Trend</span>
                  </div>
                  <div class="flex items-center justify-center gap-2">
                    <span class="text-2xl" :class="{
                      'text-green-600': calculateBowlingTrend(playerStats.seasonWiseStats).color === 'green',
                      'text-red-600': calculateBowlingTrend(playerStats.seasonWiseStats).color === 'red',
                      'text-slate-600': calculateBowlingTrend(playerStats.seasonWiseStats).color === 'slate'
                    }">
                      {{ calculateBowlingTrend(playerStats.seasonWiseStats).icon }}
                    </span>
                    <div>
                      <p class="font-bold text-lg" :class="{
                        'text-green-700': calculateBowlingTrend(playerStats.seasonWiseStats).color === 'green',
                        'text-red-700': calculateBowlingTrend(playerStats.seasonWiseStats).color === 'red',
                        'text-slate-700': calculateBowlingTrend(playerStats.seasonWiseStats).color === 'slate'
                      }">
                        {{ calculateBowlingTrend(playerStats.seasonWiseStats).trend.toUpperCase() }}
                      </p>
                      <p class="text-xs text-slate-500" v-if="calculateBowlingTrend(playerStats.seasonWiseStats).change !== 0">
                        {{ calculateBowlingTrend(playerStats.seasonWiseStats).change }}% improvement
                      </p>
                    </div>
                  </div>
                </div>
                
                <div v-if="Object.values(playerStats.seasonWiseStats).some((s: any) => s.batting?.fours > 0 || s.batting?.sixes > 0)" class="text-center p-3 bg-white rounded-lg border border-indigo-100">
                  <div class="flex items-center justify-center gap-2 mb-1">
                    <ChartBarIcon class="w-4 h-4 text-indigo-600" />
                    <span class="text-sm font-medium text-slate-600">Boundary Rate</span>
                  </div>
                  <div class="flex items-center justify-center gap-2">
                    <span class="text-2xl" :class="{
                      'text-green-600': calculateBoundaryTrend(playerStats.seasonWiseStats).color === 'green',
                      'text-red-600': calculateBoundaryTrend(playerStats.seasonWiseStats).color === 'red',
                      'text-slate-600': calculateBoundaryTrend(playerStats.seasonWiseStats).color === 'slate'
                    }">
                      {{ calculateBoundaryTrend(playerStats.seasonWiseStats).icon }}
                    </span>
                    <div>
                      <p class="font-bold text-lg" :class="{
                        'text-green-700': calculateBoundaryTrend(playerStats.seasonWiseStats).color === 'green',
                        'text-red-700': calculateBoundaryTrend(playerStats.seasonWiseStats).color === 'red',
                        'text-slate-700': calculateBoundaryTrend(playerStats.seasonWiseStats).color === 'slate'
                      }">
                        {{ calculateBoundaryTrend(playerStats.seasonWiseStats).trend.toUpperCase() }}
                      </p>
                      <p class="text-xs text-slate-500" v-if="calculateBoundaryTrend(playerStats.seasonWiseStats).rate > 0">
                        {{ calculateBoundaryTrend(playerStats.seasonWiseStats).rate.toFixed(1) }}% rate
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <div v-for="(stats, season, index) in playerStats.seasonWiseStats" :key="season" class="border border-slate-200 rounded-lg overflow-hidden">
              <div class="bg-slate-50 px-4 py-3 border-b border-slate-200 flex items-center justify-between">
                <div class="flex items-center gap-3">
                  <span class="font-bold text-slate-800 text-lg">{{ season }}</span>
                  <span v-if="stats.team" class="px-2 py-1 bg-indigo-100 text-indigo-800 rounded text-xs font-bold">{{ stats.team }}</span>
                  
                  <!-- Year-over-Year Comparison Badge -->
                  <div v-if="index > 0" class="flex gap-2">
                    <div v-if="stats.batting?.runs > 0 && getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'batting')" 
                         class="px-2 py-1 rounded text-xs font-bold flex items-center gap-1"
                         :class="{
                           'bg-green-100 text-green-800': getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'batting')?.trend === 'up',
                           'bg-red-100 text-red-800': getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'batting')?.trend === 'down'
                         }">
                      <span class="text-xs">🏏</span>
                      <span>{{ getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'batting')?.average }}</span>
                    </div>
                    <div v-if="stats.bowling?.wickets > 0 && getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'bowling')" 
                         class="px-2 py-1 rounded text-xs font-bold flex items-center gap-1"
                         :class="{
                           'bg-green-100 text-green-800': getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'bowling')?.trend === 'up',
                           'bg-red-100 text-red-800': getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'bowling')?.trend === 'down'
                         }">
                      <span class="text-xs">⚾</span>
                      <span>{{ getSeasonComparison(stats, Object.values(playerStats.seasonWiseStats)[index-1], 'bowling')?.economy }}</span>
                    </div>
                  </div>
                </div>
              </div>
              <div class="p-4">
                <!-- Batting Performance -->
                <div v-if="stats.batting?.runs > 0" class="mb-4">
                  <h4 class="text-sm font-semibold text-indigo-600 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <CricketHelmetIcon class="w-4 h-4" />
                    Batting Performance
                  </h4>
                  <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                    <div class="text-center p-3 bg-indigo-50 rounded-lg">
                      <p class="text-lg font-bold text-indigo-800">{{ stats.batting.runs }}</p>
                      <p class="text-xs text-indigo-600 font-medium">Runs</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.batting.average }}</p>
                      <p class="text-xs text-slate-600 font-medium">Average</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.batting.strikeRate }}</p>
                      <p class="text-xs text-slate-600 font-medium">SR</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.batting.highest }}</p>
                      <p class="text-xs text-slate-600 font-medium">Highest</p>
                    </div>
                    <div class="text-center p-3 bg-green-50 rounded-lg">
                      <p class="text-lg font-bold text-green-800">{{ stats.batting.centuries }}</p>
                      <p class="text-xs text-green-600 font-medium">100s</p>
                    </div>
                    <div class="text-center p-3 bg-yellow-50 rounded-lg">
                      <p class="text-lg font-bold text-yellow-800">{{ stats.batting.fifties }}</p>
                      <p class="text-xs text-yellow-600 font-medium">50s</p>
                    </div>
                  </div>
                </div>
                
                <!-- Bowling Performance -->
                <div v-if="stats.bowling && (stats.bowling.wickets >= 0 || stats.bowling.runs >= 0 || stats.bowling.innings > 0)">
                  <h4 class="text-sm font-semibold text-rose-600 uppercase tracking-wider mb-3 flex items-center gap-2">
                    <CricketBallIcon class="w-4 h-4" />
                    Bowling Performance
                  </h4>
                  <div class="grid grid-cols-2 md:grid-cols-5 gap-3">
                    <div class="text-center p-3 bg-rose-50 rounded-lg">
                      <p class="text-lg font-bold text-rose-800">{{ stats.bowling.wickets }}</p>
                      <p class="text-xs text-rose-600 font-medium">Wickets</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.average ?? 'N/A' }}</p>
                      <p class="text-xs text-slate-600 font-medium">Average</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.economy ?? 'N/A' }}</p>
                      <p class="text-xs text-slate-600 font-medium">Economy</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.runs }}</p>
                      <p class="text-xs text-slate-600 font-medium">Runs</p>
                    </div>
                    <div class="text-center p-3 bg-slate-50 rounded-lg">
                      <p class="text-lg font-bold text-slate-800">{{ stats.bowling.bestBowling }}</p>
                      <p class="text-xs text-slate-600 font-medium">Best</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Graph View Expansion -->
      <!-- <div class="bg-white rounded-3xl border border-slate-100 shadow-sm overflow-hidden">
        <div class="p-6 pb-4 border-b border-slate-100/60 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
          <div class="flex flex-col">
            <h2 class="text-xl font-black text-slate-900">Graph Visualization</h2>
            <p class="text-slate-500 text-sm font-medium">Interactive relationship explorer for {{ searchQuery }}</p>
          </div>
        </div>
        
        <div class="p-6">
          <GraphVisualization 
            :playerName="searchQuery" 
            :rivals="playerRivals" 
            :loading="loadingRivals"
            @select-rival="selectPlayer"
          />
          <div class="mt-4 p-4 bg-slate-50 rounded-xl flex items-start gap-3">
             <div class="p-2 bg-indigo-50 text-indigo-600 rounded-lg">
                <InformationCircleIcon class="w-4 h-4" />
             </div>
             <p class="text-[11px] text-slate-500 leading-relaxed font-medium mt-0.5">
               This <strong class="text-slate-900">interactive graph</strong> shows player connections and relationships. <strong class="text-indigo-600">Click</strong> nodes to view player stats. <strong class="text-indigo-600">Drag</strong> any node to move it around and explore the network layout.
             </p>
          </div>
        </div>
      </div> -->
    </div>

    <!-- Loading State -->
    <div v-else-if="loadingStats" class="space-y-6">
      <div class="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm animate-pulse">
        <div class="flex items-start gap-6">
          <div class="w-16 h-16 rounded-full bg-slate-200"></div>
          <div class="flex-1">
            <div class="h-8 bg-slate-200 rounded w-48 mb-3"></div>
            <div class="flex gap-3 mb-4">
              <div class="h-6 bg-slate-100 rounded w-20"></div>
              <div class="h-6 bg-slate-100 rounded w-24"></div>
              <div class="h-6 bg-slate-100 rounded w-16"></div>
            </div>
            <div class="space-y-3">
              <div class="flex items-center gap-2">
                <div class="h-4 bg-slate-200 rounded w-16"></div>
                <div class="h-6 bg-slate-100 rounded w-32"></div>
              </div>
              <div class="flex items-center gap-2">
                <div class="h-4 bg-slate-200 rounded w-16"></div>
                <div class="h-6 bg-slate-100 rounded w-28"></div>
              </div>
              <div class="flex items-center gap-2">
                <div class="h-4 bg-slate-200 rounded w-16"></div>
                <div class="flex gap-2">
                  <div class="h-6 bg-slate-100 rounded w-20"></div>
                  <div class="h-6 bg-slate-100 rounded w-24"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 animate-pulse">
          <div class="h-6 bg-slate-200 rounded w-32 mb-4"></div>
          <div class="grid grid-cols-3 md:grid-cols-4 gap-4">
            <div v-for="n in 8" :key="n" class="p-4 bg-slate-50 rounded-xl">
              <div class="h-3 bg-slate-200 rounded w-16 mb-2"></div>
              <div class="h-6 bg-slate-300 rounded w-12"></div>
            </div>
          </div>
        </div>
        <div class="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 animate-pulse">
          <div class="h-6 bg-slate-200 rounded w-32 mb-4"></div>
          <div class="grid grid-cols-2 gap-4">
            <div v-for="n in 4" :key="n" class="p-4 bg-slate-50 rounded-xl">
              <div class="h-3 bg-slate-200 rounded w-16 mb-2"></div>
              <div class="h-6 bg-slate-300 rounded w-12"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Placeholder State -->
    <div v-else-if="!searchQuery" class="bg-white rounded-2xl border-2 border-dashed border-slate-200 py-20 text-center">
      <div class="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6 text-slate-300">
        <UserPlusIcon class="w-10 h-10" />
      </div>
      <h3 class="text-xl font-bold text-slate-800">No Intelligence Selected</h3>
      <p class="text-slate-500 max-w-sm mx-auto mt-2 font-medium">Use the search box above to lookup any player's statistics.</p>
    </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  MagnifyingGlassIcon, 
  XMarkIcon, 
  UserIcon, 
  UserPlusIcon,
  PresentationChartLineIcon,
  FireIcon,
  ShareIcon,
  InformationCircleIcon,
  ChartBarIcon
} from '@heroicons/vue/24/outline'
import CricketBallIcon from '~/components/icons/CricketBallIcon.vue'
import CricketHelmetIcon from '~/components/icons/CricketHelmetIcon.vue'
import GraphVisualization from '~/components/GraphVisualization.vue'
import BoundarySparkline from '~/components/BoundarySparkline.vue'

const config = useRuntimeConfig()
const route = useRoute()
const searchQuery = ref('')
const searchResults = ref<any[]>([])
const showResults = ref(false)
const playerStats = ref<any>(null)
const playerRivals = ref<any[]>([])
const loadingRivals = ref(false)
const loadingStats = ref(false)
const highlightedIndex = ref(-1)
let searchTimeout: any = null

// Franchise mapping to consolidate team names
const franchiseMapping: { [key: string]: string } = {
  // Royal Challengers franchise
  'Royal Challengers Bangalore': 'Royal Challengers Bengaluru',
  'Royal Challengers Bengaluru': 'Royal Challengers Bengaluru',
  
  // Kings/Punjab franchise
  'Kings XI Punjab': 'Punjab Kings',
  'Punjab Kings': 'Punjab Kings',
  
  // Delhi franchise
  'Delhi Daredevils': 'Delhi Capitals',
  'Delhi Capitals': 'Delhi Capitals',
  
  // Sunrisers franchise
  'Deccan Chargers': 'Sunrisers Hyderabad',
  'Sunrisers Hyderabad': 'Sunrisers Hyderabad'
}

const getFranchiseName = (teamName: string): string => {
  return franchiseMapping[teamName] || teamName
}

// Computed property to process and consolidate team information
const consolidatedTeamInfo = computed(() => {
  if (!playerStats.value?.teamInfo) return null
  
  const rawTeamInfo = playerStats.value.teamInfo
  const allTeams = []
  
  // Collect all teams the player has played for
  if (rawTeamInfo.debutTeam) allTeams.push(rawTeamInfo.debutTeam)
  if (rawTeamInfo.latestTeam) allTeams.push(rawTeamInfo.latestTeam)
  if (rawTeamInfo.otherTeams) allTeams.push(...rawTeamInfo.otherTeams)
  
  // Group by franchise
  const franchiseGroups = new Map<string, string[]>()
  allTeams.forEach(team => {
    const franchise = getFranchiseName(team)
    if (!franchiseGroups.has(franchise)) {
      franchiseGroups.set(franchise, [])
    }
    if (!franchiseGroups.get(franchise)!.includes(team)) {
      franchiseGroups.get(franchise)!.push(team)
    }
  })
  
  // Convert back to team info format
  const franchises = Array.from(franchiseGroups.keys())
  const totalTeams = franchises.length
  
  let debutTeam = ''
  let latestTeam = ''
  let otherTeams: string[] = []
  
  if (rawTeamInfo.debutTeam) {
    debutTeam = getFranchiseName(rawTeamInfo.debutTeam)
  }
  
  if (rawTeamInfo.latestTeam) {
    latestTeam = getFranchiseName(rawTeamInfo.latestTeam)
  }
  
  // For other teams, only include franchises that are different from debut and latest
  otherTeams = franchises.filter(franchise => 
    franchise !== debutTeam && franchise !== latestTeam
  )
  
  return {
    totalTeams,
    debutTeam,
    latestTeam,
    otherTeams
  }
})

// Performance trend analysis functions
const calculateBattingTrend = (seasonStats: any): { trend: string, change: number, color: string, icon: string } => {
  const seasons = Object.keys(seasonStats).filter(s => s !== 'all').sort()
  if (seasons.length < 2) return { trend: 'stable', change: 0, color: 'slate', icon: '→' }
  
  const recentSeasons = seasons.slice(-3) // Last 3 seasons for trend
  const battingAverages = recentSeasons
    .map(season => seasonStats[season]?.batting?.average || 0)
    .filter(avg => avg > 0)
  
  if (battingAverages.length < 2) return { trend: 'stable', change: 0, color: 'slate', icon: '→' }
  
  const latestAvg = battingAverages[battingAverages.length - 1]
  const previousAvg = battingAverages[battingAverages.length - 2]
  const change = ((latestAvg - previousAvg) / previousAvg * 100)
  
  if (change > 15) return { trend: 'improving', change: Math.round(change), color: 'green', icon: '↗' }
  if (change < -15) return { trend: 'declining', change: Math.round(change), color: 'red', icon: '↘' }
  return { trend: 'stable', change: Math.round(change), color: 'slate', icon: '→' }
}

const calculateBowlingTrend = (seasonStats: any): { trend: string, change: number, color: string, icon: string } => {
  const seasons = Object.keys(seasonStats).filter(s => s !== 'all').sort()
  if (seasons.length < 2) return { trend: 'stable', change: 0, color: 'slate', icon: '→' }
  
  const recentSeasons = seasons.slice(-3)
  const economyRates = recentSeasons
    .map(season => seasonStats[season]?.bowling?.economy)
    .filter(eco => eco != null && eco > 0) // Filter null, undefined, and 0 values
  
  if (economyRates.length < 2) return { trend: 'stable', change: 0, color: 'slate', icon: '→' }
  
  const latestEco = economyRates[economyRates.length - 1]
  const previousEco = economyRates[economyRates.length - 2]
  const change = ((previousEco - latestEco) / previousEco * 100) // Lower economy is better
  
  if (change > 10) return { trend: 'improving', change: Math.round(change), color: 'green', icon: '↗' }
  if (change < -10) return { trend: 'declining', change: Math.round(Math.abs(change)), color: 'red', icon: '↘' }
  return { trend: 'stable', change: Math.round(Math.abs(change)), color: 'slate', icon: '→' }
}

const calculateBoundaryTrend = (seasonStats: any): { trend: string, rate: number, color: string, icon: string } => {
  const seasons = Object.keys(seasonStats).filter(s => s !== 'all').sort()
  if (seasons.length < 2) return { trend: 'stable', rate: 0, color: 'slate', icon: '→' }
  
  // Calculate boundary rates for each season
  const boundaryRates = seasons.map(season => {
    const batting = seasonStats[season]?.batting
    if (!batting || !batting.balls || batting.balls === 0) return null
    
    const boundaries = (batting.fours || 0) + (batting.sixes || 0)
    return (boundaries / batting.balls) * 100
  }).filter(rate => rate !== null)
  
  if (boundaryRates.length < 2) return { trend: 'stable', rate: 0, color: 'slate', icon: '→' }
  
  // Calculate overall rate and trend
  const overallRate = boundaryRates.reduce((sum, rate) => sum + rate, 0) / boundaryRates.length
  
  // Compare recent seasons vs earlier seasons
  const recentSeasons = boundaryRates.slice(-3)
  const earlierSeasons = boundaryRates.slice(0, -3)
  
  if (recentSeasons.length === 0 || earlierSeasons.length === 0) {
    return { trend: 'stable', rate: overallRate, color: 'slate', icon: '→' }
  }
  
  const recentAvg = recentSeasons.reduce((sum, rate) => sum + rate, 0) / recentSeasons.length
  const earlierAvg = earlierSeasons.reduce((sum, rate) => sum + rate, 0) / earlierSeasons.length
  
  const change = ((recentAvg - earlierAvg) / earlierAvg) * 100
  
  if (change > 8) return { trend: 'improving', rate: overallRate, color: 'green', icon: '↗' }
  if (change < -8) return { trend: 'declining', rate: overallRate, color: 'red', icon: '↘' }
  return { trend: 'stable', rate: overallRate, color: 'slate', icon: '→' }
}

const getSeasonComparison = (currentStats: any, previousStats: any, type: 'batting' | 'bowling') => {
  if (!currentStats || !previousStats) return null
  
  if (type === 'batting' && currentStats.batting && previousStats.batting) {
    const runsChange = currentStats.batting.runs - previousStats.batting.runs
    const avgChange = ((currentStats.batting.average - previousStats.batting.average) / previousStats.batting.average * 100)
    return {
      runs: runsChange > 0 ? `+${runsChange}` : `${runsChange}`,
      average: avgChange > 0 ? `+${avgChange.toFixed(1)}%` : `${avgChange.toFixed(1)}%`,
      trend: avgChange > 0 ? 'up' : 'down'
    }
  }
  
  if (type === 'bowling' && currentStats.bowling && previousStats.bowling) {
    const wicketsChange = currentStats.bowling.wickets - previousStats.bowling.wickets
    if (currentStats.bowling.economy != null && previousStats.bowling.economy != null) {
      const ecoChange = ((previousStats.bowling.economy - currentStats.bowling.economy) / previousStats.bowling.economy * 100)
      return {
        wickets: wicketsChange > 0 ? `+${wicketsChange}` : `${wicketsChange}`,
        economy: ecoChange > 0 ? `+${ecoChange.toFixed(1)}%` : `${ecoChange.toFixed(1)}%`,
        trend: ecoChange > 0 ? 'up' : 'down'
      }
    }
    return {
      wickets: wicketsChange > 0 ? `+${wicketsChange}` : `${wicketsChange}`,
      economy: 'N/A',
      trend: 'up'
    }
  }
  
  return null
}

type GraphData = {
  edges: Array<any>,
  nodes: Array<any>
}

const fetchPlayerGraph = async (playerName: string) => {
  // Start loading but don't block the main stats loading
  loadingRivals.value = true
  
  try {
    const graphData = await $fetch<GraphData>(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/graph`)
    
    // Convert graph data to rivals format for compatibility
    if (graphData.edges && graphData.nodes) {
      playerRivals.value = graphData.edges.map((edge: any) => {
        const targetNode = graphData.nodes.find((n: any) => n.id === edge.target)
        return {
          name: targetNode?.name || edge.target,
          weight: edge.weight,
          score: edge.weight * 10,
          type: edge.relationship
        }
      })
    } else {
      // Fallback to old rivals endpoint
      playerRivals.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/rivals`)
    }
  } catch (error) {
    console.error('Failed to fetch graph data:', error)
    // Fallback to old endpoint
    try {
      playerRivals.value = await $fetch(`${config.public.apiBase}/api/player/${encodeURIComponent(playerName)}/rivals`)
    } catch (fallbackError) {
      console.error('Fallback fetch also failed:', fallbackError)
      playerRivals.value = []
    }
  } finally {
    loadingRivals.value = false
  }
}

const clearSearch = () => {
  searchQuery.value = ''
  playerStats.value = null
  showResults.value = false
}

const searchPlayers = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  if (searchQuery.value.length < 2) {
    searchResults.value = []
    showResults.value = false
    return
  }
  searchTimeout = setTimeout(async () => {
    try {
      const data: any = await $fetch(`${config.public.apiBase}/api/players/search?query=${encodeURIComponent(searchQuery.value)}`)
      searchResults.value = data || []
      showResults.value = searchResults.value.length > 0
    } catch (error) {
      console.error('Search failed:', error)
      searchResults.value = []
      showResults.value = false
    }
  }, 200) // Reduced from 300ms to 200ms for faster response
}

const handleKeydown = (e: KeyboardEvent) => {
  if (!showResults.value || searchResults.value.length === 0) return
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    highlightedIndex.value = (highlightedIndex.value + 1) % searchResults.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    highlightedIndex.value = (highlightedIndex.value - 1 + searchResults.value.length) % searchResults.value.length
  } else if (e.key === 'Enter') {
    e.preventDefault()
    if (highlightedIndex.value >= 0) selectPlayer(searchResults.value[highlightedIndex.value])
  } else if (e.key === 'Escape') {
    showResults.value = false
  }
}

const selectPlayer = async (playerName: string) => {
  searchQuery.value = playerName
  showResults.value = false
  loadingStats.value = true
  
  // Clear previous data immediately for better UX
  playerStats.value = null
  playerRivals.value = []
  
  try {
    const playerSlug = playerName.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '')
    
    // Load main stats and graph data in parallel for better performance
    const [statsData] = await Promise.all([
      $fetch(`${config.public.apiBase}/api/players/${playerSlug}/stats`),
      fetchPlayerGraph(playerName) // This runs in parallel, has its own loading state
    ])
    
    playerStats.value = statsData
  } catch (error) {
    console.error('Fetch failed:', error)
    playerStats.value = null
  } finally {
    loadingStats.value = false
  }
}

onMounted(() => {
  if (route.query.name) selectPlayer(route.query.name as string)
})
</script>
