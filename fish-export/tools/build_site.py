#!/usr/bin/env python3
"""Builds the Worldclass Bengal Fishers static site.

  python3 tools/build_site.py

Edit products in tools/catalog.py and site-wide settings below. Outputs plain HTML
(crawlable by search engines and AI assistants), sitemap.xml, robots.txt, llms.txt
and assets/js/catalog.js.
"""
import html, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from catalog import CATEGORIES, P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.worldclassbengalfishers.com"   # ← your live domain
BRAND = "Worldclass Bengal Fishers"
SHORT = "WBF"
TODAY = datetime.date.today().isoformat()
V = "assets/video/"
E = html.escape
CAT = {c[0]: c for c in CATEGORIES}
N_PRODUCTS = len(P)
N_FISH = sum(1 for p in P if CAT[p[1]][2] == "fish")
N_FOOD = N_PRODUCTS - N_FISH

# Network figures from WBF research (EPB directory, SFDA list, BFFEA, Oct 2026)
NET = dict(mapped=148, districts=17, shortlisted=54, tier_a=19, tier_b=16, tier_c=19)
DISTRICTS = [("Dhaka", 37), ("Khulna", 33), ("Chattogram", 29), ("Brahmanbaria", 14), ("Jashore", 10),
             ("Cox's Bazar", 5), ("Sylhet", 4), ("Bagerhat", 3), ("Sunamganj", 3), ("Other districts", 10)]
HSCATS = [("0303", "Frozen fish", 78, "Sea fish, hilsa, pomfret"),
          ("0302", "Fresh & chilled fish", 58, "Chilled freshwater fish, carp"),
          ("0301", "Live fish, eel & crab", 53, "Live mud crab, live eel (kuchia)"),
          ("0306", "Crustaceans (shrimp, prawn, crab)", 46, "Black tiger, freshwater prawn"),
          ("0305", "Dried & salted fish", 27, "Dried marine fish, salted fish")]

LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#0A2540"/><path d="M8 21c4-6 11-8 18-4l6-4-1.5 7 1.5 7-6-4c-7 4-14 2-18-2z" fill="#F5FBFD"/><circle cx="14" cy="19.5" r="1.4" fill="#0A2540"/><path d="M6 29c3 0 3-1.6 6-1.6s3 1.6 6 1.6 3-1.6 6-1.6 3 1.6 6 1.6 3-1.6 4-1.6" stroke="#19A7CE" stroke-width="1.4" fill="none"/></svg>'
WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z"/></svg>'
DIV = lambda a="#E4F5FA", b="#DFF3F8": f'<div class="divider" aria-hidden="true"><svg viewBox="0 0 2880 70" preserveAspectRatio="none"><path fill="{a}" fill-opacity=".55" d="M0 38 C240 8 480 8 720 38 S1200 68 1440 38 S1920 8 2160 38 S2640 68 2880 38 V70 H0Z"/><path fill="{b}" d="M0 46 C240 22 480 70 720 46 S1200 22 1440 46 S1920 70 2160 46 S2640 22 2880 46 V70 H0Z"/></svg></div>'
BUB = '<div class="bubbles" aria-hidden="true">' + "".join(
    f'<span style="--x:{x}%;--s:{s}px;--d:{d}s;--dl:{dl}s"></span>' for x, s, d, dl in
    [(4,10,13,0),(12,16,17,3),(21,8,11,6),(33,14,15,1),(45,9,12,8),(57,18,19,2),(66,10,14,5),(74,13,16,9),(83,8,10,4),(92,15,18,7)]) + "</div>"

NAV = [("index.html","home","Home"),("products.html","products","Products"),("quality.html","quality","Quality &amp; risk"),
       ("sourcing.html","sourcing","Suppliers"),("markets.html","markets","Logistics"),("guide.html","guide","Export guide"),("contact.html","contact","Contact")]

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "alternateName": SHORT, "url": SITE + "/",
       "logo": SITE + "/assets/img/logo.png",
       "description": f"{BRAND} is a buyer's broker that sources frozen, chilled, live and dried seafood and Bangladeshi food products from licensed exporters for importers worldwide, with five-gate QC on every lot. Mission: to be the best broker in the world for food importers.",
       "areaServed": "Worldwide", "address": {"@type": "PostalAddress", "addressCountry": "BD"},
       "knowsAbout": ["Bangladesh seafood export", "Black tiger shrimp", "Hilsa", "Mud crab", "HS 0306", "HS 0303", "Cold chain logistics"],
       "contactPoint": {"@type": "ContactPoint", "contactType": "sales", "availableLanguage": ["English", "Bengali", "Arabic"]}}


def crumbs_ld(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": f"{SITE}/{path}"}]}


def faq_ld(faqs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}


def head(title, desc, path, ld=(), og="iced-snapper.jpg"):
    graph = {"@context": "https://schema.org", "@graph": [ORG, *ld]}
    url = f"{SITE}/{'' if path == 'index.html' else path}"
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{E(title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{E(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:site_name" content="{BRAND}">
<meta property="og:title" content="{E(title)}">
<meta property="og:description" content="{E(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/{V}{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F5FBFD">
<link rel="alternate" type="text/plain" title="LLM summary" href="/llms.txt">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400;1,8..60,600&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap">
<link rel="stylesheet" href="assets/css/site.css">
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>'''


def header(page):
    links = "\n      ".join(f'<a href="{h}" data-nav="{k}">{t}</a>' for h, k, t in NAV[1:])
    return f'''<body data-page="{page}">
<a class="skip" href="#main">Skip to content</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="index.html" aria-label="{BRAND} home">{LOGO}<span><span data-brand>{BRAND}</span><small>Bangladesh seafood &amp; food export</small></span></a>
    <nav class="nav" id="nav" aria-label="Main">
      {links}
    </nav>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav">Menu</button>
    <a class="btn btn-primary cta-top" href="contact.html#rfq" data-track="cta_header">Request a quote <span class="flag" data-basket-count hidden style="background:#fff;color:var(--coral-ink)">0</span></a>
  </div>
</header>
<main id="main">'''


def page_hero(crumb, title, lede, video, level="0.74", extra=""):
    return f'''  <section class="vid page-hero">
    <video class="bg" data-auto autoplay muted loop playsinline preload="auto" poster="{V}{video}.jpg" aria-hidden="true"><source src="{V}{video}.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="{level}" aria-hidden="true"></canvas>
    <div class="wrap">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span>{crumb}</span></nav>
      <h1>{title}</h1>
      <p class="lede">{lede}</p>{extra}
    </div>
  </section>'''


def tile(vid, title, detail, tall=False):
    return f'''<button class="tile{' tall' if tall else ''}" type="button" data-play="{V}{vid}.mp4" data-title="{title}">
          <video data-auto muted loop playsinline preload="none" poster="{V}{vid}.jpg" aria-hidden="true"><source src="{V}{vid}.mp4" type="video/mp4"></video>
          <span class="cap"><span><b>{title}</b><span>{detail}</span></span><i aria-hidden="true"></i></span>
        </button>'''


def faq_html(faqs, heading="Questions buyers ask first"):
    items = "\n".join(f"<details><summary>{E(q)}</summary><p>{E(a)}</p></details>" for q, a in faqs)
    return f'''  <section id="faq">
    <div class="wrap">
      <p class="eyebrow">FAQ</p>
      <h2 style="margin:.8rem 0 2rem">{heading}</h2>
      <div class="faq">{items}</div>
    </div>
  </section>'''


def cta_band(video, eyebrow, title, lede, label="Request a quote"):
    return f'''  <section class="vid center cta-band">
    <video class="bg" data-auto muted loop playsinline preload="none" poster="{V}{video}.jpg" aria-hidden="true"><source src="{V}{video}.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="0.8" data-rays="off" aria-hidden="true"></canvas>
    <div class="wrap">
      <p class="eyebrow">{eyebrow}</p>
      <h2>{title}</h2>
      <p class="lede">{lede}</p>
      <div class="actions">
        <a class="btn btn-primary" href="contact.html#rfq" data-track="cta_band">{label}</a>
        <a class="btn btn-wa" href="#" data-wa="Hello {BRAND}, I'd like a price offer." data-track="whatsapp_click">{WA} WhatsApp us</a>
      </div>
    </div>
  </section>'''


FOOT = f'''</main>

<footer>
  <div class="wrap foot-grid">
    <div>
      <a class="logo" href="index.html" style="color:var(--fg)">{LOGO}<span><span data-brand>{BRAND}</span><small>Bangladesh seafood &amp; food export</small></span></a>
      <p style="margin-top:1rem;max-width:36ch">We source seafood and food from licensed Bangladeshi exporters and manage quality, documents and cold chain for importers worldwide.</p>
    </div>
    <div><h4>Explore</h4><ul><li><a href="products.html">Product directory</a></li><li><a href="sourcing.html">Supplier network</a></li><li><a href="quality.html">Quality &amp; compliance</a></li><li><a href="markets.html">Markets &amp; logistics</a></li><li><a href="guide.html">Bangladesh export guide</a></li></ul></div>
    <div><h4>Work with us</h4><ul><li><a href="contact.html#rfq">Request a quote</a></li><li><a href="sourcing.html#apply">Become a supplier partner</a></li><li><a href="#" data-wa="Hello {BRAND}" data-track="whatsapp_click">WhatsApp</a></li><li><a href="#" data-messenger data-track="messenger_click">Messenger</a></li><li><a href="#" data-mail data-track="email_click">Email</a></li></ul></div>
    <div><h4>Office</h4><p>Dhaka, Bangladesh<br>Sunday–Thursday, 09:00–18:00 (UTC+6)<br>WhatsApp answered 7 days</p></div>
  </div>
  <div class="foot-bottom"><div class="wrap" style="padding-block:1.25rem calc(1.25rem + env(safe-area-inset-bottom,0px))">
    <span>© <span data-year>{TODAY[:4]}</span> {BRAND}</span>
    <span>Product information is indicative. HS codes and market access are confirmed per shipment.</span>
  </div></div>
</footer>

<a class="wa-float" href="#" data-wa="Hello {BRAND}, I have a question about sourcing from Bangladesh." data-track="whatsapp_click" aria-label="Chat on WhatsApp">{WA}</a>
<div class="cookie" id="cookie" hidden>
  <span>We use first-party analytics to see which products buyers look at. No advertising trackers.</span>
  <div><button class="btn btn-primary" id="ckYes" type="button">Accept</button><button class="btn btn-ghost" id="ckNo" type="button">Decline</button></div>
</div>
<div class="lightbox" id="lightbox" hidden role="dialog" aria-modal="true" aria-label="Video player">
  <button class="close" type="button">Close ✕</button>
  <div><video controls playsinline></video><p></p></div>
</div>
<div class="toast" id="toast" hidden></div>
<script src="assets/js/catalog.js"></script>
<script src="assets/js/site.js"></script>
</body>
</html>
'''


def item(p):
    pid, cat, name, local, sci, hs, forms, markets, note, _ = p
    search = " ".join([name, local, sci, hs, forms, markets, CAT[cat][1]]).lower()
    sub = f'<i>{E(sci)}</i>' + (f' · {E(local)}' if local else "")
    return f'''        <article class="item" id="p-{pid}" data-cat="{cat}" data-search="{E(search)}">
          <div class="item-main"><h3>{E(name)}</h3><p class="sci">{sub}</p>{f'<p class="note">{E(note)}</p>' if note else ''}</div>
          <dl><div><dt>HS</dt><dd class="mono">{E(hs)}</dd></div><div><dt>Forms</dt><dd>{E(forms)}</dd></div><div><dt>Main markets</dt><dd>{E(markets)}</dd></div></dl>
          <button class="add" type="button" data-add="{pid}" aria-pressed="false">Add to quote</button>
        </article>'''


def directory():
    out = []
    for cid, title, group, intro in CATEGORIES:
        items = [p for p in P if p[1] == cid]
        out.append(f'''      <section class="cat" id="cat-{cid}" data-group="{group}">
        <div class="cat-head"><h2>{E(title)} <span class="count">{len(items)}</span></h2><p>{E(intro)}</p></div>
{chr(10).join(item(p) for p in items)}
      </section>''')
    return "\n".join(out)


def featured():
    cards = []
    for p in [p for p in P if p[-1]]:
        pid, cat, name, local, sci, hs, forms, markets, note, _ = p
        cards.append(f'''        <article class="spec">
          <div class="spec-top"><div><p class="local">{E(CAT[cat][1])}</p><h3><a href="products.html#p-{pid}">{E(name)}</a></h3><div class="latin">{E(sci)}{(' · ' + E(local)) if local else ''}</div></div></div>
          <table><tr><th>Forms</th><td>{E(forms)}</td></tr><tr><th>Markets</th><td>{E(markets)}</td></tr></table>
          <div class="spec-foot"><span class="hs">HS {E(hs)}</span><button class="add" type="button" data-add="{pid}" aria-pressed="false">Add to quote</button></div>
        </article>''')
    return "\n".join(cards)


RISKS = [
 ("Border rejection for residues", "Antibiotic or chemical residues found at the importing border; the container is destroyed or returned.", "Plant residue history reviewed; every lot tested for nitrofurans, chloramphenicol, malachite green and heavy metals at an accredited lab.", "Lab certificate for the exact lot, before shipment"),
 ("Plant not approved for your market", "The plant is missing from the EU, SFDA, GACC or FDA list, so the consignment is refused.", "Current listing checked at contract and again before loading.", "Screenshot or extract of the official list"),
 ("Quality below specification", "Wrong count or grade, soft texture or black spot, so your customers complain or reject.", "Gates 2 and 4: in-process checks and AQL pre-shipment inspection against your specification.", "Inspection report with photos and video; your approval before loading"),
 ("Short weight or excess glaze", "You pay for ice instead of product.", "Glaze % fixed in the contract; deglazed net weight checked on sample cartons.", "Weight and glaze table in the inspection report"),
 ("Species substitution or mislabelling", "A cheaper species or wrong label, which breaks labelling law.", "Species checked at receiving and packing; DNA testing on request.", "Species declaration; DNA result on request"),
 ("Temperature abuse", "Thawing and refreezing in transit cause quality loss and food-safety risk.", "Core temperatures logged; reefer pre-cooled and set point verified at loading; supervised loading.", "Loading temperature log and the carrier's reefer data"),
 ("Wrong or missing documents", "Customs holds, demurrage, or loss of preferential duty.", "Document checklist per market; you approve drafts before originals are issued.", "Draft set: invoice, packing list, health certificate, origin statement, B/L"),
 ("Illegal or unreported catch (IUU)", "Wild-caught fish refused under the EU IUU regulation.", "Catch certificate validated by the Department of Fisheries for wild-caught marine fish.", "Validated catch certificate"),
 ("Payment or fraud risk", "Advance paid to the wrong party, or goods not shipped.", "Exporter identity and bank account verified; L/C at sight or payment against documents.", "Verified exporter details in the proforma invoice"),
 ("Supplier default or delay", "The plant cannot deliver on time, so your shelves run empty.", "A second qualified plant held for each product; production slot confirmed in writing.", "Production schedule and weekly status updates"),
 ("Price volatility", "Raw material prices move between offer and contract.", "Price validity stated in every offer; seasonal booking advice; supply programmes at agreed prices.", "Written offer with validity date"),
 ("Export restrictions", "Products such as hilsa or aromatic rice can face permits, quotas or bans.", "Current export policy checked before we offer.", "Policy confirmation in the offer"),
 ("Claims after arrival", "A quality issue found at destination.", "Claim procedure written into the contract; we respond within 48 hours and pursue the exporter on your behalf.", "Written claim outcome: credit note or replacement"),
]

# ------------------------------------------------------------------ FAQs
FAQ_HOME = [
 ("What does Worldclass Bengal Fishers do?", f"{BRAND} is a Bangladesh-based sourcing and export partner that buys on the importer's behalf. We negotiate with licensed Bangladeshi plants, enforce five QC gates on every lot, check compliance for your market and manage documents and shipment, so each container lands at a profitable price."),
 ("Who does WBF represent?", "The buyer. We work to your specification, carry out QC on your behalf and release a shipment only when it meets the order you placed."),
 ("How does WBF lower my landed cost?", "By buying directly from processing plants, getting competing quotes from several qualified plants, loading containers to their payload limit, specifying glaze so you pay for fish rather than ice, and using preferential duty access for Bangladeshi origin where your market grants it."),
 ("How do you reduce supply risk?", "We only use plants whose licence and market listing we have checked, qualify a backup plant for each product, use L/C or document-based payment, and require independent pre-shipment inspection before the container is sealed."),
 ("Which seafood does Bangladesh export?", "Mainly frozen black tiger shrimp and giant freshwater prawn (HS 0306), frozen marine fish such as hilsa, pomfret and ribbonfish (HS 0303), chilled freshwater fish (HS 0302), live mud crab and eel (HS 0301) and dried fish (HS 0305)."),
 ("What is the minimum order?", "Usually one 20-foot reefer for a single product, or one 40-foot reefer split across up to four products. Samples and trial lots can be arranged."),
 ("Which payment terms are used?", "Irrevocable L/C at sight or T/T with a deposit. Terms are agreed with the exporter in the proforma invoice."),
 ("How fast do you quote?", "Within 24 hours of receiving species, cut, grade, packing, quantity and destination port."),
]
FAQ_GUIDE = [
 ("How many seafood exporters are registered in Bangladesh?", f"WBF's mapping of the Export Promotion Bureau directory lists {NET['mapped']} registered seafood and fisheries exporters across {NET['districts']} districts. Dhaka (37), Khulna (33) and Chattogram (29) together account for about two-thirds."),
 ("Who certifies Bangladeshi fish for export?", "The Department of Fisheries' Fish Inspection and Quality Control (FIQC) wing licenses fish export plants and issues health certificates. Plants must also be on the importing country's approved list, for example the EU list of approved establishments, the SFDA list for Saudi Arabia or GACC registration for China."),
 ("What are the HS codes for Bangladeshi seafood?", "0301 live fish (including eel), 0302 fresh or chilled fish, 0303 frozen fish, 0304 fillets, 0305 dried or salted fish, 0306 crustaceans (shrimp, prawn, crab) and 0307 molluscs (squid, cuttlefish)."),
 ("Can hilsa be exported from Bangladesh?", "Only with a government permit, within quotas and seasons that the government announces. Volumes and timing change each year."),
 ("Which trade associations represent Bangladeshi seafood exporters?", "BFFEA (Bangladesh Frozen Foods Exporters Association) for shrimp and frozen fish processors, BLCFEA (Bangladesh Live & Chilled Food Exporters Association) for live crab and eel, and BMFA (Bangladesh Marine Fisheries Association) for deep-sea fishing companies."),
]
FAQ_SUP = [
 ("Who can join the WBF supplier network?", "Bangladeshi exporters with a valid export licence and, for fish, a DoF FIQC-approved plant. Approvals for target markets (EU, SFDA, GACC, US FDA) and certifications such as HACCP or BRCGS raise your priority."),
 ("Do you share buyer details?", "Buyer details are shared after a signed NCNDA (non-circumvention, non-disclosure agreement) and commission agreement."),
 ("Is there a fee to join?", "No. WBF earns an agreed commission on completed shipments."),
]
FAQ_MARKETS = [
 ("How long does a reefer take from Chattogram to Europe?", "Typically 28–35 days to Rotterdam, Antwerp or Hamburg via a transshipment hub such as Colombo or Singapore."),
 ("Which Incoterms do you quote?", "FOB Chattogram, CFR or CIF to your port. Air freight for live crab, eel, chilled fish and fresh produce is quoted CPT or CIP to the destination airport."),
 ("How many cartons fit in a 40-foot reefer?", "About 1,900–2,100 master cartons of 10 kg frozen shrimp, or roughly 19–21 tonnes net, depending on carton size."),
]


# ------------------------------------------------------------------ PAGES
def write(name, text):
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(text)
    print("wrote", name, len(text))


def build():
    # ---------- HOME
    home = head(f"{BRAND} | Bangladesh Seafood & Food Exporter",
                f"Source shrimp, hilsa, pomfret, mud crab, pangasius and {N_PRODUCTS} Bangladeshi seafood and food products from licensed exporters. Quotes in 24 hours, FOB or CFR.",
                "index.html", [{"@type": "WebSite", "@id": SITE + "/#web", "url": SITE + "/", "name": BRAND, "publisher": {"@id": SITE + "/#org"}}, faq_ld(FAQ_HOME)]) + header("home") + f'''
  <section class="hero vid" style="padding:0">
    <video class="bg" data-auto autoplay muted loop playsinline preload="auto" poster="{V}iced-snapper.jpg" aria-hidden="true"><source src="{V}iced-snapper.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="0.7" aria-hidden="true"></canvas>
    <div class="wrap">
      <div>
        <p class="eyebrow">Our mission: the best broker in the world for food importers</p>
        <h1>Better margins on Bangladeshi seafood, <em>with the risk taken out</em>.</h1>
        <p class="lede">{BRAND} buys for importers, distributors and retailers from the best-qualified plants in Bangladesh. We negotiate price at source, enforce strict QC on every lot and keep every shipment compliant with your market, so each container sells at a profit and the next order is easy.</p>
        <div class="actions">
          <a class="btn btn-primary" href="contact.html#rfq" data-track="cta_hero">Request a price offer</a>
          <a class="btn btn-ghost" href="products.html" style="color:var(--fg)">Browse {N_PRODUCTS} products</a>
        </div>
        <div class="trust-row"><span>Price negotiated at source</span><span>Five-gate QC on every lot</span><span>Compliant for your market</span></div>
      </div>
      <aside class="reefer" aria-label="Example reefer container readout">
        <div class="reefer-head"><span>Reefer · example shipment</span><span class="live"><i></i>Live</span></div>
        <div class="temp" id="reeferTemp">−20.1<small> °C</small></div>
        <div class="sub">Set point −20.0 °C · Return air</div>
        <dl>
          <dt>Cargo</dt><dd>HLSO Black tiger 16/20</dd>
          <dt>Pack</dt><dd>6 × 1.8 kg block</dd>
          <dt>Net weight</dt><dd>21,600 kg</dd>
          <dt>Cartons</dt><dd>2,000</dd>
          <dt>Humidity</dt><dd id="reeferHum">87 %</dd>
        </dl>
        <div class="route">
          <div style="display:flex;justify-content:space-between"><span>CGP Chattogram</span><span>RTM Rotterdam</span></div>
          <div class="track"><b></b></div>
          <div style="margin-top:.5rem">Day 19 of 31 · via Colombo</div>
        </div>
        <p class="note">Example readout. Buyers receive the carrier's reefer data for each shipment.</p>
      </aside>
    </div>
  </section>

  <section style="padding-block:3.5rem">
    <div class="wrap">
      <div class="statband">
        <div><b>{NET['mapped']}</b><span>licensed seafood exporters mapped</span><cite>EPB directory</cite></div>
        <div><b>{NET['districts']}</b><span>sourcing districts, coast to haor</span><cite>WBF research</cite></div>
        <div><b>{N_PRODUCTS}</b><span>export products in our directory</span><cite>{N_FISH} seafood · {N_FOOD} food</cite></div>
        <div><b>24 h</b><span>quote turnaround</span><cite>Working days</cite></div>
      </div>
    </div>
  </section>

  <section id="why" style="padding-top:1rem">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">The buyer wins first</p><h2>Your margin, protected at every step.</h2></div>
        <p class="lede">We only succeed when you do. We earn your next order by making this one profitable: the right price at source, the right quality on arrival, and none of the risks that eat into margin in between.</p>
      </div>
      <div class="promise" style="margin:0 0 2rem">
        <div><b>Win on price</b><span>A landed cost that lets you compete in your market.</span></div>
        <div><b>Win on quality</b><span>Every carton matches the specification you sold to your customers.</span></div>
        <div><b>Win again</b><span>Reliable supply programmes that keep your customers re-ordering.</span></div>
      </div>
      <div class="pillars">
        <article><span class="pn">01</span><h3>Better landed cost</h3><ul>
          <li>Prices negotiated directly with the processing plant, without layers of traders</li>
          <li>Several qualified plants quote each order, so you get a competitive price</li>
          <li>Containers loaded to the payload limit and glaze specified, so you pay for fish, not ice</li>
          <li>Preferential duty access for Bangladeshi origin into the EU, UK and other markets (confirm per shipment)</li>
        </ul></article>
        <article><span class="pn">02</span><h3>Lower risk</h3><ul>
          <li>Only plants whose licence and market listing we have checked</li>
          <li>Payment by L/C at sight or T/T against documents</li>
          <li>Independent pre-shipment inspection before the container is sealed</li>
          <li>A backup plant qualified for each product, so supply continues if one plant falls short</li>
        </ul></article>
        <article><span class="pn">03</span><h3>Compliance by market</h3><ul>
          <li>Plant listed for your market: EU, SFDA, GACC or US FDA</li>
          <li>Residue, heavy metal and microbiology results for the exact lot</li>
          <li>Health certificate, certificate of origin and labels checked before loading</li>
          <li>Fewer border holds, rejections and demurrage charges</li>
        </ul></article>
        <article><span class="pn">04</span><h3>Strict QC, every lot</h3><ul>
          <li>Five QC gates from raw material to loading (<a href="quality.html#qc-gates">see the gates</a>)</li>
          <li>Count, glaze and net weight checked against your specification</li>
          <li>Photos, videos and the lab report sent to you before shipment</li>
          <li>Quality claims answered within 48 hours</li>
        </ul></article>
      </div>
      <div class="broker">
        <div><p class="eyebrow">We work for the buyer</p><h3>Your broker in Bangladesh, on your side of the table.</h3>
        <p>Every lot shipped through WBF passes all five QC gates and a full document check before the container is sealed. We control 13 food-import risks, from border residues to payment fraud, and send you the evidence for each.</p></div>
        <a class="btn btn-navy" href="quality.html#risk">See the import risk controls</a>
      </div>
    </div>
  </section>

  <section id="compare">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">What sets WBF apart</p><h2>Built to be the world's best broker for buyers.</h2></div>
        <p class="lede">That is our standard, and this is how we hold ourselves to it. Most intermediaries pass on an offer and a certificate. We take responsibility for what arrives at your port.</p>
      </div>
      <div class="tbl"><table class="dtable compare">
        <thead><tr><th></th><th>Typical trading intermediary</th><th class="us">Worldclass Bengal Fishers</th></tr></thead>
        <tbody>
          <tr><td>Who we act for</td><td>Usually the seller</td><td class="us">The buyer: your specification and your approval</td></tr>
          <tr><td>Quality control</td><td>The exporter's own certificate</td><td class="us">Five QC gates on every lot, by our officers or an independent inspector</td></tr>
          <tr><td>Evidence before you pay</td><td>Documents after shipment</td><td class="us">Lab report, inspection photos and video before the balance payment</td></tr>
          <tr><td>Market compliance</td><td>Assumed</td><td class="us">Plant listing for your market checked at contract and again before loading</td></tr>
          <tr><td>Pricing</td><td>One bundled price</td><td class="us">Competing plant quotes, with FOB, freight, insurance and duty shown separately</td></tr>
          <tr><td>Supply security</td><td>One supplier</td><td class="us">A second qualified plant held for each product</td></tr>
          <tr><td>Claims</td><td>Buyer chases the exporter</td><td class="us">Answered within 48 hours; we pursue the exporter on your behalf</td></tr>
          <tr><td>Risk coverage</td><td>Not documented</td><td class="us">13 import risks controlled, with evidence for each (<a href="quality.html#risk">see the table</a>)</td></tr>
        </tbody>
      </table></div>
    </div>
  </section>

  <section id="profit" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Recurring profitability</p>
        <h2 style="margin:.7rem 0 1.2rem">Plan the margin before you order.</h2>
        <p class="lede">Enter your numbers to see the landed cost and margin per container. When you send a request, we work to the target landed price your market needs.</p>
        <ul class="ticks">
          <li><b>Supply programmes:</b> monthly or quarterly containers at agreed volumes, so your shelves stay full.</li>
          <li><b>Seasonal buying advice:</b> we tell you when to book harvest-season grades at the best price.</li>
          <li><b>Consistent specification:</b> the same count, glaze and packing on every shipment, so customers keep re-ordering.</li>
          <li><b>Open costing:</b> FOB, freight, insurance and duty shown separately in every offer.</li>
        </ul>
      </div>
      <form class="calc" id="landed" onsubmit="return false" aria-labelledby="landedTitle">
        <p class="eyebrow">Landed cost &amp; margin</p>
        <h3 id="landedTitle" style="margin-top:.4rem">Per 40′ reefer</h3>
        <div class="row">
          <div class="f"><label for="lFob">FOB price (US$/kg)</label><input id="lFob" type="number" step="0.05" min="0" value="8.40" inputmode="decimal"></div>
          <div class="f"><label for="lKg">Net weight (kg)</label><input id="lKg" type="number" step="100" min="0" value="20000" inputmode="numeric"></div>
          <div class="f"><label for="lFreight">Ocean freight (US$)</label><input id="lFreight" type="number" step="50" min="0" value="4200" inputmode="numeric"></div>
          <div class="f"><label for="lDuty">Import duty (%)</label><input id="lDuty" type="number" step="0.1" min="0" value="0" inputmode="decimal"></div>
          <div class="f"><label for="lLocal">Clearance &amp; local costs (US$)</label><input id="lLocal" type="number" step="50" min="0" value="1800" inputmode="numeric"></div>
          <div class="f"><label for="lSell">Your selling price (US$/kg)</label><input id="lSell" type="number" step="0.05" min="0" value="10.90" inputmode="decimal"></div>
        </div>
        <div class="out" aria-live="polite">
          <div><b id="lLanded">—</b><span>landed US$/kg</span></div>
          <div><b id="lMargin">—</b><span>gross margin</span></div>
          <div><b id="lProfit">—</b><span>gross profit per container</span></div>
        </div>
        <p class="hint" style="margin-top:.9rem">Example figures. Insurance is calculated at 0.3 % of CFR value. Duty depends on product, origin rules and your market. Confirm with your customs broker.</p>
        <button class="btn btn-ghost" style="margin-top:.8rem" id="landedToRfq" type="button">Send these targets with my request</button>
      </form>
    </div>
  </section>

  <section id="catch" style="padding-top:2rem">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">From the source</p><h2>Landed in the morning, iced within the hour.</h2></div>
        <p class="lede">Footage from landing points and receiving halls in Bangladesh. Select any clip to watch it full screen.</p>
      </div>
      <div class="reel">
        {tile('school-underwater','Bay of Bengal','Wild-caught marine species',True)}
        {tile('iced-snapper','Red snapper','Whole round · 0–2 °C on ice')}
        {tile('catch-carp','Rohu &amp; Indian carp','Morning landing · graded by weight')}
        {tile('catch-pangasius','Pangasius','Farm harvest · to plant in 3 h')}
        {tile('ice-holding','Ice holding','Flake ice 1:1 · core ≤ 4 °C')}
      </div>
    </div>
  </section>

  <section id="products" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Most requested</p><h2>What importers source from Bangladesh.</h2></div>
        <p class="lede">A selection from our directory of {N_PRODUCTS} products. Add items here and they carry through to your quote request.</p>
      </div>
      <div class="grid">
{featured()}
      </div>
      <div class="more"><a class="btn btn-navy" href="products.html">Open the full product directory</a></div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">How it works</p><h2>One partner from enquiry to arrival.</h2></div>
        <p class="lede">You deal with one team in Bangladesh. We coordinate the exporter, the inspection company, the shipping line and the documents.</p>
      </div>
      <ol class="steps">
        <li><h3>Specify</h3><p>Tell us the species, cut, grade, packing, volume and port. We reply with a price offer within 24 hours.</p></li>
        <li><h3>Match</h3><p>We shortlist exporters whose plants hold the approvals your market requires.</p></li>
        <li><h3>Sample &amp; contract</h3><p>Samples are couriered on dry ice. Proforma invoice, then payment by L/C or T/T.</p></li>
        <li><h3>Inspect</h3><p>Pre-shipment inspection by SGS, Bureau Veritas or Intertek, with lab results for each lot.</p></li>
        <li><h3>Ship</h3><p>Reefer booked and sealed at the plant. You receive the shipping documents and the carrier's temperature data.</p></li>
        <li><h3>Support</h3><p>We follow up at destination and handle any quality claim with the exporter within 48 hours.</p></li>
      </ol>
    </div>
  </section>

{faq_html(FAQ_HOME)}

{cta_band('school-underwater','Next sailing from Chattogram','Ready to source your next container?','Send species, grade, packing and port. You receive a CFR or FOB price offer within 24 hours.')}
''' + FOOT
    write("index.html", home)

    # ---------- PRODUCT DIRECTORY
    chips = '<button class="chip" aria-pressed="true" data-filter="all">All <span>' + str(N_PRODUCTS) + '</span></button>' + "".join(
        f'<button class="chip" aria-pressed="false" data-filter="{c}">{E(t)} <span>{sum(1 for p in P if p[1]==c)}</span></button>' for c, t, g, i in CATEGORIES)
    item_list = {"@type": "ItemList", "name": "Bangladesh export product directory", "numberOfItems": N_PRODUCTS,
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/products.html#p-{p[0]}",
                                      "item": {"@type": "Product", "name": p[2], "description": f"{p[2]} ({p[4]}) from Bangladesh. HS {p[5]}. Forms: {p[6]}.",
                                               "category": CAT[p[1]][1], "countryOfOrigin": {"@type": "Country", "name": "Bangladesh"}}}
                                     for i, p in enumerate(P)]}
    prod = head("Bangladesh Export Product Directory: Seafood & Food | " + SHORT,
                f"Directory of {N_PRODUCTS} products exported from Bangladesh: shrimp, prawn, hilsa, pomfret, mud crab, eel, dried fish, rice, spices, vegetables, fruit and processed food, with HS codes and main markets.",
                "products.html", [crumbs_ld("Product directory", "products.html"), item_list], "catch-pangasius.jpg") + header("products") + "\n" + page_hero(
        "Product directory", "Bangladesh export product directory",
        f"{N_FISH} seafood and {N_FOOD} food products exported from Bangladesh, with scientific names, Bangla names, HS headings, product forms and main buyer markets.", "catch-pangasius") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> Bangladesh's main seafood exports are frozen shrimp and prawn (HS 0306), frozen marine fish (0303), chilled freshwater fish (0302), live crab and eel (0301) and dried fish (0305). Food exports include aromatic rice, spices, fresh vegetables, mango, frozen snacks and packaged foods.</p>
      <div class="dir-tools">
        <label class="sr" for="dirSearch">Search products</label>
        <input id="dirSearch" type="search" placeholder="Search by name, Bangla name, scientific name or HS code" autocomplete="off">
        <span class="hint" id="dirCount" aria-live="polite">{N_PRODUCTS} products</span>
      </div>
      <div class="filters" role="group" aria-label="Filter by category">{chips}</div>
      <p class="hint" id="dirEmpty" hidden>No products match. Try another spelling or <a href="contact.html#rfq">ask us to source it</a>.</p>
      <div class="directory">
{directory()}
      </div>
      <p class="src">HS headings are indicative (4-digit). The full 8-digit code is confirmed for each shipment. Market lists show typical destinations for Bangladeshi supply, not exclusive rights. Updated <time datetime="{TODAY}">{TODAY}</time>.</p>
    </div>
  </section>

{cta_band('iced-snapper','Not listed?','We source on request.','If it is produced in Bangladesh, our exporter network can usually quote it. Tell us what you need.','Ask us to source a product')}
''' + FOOT
    write("products.html", prod)

    # ---------- SUPPLIER NETWORK
    maxd = max(n for _, n in DISTRICTS)
    bars = "\n".join(f'<li><span>{E(d)}</span><span class="bar"><i style="width:{n/maxd*100:.0f}%"></i></span><b>{n}</b></li>' for d, n in DISTRICTS)
    hsrows = "\n".join(f'<tr><td class="mono">{h}</td><td>{E(t)}</td><td>{E(k)}</td><td class="num">{n}</td></tr>' for h, t, n, k in HSCATS)
    sup = head(f"Bangladesh Supplier Network: Licensed Seafood Exporters | {SHORT}",
               f"How {BRAND} selects Bangladeshi seafood and food exporters: {NET['mapped']} licensed exporters mapped, approval checks (DoF FIQC, EU, SFDA, GACC) and a priority rating. Exporters can apply to join.",
               "sourcing.html", [crumbs_ld("Supplier network", "sourcing.html"), faq_ld(FAQ_SUP)], "catch-carp.jpg") + header("sourcing") + "\n" + page_hero(
        "Supplier network", "A vetted network of Bangladesh's licensed exporters.",
        f"We have mapped {NET['mapped']} registered seafood exporters across {NET['districts']} districts and rate every supplier against the approvals and records your market requires.", "catch-carp",
        extra='\n      <div class="actions" style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:.6rem"><a class="btn btn-primary" href="#apply">Apply as a supplier</a><a class="btn btn-ghost" href="contact.html#rfq" style="color:var(--fg)">Source through WBF</a></div>') + f'''

  <section style="padding-top:2rem">
    <div class="wrap">
      <div class="statband">
        <div><b>{NET['mapped']}</b><span>registered seafood exporters mapped</span><cite>EPB directory</cite></div>
        <div><b>{NET['shortlisted']}</b><span>exporters on our shortlist</span><cite>WBF research, Oct 2026</cite></div>
        <div><b>{NET['tier_a']}</b><span>Priority A: on an official approval list or BFFEA leadership</span><cite>SFDA list · BFFEA</cite></div>
        <div><b>5</b><span>HS categories covered</span><cite>0301 – 0306</cite></div>
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Where exporters are</p>
        <h2 style="margin:.6rem 0 1.5rem">Registered exporters by district</h2>
        <ul class="bars">{bars}</ul>
        <p class="src">Source: Export Promotion Bureau (EPB) directory of seafood and fisheries exporters, compiled by WBF. n = {NET['mapped']}.</p>
      </div>
      <div>
        <p class="eyebrow">What they export</p>
        <h2 style="margin:.6rem 0 1.5rem">Exporters by product category</h2>
        <div class="tbl"><table class="dtable"><thead><tr><th>HS</th><th>Category</th><th>Key items</th><th style="text-align:right">Exporters</th></tr></thead><tbody>{hsrows}</tbody></table></div>
        <p class="src">Many exporters ship more than one category, so the column adds up to more than {NET['mapped']}.</p>
      </div>
    </div>
  </section>

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">How we rate suppliers</p><h2>Three priority tiers, checked before every deal.</h2></div>
        <p class="lede">A rating is where we start, not a guarantee. Before any contract we ask for a current DoF fish export licence and proof of listing for the buyer's market.</p>
      </div>
      <div class="tiers">
        <div class="tier"><span class="badge">PRIORITY A</span><h3>Approved &amp; established</h3><p>On an official approval list (for example SFDA) or in BFFEA leadership, with products that match current buyer demand.</p><b class="n">{NET['tier_a']}</b></div>
        <div class="tier b"><span class="badge">PRIORITY B</span><h3>Credible, to confirm</h3><p>An established exporter with a narrower range, or with details still to confirm.</p><b class="n">{NET['tier_b']}</b></div>
        <div class="tier c"><span class="badge">PRIORITY C</span><h3>Verify first</h3><p>Found in a database only, or a very narrow range. We verify the licence before any deal.</p><b class="n">{NET['tier_c']}</b></div>
      </div>
      <h3 style="margin:3rem 0 1rem">What we check</h3>
      <ol class="steps">
        <li><h3>Licence</h3><p>A current DoF Fish Inspection &amp; Quality Control (FIQC) export licence and plant approval number.</p></li>
        <li><h3>Market listing</h3><p>The plant appears on the importing market's list: EU approved establishments, SFDA, GACC or US FDA.</p></li>
        <li><h3>Certification</h3><p>HACCP is required. BRCGS, ISO 22000, BAP, ASC and Halal are recorded where held.</p></li>
        <li><h3>Lab capability</h3><p>Antibiotic residue, heavy metal and microbiology testing per lot, in-house or at an accredited lab.</p></li>
        <li><h3>Track record</h3><p>Shipment history, claims record and references from existing buyers.</p></li>
        <li><h3>Agreement</h3><p>A signed NCNDA and commission agreement before any buyer details are shared.</p></li>
      </ol>
    </div>
  </section>

  {DIV()}
  <section id="apply" class="band">
    {BUB}
    <div class="wrap rfq">
      <div>
        <p class="eyebrow">For Bangladeshi exporters</p>
        <h2 style="margin-top:.8rem">Join the WBF supplier network</h2>
        <p class="lede" style="margin-top:1.2rem">We bring you qualified buyers from Europe, the Gulf, East Asia and North America. Joining is free; we earn an agreed commission on completed shipments.</p>
        <ul class="contact-list">
          <li><span>You need</span><a>A valid export licence. For fish, a DoF FIQC-approved plant.</a></li>
          <li><span>We review</span><a>Within 3 working days. We call to confirm details.</a></li>
          <li><span>Then</span><a>NCNDA and commission agreement, then buyer introductions.</a></li>
        </ul>
      </div>
      <form class="rfq-form" id="supplierForm" novalidate>
        <div class="f"><label for="s_company">Company name</label><input id="s_company" name="company" required autocomplete="organization"></div>
        <div class="f"><label for="s_name">Contact person</label><input id="s_name" name="name" required autocomplete="name"></div>
        <div class="f"><label for="s_role">Designation</label><input id="s_role" name="designation" placeholder="e.g. Managing Director"></div>
        <div class="f"><label for="s_phone">Phone / WhatsApp</label><input id="s_phone" name="phone" type="tel" required placeholder="+880 1XXX-XXXXXX" autocomplete="tel"></div>
        <div class="f"><label for="s_email">Email</label><input id="s_email" name="email" type="email" required autocomplete="email"></div>
        <div class="f"><label for="s_district">District</label>
          <select id="s_district" name="district">{''.join(f'<option>{d}</option>' for d in ['Khulna','Chattogram','Dhaka','Bagerhat','Satkhira','Jashore',"Cox's Bazar",'Brahmanbaria','Sylhet','Sunamganj','Barishal','Mymensingh','Rajshahi','Other'])}</select></div>
        <div class="f"><label for="s_licence">DoF approval / export licence no.</label><input id="s_licence" name="licence" placeholder="e.g. KLN-57"></div>
        <div class="f"><label for="s_capacity">Monthly export capacity</label>
          <select id="s_capacity" name="capacity"><option value="<20">Under 20 MT</option><option value="20-100">20–100 MT</option><option value="100-500">100–500 MT</option><option value="500+">500 MT +</option></select></div>
        <fieldset class="f full checks-inline"><legend>Product categories</legend>
          {''.join(f'<label><input type="checkbox" name="categories" value="{c}"> {E(t)}</label>' for c, t, g, i in CATEGORIES)}
        </fieldset>
        <fieldset class="f full checks-inline"><legend>Approvals &amp; certifications held</legend>
          {''.join(f'<label><input type="checkbox" name="approvals" value="{a}"> {a}</label>' for a in ['EU approved list','SFDA (Saudi)','GACC (China)','US FDA','HACCP','BRCGS','ISO 22000','BAP','ASC','Halal'])}
        </fieldset>
        <div class="f full"><label for="s_web">Website</label><input id="s_web" name="website_url" type="url" placeholder="https://"></div>
        <div class="f full"><label for="s_notes">Main products and grades</label><textarea id="s_notes" name="notes" placeholder="e.g. HLSO black tiger 8/12–31/40, 6×1.8 kg block; silver pomfret IQF"></textarea></div>
        <label class="consent full" for="s_consent"><input type="checkbox" id="s_consent" name="consent" required> I confirm the information is accurate and agree that {BRAND} may store it to assess our application.</label>
        <input type="text" name="website" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
        <div class="full"><button class="btn btn-primary" type="submit" id="supplierSubmit">Submit application</button></div>
        <div class="status" id="supplierStatus" role="status" hidden></div>
      </form>
    </div>
  </section>

{faq_html(FAQ_SUP, "Supplier questions")}
''' + FOOT
    write("sourcing.html", sup)

    # ---------- QUALITY
    qual = head(f"Food Import Risk Control & QC for Bangladeshi Seafood | {SHORT}",
                "13 food-import risks controlled for buyers, five QC gates on every lot, lab testing (antibiotic residues, heavy metals, microbiology), DoF health certificates, EU/SFDA/GACC plant approvals and a −18 °C cold chain from pond to port.",
                "quality.html", [crumbs_ld("Quality & risk", "quality.html")], "ice-holding.jpg") + header("quality") + "\n" + page_hero(
        "Quality &amp; risk", "Every lot verified. Every import risk controlled.",
        "We act for the buyer. Every lot passes five QC gates and a document check before shipment, and you receive the evidence for each import risk.", "ice-holding") + f'''

  <section style="padding-top:2rem">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Testing &amp; documents</p><h2>Tested by lot, traceable to the pond.</h2></div>
        <p class="lede">Every shipment travels with a Department of Fisheries health certificate, a certificate of origin and the lab report for the exact lot you receive.</p>
      </div>
      <div class="quality">
        <div class="checks">
          <div><b>Antibiotic residues</b><span>Nitrofurans, chloramphenicol and malachite green by LC-MS/MS on every lot.</span></div>
          <div><b>Heavy metals</b><span>Lead, cadmium and mercury within EU Regulation 2023/915 limits.</span></div>
          <div><b>Microbiology</b><span>TPC, E. coli, Salmonella, Vibrio and Listeria before release.</span></div>
          <div><b>Sulphite-free on request</b><span>Melanosis control with 4-hexylresorcinol for EU and Japanese buyers.</span></div>
          <div><b>Net weight control</b><span>Deglazed weight checked to Codex CAC/GL 50 sampling.</span></div>
          <div><b>Private label</b><span>Retail bags and printed cartons to your artwork, barcodes and language.</span></div>
        </div>
        <div class="trace">
          <span class="sample-tag">Lot trace · sample code</span>
          <h3 style="margin-top:.5rem">Where did this carton come from?</h3>
          <form id="traceForm" autocomplete="off">
            <label class="sr" for="lot">Lot code</label>
            <input id="lot" name="lot" value="WBF-26-1187" aria-describedby="lotHint">
            <button class="btn btn-primary" type="submit">Trace lot</button>
          </form>
          <p class="hint" id="lotHint" style="margin-top:-.6rem;margin-bottom:1rem">The lot code is printed on the side of every master carton.</p>
          <ol class="timeline" id="traceOut"></ol>
        </div>
      </div>
    </div>
  </section>

  <section id="qc-gates" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Strict QC</p><h2>Five gates. A lot that fails any gate does not ship.</h2></div>
        <p class="lede">Our QC officers or an independent inspector check each gate against your purchase specification, not just the exporter's own standard.</p>
      </div>
      <ol class="gates">
        <li><span class="g">Gate 1</span><h3>Raw material</h3><p>Farm or landing records, residue screening of pond samples, and temperature on arrival at the plant (≤ 4 °C).</p></li>
        <li><span class="g">Gate 2</span><h3>Processing</h3><p>Count and grade, cut, deveining and freshness (organoleptic) checked in process. Sulphite-free where specified.</p></li>
        <li><span class="g">Gate 3</span><h3>Lab release</h3><p>Antibiotic residues, heavy metals and microbiology tested at an accredited lab for the exact lot.</p></li>
        <li><span class="g">Gate 4</span><h3>Pre-shipment inspection</h3><p>AQL sampling of cartons: deglazed net weight, count, glaze %, packing and labels, with photos and video sent to you.</p></li>
        <li><span class="g">Gate 5</span><h3>Loading</h3><p>Reefer pre-cooled and set point verified. Loading supervised, core temperatures logged, seal number recorded.</p></li>
      </ol>
      <p class="src">You receive the inspection report, lab certificate and loading photos before the balance payment or document release.</p>
    </div>
  </section>

  <section id="risk">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Import risk control</p><h2>13 risks a food importer faces, and how we control each one.</h2></div>
        <p class="lede">Before you pay the balance or the documents are released, you hold evidence for every line in this table.</p>
      </div>
      <div class="tbl"><table class="dtable risk">
        <thead><tr><th>Risk</th><th>What can go wrong</th><th>How WBF controls it</th><th>Evidence you receive</th></tr></thead>
        <tbody>{''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td><td>{E(d)}</td></tr>' for a, b, c, d in RISKS)}</tbody>
      </table></div>
      <p class="src">Risk can be reduced, not removed entirely. These controls are written into each purchase contract so responsibility is clear if something goes wrong.</p>
    </div>
  </section>

  {DIV()}
  <section id="cold-chain" class="band">
    {BUB}
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Cold chain · pond to port</p><h2>Six temperatures between the pond and your port.</h2></div>
        <p class="lede">Product is iced within an hour of harvest and kept below 4 °C until freezing. Each stage is logged against the lot code on the master carton.</p>
      </div>
      <ol class="chain">
        <li style="--grad:#B5E3DC"><span class="t">0–4°</span><span class="step">Step 1</span><h3>Harvest &amp; icing</h3><p>Flake ice 1:1 at the farm gate or landing point.</p></li>
        <li style="--grad:#9ED9D0"><span class="t">≤4°</span><span class="step">Step 2</span><h3>Depot &amp; grading</h3><p>Insulated trucks to the plant. Washed and size-graded.</p></li>
        <li style="--grad:#86CFC4"><span class="t">≤4°</span><span class="step">Step 3</span><h3>Processing</h3><p>Heading, peeling and deveining in a chilled hall.</p></li>
        <li style="--grad:#6FC5B9"><span class="t">−35°</span><span class="step">Step 4</span><h3>IQF / plate freeze</h3><p>Frozen until the core reaches −18 °C. Glaze as specified.</p></li>
        <li style="--grad:#58BBAE"><span class="t">−22°</span><span class="step">Step 5</span><h3>Cold storage</h3><p>Master cartons on pallets. Pre-shipment inspection.</p></li>
        <li style="--grad:#E0522F"><span class="t">−20°</span><span class="step">Step 6</span><h3>Reefer to port</h3><p>Loaded at the plant, sealed and tracked to destination.</p></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">At source</p><h2>Receiving and grading.</h2></div><p class="lede">Raw material is iced, graded and moved into the chilled processing hall the same morning.</p></div>
      <div class="reel" style="grid-template-rows:none;grid-template-columns:repeat(auto-fit,minmax(260px,1fr))">
        {tile('ice-holding','Ice holding','Flake ice 1:1 · core ≤ 4 °C')}
        {tile('iced-snapper','Red snapper','Graded and iced on arrival')}
        {tile('catch-carp','Carp grading','Sorted by weight class')}
      </div>
    </div>
  </section>
''' + FOOT
    write("quality.html", qual)

    # ---------- MARKETS
    mk = head(f"Markets, Shipping & Ordering from Bangladesh | {SHORT}",
              "Reefer transit times from Chattogram and Mongla to Europe, the UK, the Gulf, North America and East Asia, a container load planner, Incoterms and ordering steps.",
              "markets.html", [crumbs_ld("Markets & logistics", "markets.html"), faq_ld(FAQ_MARKETS)], "catch-carp.jpg") + header("markets") + "\n" + page_hero(
        "Markets &amp; logistics", "Weekly reefer sailings to 40+ countries.",
        "FOB Chattogram, CFR or CIF to your port, with typical transit times, a container load planner and our ordering steps.", "school-underwater") + f'''

  <section id="markets" style="padding-top:2rem">
    <div class="wrap">
      <div class="markets">
        <div class="tbl">
          <table class="ports">
            <thead><tr><th>Region</th><th>Main ports</th><th>Sea transit</th></tr></thead>
            <tbody>
              <tr><td>European Union</td><td>Rotterdam, Antwerp, Hamburg, Valencia</td><td class="mono">28–35 d</td></tr>
              <tr><td>United Kingdom</td><td>Felixstowe, London Gateway</td><td class="mono">30–35 d</td></tr>
              <tr><td>GCC</td><td>Jebel Ali, Dammam, Jeddah, Doha</td><td class="mono">14–20 d</td></tr>
              <tr><td>North America</td><td>New York/NJ, Savannah, Los Angeles, Vancouver</td><td class="mono">35–45 d</td></tr>
              <tr><td>East Asia</td><td>Tokyo, Busan, Shanghai, Hong Kong</td><td class="mono">18–26 d</td></tr>
              <tr><td>Air freight</td><td>Live crab, eel, chilled fish, vegetables, fruit from Dhaka (DAC)</td><td class="mono">1–3 d</td></tr>
            </tbody>
          </table>
          <p class="src">Typical transit times via Colombo or Singapore. Confirmed at booking.</p>
        </div>
        <div class="calc" id="calc">
          <p class="eyebrow">Load planner</p>
          <h3 style="margin-top:.5rem">How much fits in one reefer?</h3>
          <div class="row">
            <div class="f"><label for="cContainer">Container</label>
              <select id="cContainer"><option value="40">40′ reefer high cube</option><option value="20">20′ reefer</option></select></div>
            <div class="f"><label for="cPack">Master carton</label>
              <select id="cPack"><option value="block">6 × 1.8 kg block (10.8 kg)</option><option value="iqf" selected>10 × 1 kg IQF bags (10 kg)</option><option value="bulk">20 kg bulk IQF</option><option value="fish">Whole fish, 20 kg carton</option></select></div>
          </div>
          <div class="out" aria-live="polite">
            <div><b id="oCartons">—</b><span>cartons</span></div>
            <div><b id="oNet">—</b><span>net tonnes</span></div>
            <div><b id="oPallets">—</b><span>pallets (if palletised)</span></div>
          </div>
          <p class="hint" style="margin-top:1rem">Estimate, floor-loaded, using 88 % of internal volume and the container's payload limit. Exact loading is confirmed in the proforma invoice.</p>
          <button class="btn btn-ghost" style="margin-top:1rem" id="calcToRfq" type="button">Use this in my quote</button>
        </div>
      </div>
    </div>
  </section>

  <section id="ordering" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Ordering</p><h2>From first message to bill of lading.</h2></div><p class="lede">A first container usually ships 3–5 weeks after the signed contract, depending on season and grade.</p></div>
      <ol class="steps">
        <li><h3>Request a quote</h3><p>Species, cut, grade, packing and port. Price offer within 24 hours.</p></li>
        <li><h3>Samples</h3><p>Frozen samples by courier on dry ice, or a video inspection of current stock.</p></li>
        <li><h3>Contract &amp; payment</h3><p>Proforma invoice. Irrevocable L/C at sight or T/T with deposit.</p></li>
        <li><h3>Production &amp; inspection</h3><p>Packed to your specification. Third-party inspection with photos per lot.</p></li>
        <li><h3>Shipment</h3><p>Reefer booked and sealed at the plant. Documents by courier or eBL.</p></li>
        <li><h3>Arrival &amp; claims</h3><p>We support border inspection. Claims answered within 48 hours.</p></li>
      </ol>
    </div>
  </section>

{faq_html(FAQ_MARKETS, "Shipping questions")}
''' + FOOT
    write("markets.html", mk)

    # ---------- GUIDE (pillar content for search & AI answers)
    hstable = "\n".join(f'<tr><td class="mono">{h}</td><td>{E(t)}</td><td>{E(k)}</td><td class="num">{n}</td></tr>' for h, t, n, k in HSCATS)
    article = {"@type": "Article", "headline": "Bangladesh Seafood & Food Export Guide", "datePublished": "2026-11-05", "dateModified": TODAY,
               "author": {"@id": SITE + "/#org"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + "/guide.html",
               "about": ["Bangladesh seafood exports", "HS codes for fish", "Fish export certification in Bangladesh"]}
    guide = head("Bangladesh Seafood & Food Export Guide: Exporters, HS Codes, Approvals",
                 f"How Bangladesh exports seafood and food: {NET['mapped']} registered exporters by district, HS codes 0301–0307, DoF FIQC licensing, EU, SFDA and GACC approvals, hilsa rules, trade associations and shipping.",
                 "guide.html", [crumbs_ld("Export guide", "guide.html"), article, faq_ld(FAQ_GUIDE)], "school-underwater.jpg") + header("guide") + "\n" + page_hero(
        "Export guide", "Bangladesh seafood &amp; food export guide",
        "A buyer's reference to who exports what from Bangladesh, how it is certified, and how it reaches your port.", "school-underwater",
        extra=f'\n      <p class="updated">Updated <time datetime="{TODAY}">{TODAY}</time> · {BRAND} research</p>') + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <article class="guide">
        <p class="answer"><b>Summary:</b> Bangladesh exports frozen shrimp and prawn, frozen and chilled fish, live mud crab and eel, and dried fish, mainly to the EU, UK, Middle East, China and the USA. Exporters must hold a Department of Fisheries (FIQC) licence, and each plant must be approved by the importing market. {NET['mapped']} registered seafood exporters operate across {NET['districts']} districts, led by Dhaka, Khulna and Chattogram.</p>
        <nav class="toc" aria-label="Contents"><b>Contents</b><ol>
          <li><a href="#what">What Bangladesh exports</a></li><li><a href="#who">Who the exporters are</a></li><li><a href="#hs">HS codes</a></li>
          <li><a href="#cert">Licences and market approvals</a></li><li><a href="#hilsa">Hilsa export rules</a></li><li><a href="#assoc">Trade associations</a></li>
          <li><a href="#ship">Shipping and terms</a></li><li><a href="#faq-guide">Frequently asked questions</a></li></ol></nav>

        <h2 id="what">What Bangladesh exports</h2>
        <p>Frozen shrimp is the country's leading seafood export. Black tiger shrimp (<i>Penaeus monodon</i>, locally <i>bagda</i>) and giant freshwater prawn (<i>Macrobrachium rosenbergii</i>, <i>golda</i>) are farmed in the south-west and processed in Khulna, Satkhira and Bagerhat. Whiteleg shrimp (vannamei) farming started recently.</p>
        <p>Wild marine fish from the Bay of Bengal (hilsa, pomfret, ribbonfish, Bombay duck, croaker, threadfin and snapper) is landed at Chattogram, Cox's Bazar and Mongla and mostly frozen whole for the Middle East and East Asia. Live mud crab and mud eel are flown to China, South Korea and South-East Asia. Chilled freshwater fish such as rohu, catla, pangasius and catfish serve South Asian communities abroad.</p>
        <p>Beyond seafood, Bangladesh exports aromatic rice, spices, tea, fresh vegetables, mango and other seasonal fruit, frozen paratha and snacks, and a wide range of packaged foods. See the <a href="products.html">product directory</a> for {N_PRODUCTS} lines with HS headings.</p>

        <h2 id="who">Who the exporters are</h2>
        <p>Our mapping of the Export Promotion Bureau (EPB) directory counts {NET['mapped']} registered seafood and fisheries exporters. They cluster by product: shrimp processors in Khulna, marine fish processors in Chattogram, live and chilled fish traders in Dhaka, and dried fish traders around the Akhaura land port in Brahmanbaria and in Cox's Bazar.</p>
        <div class="tbl"><table class="dtable"><thead><tr><th>District</th><th style="text-align:right">Exporters</th><th style="text-align:right">Share</th></tr></thead><tbody>
          {''.join(f'<tr><td>{E(d)}</td><td class="num">{n}</td><td class="num">{n/NET["mapped"]*100:.1f}%</td></tr>' for d, n in DISTRICTS)}
        </tbody></table></div>
        <p class="src">Source: EPB exporter directory, compiled by {BRAND}, October 2026.</p>

        <h2 id="hs">HS codes for Bangladeshi seafood</h2>
        <div class="tbl"><table class="dtable"><thead><tr><th>HS</th><th>Category</th><th>Typical items</th><th style="text-align:right">Exporters</th></tr></thead><tbody>
          {hstable}
          <tr><td class="mono">0304</td><td>Fish fillets</td><td>Pangasius, tilapia, barramundi fillets</td><td class="num">—</td></tr>
          <tr><td class="mono">0307</td><td>Molluscs</td><td>Squid, cuttlefish, octopus</td><td class="num">—</td></tr>
          <tr><td class="mono">1605</td><td>Prepared crustaceans</td><td>Breaded and cooked shrimp</td><td class="num">—</td></tr>
        </tbody></table></div>
        <p class="src">Exporter counts overlap because many companies ship several categories.</p>

        <h2 id="cert">Licences and market approvals</h2>
        <p>The Department of Fisheries' Fish Inspection and Quality Control wing (DoF FIQC) licenses fish processing plants for export, inspects consignments and issues the health certificate that travels with each shipment. Plants carry an approval number such as KLN-57 (Khulna) or CTG-66 (Chattogram).</p>
        <ul>
          <li><b>European Union:</b> the plant must be on the EU list of approved establishments for Bangladesh, and residue monitoring must meet EU rules.</li>
          <li><b>Saudi Arabia:</b> the plant must appear on the Saudi Food &amp; Drug Authority (SFDA) list of approved Bangladeshi establishments.</li>
          <li><b>China:</b> exporters of live crab, eel and frozen seafood need GACC registration.</li>
          <li><b>United States:</b> FDA facility registration and seafood HACCP compliance.</li>
        </ul>
        <p>Approvals change. Ask for the current listing at the time of contract, not a past one.</p>

        <h2 id="hilsa">Hilsa export rules</h2>
        <p>Hilsa (<i>Tenualosa ilisha</i>, <i>ilish</i>) is Bangladesh's national fish. Exports are restricted: the government allows limited volumes under permit, often around festival seasons, and announces quotas each time. Fishing bans during breeding periods also limit supply.</p>

        <h2 id="assoc">Trade associations</h2>
        <ul>
          <li><b>BFFEA</b>: Bangladesh Frozen Foods Exporters Association, for shrimp and frozen fish processors. Its member list is the most complete supplier list.</li>
          <li><b>BLCFEA</b>: Bangladesh Live &amp; Chilled Food Exporters Association, for live crab and eel exporters.</li>
          <li><b>BMFA</b>: Bangladesh Marine Fisheries Association, for deep-sea fishing companies.</li>
          <li><b>EPB</b>: Export Promotion Bureau, which keeps the national exporter directory and export statistics.</li>
        </ul>

        <h2 id="ship">Shipping and terms</h2>
        <p>Frozen seafood moves in 20- or 40-foot reefers from Chattogram or Mongla, usually transshipped in Colombo or Singapore. Europe takes 28–35 days and the Gulf 14–20 days. Live and chilled products fly from Dhaka. Common terms are FOB Chattogram or CFR to the destination port, paid by L/C at sight or T/T with a deposit. See <a href="markets.html">markets &amp; logistics</a>.</p>
      </article>
    </div>
  </section>

{faq_html(FAQ_GUIDE, "Frequently asked questions").replace('id="faq"', 'id="faq-guide"')}
''' + FOOT
    write("guide.html", guide)

    # ---------- CONTACT
    ct = head(f"Request a Quote: Bangladesh Seafood & Food | {SHORT}",
              "Request a CFR, CIF or FOB price offer for Bangladeshi shrimp, fish, crab and food products. Reply within 24 hours by email and WhatsApp.",
              "contact.html", [crumbs_ld("Contact", "contact.html")], "iced-snapper.jpg") + header("contact") + "\n" + page_hero(
        "Contact", "Tell us what you need. We reply within 24 hours.",
        "Fill in the quote request, or reach us directly on WhatsApp, Messenger or email.", "iced-snapper") + f'''

  <section id="rfq" class="band" style="padding-top:2rem">
    {BUB}
    <div class="wrap rfq">
      <div>
        <p class="eyebrow">Request for quotation</p>
        <h2 style="margin-top:.8rem">Your quote request</h2>
        <p class="lede" style="margin-top:1.2rem">Your request reaches our team immediately. You receive a confirmation by email, and on WhatsApp if you add your number.</p>
        <ul class="contact-list">
          <li><span>WhatsApp</span><a href="#" data-wa="Hello {BRAND}" data-track="whatsapp_click" data-show="whatsappDisplay"></a></li>
          <li><span>Messenger</span><a href="#" data-messenger data-track="messenger_click">m.me/<span data-show-text="messengerPage"></span></a></li>
          <li><span>Email</span><a href="#" data-mail data-track="email_click"></a></li>
          <li><span>Office</span><a>Dhaka, Bangladesh</a></li>
          <li><span>Hours</span><a>Sunday–Thursday, 09:00–18:00 (UTC+6). WhatsApp answered 7 days.</a></li>
        </ul>
      </div>
      <form class="rfq-form" id="rfqForm" novalidate>
        <div class="f full"><label>Products</label><div class="basket" id="basket" aria-live="polite"></div><span class="hint"><a href="products.html">Add products from the directory</a>, or describe them below.</span></div>
        <div class="f"><label for="company">Company</label><input id="company" name="company" required autocomplete="organization"></div>
        <div class="f"><label for="name">Your name</label><input id="name" name="name" required autocomplete="name"></div>
        <div class="f"><label for="email">Work email</label><input id="email" name="email" type="email" required autocomplete="email"></div>
        <div class="f"><label for="whatsapp">WhatsApp number</label><input id="whatsapp" name="whatsapp" type="tel" placeholder="+31 6 1234 5678" autocomplete="tel"><span class="hint">Optional. Include the country code.</span></div>
        <div class="f"><label for="country">Country</label><input id="country" name="country" required autocomplete="country-name"></div>
        <div class="f"><label for="port">Destination port</label><input id="port" name="port" placeholder="e.g. Rotterdam"></div>
        <div class="f"><label for="incoterm">Incoterm</label><select id="incoterm" name="incoterm"><option>CFR</option><option>CIF</option><option>FOB Chattogram</option><option>CPT / CIP (air)</option><option>Not sure yet</option></select></div>
        <div class="f"><label for="volume">Volume</label><select id="volume" name="volume"><option value="sample">Samples only</option><option value="lcl">Less than 1 container</option><option value="1" selected>1 × 40′ reefer</option><option value="2-4">2–4 containers / month</option><option value="5+">5+ containers / month</option></select></div>
        <div class="f"><label for="buyerType">You are a</label><select id="buyerType" name="buyerType"><option>Importer / distributor</option><option>Retail chain</option><option>Food service</option><option>Processor / re-packer</option><option>Trading agent</option></select></div>
        <div class="f"><label for="shipMonth">Target shipment</label><input id="shipMonth" name="shipMonth" type="month"></div>
        <div class="f full"><label for="details">Specification details</label><textarea id="details" name="details" placeholder="Cut, count grade, glaze %, packing, label, certificates required…"></textarea></div>
        <label class="consent full" for="consent"><input type="checkbox" id="consent" name="consent" required> I agree that {BRAND} may store these details to prepare a quote and contact me about it. We do not share your data with third parties.</label>
        <input type="text" name="website" id="website" tabindex="-1" autocomplete="off" class="sr" aria-hidden="true">
        <div class="full" style="display:flex;gap:.75rem;flex-wrap:wrap;align-items:center"><button class="btn btn-primary" type="submit" id="rfqSubmit">Send quote request</button><span class="hint" style="margin:0">Takes under a minute.</span></div>
        <div class="status" id="rfqStatus" role="status" hidden></div>
      </form>
    </div>
  </section>

{faq_html(FAQ_HOME)}
''' + FOOT
    write("contact.html", ct)

    # ---------- catalog.js, sitemap, robots, llms.txt
    cat_js = {p[0]: {"n": p[2], "hs": p[5], "c": CAT[p[1]][1]} for p in P}
    write("assets/js/catalog.js", "/* Generated by tools/build_site.py from tools/catalog.py */\nwindow.CATALOG=" + json.dumps(cat_js, ensure_ascii=False) + ";\n")
    pages = ["index.html", "products.html", "sourcing.html", "quality.html", "markets.html", "guide.html", "contact.html"]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(
        f'  <url><loc>{SITE}/{"" if p == "index.html" else p}</loc><lastmod>{TODAY}</lastmod></url>\n' for p in pages) + "</urlset>\n")
    write("robots.txt", f"""User-agent: *
Allow: /

# AI assistants and answer engines are welcome to read and cite this site
User-agent: GPTBot
Allow: /
User-agent: OAI-SearchBot
Allow: /
User-agent: ChatGPT-User
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: Claude-SearchBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /
User-agent: Applebot-Extended
Allow: /

Sitemap: {SITE}/sitemap.xml
""")
    groups = "\n".join(f"- {t}: " + ", ".join(p[2] for p in P if p[1] == c) for c, t, g, i in CATEGORIES)
    write("llms.txt", f"""# {BRAND}

> {BRAND} ({SHORT}) is a Bangladesh-based buyer's broker for seafood and food. Its mission is to be the best broker in the world for food importers. We match importers worldwide with licensed Bangladeshi exporters, verify plant approvals (DoF FIQC, EU, SFDA, GACC, US FDA) and lab results, and manage quotes, inspection, documents and reefer or air shipment.

Key facts
- Network: {NET['mapped']} registered Bangladeshi seafood exporters mapped across {NET['districts']} districts (EPB directory); {NET['shortlisted']} on our shortlist, {NET['tier_a']} rated Priority A.
- Products: {N_PRODUCTS} export lines ({N_FISH} seafood, {N_FOOD} food).
- Terms: FOB Chattogram, CFR or CIF; air freight from Dhaka for live and chilled products. Quotes within 24 hours.
- Minimum order: usually one 20-foot reefer per product.

Pages
- [Product directory]({SITE}/products.html): every product with scientific name, Bangla name, HS heading, forms and main markets
- [Bangladesh export guide]({SITE}/guide.html): exporters by district, HS codes, licences and approvals, hilsa rules, associations, shipping
- [Supplier network]({SITE}/sourcing.html): how suppliers are rated; exporters can apply to join
- [Quality]({SITE}/quality.html): lab testing per lot and the cold chain
- [Markets & logistics]({SITE}/markets.html): transit times, load planner, ordering steps
- [Request a quote]({SITE}/contact.html)

Product directory
{groups}
""")


if __name__ == "__main__":
    build()
