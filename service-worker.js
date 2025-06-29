const cacheName = 'putujgovori-v8';
const assets = [
  './',
  './index.html',
  './manifest.json',
  './lessons.json',
  './lessons_intermediate.json',
  './lessons_advanced.json',
  './icon-192.png',
  './icon-512.png',
  './service-worker.js'
];

// Install event - cache app shell
self.addEventListener('install', event => {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(cacheName).then(cache => {
      console.log('Caching app shell');
      return cache.addAll(assets);
    }).then(() => {
      console.log('Service Worker installed');
      return self.skipWaiting();
    })
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', event => {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames.map(cacheName => {
          if (cacheName !== cacheName) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      console.log('Service Worker activated');
      // Notify all clients that service worker is ready
      self.clients.claim().then(() => {
        self.clients.matchAll().then(clients => {
          clients.forEach(client => {
            client.postMessage({
              type: 'SW_ACTIVATED',
              version: cacheName
            });
          });
        });
      });
      return self.clients.claim();
    })
  );
});

// Fetch event - serve from cache first, then network
self.addEventListener('fetch', event => {
  // Skip non-GET requests
  if (event.request.method !== 'GET') {
    return;
  }

  // Skip chrome-extension requests
  if (event.request.url.startsWith('chrome-extension://')) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(response => {
      // Return cached version if available
      if (response) {
        console.log('Serving from cache:', event.request.url);
        return response;
      }

      // Otherwise fetch from network
      return fetch(event.request).then(fetchResponse => {
        // Don't cache if not a valid response
        if (!fetchResponse || fetchResponse.status !== 200 || fetchResponse.type !== 'basic') {
          return fetchResponse;
        }

        // Clone the response
        const responseToCache = fetchResponse.clone();

        // Cache the response for static assets
        if (event.request.url.includes('.json') || 
            event.request.url.includes('.html') || 
            event.request.url.includes('.png') ||
            event.request.url.includes('.js') ||
            event.request.url.includes('.css')) {
          
          caches.open(cacheName).then(cache => {
            console.log('Caching new response:', event.request.url);
            cache.put(event.request, responseToCache);
          });
        }

        return fetchResponse;
      }).catch(() => {
        // Return offline page for navigation requests
        if (event.request.destination === 'document') {
          return caches.match('./index.html');
        }
      });
    })
  );
});

// Background sync for offline functionality
self.addEventListener('sync', event => {
  console.log('Background sync triggered:', event.tag);
});

// Push notification handling
self.addEventListener('push', event => {
  console.log('Push notification received:', event);
  
  const options = {
    body: 'Nova lekcija je dostupna!',
    icon: './icon-192.png',
    badge: './icon-192.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: 1
    }
  };

  event.waitUntil(
    self.registration.showNotification('PutujGovori', options)
  );
});

// Notification click handling
self.addEventListener('notificationclick', event => {
  console.log('Notification clicked:', event);
  
  event.notification.close();
  
  event.waitUntil(
    clients.openWindow('./index.html')
  );
});

// Message handling for update notifications
self.addEventListener('message', event => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: cacheName });
  }
});
