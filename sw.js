const CACHE = 'budget-bites-v1';
const PRECACHE = [
  '/budget-bites/',
  '/budget-bites/index.html',
  '/budget-bites/manifest.json',
  '/budget-bites/images/icons/icon-192.png',
  '/budget-bites/images/icons/icon-512.png',
  '/budget-bites/data/restaurants_i18n.json',
  '/budget-bites/vendor/leaflet.css',
  '/budget-bites/vendor/leaflet.js',
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(PRECACHE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // Only handle GET requests for same-origin or cached assets
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);

  // Let Supabase and external API calls go straight to network
  if (url.hostname !== location.hostname) return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      const network = fetch(e.request).then(res => {
        if (res.ok) {
          caches.open(CACHE).then(c => c.put(e.request, res.clone()));
        }
        return res;
      });
      return cached || network;
    })
  );
});
