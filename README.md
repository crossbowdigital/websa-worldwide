# Websa Worldwide website

Static, framework-free rebuild of websaworldwide.com, laid out on the Procter & Gamble corporate-site pattern (floating pill header with a centred logo, full-bleed hero with a wave edge, circular imagery, pill buttons, side dot navigation, sticky bottom bar, curved dark footer) and recoloured to the Websa brand (black and gold from the logo).

## Run it

```bash
python -m http.server 5620 --directory site
```

Or `preview_start` with the `websa` entry in the workspace `.claude/launch.json`. Open http://localhost:5620/.

## Edit it

All copy, navigation, brands and projects live in `build.py`. Edit there, then:

```bash
python build.py
```

It writes 13 pages into `site/`, plus `sitemap.xml`, `robots.txt` and `site.webmanifest`, and runs an audit: zero em or en dashes, every local link and asset resolves. Do not hand-edit the HTML files; the next build overwrites them.

`site/css/site.css` and `site/js/site.js` are edited directly.

## Pages

| File | Purpose |
|---|---|
| index.html | Home: hero slideshow, mission and three-step method, four sector cards, brand carousel, Northern Cape story band, top five projects, two big calls to action, side dots, bottom bar |
| about.html | Who we are: the idea, six-step timeline (1999 to 2024), two entities, values, directors, why Websa |
| services.html | Hub for the four sectors plus advisory services |
| sourcing.html, energy.html, construction.html, agriculture.html | One page per sector: overview, services offered, why Websa, related projects |
| brands.html | Ten brands in one grid with search and category filter |
| projects.html | Nine projects with totals, sector and country filters (deep-linkable with ?sector= and ?place=) |
| contact.html | Audience blocks, enquiry form (opens email, WhatsApp alternative), head office, media |
| legal.html, privacy.html | Drafted for review by the client's lawyer |
| 404.html | Not found |

## Facts used and where they came from

Everything on the site comes from the client's current website, their Instagram bio, or the owner's message on 2026-09-27. Nothing was invented: no testimonials, no statistics beyond the project values the client already publishes, no client names other than the partners the client already names (Lesedi Solar PV, Letsatsi Solar PV, Philips Lighting, Ndewere Corporation, NDECOR Trading, Ekhaya).

- Company names, registrations, directors, history, address, phone, email: websaworldwide.com/en/about-us.
- Project list and values: websaworldwide.com/en (projects section). Shown with the note "as reported by Websa Worldwide".
- Brand list: the owner's message (Zarus, Kudus, Benny Yamin, Wakanaka, Stewart, Runningman, Bigman Autospares, EnergyOn) plus Blue Digital Printing and Sandie's Happy Basket, which have logos on the client's current site. Brands with real logos are listed first.
- Hero and page photography: the images the client already uses on their site, downloaded from it at the largest size served (mostly 1024 or 1200 px wide). Several are StockCake or Freepik stock images; confirm the client holds licences before launch or replace with their own photographs.

## Placeholders and items to confirm with the client

1. **Brand logos.** Kudus, Runningman, Blue Digital Printing and Sandie's Happy Basket have real artwork from the client's site. Zarus, Benny Yamin, Wakanaka, Stewart, Bigman Autospares and EnergyOn use generated monogram placeholders in `site/assets/brands/*.svg`. Replace each SVG with the real logo (same file name, or update `BRANDS` in `build.py`).
2. **What each brand sells.** Only Kudus (baby diapers, from the old site) is confirmed. Bigman Autospares and EnergyOn are described from their names. The other four are described only as "A Websa Worldwide brand". Ask for one line each.
3. **Logo vector.** The header and footer use a 374 px PNG rebuilt from the client's site (transparent and reversed versions in `site/assets/img/`). Ask for the vector file.
4. **South Africa address and phone.** Not published anywhere; the site says "registered in South Africa" and offers a meeting. Add an address if they have one.
5. **Office hours.** Shown as Monday to Friday 09:00 to 18:00 China time. Confirm.
6. **Enquiry form.** With no backend, the form opens the visitor's email app with the enquiry prefilled to info@websaworldwide.com, and a WhatsApp button carries the same message to +86 173 2401 0515. If the client wants submissions stored, add a form service and update `site/js/site.js`.
7. **Energy and petroleum.** The old site lists only values for this sector. The page describes solar street lighting and the two solar plant programmes (documented) plus "petroleum supply" (claimed by the old site with no detail). Confirm what they actually sell.
8. **Legal and privacy pages.** Drafted honestly for what the site does; the client's lawyer should review.
9. **Social links.** Footer points to the real Facebook, Instagram and YouTube profiles found in research. The old site had no Twitter profile, so none is linked.

## Known defects on the client's current site (for the sales conversation)

- The bare domain websaworldwide.com redirects to www.websaworldwide.com, which is a dead Odoo host (404). Only /en and /fr work.
- Kudus page is lorem ipsum. kudus. and runningman. subdomains do not resolve.
- Legal Notice and Privacy links return 404.
- French page is English content in an old template.
- Page titles read "WEB", the meta description is "WEBSA CHINA", and the hero misspells "building".

## Design tokens

Black `#141414` (primary surfaces, headings), gold `#b08a22` (accent, large text, the headline full stop), gold on dark `#d4a72c`, gold for small text `#7a5f14` (6.0:1 on white), warm tint `#f6f3ec`, muted text `#5a5a5a` (6.9:1). Montserrat 400 to 800 from Google Fonts. All text colour pairs measured at 4.5:1 or better.

## Verified 2026-09-27

Desktop 1280 and 1440 and phone 375 in the Claude browser pane: hero, dropdown menus (click, hover, Escape), mobile drawer and accordion, brand carousel (8 tiles, dots and arrows), project filters (`?sector=energy` shows 3 of 9), contact type preselect from `?type=`, WhatsApp prefill, form validity, no horizontal overflow at 375, no console errors. Build audit clean.
