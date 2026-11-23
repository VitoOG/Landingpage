(() => {
  "use strict";
  const KEY = "ggc-service-request-v1";
  const MAX_ITEMS = 33;
  const read = () => {
    try {
      const raw = localStorage.getItem(KEY);
      if (!raw) return [];
      const value = JSON.parse(raw);
      if (!Array.isArray(value)) return [];
      return [...new Set(value.filter(x => typeof x === "string" && /^SE-(0[1-9]|[12][0-9]|3[0-3])$/.test(x)))].slice(0, MAX_ITEMS);
    } catch (_) { return []; }
  };
  const write = ids => {
    try { localStorage.setItem(KEY, JSON.stringify([...new Set(ids)].slice(0, MAX_ITEMS))); return true; }
    catch (_) { return false; }
  };
  window.GGCOrderCore = Object.freeze({
    key: KEY,
    read,
    write,
    add: (ids, id) => ids.includes(id) ? ids : [...ids, id].slice(0, MAX_ITEMS),
    remove: (ids, id) => ids.filter(x => x !== id),
    has: (ids, id) => ids.includes(id)
  });
})();
