const CACHE = 'nossa-familia-v6';
self.addEventListener('install', e => e.waitUntil(caches.open(CACHE).then(c => c.addAll(['/nossa-familia/', '/nossa-familia/index.html'])).then(() => self.skipWaiting())));
self.addEventListener('activate', e => e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))));
self.addEventListener('fetch', e => {
  if (e.request.url.includes('googleapis.com') || e.request.url.includes('fonts.g')) return;
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).catch(() => caches.match('/nossa-familia/index.html'))));
});

// ── NOTIFICAÇÃO DIÁRIA ÀS 9H ─────────────────────────────────────────────────
self.addEventListener('message', e => {
  if (e.data && e.data.type === 'SCHEDULE_NOTIFICATION') {
    scheduleDaily();
  }
});

function scheduleDaily() {
  const now = new Date();
  const next = new Date();
  next.setHours(9, 0, 0, 0);
  if (now >= next) next.setDate(next.getDate() + 1);
  const delay = next - now;
  setTimeout(() => {
    self.registration.showNotification('Nossa Família 🕊️', {
      body: 'Bom dia! O devocional de hoje está esperando por você.',
      icon: '/nossa-familia/icon-192.png',
      badge: '/nossa-familia/icon-192.png',
      tag: 'devocional-diario',
      renotify: true,
      data: { url: '/nossa-familia/' }
    });
    scheduleDaily();
  }, delay);
}

self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(clients.openWindow(e.notification.data.url || '/nossa-familia/'));
});
