#!/usr/bin/env python3
"""Builds the GoodBuy Foods Global static site.

  python3 tools/build_site.py

Edit products in tools/catalog.py and site-wide settings below. Outputs plain HTML
(crawlable by search engines and AI assistants), sitemap.xml, robots.txt, llms.txt
and assets/js/catalog.js.
"""
import html, json, os, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from catalog import CATEGORIES, P

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://www.goodbuyfoodsglobal.com"   # ← your live domain
BRAND = "GoodBuy Foods Global"
SHORT = "GFG"
TODAY = datetime.date.today().isoformat()
V = "assets/video/"
E = html.escape
CAT = {c[0]: c for c in CATEGORIES}
N_PRODUCTS = len(P)
N_FISH = sum(1 for p in P if CAT[p[1]][2] == "fish")
N_FOOD = N_PRODUCTS - N_FISH

# Network figures from GFG research (EPB directory, SFDA list, BFFEA, Oct 2026)
NET = dict(mapped=148, districts=17, shortlisted=54, tier_a=19, tier_b=16, tier_c=19,
           food_short=21, bapa=479, bfvapea=500)
NET["all_short"] = NET["shortlisted"] + NET["food_short"]
# Supplier channels by sector: sector, supplier types, channel / source, status
SUPPLY = [
 ("Seafood & fish", "Processing plants; chilled, live and dried fish exporters", "EPB directory, BFFEA, BLCFEA, SFDA approved list", f"{NET['mapped']} mapped · {NET['shortlisted']} shortlisted"),
 ("Processed & packaged food", "Biscuit, snack, juice, noodle, condiment and oil manufacturers", f"BAPA (about {NET['bapa']} members), BAPA FoodPro Expo", "15 shortlisted"),
 ("Spices & aromatic rice", "Spice processors, rice millers and packers", "BAPA, brand owners, Ministry of Food export permits", "Covered within the processed shortlist"),
 ("Tea", "Tea estates, blenders and packers, including organic", "Bangladesh Tea Board, Chattogram tea auction", "4 shortlisted"),
 ("Fresh vegetables & fruit", "Produce exporters and packhouses; mango orchards", f"BFVAPEA (about {NET['bfvapea']} exporting members), DAE Plant Protection Wing", "Member directory requested"),
 ("Frozen & ready-to-cook", "Frozen paratha, snack and ready-meal makers; IQF vegetable and jackfruit packers", "BAPA", "2 shortlisted"),
 ("Sugar, jaggery & honey", "Date-palm and cane jaggery makers, honey processors", "Producer groups in Jashore, Sundarbans and the mustard belt", "Mapping in progress"),
]
DISTRICTS = [("Dhaka", 37), ("Khulna", 33), ("Chattogram", 29), ("Brahmanbaria", 14), ("Jashore", 10),
             ("Cox's Bazar", 5), ("Sylhet", 4), ("Bagerhat", 3), ("Sunamganj", 3), ("Other districts", 10)]
HSCATS = [("0303", "Frozen fish", 78, "Sea fish, hilsa, pomfret"),
          ("0302", "Fresh & chilled fish", 58, "Chilled freshwater fish, carp"),
          ("0301", "Live fish, eel & crab", 53, "Live mud crab, live eel (kuchia)"),
          ("0306", "Crustaceans (shrimp, prawn, crab)", 46, "Black tiger, freshwater prawn"),
          ("0305", "Dried & salted fish", 27, "Dried marine fish, salted fish")]

LOGO = '<svg viewBox="0 0 40 40" aria-hidden="true"><circle cx="20" cy="20" r="19" fill="#0A2540"/><path d="M7 23c4-5.5 10.5-7.3 17-3.7l5.5-3.6-1.4 6.4 1.4 6.4-5.5-3.6C17.5 28.5 11 27 7 23z" fill="#F5FBFD"/><circle cx="12.5" cy="22.4" r="1.3" fill="#0A2540"/><path d="M21 15.5c.5-5 4.5-8.3 10-8.5-.2 5.4-3.7 9.3-9 9.3" fill="#4CC28A"/><path d="M22 16c2.2-2.6 4.6-4.6 7.5-6.4" stroke="#0A2540" stroke-width=".9" fill="none"/></svg>'
WA = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .1-1.2c0-.1-.2-.2-.5-.3z"/></svg>'
DIV = lambda a="#E4F5FA", b="#DFF3F8": f'<div class="divider" aria-hidden="true"><svg viewBox="0 0 2880 70" preserveAspectRatio="none"><path fill="{a}" fill-opacity=".55" d="M0 38 C240 8 480 8 720 38 S1200 68 1440 38 S1920 8 2160 38 S2640 68 2880 38 V70 H0Z"/><path fill="{b}" d="M0 46 C240 22 480 70 720 46 S1200 22 1440 46 S1920 70 2160 46 S2640 22 2880 46 V70 H0Z"/></svg></div>'
BUB = '<div class="bubbles" aria-hidden="true">' + "".join(
    f'<span style="--x:{x}%;--s:{s}px;--d:{d}s;--dl:{dl}s"></span>' for x, s, d, dl in
    [(4,10,13,0),(12,16,17,3),(21,8,11,6),(33,14,15,1),(45,9,12,8),(57,18,19,2),(66,10,14,5),(74,13,16,9),(83,8,10,4),(92,15,18,7)]) + "</div>"

NAV = [("index.html","home","Home"),("products.html","products","Products"),("food.html","food","Food &amp; crops"),("services.html","services","Services &amp; fees"),("quality.html","quality","Quality &amp; risk"),
       ("sourcing.html","sourcing","Suppliers"),("guide.html","guide","Guide"),("contact.html","contact","Contact")]

ORG = {"@type": "Organization", "@id": SITE + "/#org", "name": BRAND, "alternateName": SHORT, "url": SITE + "/",
       "logo": SITE + "/assets/img/logo.png",
       "slogan": "One-stop food sourcing services", "description": f"{BRAND} is a one-stop food sourcing company and buyer's broker that sources frozen, chilled, live and dried seafood and Bangladeshi food products from licensed exporters for importers worldwide, with five-gate QC on every lot. Mission: to be the world's best and most trusted food sourcing company.",
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
    <a class="logo" href="index.html" aria-label="{BRAND} home">{LOGO}<span><span data-brand>{BRAND}</span><small>Best food to buy in the world</small></span></a>
    <nav class="nav" id="nav" aria-label="Main">
      {links}
    </nav>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="nav">Menu</button>
    <a class="btn btn-primary cta-top" href="contact.html#rfq" data-track="cta_header">Request a quote <span class="flag" data-basket-count hidden style="background:#fff;color:var(--coral-ink)">0</span></a>
  </div>
</header>
<main id="main">'''


def page_hero(crumb, title, lede, video, level="0.74", extra="", image=None):
    if image:
        video = None
    vid = (f'<img class="bg" src="{IMG}{image}-lg.jpg" alt="" aria-hidden="true" fetchpriority="high">' if image else None) or (f'<video class="bg" data-auto autoplay muted loop playsinline preload="auto" poster="{V}{video}.jpg" aria-hidden="true"><source src="{V}{video}.mp4" type="video/mp4"></video>'
           if video else '<div class="bg-field" aria-hidden="true"></div>')
    return f'''  <section class="vid page-hero{'' if (video or image) else ' novideo'}">
    {vid}
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
      <a class="logo" href="index.html" style="color:var(--fg)">{LOGO}<span><span data-brand>{BRAND}</span><small>Best food to buy in the world</small></span></a>
      <p style="margin-top:1rem;max-width:36ch">We source seafood and food from licensed Bangladeshi exporters and manage quality, documents and cold chain for importers worldwide.</p>
    </div>
    <div><h4>Explore</h4><ul><li><a href="products.html">Product directory</a></li><li><a href="food.html">Food &amp; crops</a></li><li><a href="sourcing.html">Supplier network</a></li><li><a href="services.html">Services &amp; fees</a></li><li><a href="quality.html">Quality &amp; compliance</a></li><li><a href="markets.html">Markets &amp; logistics</a></li><li><a href="guide.html">Bangladesh export guide</a></li></ul></div>
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
          <div class="item-main">{photo(PROD_IMG[pid], "sq", "thumb") if pid in PROD_IMG else f'<span class="thumb ph {CAT[cat][2]}" aria-hidden="true"></span>'}<div><h3>{E(name)}</h3><p class="sci">{sub}</p>{f'<p class="note">{E(note)}</p>' if note else ''}</div></div>
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
 ("Pesticide residues above limits", "Fresh produce exceeds the importing market's maximum residue limits (MRLs) and is destroyed or recalled.", "Farm spray records checked; pre-harvest interval enforced; multi-residue lab test per lot for fresh produce and spices.", "Pesticide residue report against your market's MRLs"),
 ("Plant pests and phytosanitary failure", "Fruit fly or other quarantine pests found at the border; the whole consignment is refused.", "Sourcing from monitored orchards and farms; sorting, cleaning and treatment (hot water for mango); phytosanitary inspection by the DAE Plant Protection Wing.", "Phytosanitary certificate and treatment record"),
 ("Aflatoxin and contaminants", "Aflatoxin, Sudan dyes or heavy metals in spices, rice or dried products.", "Lab tests for aflatoxin, illegal dyes and heavy metals; moisture control in storage.", "Lab certificate for the exact lot"),
 ("Allergen and labelling errors", "Packaged food recalled for undeclared allergens or non-compliant labels.", "Labels checked against your market's rules (ingredients, allergens, nutrition, language) before printing.", "Approved label proof before production"),
 ("Claims after arrival", "A quality issue found at destination.", "Claim procedure written into the contract; we respond within 48 hours and pursue the exporter on your behalf.", "Written claim outcome: credit note or replacement"),
]

# Price reference points: only figures with a public source. product, spec, price, basis, period, source label, url
PRICES = [
 ("Hilsa", "Whole, about 900 g (\"LC size\")", "US$12.50 / kg", "Government minimum export price (FOB)", "Sept–Oct 2025 export window", "Prothom Alo", "https://en.prothomalo.com/business/local/cigk04qwto"),
 ("Aromatic rice", "Kalijira, Chinigura and similar", "US$1.60 / kg (US$1,600 / t)", "Government minimum export price (FOB)", "2025–26 export windows", "The Daily Star", "https://online91.thedailystar.net/business/economy/news/aromatic-rice-export-deadline-extended-april-30-4116076"),
 ("Frozen shrimp", "All types and grades, Bangladesh origin", "US$8.25 – 15.20 / kg", "Reported export price range", "2024", "Tridge", "https://dir.tridge.com/prices/frozen-common-shrimp-and-prawn/BD"),
 ("Table potato", "50 kg bags, bulk", "About US$300 / t", "Reported export price", "2025 season", "FreshPlaza", "https://www.freshplaza.com/asia/article/9790713/bangladesh-potato-exports-hit-a-three-year-peak"),
]
# How grade and compliance move price: driver, higher price, lower price
DRIVERS = [
 ("Size and count grade", "Larger grades (shrimp U/10–16/20, hilsa 1 kg+, mango A-grade)", "Small grades (shrimp 51/60 and smaller, mixed sizes)"),
 ("Product form", "Peeled, deveined, cooked or value-added; fillets", "Whole or head-on (HOSO), block frozen"),
 ("Glaze and net weight", "Low glaze, quoted on true net weight", "High glaze that inflates gross weight"),
 ("Plant listing", "Plants listed for the EU, US or Japan", "Plants approved only for regional markets"),
 ("Certification", "ASC, BAP, Organic, GLOBALG.A.P., BRCGS, FSSC 22000", "Basic HACCP only"),
 ("Season", "Off-season and festival demand (e.g. hilsa before Durga Puja)", "Peak harvest (shrimp May–Sept, mango June–July, potato Feb–April)"),
 ("Volume and commitment", "Spot orders, mixed small lots", "Full containers and monthly supply programmes"),
 ("Packing", "Retail and private-label packs", "Bulk master cartons"),
]

# Service packages: EDIT FEES HERE. id, name, tagline, fee, fee basis, includes, responsibility, featured
SERVICES = [
 ("verify", "Verify", "Supplier verification", "US$150", "per supplier, one-time",
  ["Export Registration Certificate (ERC) and licence check", "DoF FIQC plant approval (fish) or DAE phytosanitary registration (produce)",
   "Plant listing checked for your market: EU, SFDA, GACC, US FDA", "Certificates validated with the issuing body (HACCP, BRCGS, FSSC 22000, Halal…)",
   "Factory or packhouse visit with photo and video report", "Risk rating (A / B / C) and a written verification report in 5 working days"],
  "We certify what we checked; you decide whether to buy.", False),
 ("assure", "Assure", "Per-shipment QC & compliance", "US$290", "per container · lab tests at cost, no markup",
  ["All five QC gates: raw material, processing, lab release, pre-shipment inspection, loading", "Lab testing for the lot at an accredited lab (residues, heavy metals, microbiology or pesticides), billed at cost with no markup",
   "AQL inspection against your specification, with photos and video", "Document check: health or phytosanitary certificate, origin, invoice, packing list, B/L drafts",
   "Supervised loading, reefer temperature log and seal record", "You approve before the balance payment or document release"],
  "Quality checking is our responsibility. A lot that fails any gate does not ship.", False),
 ("complete", "Complete", "End-to-end buyer's agent", "1.5% of FOB value", "per shipment · minimum US$450 per container",
  ["Everything in Verify and Assure", "Competing offers from qualified plants and price negotiation for you", "Contract, specification and label management",
   "Freight booking and shipment tracking to your port", "Claims handled with the exporter on your behalf, answered within 48 hours",
   "Quality guarantee: if a lot we released does not match the agreed specification, we refund our full service fee for that shipment and pursue the exporter for you"],
  "We carry the full quality and compliance responsibility, from supplier to port.", True),
 ("programme", "Programme", "Recurring supply programme", "From US$750", "per month · includes up to 3 containers of Assure",
  ["A dedicated GFG QC officer for your account", "Priority production slots and a backup plant for each product", "Seasonal buying plan and price-lock windows",
   "Monthly quality and supplier performance report", "US$240 per container from the fourth container"],
  "Your own QC team in Bangladesh, without the overhead.", False),
]
ADDONS = [
 ("Extended lab panel (aflatoxin, Sudan dyes, DNA species ID, extra residues)", "At lab cost, no markup"),
 ("Sample sourcing and courier on dry ice", "From US$120 per shipment, plus courier at cost"),
 ("Label and artwork compliance review for your market", "US$75 per label"),
 ("Social or ethical audit (amfori BSCI-style)", "Quoted per site"),
 ("Container-loading video call with you, live", "Included in Assure and Complete"),
]

# ------------------------------------------------------------------ FAQs
FAQ_HOME = [
 ("What does GoodBuy Foods Global do?", f"{BRAND} is a Bangladesh-based sourcing and export partner that buys on the importer's behalf. We negotiate with licensed Bangladeshi plants, enforce five QC gates on every lot, check compliance for your market and manage documents and shipment, so each container lands at a profitable price."),
 ("Who does GFG represent?", "The buyer. We work to your specification, carry out QC on your behalf and release a shipment only when it meets the order you placed."),
 ("What does GFG charge?", "Supplier verification is US$150 per supplier; per-shipment QC and compliance (Assure) is US$290 per container, with lab tests at cost; the end-to-end Complete service is 1.5% of FOB value with a minimum of US$450 per container. Buying agents commonly charge 5–10%."),
 ("How does GFG lower my landed cost?", "By buying directly from processing plants, getting competing quotes from several qualified plants, loading containers to their payload limit, specifying glaze so you pay for fish rather than ice, and using preferential duty access for Bangladeshi origin where your market grants it."),
 ("How do you reduce supply risk?", "We only use plants whose licence and market listing we have checked, qualify a backup plant for each product, use L/C or document-based payment, and require independent pre-shipment inspection before the container is sealed."),
 ("Which seafood does Bangladesh export?", "Mainly frozen black tiger shrimp and giant freshwater prawn (HS 0306), frozen marine fish such as hilsa, pomfret and ribbonfish (HS 0303), chilled freshwater fish (HS 0302), live mud crab and eel (HS 0301) and dried fish (HS 0305)."),
 ("How much does Bangladeshi seafood and food cost?", "It depends on grade, form, packing and the approvals your market needs. Public reference points include the government minimum export prices of US$12.50/kg for hilsa and US$1.60/kg FOB for aromatic rice; our price guide lists more. We return a firm, competing-plant offer within 24 hours of your specification."),
 ("What is the minimum order?", "Usually one 20-foot reefer for a single product, or one 40-foot reefer split across up to four products. Samples and trial lots can be arranged."),
 ("Which payment terms are used?", "Irrevocable L/C at sight or T/T with a deposit. Terms are agreed with the exporter in the proforma invoice."),
 ("How fast do you quote?", "Within 24 hours of receiving species, cut, grade, packing, quantity and destination port."),
]
FAQ_GUIDE = [
 ("How many seafood exporters are registered in Bangladesh?", f"GFG's mapping of the Export Promotion Bureau directory lists {NET['mapped']} registered seafood and fisheries exporters across {NET['districts']} districts. Dhaka (37), Khulna (33) and Chattogram (29) together account for about two-thirds."),
 ("Who certifies Bangladeshi fish for export?", "The Department of Fisheries' Fish Inspection and Quality Control (FIQC) wing licenses fish export plants and issues health certificates. Plants must also be on the importing country's approved list, for example the EU list of approved establishments, the SFDA list for Saudi Arabia or GACC registration for China."),
 ("What are the HS codes for Bangladeshi seafood?", "0301 live fish (including eel), 0302 fresh or chilled fish, 0303 frozen fish, 0304 fillets, 0305 dried or salted fish, 0306 crustaceans (shrimp, prawn, crab) and 0307 molluscs (squid, cuttlefish)."),
 ("Can hilsa be exported from Bangladesh?", "Only with a government permit, within quotas and seasons that the government announces. Volumes and timing change each year."),
 ("What food does Bangladesh export besides fish?", "Aromatic rice, tea, spices, potatoes, fresh vegetables (gourds, beans, leafy greens), mango, jackfruit, pineapple and lychee, frozen paratha and snacks, and processed foods such as biscuits, juices, noodles, pickles and sauces."),
 ("What certificate is needed to export fruit and vegetables from Bangladesh?", "A phytosanitary certificate from the Plant Protection Wing of the Department of Agricultural Extension (DAE), plus any treatment or orchard-registration requirements set by the importing country."),
 ("Which trade associations represent Bangladeshi seafood exporters?", "BFFEA (Bangladesh Frozen Foods Exporters Association) for shrimp and frozen fish processors, BLCFEA (Bangladesh Live & Chilled Food Exporters Association) for live crab and eel, and BMFA (Bangladesh Marine Fisheries Association) for deep-sea fishing companies."),
]
FAQ_SUP = [
 ("Who can join the GFG supplier network?", "Bangladeshi exporters with a valid export licence and, for fish, a DoF FIQC-approved plant. Approvals for target markets (EU, SFDA, GACC, US FDA) and certifications such as HACCP or BRCGS raise your priority."),
 ("Do you share buyer details?", "Buyer details are shared after a signed NCNDA (non-circumvention, non-disclosure agreement) and commission agreement."),
 ("Is there a fee to join?", "No. GFG earns an agreed commission on completed shipments."),
]
FAQ_MARKETS = [
 ("How long does a reefer take from Chattogram to Europe?", "Typically 28–35 days to Rotterdam, Antwerp or Hamburg via a transshipment hub such as Colombo or Singapore."),
 ("Which Incoterms do you quote?", "FOB Chattogram, CFR or CIF to your port. Air freight for live crab, eel, chilled fish and fresh produce is quoted CPT or CIP to the destination airport."),
 ("How many cartons fit in a 40-foot reefer?", "About 1,900–2,100 master cartons of 10 kg frozen shrimp, or roughly 19–21 tonnes net, depending on carton size."),
]


SECTORS = [  # title, category ids, blurb, link anchor
 ("Seafood & fish", ["shrimp","shell","marine","fresh","live","dried"], "Shrimp, prawn, hilsa, pomfret, crab, eel, freshwater and dried fish", "cat-shrimp"),
 ("Rice & grains", ["rice"], "Aromatic rice, puffed and flattened rice, semai", "cat-rice"),
 ("Spices & tea", ["spice"], "Turmeric, chilli, coriander, nigella, Sylhet tea", "cat-spice"),
 ("Fresh vegetables", ["veg"], "Potato, gourds, beans, okra, leafy greens", "cat-veg"),
 ("Fresh fruits", ["fruit"], "Mango, jackfruit, pineapple, lychee, seasonal fruit", "cat-fruit"),
 ("Frozen & ready-to-cook", ["frozen"], "IQF vegetables, jackfruit, paratha, snacks, meals", "cat-frozen"),
 ("Processed & packaged", ["processed"], "Biscuits, noodles, juices, pulp, pickles, oils", "cat-processed"),
 ("Sugar & sweeteners", ["sweet"], "Date-palm and cane jaggery, molasses, honey", "cat-sweet"),
]
REGIONS = [
 ("Shrimp & prawn", "Khulna, Satkhira, Bagerhat, Cox's Bazar"),
 ("Marine fish", "Chattogram, Cox's Bazar, Barguna, Patuakhali"),
 ("Mango", "Rajshahi, Chapainawabganj, Naogaon, Satkhira"),
 ("Lychee", "Dinajpur, Rajshahi, Pabna (Ishwardi)"),
 ("Jackfruit & pineapple", "Gazipur, Tangail (Madhupur), Moulvibazar"),
 ("Potato", "Munshiganj, Bogura, Rangpur, Joypurhat"),
 ("Vegetables", "Jashore, Bogura, Narsingdi, Cumilla"),
 ("Aromatic rice", "Dinajpur, Naogaon, Sherpur, Netrokona"),
 ("Tea", "Moulvibazar, Habiganj, Sylhet, Chattogram, Panchagarh"),
 ("Turmeric & chilli", "Bogura, Chattogram Hill Tracts, river char lands"),
 ("Date-palm jaggery", "Jashore, Jhenaidah"),
 ("Honey", "Sundarbans; mustard fields of Sirajganj and Tangail"),
 ("Processed food", "Dhaka, Gazipur, Narayanganj, Chattogram, Habiganj"),
]
FOOD_BODIES = [
 ("BFVAPEA", "Bangladesh Fruits, Vegetables & Allied Products Exporters' Association, for fresh produce exporters"),
 ("BAPA", "Bangladesh Agro-Processors' Association, for processed food exporters"),
 ("Bangladesh Tea Board", "Regulates tea; the Chattogram auction sets prices"),
 ("DAE Plant Protection Wing", "Issues phytosanitary certificates for plants and produce"),
 ("BFSA and BSTI", "Food safety authority and standards institution"),
 ("EPB and CCI&amp;E", "Export statistics and Export Registration Certificates (ERC)"),
]
# product, active months, peak months (1–12)
CALENDAR = [
 ("Black tiger shrimp", range(3, 12), [5, 6, 7, 8, 9]),
 ("Hilsa", range(6, 12), [8, 9, 10]),
 ("Aromatic rice", range(1, 13), [11, 12, 1]),
 ("Potato", range(1, 13), [2, 3, 4]),
 ("Winter vegetables", [11, 12, 1, 2, 3], [12, 1, 2]),
 ("Summer gourds", range(4, 11), [5, 6, 7, 8]),
 ("Mango", range(5, 9), [6, 7]),
 ("Lychee", [5, 6], [5, 6]),
 ("Jackfruit", range(5, 9), [6, 7]),
 ("Pineapple", range(5, 10), [6, 7, 8]),
 ("Tea", range(4, 13), [6, 7, 8, 9, 10]),
 ("Turmeric", range(1, 13), [1, 2, 3]),
 ("Date-palm jaggery", [12, 1, 2], [1]),
]
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()


def sectors_html():
    out = []
    for title, cats, blurb, anchor in SECTORS:
        n = sum(1 for p in P if p[1] in cats)
        im = SECTOR_IMG.get(title)
        pic = photo(im, "md") if im else '<span class="ph" aria-hidden="true"></span>'
        out.append(f'        <a class="sector" href="products.html#{anchor}" data-sector="{cats[0]}"><span class="pic">{pic}</span><span class="txt"><b>{E(title)}</b><span>{E(blurb)}</span><em>{n} products →</em></span></a>')
    return "\n".join(out)


def regions_rows():
    return "".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in REGIONS)


def calendar_html():
    head_ = "".join(f"<th>{m}</th>" for m in MONTHS)
    rows = []
    for name, act, peak in CALENDAR:
        act, peak = set(act), set(peak)
        cells = "".join(f'<td class="{"pk" if m in peak else "on" if m in act else ""}" title="{MONTHS[m-1]}"></td>' for m in range(1, 13))
        rows.append(f"<tr><th scope=\"row\">{E(name)}</th>{cells}</tr>")
    return f'<table class="cal"><thead><tr><th></th>{head_}</tr></thead><tbody>{"".join(rows)}</tbody></table>'


# Photos (assets/img/<name>-lg|md|sq.jpg). Royalty-free, supplied by GFG.
PHOTO = {
 "vegetable-market-chillies-potatoes": "Market stall with carrots, chillies and potatoes in bowls",
 "hilsa-on-ice": "Whole hilsa fish on crushed ice",
 "pointed-gourd-brinjal-beans": "Pointed gourd, brinjal and long beans at a vegetable market",
 "bitter-gourd": "Fresh bitter gourd stacked at a market",
 "green-red-chillies": "Green and red chillies in a woven basket",
 "rice-grains-falling": "Premium polao (aromatic) rice grains falling onto a pile",
 "rohu-carp-catch": "Fresh rohu and carp in a basket after landing",
 "rice-varieties": "Bowls of black, red and white rice varieties",
 "mud-crab-live": "Live mud crabs in a crate",
 "table-potatoes": "Washed table potatoes",
 "aromatic-rice-spoon": "Aromatic rice grains on a wooden spoon",
 "cauliflower-broccoli": "Fresh cauliflower and broccoli",
 "blue-swimming-crab": "Blue swimming crabs tied for live export",
 "buyer-checking-greens": "Buyer checking fresh leafy greens",
 "fresh-mangoes": "Premium Himsagar mangoes ready for export",
 "tomatoes-beans-market": "Tomatoes, beans and chillies in market baskets",
 "grain-sacks-market": "Open sacks of rice and grain at a wholesale market",
 "packed-cartons-warehouse": "Rows of packed produce cartons in a warehouse ready for inspection",
 "white-rice": "Polished white rice grains",
 "potato-harvest": "Freshly harvested potatoes spilling from a sack",
 "red-rice": "Brown rice grains",
 "jackfruit-pods": "Big, sweet premium jackfruit kosh (pods), ready to eat",
 "lentils-rice-graded-samples": "Lentils, grass pea, mung dal, pumpkin seed, pepper and polao rice sorted in sacks to show quality",
 "dry-goods-sacks": "Peanuts, raisins, sago, corn, wheat, rice, peas, lentils and chickpeas in sacks",
 "paddy-harvest-farmers": "Bengal farmers threshing ripe paddy by hand",
}
PROD_IMG = {"hl": "hilsa-on-ice", "rh": "rohu-carp-catch", "ct": "rohu-carp-catch", "mc": "mud-crab-live", "bsc": "blue-swimming-crab",
            "po": "table-potatoes", "ar": "aromatic-rice-spoon", "rr": "red-rice", "gc": "green-red-chillies", "rc": "green-red-chillies",
            "pt": "pointed-gourd-brinjal-beans", "bj": "pointed-gourd-brinjal-beans", "bg": "bitter-gourd", "cb": "cauliflower-broccoli",
            "tm": "tomatoes-beans-market", "yb": "tomatoes-beans-market", "mn": "fresh-mangoes", "jf": "jackfruit-pods", "fj": "jackfruit-pods"}
SECTOR_IMG = {"Seafood & fish": "hilsa-on-ice", "Rice & grains": "paddy-harvest-farmers", "Spices & tea": "green-red-chillies",
              "Fresh vegetables": "pointed-gourd-brinjal-beans", "Fresh fruits": "fresh-mangoes", "Frozen & ready-to-cook": "jackfruit-pods",
              "Processed & packaged": "packed-cartons-warehouse", "Sugar & sweeteners": None}
IMG = "assets/img/"


def photo(name, size="md", cls="", lazy=True, w=None, h=None):
    dims = {"md": (800, 600), "sq": (200, 200)}.get(size, (w or 1600, h or 1067))
    extra = ' loading="lazy" decoding="async"' if lazy else ''
    klass = f' class="{cls}"' if cls else ''
    return f'<img src="{IMG}{name}-{size}.jpg" alt="{E(PHOTO[name])}" width="{dims[0]}" height="{dims[1]}"{extra}{klass}>'


def figure(name, caption, cls="photo"):
    return f'<figure class="{cls}">{photo(name, "lg")}<figcaption>{caption}</figcaption></figure>'


# ------------------------------------------------------------------ PAGES
def write(name, text):
    with open(os.path.join(ROOT, name), "w") as f:
        f.write(text)
    print("wrote", name, len(text))


def build():
    # ---------- HOME
    home = head(f"{BRAND} | One-Stop Food Sourcing from Bangladesh",
                f"Buyer's broker for {N_PRODUCTS} Bangladeshi seafood, food and crop products: shrimp, hilsa, crab, aromatic rice, spices, tea, vegetables, mango and packaged foods. Five-gate QC, quotes in 24 hours.",
                "index.html", [{"@type": "WebSite", "@id": SITE + "/#web", "url": SITE + "/", "name": BRAND, "publisher": {"@id": SITE + "/#org"}}, faq_ld(FAQ_HOME)]) + header("home") + f'''
  <section class="hero vid" style="padding:0">
    <video class="bg" data-auto autoplay muted loop playsinline preload="auto" poster="{V}iced-snapper.jpg" aria-hidden="true"><source src="{V}iced-snapper.mp4" type="video/mp4"></video>
    <canvas class="sea" data-level="0.7" aria-hidden="true"></canvas>
    <div class="wrap">
      <div>
        <p class="eyebrow">Our mission: the world's best and most trusted food sourcing company</p>
        <h1>Better margins on Bangladeshi seafood and food, <em>with the risk taken out</em>.</h1>
        <p class="lede">{BRAND} buys seafood, fresh produce, rice, spices, tea and packaged foods for importers, distributors and retailers from the best-qualified exporters in Bangladesh. We negotiate price at source, enforce strict QC on every lot and keep every shipment compliant with your market, so each container sells at a profit and the next order is easy.</p>
        <div class="actions">
          <a class="btn btn-primary" href="contact.html#rfq" data-track="cta_hero">Request a price offer</a>
          <a class="btn btn-ghost" href="products.html#prices" style="color:var(--fg)">See indicative prices</a>
        </div>
        <div class="trust-row"><span>One-stop food sourcing</span><span>Price negotiated at source</span><span>Five-gate QC on every lot</span><span>Compliant for your market</span></div>
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
        <div><b>{NET['districts']}</b><span>sourcing districts, coast to haor</span><cite>GFG research</cite></div>
        <div><b>{N_PRODUCTS}</b><span>export products in our directory</span><cite>{N_FISH} seafood · {N_FOOD} food</cite></div>
        <div><b>24 h</b><span>quote turnaround</span><cite>Working days</cite></div>
      </div>
    </div>
  </section>

  <section id="sectors" style="padding-top:1rem">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">One-stop food sourcing</p><h2>Every food Bangladesh exports, from one trusted partner.</h2></div>
        <p class="lede">Seafood is where we started. Today we source across {len(SECTORS)} food and crop sectors, with the same buyer-side QC and compliance checks for every product.</p>
      </div>
      <div class="sectors">
{sectors_html()}
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
        <p>Every lot shipped through GFG passes all five QC gates and a full document check before the container is sealed. We control {len(RISKS)} food-import risks, from border residues to payment fraud, and send you the evidence for each.</p></div>
        <div style="display:flex;flex-direction:column;gap:.6rem"><a class="btn btn-navy" href="services.html">See services &amp; fees</a><a class="btn btn-ghost" href="quality.html#risk" style="color:#fff">Import risk controls</a></div>
      </div>
    </div>
  </section>

  <section id="compare">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Why buyers trust GFG</p><h2>Built to be the world's best and most trusted food sourcing company.</h2></div>
        <p class="lede">Trust is earned shipment by shipment, so we make every promise checkable. Most intermediaries pass on an offer and a certificate. We take responsibility for what arrives at your port.</p>
      </div>
      <div class="tbl"><table class="dtable compare">
        <thead><tr><th></th><th>Typical trading intermediary</th><th class="us">GoodBuy Foods Global</th></tr></thead>
        <tbody>
          <tr><td>Who we act for</td><td>Usually the seller</td><td class="us">The buyer: your specification and your approval</td></tr>
          <tr><td>Quality control</td><td>The exporter's own certificate</td><td class="us">Five QC gates on every lot, by our officers or an independent inspector</td></tr>
          <tr><td>Evidence before you pay</td><td>Documents after shipment</td><td class="us">Lab report, inspection photos and video before the balance payment</td></tr>
          <tr><td>Market compliance</td><td>Assumed</td><td class="us">Plant listing for your market checked at contract and again before loading</td></tr>
          <tr><td>Pricing</td><td>One bundled price</td><td class="us">Competing plant quotes, with FOB, freight, insurance and duty shown separately</td></tr>
          <tr><td>Supply security</td><td>One supplier</td><td class="us">A second qualified plant held for each product</td></tr>
          <tr><td>Claims</td><td>Buyer chases the exporter</td><td class="us">Answered within 48 hours; we pursue the exporter on your behalf</td></tr>
          <tr><td>Transparency</td><td>Supplier and costs hidden</td><td class="us">Supplier plant named in your contract; open cost breakdown; references from existing buyers on request</td></tr>
          <tr><td>Risk coverage</td><td>Not documented</td><td class="us">{len(RISKS)} import risks controlled, with evidence for each (<a href="quality.html#risk">see the table</a>)</td></tr>
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
          <li><b>Price guide:</b> <a href="products.html#prices" style="color:var(--sea)">public reference prices and what moves them</a>, by grade and compliance.</li>
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
        {tile('catch-carp','Cultivated carp','Harvest of mixed farmed carp')}
        {tile('catch-pangasius','Pangasius','Farm harvest · to plant in 3 h')}
        {tile('ice-holding','Frozen snapper','Organised and frozen for packing')}
      </div>
      <div class="band-photos">
        {figure("mud-crab-live", "Live mud crab, graded for air freight")}
        {figure("blue-swimming-crab", "Blue swimming crab, tied for live export")}
        {figure("fresh-mangoes", "Premium Himsagar mango, ready for export")}
        {figure("aromatic-rice-spoon", "Aromatic rice, under export permit")}
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
                                      "item": {"@type": "Product", "name": p[2], **({"image": f"{SITE}/{IMG}{PROD_IMG[p[0]]}-lg.jpg"} if p[0] in PROD_IMG else {}), "description": f"{p[2]} ({p[4]}) from Bangladesh. HS {p[5]}. Forms: {p[6]}.",
                                               "category": CAT[p[1]][1], "countryOfOrigin": {"@type": "Country", "name": "Bangladesh"}}}
                                     for i, p in enumerate(P)]}
    prod = head("Bangladesh Export Product Directory: Seafood & Food | " + SHORT,
                f"Indicative prices and a directory of {N_PRODUCTS} products exported from Bangladesh: shrimp, prawn, hilsa, pomfret, mud crab, eel, dried fish, rice, spices, vegetables, fruit and processed food, with HS codes and main markets.",
                "products.html", [crumbs_ld("Product directory", "products.html"), item_list], "catch-pangasius.jpg") + header("products") + "\n" + page_hero(
        "Product directory", "Bangladesh export product directory",
        f"{N_FISH} seafood and {N_FOOD} food products exported from Bangladesh, with scientific names, Bangla names, HS headings, product forms and main buyer markets.", "catch-pangasius") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> Bangladesh's main seafood exports are frozen shrimp and prawn (HS 0306), frozen marine fish (0303), chilled freshwater fish (0302), live crab and eel (0301) and dried fish (0305). Food exports include aromatic rice, spices, fresh vegetables, mango, frozen snacks and packaged foods.</p>
      <div class="price-guide" id="prices">
        <div class="sec-head" style="margin:2.5rem 0 1.5rem">
          <div><p class="eyebrow">Price guide</p><h2>Indicative prices, by grade and compliance.</h2></div>
          <p class="lede">Public reference points help you plan. Your firm offer depends on grade, form, packing and the approvals your market requires. Send your specification and we return a competing-plant price within 24 hours.</p>
        </div>
        <div class="tbl"><table class="dtable prices">
          <thead><tr><th>Product</th><th>Specification</th><th>Reference price</th><th>Basis</th><th>Period</th><th>Source</th></tr></thead>
          <tbody>{''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td class="num">{E(c)}</td><td>{E(d)}</td><td>{E(e)}</td><td><a href="{u}" rel="noopener" target="_blank">{E(src)}</a></td></tr>' for a, b, c, d, e, src, u in PRICES)}</tbody>
        </table></div>
        {figure("lentils-rice-graded-samples", "Graded samples: size, colour and cleanliness decide the price band", "photo wide")}
        <h3 style="margin:2.2rem 0 1rem">What moves the price</h3>
        <div class="tbl"><table class="dtable drivers">
          <thead><tr><th>Factor</th><th>Higher price</th><th>Lower price</th></tr></thead>
          <tbody>{''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td></tr>' for a, b, c in DRIVERS)}</tbody>
        </table></div>
        <div class="broker" style="margin-top:2rem">
          <div><p class="eyebrow">How we get you a better price</p><h3>Several qualified plants quote every order.</h3>
          <p>We match your grade and compliance needs to the plants that meet them, collect competing offers, and show FOB, freight, insurance and duty separately. You see exactly what you pay for.</p></div>
          <a class="btn btn-navy" href="contact.html#rfq">Get today's price</a>
        </div>
        <p class="src">Reference prices are public figures for planning only, not offers. Prices move weekly with harvest, exchange rates and freight. Updated <time datetime="{TODAY}">{TODAY}</time>.</p>
      </div>

      <h2 style="margin-top:3.5rem">Product directory</h2>
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

  <section style="padding-top:0">
    <div class="wrap cols2" style="align-items:center">
      {figure("dry-goods-sacks", "Dry goods for mixed containers")}
      <div>
        <p class="eyebrow">Mixed and dry goods on request</p>
        <h2 style="margin:.6rem 0 1rem">Fill the rest of your container.</h2>
        <p class="lede">Buyers who consolidate mixed containers can add pulses (lentil, mung, grass pea, chickpea), peanuts, sago, corn, wheat and dried fruit. We source them from wholesale markets and mills, with the same grading and QC checks.</p>
        <a class="btn btn-navy" style="margin-top:1.4rem" href="contact.html#rfq">Ask for a mixed-container offer</a>
      </div>
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
               f"How {BRAND} selects Bangladeshi seafood, food and crop exporters: {NET['mapped']} licensed exporters mapped, approval checks (DoF FIQC, EU, SFDA, GACC) and a priority rating. Exporters can apply to join.",
               "sourcing.html", [crumbs_ld("Supplier network", "sourcing.html"), faq_ld(FAQ_SUP)], "catch-carp.jpg") + header("sourcing") + "\n" + page_hero(
        "Supplier network", "A vetted network of Bangladesh's seafood, food and crop exporters.",
        f"Seafood plants, food processors, tea estates and fresh-produce packhouses across Bangladesh. We rate every supplier against the approvals and records your market requires.", "catch-carp",
        extra='\n      <div class="actions" style="display:flex;gap:.75rem;flex-wrap:wrap;margin-top:.6rem"><a class="btn btn-primary" href="#apply">Apply as a supplier</a><a class="btn btn-ghost" href="contact.html#rfq" style="color:var(--fg)">Source through GFG</a></div>') + f'''

  <section style="padding-top:2rem">
    <div class="wrap">
      <div class="statband">
        <div><b>{NET['mapped']}</b><span>seafood exporters mapped</span><cite>EPB directory</cite></div>
        <div><b>~{NET['bapa'] + NET['bfvapea']:,}</b><span>food &amp; produce exporters in our trade-body channels</span><cite>BAPA ~{NET['bapa']} · BFVAPEA ~{NET['bfvapea']}</cite></div>
        <div><b>{NET['all_short']}</b><span>suppliers on our shortlist</span><cite>{NET['shortlisted']} seafood · {NET['food_short']} food</cite></div>
        <div><b>{len(SECTORS)}</b><span>food and crop sectors covered</span><cite>Seafood to sweeteners</cite></div>
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Suppliers by sector</p><h2>Every food and crop sector, one vetting standard.</h2></div>
        <p class="lede">From seafood plants to tea estates and mango packhouses, every supplier goes through the same licence, certification and lab checks before we offer their product to you.</p>
      </div>
      <div class="tbl"><table class="dtable">
        <thead><tr><th>Sector</th><th>Supplier types</th><th>Where we find them</th><th>Network status</th></tr></thead>
        <tbody>{''.join(f'<tr><td><b>{E(a)}</b></td><td>{E(b)}</td><td>{E(c)}</td><td class="status-cell">{E(d)}</td></tr>' for a, b, c, d in SUPPLY)}</tbody>
      </table></div>
      <p class="src">Association member counts as reported in 2025 (BAPA) and by the association (BFVAPEA). Shortlists from GFG research, November 2026.</p>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Where seafood exporters are</p>
        <h2 style="margin:.6rem 0 1.5rem">Registered seafood exporters by district</h2>
        <ul class="bars">{bars}</ul>
        <p class="src">Source: Export Promotion Bureau (EPB) directory of seafood and fisheries exporters, compiled by GFG. n = {NET['mapped']}.</p>
      </div>
      <div>
        <p class="eyebrow">What they export</p>
        <h2 style="margin:.6rem 0 1.5rem">Seafood exporters by HS category</h2>
        <div class="tbl"><table class="dtable"><thead><tr><th>HS</th><th>Category</th><th>Key items</th><th style="text-align:right">Exporters</th></tr></thead><tbody>{hsrows}</tbody></table></div>
        <p class="src">Many exporters ship more than one category, so the column adds up to more than {NET['mapped']}.</p>
      </div>
    </div>
  </section>

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">How we rate suppliers</p><h2>Three priority tiers, checked before every deal.</h2></div>
        <p class="lede">A rating is where we start, not a guarantee. Before any contract we ask for current licences (ERC; DoF FIQC for fish; DAE phytosanitary for produce), factory certificates and proof of listing for the buyer's market.</p>
      </div>
      <div class="tiers">
        <div class="tier"><span class="badge">PRIORITY A</span><h3>Approved &amp; established</h3><p>On an official approval list (for example SFDA), in trade-body leadership, or a major established exporter, with products that match current buyer demand.</p><b class="n">{NET['tier_a'] + 5}</b></div>
        <div class="tier b"><span class="badge">PRIORITY B</span><h3>Credible, to confirm</h3><p>An established exporter with a narrower range, or with details still to confirm.</p><b class="n">{NET['tier_b'] + 12}</b></div>
        <div class="tier c"><span class="badge">PRIORITY C</span><h3>Verify first</h3><p>Found in a database only, or a very narrow range. We verify the licence before any deal.</p><b class="n">{NET['tier_c'] + 4}</b></div>
      </div>
      <h3 style="margin:3rem 0 1rem">What we check</h3>
      <ol class="steps">
        <li><h3>Licence</h3><p>Export Registration Certificate (ERC), plus a DoF FIQC plant approval for fish or DAE phytosanitary registration for fresh produce.</p></li>
        <li><h3>Market listing</h3><p>The plant appears on the importing market's list: EU approved establishments, SFDA, GACC or US FDA.</p></li>
        <li><h3>Certification</h3><p>HACCP is required for processors. BRCGS, ISO 22000, FSSC 22000, GLOBALG.A.P., BAP, ASC, Organic and Halal are recorded where held.</p></li>
        <li><h3>Lab capability</h3><p>Residue (antibiotic or pesticide), heavy metal, aflatoxin and microbiology testing per lot, in-house or at an accredited lab.</p></li>
        <li><h3>Track record</h3><p>Shipment history, claims record and references from existing buyers.</p></li>
        <li><h3>Agreement</h3><p>A signed NCNDA and commission agreement before any buyer details are shared.</p></li>
      </ol>
    </div>
  </section>

  <section id="food-network">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Food &amp; crop exporters</p><h2>Beyond seafood: rice, produce, spices, tea and packaged food.</h2></div>
        <p class="lede">We apply the same rating to food and crop exporters. Our mapping draws on the member lists of the trade bodies below and on the exporters' own certifications.</p>
      </div>
      <div class="cols2">
        <div class="tbl"><table class="dtable"><thead><tr><th>Sector</th><th>Main sourcing regions</th></tr></thead><tbody>{regions_rows()}</tbody></table></div>
        <div>
          {figure("grain-sacks-market", "Sourcing at wholesale markets and mills")}
          <h3 style="margin:1.5rem 0 1rem">Trade bodies and authorities we work through</h3>
          <ul class="ticks">{''.join(f'<li><b>{a}</b>: {b}</li>' for a, b in FOOD_BODIES)}</ul>
        </div>
      </div>
    </div>
  </section>

  {DIV()}
  <section id="apply" class="band">
    {BUB}
    <div class="wrap rfq">
      <div>
        <p class="eyebrow">For Bangladeshi exporters</p>
        <h2 style="margin-top:.8rem">Join the GFG supplier network: seafood, food and crops</h2>
        <p class="lede" style="margin-top:1.2rem">We bring you qualified buyers from Europe, the Gulf, East Asia and North America. Joining is free; we earn an agreed commission on completed shipments.</p>
        <ul class="contact-list">
          <li><span>You need</span><a>An Export Registration Certificate (ERC). For fish, a DoF FIQC-approved plant; for fresh produce, phytosanitary registration with DAE.</a></li>
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
        <div class="f"><label for="s_licence">ERC, DoF approval or licence no.</label><input id="s_licence" name="licence" placeholder="e.g. KLN-57"></div>
        <div class="f"><label for="s_capacity">Monthly export capacity</label>
          <select id="s_capacity" name="capacity"><option value="<20">Under 20 MT</option><option value="20-100">20–100 MT</option><option value="100-500">100–500 MT</option><option value="500+">500 MT +</option></select></div>
        <fieldset class="f full checks-inline"><legend>Product categories</legend>
          {''.join(f'<label><input type="checkbox" name="categories" value="{c}"> {E(t)}</label>' for c, t, g, i in CATEGORIES)}
        </fieldset>
        <fieldset class="f full checks-inline"><legend>Approvals &amp; certifications held</legend>
          {''.join(f'<label><input type="checkbox" name="approvals" value="{a}"> {a}</label>' for a in ['EU approved list','SFDA (Saudi)','GACC (China)','US FDA','HACCP','BRCGS','ISO 22000','FSSC 22000','GLOBALG.A.P.','BAP','ASC','Organic','BSTI','Halal'])}
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
                f"{len(RISKS)} food-import risks controlled for buyers, five QC gates on every lot, lab testing (antibiotic residues, heavy metals, microbiology), DoF health certificates, EU/SFDA/GACC plant approvals and a −18 °C cold chain from pond to port.",
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
            <input id="lot" name="lot" value="GFG-26-1187" aria-describedby="lotHint">
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
        <li><span class="g">Gate 1</span><h3>Raw material</h3><p>Farm, orchard or landing records; residue screening (antibiotics for aquaculture, pesticides for crops); temperature and condition on arrival.</p></li>
        <li><span class="g">Gate 2</span><h3>Processing</h3><p>Grade, size, cut, moisture and freshness checked in process against your specification. Sorting and treatment of fresh produce.</p></li>
        <li><span class="g">Gate 3</span><h3>Lab release</h3><p>Residues, heavy metals, aflatoxin and microbiology tested at an accredited lab for the exact lot.</p></li>
        <li><span class="g">Gate 4</span><h3>Pre-shipment inspection</h3><p>AQL sampling of cartons: net weight, grade, count or glaze, packing and labels, with photos and video sent to you.</p></li>
        <li><span class="g">Gate 5</span><h3>Loading</h3><p>Reefer pre-cooled and set point verified. Loading supervised, core temperatures logged, seal number recorded.</p></li>
      </ol>
      <div class="duo">
        {figure("packed-cartons-warehouse", "Gate 4: cartons counted, weighed and sampled before loading")}
        {figure("hilsa-on-ice", "Gate 1: fish iced at 0–2 °C from landing")}
      </div>
      <p class="src">You receive the inspection report, lab certificate and loading photos before the balance payment or document release.</p>
    </div>
  </section>

  <section id="risk">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Import risk control</p><h2>{len(RISKS)} risks a food importer faces, and how we control each one.</h2></div>
        <p class="lede">Before you pay the balance or the documents are released, you hold evidence for every line in this table.</p>
      </div>
      <div class="tbl"><table class="dtable risk">
        <thead><tr><th>Risk</th><th>What can go wrong</th><th>How GFG controls it</th><th>Evidence you receive</th></tr></thead>
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
        {tile('ice-holding','Frozen snapper','Organised and frozen for packing')}
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
                 f"How Bangladesh exports seafood, food and crops: {NET['mapped']} registered seafood exporters by district, food sourcing regions, HS codes 0301–0307, DoF FIQC licensing, EU, SFDA and GACC approvals, hilsa rules, trade associations and shipping.",
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
          <li><a href="#food">Food and crop exports</a></li><li><a href="#ship">Shipping and terms</a></li><li><a href="#faq-guide">Frequently asked questions</a></li></ol></nav>

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

        <h2 id="food">Food and crop exports</h2>
        <div class="duo">{figure("rice-varieties", "Rice varieties: black, red and white")}{figure("white-rice", "Aromatic varieties are exported under government permit")}</div>
        <p>Bangladesh's food exports range from fresh vegetables and seasonal fruit to aromatic rice, tea, spices and a large processed-food industry (biscuits, snacks, juices, noodles, frozen paratha) that reaches more than 100 countries, often through South Asian retail networks.</p>
        <ul>
          <li><b>Export registration:</b> every exporter needs an Export Registration Certificate (ERC) from the Office of the Chief Controller of Imports and Exports.</li>
          <li><b>Fresh produce:</b> each consignment needs a phytosanitary certificate from the Plant Protection Wing of the Department of Agricultural Extension (DAE). Mango for the EU and other strict markets comes from monitored orchards and may need hot-water treatment.</li>
          <li><b>Processed food:</b> buyers usually ask for HACCP, ISO 22000, FSSC 22000 or BRCGS, plus Halal certification for Muslim markets. BSTI certification applies to many products sold in Bangladesh.</li>
          <li><b>Policy limits:</b> some staples, including aromatic rice, can be subject to export bans or permits when domestic prices rise. Check the current position before you contract.</li>
        </ul>
        <div class="tbl"><table class="dtable"><thead><tr><th>Sector</th><th>Main sourcing regions</th></tr></thead><tbody>{regions_rows()}</tbody></table></div>
        <p>See the <a href="food.html">food &amp; crops page</a> for the harvest calendar.</p>

        <h2 id="ship">Shipping and terms</h2>
        <p>Frozen seafood moves in 20- or 40-foot reefers from Chattogram or Mongla, usually transshipped in Colombo or Singapore. Europe takes 28–35 days and the Gulf 14–20 days. Live and chilled products fly from Dhaka. Common terms are FOB Chattogram or CFR to the destination port, paid by L/C at sight or T/T with a deposit. See <a href="markets.html">markets &amp; logistics</a>.</p>
      </article>
    </div>
  </section>

{faq_html(FAQ_GUIDE, "Frequently asked questions").replace('id="faq"', 'id="faq-guide"')}
''' + FOOT
    write("guide.html", guide)

    # ---------- SERVICES & FEES
    def svc_card(v):
        sid, name, tag, fee, basis, inc, resp, feat = v
        items = "".join(f"<li>{E(i)}</li>" for i in inc)
        return f'''        <article class="pkg{' feat' if feat else ''}" id="pkg-{sid}">
          {'<span class="ribbon">Most chosen · tension-free</span>' if feat else ''}
          <p class="eyebrow">{E(tag)}</p><h3>{E(name)}</h3>
          <p class="fee"><b>{E(fee)}</b><span>{E(basis)}</span></p>
          <ul>{items}</ul>
          <p class="resp">{E(resp)}</p>
          <a class="btn {'btn-primary' if feat else 'btn-navy'}" href="contact.html?package={sid}#rfq" data-track="package_{sid}">Choose {E(name)}</a>
        </article>'''
    FAQ_SVC = [
     ("Who is responsible for quality checking?", "We are. Under Assure and Complete, our QC officers or an independent inspector check every gate against your specification, and a lot that fails does not ship. You approve the evidence before you pay the balance."),
     ("What happens if the goods do not match the specification on arrival?", "Under Complete, we handle the claim with the exporter within 48 hours and refund our full service fee for that shipment. Under Assure, we handle the claim with you and provide all inspection evidence."),
     ("Do I still pay the exporter directly?", "Yes. You pay the exporter by L/C or T/T against documents, so your payment is protected by the banking process. Our service fee is invoiced separately."),
     ("Can I use only the verification service?", "Yes. Verify is a one-time check of a supplier you have found yourself, with a written report in 5 working days."),
    ]
    svc_ld = [{"@type": "Service", "name": f"{BRAND} {v[1]}: {v[2]}", "provider": {"@id": SITE + "/#org"}, "areaServed": "Worldwide",
               "description": "; ".join(v[5]), "offers": {"@type": "Offer", "description": f"{v[3]} {v[4]}"}} for v in SERVICES]
    svc = head(f"One-Stop Food Sourcing Services & Fees: QC and Compliance Verification | {SHORT}",
               "Low fixed fees: US$150 supplier verification, US$290 per-container QC and compliance, 1.5% end-to-end sourcing, end-to-end buyer's agent and supply programmes for importers of Bangladeshi seafood and food. Quality responsibility stays with GFG.",
               "services.html", [crumbs_ld("Services & fees", "services.html"), faq_ld(FAQ_SVC), *svc_ld], "ice-holding.jpg") + header("services") + "\n" + page_hero(
        "Services &amp; fees", "One-stop food sourcing services.",
        "You place the order. We carry the quality responsibility, with low, fixed fees for supplier verification, compliance checks and QC on every shipment, so you can buy from Bangladesh without the worry.", "ice-holding") + f'''

  <section style="padding-top:2rem">
    <div class="wrap">
      <div class="pkgs">
{chr(10).join(svc_card(v) for v in SERVICES)}
      </div>
      <p class="src">Fees exclude the goods, freight and duty, which you pay under your contract with the exporter. Fees are in US dollars and invoiced by {BRAND}. Third-party inspection agencies (SGS, Bureau Veritas, Intertek) can be used on request at their published rates.</p>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="broker">
        <div><p class="eyebrow">Low fees, by design</p><h3>Buying agents commonly charge 5–10 % of order value. Our end-to-end service is 1.5 %.</h3>
        <p>We keep fees low because we work for the buyer and earn by keeping you re-ordering. Lab tests are passed on at cost with no markup, and every fee is fixed and published here before you order.</p></div>
        <a class="btn btn-navy" href="contact.html?package=complete#rfq">Start with Complete</a>
      </div>
    </div>
  </section>

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Our responsibility, in writing</p>
        <h2 style="margin:.7rem 0 1.2rem">What "tension-free" means.</h2>
        <ul class="ticks">
          <li><b>We check, you approve.</b> Every QC gate is our job. You receive the evidence and give the final go-ahead.</li>
          <li><b>Nothing ships on trust.</b> A lot that fails a gate is reworked, replaced or rejected before loading.</li>
          <li><b>Compliance is on us.</b> We confirm the plant listing, certificates and documents your market requires before production.</li>
          <li><b>Claims are handled for you.</b> We deal with the exporter so you don't have to.</li>
          <li><b>Our fee is at stake.</b> Under Complete, if released goods miss the agreed specification, you get our service fee back.</li>
        </ul>
        {figure("buyer-checking-greens", "What arrives is what you specified")}
      </div>
      <div>
        <p class="eyebrow">Add-ons</p>
        <h2 style="margin:.7rem 0 1.2rem">Extra checks when you need them</h2>
        <div class="tbl"><table class="dtable"><thead><tr><th>Service</th><th>Fee</th></tr></thead>
          <tbody>{''.join(f'<tr><td>{E(a)}</td><td><b>{E(b)}</b></td></tr>' for a, b in ADDONS)}</tbody></table></div>
      </div>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">What a package covers</p><h2>Verification steps, step by step.</h2></div>
        <p class="lede">The steps behind the fees, for buyers who want to know exactly what is checked.</p></div>
      <div class="tbl"><table class="dtable compare">
        <thead><tr><th>Step</th><th>Verify</th><th>Assure</th><th class="us">Complete</th></tr></thead>
        <tbody>{''.join(f'<tr><td>{E(a)}</td><td>{b}</td><td>{c}</td><td class="us">{d}</td></tr>' for a, b, c, d in [
          ("Licence, ERC and plant approval", "✓", "✓", "Included"),
          ("Market listing (EU, SFDA, GACC, FDA)", "✓", "✓", "Included"),
          ("Factory or packhouse visit", "✓", "On request", "Included"),
          ("Raw-material and in-process QC", "—", "✓", "Included"),
          ("Lab release for the lot", "—", "✓", "Included"),
          ("AQL pre-shipment inspection", "—", "✓", "Included"),
          ("Document check before issue", "—", "✓", "Included"),
          ("Loading supervision and temperature log", "—", "✓", "Included"),
          ("Competing plant offers and negotiation", "—", "—", "Included"),
          ("Freight booking and tracking", "—", "—", "Included"),
          ("Claims handled for you", "—", "Support", "Included"),
          ("Service-fee refund if released goods miss specification", "—", "—", "Included"),
        ])}</tbody>
      </table></div>
    </div>
  </section>

{faq_html(FAQ_SVC, "Service questions")}
''' + FOOT
    write("services.html", svc)

    # ---------- FOOD & CROPS
    food_items = [p for p in P if CAT[p[1]][2] == "food"]
    food_list = {"@type": "ItemList", "name": "Bangladeshi food and crop exports", "numberOfItems": len(food_items),
                 "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{SITE}/products.html#p-{p[0]}", "name": p[2]} for i, p in enumerate(food_items)]}
    FAQ_FOOD = [
     ("Can GFG source food products as well as seafood?", f"Yes. We source {N_FOOD} food and crop lines from Bangladesh, including aromatic rice, spices, tea, fresh vegetables and fruit, frozen foods and packaged foods, with the same QC gates and compliance checks as seafood."),
     ("When is Bangladeshi mango available for export?", "From May to August. Himsagar and Langra peak in June, Amrapali and Fazli in July."),
     ("How is fresh produce shipped from Bangladesh?", "Mostly by air from Dhaka for leafy greens, gourds and fruit, and by reefer container for potato, pumpkin, frozen food and packaged goods."),
    ]
    food = head(f"Bangladesh Food & Crop Exports: Rice, Produce, Spices, Tea | {SHORT}",
                f"Buyer's broker for {N_FOOD} Bangladeshi food and crop products: aromatic rice, tea, spices, potato, vegetables, mango, jackfruit, frozen and packaged foods. Sourcing regions, harvest calendar and QC.",
                "food.html", [crumbs_ld("Food & crops", "food.html"), food_list, faq_ld(FAQ_FOOD)], "../img/vegetable-market-chillies-potatoes-lg.jpg") + header("food") + "\n" + page_hero(
        "Food &amp; crops", "Bangladeshi food and crops, sourced to your specification.",
        f"{N_FOOD} food and crop lines, from Sylhet tea and aromatic rice to Rajshahi mango and packaged foods, with the same QC and compliance as our seafood.", None, level="0.72", image="vegetable-market-chillies-potatoes") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> Bangladesh exports aromatic rice, tea, spices, potatoes, fresh vegetables, seasonal fruit such as mango and lychee, frozen paratha and snacks, and a wide range of packaged foods. Fresh produce needs a DAE phytosanitary certificate; processed food buyers usually require HACCP, BRCGS or FSSC 22000, plus Halal for Muslim markets.</p>
      <div class="sectors" style="margin-top:2rem">
{sectors_html()}
      </div>
    </div>
  </section>

  <section style="padding-top:0">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">From Bangladeshi fields</p><h2>Graded at source, packed to your specification.</h2></div>
        <p class="lede">Rice, vegetables and fruit from the farms and wholesale markets our suppliers buy from.</p></div>
      <div class="mosaic">
        {figure("rice-grains-falling", "Premium polao rice, milled to your grade", "photo m-wide")}
        {figure("bitter-gourd", "Bitter gourd and summer gourds")}
        {figure("cauliflower-broccoli", "Winter vegetables, November–March")}
        {figure("potato-harvest", "Table potato, harvested February–April")}
        {figure("paddy-harvest-farmers", "Bengal farmers threshing ripe paddy", "photo m-tall")}
        {figure("red-rice", "Brown rice")}
        {figure("tomatoes-beans-market", "Tomatoes, beans and green chilli", "photo m-wide2")}
      </div>
    </div>
  </section>

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head">
        <div><p class="eyebrow">Harvest calendar</p><h2>Book at the right time, at the right price.</h2></div>
        <p class="lede">Prices are lowest and quality highest at peak harvest. We tell you when to book, and hold stock in cold storage for year-round lines.</p>
      </div>
      <div class="tbl">{calendar_html()}</div>
      <p class="cal-key"><span class="k pk"></span> Peak season <span class="k on"></span> Available <span class="k"></span> Off season or limited</p>
      <p class="src">Indicative calendar. Weather, fishing bans and export policy can shift timing each year.</p>
    </div>
  </section>

  <section>
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Where it grows</p>
        <h2 style="margin:.6rem 0 1.5rem">Sourcing regions</h2>
        <div class="tbl"><table class="dtable"><thead><tr><th>Sector</th><th>Main regions</th></tr></thead><tbody>{regions_rows()}</tbody></table></div>
      </div>
      <div>
        <p class="eyebrow">Food-specific QC</p>
        <h2 style="margin:.6rem 0 1.5rem">What we check on food</h2>
        <ul class="ticks">
          <li><b>Pesticide residues</b> tested against your market's maximum residue limits.</li>
          <li><b>Phytosanitary certificate</b> from the DAE Plant Protection Wing for every fresh consignment.</li>
          <li><b>Aflatoxin, illegal dyes and heavy metals</b> tested in spices, rice and dried products.</li>
          <li><b>Moisture, grade and foreign matter</b> checked for rice, spices and tea.</li>
          <li><b>Labels and allergens</b> checked against your market's rules before printing.</li>
          <li><b>Factory certification</b> (HACCP, BRCGS, FSSC 22000, Halal) verified for processed food.</li>
        </ul>
        <a class="btn btn-navy" style="margin-top:1.5rem" href="quality.html#risk">See all import risk controls</a>
      </div>
    </div>
  </section>

{faq_html(FAQ_FOOD, "Food sourcing questions")}

{cta_band('school-underwater','Food &amp; crops','Need rice, produce, spices or packaged food?','Tell us the product, specification, volume and destination. You get a price offer within 24 hours.')}
''' + FOOT
    write("food.html", food)

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
        <div class="f"><label for="servicePackage">Service package</label><select id="servicePackage" name="servicePackage"><option value="complete">Complete: end-to-end, tension-free</option><option value="assure">Assure: QC &amp; compliance per container</option><option value="verify">Verify: supplier check only</option><option value="programme">Programme: recurring supply</option><option value="advise">Not sure, advise me</option></select></div>
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
    pages = ["index.html", "products.html", "food.html", "services.html", "sourcing.html", "quality.html", "markets.html", "guide.html", "contact.html"]
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

> {BRAND} ({SHORT}) is a Bangladesh-based one-stop food sourcing company that works for buyers, covering seafood, food and crops. Its mission is to be the world's best and most trusted food sourcing company. We match importers worldwide with licensed Bangladeshi exporters, verify plant approvals (DoF FIQC, EU, SFDA, GACC, US FDA) and lab results, and manage quotes, inspection, documents and reefer or air shipment.

Key facts
- Network: {NET['mapped']} registered Bangladeshi seafood exporters mapped across {NET['districts']} districts (EPB directory); food and produce exporters reached through BAPA (~{NET['bapa']} members) and BFVAPEA (~{NET['bfvapea']} members); {NET['all_short']} suppliers on our shortlist ({NET['shortlisted']} seafood, {NET['food_short']} food).
- Products: {N_PRODUCTS} export lines ({N_FISH} seafood, {N_FOOD} food).
- Reference prices (public): hilsa government minimum export price US$12.50/kg (2025); aromatic rice minimum export price US$1.60/kg FOB (2025–26); Bangladeshi frozen shrimp US$8.25–15.20/kg (2024, Tridge); table potato about US$300/t (2025). Firm offers depend on grade and compliance.
- Terms: FOB Chattogram, CFR or CIF; air freight from Dhaka for live and chilled products. Quotes within 24 hours.
- Minimum order: usually one 20-foot reefer per product.

Pages
- [Product directory]({SITE}/products.html): every product with scientific name, Bangla name, HS heading, forms and main markets
- [Services & fees]({SITE}/services.html): Verify US$150 per supplier; Assure US$290 per container (lab tests at cost); Complete 1.5% of FOB (min US$450 per container) with a service-fee refund guarantee; supply programmes from US$750/month
- [Food & crops]({SITE}/food.html): food and crop sectors, sourcing regions and a harvest calendar
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
