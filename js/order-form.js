(() => {
  "use strict";
  const form = document.querySelector("#service-order-form");
  if (!form) return;
  const button = form.querySelector("[data-submit]");
  const status = form.querySelector("[data-form-status]");
  const setStatus = (message, state) => {
    status.textContent = message;
    status.dataset.state = state || "";
  };
  form.addEventListener("submit", async event => {
    event.preventDefault();
    if (button.disabled || !form.reportValidity()) return;
    if (form.elements.botcheck?.checked) return;
    if (!window.GGCOrderCart?.getIds().length) {
      setStatus(document.documentElement.lang === "ru" ? "Добавьте хотя бы одну услугу." : "Add at least one service.", "error");
      return;
    }
    button.disabled = true;
    const original = button.textContent;
    button.textContent = document.documentElement.lang === "ru" ? "Отправка…" : "Sending…";
    setStatus(document.documentElement.lang === "ru" ? "Передача заявки…" : "Submitting request…", "pending");
    try {
      const response = await fetch("https://api.web3forms.com/submit", {
        method:"POST",
        body:new FormData(form),
        headers:{Accept:"application/json"}
      });
      let result;
      try { result = await response.json(); }
      catch (_) { throw new Error("Invalid provider response"); }
      if (!response.ok || result.success !== true) {
        throw new Error(result.message || "Provider rejected submission");
      }
      setStatus(document.documentElement.lang === "ru" ? "Заявка принята сервисом. Это не подтверждение договора или оплаты." : "Request accepted by the form provider. This is not a contract or payment confirmation.", "success");
      form.reset();
      window.GGCOrderCore.write([]);
      await window.GGCOrderCart.renderCart();
    } catch (error) {
      setStatus((document.documentElement.lang === "ru" ? "Не удалось отправить заявку: " : "Submission failed: ") + error.message + (document.documentElement.lang === "ru" ? " Данные сохранены — попробуйте ещё раз." : " Your entries are preserved; please retry."), "error");
    } finally {
      button.disabled = false;
      button.textContent = original;
    }
  });
})();
