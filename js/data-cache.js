/** Stale-While-Revalidate — sessionStorage 缓存 JSON，首屏即时渲染 */

const DataCache = (() => {
  const PREFIX = "sxq:data:";
  const VERSION = "v1";

  function key(url) {
    return `${PREFIX}${VERSION}:${url}`;
  }

  function get(url) {
    try {
      const raw = sessionStorage.getItem(key(url));
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (!parsed?.data) return null;
      return parsed;
    } catch {
      return null;
    }
  }

  function set(url, data) {
    try {
      const updatedAt = data?.updatedAt || data?.generatedAt || null;
      sessionStorage.setItem(
        key(url),
        JSON.stringify({ data, updatedAt, cachedAt: Date.now() })
      );
    } catch {
      /* quota */
    }
  }

  async function fetchJson(url, { onStale, onFresh } = {}) {
    const cached = get(url);
    if (cached && typeof onStale === "function") {
      onStale(cached.data, cached.updatedAt);
    }

    const res = await fetch(`${url}?t=${Date.now()}`, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json();
    const updatedAt = data?.updatedAt || data?.generatedAt || null;

    if (!cached || cached.updatedAt !== updatedAt) {
      set(url, data);
      if (typeof onFresh === "function") onFresh(data, updatedAt);
    }
    return data;
  }

  return { get, set, fetchJson };
})();
