"""Check stable upstream releases without overwriting reviewed documentation."""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import json
import os
import sys

ROOT=Path(__file__).resolve().parent.parent

def main():
    products=json.loads((ROOT/'content/plugins.json').read_text(encoding='utf-8'))['plugins']
    headers={'Accept':'application/vnd.github+json','User-Agent':'Cobbleworks-Website-Release-Check','X-GitHub-Api-Version':'2022-11-28'}
    token=os.environ.get('GITHUB_TOKEN')
    if token: headers['Authorization']='Bearer '+token
    updates=[]
    for p in products:
        if p['status']=='archived': continue
        request=Request(f'https://api.github.com/repos/Cobbleworks/{p["repository"]}/releases/latest',headers=headers)
        try:
            with urlopen(request,timeout=30) as response: release=json.load(response)
        except HTTPError as error:
            if error.code==404 and p['status']=='development': continue
            raise
        current=p['release']['tag'] if p['release'] else None
        if release['tag_name']!=current: updates.append({'plugin':p['name'],'catalogue_version':current,'published_version':release['tag_name'],'url':release['html_url']})
    if updates:
        print(json.dumps(updates,indent=2))
        print('Review the new requirements, documentation and screenshots before updating content/plugins.json.',file=sys.stderr)
        return 1
    print('All released products match upstream stable versions. Development status is current.')
    return 0

if __name__=='__main__': sys.exit(main())
