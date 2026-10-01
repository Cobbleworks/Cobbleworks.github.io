"use strict";
document.documentElement.classList.add("js");
const menuButton = document.querySelector("[data-menu-button]");
const navigation = document.querySelector("[data-navigation]");
if (menuButton && navigation) {
  menuButton.hidden = false;
  const closeMenu = (returnFocus = false) => {
    const wasOpen = menuButton.getAttribute("aria-expanded") === "true";
    menuButton.setAttribute("aria-expanded", "false");
    menuButton.setAttribute("aria-label", "Open navigation");
    navigation.classList.remove("is-open");
    if (returnFocus && wasOpen) menuButton.focus();
  };
  menuButton.addEventListener("click", () => {
    const open = menuButton.getAttribute("aria-expanded") !== "true";
    menuButton.setAttribute("aria-expanded", String(open));
    menuButton.setAttribute(
      "aria-label",
      open ? "Close navigation" : "Open navigation",
    );
    navigation.classList.toggle("is-open", open);
  });
  navigation.addEventListener("click", (event) => {
    if (event.target.closest("a")) closeMenu();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") closeMenu(true);
  });
  document.addEventListener("click", (event) => {
    if (!event.target.closest(".site-header")) closeMenu();
  });
  window
    .matchMedia("(min-width: 861px)")
    .addEventListener("change", (event) => {
      if (event.matches) closeMenu();
    });
}
const filterForm = document.querySelector("[data-filter-form]");
if (filterForm) {
  filterForm.hidden = false;
  const search = filterForm.querySelector("[data-plugin-search]");
  const platform = filterForm.querySelector("[data-platform-filter]");
  const status = filterForm.querySelector("[data-status-filter]");
  const buttons = [...filterForm.querySelectorAll("[data-filter]")];
  const cards = [...document.querySelectorAll("[data-plugin]")];
  const count = document.querySelector("[data-plugin-count]");
  const empty = document.querySelector("[data-empty-state]");
  let category = "all";
  const filter = (updateURL = true) => {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    for (const card of cards) {
      const matches =
        (!query || card.textContent.toLocaleLowerCase().includes(query)) &&
        (category === "all" ||
          card.dataset.category.split(" ").includes(category)) &&
        (platform.value === "all" ||
          card.dataset.platform.split(" ").includes(platform.value)) &&
        (status.value === "all" ||
          (status.value === "current"
            ? card.dataset.status !== "archived"
            : card.dataset.status === status.value));
      card.hidden = !matches;
      if (matches) visible++;
    }
    buttons.forEach((button) =>
      button.setAttribute(
        "aria-pressed",
        String(button.dataset.filter === category),
      ),
    );
    count.textContent = `${visible} ${visible === 1 ? "project" : "projects"}`;
    empty.hidden = visible !== 0;
    if (updateURL) {
      const url = new URL(location.href);
      for (const [key, value, defaultValue] of [
        ["q", search.value.trim(), ""],
        ["category", category, "all"],
        ["platform", platform.value, "all"],
        ["status", status.value, "current"],
      ]) {
        if (value !== defaultValue) url.searchParams.set(key, value);
        else url.searchParams.delete(key);
      }
      history.replaceState(null, "", url);
    }
  };
  const restore = () => {
    const params = new URLSearchParams(location.search);
    search.value = params.get("q") || "";
    category = buttons.some((b) => b.dataset.filter === params.get("category"))
      ? params.get("category")
      : "all";
    for (const [key, select, fallback] of [
      ["platform", platform, "all"],
      ["status", status, "current"],
    ]) {
      select.value = [...select.options].some(
        (o) => o.value === params.get(key),
      )
        ? params.get(key)
        : fallback;
    }
    filter(false);
  };
  filterForm.addEventListener("submit", (event) => event.preventDefault());
  search.addEventListener("input", () => filter());
  platform.addEventListener("change", () => filter());
  status.addEventListener("change", () => filter());
  buttons.forEach((button) =>
    button.addEventListener("click", () => {
      category = button.dataset.filter;
      filter();
    }),
  );
  document
    .querySelector("[data-reset-filters]")
    ?.addEventListener("click", () => {
      search.value = "";
      platform.value = "all";
      status.value = "current";
      category = "all";
      filter();
      search.focus();
    });
  window.addEventListener("popstate", restore);
  restore();
}
const compatForm = document.querySelector("[data-compat-form]");
if (compatForm) {
  compatForm.hidden = false;
  compatForm.addEventListener("submit", (event) => event.preventDefault());
  const platform = compatForm.querySelector("[data-compat-platform]");
  const java = compatForm.querySelector("[data-compat-java]");
  const target = compatForm.querySelector("[data-compat-target]");
  const update = () => {
    let count = 0;
    document.querySelectorAll("[data-compat-row]").forEach((row) => {
      const matches =
        (platform.value === "all" ||
          row.dataset.platform.split(" ").includes(platform.value)) &&
        (java.value === "all" ||
          Number(row.dataset.java) <= Number(java.value)) &&
        (target.value === "all" || row.dataset.target === target.value);
      row.hidden = !matches;
      if (matches) count++;
    });
    document.querySelector("[data-compat-count]").textContent =
      `${count} ${count === 1 ? "plugin" : "plugins"}`;
    document.querySelector("[data-compat-empty]").hidden = count !== 0;
  };
  compatForm.addEventListener("change", update);
  update();
}
if (navigator.clipboard && window.isSecureContext) {
  document.querySelectorAll("[data-copy]").forEach((button) => {
    button.hidden = false;
    const label = button.querySelector("span");
    button.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(button.dataset.copy);
        label.textContent = "Copied";
        button.setAttribute("aria-label", "Command copied");
        setTimeout(() => {
          label.textContent = "Copy";
          button.setAttribute("aria-label", "Copy command");
        }, 2000);
      } catch {
        const range = document.createRange();
        range.selectNodeContents(button.previousElementSibling);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        label.textContent = "Selected";
      }
    });
  });
}
const sectionLinks = [...document.querySelectorAll('.tabs a[href^="#"]')];
if (sectionLinks.length && "IntersectionObserver" in window) {
  const sections = [...document.querySelectorAll(".doc-section[id]")];
  const visible = new Set();
  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) visible.add(entry.target);
        else visible.delete(entry.target);
      }
      const current = sections.find((section) => visible.has(section));
      if (!current) return;
      sectionLinks.forEach((link) => {
        if (link.hash === `#${current.id}`) {
          link.setAttribute("aria-current", "location");
          const strip = link.parentElement;
          if (link.offsetLeft < strip.scrollLeft || link.offsetLeft + link.offsetWidth > strip.scrollLeft + strip.clientWidth)
            strip.scrollLeft = link.offsetLeft - 16;
        } else link.removeAttribute("aria-current");
      });
    },
    { rootMargin: "-140px 0px -60% 0px" },
  );
  sections.forEach((section) => observer.observe(section));
}
