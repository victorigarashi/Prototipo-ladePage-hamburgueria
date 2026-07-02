const TOKEN_KEY = "burgerHouseAdminToken";

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

const loginScreen = $("#login-screen");
const dashboardShell = $("#dashboard-shell");
const loginForm = $("#login-form");
const loginEmail = $("#login-email");
const loginPassword = $("#login-password");
const loginError = $("#login-error");
const logoutButton = $("#logout-button");
const adminToast = $("#admin-toast");
const panelTitle = $("#panel-title");

let products = [];
let categories = [];
let combos = [];
let promotions = [];
let editProductId = null;
let editCategoryId = null;
let editComboId = null;
let editPromotionId = null;
let toastTimer;

function token() {
  return sessionStorage.getItem(TOKEN_KEY);
}

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

function showToast(message) {
  clearTimeout(toastTimer);
  adminToast.textContent = message;
  adminToast.classList.add("show");
  toastTimer = setTimeout(() => adminToast.classList.remove("show"), 2600);
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token()) headers.Authorization = `Bearer ${token()}`;

  const response = await fetch(`${API_BASE_URL}${path}`, { ...options, headers });
  if (response.status === 401) {
    sessionStorage.removeItem(TOKEN_KEY);
    updateAuthUI();
    throw new Error("Sessão expirada.");
  }
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Erro na API." }));
    throw new Error(error.detail || "Erro na API.");
  }
  if (response.status === 204) return null;
  return response.json();
}

function updateAuthUI() {
  const logged = Boolean(token());
  loginScreen.hidden = logged;
  dashboardShell.hidden = !logged;
  if (logged) loadAdminData();
}

async function loadAdminData() {
  try {
    [products, categories, combos, promotions] = await Promise.all([
      api("/admin/products"),
      api("/admin/categories"),
      api("/admin/combos"),
      api("/admin/promotions")
    ]);
    renderAll();
  } catch (error) {
    showToast(error.message);
  }
}

function renderAll() {
  renderCategoryOptions();
  renderProducts();
  renderCategories();
  renderCombos();
  renderPromotions();
  renderReports();
}

function renderSummary() {
  $("#total-products").textContent = products.length;
  $("#active-products").textContent = products.filter((item) => item.is_active).length;
  $("#soldout-products").textContent = [...products, ...combos].filter((item) => !item.is_available).length;
  $("#total-combos").textContent = combos.length;
}

function renderCategoryOptions() {
  $("#product-category").innerHTML = categories
    .map((category) => `<option value="${category.id}">${escapeHTML(category.name)}</option>`)
    .join("");
}

function itemCard(item, type) {
  const title = item.name || item.title;
  const description = item.description;
  const active = item.is_active;
  const available = "is_available" in item ? item.is_available : true;
  return `
    <article class="admin-item">
      ${item.image_url ? `<img src="${escapeHTML(item.image_url)}" alt="${escapeHTML(title)}">` : ""}
      <div>
        <h3>${escapeHTML(title)}</h3>
        <p>${escapeHTML(description || item.slug || "")}</p>
        <div class="admin-item__meta">
          ${item.price ? `<span class="status-pill status-pill--soldout">${money(item.price)}</span>` : ""}
          <span class="status-pill ${active ? "status-pill--active" : "status-pill--inactive"}">${active ? "Ativo" : "Inativo"}</span>
          ${"is_available" in item ? `<span class="status-pill ${available ? "status-pill--active" : "status-pill--soldout"}">${available ? "Disponível" : "Esgotado"}</span>` : ""}
        </div>
      </div>
      <div class="admin-item__actions">
        <button class="admin-action" data-action="edit" data-type="${type}" data-id="${item.id}">Editar</button>
        ${type === "product" ? `<button class="admin-action" data-action="toggle-active" data-type="${type}" data-id="${item.id}">Ativar/desativar</button><button class="admin-action" data-action="toggle-available" data-type="${type}" data-id="${item.id}">Disponível/esgotado</button>` : ""}
        ${type === "combo" ? `<button class="admin-action" data-action="toggle-active" data-type="${type}" data-id="${item.id}">Ativar/desativar</button><button class="admin-action" data-action="toggle-available" data-type="${type}" data-id="${item.id}">Disponível/esgotado</button>` : ""}
        <button class="admin-action admin-action--danger" data-action="delete" data-type="${type}" data-id="${item.id}">Excluir</button>
      </div>
    </article>
  `;
}

function renderProducts() {
  renderSummary();
  $("#product-list").innerHTML = products.length ? products.map((item) => itemCard(item, "product")).join("") : '<div class="admin-empty">Nenhum produto cadastrado.</div>';
}

function renderCategories() {
  $("#category-list").innerHTML = categories.length ? categories.map((item) => itemCard(item, "category")).join("") : '<div class="admin-empty">Nenhuma categoria cadastrada.</div>';
}

function renderCombos() {
  renderSummary();
  $("#combo-list").innerHTML = combos.length ? combos.map((item) => itemCard(item, "combo")).join("") : '<div class="admin-empty">Nenhum combo cadastrado.</div>';
}

function renderPromotions() {
  $("#promotion-list").innerHTML = promotions.length ? promotions.map((item) => itemCard(item, "promotion")).join("") : '<div class="admin-empty">Nenhuma promoção cadastrada.</div>';
}

function renderReports() {
  $("#report-products").textContent = `${products.length} produtos`;
  $("#report-combos").textContent = `${combos.length} combos`;
  $("#report-promotions").textContent = `${promotions.filter((item) => item.is_active).length} promoções`;
  $("#report-soldout").textContent = `${[...products, ...combos].filter((item) => !item.is_available).length} esgotados`;
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginError.textContent = "";
  try {
    const response = await api("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email: loginEmail.value, password: loginPassword.value })
    });
    sessionStorage.setItem(TOKEN_KEY, response.access_token);
    loginPassword.value = "";
    updateAuthUI();
  } catch (error) {
    loginError.textContent = error.message;
  }
});

logoutButton.addEventListener("click", () => {
  sessionStorage.removeItem(TOKEN_KEY);
  updateAuthUI();
});

$$("[data-panel]").forEach((button) => {
  button.addEventListener("click", () => {
    const panel = button.dataset.panel;
    $$(".admin-menu__item").forEach((item) => item.classList.toggle("active", item === button));
    $$(".admin-panel").forEach((section) => section.classList.toggle("active", section.id === `panel-${panel}`));
    panelTitle.textContent = button.textContent.replace(/[^\p{L}\s]/gu, "").trim();
  });
});

$("#product-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    name: $("#product-name").value,
    category_id: Number($("#product-category").value),
    description: $("#product-description").value,
    price: Number($("#product-price").value),
    image_url: $("#product-image").value || null,
    is_active: $("#product-active").checked,
    is_available: $("#product-available").checked
  };
  await api(editProductId ? `/admin/products/${editProductId}` : "/admin/products", { method: editProductId ? "PUT" : "POST", body: JSON.stringify(payload) });
  editProductId = null;
  event.target.reset();
  $("#product-active").checked = true;
  $("#product-available").checked = true;
  $("#product-title").textContent = "Novo produto";
  $("#cancel-product").hidden = true;
  showToast("Produto salvo.");
  loadAdminData();
});

$("#category-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = { name: $("#category-name").value, slug: $("#category-slug").value || null, is_active: $("#category-active").checked };
  await api(editCategoryId ? `/admin/categories/${editCategoryId}` : "/admin/categories", { method: editCategoryId ? "PUT" : "POST", body: JSON.stringify(payload) });
  editCategoryId = null;
  event.target.reset();
  $("#category-active").checked = true;
  $("#category-title").textContent = "Nova categoria";
  $("#cancel-category").hidden = true;
  showToast("Categoria salva.");
  loadAdminData();
});

$("#combo-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    name: $("#combo-name").value,
    description: $("#combo-description").value,
    items: $("#combo-items").value.split("\n").map((item) => item.trim()).filter(Boolean),
    price: Number($("#combo-price").value),
    image_url: $("#combo-image").value || null,
    is_active: $("#combo-active").checked,
    is_available: $("#combo-available").checked
  };
  await api(editComboId ? `/admin/combos/${editComboId}` : "/admin/combos", { method: editComboId ? "PUT" : "POST", body: JSON.stringify(payload) });
  editComboId = null;
  event.target.reset();
  $("#combo-active").checked = true;
  $("#combo-available").checked = true;
  $("#combo-title").textContent = "Novo combo";
  $("#cancel-combo").hidden = true;
  showToast("Combo salvo.");
  loadAdminData();
});

$("#promotion-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    title: $("#promotion-title-input").value,
    description: $("#promotion-description").value,
    code: $("#promotion-code").value || null,
    discount: $("#promotion-discount").value || null,
    is_active: $("#promotion-active").checked
  };
  await api(editPromotionId ? `/admin/promotions/${editPromotionId}` : "/admin/promotions", { method: editPromotionId ? "PUT" : "POST", body: JSON.stringify(payload) });
  editPromotionId = null;
  event.target.reset();
  $("#promotion-active").checked = true;
  $("#promotion-title").textContent = "Nova promoção";
  $("#cancel-promotion").hidden = true;
  showToast("Promoção salva.");
  loadAdminData();
});

document.addEventListener("click", async (event) => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  const { action, type, id } = button.dataset;
  const collections = { product: products, category: categories, combo: combos, promotion: promotions };
  const item = collections[type].find((current) => String(current.id) === String(id));

  if (action === "edit") {
    if (type === "product") {
      editProductId = id;
      $("#product-title").textContent = "Editar produto";
      $("#cancel-product").hidden = false;
      $("#product-name").value = item.name;
      $("#product-category").value = item.category_id;
      $("#product-description").value = item.description;
      $("#product-price").value = item.price;
      $("#product-image").value = item.image_url || "";
      $("#product-active").checked = item.is_active;
      $("#product-available").checked = item.is_available;
    }
    if (type === "category") {
      editCategoryId = id;
      $("#category-title").textContent = "Editar categoria";
      $("#cancel-category").hidden = false;
      $("#category-name").value = item.name;
      $("#category-slug").value = item.slug;
      $("#category-active").checked = item.is_active;
    }
    if (type === "combo") {
      editComboId = id;
      $("#combo-title").textContent = "Editar combo";
      $("#cancel-combo").hidden = false;
      $("#combo-name").value = item.name;
      $("#combo-description").value = item.description;
      $("#combo-items").value = (item.items || []).join("\n");
      $("#combo-price").value = item.price;
      $("#combo-image").value = item.image_url || "";
      $("#combo-active").checked = item.is_active;
      $("#combo-available").checked = item.is_available;
    }
    if (type === "promotion") {
      editPromotionId = id;
      $("#promotion-title").textContent = "Editar promoção";
      $("#cancel-promotion").hidden = false;
      $("#promotion-title-input").value = item.title;
      $("#promotion-description").value = item.description;
      $("#promotion-code").value = item.code || "";
      $("#promotion-discount").value = item.discount || "";
      $("#promotion-active").checked = item.is_active;
    }
    window.scrollTo({ top: 0, behavior: "smooth" });
    return;
  }

  if (action === "delete" && !confirm("Deseja excluir este registro?")) return;
  const endpoint = type === "product" ? "products" : type === "category" ? "categories" : type === "combo" ? "combos" : "promotions";
  const path = `/admin/${endpoint}/${id}`;
  const suffix = action === "toggle-active" ? "/toggle-active" : action === "toggle-available" ? "/toggle-available" : "";
  const method = action === "delete" ? "DELETE" : "PATCH";
  await api(`${path}${suffix}`, { method });
  showToast("Alteração salva.");
  loadAdminData();
});

["product", "category", "combo", "promotion"].forEach((name) => {
  const cancel = $(`#cancel-${name}`);
  if (!cancel) return;
  cancel.addEventListener("click", () => {
    $(`#${name}-form`).reset();
    if (name === "product") editProductId = null;
    if (name === "category") editCategoryId = null;
    if (name === "combo") editComboId = null;
    if (name === "promotion") editPromotionId = null;
    cancel.hidden = true;
  });
});

updateAuthUI();
