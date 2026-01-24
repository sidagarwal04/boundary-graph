<template>
  <div class="min-h-[70vh] flex flex-col items-center justify-center text-center px-4 relative overflow-hidden">
    <!-- Secret Background Element -->
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[500px] h-[500px] bg-brand-primary/5 rounded-full blur-3xl -z-10 animate-pulse"></div>
    
    <!-- Mystery Icon -->
    <div class="mb-8 relative group">
      <div class="w-24 h-24 bg-slate-900 rounded-3xl flex items-center justify-center shadow-2xl rotate-3 group-hover:rotate-0 transition-transform duration-500">
         <img 
           src="/bg-logo.png" 
           alt="Boundary Graph Logo" 
           class="w-20 h-20 object-contain"
         />
      </div>
      <div class="absolute -bottom-2 -right-2 w-10 h-10 bg-brand-primary rounded-full flex items-center justify-center border-4 border-slate-50 shadow-lg">
        <span class="text-white text-xs font-black">?</span>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-xl space-y-6">
      <h1 class="text-4xl md:text-5xl font-black text-slate-900 tracking-tight">
        Something <span class="text-brand-primary">Prophetic</span> is Brewing
      </h1>
      
      <p class="text-lg text-slate-600 font-medium leading-relaxed">
        The numbers are whispering. Past boundaries, wickets, and seasons are converging into something... predictive.
      </p>

      <div class="py-10">
        <div class="inline-flex flex-col items-start p-6 bg-white border border-slate-100 shadow-xl rounded-2xl text-left max-w-sm relative">
          <div class="absolute -top-3 -left-3 px-3 py-1 bg-slate-900 text-white text-[10px] font-bold rounded uppercase tracking-widest">Classification: Classified</div>
          <p class="text-slate-500 text-sm italic italic leading-relaxed">
            "We're feeding a decade of graph data into a new cognitive core. Soon, you won't just look at the history of the IPL... you'll see its future."
          </p>
          <div class="mt-4 flex items-center gap-2">
            <div class="w-2 h-2 rounded-full bg-brand-primary animate-ping"></div>
            <span class="text-[10px] font-black text-slate-400 uppercase tracking-tighter">BG-PredictEngine v0.1 Initializing...</span>
          </div>
        </div>
      </div>

      <div class="flex flex-col items-center gap-4 pt-4 relative">
        <div class="absolute -top-12 -right-8 rotate-12 border-4 border-red-600/20 px-4 py-1 rounded text-red-600/20 font-black text-2xl select-none pointer-events-none uppercase tracking-widest">
          Secret
        </div>
        <div class="px-6 py-2 bg-slate-100 text-slate-500 rounded-full text-xs font-bold uppercase tracking-widest border border-slate-200">
          Coming Soon for IPL 2026
        </div>
        <NuxtLink to="/" class="text-slate-400 hover:text-slate-900 text-sm font-bold transition-colors underline underline-offset-4 decoration-slate-200">
          Return to Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { SparklesIcon } from '@heroicons/vue/24/outline'

useHead({
  title: 'Ask BG | Coming Soon'
})
</script>
