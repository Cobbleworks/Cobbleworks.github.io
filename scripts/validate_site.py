"""Validate static routes, anchors, assets, metadata and release integrity."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
BASE = 'https://cobbleworks.github.io'

class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs=[]; self.ids=[]; self.title=''; self.h1=0; self.meta={}; self.canonical=None; self.schemas=[]; self.in_title=False; self.in_schema=False; self.schema=''; self.errors=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag=='h1': self.h1+=1
        if tag=='title': self.in_title=True
        if tag=='meta': self.meta[attrs.get('name',attrs.get('property'))]=attrs.get('content')
        if tag=='link' and attrs.get('rel')=='canonical': self.canonical=attrs.get('href')
        if tag=='script' and attrs.get('type')=='application/ld+json': self.in_schema=True; self.schema=''
        if tag=='img' and 'alt' not in attrs: self.errors.append('Image lacks alternative text')
        for key in ['href','src']:
            if key in attrs: self.refs.append(attrs[key])
        if 'srcset' in attrs: self.refs.extend(item.strip().split()[0] for item in attrs['srcset'].split(','))
    def handle_endtag(self,tag):
        if tag=='title': self.in_title=False
        if tag=='script' and self.in_schema: self.schemas.append(json.loads(self.schema)); self.in_schema=False
    def handle_data(self,text):
        if self.in_title: self.title+=text
        if self.in_schema: self.schema+=text

def main():
    plugins=json.loads((ROOT/'content/plugins.json').read_text(encoding='utf-8'))['plugins']
    errors=[]; docs={}
    files=[ROOT/'index.html',ROOT/'404.html']+list((ROOT/'plugins').rglob('index.html'))+[ROOT/p/'index.html' for p in ['downloads','docs','compatibility','changelog','about']]
    for file in files:
        doc=Document(); doc.feed(file.read_text(encoding='utf-8')); docs[file.resolve()]=doc
        errors.extend(f'{file.relative_to(ROOT)}: {x}' for x in doc.errors)
        if doc.h1!=1: errors.append(f'{file}: expected one H1')
        if len(doc.ids)!=len(set(doc.ids)): errors.append(f'{file}: duplicate IDs')
        if not doc.meta.get('description') or not doc.canonical or not doc.schemas: errors.append(f'{file}: missing search metadata')
    if len(set(d.title for d in docs.values()))!=len(docs): errors.append('Duplicate page titles')
    for file,doc in docs.items():
        for ref in doc.refs:
            url=urlsplit(ref)
            if url.scheme or url.netloc: continue
            target=(ROOT/unquote(url.path.lstrip('/'))) if url.path.startswith('/') else file.parent/unquote(url.path)
            if not url.path: target=file
            if target.is_dir(): target=target/'index.html'
            if not target.is_file(): errors.append(f'{file.relative_to(ROOT)}: missing {ref}')
            elif url.fragment and target.resolve() in docs and url.fragment not in docs[target.resolve()].ids: errors.append(f'{file.relative_to(ROOT)}: missing anchor {ref}')
    for css in [ROOT/'styles.css',*list((ROOT/'assets/fonts').glob('*.css'))]:
        for path in re.findall(r'url\([\'\"]?(/[^)\'\"]+)',css.read_text(encoding='utf-8')):
            if not (ROOT/path.lstrip('/')).is_file(): errors.append(f'{css.name}: missing {path}')
    if len(plugins)!=15 or len({p['slug'] for p in plugins})!=15: errors.append('Expected 15 unique plugin identities')
    for p in plugins:
        if not (ROOT/'plugins'/p['slug']/'index.html').is_file(): errors.append(f'Missing page for {p["slug"]}')
        r=p['release']
        if r and not r['asset']['browser_download_url'].endswith('.jar'): errors.append(f'{p["slug"]}: download is not a JAR')
        if r and f'/releases/download/{r["tag"]}/' not in r['asset']['browser_download_url']: errors.append(f'{p["slug"]}: download version mismatch')
        if p['status']=='development' and r: errors.append('Development project has a false release')
    locs=[el.text for el in ET.parse(ROOT/'sitemap.xml').findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if len(locs)!=22: errors.append('Sitemap must include all 22 indexable pages')
    for loc in locs:
        if not loc.startswith(BASE): errors.append('Unexpected sitemap origin')
        target=ROOT/urlsplit(loc).path.lstrip('/')/'index.html'
        if not target.is_file(): errors.append(f'Sitemap page missing: {loc}')
    if errors: raise SystemExit('\n'.join(errors))
    print(f'Validated {len(docs)} documents, 15 plugin pages, local links/assets/anchors, metadata, sitemap and release JAR integrity.')

if __name__=='__main__': main()
