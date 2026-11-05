(() => {
  "use strict";

  const toggle = document.querySelector(".nav-toggle");
  const navigation = document.querySelector("#primary-navigation");
  const year = document.querySelector("#current-year");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  if (!toggle || !navigation) return;

  const closeNavigation = () => {
    toggle.setAttribute("aria-expanded", "false");
    navigation.classList.remove("is-open");
  };

  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    toggle.setAttribute("aria-expanded", String(!isOpen));
    navigation.classList.toggle("is-open", !isOpen);
  });

  navigation.addEventListener("click", (event) => {
    if (event.target instanceof Element && event.target.closest("a")) {
      closeNavigation();
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeNavigation();
  });

  document.addEventListener("click", (event) => {
    if (!(event.target instanceof Node)) return;
    if (!navigation.contains(event.target) && !toggle.contains(event.target)) {
      closeNavigation();
    }
  });
})();
