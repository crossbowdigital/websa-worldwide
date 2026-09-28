# -*- coding: utf-8 -*-
"""Websa Worldwide static site generator.

    python build.py            build everything into ./site (en, zh, pt)
    python build.py --check    build, then exit 1 if the audit finds a problem

Owner-editable settings live in site.config.json next to this file (see CONFIG below
for the keys). Copy, navigation, brands, projects, case studies and team live here.
"""
import os, re, sys, json, html as htmlmod, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
I18N = os.path.join(ROOT, "i18n")

# ---------------------------------------------------------------- config
CONFIG = {
  # Where the quote wizard and contact form POST. Empty string = open the visitor's email app instead.
  # Accepts a Formspree or Web3Forms endpoint, or the Google Apps Script web app URL from tools/enquiry-log.gs.
  "form_endpoint": "",
  # "plausible" (cookieless, no banner) or "ga4" (needs the consent banner) or "" for none.
  "analytics": {"provider": "", "plausible_domain": "websaworldwide.com", "ga4_id": ""},
  "site_url": "https://websaworldwide.com",
  "languages": ["en", "zh", "pt"],
  "youtube_channel": "UCHVO1O6lElQ-rtjxux3nr1Q",
}
_cfg_path = os.path.join(ROOT, "site.config.json")
if os.path.exists(_cfg_path):
    _user = json.load(open(_cfg_path, encoding="utf-8"))
    for k, v in _user.items():
        if isinstance(v, dict) and isinstance(CONFIG.get(k), dict): CONFIG[k].update(v)
        else: CONFIG[k] = v

SITE_URL = CONFIG["site_url"].rstrip("/")
LANGS = CONFIG["languages"]
PHONE_DISPLAY = "+86 173 2401 0515"
PHONE_TEL = "+8617324010515"
WA_NUMBER = "8617324010515"
WA = "https://wa.me/" + WA_NUMBER
EMAIL = "info@websaworldwide.com"
ADDRESS_LINES = ["16 Caiping Road, Suite 412, Building 2", "Hesheng Plaza, Huangpu District", "Guangzhou 510700, China"]
MAP_URL = "https://www.google.com/maps/search/?api=1&query=16+Caiping+Road+Hesheng+Plaza+Huangpu+District+Guangzhou"
TODAY = datetime.date.today()
LANG_META = {"en": ("en", "English"), "zh": ("zh-Hans", "中文"), "pt": ("pt", "Português")}

# ---------------------------------------------------------------- icons
I = {
  "chev": '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>',
  "ext": '<svg class="ext" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M7 17 17 7M8 7h9v9"/></svg>',
  "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
  "arrowl": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>',
  "globe": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/></svg>',
  "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" aria-hidden="true"><circle cx="12" cy="12" r="9" opacity=".35"/><path d="m8 12 3 3 5-6"/></svg>',
  "pause": '<svg class="ico-pause" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>',
  "play": '<svg class="ico-play" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
  "playbig": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M8 5v14l11-7z"/></svg>',
  "search": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
  "close": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>',
  "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
  "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
  "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>',
  "ship": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 17c2 1.5 4 1.5 6 0s4-1.5 6 0 4 1.5 6 0M4 14l1-5h14l1 5M8 9V5h8v4"/></svg>',
  "bolt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M13 2 4 14h7l-1 8 9-12h-7z"/></svg>',
  "crane": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 21h18M6 21V8l6-4 6 4v13M10 21v-5h4v5M12 8v4"/></svg>',
  "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 4c-9 0-15 5-15 12a5 5 0 0 0 5 5c7 0 12-6 12-15z"/><path d="M5 21c3-6 7-9 12-12"/></svg>',
  "handshake": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m12 11 3-3 5 1 2 4-6 6-4-1M12 11 8 7 3 8l-1 4 6 6 3-1M12 11l3 3"/></svg>',
  "users": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4a3.5 3.5 0 0 1 0 7M21.5 20a6.5 6.5 0 0 0-5-6.3"/></svg>',
  "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/></svg>',
  "spark": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3v4M12 17v4M3 12h4M17 12h4M5.6 5.6l2.8 2.8M15.6 15.6l2.8 2.8M5.6 18.4l2.8-2.8M15.6 8.4l2.8-2.8"/></svg>',
  "star": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m12 3 2.8 5.8 6.2.9-4.5 4.4 1.1 6.2L12 17.4 6.4 20.3l1.1-6.2L3 9.7l6.2-.9z"/></svg>',
  "book": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 5a2 2 0 0 1 2-2h5v18H6a2 2 0 0 0-2 2zM20 5a2 2 0 0 0-2-2h-5v18h5a2 2 0 0 1 2 2z"/></svg>',
  "tag": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/></svg>',
  "grid": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>',
  "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M4 5h16v11H9l-5 4z"/></svg>',
  "doc": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 12h6M9 16h6"/></svg>',
  "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8h2.7l.4-3.2h-3.1V8.8c0-.9.3-1.6 1.6-1.6h1.7V4.3c-.3 0-1.3-.1-2.5-.1-2.5 0-4.1 1.5-4.1 4.2v2.4H7.4V14h2.8v8z"/></svg>',
  "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
  "yt": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M21.6 7.2a2.5 2.5 0 0 0-1.8-1.8C18.2 5 12 5 12 5s-6.2 0-7.8.4A2.5 2.5 0 0 0 2.4 7.2 26 26 0 0 0 2 12a26 26 0 0 0 .4 4.8 2.5 2.5 0 0 0 1.8 1.8C5.8 19 12 19 12 19s6.2 0 7.8-.4a2.5 2.5 0 0 0 1.8-1.8A26 26 0 0 0 22 12a26 26 0 0 0-.4-4.8zM10 15V9l5.2 3z"/></svg>',
  "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 2.9 2.9 0 0 0-.9 2.2 5 5 0 0 0 1.1 2.7 11.5 11.5 0 0 0 4.4 3.9c1.6.7 2.3.8 3.1.6a2.6 2.6 0 0 0 1.7-1.2 2.1 2.1 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>',
}

# ---------------------------------------------------------------- data
SECTORS = [
  dict(slug="sourcing", tag="Trade", name="Import, export and logistics", img="assets/img/warehouse.jpg",
       alt="Forklift moving pallets inside a distribution warehouse",
       short="Factory-direct sourcing from China, with the paperwork, freight and customs handled end to end."),
  dict(slug="energy", tag="Energy", name="Energy and petroleum", img="assets/img/solar-farm.jpg",
       alt="Rows of solar panels on a utility-scale solar farm",
       short="Solar street lighting, utility-scale programme delivery and fuel supply for growing towns and businesses."),
  dict(slug="construction", tag="Build", name="Construction, mining, signage and print", img="assets/img/construction.jpg",
       alt="Construction workers and an excavator on a building site",
       short="Sites, mines and storefronts: equipment, project management and the signage that puts your name on the door."),
  dict(slug="agriculture", tag="Agriculture", name="Agriculture", img="assets/img/harvest.jpg",
       alt="Farm workers harvesting vegetables in a field",
       short="Crop and livestock farming, quality seed and the equipment and training that turn a farm into a business."),
]

BRANDS = [
  dict(slug="kudus", name="Kudus", cat="baby", catname="Baby care", img="assets/brands/kudus.png", w=674, h=771, placeholder=False,
       line="Baby diapers made for African families: soft, absorbent and dependable."),
  dict(slug="runningman", name="Runningman", cat="other", catname="Websa brand", img="assets/brands/runningman.png", w=995, h=273, placeholder=False,
       line="Let's go. A Websa Worldwide brand."),
  dict(slug="blue-digital-printing", name="Blue Digital Printing", cat="print", catname="Signage and print", img="assets/brands/blue-digital-printing.png", w=405, h=164, placeholder=False,
       line="Digital printing and custom signage for businesses, public bodies, non-profits and events."),
  dict(slug="sandies-happy-basket", name="Sandie's Happy Basket", cat="consumer", catname="Everyday essentials", img="assets/brands/sandies-happy-basket.png", w=180, h=179, placeholder=False,
       line="A Websa Worldwide consumer brand."),
  dict(slug="zarus", name="Zarus", cat="other", catname="Websa brand", img="assets/brands/zarus.svg", w=400, h=400, placeholder=True,
       line="A Websa Worldwide brand."),
  dict(slug="benny-yamin", name="Benny Yamin", cat="other", catname="Websa brand", img="assets/brands/benny-yamin.svg", w=400, h=400, placeholder=True,
       line="A Websa Worldwide brand."),
  dict(slug="wakanaka", name="Wakanaka", cat="other", catname="Websa brand", img="assets/brands/wakanaka.svg", w=400, h=400, placeholder=True,
       line="A Websa Worldwide brand."),
  dict(slug="stewart", name="Stewart", cat="other", catname="Websa brand", img="assets/brands/stewart.svg", w=400, h=400, placeholder=True,
       line="A Websa Worldwide brand."),
  dict(slug="bigman-autospares", name="Bigman Autospares", cat="auto", catname="Automotive", img="assets/brands/bigman-autospares.svg", w=400, h=400, placeholder=True,
       line="Vehicle parts and spares, sourced and supplied by Websa."),
  dict(slug="energyon", name="EnergyOn", cat="energy", catname="Energy", img="assets/brands/energyon.svg", w=400, h=400, placeholder=True,
       line="Websa Worldwide's energy brand."),
]

PROJECTS = [
  dict(name="Digital printing and signage", where="South Africa", sector="print", sectorname="Signage and print", cur="R", val=52800000, note="Custom signage and digital print for business, public sector, non-profit and event clients."),
  dict(name="Lesedi Solar PV (75 MW) SED and ED programme", where="Northern Cape, South Africa", sector="energy", sectorname="Energy", cur="R", val=25000000, note="Procurement, supply and training delivered over two years for the plant's socio-economic and enterprise development commitments.", case="case-solar-programmes.html"),
  dict(name="Letsatsi Solar PV (75 MW) SED and ED programme", where="Northern Cape, South Africa", sector="energy", sectorname="Energy", cur="R", val=25000000, note="The sister programme to Lesedi, run on the same model for two years.", case="case-solar-programmes.html"),
  dict(name="Farming and mining equipment supply", where="Zimbabwe and South Africa", sector="trade", sectorname="Trade", cur="R", val=20000000, note="Sourcing, financing support and delivery of equipment for crop farmers and mining operators."),
  dict(name="Solar street lights, Postmasburg", where="Northern Cape, South Africa", sector="energy", sectorname="Energy", cur="R", val=12000000, note="Procured and installed with Lesedi Solar PV and Philips Lighting. Local residents were hired and trained to do the installation.", case="case-postmasburg.html"),
  dict(name="Medical supplies, Bloemfontein", where="Free State, South Africa", sector="health", sectorname="Health", cur="R", val=9000000, note="Supply of medical consumables and equipment."),
  dict(name="Ekhaya Takeaway restaurants", where="Bulawayo, Zimbabwe", sector="retail", sectorname="Retail", cur="R", val=8400000, note="The first outlet opened in 2018 through the WEBSA programme. Twelve shops were trading by 2024.", case="case-ekhaya.html"),
  dict(name="Vehicle importation from Durban, Japan and Singapore", where="Southern Africa", sector="trade", sectorname="Trade", cur="$", val=800000, note="Sourcing, shipping and clearance of vehicles for clients in the region."),
  dict(name="Livestock project", where="Zimbabwe", sector="agriculture", sectorname="Agriculture", cur="$", val=200000, note="Livestock farming investment delivered under the WEBSA agricultural programme."),
]

VIDEOS = [
  dict(id="m7uRI-iZhX8", title="Product sourcing from China made easy through Websa", dur="0:54", thumb="assets/video/m7uRI-iZhX8.jpg", hero=True),
  dict(id="9ER54qSuKSU", title="Connecting Africa to China's top manufacturers", dur="", thumb="assets/video/9ER54qSuKSU.jpg"),
  dict(id="pdPVVnpO2Cc", title="Connecting Africa to China's manufacturing industry", dur="", thumb="assets/video/pdPVVnpO2Cc.jpg"),
  dict(id="M96_JAnpQXs", title="Solar and power tools direct from China", dur="", thumb="assets/video/M96_JAnpQXs.jpg"),
]

TEAM = [
  dict(name="Lazarus Magura", role="Founding director", office="Guangzhou and Zimbabwe", photo=None,
       bio="Started the WEBSA programme in Zimbabwe in 1999 to make farmers and their value chain self-sufficient, and has led its agricultural, equipment and energy projects since. A director and shareholder of both Websa companies."),
  dict(name="Collins Ndewere", role="Director", office="South Africa", photo=None,
       bio="Brought the programme to South Africa through Ndewere Corporation in 2008 and NDECOR Trading in 2014, and directed the Northern Cape solar street lighting and the Lesedi and Letsatsi programme work. A director and shareholder of both Websa companies."),
]

CASES = [
  dict(slug="case-postmasburg", title="Street lights that taught a town to install them", short="Solar street lighting in Postmasburg, Northern Cape",
       img="assets/img/solar-farm.jpg", alt="Solar panels under a clear sky", sector="Energy", value="R 12 000 000", place="Postmasburg, Northern Cape, South Africa", when="From 2014",
       partners="Lesedi Solar PV, Philips Lighting, NDECOR Trading (Pty) Ltd",
       brief="Postmasburg needed reliable street lighting that did not depend on a strained grid. The lighting also had to count towards the local development commitments of the solar plants nearby, which meant the work could not simply be flown in and flown out again.",
       did=["Procured solar street lights in partnership with Lesedi Solar PV and Philips Lighting, with NDECOR Trading delivering the project under the WEBSA programme.",
            "Hired residents of the Northern Cape and trained them to install the lights, so the workforce was local from the first pole.",
            "Managed installation across the town under the direction of Collins Ndewere and Lazarus Magura.",
            "Left behind installers who could maintain and extend the system without outside help."],
       result="The town got its lighting and a trained local workforce got a trade. The delivery record led directly to a two-year role running procurement, supply and training for the Lesedi and Letsatsi solar plants' development programmes.",
       quote=None, quote_by=None, related=["case-solar-programmes.html", "energy.html"]),
  dict(slug="case-solar-programmes", title="Two solar plants, two years, one delivery partner", short="Lesedi and Letsatsi 75 MW SED and ED programmes",
       img="assets/img/factory.jpg", alt="Modern equipment inside a clean manufacturing hall", sector="Energy", value="R 25 000 000 each", place="Northern Cape, South Africa", when="Two years",
       partners="Lesedi Solar PV Company (75 MW), Letsatsi Solar PV Company (75 MW)",
       brief="South African renewable energy plants must fund socio-economic development (SED) and enterprise development (ED) in the communities around them. Lesedi and Letsatsi, two 75 MW solar plants in the Northern Cape, needed a partner who could turn those obligations into delivered goods, working enterprises and trained people, and account for every rand.",
       did=["Acted as the main company carrying out procurement, supply and training for both plants' SED and ED projects for two years.",
            "Sourced and supplied equipment and materials for community and enterprise projects.",
            "Trained local residents and small enterprises, following the WEBSA principle that the people who receive an asset must be able to run it.",
            "Reported against each programme's commitments so the plants could evidence compliance."],
       result="Two programmes valued at R25 million each were delivered in full over two years, and the solar street lighting model first proven in Postmasburg was carried into the wider region.",
       quote=None, quote_by=None, related=["case-postmasburg.html", "energy.html"]),
  dict(slug="case-ekhaya", title="From one takeaway to twelve shops", short="Ekhaya Takeaway restaurants, Bulawayo",
       img="assets/img/harvest.jpg", alt="Fresh produce being harvested", sector="Retail", value="R 8 400 000", place="Bulawayo, Zimbabwe", when="2018 to 2024",
       partners="Ekhaya Takeaway",
       brief="A fast food business in Bulawayo needed more than a loan. It needed a plan that would survive Zimbabwe's operating conditions: the right equipment at the right price, suppliers that would keep delivering, and people trained to run each outlet to the same standard.",
       did=["Formulated the business under the WEBSA wealth building strategy: specification, costed plan and funding route.",
            "Procured kitchen and shop equipment through Websa's sourcing channels.",
            "Trained the operating team before the first shop opened in 2018.",
            "Supported each new outlet on the same model as the chain grew."],
       result="What opened as one restaurant in 2018 was trading from twelve shops by 2024, a working example of the WEBSA strategy applied to retail rather than farming or energy.",
       quote=None, quote_by=None, related=["case-postmasburg.html", "sourcing.html"]),
]

# ---------------------------------------------------------------- helpers
def money(cur, val):
    s = "{:,}".format(val).replace(",", " ")
    return ("R" if cur == "R" else "US$") + " " + s

def esc(s): return htmlmod.escape(s, quote=True)

_WIDTHS = (480, 960, 1440)
_pic_cache = {}
def pic(src, alt, sizes="100vw", cls="", loading="lazy", fetchpriority=None):
    """<picture> with WebP srcset generated at build time from the JPG under site/."""
    from PIL import Image
    full = os.path.join(OUT, src)
    if src not in _pic_cache:
        im = Image.open(full); ow, oh = im.size
        base, _ = os.path.splitext(os.path.basename(src))
        outdir = os.path.join(OUT, "assets", "img", "w"); os.makedirs(outdir, exist_ok=True)
        variants = []
        for tw in _WIDTHS:
            tw = min(tw, ow)
            name = "%s-%d.webp" % (base, tw); path = os.path.join(outdir, name)
            if not os.path.exists(path) or os.path.getmtime(path) < os.path.getmtime(full):
                im2 = im.convert("RGB"); im2.thumbnail((tw, 10000), Image.LANCZOS); im2.save(path, "WEBP", quality=78, method=6)
            variants.append((tw, "assets/img/w/" + name))
            if tw == ow: break
        _pic_cache[src] = (ow, oh, variants)
    ow, oh, variants = _pic_cache[src]
    srcset = ", ".join("%s %dw" % (p, tw) for tw, p in variants)
    fp = ' fetchpriority="%s"' % fetchpriority if fetchpriority else ""
    return ('<picture><source type="image/webp" srcset="%s" sizes="%s"><img src="%s" alt="%s" width="%d" height="%d" loading="%s" decoding="async"%s%s></picture>'
            % (srcset, sizes, src, esc(alt), ow, oh, loading, fp, (' class="%s"' % cls) if cls else ""))


def first_sentences(text, limit=158):
    parts = re.split(r"(?<=[.!?])\s+", text)
    out = ""
    for part in parts:
        if not out: out = part
        elif len(out) + 1 + len(part) <= limit: out += " " + part
        else: break
    if len(out) > limit:
        cut = max(out.rfind(", ", 0, limit), out.rfind(": ", 0, limit), out.rfind("; ", 0, limit))
        out = (out[:cut] if cut > 60 else out[:limit].rsplit(" ", 1)[0]).rstrip(",;:") + "."
    return out

def wave(to=""):
    return '<svg class="wave %s" viewBox="0 0 1440 80" preserveAspectRatio="none" aria-hidden="true"><path d="M0,80 L0,70 Q720,-20 1440,70 L1440,80 Z"/></svg>' % to

def page_hero(icon, title, sub, lede, img, alt, compact=False, extra=""):
    return '''
<section class="page-hero%(c)s">
  %(pic)s
  <div class="inner">
    <div class="icon">%(icon)s</div>
    <h1>%(title)s<span class="dot">.</span></h1>
    %(sub)s
    %(lede)s
    %(extra)s
  </div>
  %(wave)s
</section>''' % dict(c=" compact" if compact else "", pic=pic(img, alt, cls="bg", loading="eager", fetchpriority="high"), icon=icon, title=title,
                     sub=('<p class="sub">%s</p>' % sub) if sub else "", lede=('<p class="lede">%s</p>' % lede) if lede else "", extra=extra, wave=wave())

def cta_strip(h, p, primary=("quote.html", "Get a quotation"), secondary=None):
    sec = '<a class="btn btn-ghost" href="%s">%s</a>' % secondary if secondary else ""
    return '''
<section class="section" style="padding-top:0">
  <div class="shell"><div class="cta-strip reveal">
    <div><h2>%s</h2><p>%s</p></div>
    <div class="btn-row"><a class="btn btn-gold" href="%s">%s</a>%s</div>
  </div></div>
</section>''' % (h, p, primary[0], primary[1], sec)

def checks(items, big=False):
    return '<ul class="checks%s">' % (" big" if big else "") + "".join('<li>%s<span>%s</span></li>' % (I["check"], t) for t in items) + '</ul>'

def place_codes(p):
    w = p["where"]; codes = []
    if "South Africa" in w or "Southern Africa" in w: codes.append("sa")
    if "Zimbabwe" in w or "Southern Africa" in w: codes.append("zw")
    return " ".join(codes)

def project_li(p, with_note=True):
    case = (' <a class="case-link" href="%s">Read the case study %s</a>' % (p["case"], I["arrow"])) if p.get("case") else ""
    return '''
        <li class="project reveal" data-item data-sector="%(sector)s" data-place="%(place)s">
          <span class="tag">%(sn)s</span>
          <div><h3>%(name)s</h3><p>%(where)s%(note)s</p>%(case)s</div>
          <div class="value">%(val)s<small>project value</small></div>
        </li>''' % dict(sector=p["sector"], place=place_codes(p), sn=p["sectorname"], name=p["name"], where=p["where"],
                       note=(". " + p["note"]) if with_note else "", case=case, val=money(p["cur"], p["val"]))

def case_card(c, i=0):
    return '''<a class="card reveal d%d" href="%s.html"><div class="circle">%s</div><div class="meta">%s &middot; %s</div><h3>%s</h3><p>%s</p><span class="more">Read the case study %s</span></a>''' % (
        i % 4, c["slug"], pic(c["img"], "", sizes="220px"), c["sector"], c["value"], c["title"], c["short"], I["arrow"])

# ---------------------------------------------------------------- navigation
NAV_LEFT = [
  ("What we do", [
    ("services.html", "All services", "Four sectors, one way of working"),
    ("sourcing.html", "Import, export and logistics", "Sourcing from China, delivered to Africa"),
    ("energy.html", "Energy and petroleum", "Solar, electricity and fuel supply"),
    ("construction.html", "Construction, mining and print", "Build, extract, brand"),
    ("agriculture.html", "Agriculture", "Farming, seed and rural livelihoods"),
  ]),
  ("Our brands", [("brands.html", "Brand portfolio", "Kudus, Runningman, Zarus, EnergyOn and more")]),
]
NAV_RIGHT = [
  ("Our story", [
    ("about.html", "Who we are", "From a 1999 farm programme to a Guangzhou company"),
    ("about.html#timeline", "Our history", "Twenty-five years of the WEBSA programme"),
    ("team.html", "Leadership and team", "The directors and the two offices"),
  ]),
  ("Projects", [
    ("projects.html", "Track record", "Nine delivered projects across two countries"),
    ("case-postmasburg.html", "Case study: Postmasburg lighting", "Solar street lights and a trained local workforce"),
    ("case-solar-programmes.html", "Case study: Lesedi and Letsatsi", "Two 75 MW plant programmes over two years"),
    ("case-ekhaya.html", "Case study: Ekhaya", "One takeaway to twelve shops in Bulawayo"),
  ]),
]

def nav_list(groups):
    out = []
    for label, links in groups:
        if len(links) == 1:
            out.append('<li><a class="nav-link" href="%s">%s</a></li>' % (links[0][0], label)); continue
        out.append('<li class="has-menu"><button class="nav-link" type="button" aria-expanded="false" aria-haspopup="true">%s%s</button><ul class="menu">' % (label, I["chev"]))
        for href, text, small in links:
            out.append('<li><a href="%s">%s<small>%s</small></a></li>' % (href, text, small))
        out.append('</ul></li>')
    return "\n".join(out)

def drawer_list():
    out = []
    for label, links in NAV_LEFT + NAV_RIGHT:
        if len(links) == 1:
            out.append('<li><a class="single" href="%s">%s</a></li>' % (links[0][0], label)); continue
        out.append('<li><button class="group-btn" type="button" aria-expanded="false">%s%s</button><ul class="sub">' % (label, I["chev"]))
        for href, text, _ in links: out.append('<li><a href="%s">%s</a></li>' % (href, text))
        out.append('</ul></li>')
    out.append('<li><a class="single" href="quote.html">Get a quotation</a></li>')
    out.append('<li><a class="single" href="contact.html">Contact</a></li>')
    return "\n".join(out)

def lang_switcher(fname):
    opts = "".join('<li><a data-lang="%s" href="%s" lang="%s" hreflang="%s">%s</a></li>' % (l, (fname if l == "en" else "%s/%s" % (l, fname)), LANG_META[l][0], LANG_META[l][0], LANG_META[l][1]) for l in LANGS)
    return '''<div class="lang has-menu"><button class="region nav-link" type="button" aria-expanded="false" aria-haspopup="true">%s<span class="sr-only">Language</span><span class="txt" data-lang-label>EN</span>%s</button><ul class="menu lang-menu">%s</ul></div>''' % (I["globe"], I["chev"], opts)

def header(fname):
    return '''
<a class="skip" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="bar">
    <div class="hdr-left">
      %(lang)s
      <ul class="nav">%(left)s</ul>
    </div>
    <a class="logo-link" href="index.html" aria-label="Websa Worldwide home"><img src="assets/img/websa-logo.png" width="374" height="298" alt="Websa Worldwide"></a>
    <div class="hdr-right">
      <ul class="nav">%(right)s</ul>
      <button class="search-pill" type="button" data-open-search aria-label="Search the site">%(search)s<span class="txt">Search</span></button>
      <a class="cta-pill" href="quote.html">Get a quotation</a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="drawer" aria-label="Open menu"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>
<nav id="drawer" class="drawer" aria-label="Mobile">
  <ul>%(drawer)s</ul>
  <div class="drawer-cta">
    <a class="btn btn-gold" href="quote.html">Get a quotation</a>
    <a class="btn btn-ghost" href="%(wa)s" rel="noopener" data-wa>WhatsApp %(phone)s</a>
    <button class="btn btn-ghost" type="button" data-open-search>%(search)s Search</button>
  </div>
  <p class="drawer-meta">Guangzhou, China and South Africa. <a href="mailto:%(email)s">%(email)s</a></p>
</nav>
<div class="search-overlay" id="search" role="dialog" aria-modal="true" aria-label="Search" hidden>
  <div class="search-box">
    <form class="search-form" role="search">
      %(search)s
      <label class="sr-only" for="search-input">Search the site</label>
      <input id="search-input" type="search" placeholder="Search pages, brands, projects" autocomplete="off">
      <button type="button" class="icon-btn" data-close-search aria-label="Close search">%(close)s</button>
    </form>
    <p class="search-hint">Try "solar", "diapers", "vehicle importation" or "Guangzhou".</p>
    <ul class="search-results list-reset" aria-live="polite"></ul>
  </div>
</div>
''' % dict(lang=lang_switcher(fname), left=nav_list(NAV_LEFT), right=nav_list(NAV_RIGHT), drawer=drawer_list(), wa=WA, phone=PHONE_DISPLAY, email=EMAIL, search=I["search"], close=I["close"])

def footer():
    addr = "<br>".join(ADDRESS_LINES)
    return '''
<footer class="site-footer">
  <svg class="curve" viewBox="0 0 1440 70" preserveAspectRatio="none" aria-hidden="true"><path d="M0,70 L0,60 Q720,-30 1440,60 L1440,70 Z"/></svg>
  <a class="btn btn-light top-btn" href="#top">Back to top</a>
  <div class="inner">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="assets/img/websa-logo-reversed.png" width="374" height="298" alt="Websa Worldwide" loading="lazy">
        <p>Wealth Building Strategy for All. Registered in Guangzhou, China and in South Africa. Working across Southern Africa since 1999.</p>
      </div>
      <div>
        <h3 class="foot-h">What we do</h3>
        <ul>
          <li><a href="sourcing.html">Import, export and logistics</a></li>
          <li><a href="energy.html">Energy and petroleum</a></li>
          <li><a href="construction.html">Construction, mining and print</a></li>
          <li><a href="agriculture.html">Agriculture</a></li>
          <li><a href="brands.html">Our brands</a></li>
        </ul>
      </div>
      <div>
        <h3 class="foot-h">Company</h3>
        <ul>
          <li><a href="about.html">Who we are</a></li>
          <li><a href="team.html">Leadership and team</a></li>
          <li><a href="projects.html">Projects</a></li>
          <li><a href="case-postmasburg.html">Case studies</a></li>
          <li><a href="contact.html">Contact</a></li>
        </ul>
      </div>
      <div>
        <h3 class="foot-h">Work with us</h3>
        <ul>
          <li><a href="quote.html">Get a quotation</a></li>
          <li><a href="contact.html#suppliers">Suppliers and manufacturers</a></li>
          <li><a href="contact.html#investors">Investors and partners</a></li>
          <li><a href="contact.html#media">Media</a></li>
        </ul>
      </div>
      <div>
        <h3 class="foot-h">Head office</h3>
        <ul class="foot-contact">
          <li>%(pin)s<span>%(addr)s</span></li>
          <li>%(phone_i)s<a href="tel:%(tel)s">%(phone)s</a></li>
          <li>%(mail_i)s<a href="mailto:%(email)s">%(email)s</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <div class="legal">
        <span>&copy; <span data-year>%(year)s</span> Websa Worldwide (Pty) Ltd and Guangzhou Websa Worldwide Co., Ltd</span>
        <a href="legal.html">Legal notice</a>
        <a href="privacy.html">Privacy</a>
      </div>
      <div class="social" aria-label="Social media">
        <a href="https://www.facebook.com/websaworldwide/" rel="noopener" aria-label="Facebook">%(fb)s</a>
        <a href="https://www.instagram.com/websaworldwide.cn/" rel="noopener" aria-label="Instagram">%(ig)s</a>
        <a href="https://www.youtube.com/channel/%(yt_ch)s" rel="noopener" aria-label="YouTube">%(yt)s</a>
        <a href="%(wa)s" rel="noopener" aria-label="WhatsApp" data-wa>%(wa_i)s</a>
      </div>
    </div>
  </div>
</footer>
<aside class="float-wa" aria-label="Quick contact">
  <a class="wa-btn" href="%(wa)s" rel="noopener" data-wa data-track="whatsapp_click">%(wa_i)s<span>Chat on WhatsApp</span></a>
  <a class="call-btn" href="tel:%(tel)s" aria-label="Call Websa Worldwide">%(phone_i)s</a>
</aside>
<div class="video-modal" id="video-modal" role="dialog" aria-modal="true" aria-label="Video player" hidden>
  <div class="video-box"><button type="button" class="icon-btn video-close" data-close-video aria-label="Close video">%(close)s</button><div class="video-frame"></div></div>
</div>
''' % dict(pin=I["pin"], addr=addr, phone_i=I["phone"], tel=PHONE_TEL, phone=PHONE_DISPLAY, mail_i=I["mail"], email=EMAIL, fb=I["fb"], ig=I["ig"], yt=I["yt"], yt_ch=CONFIG["youtube_channel"], wa=WA, wa_i=I["wa"], year=TODAY.year, close=I["close"])

# ---------------------------------------------------------------- structured data and analytics
ORG_LD = {"@type": "Organization", "@id": SITE_URL + "/#org", "name": "Websa Worldwide", "alternateName": ["WEBSA", "Websa Worldwide (Pty) Ltd", "Guangzhou Websa Worldwide Co., Ltd"],
          "url": SITE_URL + "/", "logo": SITE_URL + "/assets/img/websa-logo.png", "slogan": "Wealth Building Strategy for All", "foundingDate": "2024",
          "founder": [{"@type": "Person", "name": "Lazarus Magura"}, {"@type": "Person", "name": "Collins Ndewere"}],
          "address": {"@type": "PostalAddress", "streetAddress": "16 Caiping Road, Suite 412, Building 2, Hesheng Plaza, Huangpu District", "addressLocality": "Guangzhou", "postalCode": "510700", "addressCountry": "CN"},
          "telephone": PHONE_TEL, "email": EMAIL, "areaServed": ["ZA", "ZW", "CN", "MZ", "AO"],
          "sameAs": ["https://www.facebook.com/websaworldwide/", "https://www.instagram.com/websaworldwide.cn/", "https://www.youtube.com/channel/" + CONFIG["youtube_channel"]]}

def breadcrumbs(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE_URL + "/" + (u if u != "index.html" else "")} for i, (n, u) in enumerate(items)]}

def analytics_head():
    a = CONFIG["analytics"]
    if a["provider"] == "plausible" and a.get("plausible_domain"):
        return '<script defer data-domain="%s" src="https://plausible.io/js/script.tagged-events.js"></script><script>window.plausible=window.plausible||function(){(window.plausible.q=window.plausible.q||[]).push(arguments)}</script>' % a["plausible_domain"]
    if a["provider"] == "ga4" and a.get("ga4_id"):
        return ('<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag("consent","default",{analytics_storage:"denied",ad_storage:"denied",ad_user_data:"denied",ad_personalization:"denied"});'
                'try{if(localStorage.getItem("ww-consent")==="granted"){gtag("consent","update",{analytics_storage:"granted"})}}catch(e){}</script>'
                '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script><script>gtag("js",new Date());gtag("config","%s",{anonymize_ip:true});</script>' % (a["ga4_id"], a["ga4_id"]))
    return ""

def consent_banner():
    a = CONFIG["analytics"]
    if a["provider"] != "ga4" or not a.get("ga4_id"): return ""
    return '''<div class="consent" id="consent" role="region" aria-label="Cookie consent" hidden>
  <p>We use Google Analytics to understand which pages and countries our visitors come from. It sets cookies only if you allow it. <a href="privacy.html">Privacy</a></p>
  <div class="btn-row"><button class="btn btn-gold" type="button" data-consent="granted">Allow analytics</button><button class="btn btn-ghost" type="button" data-consent="denied">Decline</button></div>
</div>'''

UI_STRINGS = {
  "showing-all": "Showing all %n", "showing": "Showing %a of %b",
  "form-ok": "Thank you. Your enquiry has been sent. Reference %r. We reply within one working day.",
  "form-mail": "Your email app should now open with the enquiry filled in. If it did not, write to info@websaworldwide.com or use WhatsApp.",
  "form-err": "The enquiry could not be sent. Please try again, email info@websaworldwide.com or use WhatsApp.",
  "search-none": "No results. Try another word.", "search-count": "%n results",
  "wa-hello": "Hello Websa Worldwide.", "wa-page": "I am looking at your page \"%p\".", "wa-ref": "My quotation reference is %r.",
  "pause": "Pause background slideshow", "play": "Play background slideshow",
  "step": "Step %a of %b", "required": "Please complete the highlighted fields.",
}

# ---------------------------------------------------------------- page shell
PAGES = []
def page(fname, title, desc, body, body_class="", extra_head="", ld=None, crumbs=None, search=None, og_title=None):
    graph = [ORG_LD]
    if fname == "index.html":
        graph.append({"@type": "WebSite", "@id": SITE_URL + "/#website", "url": SITE_URL + "/", "name": "Websa Worldwide", "publisher": {"@id": SITE_URL + "/#org"},
                      "inLanguage": ["en", "zh-Hans", "pt"], "potentialAction": {"@type": "SearchAction", "target": SITE_URL + "/?q={search_term_string}", "query-input": "required name=search_term_string"}})
    if crumbs: graph.append(breadcrumbs(crumbs))
    if ld: graph.extend(ld if isinstance(ld, list) else [ld])
    ld_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)
    og = "assets/og/%s.jpg" % fname[:-5]
    url = SITE_URL + "/" + ("" if fname == "index.html" else fname)
    alts = "".join('<link rel="alternate" hreflang="%s" href="%s">' % (LANG_META[l][0], SITE_URL + "/" + ("" if l == "en" else l + "/") + ("" if fname == "index.html" else fname)) for l in LANGS)
    alts += '<link rel="alternate" hreflang="x-default" href="%s">' % url
    ui = " ".join('data-s-%s="%s"' % (k, esc(v)) for k, v in UI_STRINGS.items())
    doc = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="%(url)s">
%(alts)s
<meta property="og:type" content="website">
<meta property="og:site_name" content="Websa Worldwide">
<meta property="og:title" content="%(ogt)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="%(url)s">
<meta property="og:image" content="%(site)s/%(og)s">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#141414">
<link rel="icon" href="favicon.png" type="image/png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="manifest" href="site.webmanifest">
<link rel="preload" href="assets/fonts/montserrat-var-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="css/site.min.css">
<script type="application/ld+json">%(ld)s</script>
%(analytics)s
%(extra)s
</head>
<body id="top" class="%(bc)s" data-page-title="%(short)s" data-form-endpoint="%(endpoint)s" data-analytics="%(prov)s" %(ui)s>
%(header)s
<main id="main">
%(body)s
</main>
%(footer)s
%(consent)s
<script src="js/site.min.js" defer></script>
</body>
</html>
''' % dict(title=esc(title), desc=esc(desc), url=url, alts=alts, ogt=esc(og_title or title), site=SITE_URL, og=og, ld=ld_json, analytics=analytics_head(), extra=extra_head,
           bc=body_class, short=esc(title.split("|")[0].strip()), endpoint=esc(CONFIG["form_endpoint"]), prov=CONFIG["analytics"]["provider"], ui=ui,
           header=header(fname), body=body, footer=footer(), consent=consent_banner())
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f: f.write(doc)
    PAGES.append(dict(fname=fname, title=title.split("|")[0].strip(), desc=desc, og_title=og_title or title.split("|")[0].strip(), search=search or []))
    return fname

# ---------------------------------------------------------------- pages
def home():
    slides = [("assets/img/warehouse.jpg", "Forklift moving pallets inside a distribution warehouse"),
              ("assets/img/harvest.jpg", "Farm workers harvesting vegetables in a field"),
              ("assets/img/solar-farm.jpg", "Rows of solar panels on a utility-scale solar farm"),
              ("assets/img/garment-factory.jpg", "Sewing line inside a garment factory in Guangzhou")]
    slides_html = "".join('<div class="slide%s">%s</div>' % (" is-active" if i == 0 else "", pic(s, a, loading="eager" if i == 0 else "lazy", fetchpriority="high" if i == 0 else None)) for i, (s, a) in enumerate(slides))
    hero_video = next(v for v in VIDEOS if v.get("hero"))
    sector_cards = ""
    for i, s in enumerate(SECTORS):
        sector_cards += '''
      <a class="card reveal d%(d)d%(inv)s" href="%(slug)s.html">
        <div class="circle">%(pic)s</div>
        <div class="meta">%(tag)s</div>
        <h3>%(name)s</h3>
        <p>%(short)s</p>
        <span class="more">Explore %(arrow)s</span>
      </a>''' % dict(d=i % 4, inv=" inverted" if i == 0 else "", slug=s["slug"], pic=pic(s["img"], "", sizes="(max-width: 600px) 60vw, 220px"), tag=s["tag"], name=s["name"], short=s["short"], arrow=I["arrow"])
    tiles = "".join('''
        <a class="tile" href="brands.html#%(slug)s" data-track="brand_click" data-track-name="%(name)s">
          <div class="disc"><img src="%(img)s" alt="%(name)s logo" width="%(w)d" height="%(h)d" loading="lazy"></div>
          <h3>%(name)s</h3><p>%(cat)s</p><span class="pill">View brand</span>
        </a>''' % dict(slug=b["slug"], img=b["img"], name=b["name"], w=b["w"], h=b["h"], cat=b["catname"]) for b in BRANDS)
    proj = "".join(project_li(p, with_note=False) for p in PROJECTS[:5])
    body = '''
<section class="hero" id="intro" aria-label="Introduction">
  <div class="slides">%(slides)s</div>
  <button class="pause" type="button" aria-pressed="false" aria-label="Pause background slideshow">%(pause)s%(play)s</button>
  <div class="inner">
    <span class="kicker"><i></i>Guangzhou &middot; South Africa &middot; Zimbabwe</span>
    <h1>Built in Africa. Connected to China<span class="dot">.</span></h1>
    <p class="lede">Websa Worldwide sources, ships and delivers the equipment, products and projects that build businesses across Southern Africa. One partner from factory floor to hand-over.</p>
    <div class="btn-row">
      <a class="btn btn-gold" href="quote.html">Get a quotation</a>
      <button class="btn btn-ghost" type="button" data-video="%(vid)s" data-video-title="%(vtitle)s" data-track="video_play">%(playi)s Watch our story (%(vdur)s)</button>
    </div>
  </div>
  %(wave)s
</section>

<section class="section" id="mission">
  <div class="content">
    <div class="section-head reveal">
      <span class="eyebrow">Our mission</span>
      <h2>A wealth building strategy for all<span class="dot">.</span></h2>
      <p class="lede">WEBSA began in 1999 as a programme to help Zimbabwean farmers become self-sufficient. Today it is a company registered in Guangzhou and South Africa, applying the same idea to trade, energy, construction and agriculture: find the right partner, procure the right equipment, and train the people who will run it.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="num">1</div><h3>Formulate</h3><p>We turn an idea into a plan with numbers behind it: specification, suppliers, landed cost, timeline and the funding route.</p></div>
      <div class="step reveal d1"><div class="num">2</div><h3>Implement</h3><p>We source, inspect, ship, clear and install. When conditions change mid-project, and they do, our team on the ground adapts without losing the schedule.</p></div>
      <div class="step reveal d2"><div class="num">3</div><h3>Hand over</h3><p>We stay until it runs. Local people are trained to operate and maintain what we deliver, so the value stays in the community.</p></div>
    </div>
  </div>
</section>

<section class="section tint" id="sectors">
  <div class="shell">
    <div class="section-head reveal">
      <span class="eyebrow">What we do</span>
      <h2>Four sectors, one way of working<span class="dot">.</span></h2>
      <p class="lede">Every Websa engagement follows the same discipline, whether the deliverable is a container of equipment, a solar installation or a working farm.</p>
    </div>
    <div class="cards">%(cards)s</div>
    <div class="btn-row center mt-3 reveal"><a class="btn btn-outline" href="services.html">See all services</a></div>
  </div>
</section>

<section class="section" id="brands">
  <div class="shell">
    <div class="section-head reveal">
      <span class="eyebrow">Our brands</span>
      <h2>Products people reach for every day<span class="dot">.</span></h2>
    </div>
    <div class="carousel reveal">
      <div class="track" tabindex="0" aria-label="Brand carousel">%(tiles)s</div>
      <div class="car-controls">
        <button class="arrow prev" type="button" aria-label="Previous brands">%(al)s</button>
        <div class="car-dots" role="group" aria-label="Carousel position"></div>
        <button class="arrow next" type="button" aria-label="Next brands">%(ar)s</button>
      </div>
    </div>
    <div class="btn-row center mt-2 reveal"><a class="btn btn-outline" href="brands.html">Explore the portfolio</a></div>
  </div>
</section>

<section class="section tint" id="difference">
  <div class="shell">
    <div class="band reveal">
      <div class="photo">%(bandpic)s</div>
      <div class="panel on-dark">
        <span class="eyebrow">Making a difference</span>
        <h2>Street lights that taught a town to install them<span class="dot">.</span></h2>
        <p>In Postmasburg, Northern Cape, Websa's programme did more than deliver solar street lighting with Lesedi Solar PV and Philips Lighting. It hired local residents and trained them to do the installation, and went on to run procurement, supply and training for two 75 MW solar plants for two years.</p>
        <a class="btn btn-light" href="case-postmasburg.html">Read the case study</a>
      </div>
    </div>
  </div>
</section>

<section class="section" id="projects">
  <div class="content">
    <div class="section-head reveal">
      <span class="eyebrow">Track record</span>
      <h2>Delivered, not promised<span class="dot">.</span></h2>
      <p class="lede">A selection of projects formulated, procured and executed under the WEBSA programme in South Africa and Zimbabwe.</p>
    </div>
    <ul class="projects list-reset">%(proj)s</ul>
    <div class="btn-row center mt-3 reveal"><a class="btn btn-outline" href="projects.html">See all nine projects</a></div>
  </div>
</section>

<section class="section tint" id="websites">
  <div class="shell">
    <div class="bigcards">
      <a class="bigcard reveal" href="quote.html">
        %(big1)s
        <div class="cap"><h3>Source from China</h3><p>Vehicles, machinery, electronics, textiles and consumer goods, factory-direct and delivered to your door.</p><span class="more">Get a quotation %(ar)s</span></div>
      </a>
      <a class="bigcard reveal d1" href="contact.html#investors">
        %(big2)s
        <div class="cap"><h3>Partner with Websa</h3><p>Investors, suppliers and public bodies who want projects that leave skills behind.</p><span class="more">Talk to us %(ar)s</span></div>
      </a>
    </div>
  </div>
</section>

<nav class="dots-nav" aria-label="Page sections">
  <a href="#intro" aria-label="Intro"><span>Intro</span><i></i></a>
  <a href="#mission" aria-label="Mission"><span>Mission</span><i></i></a>
  <a href="#sectors" aria-label="What we do"><span>What we do</span><i></i></a>
  <a href="#brands" aria-label="Brands"><span>Brands</span><i></i></a>
  <a href="#difference" aria-label="Making a difference"><span>Making a difference</span><i></i></a>
  <a href="#projects" aria-label="Projects"><span>Projects</span><i></i></a>
  <a href="#websites" aria-label="Work with us"><span>Work with us</span><i></i></a>
</nav>

<div class="bottom-bar" aria-label="Quick links">
  <div class="left">
    <div class="bb-group"><button type="button" aria-expanded="false">Partners &amp; buyers %(chev)s</button>
      <div class="bb-pop"><a href="quote.html">Get a quotation</a><a href="contact.html#suppliers">Suppliers and manufacturers</a><a href="contact.html#investors">Investors and partners</a></div></div>
    <div class="bb-group"><button type="button" aria-expanded="false">Our company %(chev)s</button>
      <div class="bb-pop"><a href="about.html">Who we are</a><a href="team.html">Leadership and team</a><a href="brands.html">Brands</a><a href="projects.html">Projects</a></div></div>
  </div>
  <div class="mid">&copy; <span data-year>%(year)s</span> Websa Worldwide</div>
  <div class="right"><a href="contact.html">Contact</a><a href="%(wa)s" rel="noopener" data-wa>WhatsApp %(ext)s</a></div>
</div>
''' % dict(slides=slides_html, pause=I["pause"], play=I["play"], playi=I["playbig"], vid=hero_video["id"], vtitle=esc(hero_video["title"]), vdur=hero_video["dur"], wave=wave(), cards=sector_cards, tiles=tiles, al=I["arrowl"], ar=I["arrow"],
           bandpic=pic("assets/img/solar-farm.jpg", "Solar panels stretching across a plain under a clear sky", sizes="(max-width: 900px) 100vw, 55vw"),
           big1=pic("assets/img/garment-factory.jpg", "", sizes="(max-width: 760px) 100vw, 50vw"), big2=pic("assets/img/helmet-worker.jpg", "", sizes="(max-width: 760px) 100vw, 50vw"),
           proj=proj, chev=I["chev"], wa=WA, ext=I["ext"], year=TODAY.year)
    search = [("Our mission", "index.html#mission", "A wealth building strategy for all. Formulate, implement, hand over."),
              ("What we do", "index.html#sectors", "Four sectors, one way of working"),
              ("Making a difference", "index.html#difference", "Street lights that taught a town to install them")]
    return page("index.html", "Websa Worldwide | Sourcing, trade and projects between China and Africa",
                "Websa Worldwide sources, ships and delivers equipment, products and projects across Southern Africa from Guangzhou, China. Trade, energy, construction and agriculture since 1999.",
                body, body_class="has-bottom-bar", search=search, og_title="Built in Africa. Connected to China.")

def about():
    tl = [("1999", "A programme for farmers", "Lazarus Magura starts WEBSA, Wealth Building Strategy for All, in Zimbabwe: investment sourcing, equipment procurement, training and coaching to make farmers and their value chain self-sufficient and profitable."),
          ("2008", "Adopted in South Africa", "Ndewere Corporation takes up the programme, supplying farming equipment and consulting services to crop farmers in Zimbabwe by partnering with them rather than simply selling to them."),
          ("2014", "Into solar energy", "NDECOR Trading (Pty) Ltd applies the model to energy: solar street lighting in the Northern Cape with Lesedi Solar PV and Philips Lighting. Under Collins Ndewere and Lazarus Magura, local residents are hired and taught to install the lights."),
          ("2014 to 2016", "Two 75 MW solar plants", "NDECOR runs procurement, supply and training for the socio-economic and enterprise development programmes of the Lesedi and Letsatsi solar plants for two years."),
          ("2018", "Ekhaya opens in Bulawayo", "The WEBSA strategy funds the first Ekhaya fast food restaurant in Bulawayo, Zimbabwe. By 2024 the chain is trading from twelve shops."),
          ("2024", "A company of its own", "After twenty-five years as a programme, WEBSA is registered as Guangzhou Websa Worldwide Co., Ltd in the People's Republic of China and as Websa Worldwide (Pty) Ltd in South Africa, with Lazarus Magura and Collins Ndewere as directors and shareholders.")]
    tl_html = "".join('<div class="tl reveal"><div class="year">%s</div><h3>%s</h3><p>%s</p></div>' % t for t in tl)
    values = [(I["shield"], "Integrity", "We hold the highest ethical standards in every operation and every conversation, in Guangzhou and on site."),
              (I["spark"], "Innovation", "We embrace new technology and creative solutions, then make them work in the real conditions our clients face."),
              (I["leaf"], "Sustainability", "We choose practices that protect the environment and leave communities better equipped than we found them."),
              (I["star"], "Excellence", "We aim for the highest quality in our services, our production processes and our relationships."),
              (I["handshake"], "Collaboration", "We build strong partnerships with clients, suppliers and public bodies to reach shared goals.")]
    values_html = "".join('<div class="value reveal"><div class="ico">%s</div><h3>%s</h3><p>%s</p></div>' % v for v in values)
    body = page_hero(I["book"], "Who we are", "Making wealth building work for everyone",
        "Websa Worldwide is a South African and Chinese company with Zimbabwean roots, built on a simple idea that has held for twenty-five years: give people the equipment, the partners and the skills, and they will build wealth for themselves.",
        "assets/img/helmet-worker.jpg", "Engineer in a hard hat and high-visibility vest") + '''
<section class="section">
  <div class="content">
    <div class="split">
      <div class="pic round reveal">%(pic1)s</div>
      <div class="reveal d1">
        <span class="eyebrow">The idea</span>
        <h2>WEBSA stands for Wealth Building Strategy for All<span class="dot">.</span></h2>
        <p>The name is older than the company. It began in Zimbabwe in 1999 as a programme designed to help farmers and the agricultural value chain become self-sufficient and profitable, through investment sourcing, procurement of equipment, and training and coaching.</p>
        <p>The same strategy was later applied to solar energy in South Africa's Northern Cape, to equipment supply for crop farmers, and to a fast food chain in Bulawayo. In early 2024 it became a company in its own right, registered in Guangzhou, China and in South Africa.</p>
        <p>Websa develops strategies for the public sector, private companies and non-profit organisations, and implements customised solutions with world-class professionalism and expertise.</p>
      </div>
    </div>
  </div>
</section>
<section class="section tint" id="timeline">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">Our history</span><h2>Twenty-five years, one strategy<span class="dot">.</span></h2></div>
    <div class="timeline">%(tl)s</div>
  </div>
</section>
<section class="section">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">Two entities, one team</span><h2>Registered where the work is<span class="dot">.</span></h2></div>
    <div class="grid grid-2">
      <div class="feature reveal"><div class="ico">%(globe)s</div><div><h3>Guangzhou Websa Worldwide Co., Ltd</h3><p>Our head office in Huangpu District, Guangzhou, sits in the manufacturing heart of southern China. From here we visit factories, inspect goods and consolidate shipments.</p></div></div>
      <div class="feature reveal d1"><div class="ico">%(pin)s</div><div><h3>Websa Worldwide (Pty) Ltd</h3><p>Registered in South Africa, the base for project delivery, client relationships and after-sales support across Southern Africa.</p></div></div>
    </div>
    <div class="grid grid-2 mt-2">
      <div class="feature reveal"><div class="ico">%(grid)s</div><div><h3>Departments</h3><p>Agriculture. Technology and methodology in energy, electricity and alternative energy. Trading. Funding solutions.</p></div></div>
      <div class="feature reveal d1"><div class="ico">%(tag)s</div><div><h3>Services</h3><p>International trade, business advisory, technical consultancy, project management, import and export, training and skills development.</p></div></div>
    </div>
  </div>
</section>
<section class="section tint" id="values">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">Our values</span><h2>What we hold ourselves to<span class="dot">.</span></h2></div>
    <div class="values">%(values)s</div>
  </div>
</section>
<section class="section" id="leadership">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">Leadership</span><h2>The directors<span class="dot">.</span></h2>
      <p class="lede">Websa Worldwide is owned and directed by the two people who have run the WEBSA programme since its earliest projects.</p></div>
    <div class="people">
      <div class="person reveal"><div class="avatar" aria-hidden="true">LM</div><h3>Lazarus Magura</h3><div class="role">Founding director</div><p>Started the WEBSA programme in Zimbabwe in 1999 and has led its agricultural, equipment and energy projects since.</p></div>
      <div class="person reveal d1"><div class="avatar" aria-hidden="true">CN</div><h3>Collins Ndewere</h3><div class="role">Director</div><p>Brought the programme to South Africa through Ndewere Corporation and NDECOR Trading, and directed the Northern Cape solar work.</p></div>
    </div>
    <div class="btn-row center mt-3 reveal"><a class="btn btn-outline" href="team.html">Meet the team</a></div>
  </div>
</section>
<section class="section tint">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">Why clients choose Websa</span><h2>Four reasons<span class="dot">.</span></h2></div>
    <div class="features">
      <div class="feature reveal"><div class="ico">%(users)s</div><div><h3>Expertise</h3><p>Seasoned professionals with diverse backgrounds in project management, able to take on projects of any scale.</p></div></div>
      <div class="feature reveal d1"><div class="ico">%(spark)s</div><div><h3>Tailored solutions</h3><p>Every project is different. We take the time to understand your specific needs and shape our services to fit.</p></div></div>
      <div class="feature reveal d2"><div class="ico">%(handshake)s</div><div><h3>A client-centred approach</h3><p>Your objectives come first. We work alongside you, building partnerships on trust and mutual respect.</p></div></div>
      <div class="feature reveal d3"><div class="ico">%(leaf)s</div><div><h3>Sustainability</h3><p>Sustainable practice on every project, with a positive impact on the communities and environments we work in.</p></div></div>
    </div>
  </div>
</section>
''' % dict(pic1=pic("assets/img/harvest.jpg", "Farm workers harvesting vegetables", sizes="(max-width: 900px) 100vw, 45vw"), tl=tl_html, globe=I["globe"], pin=I["pin"], grid=I["grid"], tag=I["tag"], values=values_html, users=I["users"], spark=I["spark"], handshake=I["handshake"], leaf=I["leaf"]) + cta_strip("Ready to build something that lasts?", "Tell us what you need to source, build or grow. We reply within one working day.", secondary=("projects.html", "See our projects"))
    search = [("Our history", "about.html#timeline", "Twenty-five years, one strategy: 1999 to 2024"), ("Our values", "about.html#values", "Integrity, innovation, sustainability, excellence, collaboration"), ("Leadership", "about.html#leadership", "Lazarus Magura and Collins Ndewere")]
    return page("about.html", "Who we are | Websa Worldwide", "Websa Worldwide's story: from a 1999 farming programme in Zimbabwe to a company registered in Guangzhou and South Africa. History, values and leadership.",
                body, ld={"@type": "AboutPage", "name": "Who we are", "url": SITE_URL + "/about.html"}, crumbs=[("Home", "index.html"), ("Who we are", "about.html")], search=search)

def team():
    people = ""
    for i, t in enumerate(TEAM):
        ini = "".join(p[0] for p in t["name"].split()[:2])
        photo = ('<div class="photo-slot">%s</div>' % pic(t["photo"], t["name"], sizes="120px")) if t.get("photo") else '<div class="avatar" aria-hidden="true">%s</div>' % ini
        people += '<div class="person reveal d%d">%s<h3>%s</h3><div class="role">%s</div><p class="office-line">%s</p><p>%s</p></div>' % (i % 4, photo, t["name"], t["role"], t["office"], t["bio"])
    body = page_hero(I["users"], "Leadership and team", "The people behind the programme",
        "Two directors who have run the WEBSA programme since its first projects, and two offices that between them cover the whole route from a factory in Guangdong to a site in Southern Africa.",
        "assets/img/garment-factory.jpg", "Sewing line inside a Guangzhou factory") + '''
<section class="section">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">Directors</span><h2>Owners who still run the projects<span class="dot">.</span></h2></div>
    <div class="people">%(people)s</div>
  </div>
</section>
<section class="section tint">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">Two offices</span><h2>Who does what<span class="dot">.</span></h2>
      <p class="lede">Every enquiry is handled by a named person at the end of the route where the work is. Ask for an introduction and you will get a name and a direct number.</p></div>
    <div class="grid grid-2">
      <div class="office-card reveal">
        <div class="ico">%(globe)s</div>
        <h3>Guangzhou, China</h3>
        <p class="office-line">Guangzhou Websa Worldwide Co., Ltd, Huangpu District</p>
        %(gz)s
      </div>
      <div class="office-card reveal d1">
        <div class="ico">%(pin)s</div>
        <h3>South Africa</h3>
        <p class="office-line">Websa Worldwide (Pty) Ltd</p>
        %(za)s
      </div>
    </div>
  </div>
</section>
''' % dict(people=people, globe=I["globe"], pin=I["pin"],
           gz=checks(["Supplier search and factory visits across Guangdong and beyond", "Quality inspection before payment and before shipping", "Consolidation of mixed orders into one shipment", "Export documentation and freight booking by air, sea or road"]),
           za=checks(["Project formulation, funding routes and client relationships", "Customs clearance and delivery to site, warehouse or showroom", "Installation, commissioning and operator training", "After-sales support and spare parts"])) + cta_strip("Want to speak to a person, not a form?", "Call or message the head office and ask for a director.", primary=("contact.html", "Contact us"), secondary=("quote.html", "Get a quotation"))
    return page("team.html", "Leadership and team | Websa Worldwide", "Meet Websa Worldwide's directors, Lazarus Magura and Collins Ndewere, and the Guangzhou and South Africa offices that deliver sourcing, shipping, installation and training.",
                body, crumbs=[("Home", "index.html"), ("Who we are", "about.html"), ("Leadership and team", "team.html")],
                ld=[{"@type": "Person", "name": t["name"], "jobTitle": t["role"], "worksFor": {"@id": SITE_URL + "/#org"}} for t in TEAM],
                search=[(t["name"], "team.html", t["role"] + ". " + t["bio"]) for t in TEAM])

def services():
    blocks = ""
    for i, s in enumerate(SECTORS):
        blocks += '''
<section class="section%(tint)s" id="%(slug)s">
  <div class="content">
    <div class="split%(flip)s">
      <div class="pic reveal">%(pic)s</div>
      <div class="reveal d1">
        <span class="eyebrow">%(tag)s</span>
        <h2>%(name)s<span class="dot">.</span></h2>
        <p class="lede">%(short)s</p>
        <a class="btn btn-primary" href="%(slug)s.html">Explore %(arrow)s</a>
      </div>
    </div>
  </div>
</section>''' % dict(tint=" tint" if i % 2 else "", slug=s["slug"], flip=" flip" if i % 2 else "", pic=pic(s["img"], s["alt"], sizes="(max-width: 900px) 100vw, 50vw"), tag=s["tag"], name=s["name"], short=s["short"], arrow=I["arrow"])
    body = page_hero(I["grid"], "What we do", "Four sectors. One discipline.",
        "Websa formulates, implements and executes projects for the public sector, private companies and non-profit organisations. Whatever the sector, the same team handles specification, sourcing, funding routes, delivery and training.",
        "assets/img/logistics-holo.jpg", "Shipping containers, trucks and aircraft representing global logistics") + '''
<section class="section">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">How we work</span><h2>From an idea to a running asset<span class="dot">.</span></h2></div>
    <div class="steps">
      <div class="step reveal"><div class="num">1</div><h3>Project formulation</h3><p>We work closely with you to develop the idea into a viable, costed plan: specification, suppliers, landed cost, timeline and funding route.</p></div>
      <div class="step reveal d1"><div class="num">2</div><h3>Project implementation</h3><p>A hands-on approach that adapts quickly to whatever the project throws up, from a factory delay to a customs query.</p></div>
      <div class="step reveal d2"><div class="num">3</div><h3>Project execution</h3><p>We deliver, install and train, and we measure ourselves against results that exceed what was promised.</p></div>
    </div>
  </div>
</section>
''' + blocks + '''
<section class="section">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">Also available</span><h2>Advisory and support services<span class="dot">.</span></h2></div>
    <div class="features">
      <div class="feature reveal"><div class="ico">%(chat)s</div><div><h3>Business advisory</h3><p>Market entry, supplier strategy and the funding routes open to African businesses buying from China.</p></div></div>
      <div class="feature reveal d1"><div class="ico">%(spark)s</div><div><h3>Technical consultancy</h3><p>Specification, factory audits and quality inspection before anything is paid for or shipped.</p></div></div>
      <div class="feature reveal d2"><div class="ico">%(grid)s</div><div><h3>Project management</h3><p>One accountable team from purchase order to commissioning, with reporting you can put in front of a board.</p></div></div>
      <div class="feature reveal d3"><div class="ico">%(users)s</div><div><h3>Training and skills development</h3><p>Operators, installers and maintenance teams trained on site, so the asset keeps working after we leave.</p></div></div>
    </div>
  </div>
</section>
''' % dict(chat=I["chat"], spark=I["spark"], grid=I["grid"], users=I["users"]) + cta_strip("Not sure which service you need?", "Describe the outcome you want. We will tell you honestly what it takes and what it costs.")
    return page("services.html", "What we do | Websa Worldwide", "Import, export and logistics, energy and petroleum, construction, mining, signage and print, and agriculture. How Websa Worldwide formulates, implements and executes projects.",
                body, crumbs=[("Home", "index.html"), ("What we do", "services.html")], search=[(s["name"], "services.html#" + s["slug"], s["short"]) for s in SECTORS])

def video_reel():
    cards = "".join('''
      <button class="vcard reveal d%(d)d" type="button" data-video="%(id)s" data-video-title="%(t)s" data-track="video_play">
        %(pic)s<span class="vplay">%(play)s</span><span class="vtitle">%(t)s</span>%(dur)s
      </button>''' % dict(d=i % 4, id=v["id"], t=esc(v["title"]), pic=pic(v["thumb"], "", sizes="(max-width: 700px) 100vw, 25vw"), play=I["playbig"], dur=('<span class="vdur">%s</span>' % v["dur"]) if v["dur"] else "") for i, v in enumerate(VIDEOS))
    return '''
<section class="section tint" id="reel">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">From the factory floor</span><h2>See the sourcing route for yourself<span class="dot">.</span></h2>
      <p class="lede">Short films from our Guangzhou team. Videos load from YouTube only when you press play.</p></div>
    <div class="vgrid">%s</div>
  </div>
</section>''' % cards

def sector_page(slug, title, sub, lede, img, alt, icon, intro_h, intro_p, offers, offers_h, side_h, side_items, side_img, side_alt, proj_sectors, extra=""):
    offers_html = "".join('<div class="feature reveal"><div class="ico">%s</div><div><h3>%s</h3><p>%s</p></div></div>' % (I["check"], h, p) for h, p in offers)
    projs = [p for p in PROJECTS if p["sector"] in proj_sectors]
    proj_section = '''
<section class="section tint">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">Delivered</span><h2>Related projects<span class="dot">.</span></h2></div>
    <ul class="projects list-reset">%s</ul>
    <div class="btn-row center mt-3 reveal"><a class="btn btn-outline" href="projects.html">See the full track record</a></div>
  </div>
</section>''' % "".join(project_li(p, with_note=False) for p in projs) if projs else ""
    body = page_hero(icon, title, sub, lede, img, alt) + '''
<section class="section">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">Overview</span><h2>%(ih)s<span class="dot">.</span></h2><p class="lede">%(ip)s</p></div>
    <h3 class="center reveal" style="margin-bottom:22px">%(oh)s</h3>
    <div class="features">%(offers)s</div>
  </div>
</section>
<section class="section dark">
  <div class="content">
    <div class="split">
      <div class="pic reveal">%(spic)s</div>
      <div class="reveal d1">
        <span class="eyebrow">Why Websa</span>
        <h2>%(sh)s<span class="dot">.</span></h2>
        %(checks)s
        <a class="btn btn-gold" href="quote.html">Get a quotation</a>
      </div>
    </div>
  </div>
</section>
%(extra)s
%(proj)s
''' % dict(ih=intro_h, ip=intro_p, oh=offers_h, offers=offers_html, spic=pic(side_img, side_alt, sizes="(max-width: 900px) 100vw, 50vw"), sh=side_h, checks=checks(side_items), extra=extra, proj=proj_section) + cta_strip("Tell us what you need.", "Send a specification, a photo or a rough idea. We will come back with suppliers, a landed cost and a timeline.")
    ld = {"@type": "Service", "name": title, "serviceType": title, "provider": {"@id": SITE_URL + "/#org"}, "areaServed": ["ZA", "ZW", "MZ", "AO", "CN"], "description": lede}
    return page(slug + ".html", title + " | Websa Worldwide", first_sentences(lede), body, ld=ld, crumbs=[("Home", "index.html"), ("What we do", "services.html"), (title, slug + ".html")],
                search=[(h, slug + ".html", p) for h, p in offers])

def sourcing():
    extra = '''
<section class="section">
  <div class="content">
    <div class="section-head reveal"><span class="eyebrow">How sourcing works</span><h2>From your brief to your door<span class="dot">.</span></h2></div>
    <div class="steps">
      <div class="step reveal"><div class="num">1</div><h3>Brief and quotation</h3><p>You tell us what you need. We shortlist factories, check them, and quote a landed cost that includes freight, duties and clearance, not just the factory price.</p></div>
      <div class="step reveal d1"><div class="num">2</div><h3>Inspection and shipping</h3><p>Our Guangzhou team inspects the goods before they leave, consolidates your order and books air, sea or road freight to suit the budget and the deadline.</p></div>
      <div class="step reveal d2"><div class="num">3</div><h3>Clearance and delivery</h3><p>We handle documentation and customs at the destination and deliver to your warehouse, site or showroom, with training where the goods need it.</p></div>
    </div>
    <div class="grid grid-4 mt-3">
      <div class="value reveal"><div class="ico">%(ship)s</div><h3>Automobiles</h3><p>Vehicles sourced from China, Japan, Singapore and Durban.</p></div>
      <div class="value reveal d1"><div class="ico">%(spark)s</div><h3>Electronics</h3><p>Consumer and commercial electronics, factory-direct.</p></div>
      <div class="value reveal d2"><div class="ico">%(tag)s</div><h3>Textiles</h3><p>Garments and fabric from inspected Guangzhou factories.</p></div>
      <div class="value reveal d3"><div class="ico">%(crane)s</div><h3>Machinery</h3><p>Farming, mining and construction equipment with spares.</p></div>
    </div>
    <div class="btn-row center mt-3 reveal"><a class="btn btn-gold" href="quote.html">Start a quotation request</a></div>
  </div>
</section>''' % dict(ship=I["ship"], spark=I["spark"], tag=I["tag"], crane=I["crane"]) + video_reel()
    return sector_page("sourcing", "Import, export and logistics", "Factory-direct from China. Delivered in Africa.",
        "Websa connects businesses across borders and optimises their supply chains. From our Guangzhou office we source vehicles, machinery, electronics, textiles and consumer goods, then manage the documentation, freight and customs so the goods arrive on time and on budget.",
        "assets/img/warehouse-trucks.jpg", "Trucks loading at a logistics warehouse", I["ship"],
        "Seamless international trade", "Years of experience connecting African buyers with Chinese manufacturers, and the logistics discipline to make each shipment efficient and cost-effective.",
        [("Import and export services", "We manage the complexity of international trade: regulatory compliance, documentation and customs procedures, so transactions run smoothly."),
         ("Logistics management", "Warehousing, transportation and distribution designed to optimise your supply chain and improve delivery performance."),
         ("Freight forwarding", "Air, sea and land freight tailored to your cargo, budget and deadline."),
         ("Customs clearance", "An experienced team that navigates customs procedures for timely, efficient clearance of every shipment."),
         ("Supply chain solutions", "Strategic insight and tailored solutions that reduce cost and improve operational efficiency across your chain.")],
        "Services offered", "One accountable partner, both ends of the route",
        ["A registered company in Guangzhou and in South Africa, with staff at both ends of the route.",
         "Factory inspections before payment, not photographs after shipping.",
         "Landed-cost quotations that include freight, insurance, duties and clearance.",
         "Vehicles, farming equipment and mining equipment already delivered for clients in the region."],
        "assets/img/garment-factory.jpg", "Sewing line inside a Guangzhou garment factory", ["trade"], extra)

def energy():
    extra = '''<section class="section"><div class="shell"><div class="section-head reveal"><span class="eyebrow">Case studies</span><h2>Read how it was done<span class="dot">.</span></h2></div>
<div class="grid grid-2" style="max-width:820px;margin:0 auto">%s</div></div></section>''' % "".join(case_card(c, i) for i, c in enumerate(CASES[:2]))
    return sector_page("energy", "Energy and petroleum", "Sustainable power. Reliable supply.",
        "Websa delivers sustainable and innovative energy solutions for clients and the environment. Our track record runs from solar street lighting in the Northern Cape to two years of programme delivery for two 75 MW solar plants, with a focus on excellence, safety and integrity.",
        "assets/img/solar-farm.jpg", "Solar farm under a bright sky", I["bolt"],
        "A trusted partner in the energy market", "From alternative energy and electricity to petroleum supply, Websa's energy department combines technology and methodology with the WEBSA principle: train local people to install and maintain what we deliver.",
        [("Solar street lighting", "Procurement and installation of solar street lights for municipalities and mines, with local residents trained as installers."),
         ("Utility-scale programme delivery", "Procurement, supply and training for the socio-economic and enterprise development commitments of large solar plants."),
         ("Electricity and alternative energy", "Technology and methodology for reliable power where the grid is weak or absent."),
         ("Petroleum supply", "Sourcing and supply of fuel and petroleum products for commercial and industrial clients."),
         ("Training and skills transfer", "Every installation leaves behind people who can operate and maintain it.")],
        "What we deliver", "Values we are held to on every site",
        ["Integrity: the highest ethical standards in every operation and interaction.",
         "Innovation: technology and creative solutions that improve what we deliver.",
         "Sustainability: environmentally responsible practice that protects the planet for the next generation.",
         "Excellence: the highest quality in service, production and customer relations.",
         "Collaboration: strong partnerships with stakeholders to reach shared goals."],
        "assets/img/factory.jpg", "Modern manufacturing equipment in a clean factory hall", ["energy"], extra)

def construction():
    return sector_page("construction", "Construction, mining, signage and print", "Build it. Extract it. Put your name on it.",
        "Websa is a multifaceted organisation specialising in construction, mining, signage and digital printing. Our commitment to excellence and innovation drives us to deliver top-quality solutions tailored to the diverse needs of our clients.",
        "assets/img/construction.jpg", "Excavator and construction crew on a building site", I["crane"],
        "Four trades, one standard", "Whether the job is a building, a mine site, a fleet of signs or a print run, the same project discipline applies: clear specification, the right equipment, safety and environmental compliance, and delivery on time.",
        [("Construction", "Comprehensive building and infrastructure development, with project management and consultation."),
         ("Mining", "Mineral extraction and resource management, with safety and environmental compliance built in."),
         ("Mining and construction equipment", "Sourcing and supply of heavy equipment and spares from inspected manufacturers."),
         ("Signage", "Custom signage for businesses, the public sector, non-profits and events, including installation and maintenance."),
         ("Digital printing", "High-quality digital printing for every application, with fast turnaround and competitive pricing.")],
        "Core services", "Why clients bring us their sites and their storefronts",
        ["A R52.8 million digital printing and signage programme delivered.",
         "R20 million of farming and mining equipment supplied to operators in Zimbabwe and South Africa.",
         "Blue Digital Printing, our own print and signage brand, in the portfolio.",
         "Safety and environmental compliance treated as part of the specification, not an afterthought."],
        "assets/img/mining.jpg", "Worker beside a bulldozer in a sand quarry", ["print", "trade", "health"])

def agriculture():
    extra = '''
<section class="section">
  <div class="content">
    <div class="grid grid-2">
      <div class="feature reveal"><div class="ico">%(star)s</div><div><h3>Vision</h3><p>To be recognised as a premier agricultural company that drives transformation in Africa's agricultural sector, ensuring sustainable food production, the empowerment of local communities and environmental stewardship.</p></div></div>
      <div class="feature reveal d1"><div class="ico">%(leaf)s</div><div><h3>Mission</h3><p>To provide high-quality agricultural products and services that promote food security, enhance rural livelihoods and support sustainable farming, fostering the partnerships and practices that secure a healthy food supply for Africa.</p></div></div>
    </div>
  </div>
</section>''' % dict(star=I["star"], leaf=I["leaf"])
    return sector_page("agriculture", "Agriculture", "Where WEBSA began.",
        "Websa Agriculture is dedicated to enhancing the agricultural landscape of the African continent: food security and sustainable practice through innovative crop and livestock farming, high-quality seed manufacturing and a commitment to community development.",
        "assets/img/harvest.jpg", "Farm workers harvesting vegetables", I["leaf"],
        "Farming as a business", "The WEBSA programme started in 1999 with one aim: make farmers and their value chain self-sufficient and profitable. Twenty-five years on, that is still the measure of every agricultural project we take on.",
        [("Crop farming", "Innovative crop production with the equipment, inputs and agronomy support to lift yields."),
         ("Livestock farming", "Livestock projects delivered as investments, from stock and infrastructure to husbandry training."),
         ("Seed manufacturing", "High-quality seed produced for African conditions."),
         ("Equipment and inputs", "Farming equipment sourced and supplied, with financing routes and operator training."),
         ("Community development", "Rural livelihoods improved through partnership, skills and market access.")],
        "What we do", "A programme with a quarter-century of results",
        ["Farming equipment and consulting delivered to crop farmers in Zimbabwe since 2008.",
         "A US$200,000 livestock project delivered in Zimbabwe.",
         "R20 million of farming and mining equipment supplied.",
         "Training and coaching built into every engagement, from the first project in 1999."],
        "assets/img/highway-truck.jpg", "Truck on a highway at sunset", ["agriculture", "trade"], extra)

def brands():
    cats = [("auto", "Automotive"), ("baby", "Baby care"), ("consumer", "Everyday essentials"), ("energy", "Energy"), ("print", "Signage and print"), ("other", "More Websa brands")]
    radios = '<label><input type="radio" name="cat" value="all" checked> All brands</label>' + "".join('<label><input type="radio" name="cat" value="%s"> %s</label>' % c for c in cats)
    tiles = "".join('''
        <article class="tile" id="%(slug)s" data-item data-cat="%(cat)s">
          <div class="disc"><img src="%(img)s" alt="%(name)s logo" width="%(w)d" height="%(h)d" loading="lazy"></div>
          <h3>%(name)s</h3><p>%(line)s</p><a class="pill" href="quote.html?type=Brand+enquiry&amp;brand=%(name)s" data-track="brand_click" data-track-name="%(name)s">Enquire</a>
        </article>''' % b for b in BRANDS)
    body = page_hero(I["tag"], "Our brands", "Products people reach for every day",
        "Alongside its project and trading work, Websa Worldwide owns and develops ten consumer and commercial brands for African markets.",
        "assets/img/import-export.jpg", "Export and import shipping containers") + '''
<section class="section">
  <div class="shell">
    <div class="filter-layout" data-filter-root>
      <aside class="filters" aria-label="Filter brands">
        <h2>Filter</h2>
        <div class="search"><label class="sr-only" for="brand-q">Search brands</label><input id="brand-q" type="search" placeholder="Search here" data-search>%(search)s</div>
        <div role="radiogroup" aria-label="Category">%(radios)s</div>
        <button class="btn btn-outline clear" type="button" data-clear style="min-height:40px;padding:8px 18px">Clear</button>
      </aside>
      <div>
        <p class="results-note" data-results aria-live="polite"></p>
        <section class="brand-group" data-group><h2>All brands</h2><div class="brand-grid">%(tiles)s</div></section>
        <div class="empty hidden" data-empty>No brands match that search.</div>
      </div>
    </div>
  </div>
</section>
''' % dict(search=I["search"], radios=radios, tiles=tiles) + cta_strip("Interested in stocking or distributing a Websa brand?", "We work with retailers, wholesalers and distributors across Southern Africa.", primary=("quote.html?type=Brand+enquiry", "Enquire about a brand"))
    ld = {"@type": "ItemList", "name": "Websa Worldwide brands", "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Brand", "name": b["name"], "url": SITE_URL + "/brands.html#" + b["slug"], "logo": SITE_URL + "/" + b["img"], "description": b["line"]}} for i, b in enumerate(BRANDS)]}
    return page("brands.html", "Our brands | Websa Worldwide", "The Websa Worldwide brand portfolio: Kudus, Runningman, Blue Digital Printing, Sandie's Happy Basket, Zarus, Benny Yamin, Wakanaka, Stewart, Bigman Autospares and EnergyOn.",
                body, ld=ld, crumbs=[("Home", "index.html"), ("Our brands", "brands.html")], search=[(b["name"], "brands.html#" + b["slug"], b["line"]) for b in BRANDS])

def projects():
    sectors = sorted(set((p["sector"], p["sectorname"]) for p in PROJECTS), key=lambda x: x[1])
    places = [("sa", "South Africa"), ("zw", "Zimbabwe")]
    radios_s = '<label><input type="radio" name="sector" value="all" checked> All sectors</label>' + "".join('<label><input type="radio" name="sector" value="%s"> %s</label>' % s for s in sectors)
    radios_p = '<label><input type="radio" name="place" value="all" checked> Anywhere</label>' + "".join('<label><input type="radio" name="place" value="%s"> %s</label>' % p for p in places)
    rows = "".join(project_li(p) for p in PROJECTS)
    total_r = sum(p["val"] for p in PROJECTS if p["cur"] == "R"); total_d = sum(p["val"] for p in PROJECTS if p["cur"] == "$")
    fmt = lambda v: "{:.1f}".format(v / 1e6).rstrip("0").rstrip(".")
    body = page_hero(I["star"], "Projects", "Delivered, not promised",
        "Nine projects formulated, procured and executed under the WEBSA programme in South Africa and Zimbabwe, across trade, energy, health, retail, print and agriculture.",
        "assets/img/construction.jpg", "Construction site with heavy machinery") + '''
<section class="section">
  <div class="shell">
    <div class="stat-row" style="margin:0 0 48px">
      <div class="stat reveal"><div class="n">9</div><div class="l">projects delivered in South Africa and Zimbabwe</div></div>
      <div class="stat reveal d1"><div class="n">R%(tr)s m</div><div class="l">combined value of rand-denominated projects</div></div>
      <div class="stat reveal d2"><div class="n">US$%(td)s m</div><div class="l">combined value of dollar-denominated projects</div></div>
    </div>
    <div class="section-head reveal" style="margin-bottom:28px"><span class="eyebrow">Case studies</span><h2>Three projects in depth<span class="dot">.</span></h2></div>
    <div class="grid grid-3" style="margin-bottom:56px">%(cases)s</div>
    <div class="filter-layout" data-filter-root>
      <aside class="filters" aria-label="Filter projects">
        <h2>Filter</h2>
        <div role="radiogroup" aria-label="Sector">%(rs)s</div>
        <hr class="rule">
        <div role="radiogroup" aria-label="Country">%(rp)s</div>
        <button class="btn btn-outline clear" type="button" data-clear style="min-height:40px;padding:8px 18px">Clear</button>
      </aside>
      <div>
        <p class="results-note" data-results aria-live="polite"></p>
        <ul class="projects list-reset" data-group>%(rows)s</ul>
        <div class="empty hidden" data-empty>No projects match those filters.</div>
        <p class="fineprint">Project values are as reported by Websa Worldwide. SED and ED are the socio-economic development and enterprise development programmes that South African renewable energy plants are required to fund.</p>
      </div>
    </div>
  </div>
</section>
''' % dict(tr=fmt(total_r), td=fmt(total_d), cases="".join(case_card(c, i) for i, c in enumerate(CASES)), rs=radios_s, rp=radios_p, rows=rows) + cta_strip("Have a project like these?", "We formulate, fund-route, procure and execute. Start with a conversation.", primary=("contact.html", "Start a conversation"))
    return page("projects.html", "Projects | Websa Worldwide", "Websa Worldwide's track record: solar programmes in the Northern Cape, equipment supply, vehicle importation, medical supplies, restaurants in Bulawayo and a R52.8 million print and signage programme.",
                body, crumbs=[("Home", "index.html"), ("Projects", "projects.html")], search=[(p["name"], "projects.html", p["where"] + ". " + p["note"]) for p in PROJECTS])

def case_page(c):
    quote = ('<blockquote class="pull reveal"><p>%s</p><footer>%s</footer></blockquote>' % (c["quote"], c["quote_by"])) if c.get("quote") else ""
    rel = []
    for r in c["related"]:
        other = next((x for x in CASES if x["slug"] + ".html" == r), None)
        if other: rel.append(case_card(other, len(rel)))
        else:
            s = next(x for x in SECTORS if x["slug"] + ".html" == r)
            rel.append('<a class="card reveal d%d" href="%s"><div class="circle">%s</div><div class="meta">%s</div><h3>%s</h3><p>%s</p><span class="more">Explore %s</span></a>' % (len(rel), r, pic(s["img"], "", sizes="220px"), s["tag"], s["name"], s["short"], I["arrow"]))
    body = page_hero(I["doc"], c["title"], c["short"], "", c["img"], c["alt"]) + '''
<section class="section">
  <div class="content">
    <dl class="glance reveal">
      <div><dt>Sector</dt><dd>%(sector)s</dd></div>
      <div><dt>Where</dt><dd>%(place)s</dd></div>
      <div><dt>When</dt><dd>%(when)s</dd></div>
      <div><dt>Project value</dt><dd>%(value)s</dd></div>
      <div class="wide"><dt>Partners</dt><dd>%(partners)s</dd></div>
    </dl>
    <div class="prose">
      <h2>The brief<span class="dot">.</span></h2>
      <p>%(brief)s</p>
      <h2>What Websa did<span class="dot">.</span></h2>
      %(did)s
      <h2>The result<span class="dot">.</span></h2>
      <p>%(result)s</p>
      %(quote)s
    </div>
  </div>
</section>
<section class="section tint">
  <div class="shell">
    <div class="section-head reveal"><span class="eyebrow">Keep reading</span><h2>Related<span class="dot">.</span></h2></div>
    <div class="grid grid-2" style="max-width:820px;margin:0 auto">%(rel)s</div>
  </div>
</section>
''' % dict(sector=c["sector"], place=c["place"], when=c["when"], value=c["value"], partners=c["partners"], brief=c["brief"], did=checks(c["did"], big=True), result=c["result"], quote=quote, rel="".join(rel)) + cta_strip("Have a project like this one?", "We formulate, fund-route, procure and execute. Start with a conversation.", primary=("contact.html", "Start a conversation"), secondary=("projects.html", "All projects"))
    ld = {"@type": "Article", "headline": c["title"], "description": c["brief"][:200], "image": SITE_URL + "/" + c["img"], "author": {"@id": SITE_URL + "/#org"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": SITE_URL + "/" + c["slug"] + ".html"}
    return page(c["slug"] + ".html", c["title"] + " | Websa Worldwide", first_sentences(c["short"] + ". " + c["brief"]), body, ld=ld,
                crumbs=[("Home", "index.html"), ("Projects", "projects.html"), (c["title"], c["slug"] + ".html")], search=[(c["title"], c["slug"] + ".html", c["short"] + ". " + c["result"])])

def quote():
    cats = [("vehicles", I["ship"], "Vehicles", "Cars, bakkies, trucks, buses, motorcycles"),
            ("machinery", I["crane"], "Machinery and equipment", "Farming, mining, construction, workshop"),
            ("electronics", I["spark"], "Electronics", "Consumer, commercial, telecoms"),
            ("textiles", I["tag"], "Textiles and apparel", "Garments, fabric, workwear, uniforms"),
            ("building", I["grid"], "Building materials", "Tiles, fittings, steel, glass, fixtures"),
            ("solar", I["bolt"], "Solar and power", "Panels, inverters, batteries, street lights"),
            ("consumer", I["star"], "Consumer goods", "Household, baby care, personal care"),
            ("other", I["chat"], "Something else", "Tell us in the next step")]
    cat_html = "".join('<label class="choice"><input type="radio" name="category" value="%s" required><span class="choice-body"><span class="ico">%s</span><strong>%s</strong><small>%s</small></span></label>' % c for c in cats)
    countries = ["South Africa", "Zimbabwe", "Mozambique", "Angola", "Zambia", "Botswana", "Namibia", "Malawi", "Tanzania", "Kenya", "Nigeria", "Ghana", "Democratic Republic of the Congo", "Eswatini", "Lesotho", "Other"]
    c_opts = '<option value="">Choose a country</option>' + "".join('<option>%s</option>' % c for c in countries)
    body = page_hero(I["doc"], "Get a quotation", "Four short steps. One working day.",
        "Tell us what you need, how much, where it is going and who you are. We come back with shortlisted suppliers, a landed cost that includes freight, duties and clearance, and a realistic timeline.",
        "assets/img/warehouse.jpg", "Warehouse aisle with stacked pallets", compact=True) + '''
<section class="section">
  <div class="content">
    <form class="wizard form-card" id="quote" novalidate>
      <div class="progress" aria-hidden="true"><span style="width:25%%"></span></div>
      <p class="step-label" aria-live="polite" data-step-label>Step 1 of 4</p>

      <fieldset class="wstep" data-step="1">
        <legend><span class="eyebrow">Step 1</span><h2>What do you need<span class="dot">?</span></h2></legend>
        <div class="choices">%(cats)s</div>
        <div class="field full"><label for="q-desc">Describe it in your own words</label><textarea id="q-desc" name="description" required placeholder="For example: 40 solar street lights, 60 W, 8 m poles, for a municipal road. Or: a 20 ft container of ceramic floor tiles, 60 x 60 cm, matt finish."></textarea><span class="hint">Model numbers, photos and links help. You can attach files when you reply to our email.</span></div>
      </fieldset>

      <fieldset class="wstep" data-step="2" hidden>
        <legend><span class="eyebrow">Step 2</span><h2>How much, and to what standard<span class="dot">?</span></h2></legend>
        <div class="form-grid">
          <div class="field"><label for="q-qty">Quantity</label><input id="q-qty" name="quantity" type="text" inputmode="decimal" required placeholder="e.g. 500"></div>
          <div class="field"><label for="q-unit">Unit</label><select id="q-unit" name="unit"><option>pieces</option><option>sets</option><option>cartons</option><option>pallets</option><option>20 ft containers</option><option>40 ft containers</option><option>tonnes</option><option>metres</option><option>litres</option></select></div>
          <div class="field"><label for="q-budget">Target price or budget (optional)</label><input id="q-budget" name="budget" type="text" inputmode="decimal" placeholder="e.g. US$ 18 per piece, or US$ 25 000 total"></div>
          <div class="field"><label for="q-link">Link to a product or sample (optional)</label><input id="q-link" name="link" type="url" placeholder="https://"></div>
          <div class="field full"><label for="q-spec">Specifications, standards or certifications (optional)</label><textarea id="q-spec" name="specs" placeholder="Voltage, dimensions, materials, colours, SABS or CE marks, packaging, branding."></textarea></div>
        </div>
      </fieldset>

      <fieldset class="wstep" data-step="3" hidden>
        <legend><span class="eyebrow">Step 3</span><h2>Where is it going, and when<span class="dot">?</span></h2></legend>
        <div class="form-grid">
          <div class="field"><label for="q-country">Destination country</label><select id="q-country" name="country" required>%(countries)s</select></div>
          <div class="field"><label for="q-city">City or town</label><input id="q-city" name="city" type="text" required placeholder="e.g. Harare"></div>
          <div class="field"><label for="q-delivery">Delivery</label><select id="q-delivery" name="delivery"><option>Delivered to my door (duties and clearance included)</option><option>To the nearest port or border only</option><option>Ex works, I will arrange shipping</option><option>Not sure, advise me</option></select></div>
          <div class="field"><label for="q-when">When do you need it?</label><select id="q-when" name="timeline"><option>Within 4 weeks</option><option>1 to 2 months</option><option>2 to 4 months</option><option>Planning ahead, no fixed date</option></select></div>
        </div>
      </fieldset>

      <fieldset class="wstep" data-step="4" hidden>
        <legend><span class="eyebrow">Step 4</span><h2>Who should we send it to<span class="dot">?</span></h2></legend>
        <div class="form-grid">
          <div class="field"><label for="q-name">Full name</label><input id="q-name" name="name" type="text" autocomplete="name" required></div>
          <div class="field"><label for="q-company">Company (optional)</label><input id="q-company" name="company" type="text" autocomplete="organization"></div>
          <div class="field"><label for="q-email">Email</label><input id="q-email" name="email" type="email" autocomplete="email" required></div>
          <div class="field"><label for="q-phone">Phone or WhatsApp</label><input id="q-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" required placeholder="+263 ..."><span class="hint">Include the country code.</span></div>
          <div class="field"><label for="q-type">Enquiry type</label><select id="q-type" name="type"><option>Sourcing request</option><option>Brand enquiry</option><option>Project enquiry</option><option>Supplier or manufacturer</option><option>Investment or partnership</option></select></div>
          <div class="field"><label for="q-heard">How did you hear about us? (optional)</label><select id="q-heard" name="heard"><option value=""></option><option>Referral</option><option>Search engine</option><option>Facebook or Instagram</option><option>YouTube</option><option>Existing client</option><option>Other</option></select></div>
          <input type="hidden" name="brand" id="q-brand">
        </div>
        <div class="review" data-review hidden><h3>Check your request</h3><dl class="review-list"></dl></div>
        <label class="consent-line"><input type="checkbox" name="consent" required> <span>I agree that Websa Worldwide may use these details to reply to my enquiry, as described in the <a href="privacy.html">privacy notice</a>.</span></label>
      </fieldset>

      <div class="wnav">
        <button class="btn btn-outline" type="button" data-prev hidden>Back</button>
        <button class="btn btn-primary" type="button" data-next>Continue</button>
        <button class="btn btn-gold" type="submit" data-submit hidden>Send my request</button>
      </div>
      <div class="form-msg" role="status" aria-live="polite"></div>
      <div class="done" data-done hidden>
        <div class="done-ico">%(check)s</div>
        <h2>Request received<span class="dot">.</span></h2>
        <p>Your reference is <strong data-ref></strong>. A director or project lead will reply within one working day with suppliers, a landed cost and a timeline. Keep the reference for any follow-up.</p>
        <div class="btn-row"><a class="btn btn-gold" href="%(wa)s" rel="noopener" data-wa-ref>%(wai)s Confirm on WhatsApp</a><a class="btn btn-outline" href="index.html">Back to home</a></div>
      </div>
    </form>
    <p class="form-note center mt-2">Prefer to talk? WhatsApp or call <a href="tel:%(tel)s">%(phone)s</a>, or email <a href="mailto:%(email)s">%(email)s</a>.</p>
  </div>
</section>
''' % dict(cats=cat_html, countries=c_opts, check=I["check"], wa=WA, wai=I["wa"], tel=PHONE_TEL, phone=PHONE_DISPLAY, email=EMAIL)
    return page("quote.html", "Get a quotation | Websa Worldwide", "Request a quotation from Websa Worldwide in four short steps: what you need, quantity and specifications, destination and timeline, your details. Reply within one working day.",
                body, crumbs=[("Home", "index.html"), ("Get a quotation", "quote.html")], search=[("Get a quotation", "quote.html", "Four short steps. Landed cost, suppliers and timeline within one working day.")])

def contact():
    types = ["Sourcing request", "Supplier or manufacturer", "Investment or partnership", "Brand enquiry", "Media", "Other"]
    opts = "".join('<option>%s</option>' % t for t in types)
    addr = "<br>".join(ADDRESS_LINES)
    body = page_hero(I["chat"], "Let's talk", "One working day. That is our reply time.",
        "Tell us what you want to source, build or grow. A director or project lead answers every enquiry personally.",
        "assets/img/logistics-holo.jpg", "Global logistics network", compact=True) + '''
<section class="section">
  <div class="shell">
    <div class="audiences">
      <div class="aud reveal" id="buyers"><div class="ico">%(ship)s</div><h2>Buyers and importers</h2><p>Businesses in Africa that want vehicles, machinery, electronics, textiles or consumer goods sourced from China and delivered to the door.</p><a class="btn btn-primary" href="quote.html">Get a quotation</a></div>
      <div class="aud reveal d1" id="suppliers"><div class="ico">%(crane)s</div><h2>Suppliers and manufacturers</h2><p>Factories and distributors who want a reliable route into Southern African markets through a partner registered at both ends.</p><a class="btn btn-outline" href="?type=Supplier+or+manufacturer#enquiry">Offer your products</a></div>
      <div class="aud reveal d2" id="investors"><div class="ico">%(handshake)s</div><h2>Investors and partners</h2><p>Public bodies, development programmes and investors who want projects that deliver returns and leave skills behind.</p><a class="btn btn-outline" href="?type=Investment+or+partnership#enquiry">Propose a partnership</a></div>
    </div>
  </div>
</section>
<section class="section tint" id="enquiry-section">
  <div class="shell">
    <div class="split" style="align-items:start">
      <div class="reveal">
        <form class="form-card" id="enquiry" novalidate>
          <span class="eyebrow">Send an enquiry</span>
          <h2 style="font-size:clamp(26px,3vw,36px)">Tell us what you need<span class="dot">.</span></h2>
          <div class="form-grid">
            <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
            <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" type="text" autocomplete="organization"></div>
            <div class="field"><label for="f-country">Country</label><input id="f-country" name="country" type="text" autocomplete="country-name" required></div>
            <div class="field"><label for="f-type">Enquiry type</label><select id="f-type" name="type">%(opts)s</select></div>
            <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
            <div class="field"><label for="f-phone">Phone or WhatsApp</label><input id="f-phone" name="phone" type="tel" inputmode="tel" autocomplete="tel" placeholder="+263 ..."><span class="hint">Include the country code.</span></div>
            <div class="field full"><label for="f-msg">What do you need?</label><textarea id="f-msg" name="message" required placeholder="Product, quantity, destination, timeline. Attach specifications by replying to our email."></textarea></div>
          </div>
          <label class="consent-line"><input type="checkbox" name="consent" required> <span>I agree that Websa Worldwide may use these details to reply to my enquiry, as described in the <a href="privacy.html">privacy notice</a>.</span></label>
          <div class="form-foot">
            <p class="form-note" data-note-mail>Submitting opens your email app with the enquiry addressed to %(email)s. Nothing is stored on this website.</p>
            <p class="form-note" data-note-post hidden>Your enquiry goes straight to the Websa team and you receive a reference number.</p>
            <div class="btn-row"><button class="btn btn-primary" type="submit">Send enquiry</button><a class="btn btn-outline" id="wa-prefill" href="%(wa)s" rel="noopener">%(wa_i)s WhatsApp instead</a></div>
          </div>
          <div class="form-msg" role="status" aria-live="polite"></div>
        </form>
      </div>
      <div class="reveal d1" id="offices">
        <div class="office">
          <span class="eyebrow">Head office</span>
          <h3>Guangzhou, China</h3>
          <dl>
            <dt>Address</dt><dd>%(addr)s</dd>
            <dt>Phone</dt><dd><a href="tel:%(tel)s">%(phone)s</a></dd>
            <dt>WhatsApp</dt><dd><a href="%(wa)s" rel="noopener" data-wa>%(phone)s</a></dd>
            <dt>Email</dt><dd><a href="mailto:%(email)s">%(email)s</a></dd>
            <dt>Hours</dt><dd>Monday to Friday, 09:00 to 18:00 China Standard Time (03:00 to 12:00 in South Africa and Zimbabwe)</dd>
          </dl>
          <a class="btn btn-light map" href="%(map)s" rel="noopener">Open in Google Maps %(ext)s</a>
        </div>
        <div class="feature mt-2 reveal"><div class="ico">%(pin)s</div><div><h3>South Africa</h3><p>Websa Worldwide (Pty) Ltd is registered in South Africa and delivers projects across Southern Africa. Ask for a meeting in Johannesburg or on site.</p></div></div>
        <div class="feature mt-1 reveal" id="media"><div class="ico">%(chat)s</div><div><h3>Media</h3><p>Journalists can reach a director through <a href="mailto:%(email)s?subject=Media%%20enquiry">%(email)s</a> with the subject line "Media enquiry".</p></div></div>
      </div>
    </div>
  </div>
</section>
''' % dict(ship=I["ship"], crane=I["crane"], handshake=I["handshake"], opts=opts, email=EMAIL, wa=WA, wa_i=I["wa"], addr=addr, tel=PHONE_TEL, phone=PHONE_DISPLAY, map=MAP_URL, ext=I["ext"], pin=I["pin"], chat=I["chat"])
    ld = {"@type": "ContactPage", "name": "Contact Websa Worldwide", "url": SITE_URL + "/contact.html"}
    return page("contact.html", "Contact | Websa Worldwide", "Contact Websa Worldwide in Guangzhou, China or South Africa. Sourcing requests, supplier offers, partnerships and media. Phone and WhatsApp +86 173 2401 0515.",
                body, ld=ld, crumbs=[("Home", "index.html"), ("Contact", "contact.html")], search=[("Contact", "contact.html", "Guangzhou head office, phone, WhatsApp, email, hours"), ("Media enquiries", "contact.html#media", "Journalists can reach a director by email")])

def legal():
    body = page_hero(I["shield"], "Legal notice", "", "", "assets/img/import-export.jpg", "Shipping containers", compact=True) + '''
<section class="section"><div class="content"><div class="prose">
<h2>Website operator</h2>
<p>This website is operated by Websa Worldwide (Pty) Ltd, a company registered in South Africa, and Guangzhou Websa Worldwide Co., Ltd, a company registered in the People's Republic of China (together "Websa").</p>
<p>Head office: %(addr)s. Telephone %(phone)s. Email <a href="mailto:%(email)s">%(email)s</a>.</p>
<h2>Content</h2>
<p>The information on this website describes Websa's services, brands and past projects in general terms. It is not an offer capable of acceptance. Prices, availability, specifications and timelines are confirmed in a written quotation or contract.</p>
<p>Project values shown on this website are as reported by Websa. Brand names, product names and logos of third parties, including partners named in project descriptions, belong to their respective owners and are used for identification only.</p>
<h2>Intellectual property</h2>
<p>The Websa Worldwide name, logo and the brands shown on this website are the property of Websa. Text, images and design may not be reproduced without written permission, except for brief quotation with attribution.</p>
<h2>Liability</h2>
<p>Websa takes care to keep this website accurate and available but gives no warranty that it is error-free or uninterrupted. Websa is not responsible for the content of external websites linked from these pages.</p>
<h2>Governing law</h2>
<p>Use of this website is governed by the laws of the Republic of South Africa. Contracts for goods and services are governed by the law stated in the relevant contract.</p>
<p class="fineprint">Last updated <time datetime="%(iso)s">%(date)s</time>.</p>
</div></div></section>''' % dict(addr=", ".join(ADDRESS_LINES), phone=PHONE_DISPLAY, email=EMAIL, date=TODAY.strftime("%d %B %Y").lstrip("0"), iso=TODAY.isoformat())
    return page("legal.html", "Legal notice | Websa Worldwide", "Legal notice for the Websa Worldwide website: operator, content, intellectual property, liability and governing law.", body, crumbs=[("Home", "index.html"), ("Legal notice", "legal.html")])

def privacy():
    a = CONFIG["analytics"]
    if a["provider"] == "plausible" and a.get("plausible_domain"):
        analytics_p = "<p>We measure visits with Plausible Analytics, which counts page views without cookies and without storing personal information or IP addresses. It tells us which pages, countries and referring sites bring visitors, and which brands and buttons are used. It cannot identify you.</p>"
    elif a["provider"] == "ga4" and a.get("ga4_id"):
        analytics_p = "<p>We use Google Analytics to understand which pages and countries our visitors come from. It sets cookies only after you choose \"Allow analytics\" in the banner, and you can withdraw that choice at any time by clearing this site's data in your browser. IP addresses are anonymised.</p>"
    else:
        analytics_p = "<p>There are no analytics scripts and no tracking cookies on this website.</p>"
    if CONFIG["form_endpoint"]:
        form_p = "<p>When you send the enquiry form or the quotation request, the details you enter are transmitted to our form service and delivered to the Websa team by email and to a private enquiry log that only Websa staff can open. You receive a reference number. The WhatsApp button opens WhatsApp with a pre-filled message; nothing is sent until you press send there.</p>"
    else:
        form_p = "<p>Nothing is stored on this website. There are no accounts. The enquiry form and the quotation request do not send data to a server: they open your own email application with the message addressed to %s, and the WhatsApp button opens WhatsApp with a pre-filled message. Your details reach us only when you choose to send that email or message.</p>" % EMAIL
    body = page_hero(I["shield"], "Privacy", "", "", "assets/img/import-export.jpg", "Shipping containers", compact=True) + '''
<section class="section"><div class="content"><div class="prose">
<p class="lede">This website collects as little personal information as it can. Here is exactly what happens to what you share.</p>
<h2>What this website collects</h2>
%(form)s
%(analytics)s
<p>Fonts are served from this website, not from a third party. Videos are embedded from YouTube in privacy-enhanced mode and load only when you press play; at that point YouTube receives your IP address under <a href="https://policies.google.com/privacy" rel="noopener">Google's privacy policy</a>.</p>
<p>Your browser may remember a half-completed quotation request and your language choice on your own device so you can continue later. That information never leaves your device.</p>
<h2>What we do with an enquiry</h2>
<p>When you contact us, we use your name, contact details and the content of your enquiry to reply, to prepare quotations and to carry out any resulting contract. We keep enquiries for as long as needed for that purpose and for our legal and accounting obligations. We do not sell personal information or use it for marketing you did not ask for.</p>
<h2>Sharing</h2>
<p>To fulfil a request we may share the necessary details with suppliers, freight forwarders, customs agents and partners involved in your project, and with our email, messaging and form providers. We share only what each party needs.</p>
<h2>Your rights</h2>
<p>You can ask what personal information we hold about you, ask for it to be corrected or deleted, and object to its use. South African residents have these rights under the Protection of Personal Information Act, 2013. Write to <a href="mailto:%(email)s?subject=Privacy%%20request">%(email)s</a> with the subject line "Privacy request" and we will respond within one month.</p>
<h2>Contact</h2>
<p>Websa Worldwide, %(addr)s. Email <a href="mailto:%(email)s">%(email)s</a>.</p>
<p class="fineprint">Last updated <time datetime="%(iso)s">%(date)s</time>.</p>
</div></div></section>''' % dict(form=form_p, analytics=analytics_p, email=EMAIL, addr=", ".join(ADDRESS_LINES), date=TODAY.strftime("%d %B %Y").lstrip("0"), iso=TODAY.isoformat())
    return page("privacy.html", "Privacy | Websa Worldwide", "How the Websa Worldwide website handles personal information: what is collected, how enquiries are used, and your rights.", body, crumbs=[("Home", "index.html"), ("Privacy", "privacy.html")])

def notfound():
    body = '''
<section class="error-page">
  <div>
    <span class="eyebrow">Error 404</span>
    <h1>Lost<span class="dot">.</span></h1>
    <p class="lede">That page is not here. The links below will get you back on the route.</p>
    <div class="btn-row center mt-2"><a class="btn btn-primary" href="index.html">Home</a><a class="btn btn-outline" href="services.html">What we do</a><a class="btn btn-outline" href="quote.html">Get a quotation</a></div>
  </div>
</section>'''
    return page("404.html", "Page not found | Websa Worldwide", "The page you asked for does not exist on the Websa Worldwide website.", body, extra_head='<meta name="robots" content="noindex">')

# ---------------------------------------------------------------- extras: search index, og images, sitemap
def search_index():
    entries = []
    for p in PAGES:
        if p["fname"] == "404.html": continue
        entries.append({"t": p["title"], "u": p["fname"], "x": p["desc"], "k": "page"})
        for t, u, x in p["search"]: entries.append({"t": t, "u": u, "x": x, "k": "section"})
    return entries

def og_images():
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(os.path.join(OUT, "assets", "og"), exist_ok=True)
    logo = Image.open(os.path.join(OUT, "assets/img/websa-logo-reversed.png")).convert("RGBA"); logo.thumbnail((260, 200))
    f_big = ImageFont.truetype(os.path.join(ROOT, "tools/fonts/montserrat-800.ttf"), 64)
    f_small = ImageFont.truetype(os.path.join(ROOT, "tools/fonts/montserrat-600.ttf"), 28)
    for p in PAGES:
        path = os.path.join(OUT, "assets/og/%s.jpg" % p["fname"][:-5])
        im = Image.new("RGB", (1200, 630), (20, 20, 20)); d = ImageDraw.Draw(im)
        d.ellipse((820, -220, 1500, 460), fill=(31, 31, 31))
        im.paste(logo, (80, 70), logo)
        words, lines, cur = p["og_title"].split(), [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if d.textlength(t, font=f_big) > 1000 and cur: lines.append(cur); cur = w
            else: cur = t
        lines.append(cur)
        y = 310 - 39 * min(len(lines), 3)
        for i, ln in enumerate(lines[:3]): d.text((80, y + i * 78), ln, font=f_big, fill=(255, 255, 255))
        d.text((80, 540), "websaworldwide.com  |  Wealth Building Strategy for All", font=f_small, fill=(212, 167, 44))
        im.save(path, "JPEG", quality=86)

def minify_assets():
    """site.min.css by a conservative whitespace strip; site.min.js by terser when node is present, else a copy."""
    import subprocess, shutil
    css = open(os.path.join(OUT, "css", "site.css"), encoding="utf-8").read()
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{};,>])\s*", r"\1", css)
    css = re.sub(r":\s+", ":", css).replace(";}", "}").strip()
    open(os.path.join(OUT, "css", "site.min.css"), "w", encoding="utf-8").write(css)
    src, dst = os.path.join(OUT, "js", "site.js"), os.path.join(OUT, "js", "site.min.js")
    try:
        r = subprocess.run('npx --yes terser "%s" -c -m -o "%s"' % (src, dst), shell=True, capture_output=True, text=True, timeout=240)
        if r.returncode != 0 or not os.path.exists(dst): raise RuntimeError(r.stderr[:200])
    except Exception as e:
        print("terser unavailable, shipping unminified js:", e); shutil.copyfile(src, dst)

def extras():
    minify_assets()
    idx = search_index()
    json.dump(idx, open(os.path.join(OUT, "search-index.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
    urls = ""
    for p in PAGES:
        if p["fname"] == "404.html": continue
        loc = lambda l: SITE_URL + "/" + ("" if l == "en" else l + "/") + ("" if p["fname"] == "index.html" else p["fname"])
        alts = "".join('<xhtml:link rel="alternate" hreflang="%s" href="%s"/>' % (LANG_META[l][0], loc(l)) for l in LANGS)
        for l in LANGS:
            urls += '<url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority>%s</url>' % (loc(l), TODAY.isoformat(), "1.0" if p["fname"] == "index.html" else "0.8", alts)
    open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">%s</urlset>\n' % urls)
    open(os.path.join(OUT, "robots.txt"), "w", encoding="utf-8").write("User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % SITE_URL)
    open(os.path.join(OUT, "site.webmanifest"), "w", encoding="utf-8").write('{"name":"Websa Worldwide","short_name":"Websa","icons":[{"src":"assets/img/icon-192.png","sizes":"192x192","type":"image/png"},{"src":"assets/img/icon-512.png","sizes":"512x512","type":"image/png"}],"theme_color":"#141414","background_color":"#141414","display":"browser","start_url":"index.html"}\n')
    og_images()
    return idx

# ---------------------------------------------------------------- i18n
_TAG_RE = re.compile(r'(<[^>]+>)')
_ATTRS = "alt|placeholder|aria-label|title|content|data-s-[\\w-]+|data-video-title"
_SKIP_META = {"viewport", "theme-color", "twitter:card", "og:type", "og:url", "og:image", "og:image:width", "og:image:height", "og:site_name", "robots"}
_KEEP = re.compile(r"[\W\d_]+|WEBSA|LM|CN|R|US\$|Websa Worldwide|Kudus|Runningman|Zarus|Wakanaka|Stewart|EnergyOn|Benny Yamin|Bigman Autospares|Blue Digital Printing|Sandie's Happy Basket|Websa|info@websaworldwide\.com|\+86 173 2401 0515|Guangzhou|Facebook|Instagram|YouTube|WhatsApp|Postmasburg|Bulawayo|Lesedi Solar PV|EN|中文|Português|English|Google Maps|(?:R|US\$) ?[\d][\d ,.]*(?: m| each)?|Lazarus Magura|Collins Ndewere|Ekhaya Takeaway|Search|Websa Worldwide \(Pty\) Ltd|Guangzhou Websa Worldwide Co\., Ltd|https://")

def _attr_ok(tok, k, v):
    if k == "content":
        m = re.search(r'(?:name|property)="([^"]+)"', tok)
        if not m or m.group(1) in _SKIP_META: return False
    uv = htmlmod.unescape(v).strip()
    return bool(uv) and not uv.startswith(("http", "#", "assets", "+", "mailto"))

def collect_strings(html):
    out = set(); skip = 0
    for tok in _TAG_RE.split(html):
        if not tok: continue
        if tok.startswith("<"):
            low = tok.lower()
            if low.startswith(("<script", "<style")): skip += 1
            elif low.startswith(("</script", "</style")): skip = max(0, skip - 1)
            elif not low.startswith("<!"):
                for k, v in re.findall(r'\s(%s)="([^"]*)"' % _ATTRS, tok):
                    if _attr_ok(tok, k, v): out.add(htmlmod.unescape(v).strip())
            continue
        if skip: continue
        t = " ".join(htmlmod.unescape(tok).split())
        if t and not _KEEP.fullmatch(t): out.add(t)
    return out

_MONTHS_PT = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
def localise_date(text, lang):
    d = datetime.datetime.strptime(text, "%d %B %Y")
    if lang == "zh": return "%d年%d月%d日" % (d.year, d.month, d.day)
    if lang == "pt": return "%d de %s de %d" % (d.day, _MONTHS_PT[d.month - 1], d.year)
    return text

def translate_html(html, lang, dic, fname, missing):
    def tr(s):
        key = " ".join(s.split())
        if key in dic: return dic[key]
        if key and not _KEEP.fullmatch(key): missing.add(key)
        return s
    out = []; skip = 0
    for tok in _TAG_RE.split(html):
        if not tok: continue
        if tok.startswith("<"):
            low = tok.lower()
            if low.startswith(("<script", "<style")):
                skip += 1
                tok = re.sub(r'src="(js/)', lambda m: 'src="../%s' % m.group(1), tok)
            elif low.startswith(("</script", "</style")): skip = max(0, skip - 1)
            elif not low.startswith("<!"):
                def rep(m):
                    k, v = m.group(1), m.group(2)
                    if not _attr_ok(tok, k, v): return m.group(0)
                    return ' %s="%s"' % (k, esc(tr(htmlmod.unescape(v).strip())))
                tok = re.sub(r'\s(%s)="([^"]*)"' % _ATTRS, rep, tok)
                tok = re.sub(r'(href|src|content)="(assets/|css/|js/|favicon\.png|site\.webmanifest)', lambda m: '%s="../%s' % (m.group(1), m.group(2)), tok)
                tok = re.sub(r'srcset="([^"]+)"', lambda m: 'srcset="' + re.sub(r'(^|, )(assets/)', r'\1../\2', m.group(1)) + '"', tok)
                if 'rel="canonical"' in tok or 'property="og:url"' in tok:
                    tok = tok.replace(SITE_URL + "/", SITE_URL + "/%s/" % lang)
                if low.startswith("<html"): tok = '<html lang="%s">' % LANG_META[lang][0]
                if 'data-lang="' in tok:
                    target = re.search(r'data-lang="(\w+)"', tok).group(1)
                    href = ("../%s" % fname) if target == "en" else (fname if target == lang else "../%s/%s" % (target, fname))
                    tok = re.sub(r'href="[^"]*"', 'href="%s"' % href, tok)
                    if target == lang: tok = tok.replace("<a ", '<a aria-current="true" ', 1)
                if 'data-page-lang' in tok: tok = tok.replace('data-page-lang="en"', 'data-page-lang="%s"' % lang)
            out.append(tok); continue
        if skip or not tok.strip(): out.append(tok); continue
        lead = tok[:len(tok) - len(tok.lstrip())]; trail = tok[len(tok.rstrip()):]
        core = htmlmod.unescape(tok.strip())
        if core == "EN" and lang != "en": core = {"zh": "中文", "pt": "PT"}[lang]
        elif re.fullmatch(r"\d{1,2} [A-Z][a-z]+ \d{4}", core): core = localise_date(core, lang)
        else: core = tr(core)
        out.append(lead + esc(core).replace("&#x27;", "'") + trail)
    return "".join(out)

def build_translations(idx):
    report = {}
    en_pages = [p["fname"] for p in PAGES]
    all_strings = set()
    for f in en_pages: all_strings |= collect_strings(open(os.path.join(OUT, f), encoding="utf-8").read())
    for e in idx: all_strings.add(e["t"]); all_strings.add(e["x"])
    os.makedirs(I18N, exist_ok=True)
    open(os.path.join(I18N, "en-strings.txt"), "w", encoding="utf-8").write("\n".join(sorted(all_strings)))
    for lang in LANGS:
        if lang == "en": continue
        path = os.path.join(I18N, lang + ".json")
        dic = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
        missing = set(); outdir = os.path.join(OUT, lang); os.makedirs(outdir, exist_ok=True)
        for f in en_pages:
            html = open(os.path.join(OUT, f), encoding="utf-8").read()
            open(os.path.join(outdir, f), "w", encoding="utf-8").write(translate_html(html, lang, dic, f, missing))
        tidx = [{"t": dic.get(e["t"], e["t"]), "u": e["u"], "x": dic.get(e["x"], e["x"]), "k": e["k"]} for e in idx]
        json.dump(tidx, open(os.path.join(outdir, "search-index.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
        open(os.path.join(I18N, "missing-%s.txt" % lang), "w", encoding="utf-8").write("\n".join(sorted(missing)))
        total = len(all_strings); done = len([s for s in all_strings if s in dic])
        report[lang] = (done, total, len(missing))
    return report

# ---------------------------------------------------------------- audit
def audit(pages, i18n_report):
    problems = []
    files = [os.path.join(OUT, p) for p in pages] + [os.path.join(OUT, "css", "site.css"), os.path.join(OUT, "js", "site.js"), os.path.join(ROOT, "build.py")]
    for lang in LANGS:
        if lang != "en": files += [os.path.join(OUT, lang, p) for p in pages]
    for fp in files:
        s = open(fp, encoding="utf-8").read()
        em, en = s.count(chr(0x2014)), s.count(chr(0x2013))
        if em or en: problems.append("%s: %d em, %d en dashes" % (os.path.relpath(fp, ROOT), em, en))
        if fp.endswith(".html"):
            base = os.path.dirname(fp)
            for m in re.findall(r'(?:href|src)="([^"#?]+)', s):
                if m.startswith(("http", "mailto:", "tel:")) or not m: continue
                if not os.path.exists(os.path.normpath(os.path.join(base, m))): problems.append("%s: missing %s" % (os.path.relpath(fp, ROOT), m))
            for m in re.findall(r'srcset="([^"]+)"', s):
                for part in m.split(","):
                    src = part.strip().split(" ")[0]
                    if src and not os.path.exists(os.path.normpath(os.path.join(base, src))): problems.append("%s: missing srcset %s" % (os.path.relpath(fp, ROOT), src))
            if "<h1" not in s: problems.append("%s: no h1" % os.path.relpath(fp, ROOT))
            if 'name="description"' not in s: problems.append("%s: no description" % os.path.relpath(fp, ROOT))
    for lang, (done, total, miss) in i18n_report.items():
        if total and done / total < 0.95: problems.append("i18n %s: %d of %d strings translated (%d missing)" % (lang, done, total, miss))
    return problems

if __name__ == "__main__":
    pages = [home(), about(), team(), services(), sourcing(), energy(), construction(), agriculture(), brands(), projects()]
    pages += [case_page(c) for c in CASES]
    pages += [quote(), contact(), legal(), privacy(), notfound()]
    idx = extras()
    rep = build_translations(idx)
    problems = audit(pages, rep)
    print("built %d pages x %d languages into %s" % (len(pages), len(LANGS), OUT))
    for lang, (done, total, miss) in rep.items(): print("i18n %s: %d/%d strings (%d missing)" % (lang, done, total, miss))
    print("audit:", "clean" if not problems else "\n  " + "\n  ".join(problems))
    if "--check" in sys.argv and problems: sys.exit(1)
