#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "plugins.json"
OUT = ROOT

with DATA.open("r", encoding="utf-8") as fh:
    plugins = json.load(fh)["plugins"]

PLUGIN_TEMPLATE = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <title>{title}</title>
    <meta name=\"description\" content=\"{description}\">\n    <link rel=\"canonical\" href=\"https://cobbleworks.github.io/plugins/{slug}/\">\n    <link rel=\"icon\" href=\"/assets/favicon.svg\" type=\"image/svg+xml\">\n    <link rel=\"stylesheet\" href=\"/styles.css\">\n    <meta name=\"theme-color\" content=\"#0b0a08\">\n    <meta property=\"og:type\" content=\"website\">\n    <meta property=\"og:title\" content=\"{title}\">\n    <meta property=\"og:description\" content=\"{description}\">\n    <meta property=\"og:url\" content=\"https://cobbleworks.github.io/plugins/{slug}/\">\n    <meta property=\"og:image\" content=\"https://cobbleworks.github.io/assets/cobbleworks-social-preview.png\">\n    <meta name=\"twitter:card\" content=\"summary_large_image\">\n  </head>
  <body data-page=\"plugin-page\" data-plugin-slug=\"{slug}\">
    <a class=\"skip-link\" href=\"#main-content\">Skip to content</a>
    <header class=\"site-header\" data-header>
      <a class=\"brand\" href=\"/\" aria-label=\"Cobbleworks home\">
        <img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\">
        <span>Cobbleworks</span>
      </a>
      <button class=\"menu-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"site-navigation\" data-menu-button>
        <span class=\"sr-only\">Open navigation</span>
        <span></span><span></span><span></span>
      </button>
      <nav id=\"site-navigation\" class=\"site-nav\" aria-label=\"Primary navigation\" data-navigation>
        <a href=\"/plugins/\">Plugins</a>
        <a href=\"/docs/\">Documentation</a>
        <a href=\"/releases/\">Releases</a>
        <a href=\"/about/\">About</a>
      </nav>
      <div class=\"header-actions\">
        <a class=\"header-github\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\" aria-label=\"Cobbleworks on GitHub\">
          <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z\"/></svg>
        </a>
        <a class=\"button button-primary header-cta\" href=\"{repo}\" target=\"_blank\" rel=\"noreferrer\">View on GitHub</a>
      </div>
    </header>

    <main id=\"main-content\" class=\"page-shell\">
      <div id=\"plugin-page-root\"></div>
    </main>

    <footer class=\"site-footer\">
      <div class=\"shell footer-inner\">
        <a class=\"brand\" href=\"/\"><img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\"><span>Cobbleworks</span></a>
        <p>Open-source Minecraft server plugins released under the MIT License.</p>
        <nav aria-label=\"Footer navigation\"><a href=\"/plugins/\">Plugins</a><a href=\"/docs/\">Documentation</a><a href=\"https://github.com/Cobbleworks\">GitHub</a></nav>
      </div>
    </footer>
    <script src=\"/script.js\" defer></script>
  </body>
</html>
"""

PLUGINS_DIR = OUT / "plugins"
PLUGINS_DIR.mkdir(exist_ok=True)

for plugin in plugins:
    slug = plugin["slug"]
    path = PLUGINS_DIR / slug
    path.mkdir(exist_ok=True)
    title = f"{plugin['name']} | Cobbleworks"
    description = plugin["description"]
    content = PLUGIN_TEMPLATE.format(title=title, description=description, slug=slug, repo=plugin["repository"])
    (path / "index.html").write_text(content, encoding="utf-8")

index_html = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Cobbleworks | Open-Source Minecraft Server Plugins</title>
    <meta name=\"description\" content=\"Cobbleworks publishes practical Minecraft server plugins for Paper, Spigot, and Purpur with a focus on automation, logistics, systems, and world tools.\">\n    <meta name=\"theme-color\" content=\"#0b0a08\">\n    <meta name=\"color-scheme\" content=\"dark\">\n    <link rel=\"canonical\" href=\"https://cobbleworks.github.io/\">\n    <link rel=\"icon\" href=\"/assets/favicon.svg\" type=\"image/svg+xml\">\n    <link rel=\"manifest\" href=\"/site.webmanifest\">\n    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n    <link href=\"https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@500;600&display=swap\" rel=\"stylesheet\">\n    <link rel=\"stylesheet\" href=\"/styles.css\">\n    <meta property=\"og:type\" content=\"website\">\n    <meta property=\"og:site_name\" content=\"Cobbleworks\">\n    <meta property=\"og:title\" content=\"Cobbleworks | Open-Source Minecraft Server Plugins\">\n    <meta property=\"og:description\" content=\"Minecraft plugins for automation, world tools, transport, redstone, NPCs, and gameplay systems.\">\n    <meta property=\"og:url\" content=\"https://cobbleworks.github.io/\">\n    <meta property=\"og:image\" content=\"https://cobbleworks.github.io/assets/cobbleworks-social-preview.png\">\n    <meta name=\"twitter:card\" content=\"summary_large_image\">\n  </head>
  <body>
    <a class=\"skip-link\" href=\"#main-content\">Skip to content</a>
    <header class=\"site-header\" data-header>
      <a class=\"brand\" href=\"/\" aria-label=\"Cobbleworks home\">
        <img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\">
        <span>Cobbleworks</span>
      </a>
      <button class=\"menu-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"site-navigation\" data-menu-button>
        <span class=\"sr-only\">Open navigation</span>
        <span></span><span></span><span></span>
      </button>
      <nav id=\"site-navigation\" class=\"site-nav\" aria-label=\"Primary navigation\" data-navigation>
        <a href=\"/plugins/\">Plugins</a>
        <a href=\"/docs/\">Documentation</a>
        <a href=\"/releases/\">Releases</a>
        <a href=\"/about/\">About</a>
      </nav>
      <div class=\"header-actions\">
        <a class=\"header-github\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\" aria-label=\"Cobbleworks on GitHub\">
          <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z\"/></svg>
        </a>
        <a class=\"button button-primary header-cta\" href=\"/plugins/\">Browse plugins</a>
      </div>
    </header>

    <main id=\"main-content\">
      <section class=\"hero\" aria-labelledby=\"hero-title\">
        <img class=\"hero-image\" src=\"/assets/cobbleworks-hero-september-2026.png\" width=\"1672\" height=\"941\" alt=\"A Minecraft settlement at sunset\" fetchpriority=\"high\">
        <div class=\"hero-shade\" aria-hidden=\"true\"></div>
        <div class=\"hero-content shell\">
          <p class=\"eyebrow\"><span></span> Open-source plugin publishing</p>
          <h1 id=\"hero-title\">Minecraft plugins<br>that do more.</h1>
          <p class=\"hero-copy\">Cobbleworks builds a practical library of Minecraft server plugins for automation, logistics, utilities, terrain systems, NPCs, and custom gameplay. Every project is open source and maintained as an independent release.</p>
          <div class=\"hero-actions\">
            <a class=\"button button-primary\" href=\"/plugins/\">Browse plugins</a>
            <a class=\"button button-secondary\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\">View GitHub</a>
          </div>
        </div>
        <div class=\"hero-features\" aria-label=\"Cobbleworks project principles\">
          <div class=\"hero-feature\"><strong>Open source</strong><span>Code, issues, and releases stay public.</span></div>
          <div class=\"hero-feature\"><strong>Paper-ready</strong><span>Each plugin outlines its own supported stack.</span></div>
          <div class=\"hero-feature\"><strong>Independent projects</strong><span>Every plugin is versioned and documented separately.</span></div>
          <div class=\"hero-feature\"><strong>Built for servers</strong><span>Focused on practical gameplay and systems tools.</span></div>
        </div>
      </section>

      <section class=\"shell section-stack\">
        <div class=\"section-heading\">
          <p class=\"eyebrow\"><span></span> Featured plugins</p>
          <h2>Built for real server workflows.</h2>
        </div>
        <div id=\"featured-plugins\" class=\"plugin-grid\"></div>
      </section>

      <section class=\"shell section-stack\" id=\"getting-started\">
        <div class=\"section-heading section-heading-split\">
          <h2>Start with the right plugin.</h2>
          <p class=\"section-lead\">Each plugin maintains its own README, compatibility notes, and release page. Use the directory to compare options, then confirm support before installing on your server.</p>
        </div>
        <div class=\"info-grid\">
          <article class=\"info-card\"><h3>Browse the collection</h3><p>Each plugin page highlights supported platforms, Java requirements, and the primary server use case.</p><a href=\"/plugins/\">Open plugin directory</a></article>
          <article class=\"info-card\"><h3>Read the docs</h3><p>Installation steps, commands, permissions, and configuration notes live in the plugin’s GitHub README.</p><a href=\"/docs/\">Documentation landing page</a></article>
          <article class=\"info-card\"><h3>Track releases</h3><p>Use the release hub to jump to each repository’s latest download or changelog entry.</p><a href=\"/releases/\">View releases</a></article>
        </div>
      </section>
    </main>

    <footer class=\"site-footer\">
      <div class=\"shell footer-inner\">
        <a class=\"brand\" href=\"/\"><img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\"><span>Cobbleworks</span></a>
        <p>Open-source Minecraft server plugins.</p>
        <nav aria-label=\"Footer navigation\"><a href=\"/plugins/\">Plugins</a><a href=\"/docs/\">Documentation</a><a href=\"/about/\">About</a><a href=\"https://github.com/Cobbleworks\">GitHub</a></nav>
      </div>
    </footer>
    <script src=\"/script.js\" defer></script>
  </body>
</html>
"""
(OUT / "index.html").write_text(index_html, encoding="utf-8")

plugin_dir_html = """<!doctype html>
<html lang=\"en\">
  <head>
    <meta charset=\"utf-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <title>Plugin directory | Cobbleworks</title>
    <meta name=\"description\" content=\"Browse all Cobbleworks Minecraft plugins and compare supported platforms, versions, and use cases.\">\n    <link rel=\"canonical\" href=\"https://cobbleworks.github.io/plugins/\">\n    <link rel=\"icon\" href=\"/assets/favicon.svg\" type=\"image/svg+xml\">\n    <link rel=\"stylesheet\" href=\"/styles.css\">\n    <meta property=\"og:title\" content=\"Cobbleworks plugin directory\">\n    <meta property=\"og:description\" content=\"Browse all Cobbleworks plugins for Paper, Spigot, and Purpur.\">\n    <meta property=\"og:url\" content=\"https://cobbleworks.github.io/plugins/\">\n  </head>
  <body data-page=\"directory\">
    <a class=\"skip-link\" href=\"#main-content\">Skip to content</a>
    <header class=\"site-header\" data-header>
      <a class=\"brand\" href=\"/\" aria-label=\"Cobbleworks home\">
        <img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\">
        <span>Cobbleworks</span>
      </a>
      <button class=\"menu-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"site-navigation\" data-menu-button>
        <span class=\"sr-only\">Open navigation</span>
        <span></span><span></span><span></span>
      </button>
      <nav id=\"site-navigation\" class=\"site-nav\" aria-label=\"Primary navigation\" data-navigation>
        <a href=\"/plugins/\" aria-current=\"page\">Plugins</a>
        <a href=\"/docs/\">Documentation</a>
        <a href=\"/releases/\">Releases</a>
        <a href=\"/about/\">About</a>
      </nav>
      <div class=\"header-actions\">
        <a class=\"header-github\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\" aria-label=\"Cobbleworks on GitHub\">
          <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z\"/></svg>
        </a>
        <a class=\"button button-primary header-cta\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\">GitHub</a>
      </div>
    </header>
    <main id=\"main-content\" class=\"page-shell\">
      <section class=\"section-stack\">
        <div class=\"section-heading section-heading-split\">
          <div>
            <p class=\"eyebrow\"><span></span> Cobbleworks catalog</p>
            <h1>Plugin directory</h1>
          </div>
          <p class=\"section-lead\">Browse the full plugin library and compare supported platforms, Java versions, and core use cases.</p>
        </div>
        <div class=\"plugin-toolbar\" aria-label=\"Plugin search and filter\">
          <div class=\"plugin-toolbar-row\">
            <label class=\"search-control\">
              <span class=\"sr-only\">Search plugins</span>
              <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"m21 21-4.35-4.35m2.35-5.15a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z\"/></svg>
              <input type=\"search\" placeholder=\"Search plugin names and features…\" data-plugin-search>
            </label>
            <span class=\"plugin-count\" data-plugin-count></span>
          </div>
          <div class=\"filter-buttons\" role=\"group\" aria-label=\"Plugin categories\">
            <button type=\"button\" class=\"is-active\" data-filter=\"all\" aria-pressed=\"true\">All</button>
            <button type=\"button\" data-filter=\"automation\" aria-pressed=\"false\">Automation</button>
            <button type=\"button\" data-filter=\"npcs\" aria-pressed=\"false\">NPCs</button>
            <button type=\"button\" data-filter=\"world\" aria-pressed=\"false\">World tools</button>
            <button type=\"button\" data-filter=\"redstone\" aria-pressed=\"false\">Redstone</button>
            <button type=\"button\" data-filter=\"progression\" aria-pressed=\"false\">Progression</button>
          </div>
        </div>
        <div id=\"directory-grid\" class=\"plugin-grid\"></div>
      </section>
    </main>
    <footer class=\"site-footer\">
      <div class=\"shell footer-inner\">
        <a class=\"brand\" href=\"/\"><img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\"><span>Cobbleworks</span></a>
        <p>Open-source Minecraft server plugins.</p>
        <nav aria-label=\"Footer navigation\"><a href=\"/plugins/\">Plugins</a><a href=\"/docs/\">Documentation</a><a href=\"https://github.com/Cobbleworks\">GitHub</a></nav>
      </div>
    </footer>
    <script src=\"/script.js\" defer></script>
  </body>
</html>
"""
(OUT / "plugins" / "index.html").write_text(plugin_dir_html, encoding="utf-8")

for filename, title, content in [
    ("docs/index.html", "Documentation | Cobbleworks", """<!doctype html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <title>Documentation | Cobbleworks</title>\n    <meta name=\"description\" content=\"Cobbleworks documentation hub for plugin installation, configuration, and troubleshooting.\">\n    <link rel=\"canonical\" href=\"https://cobbleworks.github.io/docs/\">\n    <link rel=\"icon\" href=\"/assets/favicon.svg\" type=\"image/svg+xml\">\n    <link rel=\"stylesheet\" href=\"/styles.css\">\n  </head>\n  <body data-page=\"docs\">\n    <a class=\"skip-link\" href=\"#main-content\">Skip to content</a>\n    <header class=\"site-header\" data-header>\n      <a class=\"brand\" href=\"/\" aria-label=\"Cobbleworks home\">\n        <img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\">\n        <span>Cobbleworks</span>\n      </a>\n      <button class=\"menu-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"site-navigation\" data-menu-button>\n        <span class=\"sr-only\">Open navigation</span>\n        <span></span><span></span><span></span>\n      </button>\n      <nav id=\"site-navigation\" class=\"site-nav\" aria-label=\"Primary navigation\" data-navigation>\n        <a href=\"/plugins/\">Plugins</a>\n        <a href=\"/docs/\" aria-current=\"page\">Documentation</a>\n        <a href=\"/releases/\">Releases</a>\n        <a href=\"/about/\">About</a>\n      </nav>\n      <div class=\"header-actions\">\n        <a class=\"header-github\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\" aria-label=\"Cobbleworks on GitHub\">\n          <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z\"/></svg>\n        </a>\n        <a class=\"button button-primary header-cta\" href=\"/plugins/\">Browse plugins</a>\n      </div>\n    </header>\n    <main id=\"main-content\" class=\"page-shell\">\n      <section class=\"section-stack\">\n        <div class=\"section-heading section-heading-split\">\n          <div>\n            <p class=\"eyebrow\"><span></span> Getting started</p>\n            <h1>Documentation</h1>\n          </div>\n          <p class=\"section-lead\">The plugin README in each repository is the definitive reference; this page acts as a quick gateway for install basics, troubleshooting, and navigation.</p>\n        </div>\n        <div class=\"docs-layout\">\n          <aside class=\"docs-sidebar\">\n            <nav aria-label=\"Documentation sections\">\n              <a href=\"#getting-started\">Getting started</a>\n              <a href=\"#installing-a-plugin\">Installing a plugin</a>\n              <a href=\"#configuration\">Configuration basics</a>\n              <a href=\"#troubleshooting\">Troubleshooting</a>\n              <a href=\"#plugin-readmes\">Plugin READMEs</a>\n              <a href=\"#contributing\">Contributing</a>\n            </nav>\n          </aside>\n          <div class=\"docs-content\">\n            <section id=\"getting-started\" class=\"doc-section\">\n              <h2>Getting started</h2>\n              <p>Choose the plugin that matches your server’s needs, then verify its README for supported platform, Java, Minecraft version, and dependency requirements before installation.</p>\n            </section>\n            <section id=\"installing-a-plugin\" class=\"doc-section\">\n              <h2>Installing a plugin</h2>\n              <ol>\n                <li>Download the plugin’s latest release JAR from the repository’s Releases page.</li>\n                <li>Place it into the server’s <code>plugins</code> folder.</li>\n                <li>Install any listed dependency before starting the server.</li>\n                <li>Restart the server and review the generated config files.</li>\n              </ol>\n            </section>\n            <section id=\"configuration\" class=\"doc-section\">\n              <h2>Configuration basics</h2>\n              <p>Most Cobbleworks plugins generate their own YAML configuration on first start. Review the project README to learn which file controls enabled features, item filters, commands, or reward settings.</p>\n            </section>\n            <section id=\"troubleshooting\" class=\"doc-section\">\n              <h2>Troubleshooting</h2>\n              <p>Confirm the server software, Java version, and Minecraft version match the plugin’s supported versions. If behavior looks wrong, compare the plugin’s README and releases for known compatibility notes and recent fixes.</p>\n            </section>\n            <section id=\"plugin-readmes\" class=\"doc-section\">\n              <h2>Plugin READMEs</h2>\n              <div class=\"doc-links\">\n                <a href=\"/plugins/\">Browse all plugins</a>\n                <a href=\"https://github.com/Cobbleworks\">Open the Cobbleworks organization</a>\n              </div>\n            </section>\n            <section id=\"contributing\" class=\"doc-section\">\n              <h2>Development and contributing</h2>\n              <p>Project source, issues, version history, and pull requests remain public on GitHub. The organization page is the best place to start if you want to follow a plugin’s active development.</p>\n            </section>\n          </div>\n        </div>\n      </section>\n    </main>\n    <footer class=\"site-footer\">\n      <div class=\"shell footer-inner\">\n        <a class=\"brand\" href=\"/\"><img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\"><span>Cobbleworks</span></a>\n        <p>Open-source Minecraft server plugins.</p>\n        <nav aria-label=\"Footer navigation\"><a href=\"/plugins/\">Plugins</a><a href=\"/docs/\">Documentation</a><a href=\"https://github.com/Cobbleworks\">GitHub</a></nav>\n      </div>\n    </footer>\n    <script src=\"/script.js\" defer></script>\n  </body>\n</html>\n"""),
    ("releases/index.html", "Releases | Cobbleworks", """<!doctype html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <title>Releases | Cobbleworks</title>\n    <meta name=\"description\" content=\"Release hub for Cobbleworks plugins and their latest public downloads.\">\n    <link rel=\"canonical\" href=\"https://cobbleworks.github.io/releases/\">\n    <link rel=\"icon\" href=\"/assets/favicon.svg\" type=\"image/svg+xml\">\n    <link rel=\"stylesheet\" href=\"/styles.css\">\n  </head>\n  <body data-page=\"releases\">\n    <a class=\"skip-link\" href=\"#main-content\">Skip to content</a>\n    <header class=\"site-header\" data-header>\n      <a class=\"brand\" href=\"/\" aria-label=\"Cobbleworks home\">\n        <img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\">\n        <span>Cobbleworks</span>\n      </a>\n      <button class=\"menu-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"site-navigation\" data-menu-button>\n        <span class=\"sr-only\">Open navigation</span>\n        <span></span><span></span><span></span>\n      </button>\n      <nav id=\"site-navigation\" class=\"site-nav\" aria-label=\"Primary navigation\" data-navigation>\n        <a href=\"/plugins/\">Plugins</a>\n        <a href=\"/docs/\">Documentation</a>\n        <a href=\"/releases/\" aria-current=\"page\">Releases</a>\n        <a href=\"/about/\">About</a>\n      </nav>\n      <div class=\"header-actions\">\n        <a class=\"header-github\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\" aria-label=\"Cobbleworks on GitHub\">\n          <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z\"/></svg>\n        </a>\n        <a class=\"button button-primary header-cta\" href=\"/plugins/\">Browse plugins</a>\n      </div>\n    </header>\n    <main id=\"main-content\" class=\"page-shell\">\n      <section class=\"section-stack\">\n        <div class=\"section-heading section-heading-split\">\n          <div>\n            <p class=\"eyebrow\"><span></span> All releases</p>\n            <h1>Release hub</h1>\n          </div>\n          <p class=\"section-lead\">The GitHub Releases page is the canonical source for each plugin’s latest download and changelog notes.</p>\n        </div>\n        <div id=\"release-grid\" class=\"release-grid\"></div>\n      </section>\n    </main>\n    <footer class=\"site-footer\">\n      <div class=\"shell footer-inner\">\n        <a class=\"brand\" href=\"/\"><img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\"><span>Cobbleworks</span></a>\n        <p>Open-source Minecraft server plugins.</p>\n        <nav aria-label=\"Footer navigation\"><a href=\"/plugins/\">Plugins</a><a href=\"/docs/\">Documentation</a><a href=\"https://github.com/Cobbleworks\">GitHub</a></nav>\n      </div>\n    </footer>\n    <script src=\"/script.js\" defer></script>\n  </body>\n</html>\n"""),
    ("about/index.html", "About | Cobbleworks", """<!doctype html>\n<html lang=\"en\">\n  <head>\n    <meta charset=\"utf-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n    <title>About | Cobbleworks</title>\n    <meta name=\"description\" content=\"Learn what Cobbleworks is, how it maintains open-source Minecraft plugins, and how to report issues or contribute.\">\n    <link rel=\"canonical\" href=\"https://cobbleworks.github.io/about/\">\n    <link rel=\"icon\" href=\"/assets/favicon.svg\" type=\"image/svg+xml\">\n    <link rel=\"stylesheet\" href=\"/styles.css\">\n  </head>\n  <body data-page=\"about\">\n    <a class=\"skip-link\" href=\"#main-content\">Skip to content</a>\n    <header class=\"site-header\" data-header>\n      <a class=\"brand\" href=\"/\" aria-label=\"Cobbleworks home\">\n        <img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\">\n        <span>Cobbleworks</span>\n      </a>\n      <button class=\"menu-button\" type=\"button\" aria-expanded=\"false\" aria-controls=\"site-navigation\" data-menu-button>\n        <span class=\"sr-only\">Open navigation</span>\n        <span></span><span></span><span></span>\n      </button>\n      <nav id=\"site-navigation\" class=\"site-nav\" aria-label=\"Primary navigation\" data-navigation>\n        <a href=\"/plugins/\">Plugins</a>\n        <a href=\"/docs/\">Documentation</a>\n        <a href=\"/releases/\">Releases</a>\n        <a href=\"/about/\" aria-current=\"page\">About</a>\n      </nav>\n      <div class=\"header-actions\">\n        <a class=\"header-github\" href=\"https://github.com/Cobbleworks\" target=\"_blank\" rel=\"noreferrer\" aria-label=\"Cobbleworks on GitHub\">\n          <svg viewBox=\"0 0 24 24\" aria-hidden=\"true\"><path d=\"M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z\"/></svg>\n        </a>\n        <a class=\"button button-primary header-cta\" href=\"/plugins/\">Browse plugins</a>\n      </div>\n    </header>\n    <main id=\"main-content\" class=\"page-shell\">\n      <section class=\"section-stack\">\n        <div class=\"section-heading section-heading-split\">\n          <div>\n            <p class=\"eyebrow\"><span></span> Mission</p>\n            <h1>About Cobbleworks</h1>\n          </div>\n          <p class=\"section-lead\">Cobbleworks publishes practical, open-source Minecraft server plugins built around server ownership, systems design, and independent maintenance.</p>\n        </div>\n        <div class=\"info-grid\">\n          <article class=\"info-card\"><h3>Open source</h3><p>Every Cobbleworks plugin is published with open source code and public project history on GitHub.</p></article>\n          <article class=\"info-card\"><h3>Independent</h3><p>Each project has its own README, releases, issue tracker, and compatibility profile instead of a single shared monolith.</p></article>\n          <article class=\"info-card\"><h3>Built for servers</h3><p>The plugin library focuses on tools that solve real server problems, from progression to automation and world systems.</p></article>\n        </div>\n        <div class=\"doc-section\">\n          <h2>Project links</h2>\n          <div class=\"doc-links\">\n            <a href=\"https://github.com/Cobbleworks\">Cobbleworks organization</a>\n            <a href=\"https://github.com/Cobbleworks/.github\">Organization profile and shared project docs</a>\n            <a href=\"/plugins/\">Plugin directory</a>\n            <a href=\"/docs/\">Documentation</a>\n          </div>\n        </div>\n      </section>\n    </main>\n    <footer class=\"site-footer\">\n      <div class=\"shell footer-inner\">\n        <a class=\"brand\" href=\"/\"><img src=\"/assets/brand-mark.svg\" width=\"32\" height=\"32\" alt=\"\"><span>Cobbleworks</span></a>\n        <p>Open-source Minecraft server plugins.</p>\n        <nav aria-label=\"Footer navigation\"><a href=\"/plugins/\">Plugins</a><a href=\"/docs/\">Documentation</a><a href=\"https://github.com/Cobbleworks\">GitHub</a></nav>\n      </div>\n    </footer>\n    <script src=\"/script.js\" defer></script>\n  </body>\n</html>\n"""),
]:
    target = OUT / filename
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

print(f"Generated {len(plugins)} plugin pages and site pages under {OUT}")
