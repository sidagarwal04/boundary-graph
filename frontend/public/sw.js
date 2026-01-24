// Service Worker for Boundary Graph
// Enhanced caching for mobile performance

const CACHE_NAME = 'boundary-graph-v1';
const API_CACHE_NAME = 'boundary-graph-api-v1';

// Assets to cache immediately
const STATIC_ASSETS = [
  '/',
  '/bg-logo.png',
  '/icon.png',
  '/icon-512.png',
  '/manifest.json'
];

// API endpoints to cache with different strategies
const API_ENDPOINTS = [
  '/api/overview',
  '/api/batsmen/top',
  '/api/bowlers/top',
  '/api/teams',
  '/api/venues'
];

// Install event - cache static assets
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('📦 Caching static assets...');
        return cache.addAll(STATIC_ASSETS);
      })
      .then(() => {
        console.log('✅ Static assets cached successfully');
        return self.skipWaiting();
      })
      .catch(err => {
        console.error('❌ Cache installation failed:', err);
      })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME && cacheName !== API_CACHE_NAME) {
              console.log('🗑️ Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ Cache cleanup completed');
        return self.clients.claim();
      })
  );
});

// Fetch event - implement caching strategies
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // Handle API requests with network-first strategy
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      networkFirstStrategy(request, API_CACHE_NAME)
    );
    return;
  }

  // Handle static assets with cache-first strategy
  if (request.method === 'GET' && 
      (request.destination === 'document' || 
       request.destination === 'script' || 
       request.destination === 'style' ||
       request.destination === 'image')) {
    event.respondWith(
      cacheFirstStrategy(request, CACHE_NAME)
    );
    return;
  }
});

// Network-first strategy for API calls
async function networkFirstStrategy(request, cacheName) {
  try {
    // Try network first
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache successful response for mobile users
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
      
      console.log('📡 Network response cached:', request.url);
      return networkResponse;
    }
    
    throw new Error('Network response not ok');
  } catch (error) {
    // Fall back to cache
    console.log('🔄 Network failed, trying cache for:', request.url);
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      console.log('📋 Serving from cache:', request.url);
      return cachedResponse;
    }
    
    // Return offline fallback for API calls
    return new Response(
      JSON.stringify({ 
        error: 'Offline', 
        message: 'Data temporarily unavailable. Please check your connection.' 
      }),
      {
        status: 503,
        statusText: 'Service Unavailable',
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Cache-first strategy for static assets
async function cacheFirstStrategy(request, cacheName) {
  try {
    // Try cache first
    const cachedResponse = await caches.match(request);
    
    if (cachedResponse) {
      console.log('⚡ Serving from cache:', request.url);
      return cachedResponse;
    }
    
    // Fall back to network
    console.log('📡 Cache miss, fetching from network:', request.url);
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      // Cache for future use
      const cache = await caches.open(cacheName);
      cache.put(request, networkResponse.clone());
      console.log('📦 Cached new resource:', request.url);
    }
    
    return networkResponse;
  } catch (error) {
    console.error('❌ Both cache and network failed for:', request.url);
    
    // Return a basic offline page for navigation requests
    if (request.mode === 'navigate') {
      return new Response(
        `<!DOCTYPE html>
        <html>
          <head>
            <title>Boundary Graph - Offline</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
              body { font-family: system-ui, sans-serif; text-align: center; padding: 2rem; }
              .offline { color: #64748b; }
            </style>
          </head>
          <body>
            <h1>🏏 Boundary Graph</h1>
            <p class="offline">You're offline. Please check your connection.</p>
          </body>
        </html>`,
        { 
          headers: { 'Content-Type': 'text/html' } 
        }
      );
    }
    
    throw error;
  }
}

// Background sync for mobile data efficiency
self.addEventListener('sync', event => {
  if (event.tag === 'background-sync-api') {
    event.waitUntil(
      syncApiData()
    );
  }
});

// Sync essential API data in background
async function syncApiData() {
  try {
    console.log('🔄 Background syncing API data...');
    
    const cache = await caches.open(API_CACHE_NAME);
    const baseUrl = 'https://boundary-graph.onrender.com';
    
    // Sync essential endpoints
    const endpoints = [
      '/api/overview',
      '/api/batsmen/top?limit=20',
      '/api/bowlers/top?limit=20'
    ];
    
    for (const endpoint of endpoints) {
      try {
        const response = await fetch(baseUrl + endpoint);
        if (response.ok) {
          await cache.put(endpoint, response);
          console.log('✅ Synced:', endpoint);
        }
      } catch (err) {
        console.log('⚠️ Sync failed for:', endpoint, err.message);
      }
    }
    
    console.log('✅ Background sync completed');
  } catch (error) {
    console.error('❌ Background sync failed:', error);
  }
}

// Message handling for cache management
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'CLEAR_CACHE') {
    event.waitUntil(
      caches.keys().then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => caches.delete(cacheName))
        );
      })
    );
  }
});