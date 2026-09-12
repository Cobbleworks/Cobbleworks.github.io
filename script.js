const header = document.querySelector('[data-header]');
const menuButton = document.querySelector('[data-menu-button]');
const navigation = document.querySelector('[data-navigation]');
const setHeaderState = () => {
  header?.classList.toggle('is-scrolled', window.scrollY > 24);
};

setHeaderState();
window.addEventListener('scroll', setHeaderState, { passive: true });

const closeMenu = () => {
  if (menuButton) {
    menuButton.setAttribute('aria-expanded', 'false');
  }
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

const sanitize = (value) => (value ?? '').replace(/\s+/g, ' ').trim();
const normalizeCategory = (value) => (value ?? '').toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

const pluginCardMarkup = (plugin) => {
  const image = plugin.screenshots?.[0] || '/assets/plugins/default-banner.png';
  const detailUrl = `/plugins/${plugin.slug}/`;
  const repoUrl = plugin.repository;

  return `
    <article class="plugin-card" data-plugin data-category="${normalizeCategory(plugin.category)}" data-search="${sanitize(`${plugin.name} ${plugin.tagline} ${plugin.description} ${plugin.minecraftVersions.join(' ')} ${plugin.platforms.join(' ')}`)}">
      <a class="card-image" href="${detailUrl}" aria-label="Open ${plugin.name} details">
        <img src="${image}" alt="${plugin.name} plugin artwork" loading="lazy" width="818" height="196">
      </a>
      <div class="card-body">
        <div class="card-topline"><span>${plugin.category || 'Plugin'}</span><span>${plugin.minecraftVersions?.[0] || 'Version info'}</span></div>
        <h3>${plugin.name}</h3>
        <p>${plugin.tagline}</p>
        <div class="card-badges">
          ${(plugin.platforms || []).slice(0, 3).map((platform) => `<span class="badge">${platform}</span>`).join('')}
        </div>
        <div class="card-actions">
          <a href="${detailUrl}">View plugin</a>
          <a href="${repoUrl}" target="_blank" rel="noreferrer">GitHub</a>
        </div>
      </div>
    </article>
  `;
};

const renderHomePlugins = (plugins) => {
  const featured = (plugins || []).filter((plugin) => plugin.featured).slice(0, 4);
  const target = document.getElementById('featured-plugins');
  if (!target) return;
  target.innerHTML = featured.map(pluginCardMarkup).join('');
};

const renderDirectory = (plugins) => {
  const grid = document.getElementById('directory-grid');
  const searchInput = document.querySelector('[data-plugin-search]');
  const pluginCount = document.querySelector('[data-plugin-count]');
  const filterButtons = [...document.querySelectorAll('[data-filter]')];
  const allCards = plugins || [];
  let selectedCategory = 'all';

  const applyFilter = () => {
    const query = sanitize(searchInput?.value || '').toLowerCase();
    const cards = allCards.filter((plugin) => {
      const categoryMatch = selectedCategory === 'all' || normalizeCategory(plugin.category).includes(selectedCategory);
      const searchText = `${plugin.name} ${plugin.tagline} ${plugin.description} ${plugin.platforms.join(' ')} ${plugin.minecraftVersions.join(' ')}`.toLowerCase();
      const queryMatch = !query || searchText.includes(query);
      return categoryMatch && queryMatch;
    });

    if (grid) {
      grid.innerHTML = cards.map(pluginCardMarkup).join('');
    }

    if (pluginCount) {
      const label = cards.length === 1 ? 'plugin' : 'plugins';
      pluginCount.textContent = `${cards.length} ${label}`;
    }
  };

  filterButtons.forEach((button) => {
    button.addEventListener('click', () => {
      selectedCategory = button.dataset.filter || 'all';
      filterButtons.forEach((candidate) => {
        const active = candidate === button;
        candidate.classList.toggle('is-active', active);
        candidate.setAttribute('aria-pressed', String(active));
      });
      applyFilter();
    });
  });

  searchInput?.addEventListener('input', applyFilter);
  applyFilter();
};

const renderReleases = (plugins) => {
  const target = document.getElementById('release-grid');
  if (!target) return;
  target.innerHTML = (plugins || []).map((plugin) => `
    <article class="release-card">
      <div>
        <p class="eyebrow"><span></span> ${plugin.category || 'Plugin'}</p>
        <h3>${plugin.name}</h3>
      </div>
      <ul>
        <li><strong>Latest release:</strong> ${plugin.releaseUrl ? '<a href="' + plugin.releaseUrl + '" target="_blank" rel="noreferrer">Open releases</a>' : 'See GitHub'}</li>
        <li><strong>Java:</strong> ${plugin.javaVersion || 'See README'}</li>
        <li><strong>Platform:</strong> ${(plugin.platforms || []).join(', ') || 'See README'}</li>
      </ul>
      <div class="release-actions">
        <a class="button button-primary" href="${plugin.releaseUrl || plugin.repository}" target="_blank" rel="noreferrer">Latest download</a>
        <a class="button button-secondary" href="${plugin.repository}" target="_blank" rel="noreferrer">Source</a>
      </div>
    </article>
  `).join('');
};

const renderPluginPage = (plugins) => {
  const pluginData = window.PLUGIN_DATA || null;
  const root = document.getElementById('plugin-page-root');
  if (!root || !pluginData) return;

  const details = pluginData;
  const badges = (details.platforms || []).map((platform) => `<span class="badge">${platform}</span>`).join('');
  const screenshots = (details.screenshots || []).slice(1);
  const features = (details.features || []).map((feature) => `
    <li>
      <span class="feature-icon" aria-hidden="true">✦</span>
      <div>
        <strong>${feature}</strong>
      </div>
    </li>
  `).join('');

  const gallery = screenshots.length ? `
    <div class="gallery-grid">
      ${screenshots.map((src, index) => `
        <figure class="gallery-item">
          <img src="${src}" alt="${details.name} screenshot ${index + 1}" loading="lazy">
        </figure>
      `).join('')}
    </div>
  ` : '<div class="empty-state small">No screenshot set has been published for this plugin yet; the project README remains the source of truth.</div>';

  const related = (plugins || [])
    .filter((plugin) => plugin.slug !== details.slug)
    .slice(0, 3)
    .map((plugin) => `
      <article class="related-card">
        <div>
          <p class="eyebrow"><span></span> ${plugin.category || 'Plugin'}</p>
          <h3>${plugin.name}</h3>
        </div>
        <p>${plugin.tagline}</p>
        <a href="/plugins/${plugin.slug}/">View plugin</a>
      </article>
    `)
    .join('');

  root.innerHTML = `
    <section class="plugin-hero shell">
      <nav class="breadcrumb" aria-label="Breadcrumb">
        <a href="/plugins/">Plugins</a>
        <span> / </span>
        <span>${details.name}</span>
      </nav>
      <div class="plugin-hero-inner">
        <div class="plugin-hero-art">
          <img src="${details.screenshots?.[0] || '/assets/plugins/default-banner.png'}" alt="${details.name} banner" width="800" height="220">
        </div>
        <div class="plugin-hero-copy">
          <p class="eyebrow"><span></span> ${details.category || 'Plugin'}</p>
          <h1>${details.name}</h1>
          <p class="hero-copy">${details.tagline}</p>
          <p class="plugin-description">${details.description}</p>
          <div class="plugin-cta-row">
            <a class="button button-primary" href="${details.releaseUrl || details.repository}" target="_blank" rel="noreferrer">Download latest</a>
            <a class="button button-secondary" href="${details.repository}" target="_blank" rel="noreferrer">View on GitHub</a>
          </div>
          <div class="badge-row">${badges}</div>
          <div class="meta-row">
            <span>${details.javaVersion || 'Java version varies by release'}</span>
            <span>${details.minecraftVersions?.join(', ') || 'Minecraft version varies by release'}</span>
            <span>Open source</span>
          </div>
        </div>
      </div>
    </section>

    <section class="plugin-body shell">
      <div class="plugin-section-nav" aria-label="Plugin sections">
        <a href="#overview">Overview</a>
        <a href="#features">Features</a>
        <a href="#screenshots">Screenshots</a>
        <a href="#support">Support</a>
      </div>

      <article id="overview" class="plugin-section">
        <div class="section-heading">
          <p class="eyebrow"><span></span> Overview</p>
          <h2>${details.name}</h2>
        </div>
        <p>${details.description}</p>
      </article>

      <article id="features" class="plugin-section">
        <div class="section-heading">
          <p class="eyebrow"><span></span> Features</p>
          <h2>What this plugin adds</h2>
        </div>
        <ul class="feature-list">${features}</ul>
      </article>

      <article id="screenshots" class="plugin-section">
        <div class="section-heading">
          <p class="eyebrow"><span></span> Screenshots</p>
          <h2>Examples from the project</h2>
        </div>
        ${gallery}
      </article>

      <article id="support" class="plugin-section">
        <div class="section-heading">
          <p class="eyebrow"><span></span> Support</p>
          <h2>Install and maintain</h2>
        </div>
        <div class="support-grid">
          <div class="support-card">
            <h3>Installation</h3>
            <ol>
              <li>Download the latest release JAR from GitHub.</li>
              <li>Place it in your server's <code>plugins</code> directory.</li>
              <li>Install any listed dependency before starting the server.</li>
              <li>Review the generated config and restart once the plugin has loaded.</li>
            </ol>
          </div>
          <div class="support-card">
            <h3>Dependencies</h3>
            <p>${(details.dependencies || ['None']).join(', ') || 'None specified in the project README.'}</p>
          </div>
        </div>
      </article>

      <article class="plugin-section related-section">
        <div class="section-heading">
          <p class="eyebrow"><span></span> Related plugins</p>
          <h2>Keep exploring</h2>
        </div>
        <div class="related-grid">${related}</div>
      </article>
    </section>
  `;
};

const initialize = async () => {
  const page = document.body.dataset.page || 'home';

  if (window.PLUGIN_DATA && page === 'plugin-page') {
    renderPluginPage([window.PLUGIN_DATA]);
    return;
  }

  try {
    const response = await fetch('/data/plugins.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('Unable to load plugin data');
    const data = await response.json();
    const plugins = data.plugins || [];

    if (page === 'home') renderHomePlugins(plugins);
    if (page === 'directory') renderDirectory(plugins);
    if (page === 'releases') renderReleases(plugins);
    if (page === 'plugin-page') {
      const slug = document.body.dataset.pluginSlug || (window.location.pathname.match(/plugins\/([^/]+)/)?.[1] || '');
      const plugin = plugins.find((item) => item.slug === slug) || null;
      if (plugin) {
        const root = document.getElementById('plugin-page-root');
        if (root) {
          window.PLUGIN_DATA = plugin;
          renderPluginPage(plugins);
        }
      }
    }
  } catch (error) {
    console.warn('Plugin data could not be loaded:', error);
  }
};

document.addEventListener('DOMContentLoaded', initialize);
