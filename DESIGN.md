# Cobbleworks design direction

The site uses a title-screen-era Minecraft look across every page: dirt, deepslate, cobblestone, and bedrock grounds; bevelled stone buttons that turn blue on hover; inventory slots for plugin icons; purple-edged item tooltips for plugin cards; advancement toasts for releases; and a written-book page for compatibility facts. Colours come from Minecraft's chat palette (yellow labels, aqua names and links, gold notices).

Type has three roles. Press Start 2P is for the logo and h1/h2 titles. Pixelify Sans is for interface text at 18px and above: navigation, buttons, plugin names, tags, and table headings. Inter is for everything people read: paragraphs, lists, descriptions, chips, tables, and captions. Pixel fonts are kept out of small and long text because they are hard to read there. All three fonts are self-hosted with their OFL licences.

## Homepage

1. **Title screen.** A slowly panning panorama, the extruded cobblestone logo, a clickable yellow splash line, stone menu buttons, four factual toasts, and corner text. The header is transparent over it until the page scrolls.
2. **Highlights.** Five spotlights, each laid out to show what players get: Blockfolk on dirt with a hotbar screenshot picker, Wireless Redstone in a torch-lit deepslate shaft with a lever-and-lamps demo, Blood Moon as a red night with its seven encounters, and Custom Jukebox and Map Revealer as paired item tooltips. Copy lives in `content/spotlights.json`; versions, requirements, and downloads come from `content/plugins.json`.
3. **Latest releases and the whole collection.** On cobblestone: the four newest releases as toasts, then all fifteen projects in three columns of groups, each linking to its plugin page.
4. **Everything is on GitHub.** A multiplayer server-list entry for the organisation.

## Plugin pages

Each plugin page has a cinematic header from its own artwork: breadcrumb, icon, name, headline, requirement chips, and Download / Documentation / GitHub actions. A sticky section bar then links to Overview, Features, Installation, Commands, Permissions, Configuration, and Release notes, showing only the sections that exist. The overview pairs "What it does" with a compatibility card and the real gameplay gallery. Long permission and configuration tables collapse behind a disclosure. Each page ends with a support panel and three related plugins.

Header variants depend on available artwork: full-bleed artwork, a native-size banner over a blurred backdrop, or the large pixel icon on a grid for projects without artwork (Superwarp, NPC PickUp).

## Icons

One hand-made 16 × 16 pixel-art family (`scripts/icons.py`): a shared 30-colour palette, one warm outline colour, light from the top left, and three tones per material. Each icon shows a concrete subject (trophy, rewind block, villager head, blood moon, music disc, grappling hook, revealed map, piston, pickaxe, minecart, enchanted sword, crafter grid, redstone torch, portal, lifted NPC). They are displayed in a consistent dark tile and rendered with `image-rendering: pixelated`.

## Deliberately left out

Some reference elements were not adopted because they would be untrue for Cobbleworks: prices, carts, "bestseller" badges, customer counts, ratings, testimonials, "regular updates" promises, and invented version histories. The compatibility table distinguishes build target from documented range and shows no fabricated tested matrix. A theme switch was omitted because the identity is dark-only.

## Content boundaries

Thirteen released plugins, Superwarp in development (no release, no licence), and the archived NPC PickUp. Blood Moon 2.0.1 needs Blockfolk 1.4.0+, Paper 26.2, and Java 25. Power Mining's platform discrepancy is explained on the compatibility page. Repository names, plugin implementations, and historical releases are unchanged.
