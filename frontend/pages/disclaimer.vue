<template>
  <div class="max-w-4xl mx-auto py-12 px-4 space-y-12">
    <!-- Header -->
    <div class="text-center space-y-4">
      <div class="w-16 h-16 bg-slate-900 text-white rounded-2xl flex items-center justify-center mx-auto shadow-xl">
        <ShieldExclamationIcon class="w-8 h-8" />
      </div>
      <h1 class="text-4xl font-black text-slate-900 tracking-tight">Legal Disclaimer & Data Attribution</h1>
      <p class="text-slate-500 font-medium">Please read carefully before using Boundary Graph</p>
    </div>

    <!-- Data Attribution -->
    <section class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm space-y-4">
      <div class="flex items-center gap-3 mb-2">
        <div class="p-2 bg-blue-50 rounded-lg">
          <CircleStackIcon class="w-5 h-5 text-blue-600" />
        </div>
        <h2 class="text-xl font-bold text-slate-800">Data Source & Attribution</h2>
      </div>
      <p class="text-slate-600 leading-relaxed">
        The ball-by-ball cricket data visualized on this platform is sourced from 
        <a href="https://cricsheet.org/" target="_blank" class="text-brand-primary font-bold hover:underline">Cricsheet.org</a>. 
        We are immensely grateful to the Cricsheet project for providing freely available, structured cricket data that enables developers and researchers to build deep analytics platforms like Boundary Graph.
      </p>
    </section>

    <!-- Content Accuracy -->
    <section class="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm space-y-4">
      <div class="flex items-center gap-3 mb-2">
        <div class="p-2 bg-green-50 rounded-lg">
          <CheckBadgeIcon class="w-5 h-5 text-green-600" />
        </div>
        <h2 class="text-xl font-bold text-slate-800">Accuracy of Information</h2>
      </div>
      <p class="text-slate-600 leading-relaxed">
        While we strive to provide the most authentic and up-to-date statistics using our Neo4j graph processing engine, the analytics presented here are for <strong class="text-slate-900">informational, educational, and entertainment purposes only</strong>. 
        Cricket stats are complex and subject to varying interpretations or errors in raw data processing. Boundary Graph does not guarantee the 100% accuracy or completeness of any data shown.
      </p>
    </section>

    <!-- Liability & Betting -->
    <section class="bg-red-50 p-8 rounded-3xl border border-red-100 space-y-4">
      <div class="flex items-center gap-3 mb-2">
        <div class="p-2 bg-red-100 rounded-lg">
          <ExclamationTriangleIcon class="w-5 h-5 text-red-600" />
        </div>
        <h2 class="text-xl font-bold text-red-900">Limitation of Liability</h2>
      </div>
      <div class="space-y-4 text-red-800/80 text-sm leading-relaxed font-medium">
        <p>
          <strong>No Financial or Betting Advice:</strong> Boundary Graph is NOT a betting platform and does not provide gambling, financial, or investment advice. Any predictive features (including "Ask BG") are purely algorithmic experiments based on historical data and should NOT be used as a basis for real-world wagering or financial decisions.
        </p>
        <p>
          <strong>Disclaimer of Liability:</strong> Under no circumstances shall the developer of Boundary Graph be held liable for any direct, indirect, special, incidental, or consequential damages (including, but not limited to, financial loss, loss of data, or betting losses) arising out of the use of, or inability to use, the materials on this site.
        </p>
        <p>
          By using this application, you agree that you do so at your own risk. You are solely responsible for compliance with any local laws regarding data usage and sports analytics.
        </p>
      </div>
    </section>

    <div class="text-center pt-8">
      <NuxtLink to="/" class="text-slate-400 hover:text-slate-900 text-sm font-bold transition-colors underline underline-offset-4 decoration-slate-200">
        I understand, take me back to the Dashboard
      </NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
import { 
  ShieldExclamationIcon, 
  CircleStackIcon, 
  CheckBadgeIcon, 
  ExclamationTriangleIcon 
} from '@heroicons/vue/24/outline'

useHead({
  title: 'Disclaimer | Boundary Graph'
})
</script>
