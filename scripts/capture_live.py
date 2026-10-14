#!/usr/bin/env python3
"""One-shot, fail-closed HTTPS snapshot of known public Status routes.

Never overwrites site/. Capture into a NEW empty repository and pin the exact
live response bytes. A source push is not a deployment.
"""
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import quote
import argparse
import hashlib
import json
import time

HOST = "https://status.fountain.coach"
ROOT = Path(__file__).resolve().parents[1]

def remote(route):
    url=HOST+quote(route,safe='/.-_~')
    last=None
    for attempt in range(4):
        try:
            with urlopen(Request(url,headers={'Cache-Control':'no-cache','User-Agent':'FountainCoach-source-admission/1.0'}),timeout=22) as response:
                if response.status != 200:raise ValueError("non-200: "+url)
                if response.url.rstrip('/') != url.rstrip('/'):
                    raise ValueError("redirect identity drift: "+url+" => "+response.url)
                return response.read()
        except (URLError, TimeoutError, OSError) as exc:
            last=exc
            if attempt < 3:time.sleep(attempt+1)
    raise RuntimeError(f"Failed public read {url}: {last}")

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--routes',type=Path,default=ROOT/'docs/expected-public-routes.txt')
    parser.add_argument('--out',type=Path,default=ROOT/'site')
    args=parser.parse_args()
    out=args.out.resolve()
    if out.exists() and any(out.rglob('*')):
        raise SystemExit('REFUSING TO OVERWRITE a non-empty source snapshot: '+str(out))
    routes=[s.strip() for s in args.routes.read_text().splitlines() if s.strip()]
    if len(routes)!=len(set(routes)) or len(routes)<20:
        raise SystemExit('Bad or incomplete expected public route set')
    with ThreadPoolExecutor(max_workers=6) as pool:
        responses=list(pool.map(remote,routes))
    for route,content in zip(routes,responses):
        rel=route.lstrip('/') or 'index.html'
        if rel.endswith('/'):rel+='index.html'
        file=out/rel
        file.parent.mkdir(parents=True,exist_ok=True)
        file.write_bytes(content)
    checks=sorted((hashlib.sha256(content).hexdigest(),(route.lstrip('/')+'index.html' if route != '/' and route.endswith('/') else (route.lstrip('/') or 'index.html'))) for route,content in zip(routes,responses))
    inventory=''.join(digest+'  '+name+'\n' for digest,name in checks)
    (ROOT/'publication-files.sha256').write_text(inventory)
    print('LIVE_SNAPSHOT_CAPTURED',len(routes),'contentSHA256',hashlib.sha256(inventory.encode()).hexdigest())

if __name__=='__main__':main()
