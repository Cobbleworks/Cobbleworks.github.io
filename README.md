# Cobbleworks website

This repository contains the static GitHub Pages site for the Cobbleworks plugin publisher. The site is intentionally lightweight: plain HTML, shared CSS, small vanilla JavaScript, and a single source-of-truth plugin metadata file.

## Site structure

- `index.html` — homepage and featured plugin entry point
- `plugins/index.html` — directory/listing page for the plugin catalog
- `plugins/<slug>/index.html` — individual product pages for each plugin
- `docs/index.html` — documentation landing page
- `releases/index.html` — release hub
- `about/index.html` — about/community overview
- `data/plugins.json` — canonical plugin metadata used by the homepage, plugin directory, and generated pages
- `assets/` — shared site branding, hero art, and plugin images
- `scripts/generate_site.py` — utility script used to generate plugin product pages from the metadata file
- `styles.css` — shared design system
- `script.js` — small interactive layer for navigation, filtering, and card rendering

## Plugin metadata

The canonical metadata lives in `data/plugins.json`. Each entry should include the real plugin name, repository URL, supported Minecraft versions, Java version, platforms, summary, features, screenshots, and release URL.

When a plugin changes, update that file first and then regenerate the product pages with:

```bash
python scripts/generate_site.py
```

The generated detail pages are static HTML and remain fully compatible with GitHub Pages.

## Plugin images

Plugin artwork and screenshots should be kept under `assets/plugins/<slug>/`. Use the project's own repository images where possible, but keep only the selected images needed by the website. Keep filenames consistent and reasonably descriptive.

## Local preview

Run a static web server from the repository root:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/`.

## Deployment

GitHub Pages deploys the repository content exactly as checked in. The workflow in `.github/workflows/deploy-pages.yml` validates the required static files and publishes the site from the `main` branch.

## Adding a new plugin

1. Add the plugin entry to `data/plugins.json`.
2. Copy any relevant banner/screenshots into `assets/plugins/<slug>/`.
3. Regenerate the pages with `python scripts/generate_site.py`.
4. Verify the homepage, directory, and detail page render correctly.
