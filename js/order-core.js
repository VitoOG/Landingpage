(() => {
  "use strict";
  const KEY = "ggc-service-request-v1";
  const MAX_ITEMS = 33;
  const valid = id => typeof id === "string" && /^SE-(0[1-9]|[12][0-9]|3[0-3])$/.test(id);
  const normalize = ids => [...new Set(Array.isArray(ids) ? ids.filter(valid) : [])].slice(0, MAX_ITEMS);
  const read = () => {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return [];
      return normalize(JSON.parse(raw));
    } catch (_) { return []; }
  };
  const write = ids => {
    try { localStorage.setItem(KEY, JSON.stringify(normalize(ids))); return true; }
    catch (_) { return false; }
  };
  window.GGCOrderCore = Object.freeze({
    key: KEY, read, write,
    add: (ids, id) => valid(id) ? normalize([...ids, id]) : normalize(ids),
    remove: (ids, id) => normalize(ids).filter(x => x !== id),
    has: (ids, id) => normalize(ids).includes(id)
  });
})();
