# Websa Worldwide website

Static, framework-free rebuild of websaworldwide.com laid out on the Procter & Gamble corporate-site pattern (floating pill header with a centred logo, full-bleed hero with a wave edge, circular imagery, pill buttons, side dot navigation, sticky bottom bar, curved dark footer) and recoloured to the Websa brand: black and gold from the logo, Montserrat self-hosted.

Eighteen pages in three languages (English, Simplified Chinese, Portuguese), a four-step quotation wizard, three case studies, a team page, site search, video, per-page SEO, WebP images, an accessibility pass and an audit that runs on every commit.

## Run it

```bash
python -m http.server 5620 --directory site
```

Or `preview_start` with the `websa` entry in the workspace `.claude/launch.json`. Open http://localhost:5620/.

## Edit it

Everything editorial lives in `build.py`: copy, navigation, brands, projects, case studies, team, videos. Owner settings live in `site.config.json` (copy `site.config.example.json`). Then:

```bash
python build.py
```

It writes 18 English pages into `site/`, translates them into `site/zh/` and `site/pt/` from `i18n/zh.json` and `i18n/pt.json`, generates WebP image sets, per-page share images, `search-index.json` per language, `sitemap.xml` with hreflang, `robots.txt`, the manifest, `site.min.css` and `site.min.js` (terser via npx when node is present, otherwise a copy), and runs an audit: zero em or en dashes, every asset and link resolves, every page has one h1 and a description, translations at least 95 percent complete. Never hand-edit the HTML; the next build overwrites it.

`site/css/site.css` and `site/js/site.js` are edited directly. `python tools/audit.py` runs the build check plus a crawl of all 54 pages (links, anchors, alt text, h1s, unique titles). The pre-commit hook in `.githooks` runs it on every commit (enabled with `git config core.hooksPath .githooks`, already set in this clone) and `.github/workflows/audit.yml` runs it on every push once a remote exists.

## Pages

| File | Purpose |
|---|---|
| index.html | Hero slideshow with "Watch our story" video, mission and three-step method, four sector cards, ten-brand carousel, Northern Cape story band, top five projects, two big calls to action, side dots, bottom bar |
| about.html | Who we are: the idea, six-step timeline 1999 to 2024, two entities, values, directors, why Websa |
| team.html | Leadership and team: the two directors with bios, what the Guangzhou and South Africa offices each do |
| services.html | Hub for the four sectors plus advisory services |
| sourcing.html, energy.html, construction.html, agriculture.html | One page per sector: overview, services offered, why Websa, related projects. Sourcing has the video reel; Energy links its two case studies |
| brands.html | Ten brands in one grid with search and category filter |
| projects.html | Nine projects with totals, three case study cards, sector and country filters (deep-linkable with ?sector= and ?place=) |
| case-postmasburg.html, case-solar-programmes.html, case-ekhaya.html | Case studies: at-a-glance facts, the brief, what Websa did, the result, related links. A partner quote block renders only when a quote is supplied in `CASES` |
| quote.html | Four-step quotation wizard: what, quantity and specs, destination and timeline, contact. Validates each step, saves a draft locally, shows a review, issues a reference like WW-260928-DV9Z, offers WhatsApp confirmation. Accepts ?type= and ?brand= |
| contact.html | Audience blocks, enquiry form, head office card with map, media contact |
| legal.html, privacy.html | Drafted for review by the client's lawyer. Privacy text adapts to the analytics and form settings in the config |
| 404.html | Not found |

Every page exists at `/`, `/zh/` and `/pt/` with hreflang links and a language pill in the header.

## Features and how they are wired

- **Quotation wizard and contact form.** With `form_endpoint` empty (the default) they open the visitor's email app with the request prefilled and addressed to info@websaworldwide.com. With an endpoint set they POST JSON, show the reference on success, and fall back to an error message on failure. Endpoint options: Formspree, Web3Forms, or the Google Apps Script in `tools/enquiry-log.gs`, which appends every submission to a Google Sheet the directors can open on their phones and emails them a summary. Set-up steps are at the top of that file.
- **Floating WhatsApp button** on every page, prefilled with the page title; a call button appears beside it on phones. Every WhatsApp link on the site carries the page context.
- **Search.** The header pill (or Ctrl/Cmd+K) opens an overlay that searches `search-index.json` (pages, sections, brands, projects, case studies) in the browser. Arrow keys and Enter work. `?q=` opens it prefilled.
- **Video.** Four films from the client's YouTube channel. Thumbnails are stored locally; YouTube loads in privacy-enhanced mode only when someone presses play.
- **Languages.** `build_translations()` walks the English HTML, translates every text node and translatable attribute from the dictionaries, rewrites asset paths and language links, localises dates, and writes a translated search index. Untranslated strings fall back to English and are listed in `i18n/missing-<lang>.txt`; the audit fails under 95 percent. The Chinese and Portuguese were written by the developer, not a native translator: budget for a native review before launch.
- **SEO.** Per-page title, description, canonical, hreflang, Open Graph image (generated 1200x630 per page), JSON-LD graph: Organization, WebSite with SearchAction, BreadcrumbList, Service per sector, Article per case study, ItemList of Brands, Person per director, ContactPage, AboutPage.
- **Performance.** One variable Montserrat woff2 (38 KB) self-hosted and preloaded, WebP at 480/960/1440 with JPG fallback, lazy loading below the fold, minified CSS and JS, no third-party requests on load.
- **Analytics.** Off by default. `provider: "plausible"` loads Plausible (cookieless, no banner). `provider: "ga4"` loads Google Analytics behind a consent banner with Consent Mode defaulting to denied. Custom events: enquiry_submit, quote_step, quote_submit, brand_click, video_play, search, whatsapp_click, language_switch.

## Measured 2026-09-28

Lighthouse desktop against the local server, after the axe fixes: performance, accessibility, best practices and SEO all 100 on the home page, the Chinese home page, quote, sourcing and contact. axe-core 4.10 (WCAG 2.2 AA plus best practice) reports zero violations on home, quote, contact and the Portuguese brands page.

Verified in the browser: dropdown menus, drawer, search, video modal, language switch, quote wizard end to end (URL prefill, per-step validation, review, reference, WhatsApp confirmation, draft clearing), filters with translated counters, WhatsApp prefill, no horizontal overflow at 375 px, no console errors.

## Facts used and where they came from

Everything comes from the client's current website, their Instagram bio, their YouTube channel, or the owner's messages on 2026-09-27. No invented testimonials, statistics or client names beyond the partners the client already names (Lesedi Solar PV, Letsatsi Solar PV, Philips Lighting, Ndewere Corporation, NDECOR Trading, Ekhaya).

- Company names, registrations, directors, history, address, phone, email: websaworldwide.com/en/about-us.
- Project list and values: websaworldwide.com/en. Shown with the note "as reported by Websa Worldwide".
- Brand list: the owner (Zarus, Kudus, Benny Yamin, Wakanaka, Stewart, Runningman, Bigman Autospares, EnergyOn) plus Blue Digital Printing and Sandie's Happy Basket, which have logos on the client's current site. Brands with real logos are listed first.
- Videos: the client's YouTube channel UCHVO1O6lElQ-rtjxux3nr1Q.
- Photography: the images the client already uses, downloaded at the largest size served. Several are StockCake or Freepik stock; confirm licences before launch or replace with their own photographs.

## Placeholders and items to confirm with the client

1. **Brand logos.** Kudus, Runningman, Blue Digital Printing and Sandie's Happy Basket have real artwork. Zarus, Benny Yamin, Wakanaka, Stewart, Bigman Autospares and EnergyOn use generated monogram placeholders in `site/assets/brands/*.svg`. Replace each SVG with the real logo.
2. **What each brand sells.** Only Kudus (baby diapers) is confirmed. Bigman Autospares and EnergyOn are described from their names. The other four are described only as "A Websa Worldwide brand".
3. **Case study partner quotes.** Each case study has a quote slot that stays hidden until a real quote is supplied.
4. **Team photos and names.** Directors only. Add staff to `TEAM` in `build.py` when the client supplies names, roles and photos.
5. **Logo vector**, a **South Africa address** and **office hours** (shown as Monday to Friday 09:00 to 18:00 China time).
6. **Form endpoint.** Choose Apps Script, Formspree or Web3Forms and set `form_endpoint`. Until then the forms open email.
7. **Analytics account.** Choose Plausible or GA4 and set the config. Until then nothing loads.
8. **Native review of the Chinese and Portuguese.**
9. **Energy and petroleum.** Describes documented solar work plus "petroleum supply", which the old site claims without detail.
10. **Legal and privacy pages.** Lawyer review.

## Known defects on the client's current site

- The bare domain websaworldwide.com redirects to www.websaworldwide.com, a dead Odoo host. Only /en and /fr work.
- Kudus page is lorem ipsum. kudus. and runningman. subdomains do not resolve.
- Legal Notice and Privacy links return 404. The French page is English content in an old template.

## Design tokens

Black `#141414`, gold `#b08a22` (accent, large text, the headline full stop), gold on dark `#d4a72c`, gold for small text `#7a5f14` (6.0:1 on white), warm tint `#f6f3ec`, muted text `#5a5a5a` (6.9:1), WhatsApp green `#16703a` (5.8:1 with white). Montserrat 100 to 900 variable. Chinese pages fall back to the system CJK stack.
