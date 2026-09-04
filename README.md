# Cobbleworks Website

The static landing page for [Cobbleworks](https://github.com/Cobbleworks), published at [cobbleworks.github.io](https://cobbleworks.github.io/).

The site has no runtime framework or third-party JavaScript. GitHub Pages deploys the checked-in HTML, CSS, JavaScript, and image assets after every push to `main`.

## Local preview

Run any static HTTP server from the repository root. For example:

```bash
python -m http.server 8080
```

Then open `http://localhost:8080/`.

## Updating plugins

Plugin cards are kept in `index.html`, and their artwork lives under `assets/plugins/`. Keep repository links, descriptions, supported Java versions, the plugin count, structured data, and filter keywords aligned when adding or retiring a plugin.

## Search visibility

The landing page includes a canonical URL, crawl directives, Open Graph metadata, `WebSite` and `Organization` structured data, a sitemap, and descriptive semantic content. Indexing timing and final search presentation remain controlled by search engines.
