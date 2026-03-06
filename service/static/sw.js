self.addEventListener('install', function(event) {
  console.log('Service Worker installed.');
});

self.addEventListener('fetch', function(event) {
  // Poți adăuga caching aici
});
