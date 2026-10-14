#!/usr/bin/env python3
"""Admit Company Status to required footer legals, never header estate rails.

Works against checked-in static HTML only. Read-only by default and idempotent.
Source repositories remain authoritative for their respective publication roots.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

NAV = re.compile(r'(<nav\b[^>]*\bclass="[^"]*\bestate-nav\b[^"]*"[^>]*>)(.*?)(</nav>)', re.S | re.I)
FOOTER = re.compile(r'<footer\b[^>]*>.*?</footer>', re.S | re.I)
STATUS_ANCHOR = re.compile(
    r'<a\b[^>]*\bdata-estate-id="status"[^>]*>.*?</a>', re.S | re.I
)
STATUS_URL = "https://status.fountain.coach/"
PUB_LINK = re.compile(
    r'\s*·\s*<a\b[^>]*href="https://status\.fountain\.coach/"[^>]*>.*?</a>',
    re.S | re.I
)
LEGAL_ANCHOR = (
    '<a href="https://status.fountain.coach/" data-legal-role="company-status"'
    '{current} aria-label="Company status and transparency">'
    'Company status &amp; transparency</a>'
)
POLICY_REF = 'href="https://governance.fountain.coach/legal/"'
LEGAL_RE = re.compile(r'<p\b[^>]*class="[^"]*\bfooter-footnote\b[^"]*"[^>]*>.*?</p>', re.S)
# The same URL may still appear inside an article discussing the publication;
# restrictions apply strictly to navigation rails and policy footer grouping.

def normalize_page(html: str, *, host: str, source: str) -> tuple[str, str]:
    nav = NAV.search(html)
    if nav:
        original = nav.group(2)
        clean, removed = STATUS_ANCHOR.subn("", original)
        if removed > 1:
            raise ValueError(f"{source}: multiple Status actions in one estate rail")
        html = html[:nav.start(2)] + clean + html[nav.end(2):]
    footer = FOOTER.search(html)
    if not footer:
        # Some old chapter routes never received the shared footer.
        # Add the mandatory links after the authored document, not inside it.
        links = (
            '<footer id="footer" class="footer footer-legals-only" role="contentinfo"'
            ' data-footer-style="legal-links"><nav class="footer-legals"'
            ' aria-label="Legal and company information" data-footer-legals="required">'
            + LEGAL_ANCHOR.format(current=(' aria-current="page"' if host=="status.fountain.coach" else '')) +
            ' · <a href="https://governance.fountain.coach/legal/">Legal notices</a>'
            ' · <a href="https://governance.fountain.coach/privacy/">Privacy</a>'
            ' · <a href="https://governance.fountain.coach/accessibility/">Accessibility</a>'
            ' · <a href="https://governance.fountain.coach/copyright/">Copyright</a>'
            ' · <a href="https://governance.fountain.coach/compliance/">EU compliance</a>'
            '</nav></footer>'
        )
        if "</body>" not in html:
            return html, "fragment-no-body"
        return html.replace("</body>",links+"</body>",1), "legal-footer"
    block = footer.group()
    if 'class="book-pagination"' in block or 'aria-label="Book pagination"' in block:
        return html, "book-pagination-not-legal-footer"

    # A published footer may contain Status among publications. Move, don't
    # duplicate. This preserves all other sibling publication URLs.
    block, _ = PUB_LINK.subn("", block)
    # Remove the previously generated fallback legal group as a whole.
    block = re.sub(r'<nav\b(?=[^>]*data-footer-legals="required")[^>]*>.*?</nav>', '', block, flags=re.S)
    # In canonical footnotes a formerly inserted Status anchor is the first
    # legal link; consume its trailing separator, not the predecessor.
    block = re.sub(
        r'<a\b(?=[^>]*data-legal-role="company-status")[^>]*>.*?</a>\s*·\s*',
        "", block, flags=re.S
    )
    # A previous legal anchor inserted before a data-role existed also needs
    # removal to make repeat builds deterministic.
    block = re.sub(
        r'(?:\s*·\s*)?<a\b(?=[^>]*href="https://status\.fountain\.coach/")[^>]*>.*?</a>',
        "", block, flags=re.S
    )
    current = ' aria-current="page"' if host == "status.fountain.coach" else ""
    link = LEGAL_ANCHOR.format(current=current)
    policy_row = next(
        (match for match in LEGAL_RE.finditer(block) if POLICY_REF in match.group()),
        None
    )
    if policy_row:
        group = policy_row.group()
        target = group.find('<a ', group.find(POLICY_REF)-100 if group.find(POLICY_REF)>100 else 0)
        # Insert before Legal notices; preserve the original list unchanged.
        target = group.find('<a', group.find("<span", group.find("footer-footnote-number"))+5)
        if target < 0:
            raise ValueError(f"{source}: footnote has no legal anchor")
        group = group[:target] + link + " · " + group[target:]
        block = block[:policy_row.start()] + group + block[policy_row.end():]
    else:
        # Publication-specific footers without a standard footnote row:
        # provide an accessible small legal navigation immediately BEFORE
        # the existing closing logo. Do not rewrite its editorial content.
        legal = (
            '<nav class="footer-legals" aria-label="Legal and company information"'
            ' data-footer-legals="required">'
            + link + ' · '
            '<a href="https://governance.fountain.coach/legal/">Legal notices</a> · '
            '<a href="https://governance.fountain.coach/privacy/">Privacy</a> · '
            '<a href="https://governance.fountain.coach/accessibility/">Accessibility</a> · '
            '<a href="https://governance.fountain.coach/copyright/">Copyright</a> · '
            '<a href="https://governance.fountain.coach/compliance/">EU compliance</a>'
            '</nav>'
        )
        logo = re.search(
            r'<a\b[^>]*class="[^"]*(?:footer-mark|solstice-close-mark)[^"]*"[^>]*>',
            block,
        )
        if logo:
            block = block[:logo.start()] + legal + block[logo.start():]
        else:
            block = block.replace("</footer>", legal + "</footer>", 1)
    if block.count(STATUS_URL) != 1:
        raise ValueError(f"{source}: must have exactly one Status legal link in footer")
    if nav and 'data-estate-id="status"' in NAV.search(html).group():
        raise ValueError(f"{source}: Status remains in the header rail")
    return html[:footer.start()] + block + html[footer.end():], "legal-footer"

def execute(root: Path, apply: bool) -> dict:
    checked = changed = ready = exceptions = 0
    by_host = {}
    for page in sorted(root.rglob("index.html")):
        host = (
            "status.fountain.coach"
            if root.name=="site" and (root.parent/"edition.json").is_file()
            else root.name if root.name != "sites"
            else page.relative_to(root).parts[0]
        )
        old = page.read_text(encoding="utf8")
        new, outcome = normalize_page(old, host=host, source=str(page))
        checked += 1
        by_host.setdefault(host, {"pages":0, "ready":0, "updated":0, "exception":0})
        by_host[host]["pages"] += 1
        if outcome == "legal-footer":
            ready += 1
            by_host[host]["ready"] += 1
        else:
            exceptions += 1
            by_host[host]["exception"] += 1
        if old != new:
            changed += 1
            by_host[host]["updated"] += 1
            if apply:
                page.write_text(new, encoding="utf8")
    return {"files":checked,"legalFooters":ready,"exceptions":exceptions,
            "changed":changed,"applied":apply,"byHost":by_host}

if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("--root",type=Path,default=Path("site"))
    cli.add_argument("--apply",action="store_true")
    cli.add_argument("--host",action="append",default=[],
                     help="Only operate the named publication host (repeatable).")
    args=cli.parse_args()
    roots=[args.root/host for host in args.host] if args.host else [args.root]
    for root in roots:
        if not root.is_dir() or not root.resolve().is_relative_to(args.root.resolve()):
            raise SystemExit("Invalid scoped publication root: "+str(root))
    summaries=[execute(root,args.apply) for root in roots]
    print(json.dumps(summaries[0] if len(summaries)==1 else summaries,indent=2))
