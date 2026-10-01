# Cobbleworks website

The official [Cobbleworks website](https://cobbleworks.github.io/): plugin directory, individual product pages, downloads, installation guides, compatibility information, and release notes.

The website serves static HTML, CSS, SVG, WebP images, and a small JavaScript enhancement. It uses no runtime framework, third-party visitor JavaScript, or browser GitHub API requests. Fonts are hosted locally with their OFL licences. Navigation, product information, and JAR downloads remain usable without JavaScript.

## Build and preview

Python 3.12 or newer is the only build requirement. No additional Python packages are needed.

```sh
python scripts/build_site.py
python scripts/validate_site.py
python -m http.server 8080
```

Open `http://localhost:8080/`. Generated HTML is checked in so any static server can preview it. GitHub Actions rebuilds and validates every route before packaging and deploying to GitHub Pages on pushes to `main`.

## Updating a product

Edit `content/plugins.json`, then rebuild. It is the shared source for cards, individual pages, downloads, compatibility, release summaries, and product metadata. Do not edit generated HTML directly.

Each product records its status, content, SVG symbol, real gameplay screenshots, commands, permissions, and release-specific facts. Keep platform, Minecraft build target, documented range, Java requirement, dependencies, integrations, licence evidence, and named JAR separate. Development projects have no invented release or licence; archived projects retain historical documentation.

Check for newer stable releases with:

```sh
python scripts/check_releases.py
```

Set `GITHUB_TOKEN` when needed for an authenticated API limit. The checker reports changes without overwriting reviewed documentation. For a new version, read its tagged README and release notes, update the catalogue, and check screenshot relevance before rebuilding. Never rewrite historical plugin releases.

## Artwork and symbols

The homepage uses the supplied evening fortress artwork in responsive WebP sizes. Product galleries use gameplay captures from the respective repositories. Large gallery images are linked separately and loaded only when requested. Previous public artwork URLs remain available.

Product symbols use one 48 px SVG grid with shared strokes, colours, and geometry; their source is in `scripts/build_site.py`. The organisation mark retains its existing cube design.

## Validation

`scripts/validate_site.py` checks every generated page, local asset/link, section anchor, unique title, structured data, sitemap route, and release JAR tag. Deployment packages all nested routes. The separate Blockfolk documentation site at `/Blockfolk-NPC-Plugin/` is preserved.

The redesign was also checked in Chromium at 1440, 768, 390, and 320 px, with mobile WebKit checks, accessibility audits, search/filter journeys, keyboard navigation, and no-JavaScript operation. See [DESIGN.md](DESIGN.md) for design decisions and content boundaries.
