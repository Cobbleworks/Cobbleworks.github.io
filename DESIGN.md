# Cobbleworks design direction

The site follows the supplied dark design studio concept: blue-charcoal surfaces (`#080D12`, `#0F1720`, `#14202A`), warm copper for actions (`#E8903A`), cyan only for focus rings, Space Grotesk headings, and Inter body text. Layout rhythm on the homepage also borrows from the second reference (hero facts, image band with figures, principle tiles, FAQ).

## Homepage

1. **Evening fortress header.** Text sits on a local left-side shade so the castle stays visible. Four factual hero facts follow.
2. **Featured plugins.** Four cards with plugin artwork, the pixel icon overlapping the image edge, and requirement chips.
3. **Latest releases.** Generated from release dates in the catalogue.
4. **Whole collection.** All fifteen projects grouped by purpose.
5. **Moonlit castle band.** "Open source. Built for real servers." with true figures only.
6. **How Cobbleworks works and FAQ.** Real questions about platforms, Java, licence, dependencies, upgrades, and bug reports.

## Plugin pages

Each plugin page has a cinematic header from its own artwork: breadcrumb, icon, name, headline, requirement chips, and Download / Documentation / GitHub actions. A sticky section bar then links to Overview, Features, Installation, Commands, Permissions, Configuration, and Release notes, showing only the sections that exist. The overview pairs "What it does" with a compatibility card and the real gameplay gallery. Long permission and configuration tables collapse behind a disclosure. Each page ends with a support panel and three related plugins.

Header variants depend on available artwork: full-bleed artwork, a native-size banner over a blurred backdrop, or the large pixel icon on a grid for projects without artwork (Superwarp, NPC PickUp).

## Icons

One hand-made 16 × 16 pixel-art family (`scripts/icons.py`): a shared 30-colour palette, one warm outline colour, light from the top left, and three tones per material. Each icon shows a concrete subject (trophy, rewind block, villager head, blood moon, music disc, grappling hook, revealed map, piston, pickaxe, minecart, enchanted sword, crafter grid, redstone torch, portal, lifted NPC). They are displayed in a consistent dark tile and rendered with `image-rendering: pixelated`.

## Deliberately left out

Some reference elements were not adopted because they would be untrue for Cobbleworks: prices, carts, "bestseller" badges, customer counts, ratings, testimonials, "regular updates" promises, and invented version histories. The compatibility table distinguishes build target from documented range and shows no fabricated tested matrix. A theme switch was omitted because the identity is dark-only.

## Content boundaries

Thirteen released plugins, Superwarp in development (no release, no licence), and the archived NPC PickUp. Blood Moon 2.0.1 needs Blockfolk 1.4.0+, Paper 26.2, and Java 25. Power Mining's platform discrepancy is explained on the compatibility page. Repository names, plugin implementations, and historical releases are unchanged.
