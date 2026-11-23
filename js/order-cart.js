(() => {
  "use strict";
  const core = window.GGCOrderCore;
  if (!core) return;
  const lang = document.documentElement.lang === "ru" ? "ru" : "en";
  const labels = lang === "ru"
    ? {added:"Добавлено", add:"Добавить в заявку", count:n=>`Корзина, ${n} услуг`}
    : {added:"Added", add:"Add to request", count:n=>`Cart, ${n} services`};
  let ids = core.read();
  const save = () => { core.write(ids); update(); };
  function update() {
    document.querySelectorAll("[data-cart-count]").forEach(el => { el.textContent = String(ids.length); });
    document.querySelectorAll(".nav-cart").forEach(el => el.setAttribute("aria-label", labels.count(ids.length)));
    syncButtons();
  }
  function syncButtons() {
    document.querySelectorAll("[data-add-offer]").forEach(btn => {
      const added = ids.includes(btn.dataset.addOffer);
      btn.classList.toggle("is-added", added);
      btn.textContent = added ? labels.added : labels.add;
      btn.setAttribute("aria-pressed", String(added));
    });
  }
  function add(id) {
    if (!/^SE-(0[1-9]|[12][0-9]|3[0-3])$/.test(id)) return;
    ids = core.add(ids, id); save();
  }
  document.addEventListener("click", event => {
    const addButton = event.target.closest("[data-add-offer]");
    if (addButton) {
      add(addButton.dataset.addOffer);
      if (document.querySelector("#offer-dialog")?.open) document.querySelector("#offer-dialog").close();
      return;
    }
    const removeButton = event.target.closest("[data-remove-offer]");
    if (removeButton) {
      ids = core.remove(ids, removeButton.dataset.removeOffer);
      save();
      renderCart();
    }
  });
  async function renderCart() {
    const root = document.querySelector("[data-cart-items]");
    if (!root) return;
    const dataUrl = root.dataset.catalogUrl;
    try {
      const response = await fetch(dataUrl, {credentials:"same-origin"});
      if (!response.ok) throw new Error("Catalogue unavailable");
      const data = await response.json();
      const offers = new Map(data.offers.map(x => [x.id, x]));
      ids = ids.filter(id => offers.has(id));
      core.write(ids);
      root.replaceChildren();
      const empty = document.querySelector("[data-cart-empty]");
      const form = document.querySelector("[data-order-form]");
      if (!ids.length) {
        empty.hidden = false;
        form.hidden = true;
        update();
        return;
      }
      empty.hidden = true;
      form.hidden = false;
      for (const id of ids) {
        const offer = offers.get(id);
        const item = document.createElement("article");
        item.className = "request-item";
        const info = document.createElement("div");
        const title = document.createElement("h3"); title.textContent = offer.name;
        const meta = document.createElement("p"); meta.textContent = id + " · " + offer.category;
        const price = document.createElement("p"); price.className = "request-price"; price.textContent = offer.price + " · " + offer.billing;
        info.append(meta, title, price);
        const remove = document.createElement("button");
        remove.type = "button"; remove.className = "request-remove";
        remove.dataset.removeOffer = id;
        remove.textContent = lang === "ru" ? "Убрать" : "Remove";
        item.append(info, remove); root.append(item);
      }
      const hidden = document.querySelector("[name=selected_services]");
      if (hidden) hidden.value = ids.map(id => {
        const o=offers.get(id); return id + " | " + o.name + " | " + o.price + " | " + o.billing;
      }).join("\n");
      update();
    } catch (_) {
      root.textContent = lang === "ru" ? "Не удалось загрузить каталог. Обновите страницу." : "Could not load catalogue. Refresh the page.";
    }
  }
  window.GGCOrderCart = Object.freeze({syncButtons, renderCart, getIds:()=>[...ids]});
  update();
  renderCart();
})();
