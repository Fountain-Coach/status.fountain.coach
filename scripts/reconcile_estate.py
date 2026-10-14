#!/usr/bin/env python3
"""Read-only by default: project canonical Git Status bytes into old estate.

Explicit --apply changes only the named status.fountain.coach destination.
Never triggers publication, DNS, or direct host writes. Never removes extra
destination files silently. The canonical repository alone owns editing.
"""
import argparse
import hashlib
import os
import shutil
from pathlib import Path
from verify_publication import SITE,inventory,sha

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--estate-site',required=True,type=Path,
        help='Absolute path ending estate/sites/status.fountain.coach')
    ap.add_argument('--apply',action='store_true')
    args=ap.parse_args()
    dst=args.estate_site.resolve()
    if dst.name!='status.fountain.coach' or dst.parent.name!='sites' or dst.parent.parent.name!='estate' or not dst.is_dir():
        raise ValueError('Invalid exact Status estate destination')
    expected=inventory()
    original={p.relative_to(dst).as_posix() for p in dst.rglob('*') if p.is_file()}
    unexpected=sorted(original-set(expected))
    if unexpected:raise ValueError('Unreviewed extra destination files; refusing: '+str(unexpected))
    changed=[name for name in sorted(expected) if not (dst/name).is_file() or sha((dst/name).read_bytes())!=expected[name]]
    print('CANONICAL_STATUS_SOURCE',SITE)
    print('DERIVED_ESTATE_TARGET',dst)
    print('INVENTORY',len(expected),'DIFFERENCES',len(changed),'APPLY',args.apply)
    for name in changed:print('DIFF',name)
    if args.apply:
        for name in changed:
            target=dst/name
            target.parent.mkdir(parents=True,exist_ok=True)
            temp=target.with_name(target.name+'.canonical-source-tmp')
            shutil.copyfile(SITE/name,temp)
            os.replace(temp,target)
        print('LOCAL_MATERIALIZATION_COMPLETE',len(changed),'HTTPS_RELEASE_NOT_PERFORMED')
    else:
        print('READ_ONLY_DIFF_ONLY — use --apply for explicit local materialization')

if __name__=='__main__':main()
