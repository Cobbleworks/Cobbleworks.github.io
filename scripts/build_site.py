"""Build the Cobbleworks static website using Python's standard library."""
from datetime import datetime
from html import escape
from pathlib import Path
import json
import re

from icons import build as build_icons

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://cobbleworks.github.io'
CATALOGUE = json.loads((ROOT / 'content/plugins.json').read_text(encoding='utf-8'))
PLUGINS = CATALOGUE['plugins']
RELEASED = [p for p in PLUGINS if p['status'] == 'released']
BY_SLUG = {p['slug']: p for p in PLUGINS}
ORG = 'https://github.com/Cobbleworks'
PAGES = []

SPOTLIGHTS = json.loads((ROOT / 'content/spotlights.json').read_text(encoding='utf-8'))
SPLASHES = ['Open source!', 'Do distribute!', 'MIT licensed!', 'Also try Paper!', 'Now with Java 25!', 'Redstone not included!',
            'Minecarts go brr!', 'Pull requests welcome!', 'Blood Moon rising!', 'Backups saved!', 'Made of cobblestone!',
            '100% pure Java!', 'Wireless redstone!', 'Read the README!', 'Grapple responsibly!']
GROUPS = [
    ('World & maps', ['map-revealer', 'area-rewind', 'superwarp']),
    ('Automation & redstone', ['wireless-redstone', 'useful-autocrafter', 'piston-crusher']),
    ('NPCs & events', ['blockfolk', 'blood-moon', 'npc-pickup']),
    ('Gameplay & equipment', ['advanced-achievements', 'super-enchantments', 'power-mining', 'custom-jukebox']),
    ('Transport & movement', ['rail-boost', 'hookshot']),
]
# Horizontal focus of each plugin's header artwork (CSS object-position).
FOCUS = {'blockfolk': '30%', 'advanced-achievements': '62%', 'area-rewind': '70%', 'rail-boost': '60%'}


def e(value):
    return escape(str(value), quote=True)


def date(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%d %b %Y').lstrip('0')


def glyph(name):
    paths = {
        'arrow': '<path d="M5 12h14m-6-6 6 6-6 6"/>',
        'external': '<path d="M14 5h5v5m0-5-8 8M18 14v5H5V6h5"/>',
        'download': '<path d="M12 4v11m-5-5 5 5 5-5M5 20h14"/>',
        'book': '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5v-15ZM4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
        'licence': '<path d="M12 3 4 6v6c0 4.5 3.4 8.3 8 9 4.6-.7 8-4.5 8-9V6l-8-3Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
        'blocks': '<path d="M3 7.5 8 5l5 2.5v5L8 15l-5-2.5v-5ZM11 14.5l5-2.5 5 2.5v5L16 22l-5-2.5v-5Z"/><path d="M3 7.5 8 10l5-2.5M8 10v5M11 14.5l5 2.5 5-2.5M16 17v5"/>',
        'server': '<rect x="3" y="4" width="18" height="7" rx="1.5"/><rect x="3" y="13" width="18" height="7" rx="1.5"/><path d="M7 7.5h.01M7 16.5h.01M11 7.5h6M11 16.5h6"/>',
        'code': '<path d="m8 7-5 5 5 5m8-10 5 5-5 5M14 4l-4 16"/>',
        'list': '<path d="M9 6h11M9 12h11M9 18h11M4 6h.01M4 12h.01M4 18h.01"/>',
        'issue': '<circle cx="12" cy="12" r="9"/><path d="M12 7.5v5.5M12 16.5h.01"/>',
        'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        'dash': '<path d="M7 12h10"/>',
        'chevron': '<path d="m6 9 6 6 6-6"/>',
        'menu': '<path d="M4 6h16M4 12h16M4 18h16"/>',
        'copy': '<rect x="8" y="8" width="12" height="12" rx="2"/><path d="M16 8V5a1 1 0 0 0-1-1H5a1 1 0 0 0-1 1v10a1 1 0 0 0 1 1h3"/>',
    }
    return f'<svg class="glyph" viewBox="0 0 24 24" aria-hidden="true">{paths[name]}</svg>'


GITHUB = '<svg class="glyph" viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" stroke="none" d="M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z"/></svg>'


def icon(slug, size=40):
    return f'<span class="plugin-icon" style="--size:{size}px"><img src="/assets/icons/{e(slug)}.svg" width="{size}" height="{size}" alt=""></span>'


def button(href, label, kind='secondary', lead='', trail=''):
    return f'<a class="button button-{kind}" href="{e(href)}">{glyph(lead) if lead and lead != "github" else GITHUB if lead == "github" else ""}<span>{e(label)}</span>{glyph(trail) if trail else ""}</a>'


def text_link(href, label, trail='arrow'):
    return f'<a class="text-link" href="{e(href)}">{e(label)}{glyph(trail)}</a>'


def product_link(p): return '/plugins/' + p['slug'] + '/'
def repository(p): return ORG + '/' + p['repository']
def version(p): return p['release']['tag'] if p['release'] else 'In development'
def asset(p): return p['release']['asset']['browser_download_url']
def has_art(p): return (ROOT / 'assets/art' / f'{p["slug"]}-card.webp').is_file()
def platforms(p): return 'spigot paper' if 'Spigot' in p['platform'] else 'paper'


def header(active):
    links = [('plugins', 'Plugins'), ('docs', 'Docs'), ('downloads', 'Downloads'), ('compatibility', 'Compatibility'), ('changelog', 'Changelog')]
    nav = ''.join(f'<a href="/{key}/"{" aria-current=page" if active == key else ""}>{label}</a>' for key, label in links)
    return f'''<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><div class="shell header-inner">
<a class="brand" href="/" aria-label="Cobbleworks home"><img src="/assets/brand-mark.svg" width="32" height="32" alt=""><span>Cobbleworks</span></a>
<nav class="site-nav" id="site-navigation" aria-label="Primary" data-navigation>{nav}</nav>
<a class="header-github" href="{ORG}" aria-label="Cobbleworks on GitHub">{GITHUB}<span>GitHub</span></a>
<button class="menu-button" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="site-navigation" hidden data-menu-button>{glyph('menu')}</button>
</div></header>'''


def footer():
    plugin_links = ''.join(f'<li><a href="{product_link(p)}">{e(p["name"])}</a></li>' for p in sorted(RELEASED, key=lambda p: p['name']))
    return f'''<footer class="site-footer"><div class="shell footer-grid">
<div class="footer-brand"><a class="brand" href="/"><img src="/assets/brand-mark.svg" width="28" height="28" alt=""><span>Cobbleworks</span></a><p>Independent, open-source plugins for Minecraft servers. Each project has its own repository, releases, and documentation.</p>{button(ORG, 'Cobbleworks on GitHub', 'secondary', 'github')}</div>
<nav class="footer-plugins" aria-label="Plugins"><h2>Plugins</h2><ul>{plugin_links}</ul></nav>
<nav aria-label="Resources"><h2>Resources</h2><ul><li><a href="/docs/">Installation guide</a></li><li><a href="/downloads/">Downloads</a></li><li><a href="/compatibility/">Compatibility</a></li><li><a href="/changelog/">Release notes</a></li></ul></nav>
<nav aria-label="Organisation"><h2>Organisation</h2><ul><li><a href="/about/">About</a></li><li><a href="{ORG}/.github/blob/main/CONTRIBUTING.md">Contributing</a></li><li><a href="{ORG}/.github/blob/main/SECURITY.md">Security</a></li><li><a href="{ORG}">GitHub</a></li></ul></nav>
</div><div class="shell footer-bottom"><span>MIT-licensed plugins, built in the open.</span><span>Not an official Minecraft product. Not approved by or associated with Mojang or Microsoft.</span></div></footer>'''


def write_page(route, title, description, content, active='', schema=None, preload='', noindex=False):
    full_title = 'Cobbleworks — Open-source Minecraft server plugins' if route == '/' else f'{title} · Cobbleworks'
    graph = [{'@context': 'https://schema.org', '@type': 'WebPage', 'name': full_title, 'url': BASE + route, 'description': description}]
    if schema:
        graph.append({'@context': 'https://schema.org', **schema})
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#080d12"><meta name="color-scheme" content="dark"><meta name="robots" content="{'noindex' if noindex else 'index, follow, max-image-preview:large'}">
<link rel="canonical" href="{BASE + route}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest"><link rel="preload" href="/assets/fonts/inter-0.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/space-grotesk-0.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/styles.css">{preload}
<meta property="og:type" content="website"><meta property="og:site_name" content="Cobbleworks"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE + route}"><meta property="og:image" content="{BASE}/assets/social-preview.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="A lantern-lit Minecraft fortress overlooking a mountain valley at sunset"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/assets/social-preview.jpg">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False).replace('<', '\\u003c')}</script><script src="/script.js" defer></script></head><body>{header(active)}<main id="main-content" tabindex="-1">{content}</main>{footer()}</body></html>'''
    output = ROOT / ('index.html' if route == '/' else '404.html' if route == '/404.html' else route.strip('/') + '/index.html')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html + '\n', encoding='utf-8')
    if not noindex:
        PAGES.append(route)


def page_head(eyebrow, title, lead, extra=''):
    return f'<section class="page-head"><div class="shell"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(title)}</h1><p class="lead">{e(lead)}</p>{extra}</div></section>'


def section_head(title, lead='', link='', label='', eyebrow=''):
    more = text_link(link, label) if link else ''
    return f'<div class="section-head"><div>{f"<p class=eyebrow>{e(eyebrow)}</p>" if eyebrow else ""}<h2>{e(title)}</h2>{f"<p>{e(lead)}</p>" if lead else ""}</div>{more}</div>'


def chips(items):
    return '<ul class="chips">' + ''.join(f'<li>{e(x)}</li>' for x in items if x) + '</ul>'


def card_art(p):
    if has_art(p):
        return f'<img class="card-art" src="/assets/art/{p["slug"]}-card.webp" width="720" height="327" alt="" loading="lazy">'
    return f'<div class="card-art card-art-empty" aria-hidden="true"><img src="/assets/icons/{p["slug"]}.svg" width="64" height="64" alt=""></div>'


def card(p):
    status = {'development': 'In development', 'archived': 'Archived'}.get(p['status'])
    meta = [p['platform'], f'Java {p["java"]}+' if p['status'] != 'archived' else '', version(p) if p['status'] == 'released' else '']
    return f'''<article class="plugin-card" data-plugin data-category="{e(' '.join(p['categories']))}" data-platform="{platforms(p)}" data-status="{p['status']}">
<a class="card-link" href="{product_link(p)}"><div class="card-media">{card_art(p)}{f'<span class="status-badge">{status}</span>' if status else ''}</div>
<div class="card-body"><div class="card-title">{icon(p['slug'], 36)}<div><h3>{e(p['name'])}</h3><p class="card-category">{e(p['category'])}</p></div>{glyph('arrow')}</div>
<p class="card-description">{e(p['description'])}</p>{chips(meta)}</div></a></article>'''


# ---------------------------------------------------------------- homepage

def title_screen():
    """Homepage hero in the style of the Minecraft title screen."""
    java = sorted({p['java'] for p in RELEASED})
    toasts = [
        ('book', 'MIT licensed', f'All {len(RELEASED)} released plugins.'),
        ('chest', 'Independent projects', 'Install only what you need.'),
        ('redstone', 'Paper & Spigot', f'Java {java[0]} to {java[-1]}.'),
        ('pickaxe', 'Built in the open', 'Source, issues, and releases on GitHub.'),
    ]
    toast_html = ''.join(f'<li class="toast"><img src="/assets/textures/{i}.svg" width="32" height="32" alt=""><div><strong>{e(t)}</strong><span>{e(s)}</span></div></li>' for i, t, s in toasts)
    splashes = [f'{len(RELEASED)} plugins!'] + SPLASHES
    return f'''<section class="title-screen" aria-labelledby="hero-title">
<div class="panorama" aria-hidden="true"><img class="panorama-image" src="/assets/hero/title-screen-1672.webp" srcset="/assets/hero/title-screen-960.webp 960w, /assets/hero/title-screen-1672.webp 1672w" sizes="125vw" width="1672" height="941" alt="" fetchpriority="high"></div>
<div class="title-shade" aria-hidden="true"></div>
<div class="shell title-content"><div class="logo-wrap"><h1 id="hero-title" class="logo"><span class="logo-word" data-text="COBBLEWORKS">COBBLEWORKS</span><span class="logo-edition">Minecraft plugins that do more.</span></h1>
<button class="splash" type="button" aria-hidden="true" tabindex="-1" title="Click for another splash" data-splash data-splashes="{e(json.dumps(splashes))}">{e(splashes[0])}</button></div>
<p class="title-copy">Cobbleworks creates open-source plugins for Minecraft servers. From world tools and automation to NPCs and gameplay systems, each project is built around a specific server need.</p>
<nav class="title-menu" aria-label="Quick links"><a class="mc-button" href="/plugins/">Browse Plugins</a><a class="mc-button" href="{ORG}">{GITHUB}View on GitHub</a>
<div class="title-menu-row"><a class="mc-button" href="/docs/">Install Guide...</a><a class="mc-button" href="/about/">About</a></div></nav></div>
<ul class="title-toasts" aria-label="Cobbleworks at a glance">{toast_html}</ul>
<p class="title-corner title-corner-left">Cobbleworks · Paper &amp; Spigot</p><p class="title-corner title-corner-right">Open source. Do distribute!</p></section>'''


def spot_command(command):
    cmd, arg = command
    return f'<p class="spot-command"><code><b>/</b>{e(cmd.lstrip("/"))}{f" <span>{e(arg)}</span>" if arg else ""}</code></p>'


def inline_code(text):
    """Escape text and render `backticked` spans as code."""
    return re.sub(r'`([^`]+)`', r'<code>\1</code>', e(text))


def spot_points(points):
    return '<ul class="spot-points">' + ''.join(f'<li>{f"<b>{e(b)}</b> " if b else ""}{inline_code(t)}</li>' for b, t in points) + '</ul>'


def spot_requirements(p):
    return chips([p['platform'], f'Minecraft {p["target"]}', f'Java {p["java"]}+'] + [f'Needs {d["name"]}' for d in p['required']])


def spot_actions(p, kind='primary'):
    return f'<div class="actions">{button(asset(p), "Download " + version(p), kind, "download")}{button(product_link(p), "Plugin details", "secondary", "", "arrow")}</div>'


def spot_title(p, s):
    return f'<p class="spot-tag">{e(s["tag"])}</p><div class="spot-title">{icon(p["slug"], 40)}<h3>{e(p["name"])}</h3></div><p class="spot-lede">{e(s["lede"])}</p>'


def spot_img(slug, name, alt, width=1120, height=630, cls=''):
    return f'<img{f" class={cls}" if cls else ""} src="/assets/spotlight/{slug}-{name}.webp" width="{width}" height="{height}" alt="{e(alt)}" loading="lazy">'


def spotlight(s):
    p = BY_SLUG[s['slug']]
    slug = p['slug']
    accent = f'style="--accent:{s["accent"]}"'
    copy = f'<div class="spot-copy">{spot_title(p, s)}{spot_points(s["points"])}{spot_command(s["command"]) if s.get("command") else ""}<div class="spot-foot">{spot_requirements(p)}{spot_actions(p)}</div></div>'

    if s['layout'] == 'gallery':
        first = s['gallery'][0]
        thumbs = ''.join(
            f'<a class="spot-thumb" href="/assets/spotlight/{slug}-{g["name"]}.webp" data-alt="{e(g["alt"])}"{" aria-current=true" if i == 0 else ""}>'
            f'<img src="/assets/spotlight/{slug}-{g["name"]}-thumb.webp" width="320" height="180" alt="" loading="lazy"><span>{e(g["label"])}</span></a>'
            for i, g in enumerate(s['gallery']))
        media = f'<div class="spot-media spot-gallery" data-gallery><figure class="spot-frame">{spot_img(slug, first["name"], first["alt"])}</figure><nav class="spot-thumbs" aria-label="{e(p["name"])} screenshots">{thumbs}</nav></div>'
        return f'<article class="spot" id="{slug}" {accent}><div class="shell spot-grid">{media}{copy}</div></article>'

    if s['layout'] == 'lamps':
        lamps = ''.join(f'<span class="lamp{" lamp-bulb" if i % 2 else ""}" style="--i:{i}"><i>{e(d)}</i></span>' for i, d in enumerate(s['lamps']))
        demo = f'''<div class="lampdemo" data-lampdemo><div class="lampdemo-bar"><span>group <b>factory-lights</b></span><span class="lampdemo-state" aria-live="polite">OFF</span></div>
<div class="lampdemo-row"><button class="lever" type="button" aria-pressed="false" aria-label="Flip the lever to toggle every linked lamp"><span class="lever-base"></span><span class="lever-stick"></span></button><span class="lampdemo-link" aria-hidden="true"></span><span class="lampdemo-lamps" aria-hidden="true">{lamps}</span></div>
<p class="lampdemo-hint">Flip the lever. No dust, no repeaters, no chunk loaders.</p></div>'''
        media = f'<div class="spot-media">{demo}<figure class="spot-frame spot-frame-wide">{spot_img(slug, s["shot"]["name"], s["shot"]["alt"])}</figure></div>'
        return f'<article class="spot spot-flip" id="{slug}" {accent}><div class="shell spot-grid">{media}{copy}</div></article>'

    if s['layout'] == 'night':
        foes = ''.join(f'<li><b>{e(n)}</b><span>{e(t)}</span></li>' for n, t in s['foes'])
        shots = ''.join(spot_img(slug, g['name'], g['alt']) for g in s['gallery'])
        needs = ', '.join(f'<a href="#{d["name"].split()[0].lower()}">{e(d["name"].split()[0])}</a>' for d in p['required'])
        return f'''<article class="spot-night" id="{slug}" {accent}><div class="night-sky" aria-hidden="true"><span class="night-moon"></span></div><div class="shell">
<div class="night-head">{spot_title(p, s)}</div><ol class="night-foes" aria-label="The seven Blood Moon encounters">{foes}</ol><div class="night-strip">{shots}</div>
<div class="night-foot">{spot_points(s["points"])}<div class="spot-foot"><p class="night-pair">Powered by {needs}. The bosses are Blockfolk NPCs, so install both.</p>{spot_requirements(p)}{spot_actions(p, "blood")}</div></div></div></article>'''

    overlay = ''
    if s.get('overlay') == 'nowplaying':
        overlay = '<div class="nowplaying" aria-hidden="true"><span class="nowplaying-disc"></span><span class="nowplaying-meta"><b>tetris a.nbs</b><small>playing · loop on</small></span><span class="nowplaying-bar"><i></i></span></div>'
    elif s.get('overlay') == 'swatches':
        overlay = '<ul class="swatches" aria-label="Some of the colour schemes">' + ''.join(f'<li style="--c:{c}">{e(n)}</li>' for n, c in s['swatches']) + '</ul>'
    return f'''<article class="spot-card" id="{slug}" {accent}><figure class="spot-card-media">{spot_img(slug, s["shot"]["name"], s["shot"]["alt"])}{overlay}</figure>
<div class="spot-card-body">{spot_title(p, s)}{spot_points(s["points"])}{spot_command(s["command"])}<div class="spot-foot">{spot_requirements(p)}{spot_actions(p)}</div></div></article>'''


def spotlights():
    intro = SPOTLIGHTS['intro']
    items = SPOTLIGHTS['spotlights']
    wide = ''.join(spotlight(s) for s in items if s['layout'] != 'card')
    cards = ''.join(spotlight(s) for s in items if s['layout'] == 'card')
    return f'''<section class="spotlights" aria-labelledby="highlights-title"><div class="shell">{section_head(intro['title'], intro['lead'], '/plugins/', 'View all plugins', intro['eyebrow']).replace('<h2>', '<h2 id="highlights-title">', 1)}</div>
{wide}<div class="shell spot-duo">{cards}</div></section>'''


def homepage():
    hero = title_screen()
    java = sorted({p['java'] for p in RELEASED})
    recent = sorted(RELEASED, key=lambda p: p['release']['published'], reverse=True)[:4]
    releases = ''.join(f'''<a class="release-tile" href="{product_link(p)}#release">{icon(p['slug'], 40)}<div><h3>{e(p['name'])}</h3><p><span class="version">{e(version(p))}</span><time datetime="{p['release']['published']}">{date(p['release']['published'])}</time></p></div>{glyph('arrow')}</a>''' for p in recent)

    groups = ''.join(f'<div class="collection-group"><h3>{e(name)}</h3><ul>' + ''.join(
        f'<li><a href="{product_link(BY_SLUG[s])}">{icon(s, 28)}<span>{e(BY_SLUG[s]["name"])}</span>{"<em>Archived</em>" if BY_SLUG[s]["status"] == "archived" else "<em>In development</em>" if BY_SLUG[s]["status"] == "development" else ""}</a></li>'
        for s in slugs) + '</ul></div>' for name, slugs in GROUPS)

    band = f'''<section class="band"><picture><img class="band-image" src="/assets/art/moonlit-castle-1672.webp" srcset="/assets/art/moonlit-castle-960.webp 960w, /assets/art/moonlit-castle-1672.webp 1672w" sizes="100vw" width="1672" height="941" alt="" loading="lazy"></picture><div class="band-shade" aria-hidden="true"></div>
<div class="shell band-inner"><div class="band-copy"><h2>Open source.<span>Built for real servers.</span></h2><p>Read the code, check the requirements, and follow each project on GitHub. Bug reports and contributions go straight to the plugin they concern.</p><div class="actions">{button('/plugins/', 'Browse plugins', 'primary', '', 'arrow')}{button(ORG, 'Join on GitHub', 'secondary', 'github')}</div></div>
<dl class="band-stats"><div><dt>Released plugins</dt><dd>{len(RELEASED)}</dd></div><div><dt>Licence</dt><dd>MIT</dd></div><div><dt>Server platforms</dt><dd>Paper · Spigot</dd></div><div><dt>Source</dt><dd>Open</dd></div></dl></div></section>'''

    principles = [
        ('blocks', 'One plugin, one purpose', 'No bundles and no shared core library. Add the plugins your server needs and leave the rest out.'),
        ('list', 'Requirements per release', 'Every page states the server software, Minecraft build target, Java version, and dependencies of the current release.'),
        ('book', 'Documented commands', 'Commands, permissions, and configuration keys are listed on each plugin page and in the tagged README.'),
        ('issue', 'Issues tracked in public', 'Report bugs and propose changes in the repository of the plugin concerned, where everyone can follow them.'),
    ]
    tiles = ''.join(f'<li>{glyph(g)}<h3>{t}</h3><p>{c}</p></li>' for g, t, c in principles)
    faq = [
        ('Which server software do the plugins support?', 'All plugins run on Paper. Several also support Spigot; each plugin page and the <a href="/compatibility/">compatibility table</a> state the platform of the current release.'),
        ('Which Java version do I need?', f'Between Java {java[0]} and Java {java[-1]}, depending on the plugin. Plugins built for Paper 26.2 need Java 25.'),
        ('Are the plugins free to use?', 'Yes. All released plugins are MIT licensed. You can run them on any server, read the source, and adapt them.'),
        ('Do any plugins depend on each other?', 'Blood Moon 2.0 requires <a href="/plugins/blockfolk/">Blockfolk 1.4.0</a> or newer. Custom Jukebox requires NoteBlockAPI. Every other plugin installs on its own.'),
        ('How do I update a plugin?', 'Read the release notes, stop the server, and replace the old JAR in <code>plugins/</code> with the new one. Keep a backup of your world and plugin data before upgrading.'),
        ('Where do I report a bug?', 'Open an issue in the repository of the plugin concerned. Include the plugin, server, and Java versions, plus the relevant console output.'),
    ]
    faq_html = ''.join(f'<details><summary>{q}{glyph("chevron")}</summary><p>{a}</p></details>' for q, a in faq)

    content = f'''{hero}
{spotlights()}
<section class="section section-tight shell">{section_head('Latest releases', 'Recent stable releases across the collection.', '/changelog/', 'View changelog')}<div class="release-row">{releases}</div></section>
<section class="section shell">{section_head('The whole collection', 'Fifteen projects, grouped by what they do on your server.')}<div class="collection">{groups}</div></section>
{band}
<section class="section shell split"><div>{section_head('How Cobbleworks works')}<ul class="principles">{tiles}</ul></div><div class="faq">{section_head('Frequently asked questions')}{faq_html}</div></section>'''
    preload = ('<link rel="preload" as="image" type="image/webp" href="/assets/hero/title-screen-1672.webp" imagesrcset="/assets/hero/title-screen-960.webp 960w, /assets/hero/title-screen-1672.webp 1672w" imagesizes="125vw" fetchpriority="high">'
               '<link rel="preload" href="/assets/fonts/press-start-2p-0.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/pixelify-sans-0.woff2" as="font" type="font/woff2" crossorigin>')
    write_page('/', 'Cobbleworks', 'Independent, open-source Minecraft server plugins for gameplay, world tools, automation, NPCs, and transport. Check requirements, download releases, and read the documentation.', content,
               schema={'@type': 'Organization', 'name': 'Cobbleworks', 'url': BASE, 'logo': BASE + '/assets/brand-mark.svg', 'sameAs': [ORG]}, preload=preload)


# ---------------------------------------------------------------- directory

def directory():
    content = page_head('Plugins', 'Every Cobbleworks plugin', f'{len(RELEASED)} released plugins, one project in development, and one archived project. Each has its own page with requirements, commands, and downloads.')
    filters = ''.join(f'<button type="button" data-filter="{k}" aria-pressed="{str(k == "all").lower()}">{l}</button>' for k, l in [('all', 'All'), ('world', 'World tools'), ('automation', 'Automation'), ('npc', 'NPCs'), ('gameplay', 'Gameplay'), ('admin', 'Administration')])
    content += f'''<section class="shell directory"><form class="toolbar" role="search" data-filter-form hidden>
<label class="search"><span class="visually-hidden">Search plugins</span><svg class="glyph" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg><input type="search" name="q" placeholder="Search plugins, e.g. maps or redstone" autocomplete="off" data-plugin-search></label>
<label class="select"><span class="visually-hidden">Platform</span><select name="platform" data-platform-filter><option value="all">All platforms</option><option value="paper">Paper</option><option value="spigot">Spigot</option></select></label>
<label class="select"><span class="visually-hidden">Project status</span><select name="status" data-status-filter><option value="current">Current projects</option><option value="released">Released</option><option value="development">In development</option><option value="archived">Archived</option><option value="all">All projects</option></select></label>
<div class="filter-row"><div class="segmented" role="group" aria-label="Category">{filters}</div><span class="count" aria-live="polite" data-plugin-count></span></div></form>
<div class="card-grid">{''.join(card(p) for p in PLUGINS)}</div>
<div class="empty-state" data-empty-state hidden><h2>No plugins match these filters.</h2><p>Try another search term or show the whole collection.</p><button class="button button-secondary" type="button" data-reset-filters><span>Reset filters</span></button></div>
<noscript><p class="note">All projects are shown. Search and filters need JavaScript.</p></noscript></section>'''
    write_page('/plugins/', 'Plugins', 'Browse every Cobbleworks Minecraft plugin by purpose, platform, and project status.', content, 'plugins',
               {'@type': 'ItemList', 'numberOfItems': len(PLUGINS), 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': p['name'], 'url': BASE + product_link(p)} for i, p in enumerate(PLUGINS)]})


# ---------------------------------------------------------------- plugin pages

def table(t, first_code=True, label='Reference table'):
    head = ''.join(f'<th scope="col">{e(h)}</th>' for h in t['headers'])
    rows = ''.join('<tr>' + ''.join(f'<td>{"<code>" + e(c) + "</code>" if i == 0 and first_code else e(c)}</td>' for i, c in enumerate(r)) + '</tr>' for r in t['rows'])
    return f'<div class="table-wrap" tabindex="0" role="region" aria-label="{e(label)}"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'


COLLAPSE_AFTER = {'commands': 24, 'permissions': 16, 'configuration': 16}


def reference_section(p, key, title, noun):
    tables = p[key]
    if not tables:
        return ''
    count = sum(len(t['rows']) for t in tables)
    body = ''.join(table(t, label=title) for t in tables)
    if count > COLLAPSE_AFTER[key]:
        body = f'<details class="disclosure"><summary><span>Show all {count} {noun}</span>{glyph("chevron")}</summary>{body}</details>'
    return f'<section class="doc-section" id="{key}"><h2>{title}<span class="count-badge">{count}</span></h2>{body}</section>'


def facts_card(p):
    r = p['release']
    required = ', '.join(f'<a href="{e(d["url"])}">{e(d["name"])}</a>' for d in p['required']) or 'None'
    optional = '<br>'.join(e(x) for x in p['optional']) or 'None'
    rows = [
        ('Latest release', f'{e(version(p))}' + (f' <span class="muted">· {date(r["published"])}</span>' if r else '')),
        ('Server software', e(p['platform'])),
        ('Minecraft build target', e(p['target'])),
        ('Documented range', e(p['documented_range'])),
        ('Java', f'{p["java"]}+' if p['status'] != 'archived' else 'Set by server and Citizens'),
        ('Required plugins', required),
        ('Optional integrations', optional),
        ('Licence', e(p['license'] or 'No licence published')),
    ]
    return '<aside class="facts-card"><h2>Compatibility</h2><dl>' + ''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a, b in rows) + f'</dl><a class="text-link small" href="/compatibility/">Compare all plugins{glyph("arrow")}</a></aside>'


def plugin_page(p):
    r = p['release']
    docs = p['docs']
    slug = p['slug']
    if r:
        primary = button(asset(p), ('Historical JAR ' if p['status'] == 'archived' else 'Download ') + version(p), 'primary', 'download')
    else:
        primary = button(repository(p), 'View source on GitHub', 'primary', 'github')
    actions = primary + button(docs, 'Documentation', 'secondary', 'book') + (button(repository(p), 'GitHub', 'ghost', 'github') if r else '')
    notice = ''
    if p['status'] == 'development':
        notice = '<div class="notice"><strong>In development.</strong> There is no published release or licence yet. Source and build instructions are on GitHub.</div>'
    elif p['status'] == 'archived':
        notice = '<div class="notice"><strong>Archived project.</strong> This page keeps a historical release available. The repository is no longer maintained.</div>'
    elif slug == 'blood-moon':
        notice = '<div class="notice"><strong>Upgrading to 2.0?</strong> Install <a href="/plugins/blockfolk/">Blockfolk 1.4.0 or newer</a> first. This release needs Paper 26.2 and Java 25. <a href="https://github.com/Cobbleworks/BloodMoon-Plugin/releases">Earlier releases</a> remain available for older servers.</div>'

    art_dir = ROOT / 'assets/art'
    hero_class = 'plugin-hero'
    if (art_dir / f'{slug}-header.webp').is_file():
        art = f'<img class="plugin-hero-art" src="/assets/art/{slug}-header.webp" alt="" style="object-position:{FOCUS.get(slug, "50%")} 40%" fetchpriority="high">'
    elif (art_dir / f'{slug}-banner.webp').is_file():
        hero_class += ' plugin-hero-banner'
        art = (f'<img class="plugin-hero-art plugin-hero-backdrop" src="/assets/art/{slug}-backdrop.webp" alt="">'
               f'<img class="hero-keyart" src="/assets/art/{slug}-banner.webp" width="790" height="168" alt="" fetchpriority="high">')
    else:
        art = f'<div class="plugin-hero-art plugin-hero-pattern" aria-hidden="true"></div><img class="hero-keyicon" src="/assets/icons/{slug}.svg" width="208" height="208" alt="">'
    hero_chips = [p['platform'], f'Minecraft {p["target"]}', f'Java {p["java"]}+' if p['status'] != 'archived' else '', p['license'] or '']
    hero = f'''<section class="{hero_class}">{art}<div class="plugin-hero-shade" aria-hidden="true"></div><div class="shell plugin-hero-inner">
<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/plugins/">Plugins</a><span aria-hidden="true">/</span><span aria-current="page">{e(p['name'])}</span></nav>
<div class="plugin-title">{icon(slug, 64)}<div><p class="eyebrow">{e(p['category'])}</p><h1>{e(p['name'])}</h1></div></div>
<p class="plugin-headline">{e(p['headline'])}</p><p class="plugin-lead">{e(p['description'])}</p>{chips(hero_chips)}
<div class="actions">{actions}</div>{notice}</div></section>'''

    tabs = [('overview', 'Overview'), ('features', 'Features'), ('installation', 'Installation')]
    tabs += [(k, l) for k, l in [('commands', 'Commands'), ('permissions', 'Permissions'), ('configuration', 'Configuration')] if p[k]]
    if r:
        tabs.append(('release', 'Release notes'))
    tab_nav = '<nav class="tabs" aria-label="On this page"><div class="shell tabs-inner">' + ''.join(f'<a href="#{k}">{l}</a>' for k, l in tabs) + '</div></nav>'

    highlights = ''.join(f'<li>{glyph("check")}<span>{e(f["title"])}</span></li>' for f in p['features'][:4])
    gallery = ''
    if p['screenshots']:
        gallery = '<div class="gallery">' + ''.join(f'<figure><a href="{s["full"]}"><img src="{s["src"]}" width="720" height="405" alt="{e(s["caption"])}" loading="lazy"></a><figcaption>{e(s["caption"])}</figcaption></figure>' for s in p['screenshots']) + '</div>'
    overview = f'''<section class="doc-section" id="overview"><div class="overview"><div><h2>What it does</h2><p class="body-lead">{e(p['notes'])}</p><ul class="checklist">{highlights}</ul></div>{facts_card(p)}</div>{gallery}</section>'''

    detailed = all(f['copy'] for f in p['features'])
    if detailed:
        items = ''.join(f'<li><h3>{e(f["title"])}</h3><p>{e(f["copy"])}</p></li>' for f in p['features'])
        features = f'<section class="doc-section" id="features"><h2>Features</h2><ul class="feature-grid">{items}</ul></section>'
    else:
        items = ''.join(f'<li>{glyph("check")}<span>{e(f["title"])}{": " + e(f["copy"]) if f["copy"] else ""}</span></li>' for f in p['features'])
        features = f'<section class="doc-section" id="features"><h2>Features</h2><ul class="checklist checklist-columns">{items}</ul></section>'

    if r:
        dep = 'Install ' + ', '.join(f'<a href="{e(d["url"])}">{e(d["name"])}</a>' for d in p['required']) + ' first.' if p['required'] else 'No other plugins are required.'
        steps = [
            ('Check your server', f'Run {e(p["platform"])} with Java {p["java"]} or newer, built for Minecraft {e(p["target"])}. {dep}' if p['status'] != 'archived' else f'Use a server with Citizens installed. {dep}'),
            ('Add the JAR', f'Stop the server, download <a href="{asset(p)}">{e(r["asset"]["name"])}</a>, and place it in <code>plugins/</code>. When upgrading, replace the previous JAR.'),
            ('Start and configure', f'Start the server and check the console. Review the generated configuration with the <a href="{docs}">release documentation</a>.'),
        ]
    else:
        steps = [
            ('Get the source', f'Clone <a href="{repository(p)}">{e(p["repository"])}</a> from GitHub.'),
            ('Build the JAR', f'Follow the <a href="{docs}">build instructions</a> with Java 25 and Maven 3.9 or newer.'),
            ('Install', 'Place the built JAR in the <code>plugins/</code> directory of a Paper 26.2 server and start it.'),
        ]
    step_html = ''.join(f'<li><span class="step-number">{i}</span><h3>{t}</h3><p>{c}</p></li>' for i, (t, c) in enumerate(steps, 1))
    first = ''
    if p['first_command']:
        first = f'<div class="command"><div class="command-label">First command</div><div class="command-line"><code>{e(p["first_command"])}</code><button type="button" class="copy-button" data-copy="{e(p["first_command"])}" aria-label="Copy command" hidden>{glyph("copy")}<span>Copy</span></button></div><p>{e(p["first_copy"])}</p></div>'
    installation = f'<section class="doc-section" id="installation"><h2>Installation</h2><ol class="steps">{step_html}</ol>{first}</section>'

    reference = reference_section(p, 'commands', 'Commands', 'commands') + reference_section(p, 'permissions', 'Permissions', 'permissions') + reference_section(p, 'configuration', 'Configuration', 'settings')

    release = ''
    if r:
        release = f'''<section class="doc-section" id="release"><h2>Release notes</h2><div class="release-card">{icon(slug, 48)}<div><p class="release-title">{e(p['name'])} <span class="version">{e(version(p))}</span></p><p class="muted"><time datetime="{r['published']}">Published {date(r['published'])}</time></p><p>{e(r['summary'])}</p>
<div class="link-row">{text_link(r['url'], 'Full release notes', 'external')}{text_link(repository(p) + '/releases', 'Earlier releases', 'external')}</div></div></div></section>'''

    related_pool = [q for q in RELEASED if q['slug'] != slug]
    related = sorted(related_pool, key=lambda q: (-len(set(q['categories']) & set(p['categories'])), q['name']))[:3]
    related_html = f'<section class="related"><div class="shell">{section_head("More from Cobbleworks", "", "/plugins/", "All plugins")}<div class="card-grid card-grid-3">{"".join(card(q) for q in related)}</div></div></section>'

    support_title = 'Historical reference' if p['status'] == 'archived' else 'Questions or an issue?'
    support_copy = 'The archived repository and its version-specific documentation remain available.' if p['status'] == 'archived' else 'Bug reports, questions, and contributions go to this plugin\u2019s GitHub repository.'
    support_btn = button(repository(p), 'View archived repository', 'secondary', 'github') if p['status'] == 'archived' else button(repository(p) + '/issues', 'Open an issue', 'secondary', 'github')
    support = f'<div class="support"><div><h2>{support_title}</h2><p>{support_copy}</p></div>{support_btn}</div>'

    content = f'{hero}{tab_nav}<div class="shell doc">{overview}{features}{installation}{reference}{release}{support}</div>{related_html}'
    schema = {'@type': 'SoftwareApplication', 'name': p['name'], 'applicationCategory': 'GameApplication', 'operatingSystem': 'Minecraft ' + p['platform'], 'url': BASE + product_link(p), 'description': p['description'], 'sameAs': repository(p)}
    if r:
        schema.update(softwareVersion=r['tag'], downloadUrl=asset(p), datePublished=r['published'])
    if p['license']:
        schema['license'] = repository(p) + '/blob/' + (r['tag'] if r else 'main') + '/LICENSE'
    write_page(product_link(p), p['name'], p['description'], content, 'plugins', schema)


# ---------------------------------------------------------------- supporting pages

def plugin_cell(p):
    return f'<th scope="row"><a class="table-plugin" href="{product_link(p)}">{icon(p["slug"], 32)}<span>{e(p["name"])}</span></a></th>'


def downloads():
    rows = ''
    for p in sorted(RELEASED, key=lambda p: p['name']):
        r = p['release']
        dep = ', '.join(d['name'] for d in p['required']) or '—'
        rows += (f'<tr>{plugin_cell(p)}<td data-label="Release"><a href="{r["url"]}">{e(version(p))}</a></td><td data-label="Released"><time datetime="{r["published"]}">{date(r["published"])}</time></td>'
                 f'<td data-label="Platform">{e(p["platform"])}</td><td data-label="Minecraft">{e(p["target"])}</td><td data-label="Java">{p["java"]}+</td><td data-label="Requires">{e(dep)}</td>'
                 f'<td class="cell-action"><a class="download-button" href="{asset(p)}" aria-label="Download {e(p["name"])} {e(version(p))}">{glyph("download")}<span>JAR</span></a></td></tr>')
    head = ''.join(f'<th scope="col">{x}</th>' for x in ['Plugin', 'Release', 'Released', 'Platform', 'Minecraft', 'Java', 'Requires', '<span class="visually-hidden">Download</span>'])
    content = page_head('Downloads', 'Downloads', 'The latest stable release of every plugin. Each plugin installs on its own: check the requirements, then download the JAR.', text_link('/compatibility/', 'Check compatibility'))
    content += f'''<section class="shell page-body"><div class="table-wrap table-cards"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p class="note">Minecraft versions are the build targets of each release, not a list of every tested version. See <a href="/compatibility/">compatibility</a> for documented ranges.</p>
<div class="aside-grid"><div class="aside-box">{icon('superwarp', 40)}<div><h2>Superwarp</h2><p>In development. Source and build instructions are available; there is no release JAR yet.</p>{text_link('/plugins/superwarp/', 'View project')}</div></div>
<div class="aside-box">{icon('npc-pickup', 40)}<div><h2>NPC PickUp</h2><p>Archived Citizens extension with one historical release.</p>{text_link('/plugins/npc-pickup/', 'View project')}</div></div></div></section>'''
    write_page('/downloads/', 'Downloads', 'Download current Cobbleworks plugin JARs with exact versions, Java requirements, Minecraft build targets, and dependencies.', content, 'downloads')


def compatibility():
    targets = sorted({p['target'] for p in RELEASED}, key=lambda v: [int(x) for x in v.split('.')], reverse=True)
    options = ''.join(f'<option value="{x}">{x}</option>' for x in targets)
    tick = f'<span class="tick" title="Supported">{glyph("check")}<span class="visually-hidden">Supported</span></span>'
    no = f'<span class="no" title="Not supported">{glyph("dash")}<span class="visually-hidden">Not supported</span></span>'
    rows = ''
    for p in sorted(RELEASED, key=lambda p: p['name']):
        dep = ', '.join(d['name'] for d in p['required']) or '—'
        rows += (f'<tr data-compat-row data-platform="{platforms(p)}" data-java="{p["java"]}" data-target="{p["target"]}">{plugin_cell(p)}'
                 f'<td data-label="Paper" class="cell-center">{tick}</td><td data-label="Spigot" class="cell-center">{tick if "Spigot" in p["platform"] else no}</td>'
                 f'<td data-label="Build target">{e(p["target"])}</td><td data-label="Documented range">{e(p["documented_range"])}</td><td data-label="Java">{p["java"]}+</td><td data-label="Requires">{e(dep)}</td></tr>')
    head = ''.join(f'<th scope="col"{" class=cell-center" if x in ("Paper", "Spigot") else ""}>{x}</th>' for x in ['Plugin', 'Paper', 'Spigot', 'Build target', 'Documented range', 'Java', 'Requires'])
    content = page_head('Compatibility', 'Compatibility', 'Find out which plugins fit your server. Platform, Java, and Minecraft requirements are taken from each release and its tagged README.')
    content += f'''<section class="shell page-body"><form class="toolbar compact" data-compat-form hidden>
<label class="select"><span>Server platform</span><select data-compat-platform><option value="all">Any</option><option value="paper">Paper</option><option value="spigot">Spigot</option></select></label>
<label class="select"><span>Java installed</span><select data-compat-java><option value="all">Any</option><option value="17">Java 17</option><option value="21">Java 21</option><option value="25">Java 25</option></select></label>
<label class="select"><span>Build target</span><select data-compat-target><option value="all">Any</option>{options}</select></label><span class="count" aria-live="polite" data-compat-count></span></form>
<div class="table-wrap table-cards"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>
<p data-compat-empty hidden class="empty-state">No releases match these requirements. Try a different platform, Java version, or build target.</p>
<div class="prose notes"><h2>Reading this table</h2><p><strong>Build target</strong> is the Minecraft API version the published JAR was built against. <strong>Documented range</strong> is the support range stated in the README for that release. A wider range does not mean every combination has been tested.</p>
<p>The Java filter shows plugins whose minimum Java version is at or below the version you select. Your server software and its dependencies have their own requirements.</p>
<p><strong>Power Mining:</strong> the v1.1.0 release notes name Paper, while the tagged README also lists Spigot. The table follows the narrower release notes; read <a href="https://github.com/Cobbleworks/Power-Mining-Plugin/releases/tag/v1.1.0">the release</a> before using another platform.</p>
<p class="muted">Release metadata checked on {date(CATALOGUE['verified'] + 'T00:00:00')}.</p></div></section>'''
    write_page('/compatibility/', 'Compatibility', 'Compare Cobbleworks plugin platforms, Minecraft and Java requirements, documented support ranges, and dependencies.', content, 'compatibility')


def docs():
    guides = ''.join(f'<a href="{product_link(p)}#installation">{icon(p["slug"], 28)}<span>{e(p["name"])}</span>{glyph("arrow")}</a>' for p in sorted(PLUGINS, key=lambda p: p['name']))
    content = page_head('Documentation', 'Install a Cobbleworks plugin', 'Find the right release, install its dependencies, and follow the guide for your plugin.')
    content += f'''<div class="shell page-body docs-layout"><div class="prose">
<h2>Installation</h2><ol class="steps steps-vertical">
<li><span class="step-number">1</span><h3>Choose and check</h3><p>Open the plugin page and check the platform, Java version, Minecraft build target, and dependencies of the release. <a href="/compatibility/">Compare requirements</a> across the collection.</p></li>
<li><span class="step-number">2</span><h3>Download the JAR</h3><p>Use <a href="/downloads/">Downloads</a> or the plugin's release page. Download the named <code>.jar</code> asset, not the automatically generated source archive.</p></li>
<li><span class="step-number">3</span><h3>Install with the server stopped</h3><p>Install any required plugins, place the JAR in <code>plugins/</code>, and replace the previous JAR when upgrading. Start the server and check the console.</p></li>
<li><span class="step-number">4</span><h3>Configure and try it</h3><p>Review the generated configuration and permission nodes in the plugin guide, then run its first command.</p></li></ol>
<h2>Upgrading</h2><p>Read the release notes before replacing a JAR. Requirements can change between releases. Back up your server and test changes to worlds, inventories, and player data on a copy first.</p>
<div class="notice"><strong>Blood Moon 2.0</strong> uses <a href="/plugins/blockfolk/">Blockfolk 1.4.0+</a> and needs Paper 26.2 with Java 25. The earlier Citizens and Sentinel setup belongs to historical releases.</div>
<h2>Getting help</h2><p>Open an issue in the plugin's GitHub repository. Include the plugin version, server version, Java version, relevant console output, and the steps that reproduce the problem.</p></div>
<aside class="side-index"><h2>Plugin guides</h2>{guides}</aside></div>'''
    write_page('/docs/', 'Documentation', 'Install and configure Cobbleworks plugins. Find release-specific commands, permissions, dependencies, and individual plugin guides.', content, 'docs')


def changelog():
    entries = ''
    for p in sorted(RELEASED, key=lambda p: p['release']['published'], reverse=True):
        r = p['release']
        entries += f'''<li class="timeline-entry"><time datetime="{r['published']}">{date(r['published'])}</time><div class="timeline-card">{icon(p['slug'], 44)}<div><h2><a href="{product_link(p)}">{e(p['name'])}</a><span class="version">{e(r['tag'])}</span></h2><p>{e(r['summary'])}</p>{text_link(r['url'], 'Read the full release notes', 'external')}</div></div></li>'''
    content = page_head('Changelog', 'Release notes', 'The latest stable release of each plugin, newest first. Each project keeps its full version history on GitHub.')
    content += f'<section class="shell page-body"><ol class="timeline">{entries}</ol></section>'
    write_page('/changelog/', 'Release notes', 'Read the latest stable Cobbleworks plugin release summaries and follow each project’s version history on GitHub.', content, 'changelog')


def about():
    content = page_head('About', 'About Cobbleworks', 'Independent Minecraft server plugins with their code, releases, and discussions in the open.')
    content += f'''<div class="shell page-body about-layout"><div class="prose">
<h2>One project, one purpose</h2><p>Cobbleworks brings together plugins for gameplay, world management, automation, transport, and server administration. Each plugin has its own repository, requirements, documentation, and release history, so you install only the projects your server needs.</p>
<h2>Licensing</h2><p>All {len(RELEASED)} released plugins use the MIT licence. Licence links on their pages point to the file in the tagged release. The archived NPC PickUp project keeps its historical MIT licence. Superwarp has no licence or release yet.</p>
<h2>Contributing</h2><p>Report bugs and propose changes in the repository of the plugin concerned. Read the contribution and security guides before contributing or reporting a security issue.</p>
<div class="actions">{button(ORG, 'Explore the organisation', 'primary', 'github')}{button(ORG + '/.github/blob/main/CONTRIBUTING.md', 'Contribution guide', 'secondary', 'book')}</div></div>
<aside class="facts-card"><h2>At a glance</h2><dl><div><dt>Released plugins</dt><dd>{len(RELEASED)}</dd></div><div><dt>In development</dt><dd>{sum(p['status'] == 'development' for p in PLUGINS)}</dd></div><div><dt>Archived</dt><dd>{sum(p['status'] == 'archived' for p in PLUGINS)}</dd></div><div><dt>Licence</dt><dd>MIT</dd></div></dl>{text_link('/plugins/', 'Browse the collection')}</aside></div>'''
    write_page('/about/', 'About', 'Learn about Cobbleworks: independent Minecraft plugins, licensing, contributing, and support.', content)


def main():
    build_icons(ROOT / 'assets/icons')
    homepage()
    directory()
    for p in PLUGINS:
        plugin_page(p)
    downloads()
    compatibility()
    docs()
    changelog()
    about()
    write_page('/404.html', 'Page not found', 'The requested Cobbleworks page could not be found.',
               page_head('404', 'Page not found', 'This page does not exist. Head back to the collection to find your plugin.', f'<div class="actions">{button("/plugins/", "Browse plugins", "primary", "", "arrow")}{button("/", "Home")}</div>'), noindex=True)
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{BASE + route}</loc></url>\n' for route in PAGES) + '</urlset>\n'
    (ROOT / 'sitemap.xml').write_text(sitemap, encoding='utf-8')
    print(f'Built {len(PAGES)} indexable pages, a 404 page, and {len(PLUGINS)} plugin icons.')


if __name__ == '__main__':
    main()
