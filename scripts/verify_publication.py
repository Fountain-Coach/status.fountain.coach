#!/usr/bin/env python3
"""Verify Git authoritative Status content and optional independent live HTTPS.

No mutation. Every public payload file is inventoried; an exact source commit
is not proof of a public deployment.
"""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.request import Request,urlopen
from urllib.error import URLError
from urllib.parse import quote
import argparse
import hashlib
import json
import time

ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
HOST='https://status.fountain.coach'

def sha(blob):
    return hashlib.sha256(blob).hexdigest()

def inventory():
    declared={}
    for line in (ROOT/'publication-files.sha256').read_text().splitlines():
        digest,separator,name=line.partition('  ')
        if not separator or name in declared or len(digest)!=64:
            raise ValueError('Invalid or duplicate inventory line')
        declared[name]=digest
    local={p.relative_to(SITE).as_posix():sha(p.read_bytes()) for p in SITE.rglob('*') if p.is_file()}
    if local!=declared:
        missing=sorted(set(declared)-set(local))
        extra=sorted(set(local)-set(declared))
        changed=sorted(k for k in set(local)&set(declared) if local[k]!=declared[k])
        raise ValueError(f'Inventory mismatch: missing={missing}, extra={extra}, changed={changed}')
    assert len(declared)==26,(len(declared),'Expected full current Status site')
    html=[p for p in SITE.rglob('index.html') if p.is_file()]
    assert len(html)==13,(len(html),'Expected all public Status HTML routes')
    assert (SITE/'.well-known/agent-bootstrap.json').is_file()
    assert (SITE/'for-agents/bootstrap.json').is_file()
    assert (SITE/'business-architecture.json').is_file()
    return declared

def fetch_item(item):
    name,digest=item
    route='/'+name
    if route.endswith('/index.html'):route=route[:-len('index.html')]
    if route=='/index.html':route='/'
    url=HOST+quote(route,safe='/.-_~')
    last=None
    for attempt in range(3):
        try:
            with urlopen(Request(url,headers={'Cache-Control':'no-cache','User-Agent':'FountainCoach-parity-verifier/1.0'}),timeout=20) as response:
                data=response.read()
                if response.status!=200 or response.url.rstrip('/')!=url.rstrip('/'):
                    raise ValueError(f'Readback identity/status mismatch {url}: {response.url} {response.status}')
                got=sha(data)
                return (name,got==digest,got)
        except (URLError,TimeoutError,OSError) as err:
            last=err
            if attempt<2:time.sleep(attempt+1)
    raise RuntimeError(f'No HTTPS witness for {url}: {last}')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--against-live',action='store_true')
    args=parser.parse_args()
    declared=inventory()
    print('STATUS_GIT_SOURCE_VERIFIED',len(declared),'files, 13 HTML routes')
    if args.against_live:
        with ThreadPoolExecutor(max_workers=6) as pool:
            response=list(pool.map(fetch_item,sorted(declared.items())))
        drift=[dict(file=name,expected=declared[name],actual=got) for name,matched,got in response if not matched]
        if drift:raise SystemExit('STATUS_LIVE_MISMATCH '+json.dumps(drift))
        print('STATUS_ALL_FILE_HTTPS_PARITY_VERIFIED',len(response),'files')

if __name__=='__main__':main()
