/**
 * Performance Monitoring Composable
 * Tracks API performance, cache hits/misses, and provides insights
 */

import { ref, computed } from 'vue'

interface PerformanceMetric {
  name: string
  startTime: number
  endTime?: number
  duration?: number
  type: 'api' | 'cache' | 'render'
  success: boolean
  error?: string
}

interface CacheMetric {
  key: string
  hit: boolean
  source: 'memory' | 'localStorage' | 'stale' | 'miss'
  timestamp: number
}

interface APIHealth {
  endpoint: string
  responseTime: number
  status: number
  timestamp: number
}

class PerformanceMonitor {
  private static instance: PerformanceMonitor
  
  private metrics = ref<PerformanceMetric[]>([])
  private cacheMetrics = ref<CacheMetric[]>([])
  private apiHealth = ref<APIHealth[]>([])
  private isEnabled = ref(true)

  private constructor() {
    this.startPerformanceTracking()
  }

  static getInstance(): PerformanceMonitor {
    if (!PerformanceMonitor.instance) {
      PerformanceMonitor.instance = new PerformanceMonitor()
    }
    return PerformanceMonitor.instance
  }

  // Start tracking a performance metric
  startMetric(name: string, type: 'api' | 'cache' | 'render' = 'api'): string {
    if (!this.isEnabled.value) return name
    
    const metric: PerformanceMetric = {
      name,
      startTime: performance.now(),
      type,
      success: true
    }
    
    this.metrics.value.push(metric)
    return name // Return name as ID for ending the metric
  }

  // End tracking a performance metric
  endMetric(id: string, success: boolean = true, error?: string): void {
    if (!this.isEnabled.value) return
    
    const metric = this.metrics.value.find(m => m.name === id && !m.endTime)
    if (metric) {
      metric.endTime = performance.now()
      metric.duration = metric.endTime - metric.startTime
      metric.success = success
      metric.error = error
    }
  }

  // Track cache performance
  trackCacheHit(key: string, hit: boolean, source: CacheMetric['source']): void {
    if (!this.isEnabled.value) return
    
    this.cacheMetrics.value.push({
      key,
      hit,
      source,
      timestamp: Date.now()
    })

    // Keep only last 100 cache metrics
    if (this.cacheMetrics.value.length > 100) {
      this.cacheMetrics.value = this.cacheMetrics.value.slice(-100)
    }
  }

  // Track API health
  trackAPICall(endpoint: string, responseTime: number, status: number): void {
    if (!this.isEnabled.value) return
    
    this.apiHealth.value.push({
      endpoint,
      responseTime,
      status,
      timestamp: Date.now()
    })

    // Keep only last 50 API calls per endpoint
    const endpointCalls = this.apiHealth.value.filter(call => call.endpoint === endpoint)
    if (endpointCalls.length > 50) {
      this.apiHealth.value = this.apiHealth.value.filter(call => 
        call.endpoint !== endpoint || 
        call.timestamp >= endpointCalls[endpointCalls.length - 50].timestamp
      )
    }
  }

  // Performance Analytics
  get analytics() {
    return computed(() => {
      const completedMetrics = this.metrics.value.filter(m => m.duration !== undefined)
      
      const apiMetrics = completedMetrics.filter(m => m.type === 'api')
      const cacheMetrics = this.cacheMetrics.value
      const recentAPIHealth = this.apiHealth.value.slice(-20)
      
      // Cache statistics
      const totalCacheRequests = cacheMetrics.length
      const cacheHits = cacheMetrics.filter(m => m.hit).length
      const cacheHitRate = totalCacheRequests > 0 ? (cacheHits / totalCacheRequests) * 100 : 0
      
      const cacheSources = cacheMetrics.reduce((acc, metric) => {
        acc[metric.source] = (acc[metric.source] || 0) + 1
        return acc
      }, {} as Record<string, number>)

      // API performance
      const avgResponseTime = apiMetrics.length > 0 
        ? apiMetrics.reduce((sum, m) => sum + (m.duration || 0), 0) / apiMetrics.length
        : 0
      
      const successfulAPICalls = apiMetrics.filter(m => m.success).length
      const apiSuccessRate = apiMetrics.length > 0 ? (successfulAPICalls / apiMetrics.length) * 100 : 0
      
      // Endpoint performance
      const endpointStats = recentAPIHealth.reduce((acc, call) => {
        if (!acc[call.endpoint]) {
          acc[call.endpoint] = {
            calls: 0,
            totalTime: 0,
            errors: 0,
            avgResponseTime: 0
          }
        }
        
        acc[call.endpoint].calls++
        acc[call.endpoint].totalTime += call.responseTime
        if (call.status >= 400) acc[call.endpoint].errors++
        acc[call.endpoint].avgResponseTime = acc[call.endpoint].totalTime / acc[call.endpoint].calls
        
        return acc
      }, {} as Record<string, any>)

      return {
        cache: {
          totalRequests: totalCacheRequests,
          hitRate: Math.round(cacheHitRate * 100) / 100,
          sources: cacheSources
        },
        api: {
          totalCalls: apiMetrics.length,
          avgResponseTime: Math.round(avgResponseTime * 100) / 100,
          successRate: Math.round(apiSuccessRate * 100) / 100,
          endpointStats
        },
        performance: {
          slowestEndpoints: Object.entries(endpointStats)
            .sort(([,a], [,b]) => b.avgResponseTime - a.avgResponseTime)
            .slice(0, 5),
          fastestEndpoints: Object.entries(endpointStats)
            .sort(([,a], [,b]) => a.avgResponseTime - b.avgResponseTime)
            .slice(0, 5)
        }
      }
    })
  }

  // Get performance recommendations
  get recommendations() {
    return computed(() => {
      const analytics = this.analytics.value
      const recommendations: string[] = []

      // Cache recommendations
      if (analytics.cache.hitRate < 70) {
        recommendations.push("🔥 Cache hit rate is low. Consider increasing cache TTL or implementing better cache keys.")
      }
      
      if (analytics.cache.sources.miss > analytics.cache.totalRequests * 0.5) {
        recommendations.push("💾 High cache miss rate detected. Review caching strategy for frequently accessed data.")
      }

      // API recommendations
      if (analytics.api.avgResponseTime > 2000) {
        recommendations.push("⚡ Average API response time is high. Consider implementing server-side caching or database optimization.")
      }
      
      if (analytics.api.successRate < 95) {
        recommendations.push("🚨 API error rate is high. Check error handling and retry logic.")
      }

      // Endpoint-specific recommendations
      analytics.performance.slowestEndpoints.forEach(([endpoint, stats]) => {
        if (stats.avgResponseTime > 3000) {
          recommendations.push(`🐌 ${endpoint} is consistently slow (${Math.round(stats.avgResponseTime)}ms avg). Consider optimization.`)
        }
      })

      return recommendations
    })
  }

  // Performance report
  generateReport(): object {
    return {
      timestamp: new Date().toISOString(),
      analytics: this.analytics.value,
      recommendations: this.recommendations.value,
      rawMetrics: {
        performance: this.metrics.value.slice(-50),
        cache: this.cacheMetrics.value.slice(-50),
        api: this.apiHealth.value.slice(-20)
      }
    }
  }

  // Enable/disable monitoring
  setEnabled(enabled: boolean): void {
    this.isEnabled.value = enabled
  }

  // Clear all metrics
  clearMetrics(): void {
    this.metrics.value = []
    this.cacheMetrics.value = []
    this.apiHealth.value = []
  }

  // Start automatic performance tracking
  private startPerformanceTracking(): void {
    if (typeof window === 'undefined') return

    // Track navigation timing
    window.addEventListener('load', () => {
      if (window.performance && window.performance.timing) {
        const timing = window.performance.timing
        this.trackNavigation(timing)
      }
    })

    // Track long tasks (if available)
    if ('PerformanceObserver' in window) {
      try {
        const observer = new PerformanceObserver((list) => {
          list.getEntries().forEach((entry) => {
            if (entry.entryType === 'longtask') {
              console.warn(`🐌 Long task detected: ${entry.duration}ms`)
            }
          })
        })
        observer.observe({ entryTypes: ['longtask'] })
      } catch (e) {
        // Long task observer not supported
      }
    }
  }

  private trackNavigation(timing: PerformanceTiming): void {
    const metrics = {
      'DNS Lookup': timing.domainLookupEnd - timing.domainLookupStart,
      'TCP Connection': timing.connectEnd - timing.connectStart,
      'Request': timing.responseStart - timing.requestStart,
      'Response': timing.responseEnd - timing.responseStart,
      'DOM Processing': timing.domComplete - timing.domLoading,
      'Load Event': timing.loadEventEnd - timing.loadEventStart,
      'Total Load Time': timing.loadEventEnd - timing.navigationStart
    }

    Object.entries(metrics).forEach(([name, duration]) => {
      if (duration > 0) {
        this.metrics.value.push({
          name: `Navigation: ${name}`,
          startTime: 0,
          endTime: duration,
          duration,
          type: 'render',
          success: true
        })
      }
    })
  }
}

// Composable function for Vue components
export function usePerformanceMonitor() {
  const monitor = PerformanceMonitor.getInstance()
  
  const trackAPI = async <T>(
    endpoint: string, 
    apiCall: () => Promise<T>
  ): Promise<T> => {
    const metricId = monitor.startMetric(`API: ${endpoint}`, 'api')
    const startTime = performance.now()
    
    try {
      const result = await apiCall()
      const endTime = performance.now()
      const duration = endTime - startTime
      
      monitor.endMetric(metricId, true)
      monitor.trackAPICall(endpoint, duration, 200)
      
      return result
    } catch (error) {
      const endTime = performance.now()
      const duration = endTime - startTime
      
      monitor.endMetric(metricId, false, error instanceof Error ? error.message : String(error))
      monitor.trackAPICall(endpoint, duration, 500)
      
      throw error
    }
  }

  const trackCache = (key: string, hit: boolean, source: CacheMetric['source']) => {
    monitor.trackCacheHit(key, hit, source)
  }

  return {
    trackAPI,
    trackCache,
    startMetric: monitor.startMetric.bind(monitor),
    endMetric: monitor.endMetric.bind(monitor),
    analytics: monitor.analytics,
    recommendations: monitor.recommendations,
    generateReport: monitor.generateReport.bind(monitor),
    setEnabled: monitor.setEnabled.bind(monitor),
    clearMetrics: monitor.clearMetrics.bind(monitor)
  }
}

export default PerformanceMonitor