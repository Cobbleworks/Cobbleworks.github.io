# Redesign validation — 1 October 2026

The static builder and validator passed for 22 indexable pages plus the 404 document. Validation covers local links/assets, anchors, unique page titles, structured data, sitemap coverage, and named release JARs with matching tags.

Browser verification checked all 22 pages at 1440, 768, 390, and 320 px: **88 layout checks**, with no document overflow, clipped hero actions, clipped requirement panels, or extra H1 headings. Representative mobile layouts also passed WebKit checks.

**14 axe audits** across desktop/mobile homepage, directory, Map Revealer, Blood Moon, downloads, compatibility, and docs reported no WCAG A/AA violations. Automated audits do not cover every aspect of accessibility; keyboard menu operation, Escape/focus return, and no-JavaScript navigation/download availability were separately exercised.

Search, combined category/platform/status filters, shareable URLs and reload restoration, empty-state reset, development/archive states, and compatibility filters passed browser checks. All release metadata matched upstream stable versions after the same-day Blockfolk 1.4.0, Blood Moon 2.0.1, and Map Revealer 1.2.1 updates.

Local Lighthouse mobile simulation: **97 performance, 100 accessibility, 100 best practices, 100 SEO**. Measured LCP was 2.6 s, CLS 0, total blocking time 0 ms, and initial transfer about 334 KiB. These are lab measurements from the local static preview, not field guarantees. The earlier homepage audit fetched approximately 3.36 MB on mobile and 5.78 MB on desktop; its 390 px hero content extended to 510 px and clipped.
