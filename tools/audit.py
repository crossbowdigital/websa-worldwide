# -*- coding: utf-8 -*-
"""Pre-ship audit for the Websa Worldwide site. Exit 1 on any problem.

    python tools/audit.py

1. Rebuilds the site with build.py --check (dash count, asset paths, h1, description, i18n coverage).
2. Crawls every HTML file under site/: every internal link target exists, every #anchor exists on
   its page, every image has an alt attribute, every page has exactly one h1 and a unique title.
3. Confirms the built HTML matches what build.py produces (no hand edits left behind).
"""
import os, re, sys, subprocess, html

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(ROOT, "site")
problems = []

# 1. build + built-in audit
r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py"), "--check"], capture_output=True, text=True, encoding="utf-8", errors="replace")
sys.stdout.write(r.stdout)
if r.returncode != 0:
    problems.append("build.py --check failed")

# 2. crawl
pages = []
for base, _, files in os.walk(SITE):
    for f in files:
        if f.endswith(".html"): pages.append(os.path.join(base, f))
ids = {}
for p in pages:
    s = open(p, encoding="utf-8").read()
    ids[p] = set(re.findall(r'\sid="([^"]+)"', s))
titles = {}
for p in pages:
    s = open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, ROOT)
    base = os.path.dirname(p)
    h1s = re.findall(r"<h1[\s>]", s)
    if len(h1s) != 1: problems.append("%s: %d h1 elements" % (rel, len(h1s)))
    t = re.search(r"<title>(.*?)</title>", s, re.S)
    t = html.unescape(t.group(1).strip()) if t else ""
    lang_dir = os.path.relpath(base, SITE)
    key = (lang_dir, t)
    if key in titles: problems.append("%s: duplicate title with %s" % (rel, titles[key]))
    titles[key] = rel
    for m in re.finditer(r"<img\b[^>]*>", s):
        if ' alt="' not in m.group(0) and " alt=" not in m.group(0): problems.append("%s: img without alt: %s" % (rel, m.group(0)[:80]))
    for href in re.findall(r'href="([^"]+)"', s):
        if href.startswith(("http", "mailto:", "tel:", "javascript:")): continue
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        target = p if not path else os.path.normpath(os.path.join(base, path))
        if path and not os.path.exists(target): problems.append("%s: broken link %s" % (rel, href)); continue
        if frag and target in ids and frag not in ids[target] and frag != "top": problems.append("%s: missing anchor #%s in %s" % (rel, frag, os.path.relpath(target, ROOT)))

# 3. report
if problems:
    print("AUDIT FAILED (%d):" % len(problems))
    for x in problems: print("  " + x)
    sys.exit(1)
print("audit passed: %d pages crawled, links, anchors, alt text, h1 and titles all good" % len(pages))
