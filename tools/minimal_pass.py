# -*- coding: utf-8 -*-
"""Minimal home page (2026-10-11): hero, brands, power of China, what we solve, one proof story, one CTA."""
import os, re
P = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "build.py")
s = open(P, encoding="utf-8").read()

def cut(start_marker, end_marker, label):
    global s
    i = s.find(start_marker)
    if i < 0: print("skip (not found):", label); return
    j = s.find(end_marker, i)
    if j < 0: print("skip (end not found):", label); return
    s = s[:i] + s[j + len(end_marker):]
    print("removed:", label)

cut('<section class="section" id="projects">', '</section>\n', "home projects list")
cut('<section class="section tint" id="websites">', '</section>\n', "home big cards")
cut('<nav class="dots-nav" aria-label="Page sections">', '</nav>\n', "side dots")
cut('<div class="bottom-bar" aria-label="Quick links">', '</div>\n</div>\n', "bottom bar")

pairs = [
# one CTA block where the big cards were
("</section>\n''' % dict(slides=slides_html,", '''</section>

<section class="section" id="start">
  <div class="shell"><div class="cta-strip reveal">
    <div><h2>Bring the power of China to your business<span class="dot">.</span></h2><p>Tell us the product, the quantity and the destination. You get a delivered price and a timeline within one working day.</p></div>
    <div class="btn-row"><a class="btn btn-gold" href="quote.html">Get your quotation today</a><a class="btn btn-ghost" href="contact.html#investors">Partner with us</a></div>
  </div></div>
</section>
\'\'\' % dict(slides=slides_html,'''),
# single still hero image, no slideshow, no pause button
('''    slides = [("assets/img/hero-produce-factory.jpg", "A farmer holding a crate of fresh produce, with a Guangzhou factory floor behind her"),
              ("assets/img/warehouse.jpg", "Forklift moving pallets inside a distribution warehouse"),
              ("assets/img/solar-farm.jpg", "Rows of solar panels on a utility-scale solar farm")]''',
 '''    slides = [("assets/img/hero-produce-factory.jpg", "A farmer holding a crate of fresh produce, with a Guangzhou factory floor behind her")]'''),
('''  <button class="pause" type="button" aria-pressed="false" aria-label="Pause background slideshow">%(pause)s%(play)s</button>\n''', ''),
('body, body_class="has-bottom-bar", search=search, og_title=', 'body, search=search, og_title='),
# shorter sector lines
('short="Is an unreliable grid holding you back? We deliver solar, electrical and fuel solutions and train your people to keep them running."',
 'short="Solar, electrical and fuel solutions, with your people trained to keep them running."'),
('short="Building, mining or opening a storefront? We supply the machines, manage the project and put your name on the door."',
 'short="Machines, project management and the signage that puts your name on the door."'),
('short="Want your farm to earn like a business? We bring the seed, equipment, finance routes and training that turn a harvest into a livelihood."',
 'short="Seed, equipment, finance routes and training that turn a harvest into a livelihood."'),
('short="Need vehicles, machinery or stock? Our own logistics team brings China\'s products to your door, documents and customs handled."',
 'short="China\'s products to your door, and yours to the world, by our own logistics team."'),
# tighter section intros
('''      <p class="lede">Ten Websa brands, from baby care to vehicle parts and energy, manufactured with China's scale and technology and delivered to you by our own teams.</p>''',
 '''      <p class="lede">Ten brands, from baby care to vehicle parts and energy, made with China's scale and delivered by our own teams.</p>'''),
('''      <p class="lede">China builds faster, at a scale and a price no one else can match. Websa puts that power behind our own brands and your projects, with our people accountable for every step.</p>''',
 '''      <p class="lede">China builds faster, at a scale and price no one else matches. We put that power behind our brands and your projects.</p>'''),
('''      <p class="lede">Four divisions, one accountable partner from the first call to the hand-over.</p>''', '''      <p class="lede">Four divisions, one accountable partner.</p>'''),
('''<p>In Postmasburg we did more than install solar street lights with Lesedi Solar PV and Philips Lighting. We trained local residents as installers, then ran two years of supply and training for two 75 MW plants.</p>''',
 '''<p>In Postmasburg we installed solar street lights with Lesedi Solar PV and Philips Lighting, trained local residents as installers, then served two 75 MW plants for two years.</p>'''),
]
for a, b in pairs:
    if a in s: s = s.replace(a, b); print("ok:", a[:50].replace("\n", " "))
    elif b and b in s: pass
    else: print("NOT FOUND:", a[:80].replace("\n", " "))
# the pause and play icons may now be unused in the dict call; keep the keys harmlessly
open(P, "w", encoding="utf-8").write(s)
print("home sections now:", re.findall(r'<section class="(?:hero|section[^"]*)" id="([^"]+)"', s[s.find("def home"):s.find("def about")]))
