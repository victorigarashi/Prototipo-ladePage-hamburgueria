const CATEGORY_ORDER = ["Lanches", "Combos", "Acompanhamentos", "Bebidas", "Sobremesas"];

const header = document.querySelector(".header");
const navToggle = document.querySelector(".nav-toggle");
const navMenu = document.querySelector(".nav-menu");
const navLinks = document.querySelectorAll(".nav-link");
const backToTop = document.querySelector(".back-to-top");
const categoryMenu = document.querySelector("#category-menu");
const comboGrid = document.querySelector("#combo-grid");
const menuTabs = document.querySelector("#menu-tabs");
const sections = document.querySelectorAll("main section[id]");

let catalogItems = [];
let currentFilter = "Todos";

function money(value) {
  return Number(value).toLocaleString("pt-BR", { style: "currency", currency: "BRL" });
}

function escapeHTML(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

async function api(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) throw new Error("Erro ao carregar dados da API.");
  return response.json();
}

function openWhatsApp(product) {
  const message = `Olá! Gostaria de fazer o seguinte pedido:\n\n${product.name}\nCategoria: ${product.category}\nValor: ${money(product.price)}\n\nPoderia me informar o tempo de entrega?`;
  window.open(`https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`, "_blank", "noopener,noreferrer");
}

function configureWhatsAppLinks() {
  const message = encodeURIComponent("Olá! Gostaria de fazer um pedido.");
  document.querySelectorAll('a[href*="wa.me"]').forEach((link) => {
    link.href = `https://wa.me/${WHATSAPP_NUMBER}?text=${message}`;
  });
}

function bindOrderButtons(scope = document) {
  scope.querySelectorAll("[data-order]").forEach((button) => {
    button.addEventListener("click", () => {
      if (button.disabled) return;
      openWhatsApp({
        name: button.dataset.name,
        category: button.dataset.category,
        price: button.dataset.price
      });
    });
  });
}

function productCard(product) {
  const soldOut = !product.is_available;
  const name = escapeHTML(product.name);
  const category = escapeHTML(product.category);

  return `
    <article class="product-card ${soldOut ? "product-card--soldout" : ""}">
      ${product.badge ? `<span class="card-badge">${escapeHTML(product.badge)}</span>` : ""}
      <img src="${escapeHTML(product.image_url || "images/burger-classic.svg")}" alt="${name}">
      <div class="product-card__body">
        ${soldOut ? '<span class="status-pill status-pill--soldout">Esgotado</span>' : ""}
        <small>${category}</small>
        <h3>${name}</h3>
        <p>${escapeHTML(product.description)}</p>
        <div class="product-card__footer">
          <strong>${money(product.price)}</strong>
          <button
            class="btn btn--whatsapp"
            type="button"
            data-order
            data-name="${name}"
            data-category="${category}"
            data-price="${product.price}"
            ${soldOut ? "disabled" : ""}
          >${soldOut ? "Indisponível" : "Pedir"}</button>
        </div>
      </div>
    </article>
  `;
}

function renderCatalog() {
  const items = currentFilter === "Todos"
    ? catalogItems
    : catalogItems.filter((item) => item.category === currentFilter);

  if (!items.length) {
    categoryMenu.innerHTML = '<p class="empty-state">Nenhum item disponível nesta categoria.</p>';
    return;
  }

  if (currentFilter !== "Todos") {
    categoryMenu.innerHTML = `
      <div class="cards-grid reveal">
        ${items.map(productCard).join("")}
      </div>
    `;
  } else {
    categoryMenu.innerHTML = CATEGORY_ORDER
      .map((category) => {
        const group = items.filter((item) => item.category === category);
        if (!group.length) return "";
        return `
          <div class="category-section reveal">
            <h3>${category}</h3>
            <div class="cards-grid">${group.map(productCard).join("")}</div>
          </div>
        `;
      })
      .join("");
  }

  bindOrderButtons(categoryMenu);
  observeRevealElements(categoryMenu);
}

function renderCombos() {
  const combos = catalogItems.filter((item) => item.category === "Combos");
  if (!combos.length) {
    comboGrid.innerHTML = '<p class="empty-state">Nenhum combo ativo no momento.</p>';
    return;
  }

  comboGrid.innerHTML = `
    <div class="combo-cards-grid">
      ${combos.map((combo) => {
    const soldOut = !combo.is_available;
    const name = escapeHTML(combo.name);
    const saving = combo.badge || "Oferta especial";
    return `
      <article class="combo-deal-card reveal ${soldOut ? "product-card--soldout" : ""}">
        <span class="card-badge">${soldOut ? "Esgotado" : escapeHTML(saving)}</span>
        <img src="${escapeHTML(combo.image_url || "images/combo-house.svg")}" alt="${name}">
        <div class="combo-deal-card__body">
          <h3>${name}</h3>
          <p>${escapeHTML(combo.description)}</p>
          <ul class="check-list">${(combo.items || []).map((item) => `<li>${escapeHTML(item)}</li>`).join("")}</ul>
          <div class="combo-deal-card__footer">
            <strong>${money(combo.price)}</strong>
            <button class="btn btn--whatsapp" type="button" data-order data-name="${name}" data-category="Combos" data-price="${combo.price}" ${soldOut ? "disabled" : ""}>${soldOut ? "Indisponível" : "Quero esse!"}</button>
          </div>
        </div>
      </article>
    `;
  }).join("")}
    </div>
  `;

  bindOrderButtons(comboGrid);
  observeRevealElements(comboGrid);
}

function normalizeProducts(products) {
  return products
    .filter((product) => product.is_active)
    .map((product) => ({
      ...product,
      category: product.category?.name || "Lanches",
      badge: {
        "Classic Burger": "Mais Vendido",
        "Bacon Supreme": "Promoção",
        "Double Smash": "Novo",
        "Veggie Burger": "Vegano"
      }[product.name] || ""
    }));
}

function normalizeCombos(combos) {
  return combos
    .filter((combo) => combo.is_active)
    .map((combo) => ({
      ...combo,
      category: "Combos",
      badge: {
        "Combo Classic": "Economize R$ 8",
        "Combo Bacon": "Economize R$ 10",
        "Combo Double": "Economize R$ 12",
        "Combo Família": "Para dividir"
      }[combo.name] || "Oferta especial"
    }));
}

function setFilter(filter) {
  currentFilter = filter;
  menuTabs.querySelectorAll(".menu-tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.filter === filter);
  });
  renderCatalog();
  document.querySelector("#cardapio").scrollIntoView({ behavior: "smooth", block: "start" });
}

async function loadLanding() {
  try {
    const [products, combos] = await Promise.all([
      api("/products"),
      api("/combos")
    ]);

    catalogItems = [...normalizeProducts(products), ...normalizeCombos(combos)];
    renderCatalog();
    renderCombos();
  } catch (error) {
    categoryMenu.innerHTML = '<p class="empty-state">Não foi possível carregar o cardápio. Verifique se a API está rodando.</p>';
  }
}

function closeMobileMenu() {
  navToggle.classList.remove("active");
  navMenu.classList.remove("active");
  navToggle.setAttribute("aria-expanded", "false");
  document.body.classList.remove("menu-open");
}

function updateHeaderState() {
  header.classList.toggle("scrolled", window.scrollY > 24);
  backToTop.classList.toggle("show", window.scrollY > 520);
}

const revealObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      revealObserver.unobserve(entry.target);
    }
  });
}, { threshold: 0.18 });

const sectionObserver = new IntersectionObserver((entries) => {
  const visible = entries
    .filter((entry) => entry.isIntersecting)
    .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

  if (!visible) return;

  navLinks.forEach((link) => {
    link.classList.toggle("active", link.getAttribute("href") === `#${visible.target.id}`);
  });
}, { rootMargin: "-35% 0px -55% 0px", threshold: [0.12, 0.32, 0.6] });

function observeRevealElements(scope = document) {
  scope.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));
}

navToggle.addEventListener("click", () => {
  const isOpen = navMenu.classList.toggle("active");
  navToggle.classList.toggle("active", isOpen);
  navToggle.setAttribute("aria-expanded", String(isOpen));
  document.body.classList.toggle("menu-open", isOpen);
});

navLinks.forEach((link) => link.addEventListener("click", closeMobileMenu));
backToTop.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
window.addEventListener("scroll", updateHeaderState, { passive: true });
menuTabs.querySelectorAll(".menu-tab").forEach((tab) => {
  tab.addEventListener("click", () => setFilter(tab.dataset.filter));
});

observeRevealElements();
sections.forEach((section) => sectionObserver.observe(section));
updateHeaderState();
configureWhatsAppLinks();
loadLanding();
