"""Build the Cobbleworks static website using Python's standard library."""
from datetime import datetime
from html import escape
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://cobbleworks.github.io'
CATALOGUE = json.loads((ROOT / 'content/plugins.json').read_text(encoding='utf-8'))
PLUGINS = CATALOGUE['plugins']
RELEASED = [p for p in PLUGINS if p['status'] == 'released']
BY_SLUG = {p['slug']: p for p in PLUGINS}
PAGES = []

def e(value):
    return escape(str(value), quote=True)

def date(value):
    return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime('%d %b %Y').lstrip('0')

def icon(name, size=40):
    return f'<img class="product-icon" src="/assets/icons/{e(name)}.svg" width="{size}" height="{size}" alt="">'

ARROW = '<svg class="arrow" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>'
GITHUB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 .7a11.5 11.5 0 0 0-3.64 22.4c.58.1.79-.25.79-.56v-2.23c-3.23.7-3.91-1.37-3.91-1.37-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.71.08-.71 1.17.08 1.78 1.2 1.78 1.2 1.04 1.78 2.72 1.27 3.38.97.11-.75.41-1.27.74-1.56-2.58-.29-5.29-1.29-5.29-5.68 0-1.26.45-2.28 1.19-3.09-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.16 1.18a10.9 10.9 0 0 1 5.76 0c2.2-1.49 3.16-1.18 3.16-1.18.63 1.58.23 2.76.11 3.05.74.81 1.19 1.83 1.19 3.09 0 4.4-2.72 5.38-5.3 5.67.42.36.79 1.06.79 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .7Z"/></svg>'

def button(href, label, primary=False, arrow=False):
    return f'<a class="button {"button-primary" if primary else "button-secondary"}" href="{e(href)}">{e(label)}{ARROW if arrow else ""}</a>'

def header(active):
    links = [('plugins', 'Plugins'), ('docs', 'Docs'), ('downloads', 'Downloads'), ('changelog', 'Changelog')]
    nav = ''.join(f'<a href="/{key}/" {"aria-current=\"page\"" if active == key else ""}>{label}</a>' for key,label in links)
    return f'''<a class="skip-link" href="#main-content">Skip to content</a>
<header class="site-header"><div class="shell header-inner">
<a class="brand" href="/" aria-label="Cobbleworks home"><img src="/assets/brand-mark.svg" width="34" height="34" alt=""><span>Cobbleworks</span></a>
<button class="menu-button" type="button" aria-label="Open navigation" aria-expanded="false" aria-controls="site-navigation" hidden data-menu-button><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg></button>
<nav class="site-nav" id="site-navigation" aria-label="Primary navigation" data-navigation>{nav}<a class="nav-github" href="https://github.com/Cobbleworks">{GITHUB}<span>GitHub</span></a></nav>
</div></header>'''

def footer():
    return '''<footer class="site-footer"><div class="shell footer-main"><div><a class="brand" href="/"><img src="/assets/brand-mark.svg" width="28" height="28" alt=""><span>Cobbleworks</span></a><p>Independent plugins for Minecraft servers.<br>Built in the open, one project at a time.</p></div><nav aria-label="Footer navigation"><a href="/about/">About</a><a href="/compatibility/">Compatibility</a><a href="https://github.com/Cobbleworks/.github/blob/main/CONTRIBUTING.md">Contributing</a><a href="https://github.com/Cobbleworks/.github/blob/main/SECURITY.md">Security</a><a href="https://github.com/Cobbleworks">GitHub</a></nav></div><div class="shell footer-bottom"><span>Made for the worlds you build.</span><span>Not an official Minecraft product. Not affiliated with Mojang or Microsoft.</span></div></footer>'''

def write_page(route, title, description, content, active='', schema=None, hero=False, noindex=False):
    full_title = 'Cobbleworks — Open-source Minecraft plugins' if route == '/' else f'{title} | Cobbleworks'
    graph = [{'@context':'https://schema.org','@type':'WebPage','name':full_title,'url':BASE+route,'description':description}]
    if schema: graph.append({'@context':'https://schema.org',**schema})
    preload = '<link rel="preload" as="image" type="image/avif" href="/assets/hero/evening-fortress-1600.avif" imagesrcset="/assets/hero/evening-fortress-640.avif 640w, /assets/hero/evening-fortress-960.avif 960w, /assets/hero/evening-fortress-1600.avif 1600w" imagesizes="100vw" fetchpriority="high">' if hero else ''
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(full_title)}</title><meta name="description" content="{e(description)}"><meta name="theme-color" content="#080d12"><meta name="color-scheme" content="dark"><meta name="robots" content="{'noindex' if noindex else 'index, follow, max-image-preview:large'}">
<link rel="canonical" href="{BASE+route}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="manifest" href="/site.webmanifest"><link rel="preload" href="/assets/fonts/inter-0.woff2" as="font" type="font/woff2" crossorigin><link rel="preload" href="/assets/fonts/space-grotesk-0.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="/styles.css">{preload}
<meta property="og:type" content="website"><meta property="og:site_name" content="Cobbleworks"><meta property="og:title" content="{e(full_title)}"><meta property="og:description" content="{e(description)}"><meta property="og:url" content="{BASE+route}"><meta property="og:image" content="{BASE}/assets/social-preview.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="A lantern-lit Minecraft fortress overlooking a mountain valley at sunset"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{BASE}/assets/social-preview.jpg">
<script type="application/ld+json">{json.dumps(graph,ensure_ascii=False).replace('<','\\u003c')}</script><script src="/script.js" defer></script></head><body>{header(active)}<main id="main-content" tabindex="-1">{content}</main>{footer()}</body></html>'''
    output = ROOT / ('index.html' if route == '/' else '404.html' if route == '/404.html' else route.strip('/')+'/index.html')
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(html+'\n',encoding='utf-8')
    if not noindex: PAGES.append(route)

def intro(eyebrow, title, copy, extra=''):
    return f'<section class="page-intro shell"><p class="eyebrow">{e(eyebrow)}</p><h1>{e(title)}</h1><p class="page-lead">{e(copy)}</p>{extra}</section>'

def product_link(p): return '/plugins/'+p['slug']+'/'
def repository(p): return 'https://github.com/Cobbleworks/'+p['repository']
def version(p): return p['release']['tag'] if p['release'] else 'In development'
def asset(p): return p['release']['asset']['browser_download_url']

def badges(p):
    return f'<div class="badges"><span>{e(p["platform"])}</span><span>Java {p["java"]}+</span><span>{e(version(p)) if p["status"] != "archived" else "Archived"}</span></div>'

def card(p, featured=False):
    image = f'<img class="card-screenshot" src="{p["screenshots"][0]["src"]}" width="720" height="405" alt="{e(p["screenshots"][0]["caption"])}" loading="lazy">' if featured and p['screenshots'] else ''
    label = 'No published release' if p['status']=='development' else 'Archived' if p['status']=='archived' else p['category']
    return f'''<article class="plugin-card {"featured-card" if featured else ""}" data-plugin data-category="{e(' '.join(p['categories']))}" data-platform="{e('spigot paper' if 'Spigot' in p['platform'] else 'paper')}" data-status="{p['status']}">
<a class="card-link" href="{product_link(p)}">{image}<div class="card-body"><div class="card-title">{icon(p['slug'])}<div><p class="card-category">{e(label)}</p><h3>{e(p['name'])}</h3></div></div><p class="card-description">{e(p['description'])}</p>{badges(p)}<span class="card-more">Explore plugin {ARROW}</span></div></a></article>'''

def section_heading(title, copy='', link='', label=''):
    return f'<div class="section-heading"><div><h2>{e(title)}</h2>{"<p>"+e(copy)+"</p>" if copy else ""}</div>{f"<a class=\"text-link\" href=\"{e(link)}\">{e(label)} {ARROW}</a>" if link else ""}</div>'

def recent_releases():
    recent=sorted(RELEASED,key=lambda p:p['release']['published'],reverse=True)[:4]
    return '<div class="release-grid">'+''.join(f'<a class="release-card" href="{p["release"]["url"]}">{icon(p["slug"],36)}<div><h3>{e(p["name"])}</h3><span class="release-version">{e(version(p))}</span><time datetime="{p["release"]["published"]}">{date(p["release"]["published"])}</time></div>{ARROW}</a>' for p in recent)+'</div>'

def hero_art():
    return '<picture class="hero-picture"><source type="image/avif" srcset="/assets/hero/evening-fortress-640.avif 640w, /assets/hero/evening-fortress-960.avif 960w, /assets/hero/evening-fortress-1600.avif 1600w" sizes="100vw"><img class="hero-image" src="/assets/hero/evening-fortress-1600.webp" srcset="/assets/hero/evening-fortress-640.webp 640w, /assets/hero/evening-fortress-960.webp 960w, /assets/hero/evening-fortress-1600.webp 1600w" sizes="100vw" width="1672" height="941" alt="A lantern-lit Minecraft fortress overlooking a mountain valley at sunset" fetchpriority="high"></picture>'

def homepage():
    featured=[BY_SLUG[s] for s in ['map-revealer','blockfolk','wireless-redstone','area-rewind']]
    content=f'''<section class="hero"><img class="hero-image" src="/assets/hero/evening-fortress-1600.webp" srcset="/assets/hero/evening-fortress-640.webp 640w, /assets/hero/evening-fortress-960.webp 960w, /assets/hero/evening-fortress-1600.webp 1600w" sizes="100vw" width="1672" height="941" alt="A lantern-lit Minecraft fortress overlooking a mountain valley at sunset" fetchpriority="high"><div class="hero-shade" aria-hidden="true"></div><div class="hero-content shell"><p class="eyebrow">Open-source Minecraft plugins</p><h1>Tools for<br>Minecraft servers.<br><span>Built in the open.</span></h1><p class="hero-copy">Gameplay, world tools, and automation.<br>Independent projects for the worlds you build.</p><div class="actions">{button('/plugins/','Browse plugins',True,True)}{button('https://github.com/Cobbleworks','View on GitHub')}</div></div></section>
<div class="principles"><div class="shell principles-inner"><div><strong>13 released plugins</strong><span>Choose the tools your server needs.</span></div><div><strong>Independent projects</strong><span>Separate releases and documentation.</span></div><div><strong>Code in the open</strong><span>Explore, report issues, and contribute.</span></div></div></div>
<section class="section shell" id="plugins">{section_heading('From the workshop','A few projects to get you started.','/plugins/','Explore all plugins')}<div class="featured-grid">{''.join(card(p,True) for p in featured)}</div></section>
<section class="section section-compact shell">{section_heading('Fresh from GitHub','Latest stable releases across the collection.','/changelog/','All release notes')}{recent_releases()}</section>
<section class="start-callout shell" id="getting-started"><div><p class="eyebrow">Your server, your setup</p><h2>A few checks.<br>Then you’re ready.</h2><p>Choose a plugin, check its server and Java requirements, and follow its installation guide. Each project has its own setup.</p></div>{button('/docs/','Read the installation guide',False,True)}</section>
<div class="shell about-anchor" id="about"><a class="text-link" href="/about/">Meet Cobbleworks {ARROW}</a></div>'''
    content=re.sub(r'<img class="hero-image"[^>]+>',hero_art(),content,count=1)
    write_page('/','Cobbleworks','Independent Minecraft plugins for gameplay, world tools, automation, NPCs, and transport. Explore releases, requirements, and documentation.',content,schema={'@type':'Organization','name':'Cobbleworks','url':BASE,'logo':BASE+'/assets/brand-mark.svg','sameAs':['https://github.com/Cobbleworks']},hero=True)

def directory():
    content=intro('The collection','Find your next server tool.','Thirteen released plugins, a project in development, and a historical archive. Each has its own features, requirements, and documentation.')
    content+='''<section class="shell directory-section"><form class="plugin-toolbar" role="search" data-filter-form hidden><div class="toolbar-top"><label class="search-control"><span>Search plugins</span><input type="search" name="q" placeholder="Try maps, mining, or redstone" autocomplete="off" data-plugin-search></label><label class="select-control"><span>Platform</span><select name="platform" data-platform-filter><option value="all">All platforms</option><option value="paper">Paper</option><option value="spigot">Spigot</option></select></label><label class="select-control"><span>Project status</span><select name="status" data-status-filter><option value="current">Current projects</option><option value="released">Released</option><option value="development">In development</option><option value="archived">Archived</option><option value="all">All projects</option></select></label></div><div class="filter-row"><div class="filter-buttons" role="group" aria-label="Plugin category">'''
    for key,label in [('all','All'),('world','World tools'),('automation','Automation'),('npc','NPCs'),('gameplay','Gameplay'),('admin','Management')]:
        content+=f'<button type="button" data-filter="{key}" aria-pressed="{str(key=="all").lower()}">{label}</button>'
    content+='''</div><span class="plugin-count" aria-live="polite" data-plugin-count>15 projects</span></div></form><div class="plugin-grid">'''+''.join(card(p) for p in PLUGINS)+'''</div><div class="empty-state" data-empty-state hidden><h2>No plugins match these filters.</h2><p>Try another search or show the whole collection.</p><button class="button button-secondary" type="button" data-reset-filters>Reset filters</button></div><noscript><p class="note">All projects are shown. Search and filtering are available when JavaScript is enabled.</p></noscript></section>'''
    write_page('/plugins/','Plugins','Browse every Cobbleworks Minecraft plugin by purpose, platform, and project status.',content,'plugins',{'@type':'ItemList','numberOfItems':len(PLUGINS),'itemListElement':[{'@type':'ListItem','position':i+1,'name':p['name'],'url':BASE+product_link(p)} for i,p in enumerate(PLUGINS)]})

def requirements(p):
    required=', '.join(f'<a href="{e(d["url"])}">{e(d["name"])}</a>' for d in p['required']) or 'None'
    rows=[('Release',e(version(p))),('Server',e(p['platform'])),('Minecraft build target',e(p['target'])),('Java',f'{p["java"]}+' if p['status']!='archived' else 'Server / Citizens requirement'),('Required plugins',required),('Licence',e(p['license'] or 'Not specified'))]
    return '<aside class="requirements"><h2>At a glance</h2><dl>'+''.join(f'<div><dt>{label}</dt><dd>{value}</dd></div>' for label,value in rows)+'</dl><p>Requirements refer to this release. See <a href="/compatibility/">compatibility details</a> for documented ranges.</p></aside>'

def render_tables(tables):
    output=''
    for table in tables:
        output+='<div class="table-scroll" tabindex="0" role="region" aria-label="Reference table"><table><thead><tr>'+''.join(f'<th scope="col">{e(h)}</th>' for h in table['headers'])+'</tr></thead><tbody>'
        for row in table['rows']:
            output+='<tr>'+''.join(f'<td>{"<code>"+e(cell)+"</code>" if i==0 else e(cell)}</td>' for i,cell in enumerate(row))+'</tr>'
        output+='</tbody></table></div>'
    return output

def plugin_page(p):
    release=p['release']
    docs='https://cobbleworks.github.io/Blockfolk-NPC-Plugin/' if p['slug']=='blockfolk' else p['docs']
    actions=button(asset(p),('Historical JAR '+version(p)) if p['status']=='archived' else 'Download '+version(p),True,True) if release else button(repository(p),'View source on GitHub',True,True)
    actions+=button(docs,'Documentation')
    notices=''
    if p['status']=='development': notices='<div class="notice"><strong>In development · no published release</strong><p>Source and build instructions are available on GitHub. There is no downloadable release JAR or specified licence.</p></div>'
    elif p['status']=='archived': notices='<div class="notice"><strong>Archived project</strong><p>This page preserves a historical release. The repository is no longer maintained; use the release-specific documentation for its original setup.</p></div>'
    elif p['slug']=='blood-moon': notices='<div class="notice"><strong>Upgrading to 2.0?</strong><p>Install <a href="/plugins/blockfolk/">Blockfolk 1.4.0 or newer</a> first. This release requires Paper 26.2 and Java 25. <a href="https://github.com/Cobbleworks/BloodMoon-Plugin/releases">Earlier releases</a> remain available for older servers.</p></div>'
    title_block=f'''<section class="product-intro shell"><nav class="breadcrumbs" aria-label="Breadcrumb"><a href="/plugins/">Plugins</a><span aria-hidden="true">/</span><span aria-current="page">{e(p['name'])}</span></nav><div class="product-top"><div class="product-copy"><div class="product-name">{icon(p['slug'],56)}<div><p class="eyebrow">{e(p['category'])}</p><h1>{e(p['name'])}</h1></div></div><p class="product-headline">{e(p['headline'])}</p><p class="page-lead">{e(p['description'])}</p><div class="actions">{actions}</div><a class="repository-link" href="{repository(p)}">View project on GitHub ↗</a></div>{requirements(p)}</div>{notices}</section>'''
    section_nav='<nav class="product-sections shell" aria-label="On this page">'+''.join(f'<a href="#{key}">{label}</a>' for key,label in [('overview','Overview'),('features','Features'),('installation','Installation'),('reference','Reference')])+'</nav>'
    overview=f'<section class="content-section" id="overview"><h2>What it does</h2><p>{e(p["notes"])}</p>'
    if p['screenshots']:
        overview+='<div class="screenshot-gallery">'+''.join(f'<figure><a href="{s["full"]}" aria-label="View full screenshot: {e(s["caption"])}"><img src="{s["src"]}" width="720" height="405" alt="{e(s["caption"])}" loading="lazy"></a><figcaption>{e(s["caption"])}</figcaption></figure>' for s in p['screenshots'])+'</div>'
    overview+='</section>'
    feature_items=''.join(f'<li><span class="feature-check" aria-hidden="true">✓</span><span>{e(f["title"])}{": "+e(f["copy"]) if f["copy"] else ""}</span></li>' for f in p['features'])
    features=f'<section class="content-section" id="features"><h2>Features</h2><ul class="feature-list">{feature_items}</ul></section>'
    if release:
        deptext='Install '+', '.join(e(d['name']) for d in p['required'])+' first.' if p['required'] else 'No additional plugins are required.'
        install=f'<ol class="steps"><li><strong>Check your server</strong><p>Use {e(p["platform"])} with the Java and Minecraft requirements listed above. {deptext}</p></li><li><strong>Install the release JAR</strong><p>Stop the server. Download <a href="{asset(p)}">{e(release["asset"]["name"])}</a> and put it in <code>plugins/</code>. Replace the previous JAR when upgrading.</p></li><li><strong>Start and check the console</strong><p>Start the server and confirm the plugin loads. Review any generated configuration and the <a href="{p["docs"]}">release-specific documentation</a>.</p></li></ol>'
    else:
        install=f'<p>No release JAR has been published. Follow the <a href="{p["docs"]}">source build instructions</a> using Java 25 and Maven 3.9+, then place the built JAR in your Paper 26.2 server’s <code>plugins/</code> directory.</p>'
    first=f'<div class="first-action"><span class="eyebrow">Your first step</span><div class="command-line"><code>{e(p["first_command"])}</code><button type="button" class="copy-button" data-copy="{e(p["first_command"])}" aria-label="Copy first command" hidden>Copy</button></div><p>{e(p["first_copy"])}</p></div>' if p['first_command'] else ''
    installation=f'<section class="content-section" id="installation"><h2>Installation</h2>{install}{first}</section>'
    reference=f'<section class="content-section" id="reference"><h2>Reference</h2><p>Commands and permission defaults from the <a href="{p["docs"]}">documented version</a>. Administrator actions may require operator access or a permission grant.</p>'
    for key,label in [('commands','Commands'),('permissions','Permissions'),('configuration','Configuration')]:
        if p[key]: reference+=f'<h3 id="{key}">{label}</h3>'+render_tables(p[key])
    if p['optional']: reference+='<h3>Optional integrations</h3><ul>'+''.join(f'<li>{e(x)}</li>' for x in p['optional'])+'</ul>'
    reference+=f'<p class="reference-end"><a class="text-link" href="{p["docs"]}">Full configuration and operational notes {ARROW}</a></p></section>'
    release_section=f'<section class="content-section" id="release"><h2>Release notes</h2><p class="release-meta">{e(version(p))} · <time datetime="{release["published"]}">{date(release["published"])}</time></p><p>{e(release["summary"])}</p><div class="inline-links"><a href="{release["url"]}">Read release notes ↗</a><a href="{repository(p)}/releases">Earlier releases ↗</a></div></section>' if release else ''
    support=f'<section class="content-section support-block"><h2>{"Historical reference" if p["status"]=="archived" else "Questions or an issue?"}</h2><p>{"The archived repository and its version-specific documentation remain available." if p["status"]=="archived" else "Use the project’s GitHub repository for bug reports, questions, and contributions."}</p><a class="text-link" href="{repository(p) if p["status"]=="archived" else repository(p)+"/issues"}">{"View archived repository" if p["status"]=="archived" else "Open project issues"} {ARROW}</a></section>'
    rail='<aside class="contents-rail"><span class="eyebrow">On this page</span>'+''.join(f'<a href="#{key}">{label}</a>' for key,label in [('overview','Overview'),('features','Features'),('installation','Installation'),('reference','Reference')])+('<a href="#release">Release notes</a>' if release else '')+f'<a href="/downloads/">All downloads</a></aside>'
    content=title_block+section_nav+f'<div class="shell product-layout"><div class="reading-content">{overview}{features}{installation}{reference}{release_section}{support}</div>{rail}</div>'
    schema={'@type':'SoftwareApplication','name':p['name'],'applicationCategory':'GameApplication','operatingSystem':'Minecraft '+p['platform'],'url':BASE+product_link(p),'description':p['description'],'sameAs':repository(p)}
    if release: schema.update(softwareVersion=release['tag'],downloadUrl=asset(p),datePublished=release['published'])
    if p['license']: schema['license']=repository(p)+'/blob/'+(release['tag'] if release else 'main')+'/LICENSE'
    write_page(product_link(p),p['name'],p['description'],content,'plugins',schema)

def download_rows():
    output=''
    for p in RELEASED:
        dep=', '.join(d['name'] for d in p['required']) or 'None'
        output+=f'<tr data-download-row data-platform="{"spigot paper" if "Spigot" in p["platform"] else "paper"}" data-java="{p["java"]}" data-target="{p["target"]}"><th scope="row"><a class="table-product" href="{product_link(p)}">{icon(p["slug"],32)}<span>{e(p["name"])}</span></a></th><td data-label="Version"><a href="{p["release"]["url"]}">{e(version(p))}</a><time datetime="{p["release"]["published"]}">{date(p["release"]["published"])}</time></td><td data-label="Platform">{e(p["platform"])}</td><td data-label="Minecraft target">{e(p["target"])}</td><td data-label="Java">{p["java"]}+</td><td data-label="Required plugins">{e(dep)}</td><td class="table-action" data-label="Download"><a class="download-link" href="{asset(p)}" aria-label="Download {e(p["name"])} {e(version(p))}">JAR ↓</a></td></tr>'
    return output

def downloads():
    content=intro('Ready to install','Downloads','The latest stable release of each plugin. Check its requirements, then download the named JAR. Each plugin is installed separately.',f'<a class="text-link" href="/compatibility/">Check compatibility {ARROW}</a>')
    content+='<section class="shell downloads-section"><div class="table-scroll downloads-table"><table><thead><tr>'+''.join(f'<th scope="col">{x}</th>' for x in ['Plugin','Release','Platform','Minecraft target','Java','Required plugins','Download'])+'</tr></thead><tbody>'+download_rows()+'</tbody></table></div><p class="note">Minecraft targets are the versions the releases were built against, not a list of every tested server version. <a href="/compatibility/">Read the requirement details.</a></p><div class="download-other"><h2>Looking for something else?</h2><p><a href="/plugins/superwarp/">Superwarp</a> has source and build instructions, with no published JAR. <a href="/plugins/npc-pickup/">NPC PickUp</a> is an archived project with a historical release.</p></div></section>'
    write_page('/downloads/','Downloads','Download current Cobbleworks plugin JARs with exact versions, Java requirements, Minecraft build targets, and dependencies.',content,'downloads')

def compatibility():
    options=''.join(f'<option value="{x}">{x}</option>' for x in ['26.2','1.21.10','1.21.8','1.21.4','1.21.1','1.20.4','1.20.1','1.19.4'])
    content=intro('Know your setup','Compatibility','Release requirements, documented ranges, and build targets. Additional versions are not certified by this table.')
    content+=f'<section class="shell compatibility-section"><form class="compatibility-filters" data-compat-form hidden><label class="select-control"><span>Server platform</span><select data-compat-platform><option value="all">All platforms</option><option value="paper">Paper</option><option value="spigot">Spigot</option></select></label><label class="select-control"><span>Java installed</span><select data-compat-java><option value="all">Any version</option><option value="17">Java 17</option><option value="21">Java 21</option><option value="25">Java 25</option></select></label><label class="select-control"><span>Minecraft build target</span><select data-compat-target><option value="all">All targets</option>{options}</select></label><span aria-live="polite" data-compat-count>13 plugins</span></form><div class="table-scroll compatibility-table"><table><thead><tr>'+''.join(f'<th scope="col">{x}</th>' for x in ['Plugin','Platform','Build target','Documented range','Java','Required plugins'])+'</tr></thead><tbody>'
    for p in RELEASED:
        content+=f'<tr data-compat-row data-platform="{"spigot paper" if "Spigot" in p["platform"] else "paper"}" data-java="{p["java"]}" data-target="{p["target"]}"><th scope="row"><a class="table-product" href="{product_link(p)}">{icon(p["slug"],32)}<span>{e(p["name"])}</span></a></th>'+''.join(f'<td data-label="{label}">{e(val)}</td>' for label,val in [('Platform',p['platform']),('Build target',p['target']),('Documented range',p['documented_range']),('Java',str(p['java'])+'+'),('Required plugins',', '.join(d['name'] for d in p['required']) or 'None')])+'</tr>'
    content+='</tbody></table></div><p data-compat-empty hidden class="empty-state">No releases match these requirements. Try a different platform, Java version, or build target.</p><div class="compatibility-notes"><h2>How to read this table</h2><p><strong>Build target</strong> is the Minecraft API version used for the published build. <strong>Documented range</strong> is the support range stated in its version-specific README. A broader range does not mean every combination has been tested.</p><p>Java filtering shows plugins whose declared minimum is at or below your selection. Your server and required dependencies also have their own Java requirements.</p><p><strong>Power Mining:</strong> v1.1.0 release notes specify Paper; the tagged README also lists Spigot. The platform column follows the narrower release description. Consult <a href="https://github.com/Cobbleworks/Power-Mining-Plugin/releases/tag/v1.1.0">the release notes</a> before choosing another platform.</p><p>Metadata checked on 1 October 2026. Each plugin page links to the original release and its documentation.</p></div></section>'
    write_page('/compatibility/','Compatibility','Compare Cobbleworks plugin platform, Minecraft and Java requirements, documented support ranges, and required dependencies.',content,'downloads')

def docs():
    content=intro('Get started','A good start for your server.','Find the right release, install its dependencies, and follow the guide for your plugin.')
    content+='''<div class="shell docs-layout"><section class="reading-content"><h2>Install a plugin</h2><ol class="steps"><li><strong>Choose and check</strong><p>Open the plugin page and check the release’s platform, Java version, Minecraft requirements, and dependencies. <a href="/compatibility/">Compare requirements</a> across the collection.</p></li><li><strong>Download the JAR</strong><p>Use <a href="/downloads/">Downloads</a> or the plugin’s release page. Download the named <code>.jar</code> asset rather than the automatically generated source archive.</p></li><li><strong>Install with the server stopped</strong><p>Install required dependencies, place the plugin JAR in <code>plugins/</code>, and replace the previous JAR when upgrading. Start the server and check the console for successful loading.</p></li><li><strong>Configure and try it</strong><p>Review generated files and permission nodes in the plugin guide. Run its first command and test the behaviour on your server.</p></li></ol><h2>When upgrading</h2><p>Read the new release notes before replacing a JAR. Requirements can change between releases. Keep a server backup and test changes to worlds, inventories, and player data on a copy first.</p><div class="notice"><strong>Blood Moon 2.0</strong><p>The current release uses <a href="/plugins/blockfolk/">Blockfolk 1.4.0+</a> and needs Paper 26.2 with Java 25. Its earlier Citizens/Sentinel setup belongs to historical releases.</p></div><h2>Need help?</h2><p>Use the plugin’s GitHub Issues page. Include the plugin version, server version, Java version, relevant console output, and the steps that reproduce the problem.</p></section><aside class="docs-index"><h2>Plugin guides</h2>'''+''.join(f'<a href="{product_link(p)}#installation">{icon(p["slug"],28)}<span>{e(p["name"])}</span>{ARROW}</a>' for p in PLUGINS)+'</aside></div>'
    write_page('/docs/','Documentation','Install and configure Cobbleworks plugins. Find release-specific commands, permissions, dependencies, and individual plugin guides.',content,'docs')

def changelog():
    content=intro('Project updates','Release notes','The latest stable releases across Cobbleworks. Each project has its own version history.')
    content+='<section class="shell changelog-list">'
    for p in sorted(RELEASED,key=lambda p:p['release']['published'],reverse=True):
        r=p['release']
        content+=f'<article class="changelog-entry"><time datetime="{r["published"]}">{date(r["published"])}</time><div>{icon(p["slug"],40)}<h2><a href="{product_link(p)}">{e(p["name"])}</a><span>{e(r["tag"])}</span></h2><p>{e(r["summary"])}</p><a class="text-link" href="{r["url"]}">Read full release notes {ARROW}</a></div></article>'
    content+='</section>'
    write_page('/changelog/','Release notes','Read the latest stable Cobbleworks plugin release summaries and follow each project’s version history on GitHub.',content,'changelog')

def about():
    content=intro('The organisation','Cobbleworks','Independent Minecraft server plugins, with their code, releases, and discussions in the open.')
    content=''+content+'''<div class="shell about-layout"><div class="reading-content"><section class="content-section"><h2>One project, one purpose.</h2><p>Cobbleworks brings together tools for gameplay, world management, automation, transport, and server administration. Each plugin has its own repository, requirements, documentation, and release history. Install the projects that fit your server.</p></section><section class="content-section"><h2>Licensing</h2><p>The thirteen released plugins in the current collection use the MIT licence. Licence links on their individual pages lead to the version-specific repository files. The archived NPC PickUp project also carries its historical MIT licence.</p><p>Superwarp currently has no licence file or published release. Its page links to the source and build instructions without assigning a licence.</p></section><section class="content-section"><h2>Contribute or ask a question</h2><p>Report bugs and propose changes in the relevant plugin repository. Read the organisation’s contribution and security guides when contributing or reporting a security issue.</p><div class="actions">'''+button('https://github.com/Cobbleworks','Explore the organisation',True,True)+button('https://github.com/Cobbleworks/.github/blob/main/CONTRIBUTING.md','Contribution guide')+'''</div></section></div><aside class="about-facts"><dl><div><dt>Released projects</dt><dd>13</dd></div><div><dt>In development</dt><dd>1</dd></div><div><dt>Historical archive</dt><dd>1</dd></div></dl><a class="text-link" href="/plugins/">Browse the collection '''+ARROW+'''</a></aside></div>'''
    write_page('/about/','About','Learn about Cobbleworks, independent Minecraft plugins, project licensing, contribution, and support.',content)

def build_icons():
    drawings={
      'advanced-achievements':'<path d="m16 7 8 4 8-4v11l-8 4-8-4Z"/><path class="accent" d="m24 23 3 5 6 1-4 5 1 6-6-3-6 3 1-6-4-5 6-1Z"/>',
      'area-rewind':'<path d="m24 15 10 6v12l-10 6-10-6V21Z M14 21l10 6 10-6M24 27v12"/><path class="accent" d="M37 13a18 18 0 0 0-28 7M9 9v11h11"/>',
      'blockfolk':'<path d="M17 8h14v14H17ZM14 29l10-5 10 5v12H14Z"/><path class="accent" d="M21 14v2m6-2v2M24 24v17"/>',
      'blood-moon':'<path d="M32 8H18L8 18v14l10 9h14l8-8H25L16 24l9-9h15Z"/><path class="accent" d="M32 8H18L8 18v14l10 9h14l8-8"/>',
      'custom-jukebox':'<path d="m24 8 15 8v22L24 45 9 38V16ZM9 16l15 8 15-8M24 24v21"/><path class="accent" d="m16 15 8 4 8-4m-4 17 6-3v7l-6 3Z"/>',
      'hookshot':'<path d="M10 9h15v13M25 22h12v11l-6 6h-6l-6-6v-5"/><path class="accent" d="M10 9v18m-4 0h8M19 28v5l6 6h6l6-6"/>',
      'map-revealer':'<path d="m6 12 12-5 12 5 12-5v29l-12 5-12-5-12 5ZM18 7v29m12-24v29"/><path class="accent" d="m11 26 10-7 7 8 9-8M33 13h4"/>',
      'piston-crusher':'<path d="M7 14h11v20H7Zm11 7h11v6H18Zm13-9 11 6v16l-11 6-8-5V18Z"/><path class="accent" d="m23 18 8 6 11-6M31 24v16"/>',
      'power-mining':'<path d="m13 8 19 4 9 13-7 4-7-11-17-3Z"/><path class="accent" d="m25 17-16 23 5 3 16-23"/>',
      'rail-boost':'<path d="M9 13h30l-4 17H13ZM12 30v6h24v-6M6 41h36"/><path class="accent" d="M18 36v5m12-5v5M17 13v17m14-17v17"/>',
      'super-enchantments':'<path d="m5 12 19 6 19-6v25l-19 6-19-6ZM24 18v25M10 18l9 3m-9 5 9 3"/><path class="accent" d="m34 20 2 5 5 2-5 2-2 5-2-5-5-2 5-2Z"/>',
      'useful-autocrafter':'<path d="M8 8h32v32H8ZM18 8v32m12-32v32M8 18h32M8 30h32"/><path class="accent" d="M22 22h4v4h-4Z"/>',
      'wireless-redstone':'<path d="M6 25h12v14H6Zm24 0h12v14H30Z"/><path class="accent" d="M12 25V14h24v11M20 9h8M10 30h4m20 0h4"/>',
      'superwarp':'<path d="M10 41V7h28v34M16 41V13h16v28"/><path class="accent" d="M21 26h21m-7-6 7 6-7 6"/>',
      'npc-pickup':'<path d="m8 25 16-7 16 7v14H8ZM8 25l16 7 16-7M24 32v7"/><path class="accent" d="M24 5v18m-5-5 5 5 5-5"/>',
    }
    dest=ROOT/'assets/icons';dest.mkdir(exist_ok=True)
    for name,drawing in drawings.items():
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" fill="none" stroke="#b8c8d4" stroke-width="2" stroke-linecap="square" stroke-linejoin="miter"><style>.accent{{stroke:#e8903a}}</style>{drawing}</svg>\n'
        (dest/(name+'.svg')).write_text(svg,encoding='utf-8')

def main():
    build_icons()
    homepage(); directory()
    for p in PLUGINS: plugin_page(p)
    downloads(); compatibility(); docs(); changelog(); about()
    write_page('/404.html','Page not found','The requested Cobbleworks page could not be found.',intro('Page not found','A different path.','This page does not exist. Head back to the collection to find your plugin.',button('/plugins/','Browse plugins',True,True)),noindex=True)
    sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{BASE+route}</loc></url>\n' for route in PAGES)+'</urlset>\n'
    (ROOT/'sitemap.xml').write_text(sitemap,encoding='utf-8')
    print(f'Built {len(PAGES)} indexable pages, a 404 page, and {len(PLUGINS)} matching SVG symbols.')

if __name__=='__main__': main()
