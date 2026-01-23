/**
 * Optimized API Composable with Advanced Caching
 * Provides intelligent data fetching with multiple cache strategies
 */

import { ref, computed, type Ref, type ComputedRef } from 'vue'
import { cacheAPI } from '~/utils/cache'
import { usePerformanceMonitor } from '~/composables/usePerformance'

interface APIOptions {
  cache?: boolean
  cacheTTL?: number
  staleWhileRevalidate?: number
  retries?: number
  timeout?: number
}

interface APIState<T> {
  data: T | null
  loading: boolean
  error: string | null
  cached: boolean
}

interface APIStateReturn<T> {
  data: Ref<T | null>
  loading: Ref<boolean>
  error: Ref<string | null>
  cached: Ref<boolean>
  fetch: () => Promise<void>
  refresh: () => Promise<void>
  state: ComputedRef<APIState<T>>
}

export function useOptimizedAPI() {
  const config = useRuntimeConfig()
  const { trackAPI, trackCache } = usePerformanceMonitor()

  // Default API options
  const defaultOptions: APIOptions = {
    cache: true,
    cacheTTL: 30 * 60 * 1000, // 30 minutes
    staleWhileRevalidate: 60 * 60 * 1000, // 1 hour
    retries: 3,
    timeout: 30000 // 30 seconds
  }

  /**
   * Optimized fetch with intelligent caching and performance tracking
   */
  async function optimizedFetch<T>(
    endpoint: string, 
    options: APIOptions = {}
  ): Promise<T> {
    const opts = { ...defaultOptions, ...options }
    const fullUrl = `${config.public.apiUrl || 'http://localhost:8000'}${endpoint}`

    const fetchFn = async (): Promise<T> => {
      const controller = new AbortController()
      const timeoutId = setTimeout(() => controller.abort(), opts.timeout!)

      try {
        return await trackAPI(endpoint, async () => {
          const response = await fetch(fullUrl, {
            signal: controller.signal,
            headers: {
              'Content-Type': 'application/json',
              'Accept': 'application/json',
              'Accept-Encoding': 'gzip, deflate, br'
            }
          })

          clearTimeout(timeoutId)

          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`)
          }

          return await response.json()
        })
      } catch (error) {
        clearTimeout(timeoutId)
        throw error
      }
    }

    if (opts.cache) {
      return await cacheAPI(endpoint, fetchFn, opts.cacheTTL!, opts.staleWhileRevalidate!)
    } else {
      return await fetchFn()
    }
  }

  /**
   * Reactive API state management
   */
  function useAPIState<T>(
    endpoint: string, 
    options: APIOptions = {}
  ): APIStateReturn<T> {
    const data = ref<T | null>(null)
    const loading = ref(false)
    const error = ref<string | null>(null)
    const cached = ref(false)

    const fetch = async () => {
      loading.value = true
      error.value = null

      try {
        const result = await optimizedFetch<T>(endpoint, options)
        data.value = result
        cached.value = options.cache !== false
      } catch (err) {
        error.value = err instanceof Error ? err.message : String(err)
        console.error(`API Error for ${endpoint}:`, err)
      } finally {
        loading.value = false
      }
    }

    const refresh = async () => {
      // Force fresh fetch by disabling cache temporarily
      const originalCache = options.cache
      options.cache = false
      await fetch()
      options.cache = originalCache
    }

    const state = computed<APIState<T>>(() => ({
      data: data.value,
      loading: loading.value,
      error: error.value,
      cached: cached.value
    }))

    return {
      data: data as Ref<T | null>,
      loading,
      error,
      cached,
      fetch,
      refresh,
      state
    } as APIStateReturn<T>
  }

  // Predefined API endpoints with optimized cache settings
  const endpoints = {
    overview: () => useAPIState('/api/overview', { 
      cacheTTL: 60 * 60 * 1000, // 1 hour - overview data changes infrequently
      staleWhileRevalidate: 4 * 60 * 60 * 1000 // 4 hours stale
    }),
    
    venues: () => useAPIState('/api/venues', { 
      cacheTTL: 30 * 60 * 1000, // 30 minutes
      staleWhileRevalidate: 2 * 60 * 60 * 1000 // 2 hours stale
    }),
    
    topBatsmen: (limit: number = 20) => useAPIState(`/api/batsmen/top?limit=${limit}`, { 
      cacheTTL: 15 * 60 * 1000, // 15 minutes - player stats change more frequently
      staleWhileRevalidate: 60 * 60 * 1000 // 1 hour stale
    }),
    
    topBowlers: (limit: number = 20) => useAPIState(`/api/bowlers/top?limit=${limit}`, { 
      cacheTTL: 15 * 60 * 1000, // 15 minutes
      staleWhileRevalidate: 60 * 60 * 1000 // 1 hour stale
    }),
    
    seasons: () => useAPIState('/api/seasons', { 
      cacheTTL: 2 * 60 * 60 * 1000, // 2 hours - season data is historical
      staleWhileRevalidate: 24 * 60 * 60 * 1000 // 24 hours stale
    }),
    
    playerStats: (playerName: string) => useAPIState(`/api/players/${playerName}/stats`, { 
      cacheTTL: 10 * 60 * 1000, // 10 minutes - individual stats
      staleWhileRevalidate: 30 * 60 * 1000 // 30 minutes stale
    }),
    
    teamStats: (teamName: string) => useAPIState(`/api/team/${teamName}/stats`, { 
      cacheTTL: 20 * 60 * 1000, // 20 minutes
      staleWhileRevalidate: 60 * 60 * 1000 // 1 hour stale
    }),
    
    search: (query: string) => useAPIState(`/api/search?q=${encodeURIComponent(query)}`, { 
      cacheTTL: 5 * 60 * 1000, // 5 minutes - search results are dynamic
      staleWhileRevalidate: 15 * 60 * 1000 // 15 minutes stale
    })
  }

  // Batch API calls for efficiency
  async function batchFetch<T>(requests: Array<{ endpoint: string; options?: APIOptions }>): Promise<T[]> {
    const promises = requests.map(({ endpoint, options }) => 
      optimizedFetch<T>(endpoint, options)
    )
    
    try {
      return await Promise.all(promises)
    } catch (error) {
      // If batch fails, try individual requests
      console.warn('Batch fetch failed, falling back to individual requests:', error)
      const results: T[] = []
      
      for (const { endpoint, options } of requests) {
        try {
          const result = await optimizedFetch<T>(endpoint, options)
          results.push(result)
        } catch (individualError) {
          console.error(`Individual fetch failed for ${endpoint}:`, individualError)
          throw individualError
        }
      }
      
      return results
    }
  }

  // Preload critical data
  async function preloadCriticalData() {
    const criticalEndpoints = [
      '/api/overview',
      '/api/venues',
      '/api/batsmen/top?limit=10',
      '/api/bowlers/top?limit=10'
    ]

    const requests = criticalEndpoints.map(endpoint => ({
      endpoint,
      options: { cache: true }
    }))

    try {
      await batchFetch(requests)
      console.log('✅ Critical data preloaded successfully')
    } catch (error) {
      console.warn('⚠️ Failed to preload critical data:', error)
    }
  }

  // Background data refresh
  function startBackgroundRefresh() {
    if (typeof window === 'undefined') return

    // Refresh critical data every 10 minutes
    setInterval(async () => {
      try {
        await preloadCriticalData()
        console.log('🔄 Background refresh completed')
      } catch (error) {
        console.warn('🔄 Background refresh failed:', error)
      }
    }, 10 * 60 * 1000)
  }

  return {
    // Core functions
    optimizedFetch,
    useAPIState,
    batchFetch,
    
    // Predefined endpoints
    endpoints,
    
    // Performance optimizations
    preloadCriticalData,
    startBackgroundRefresh,
    
    // Utilities
    trackCache,
    trackAPI
  }
}