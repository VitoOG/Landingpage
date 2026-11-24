(() => {
  "use strict";

  const lang = document.body.dataset.lang || document.documentElement.lang || "en";
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
      priceNote: "Indicative price. Final scope and price are agreed before work begins."
    },
    ru: {
      all: "Все направления", results: n => `Показано ${n} из 33 предложений`,
      empty: "Ничего не найдено. Измените запрос или категорию.",
      detail: "Подробнее об объёме ↗", buyer: "Для кого",
      problem: "Решаемая проблема", deliverables: "Результат работы",
      scope: "Объём и исключения", recurring: "Сопровождение",
      billing: "Модель оплаты", request: "Запросить предложение ↗",
      priceNote: "Ориентировочная цена. Итоговый объём и стоимость согласуются до начала работы."
    },
    es: {
      all: "Todas las categorías", results: n => `${n} de 33 servicios`,
      empty: "No hay servicios que coincidan. Pruebe otra búsqueda o categoría.",
      detail: "Ver alcance y detalles ↗", buyer: "Dirigido a",
      problem: "Problema que aborda", deliverables: "Entregables",
      scope: "Alcance y exclusiones", recurring: "Soporte continuo",
      billing: "Modalidad de contratación", request: "Solicitar propuesta ↗",
      priceNote: "Precio orientativo. El alcance y el precio definitivos se acuerdan antes de comenzar."
    },
    fr: {
      all: "Toutes les catégories", results: n => `${n} offres sur 33`,
      empty: "Aucune offre ne correspond. Essayez une autre recherche ou catégorie.",
      detail: "Voir le périmètre et les détails ↗", buyer: "Public concerné",
      problem: "Problème traité", deliverables: "Livrables",
      scope: "Périmètre et exclusions", recurring: "Assistance continue",
      billing: "Modalité de facturation", request: "Demander une proposition ↗",
      priceNote: "Prix indicatif. Le périmètre et le prix définitifs sont convenus avant le début des travaux."
    }
  }[lang];

  if (!ui) {
    error.hidden = false;
    error.textContent = `Unsupported catalogue language: ${lang}`;
    count.textContent = "";
    return;
  }

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

    const link = make("a", "button button-primary dialog-action", ui.request);
    const subject = encodeURIComponent(`${offer.id} — ${offer.name}`);
    const inquiryFields = {
      en: ["Company / project:", "Task:", "Expected result:", "Timeframe:", "Budget:"],
      ru: ["Компания / проект:", "Задача:", "Ожидаемый результат:", "Сроки:", "Бюджет:"],
      es: ["Empresa / proyecto:", "Tarea:", "Resultado esperado:", "Plazo:", "Presupuesto:"],
      fr: ["Entreprise / projet :", "Mission :", "Résultat attendu :", "Échéance :", "Budget :"]
    }[lang];
    const body = encodeURIComponent(`${offer.name}\\n\\n${inquiryFields.join("\\n")}\\n`);
    link.href = `mailto:viksim1221@gmail.com?subject=${subject}&body=${body}`;
    dialogContent.append(link);

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
      card.append(details);
      grid.append(card);
    }
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
