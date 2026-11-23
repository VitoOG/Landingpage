(() => {
  "use strict";

  const lang = document.body.dataset.lang;
  const source = document.body.dataset.catalogUrl;
  const grid = document.querySelector("#catalog-grid");
  const filters = document.querySelector("#catalog-filters");
  const search = document.querySelector("#catalog-search");
  const count = document.querySelector("#catalog-count");
  const error = document.querySelector("#catalog-error");
  const dialog = document.querySelector("#offer-dialog");
  const dialogContent = document.querySelector("#offer-dialog-content");

  const ui = {
    en: {
      all: "All categories", results: n => `${n} of 33 offers`,
      empty: "No offers match the search. Try another phrase or category.",
      detail: "View scope and details ↗", buyer: "Suitable for",
      problem: "Problem addressed", deliverables: "Deliverables",
      scope: "Scope and exclusions", recurring: "Ongoing support",
      billing: "Billing model", request: "Request a proposal ↗",
      priceNote: "Indicative price. Final scope and price are agreed before work begins.", add: "Add to request"
    },
    ru: {
      all: "Все направления", results: n => `Показано ${n} из 33 предложений`,
      empty: "Ничего не найдено. Измените запрос или категорию.",
      detail: "Подробнее об объёме ↗", buyer: "Для кого",
      problem: "Решаемая проблема", deliverables: "Результат работы",
      scope: "Объём и исключения", recurring: "Сопровождение",
      billing: "Модель оплаты", request: "Запросить предложение ↗",
      priceNote: "Ориентировочная цена. Итоговый объём и стоимость согласуются до начала работы.", add: "Добавить в заявку"
    }
  }[lang];

  const make = (tag, className, value) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (value !== undefined) node.textContent = value;
    return node;
  };

  let offers = [];
  let activeCategory = "";

  function showDetails(offer) {
    dialogContent.replaceChildren();

    dialogContent.append(
      make("p", "eyebrow", `${offer.id} / ${offer.category}`),
      make("h2", "", offer.name),
      make("p", "dialog-price", offer.price)
    );

    for (const [key, label] of [
      ["buyer", ui.buyer],
      ["problem", ui.problem],
      ["deliverables", ui.deliverables],
      ["scope", ui.scope],
      ["recurring", ui.recurring],
      ["billing", ui.billing]
    ]) {
      const field = make("section", "dialog-field");
      field.append(make("strong", "", label), make("p", "", offer[key]));
      dialogContent.append(field);
    }

    dialogContent.append(make("p", "catalog-note", ui.priceNote));

    const add = make("button", "button button-primary dialog-action catalog-add", ui.add);
    add.type = "button"; add.dataset.addOffer = offer.id;
    dialogContent.append(add);
    window.GGCOrderCart?.syncButtons();

    dialog.showModal();
  }

  function renderFilters() {
    filters.replaceChildren();

    const categories = ["", ...new Set(offers.map(o => o.category))];
    for (const category of categories) {
      const button = make("button", "catalog-filter", category || ui.all);
      button.type = "button";
      button.classList.toggle("is-active", category === activeCategory);
      button.setAttribute("aria-pressed", String(category === activeCategory));
      button.addEventListener("click", () => {
        activeCategory = category;
        renderFilters();
        render();
      });
      filters.append(button);
    }
  }

  function render() {
    const query = search.value.trim().toLocaleLowerCase(lang);
    const visible = offers.filter(o => {
      const categoryMatch = !activeCategory || o.category === activeCategory;
      const searchable = [
        o.id, o.category, o.name, o.price, o.buyer,
        o.problem, o.deliverables, o.scope, o.recurring, o.billing
      ].join(" ").toLocaleLowerCase(lang);
      return categoryMatch && searchable.includes(query);
    });

    count.textContent = ui.results(visible.length);
    grid.replaceChildren();

    if (!visible.length) {
      grid.append(make("p", "catalog-empty", ui.empty));
      return;
    }

    for (const offer of visible) {
      const card = make("article", "catalog-card");
      const meta = make("div", "catalog-card-meta");
      meta.append(
        make("span", "catalog-id", offer.id),
        make("span", "catalog-category", offer.category)
      );

      card.append(
        meta,
        make("h2", "", offer.name),
        make("p", "catalog-problem", offer.problem),
        make("p", "catalog-deliverables", offer.deliverables)
      );

      const priceRow = make("div", "catalog-price-row");
      priceRow.append(
        make("strong", "catalog-price", offer.price),
        make("span", "catalog-billing", offer.billing)
      );
      card.append(priceRow);

      const details = make("button", "catalog-details", ui.detail);
      details.type = "button";
      details.addEventListener("click", () => showDetails(offer));
      const add = make("button", "button button-primary catalog-add", ui.add);
      add.type = "button"; add.dataset.addOffer = offer.id;
      const actions = make("div", "catalog-card-actions"); actions.append(details, add);
      card.append(actions);
      grid.append(card);
    }
    window.GGCOrderCart?.syncButtons();
  }

  async function init() {
    try {
      const response = await fetch(source, { credentials: "same-origin" });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const payload = await response.json();

      if (!Array.isArray(payload.offers) || payload.offers.length !== 33) {
        throw new Error("Catalogue must contain exactly 33 offers");
      }

      offers = payload.offers;
      renderFilters();
      render();
    } catch (err) {
      error.hidden = false;
      error.textContent = `Catalogue loading failed: ${err.message}`;
      count.textContent = "";
    }
  }

  search.addEventListener("input", render);
  init();
})();
