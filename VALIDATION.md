# Validation — 1 October 2026

`python scripts/build_site.py && python scripts/validate_site.py` passes: 22 indexable pages plus the 404 page, with local links, assets, anchors, unique titles, structured data, sitemap coverage, and release JAR tags all checked.

Browser checks were run in Chrome (headless, Playwright):

- **Layout sweep.** All 23 documents at 320, 768, 1024, and 1440 px (92 checks): no horizontal page overflow, no element extending past the viewport outside scroll containers, no broken eager images, exactly one H1 per page, and no script errors or failed requests.
- **Interactions.** Mobile menu opens and closes with Escape. Plugin search narrows results and shows the empty state. The compatibility Java filter narrows rows. Jumping to a section updates the sticky section bar.
- **Visual review.** Screenshots of the homepage, directory, a full-artwork plugin (Map Revealer), a banner-only plugin (Area Rewind), a project without artwork (Superwarp), downloads, compatibility, changelog, and docs at desktop and 390 px mobile widths.

Not re-run for this version: automated accessibility audits (axe) and Lighthouse.
