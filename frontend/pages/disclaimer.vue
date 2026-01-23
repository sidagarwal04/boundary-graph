<template>
  <div class="min-h-screen bg-slate-50 py-12">
    <div class="max-w-4xl mx-auto px-4">
      <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden">
        <!-- Header -->
        <div class="px-8 py-6 border-b border-slate-100 bg-slate-50/50">
          <div class="flex items-center gap-4">
            <div class="p-3 bg-amber-100 rounded-xl">
              <ShieldExclamationIcon class="w-8 h-8 text-amber-600" />
            </div>
            <div>
              <h1 class="text-2xl font-bold text-slate-900">Legal Disclaimer & Terms</h1>
              <p class="text-slate-600 mt-1">Educational project terms and trademark acknowledgments</p>
            </div>
          </div>
        </div>

        <!-- Content -->
        <div class="px-8 py-8 space-y-8">
          <!-- Independence Statement -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Independence & Non-Affiliation</h2>
            <div class="bg-amber-50 border border-amber-200 rounded-lg p-6">
              <div class="prose prose-slate text-slate-700 space-y-3">
                <p class="font-medium text-amber-800">
                  <strong>This is an independent project and is NOT affiliated with, endorsed by, or sponsored by:</strong>
                </p>
                <ul class="list-disc pl-6 space-y-1 text-amber-700">
                  <li>The Board of Control for Cricket in India (BCCI)</li>
                  <li>Indian Premier League (IPL) or any tournament organizers</li>
                  <li>Any cricket teams, franchises, or their management</li>
                  <li>Any broadcasting partners or official sponsors</li>
                  <li>Any cricket governing bodies or organizations</li>
                </ul>
              </div>
            </div>
          </section>

          <!-- Educational Purpose -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Educational Purpose Only</h2>
            <div class="prose prose-slate text-slate-700 space-y-3">
              <p>
                This project, "Boundary Graph," is created solely for <strong>educational, research, and portfolio demonstration purposes</strong>. 
                It serves as a technical showcase of modern web development technologies including graph databases, API development, 
                and data visualization techniques.
              </p>
              <p>
                This application is <strong>not monetized</strong> and serves no commercial purpose. No revenue is generated 
                from this project through advertisements, subscriptions, or any other means.
              </p>
            </div>
          </section>

          <!-- Trademark Acknowledgment -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Trademark & Copyright Acknowledgment</h2>
            <div class="prose prose-slate text-slate-700 space-y-3">
              <p>
                All team names, logos, tournament names, and related intellectual property referenced in this project 
                are the exclusive property of their respective owners:
              </p>
              <ul class="list-disc pl-6 space-y-1">
                <li><strong>Tournament names and branding</strong> - Property of BCCI and tournament organizers</li>
                <li><strong>Team names and logos</strong> - Property of respective franchise owners</li>
                <li><strong>Player names and statistics</strong> - Used for analytical purposes under fair use</li>
                <li><strong>Match data and records</strong> - Compiled from publicly available sources</li>
              </ul>
            </div>
          </section>

          <!-- Fair Use Statement -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Fair Use Statement</h2>
            <div class="prose prose-slate text-slate-700 space-y-3">
              <p>
                The use of trademarked names, logos, and statistical data in this project is believed to fall under 
                <strong>fair use</strong> provisions for educational and non-commercial purposes:
              </p>
              <ul class="list-disc pl-6 space-y-1">
                <li><strong>Educational Purpose</strong> - Used for learning and technical demonstration</li>
                <li><strong>Non-Commercial</strong> - No monetary gain or commercial benefit</li>
                <li><strong>Transformative</strong> - Data is analyzed and presented in new analytical formats</li>
                <li><strong>Limited Use</strong> - Only necessary elements used for functionality</li>
              </ul>
            </div>
          </section>

          <!-- Contact for Rights Holders -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Contact for Rights Holders</h2>
            <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <div class="prose prose-slate text-slate-700 space-y-3">
                <p class="font-medium text-blue-800">
                  If you are a rights holder and have concerns about this project:
                </p>
                <p class="text-blue-700">
                  Please contact the repository owner through the GitHub repository or the developer's website. 
                  We are committed to addressing any legitimate concerns promptly and will take appropriate action, 
                  including modification or removal of content if necessary.
                </p>
                <div class="flex items-center gap-4 mt-4">
                  <a 
                    href="https://github.com/sidagarwal04/boundary-graph" 
                    target="_blank" 
                    class="text-blue-600 hover:underline font-medium"
                  >
                    GitHub Repository
                  </a>
                  <span class="text-blue-400">•</span>
                  <a 
                    href="https://meetsid.dev" 
                    target="_blank" 
                    class="text-blue-600 hover:underline font-medium"
                  >
                    Developer Contact
                  </a>
                </div>
              </div>
            </div>
          </section>

          <!-- Data Sources -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Data Sources & Attribution</h2>
            <div class="prose prose-slate text-slate-700 space-y-3">
              <p>
                All cricket data used in this project has been compiled from publicly available sources and official 
                statistics. This includes match results, player statistics, and historical records that are part of 
                the public domain or available through official channels.
              </p>
              <p>
                We acknowledge that while the data may be public, the presentation formats, team identities, and 
                tournament branding remain the intellectual property of their respective owners.
              </p>
            </div>
          </section>

          <!-- Technical Implementation -->
          <section>
            <h2 class="text-xl font-semibold text-slate-900 mb-4">Technical Implementation Note</h2>
            <div class="prose prose-slate text-slate-700 space-y-3">
              <p>
                This project demonstrates advanced technical concepts including graph databases (Neo4j), 
                API development (FastAPI), modern frontend frameworks (Nuxt 3/Vue.js), and data visualization. 
                The primary value lies in the technical implementation and educational aspects of the codebase.
              </p>
            </div>
          </section>

          <!-- Last Updated -->
          <section class="text-center pt-8 border-t border-slate-100">
            <p class="text-slate-500 text-sm">
              Last updated: January 23, 2026
            </p>
          </section>
        </div>
      </div>

      <!-- Back to Home -->
      <div class="text-center mt-8">
        <NuxtLink 
          to="/" 
          class="inline-flex items-center gap-2 text-brand-primary hover:underline font-medium"
        >
          ← Back to Analytics Dashboard
        </NuxtLink>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ShieldExclamationIcon } from '@heroicons/vue/24/outline'

// SEO Meta
useHead({
  title: 'Legal Disclaimer - Boundary Graph',
  meta: [
    { name: 'description', content: 'Legal disclaimer and terms for the Boundary Graph cricket analytics project' },
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})
</script>

