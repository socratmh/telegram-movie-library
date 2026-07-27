import { useEffect, useRef } from 'react';
import { trackVisit } from '../api/client';

/**
 * Lightweight visitor tracking hook.
 * Generates a persistent visitor_id in localStorage and sends
 * a beacon on each page path change.
 */
export default function useTracking() {
  const lastPath = useRef('');

  useEffect(() => {
    // Generate or retrieve persistent visitor ID
    let visitorId = localStorage.getItem('_vid');
    if (!visitorId) {
      visitorId = crypto.randomUUID
        ? crypto.randomUUID()
        : 'v-' + Math.random().toString(36).slice(2) + Date.now().toString(36);
      localStorage.setItem('_vid', visitorId);
    }

    const sendBeacon = () => {
      const path = window.location.pathname + window.location.hash;
      if (path === lastPath.current) return;
      lastPath.current = path;

      trackVisit({
        visitor_id: visitorId,
        page: path,
        referrer: document.referrer || '',
        screen_width: window.screen?.width || window.innerWidth,
      });
    };

    // Track initial page load
    sendBeacon();

    // Track hash/popstate changes (SPA navigation)
    window.addEventListener('hashchange', sendBeacon);
    window.addEventListener('popstate', sendBeacon);

    // Also track pushState calls (React Router uses these)
    const origPush = history.pushState;
    history.pushState = function (...args) {
      origPush.apply(this, args);
      setTimeout(sendBeacon, 0);
    };

    return () => {
      window.removeEventListener('hashchange', sendBeacon);
      window.removeEventListener('popstate', sendBeacon);
      history.pushState = origPush;
    };
  }, []);
}
