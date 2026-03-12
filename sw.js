const CACHE_NAME = 'babula-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/icon.svg',
  '/qr_platba.png',
  '/manifest.json'
];

// Install: cache core assets (not audio — too large, cache on demand)
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

// Activate: clean old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Fetch: cache-first for cached assets, network-first for audio (cache after fetch)
self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Audio files: network first, cache for offline
  if (url.pathname.startsWith('/Audio_files/')) {
    e.respondWith(
      fetch(e.request)
        .then((response) => {
          const clone = response.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, clone));
          return response;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Everything else: cache first
  e.respondWith(
    caches.match(e.request).then((cached) => cached || fetch(e.request))
  );
});
