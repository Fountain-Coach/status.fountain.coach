# Status references, discretionary publication and unfeatured Works

Decision candidate — 24 October 2026. The author requires a bounded, durable distinction between visible publications and discreet or private documentary material, so navigation cannot later drift into an unexplained missing backlink.

## One estate, different editorial lanes

**Book** is the featured public entrance to approved authored editions and their reader. **Works** is the author's source-owned portfolio, attribution record and preparation context, independently available but **off the estate reel**. It is not the canonical WLAN staging environment, and publicly accessible Works pages are not private. **Status** is a public supporting company/transparency domain, placed in the legal/footer group, not the reel. Its new `/references/` route explains recipient-directed references and privacy limits.

The existing public First Reading URL under Works/Solstice is preserved. The source owner retains original material and credits while Book may direct readers to the actual published edition. Source ownership, Book publication, Reframe Bookshelf admission and EstatePublisher public promotion are distinct decisions.

## Three visibility states (independent of reel membership)

1. **Featured public:** intentional edition/publication in the editorial index.
2. **Discreet public:** explicitly selected and redacted document, directly reachable without authentication, not promoted in main editorial reel or search index. Its privacy status is PUBLIC, despite its low prominence. Each released document must carry return navigation, authority, title/date/version, and an unambiguous context.
3. **Private controlled:** original Jobcenter/administrative correspondence, bank/billing/benefit documents, identifiable legal evidence, personal case records, unapproved drafts. Never commit to a public Git source or put in `site/`, a publicly readable origin, or even a public staging route. Use the original private repo/authorized delivery channel. A recipient-specific public summary may be separately approved only after checking redaction, consent, lawful purpose and third-party interests.

## No tracking claims beyond the evidence

The static `site/references/index.html` has **no page-side analytics, scripts, cookies, tracking pixels, external fonts or third-party content**. It uses inline first-party CSS and a plain HTML page, with `noindex,nofollow,noarchive,nosnippet` and `no-referrer` metatags. These are preference signals, NOT an access control, assurance of deindexing or absolute anonymity. The server, reverse proxy and transport still potentially process IP addresses, timestamps and request URLs. Any future strong anonymity promise must be grounded in host/log/transport evidence, not a static HTML assertion.

Recipients who do not want to access a website should be able to receive the separately authorized, locally readable PDF/document through an agreed private channel. Do not track clicks or introduce a paywall/login or bespoke sharing system for an ordinary static reference.

## Link/backlink contract

- Featured Book entry links to the real source-owned reader, carries relevant source credit and a return route to Book.
- Works is accessible as a supporting source and author portfolio; its actual editions can return to the Book editorial index while preserving individual source authority.
- Status `/transparency/` includes a quiet link to `/references/`; the references route links back to Status and Transparency. Neither is promoted into the estate reel.
- A shared redacted reference should have an internal backlink to its own Status/reference context but should **not** embed backlinks to private case files, recipients, repositories or identifiers.
- The public site contains **zero actual administrative records** until each record is independently reviewed and authorized.

## Source, staging and publication boundaries

The current status.fountain.coach owner is Fountain-Coach/status.fountain.coach (`site/`); Book, Works and Estate retain their independent Git source authorities. Development is Git; the existing owner-WLAN Ubuntu Mac mini is the only estate staging server; the public HTTPS Status domain stays on its separately published release. No new DNS environment, public document vault, authentication service or GitHub CI is justified by this bounded editorial requirement.

This decision does not authorize production deployment or broad publication of administrative files. Approval of specific recipient-safe records, host-side logging policy and live HTTPS verification are separate.
