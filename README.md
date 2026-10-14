# status.fountain.coach — authoritative public edition

**Public URL:** https://status.fountain.coach/

This Git repository is the **sole authoritative source edition** for the
complete Fountain Coach company-status, business context and transparency
publication. Its content root is [site/](site/), not the repository root.

The initial baseline was fetched from the real public HTTPS domain on
14 October 2026. **All 25 publicly served files (12 HTML routes)** were
individually verified byte-for-byte against a fresh HTTPS GET using SHA-256.
It includes the published business-architecture data/schema, company and
transparency pages, machine discovery endpoints, original illustration and
assets. It is not a newly generated rewrite of the public status domain.

## Domain ownership

1. **This repository owns future Status text, company-status claims,
   publication routes, assets and legal/footer placement.** Reviewed changes
   go into `site/` and require an explicit canonical Git commit.
2. The old `midi2-gpu-fabric/estate/sites/status.fountain.coach/` checkout
   is a **downstream materialization**, not another authoring tree.
3. A change becomes *source-authored* on commit here. It becomes *published*
   only after independent authorization, an exact-host EstatePublisher
   operation and receipt, and independently verified public HTTPS read-back.
   Neither a Git push nor a local static preview deploys anything.
4. The persistent shared estate footer links to this host as **Company
   status & transparency**, grouped with Legal notices, Privacy,
   Accessibility, Copyright and EU compliance. Status is **not** a header
   rail destination. That new design rule is a **subsequent source edition**:
   the initial live-exact snapshot retains the old published header layout
   for historical byte parity.
5. This site supplies company status and transparency, **not a replacement**
   for a legally required Impressum, Privacy statement or accessibility
   declaration.

## Verify

```sh
python3 scripts/verify_publication.py
python3 scripts/verify_publication.py --against-live
python3 scripts/reconcile_estate.py \
  --estate-site /absolute/estate/sites/status.fountain.coach
```

The first verifies every Git-owned byte against
[publication-files.sha256](publication-files.sha256), including exact file
inventory and expected routes. The second independently downloads the
entire public website for all-file HTTPS parity; run that **after** release
when the Git source has changed. `scripts/reconcile_estate.py` compares the
estate-derived files **read-only by default** and can materialize only that
site with an explicit `--apply`. It does not deploy.

The initial witness is preserved at
[docs/live-parity-audit.json](docs/live-parity-audit.json).
The original public parity tag is `status-public-snapshot-20261014`.
That audit does not imply a subsequent un-deployed source edition is live.

No GitHub workflows/CI, deployment credentials, private host data or
programmatic production mutation are stored here. Only the published
public site is in `site/`.

## Publication semantics

Status covers the business and published project state, not private runtime
state. Other Git-authoritative domains are siblings, not Status content
stores: `Fountain-Coach/governance.fountain.coach` owns Governance,
`Fountain-Coach/midi2` owns MIDI2 technical publication, and Fountain
Press may derive reader views without altering any owner.

## Current unpublished editorial revision

After the exact-public snapshot tag, the normalizer was admitted as the **owner repository source change**: all 12 pages now show Company Status & Transparency in their footer legal group, not in the header rail. The complete source checksum manifest has been updated. The historical HTTPS witness remains pinned to the original snapshot tag. The current source revision deliberately differs from the live domain until a separately authorized EstatePublisher release and independent HTTPS proof.
