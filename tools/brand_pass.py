# -*- coding: utf-8 -*-
"""Copy pass (2026-10-11): Websa as a brand owner bringing the power of China to the customer, not an agent."""
import os, re
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build.py")
s = open(P, encoding="utf-8").read()
PAIRS = [
# nav: brands first
('''NAV_LEFT = [
  ("What we do", [''', '''NAV_LEFT = [
  ("Our brands", [("brands.html", "Brand portfolio", "Kudus, Runningman, Zarus, EnergyOn and more")]),
  ("What we do", ['''),
('''  ]),
  ("Our brands", [("brands.html", "Brand portfolio", "Kudus, Runningman, Zarus, EnergyOn and more")]),
]
NAV_RIGHT''', '''  ]),
]
NAV_RIGHT'''),
# home: brands section first, new copy
('''<section class="section" id="mission">
  <div class="content">
    <div class="section-head reveal">
      <span class="eyebrow">Why we exist</span>
      <h2>Your growth is the strategy<span class="dot">.</span></h2>
      <p class="lede">WEBSA stands for Wealth Building Strategy for All: the equipment, the partners and the skills that let you build wealth yourself. Since 1999, now brought from Guangzhou straight to you.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="num">1</div><h3>Tell us the problem</h3><p>A machine you cannot find, a tender you need to win, a farm that should earn more. We turn it into a costed plan with suppliers, landed cost, timeline and a funding route.</p></div>
      <div class="step reveal d1"><div class="num">2</div><h3>We make it happen</h3><p>We procure, inspect, ship, clear and install. When conditions change mid-project, and they do, our team on the ground adapts so your schedule does not slip.</p></div>
      <div class="step reveal d2"><div class="num">3</div><h3>You own it, fully</h3><p>We stay until it runs and train your people to operate and maintain it, so the value stays with you long after we leave.</p></div>
    </div>
  </div>
</section>
''', ''),
('''<section class="section" id="brands">
  <div class="shell">
    <div class="section-head reveal">
      <span class="eyebrow">Stock our brands</span>
      <h2>Products your customers already ask for<span class="dot">.</span></h2>
    </div>''', '''<section class="section" id="brands">
  <div class="shell">
    <div class="section-head reveal">
      <span class="eyebrow">Our brands</span>
      <h2>Built with the power of China. Made for you<span class="dot">.</span></h2>
      <p class="lede">Ten Websa brands, from baby care to vehicle parts and energy, manufactured with China's scale and technology and delivered to you by our own teams.</p>
    </div>'''),
('''    <div class="btn-row center mt-2 reveal"><a class="btn btn-outline" href="brands.html">Explore the portfolio</a></div>
  </div>
</section>
''', '''    <div class="btn-row center mt-2 reveal"><a class="btn btn-outline" href="brands.html">Meet every brand</a></div>
  </div>
</section>

<section class="section tint" id="mission">
  <div class="content">
    <div class="section-head reveal">
      <span class="eyebrow">The power of China</span>
      <h2>Scale, speed and technology, working for you<span class="dot">.</span></h2>
      <p class="lede">China builds faster, at a scale and a price no one else can match. Websa puts that power behind our own brands and your projects, with our people accountable for every step.</p>
    </div>
    <div class="steps">
      <div class="step reveal"><div class="num">1</div><h3>Tell us the problem</h3><p>A product your market is missing, a tender you need to win, a farm that should earn more. We turn it into a plan with a delivered price, a timeline and a funding route.</p></div>
      <div class="step reveal d1"><div class="num">2</div><h3>We build it and bring it</h3><p>Our brands and projects are made with China's manufacturing strength, then shipped, cleared and installed by our own team, so your schedule does not slip.</p></div>
      <div class="step reveal d2"><div class="num">3</div><h3>You own it, fully</h3><p>We stay until it runs and train your people to operate and maintain it, so the value stays with you long after we leave.</p></div>
    </div>
  </div>
</section>
'''),
('<section class="section tint" id="sectors">', '<section class="section" id="sectors">'),
('''<span class="eyebrow">What we solve</span>
      <h2>Whatever you need to move, build or grow<span class="dot">.</span></h2>
      <p class="lede">One accountable partner from the first call to the hand-over.</p>''', '''<span class="eyebrow">What we solve</span>
      <h2>Whatever you need to move, build or grow<span class="dot">.</span></h2>
      <p class="lede">Four divisions, one accountable partner from the first call to the hand-over.</p>'''),
('short="Need equipment, vehicles or stock from China without the risk? We find the factory, check the goods and land them at your door, paperwork included."',
 'short="Need vehicles, machinery or stock? Our own logistics team brings China\'s products to your door, documents and customs handled."'),
('<section class="section tint" id="difference">', '<section class="section tint" id="difference">'),
('''<a href="#mission" aria-label="Why we exist"><span>Why we exist</span><i></i></a>
  <a href="#sectors" aria-label="What we solve"><span>What we solve</span><i></i></a>
  <a href="#brands" aria-label="Brands"><span>Brands</span><i></i></a>''', '''<a href="#brands" aria-label="Brands"><span>Brands</span><i></i></a>
  <a href="#mission" aria-label="The power of China"><span>The power of China</span><i></i></a>
  <a href="#sectors" aria-label="What we solve"><span>What we solve</span><i></i></a>'''),
('<div class="cap"><h3>Need it from China?</h3><p>Tell us the product, the quantity and the destination. You get suppliers, a landed cost and a timeline within one working day.</p><span class="more">Start now %(ar)s</span></div>',
 '<div class="cap"><h3>Bring the power of China to your business</h3><p>Tell us the product, the quantity and the destination. You get a delivered price and a timeline within one working day.</p><span class="more">Start now %(ar)s</span></div>'),
('''search = [("Why we exist", "index.html#mission", "Your growth is the strategy. Tell us the problem, we make it happen, you own it fully."),''',
 '''search = [("The power of China", "index.html#mission", "Scale, speed and technology, working for you. Tell us the problem, we build it and bring it, you own it fully."),'''),
('"Tell Websa Worldwide what your business needs and we find it, check it, ship it and deliver it to your door from Guangzhou, then train your people to run it. Trade, energy, construction and agriculture since 1999."',
 '"Websa Worldwide brings the power of China to you: ten brands of our own and projects in trade, energy, construction and agriculture, built with China\'s manufacturing strength and delivered by our own teams since 1999."'),
('"Websa Worldwide | From China to you: trade, energy, construction and agriculture"', '"Websa Worldwide | From China to you: our brands, your projects, the power of China"'),
# sourcing page
('sector_page("sourcing", "Import, export and logistics", "From the factory to your door.",\n        "Need vehicles, machinery, electronics, textiles or consumer goods from China without the guesswork? From Guangzhou we procure, inspect and ship for you, and handle the documents, freight and customs so your goods arrive on time and on budget.",',
 'sector_page("sourcing", "Import, export and logistics", "The power of China, delivered to your door.",\n        "Vehicles, machinery, electronics, textiles, consumer goods: Websa brings China\'s products to you and moves yours to the world, with our own logistics team handling documents, freight and customs so everything arrives on time and on budget.",'),
('"Your goods, handled end to end", "Years of connecting African buyers with Chinese manufacturers, and the logistics discipline to make every shipment of yours efficient and cost-effective.",',
 '"Your goods, handled end to end", "Our own brands, our own warehouses and our own logistics discipline, so every shipment of yours is efficient and arrives when we said it would.",'),
('("Logistics management", "Warehousing, transport and distribution designed around your supply chain, so your deliveries arrive when you said they would."),',
 '("Logistics management", "Warehousing, transport and distribution run by our team around your business, so your deliveries arrive when you said they would."),'),
('("Supply chain solutions", "Strategic insight and practical fixes that cut your costs and lift efficiency across your whole chain.")',
 '("Supply chain solutions", "Practical fixes from a company that runs its own supply chain, to cut your costs and lift efficiency across yours.")'),
('["A Guangzhou company with its own delivery team in Africa, so someone is accountable at both ends of the route.",\n         "Factory inspections before payment, not photographs after shipping.",\n         "Landed-cost quotations that include freight, insurance, duties and clearance.",\n         "Vehicles, farming equipment and mining equipment already delivered for clients in the region."],',
 '["A Guangzhou company with its own delivery team in Africa, so someone is accountable at both ends of the route.",\n         "Our own brands and our own quality checks before anything ships to you.",\n         "Delivered prices that include freight, insurance, duties and clearance.",\n         "Vehicles, farming equipment and mining equipment already delivered for partners in the region."],'),
('<div class="num">1</div><h3>Brief and quotation</h3><p>You tell us what you need. We shortlist factories, check them, and quote a landed cost that includes freight, duties and clearance, not just the factory price.</p>',
 '<div class="num">1</div><h3>Brief and quotation</h3><p>You tell us what you need. We match it from our brands and our manufacturing partners and quote a delivered price that includes freight, duties and clearance.</p>'),
('<div class="num">2</div><h3>Inspection and shipping</h3><p>Our Guangzhou team inspects the goods before they leave, consolidates your order and books air, sea or road freight to suit the budget and the deadline.</p>',
 '<div class="num">2</div><h3>Quality and shipping</h3><p>Our Guangzhou team checks the goods before they leave, consolidates your order and books air, sea or road freight to suit your budget and deadline.</p>'),
('<h3>Automobiles</h3><p>Vehicles supplied from China, Japan, Singapore and Durban.</p>', '<h3>Automobiles</h3><p>Vehicles and Bigman Autospares parts, delivered from China, Japan, Singapore and Durban.</p>'),
('<h3>Electronics</h3><p>Consumer and commercial electronics, factory-direct.</p>', '<h3>Electronics</h3><p>Consumer and commercial electronics with China\'s technology behind them.</p>'),
('<h3>Textiles</h3><p>Garments and fabric from inspected Guangzhou factories.</p>', '<h3>Textiles</h3><p>Garments and fabric made in Guangzhou to your specification.</p>'),
('<h3>Machinery</h3><p>Farming, mining and construction equipment with spares.</p>', '<h3>Machinery</h3><p>Farming, mining and construction equipment, with spares and training.</p>'),
('<span class="eyebrow">From the factory floor</span><h2>See the route from factory to you<span class="dot">.</span></h2>', '<span class="eyebrow">From the factory floor</span><h2>See the power of China at work for you<span class="dot">.</span></h2>'),
('title="Buying from China made easy through Websa"', 'title="The power of China, brought to you by Websa"'),
# energy / construction leftovers
('("Mining and construction equipment", "Heavy equipment and spares for your site, procured from manufacturers we have inspected."),',
 '("Mining and construction equipment", "Heavy equipment and spares for your site, built by our manufacturing partners in China."),'),
('("Petroleum supply", "Fuel and petroleum products procured and supplied to keep your operation moving."),',
 '("Petroleum supply", "Fuel and petroleum products supplied to keep your operation moving."),'),
('("Equipment and inputs", "Farming equipment procured and supplied to you, with financing routes and operator training."),',
 '("Equipment and inputs", "Farming equipment supplied to you, with financing routes and operator training."),'),
# services hub advisory
("<h3>Business advisory</h3><p>Market entry, supplier strategy and the funding routes open to you when you buy from China.</p>",
 "<h3>Business advisory</h3><p>Market entry, product strategy and the funding routes open to you when you work with China.</p>"),
("<h3>Technical consultancy</h3><p>Specification, factory audits and quality inspection before you pay for or ship anything.</p>",
 "<h3>Technical consultancy</h3><p>Specification, quality checks and factory audits before anything ships to you.</p>"),
# brands page
('page_hero(I["tag"], "Our brands", "Products your customers already ask for",\n        "Stock or distribute a Websa brand and you get more than a product: a partner that handles supply, logistics and support with you.",',
 'page_hero(I["tag"], "Our brands", "Built with the power of China. Made for you.",\n        "Every Websa brand is designed for African homes and businesses, manufactured with China\'s scale and technology, and backed by our own teams. Stock one and you get a partner, not just a product.",'),
('"The Websa Worldwide brand portfolio: Kudus, Runningman, Blue Digital Printing, Sandie\'s Happy Basket, Zarus, Benny Yamin, Wakanaka, Stewart, Bigman Autospares and EnergyOn."',
 '"Ten Websa Worldwide brands built with the power of China: Kudus, Runningman, Blue Digital Printing, Sandie\'s Happy Basket, Zarus, Benny Yamin, Wakanaka, Stewart, Bigman Autospares and EnergyOn."'),
# quote
('page_hero(I["doc"], "Get your quotation", "Four short steps. One working day.",\n        "Tell us what you need, how much, where it is going and who you are. Within one working day you get shortlisted suppliers, a landed cost that includes freight, duties and clearance, and a realistic timeline.",',
 'page_hero(I["doc"], "Get your quotation", "Four short steps. One working day.",\n        "Tell us what you need, how much, where it is going and who you are. Within one working day you get a delivered price that includes freight, duties and clearance, and a realistic timeline.",'),
('"Tell Websa Worldwide what you need in four short steps and get suppliers, a landed cost and a timeline back within one working day."',
 '"Tell Websa Worldwide what you need in four short steps and get a delivered price and a timeline back within one working day."'),
(". A director or project lead will reply within one working day with suppliers, a landed cost and a timeline. Keep the reference for any follow-up.",
 ". A director or project lead will reply within one working day with a delivered price and a timeline. Keep the reference for any follow-up."),
('<option>Sourcing request</option>', '<option>Product or quotation request</option>'),
('<option>Purchase request</option>', '<option>Product or quotation request</option>'),
('types = ["Purchase request",', 'types = ["Product or quotation request",'),
# contact
('<h2>You need goods from China</h2><p>Vehicles, machinery, electronics, textiles or consumer goods, bought in China and delivered to your door, with the risk handled by us.</p>',
 '<h2>You want our products</h2><p>Websa brands, vehicles, machinery and equipment built with the power of China, delivered to your door and supported by our team.</p>'),
('("Four short steps. Landed cost, suppliers and timeline within one working day.")', '("Four short steps. A delivered price and a timeline within one working day.")'),
('"Four short steps. Landed cost, suppliers and timeline within one working day."', '"Four short steps. A delivered price and a timeline within one working day."'),
# cta strips
('cta_strip("Tell us what you need today.", "Send a specification, a photo or a rough idea. You get suppliers, a landed cost and a timeline back within one working day.", primary=("quote.html", "Get your quotation"))',
 'cta_strip("Tell us what you need today.", "Send a specification, a photo or a rough idea. You get a delivered price and a timeline back within one working day.", primary=("quote.html", "Get your quotation"))'),
("Tell us what you need to buy, build or grow. A director replies within one working day.", "Tell us what you want to build or grow. A director replies within one working day."),
("Tell us what you want to buy, build or grow. A director or project lead answers you personally, today if you write before noon.", "Tell us what you want to build or grow. A director or project lead answers you personally, today if you write before noon."),
('"Contact Websa Worldwide at its Guangzhou head office or its Africa delivery office. Purchase requests, supplier offers, partnerships and media. Phone and WhatsApp +86 173 2401 0515."',
 '"Contact Websa Worldwide at its Guangzhou head office or its Africa delivery office. Product and quotation requests, partnerships and media. Phone and WhatsApp +86 173 2401 0515."'),
]
applied = 0
for a, b in PAIRS:
    if a in s: s = s.replace(a, b); applied += 1
    elif b and b in s: pass
    else: print("NOT FOUND:", a[:90].replace("\n", " "))
open(P, "w", encoding="utf-8").write(s)
print("applied", applied, "of", len(PAIRS))
left = [l.strip()[:140] for l in s.splitlines() if re.search(r"landed|shortlist|find the factory|factory-direct|bought in China|Buy from China|procure", l, re.I) and "def " not in l]
print("leftovers:"); [print("  ", x) for x in left]
