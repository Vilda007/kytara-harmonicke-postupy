const CACHE_NAME = 'guitar-harmony-v1';
const ASSETS_TO_CACHE = [
  '/',
  '/index.html',
  '/app.v1.js',
  '/app.v1.css',
  '/chords.json',
  '/manifest.json',
  '/favicon-180.png',
  '/favicon-32.png',
  '/favicon.svg'
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS_TO_CACHE);
    })
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return response || fetch(event.request);
    })
  );
});
