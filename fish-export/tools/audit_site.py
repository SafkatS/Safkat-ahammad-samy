"""Technical SEO / AI-search audit of the generated site.

  python3 tools/audit_site.py .            (run from fish-export/ after building)

Checks titles, descriptions, h1, canonical, hreflang reciprocity, JSON-LD, internal links and the sitemap."""
import json, os, re, sys, collections
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(sys.argv[1])
SITE = "https://goodbuyfoods.com"


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.imgs, self.ld, self.h1, self.alts, self.meta = [], [], [], 0, [], {}
        self.title, self._t, self._ld, self.canon, self.lang, self.dir, self.ids = "", False, None, None, None, None, set()
        self.hreflang = {}
        self.text_len = 0

    def handle_starttag(self, tag, a):
        a = dict(a)
        if a.get("id"): self.ids.add(a["id"])
        if tag == "html": self.lang, self.dir = a.get("lang"), a.get("dir")
        if tag == "a" and a.get("href"): self.links.append(a["href"])
        if tag in ("img", "source", "video", "script", "link") and (a.get("src") or (tag == "link" and a.get("rel") == "stylesheet")):
            self.imgs.append(a.get("src") or a.get("href"))
        if tag == "video" and a.get("poster"): self.imgs.append(a["poster"])
        if tag == "img": self.alts.append(a.get("alt"))
        if tag == "h1": self.h1 += 1
        if tag == "title": self._t = True
        if tag == "meta" and a.get("name"): self.meta[a["name"]] = a.get("content", "")
        if tag == "link" and a.get("rel") == "canonical": self.canon = a.get("href")
        if tag == "link" and a.get("rel") == "alternate" and a.get("hreflang"): self.hreflang[a["hreflang"]] = a["href"]
        if tag == "script" and a.get("type") == "application/ld+json": self._ld = ""

    def handle_endtag(self, tag):
        if tag == "title": self._t = False
        if tag == "script" and self._ld is not None: self.ld.append(self._ld); self._ld = None

    def handle_data(self, d):
        if self._t: self.title += d
        if self._ld is not None: self._ld += d
        else: self.text_len += len(d.strip())


pages = {}
for dp, dn, fn in os.walk(ROOT):
    rp = os.path.relpath(dp, ROOT)
    if rp.startswith((".", "node_modules", "tools", "automation")) and rp != ".": continue
    for f in fn:
        if f.endswith(".html"):
            rel = os.path.relpath(os.path.join(dp, f), ROOT)
            p = P(); p.feed(open(os.path.join(dp, f), encoding="utf-8").read()); pages[rel] = p

issues = collections.defaultdict(list)
titles = collections.Counter(p.title.strip() for p in pages.values())
descs = collections.Counter(p.meta.get("description", "") for p in pages.values())
url_of = lambda rel: SITE + "/" + ("" if rel == "index.html" else rel[:-10] if rel.endswith("/index.html") else rel)
nlinks = 0
for rel, p in pages.items():
    base = os.path.dirname(rel)
    t = p.title.strip(); d = p.meta.get("description", "")
    if not t: issues["missing title"].append(rel)
    elif len(t) > 70: issues["title over 70 characters"].append((rel, len(t)))
    if titles[t] > 1: issues["duplicate title"].append(rel)
    if not d: issues["missing meta description"].append(rel)
    elif len(d) > 175: issues["meta description over 175 characters"].append((rel, len(d)))
    elif len(d) < 70: issues["meta description under 70 characters"].append((rel, len(d)))
    if descs[d] > 1: issues["duplicate meta description"].append(rel)
    if p.h1 != 1: issues["h1 count not 1"].append((rel, p.h1))
    if not p.canon: issues["missing canonical"].append(rel)
    elif p.canon != url_of(rel): issues["canonical mismatch"].append((rel, p.canon))
    if not p.lang: issues["missing html lang"].append(rel)
    if any(a is None for a in p.alts): issues["img without alt"].append(rel)
    for blob in p.ld:
        try: json.loads(blob)
        except Exception as e: issues["invalid JSON-LD"].append((rel, str(e)[:60]))
    if not p.ld: issues["no structured data"].append(rel)
    for h in p.hreflang.values():
        tgt = urlparse(h).path.lstrip("/") or "index.html"
        if tgt.endswith("/"): tgt += "index.html"
        if tgt not in pages: issues["hreflang target missing"].append((rel, h))
        elif pages[tgt].hreflang != p.hreflang: issues["hreflang not reciprocal"].append((rel, tgt))
    for h in p.links + p.imgs:
        if not h or h.startswith(("http", "mailto:", "tel:", "#", "data:", "javascript:")): continue
        u = urlparse(h); nlinks += 1
        target = os.path.normpath(os.path.join(base, unquote(u.path))) if u.path else rel
        if u.path and not os.path.exists(os.path.join(ROOT, target)):
            issues["broken internal link"].append((rel, h))
        elif u.fragment and target.endswith(".html") and target in pages and u.fragment not in pages[target].ids and not u.fragment.startswith(("p-", "cat-")):
            issues["missing anchor"].append((rel, h))

sm = open(os.path.join(ROOT, "sitemap.xml"), encoding="utf-8").read()
sm_urls = set(re.findall(r"<loc>([^<]+)</loc>", sm))
for rel in pages:
    if url_of(rel) not in sm_urls: issues["page not in sitemap"].append(rel)
for u in sm_urls:
    rel = urlparse(u).path.lstrip("/") or "index.html"
    if rel.endswith("/"): rel += "index.html"
    if rel not in pages: issues["sitemap URL without page"].append(u)

by_lang = collections.Counter(p.lang for p in pages.values())
summary = {"pages": len(pages), "by_lang": dict(by_lang), "internal_refs_checked": nlinks, "sitemap_urls": len(sm_urls),
           "issues": {k: {"count": len(v), "examples": v[:6]} for k, v in sorted(issues.items())}}
print(json.dumps(summary, ensure_ascii=False, indent=1))
if len(sys.argv) > 2:
    json.dump(summary, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
