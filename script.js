const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-button]');
const navigation = document.querySelector('[data-navigation]');
const search = document.querySelector('[data-plugin-search]');
const filterButtons = [...document.querySelectorAll('[data-filter]')];
const pluginCards = [...document.querySelectorAll('[data-plugin]')];
const resultsStatus = document.querySelector('[data-results-status]');
const emptyState = document.querySelector('[data-empty-state]');

const setHeaderState = () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 24);
};

setHeaderState();
window.addEventListener('scroll', setHeaderState, { passive: true });

const closeMenu = () => {
  menuButton?.setAttribute('aria-expanded', 'false');
  navigation?.classList.remove('is-open');
};

menuButton?.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  navigation?.classList.toggle('is-open', !isOpen);
});

navigation?.addEventListener('click', (event) => {
  if (event.target.closest('a')) closeMenu();
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') closeMenu();
});

let selectedCategory = 'all';

const filterPlugins = () => {
  const query = search?.value.trim().toLocaleLowerCase() ?? '';
  let visibleCount = 0;

  pluginCards.forEach((card) => {
    const categories = card.dataset.category?.split(' ') ?? [];
    const searchableText = `${card.dataset.search ?? ''} ${card.textContent}`.toLocaleLowerCase();
    const categoryMatches = selectedCategory === 'all' || categories.includes(selectedCategory);
    const queryMatches = !query || searchableText.includes(query);
    const visible = categoryMatches && queryMatches;

    card.hidden = !visible;
    if (visible) visibleCount += 1;
  });

  if (resultsStatus) {
    const label = visibleCount === 1 ? 'plugin' : 'plugins';
    resultsStatus.textContent = query || selectedCategory !== 'all'
      ? `${visibleCount} matching ${label}`
      : `Showing all ${visibleCount} ${label}`;
  }

  if (emptyState) emptyState.hidden = visibleCount !== 0;
};

filterButtons.forEach((button) => {
  button.addEventListener('click', () => {
    selectedCategory = button.dataset.filter ?? 'all';
    filterButtons.forEach((candidate) => {
      const active = candidate === button;
      candidate.classList.toggle('is-active', active);
      candidate.setAttribute('aria-pressed', String(active));
    });
    filterPlugins();
  });
});

search?.addEventListener('input', filterPlugins);
