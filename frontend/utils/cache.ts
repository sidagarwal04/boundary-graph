/**
 * Advanced Caching Utility for IPL Cricket Dashboard
 * Provides intelligent caching with multiple fallback strategies
 */

export interface CacheConfig {
  key: string;
  ttl: number; // Time to live in milliseconds
  staleWhileRevalidate?: number; // Additional time to serve stale data
  retryAttempts?: number;
  retryDelay?: number;
}

export interface CacheItem<T> {
  data: T;
  expires: number;
  created: number;
  staleExpires?: number;
}

export class AdvancedCache {
  private static instance: AdvancedCache;
  private storage: Storage;
  private memoryCache: Map<string, CacheItem<any>>;
  private maxMemoryItems: number = 100;

  private constructor() {
    this.storage = typeof window !== 'undefined' ? localStorage : null as any;
    this.memoryCache = new Map();
    this.startCleanupInterval();
  }

  static getInstance(): AdvancedCache {
    if (!AdvancedCache.instance) {
      AdvancedCache.instance = new AdvancedCache();
    }
    return AdvancedCache.instance;
  }

  /**
   * Get data from cache with intelligent fallback
   */
  async get<T>(config: CacheConfig, fetchFn: () => Promise<T>): Promise<T> {
    const now = Date.now();
    
    // Try memory cache first (fastest)
    const memoryCached = this.memoryCache.get(config.key);
    if (memoryCached && now < memoryCached.expires) {
      console.log(`🚀 Memory cache HIT for ${config.key}`);
      return memoryCached.data;
    }

    // Try localStorage (fast)
    const localCached = this.getFromStorage<T>(config.key);
    if (localCached && now < localCached.expires) {
      console.log(`💾 Local storage cache HIT for ${config.key}`);
      // Also update memory cache for faster future access
      this.setMemoryCache(config.key, localCached);
      return localCached.data;
    }

    // Check for stale data that we can serve while revalidating
    const staleData = this.getStaleData<T>(config.key, now);
    if (staleData) {
      console.log(`⚡ Serving stale data for ${config.key} while revalidating...`);
      // Trigger background revalidation
      this.backgroundRevalidate(config, fetchFn);
      return staleData;
    }

    // No cache hit - fetch fresh data with retries
    console.log(`🔄 Cache MISS for ${config.key} - fetching fresh data...`);
    const data = await this.fetchWithRetry(fetchFn, config.retryAttempts || 3, config.retryDelay || 1000);
    
    // Cache the fresh data
    this.set(config.key, data, config.ttl, config.staleWhileRevalidate);
    
    return data;
  }

  /**
   * Set data in cache
   */
  set<T>(key: string, data: T, ttl: number, staleWhileRevalidate?: number): void {
    const now = Date.now();
    const expires = now + ttl;
    const staleExpires = staleWhileRevalidate ? expires + staleWhileRevalidate : expires;
    
    const cacheItem: CacheItem<T> = {
      data,
      expires,
      created: now,
      staleExpires
    };

    // Set in memory cache
    this.setMemoryCache(key, cacheItem);

    // Set in localStorage
    if (this.storage) {
      try {
        this.storage.setItem(key, JSON.stringify(cacheItem));
      } catch (error) {
        console.warn(`Failed to set localStorage cache for ${key}:`, error);
        // Clear some space and retry
        this.clearOldestFromStorage();
        try {
          this.storage.setItem(key, JSON.stringify(cacheItem));
        } catch (retryError) {
          console.error(`Failed to set cache even after cleanup for ${key}:`, retryError);
        }
      }
    }
  }

  /**
   * Clear specific cache entry
   */
  clear(key: string): void {
    this.memoryCache.delete(key);
    if (this.storage) {
      this.storage.removeItem(key);
    }
  }

  /**
   * Clear all cache
   */
  clearAll(): void {
    this.memoryCache.clear();
    if (this.storage) {
      const keys = [];
      for (let i = 0; i < this.storage.length; i++) {
        const key = this.storage.key(i);
        if (key && this.isCacheKey(key)) {
          keys.push(key);
        }
      }
      keys.forEach(key => this.storage.removeItem(key));
    }
  }

  /**
   * Get cache statistics
   */
  getStats() {
    return {
      memoryItems: this.memoryCache.size,
      maxMemoryItems: this.maxMemoryItems,
      storageItems: this.getStorageCacheCount(),
      storageSize: this.getStorageSize()
    };
  }

  // Private methods

  private getFromStorage<T>(key: string): CacheItem<T> | null {
    if (!this.storage) return null;
    
    try {
      const cached = this.storage.getItem(key);
      if (cached) {
        return JSON.parse(cached);
      }
    } catch (error) {
      console.warn(`Failed to parse cached data for ${key}:`, error);
      this.storage.removeItem(key);
    }
    return null;
  }

  private getStaleData<T>(key: string, now: number): T | null {
    // Check memory first
    const memoryCached = this.memoryCache.get(key);
    if (memoryCached && memoryCached.staleExpires && now < memoryCached.staleExpires) {
      return memoryCached.data;
    }

    // Check localStorage
    const localCached = this.getFromStorage<T>(key);
    if (localCached && localCached.staleExpires && now < localCached.staleExpires) {
      return localCached.data;
    }

    return null;
  }

  private setMemoryCache<T>(key: string, item: CacheItem<T>): void {
    // Implement LRU eviction
    if (this.memoryCache.size >= this.maxMemoryItems) {
      const firstKey = this.memoryCache.keys().next().value;
      this.memoryCache.delete(firstKey);
    }
    this.memoryCache.set(key, item);
  }

  private async fetchWithRetry<T>(
    fetchFn: () => Promise<T>, 
    attempts: number, 
    delay: number
  ): Promise<T> {
    for (let i = 0; i < attempts; i++) {
      try {
        return await fetchFn();
      } catch (error) {
        console.warn(`Fetch attempt ${i + 1} failed:`, error);
        
        if (i === attempts - 1) {
          throw error; // Last attempt failed
        }
        
        // Exponential backoff
        await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
      }
    }
    throw new Error('All retry attempts failed');
  }

  private async backgroundRevalidate<T>(config: CacheConfig, fetchFn: () => Promise<T>): Promise<void> {
    try {
      const freshData = await fetchFn();
      this.set(config.key, freshData, config.ttl, config.staleWhileRevalidate);
      console.log(`✅ Background revalidation completed for ${config.key}`);
    } catch (error) {
      console.warn(`❌ Background revalidation failed for ${config.key}:`, error);
    }
  }

  private startCleanupInterval(): void {
    if (typeof window === 'undefined') return;
    
    setInterval(() => {
      this.cleanupExpiredItems();
    }, 5 * 60 * 1000); // Cleanup every 5 minutes
  }

  private cleanupExpiredItems(): void {
    const now = Date.now();
    
    // Cleanup memory cache
    for (const [key, item] of this.memoryCache.entries()) {
      if (now > (item.staleExpires || item.expires)) {
        this.memoryCache.delete(key);
      }
    }

    // Cleanup localStorage
    if (!this.storage) return;
    
    const keysToRemove: string[] = [];
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key && this.isCacheKey(key)) {
        const cached = this.getFromStorage(key);
        if (cached && now > (cached.staleExpires || cached.expires)) {
          keysToRemove.push(key);
        }
      }
    }
    
    keysToRemove.forEach(key => this.storage.removeItem(key));
    
    if (keysToRemove.length > 0) {
      console.log(`🧹 Cleaned up ${keysToRemove.length} expired cache items`);
    }
  }

  private clearOldestFromStorage(): void {
    if (!this.storage) return;
    
    const cacheItems: { key: string; created: number }[] = [];
    
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key && this.isCacheKey(key)) {
        const cached = this.getFromStorage(key);
        if (cached) {
          cacheItems.push({ key, created: cached.created });
        }
      }
    }
    
    // Sort by creation time and remove oldest 20%
    cacheItems.sort((a, b) => a.created - b.created);
    const toRemove = Math.ceil(cacheItems.length * 0.2);
    
    for (let i = 0; i < toRemove; i++) {
      this.storage.removeItem(cacheItems[i].key);
    }
  }

  private isCacheKey(key: string): boolean {
    return key.includes('_cache') || key.includes('api_');
  }

  private getStorageCacheCount(): number {
    if (!this.storage) return 0;
    
    let count = 0;
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key && this.isCacheKey(key)) {
        count++;
      }
    }
    return count;
  }

  private getStorageSize(): string {
    if (!this.storage) return '0 B';
    
    let totalSize = 0;
    for (let i = 0; i < this.storage.length; i++) {
      const key = this.storage.key(i);
      if (key && this.isCacheKey(key)) {
        const value = this.storage.getItem(key);
        if (value) {
          totalSize += new Blob([value]).size;
        }
      }
    }
    
    return this.formatBytes(totalSize);
  }

  private formatBytes(bytes: number): string {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  }
}

// Convenience functions for common cache patterns
export const cache = AdvancedCache.getInstance();

export const cacheAPI = async <T>(
  endpoint: string, 
  fetchFn: () => Promise<T>,
  ttl: number = 30 * 60 * 1000, // 30 minutes default
  staleWhileRevalidate: number = 60 * 60 * 1000 // 1 hour stale-while-revalidate
): Promise<T> => {
  return cache.get({
    key: `api_${endpoint}`,
    ttl,
    staleWhileRevalidate,
    retryAttempts: 3,
    retryDelay: 1000
  }, fetchFn);
};

// Export for direct use in components
export default AdvancedCache;