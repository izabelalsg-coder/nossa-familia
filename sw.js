const CACHE = 'nossa-familia-v8';
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(['/nossa-familia/', '/nossa-familia/index.html'])).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))));
self.addEventListener('fetch', e => {
  if (e.request.url.includes('googleapis.com') || e.request.url.includes('fonts.g')) return;
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).catch(() => caches.match('/nossa-familia/index.html'))));
});
