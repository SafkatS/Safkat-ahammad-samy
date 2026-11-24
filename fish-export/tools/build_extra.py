"""Extra English pages: dry food, fresh vegetables, Gulf importers, Bengali grocery importers.

Called from tools/build_site.py; B is the build_site module (helpers, catalogue, layout).
"""

SRC_SPICE = ("OEC: Bangladesh spice exports by destination", "https://oec.world/profile/bilateral-product/spices/reporter/bgd")
SRC_SHUTKI = ("The Financial Express: how shutki can be a mainstay of Bangladesh's fisheries exports",
              "https://thefinancialexpress.com.bd/economy/bangladesh/how-shutki-can-be-a-mainstay-of-bangladeshs-robust-fisheries-export-sector")
SRC_SFDA = ("SFDA: conditions and requirements for food clearance (April 2025)", "https://sfda.gov.sa/sites/default/files/2025-04/ConditionsRequirementsFoodClearanceE.pdf")

# Dry-food groups: title, product ids, who buys, peak demand, typical shelf life, packs
DRY = [
 ("Dried fish (shutki)", ["dl", "dr", "ds", "dm", "dpf", "dan", "dcr", "nh"], "Gulf importers; Bengali grocers in the UK, USA and Italy",
  "Year-round; drying season October–March", "6–12 months, vacuum packed", "Vacuum packs 100 g–1 kg; 5–20 kg cartons"),
 ("Rice, muri, chira & semai", ["ar", "rr", "mu", "ch", "kh", "se", "rf"], "Gulf importers and Bengali grocers everywhere",
  "Peaks before Ramadan, Eid and winter (pitha season)", "Rice 12–18 months; muri 4–6 months; chira and semai 9–12 months", "Retail packs 250 g–5 kg; 25 kg bags"),
 ("Spices & tea", ["tu", "rc", "co", "nc", "bay", "msd", "pp", "sm", "te", "gt2", "ses"], "Gulf importers (the UAE, Kuwait and Oman are top buyers of Bangladeshi spices); Bengali grocers",
  "Year-round", "Whole spices 12–24 months; powders 12 months; tea up to 24 months", "Retail packs 50 g–1 kg; 25 kg bags; tea chests"),
 ("Biscuits, snacks, noodles & pulses", ["bi", "rus", "sn", "nd", "len", "rm"], "Gulf supermarkets and Bengali grocers",
  "Ramadan and Eid; school terms", "Biscuits and toast 6–12 months; chanachur 4–6 months; pulses 12 months", "Retail packs in master cartons; private label available"),
 ("Oil, jaggery & honey", ["mo2", "jg", "cj", "hn"], "Bengali grocers; Gulf specialty buyers", "Jaggery December–February; oil and honey year-round",
  "Mustard oil 12 months; jaggery 6–9 months; honey 24 months", "PET bottles, tins, blocks, glass jars"),
]

AIR = {"po", "pk2", "ag", "ta", "cb"}   # vegetables that also ship by sea (reefer)


def build(B):
    E, P, CAT, BRAND, SHORT, SITE, WA, FOOT = B.E, B.P, B.CAT, B.BRAND, B.SHORT, B.SITE, B.WA, B.FOOT
    byid = {p[0]: p for p in P}
    out = []

    def link(pid):
        p = byid[pid]
        return f'<a href="{B.pslug(p)}">{E(p[2])}</a>'

    def rows(ids, extra_cols):
        body = []
        for pid in ids:
            p = byid[pid]
            cells = "".join(f"<td>{E(c(p))}</td>" for _, c in extra_cols)
            bn = f'<br><small lang="bn">{E(B.BN_NAME[pid])}</small>' if pid in B.BN_NAME else ""
            body.append(f'<tr><td>{link(pid)}{bn}</td>{cells}'
                        f'<td><button class="add" type="button" data-add="{pid}" aria-pressed="false">Add to quote</button></td></tr>')
        head = "".join(f"<th>{E(h)}</th>" for h, _ in extra_cols)
        return f'<div class="tbl"><table class="dtable prodtable"><thead><tr><th>Product</th>{head}<th><span class="sr">Quote</span></th></tr></thead><tbody>{"".join(body)}</tbody></table></div>'

    def src(t):
        return f'<a href="{t[1]}" rel="noopener" target="_blank">{E(t[0])}</a>'

    def season(p):
        return B.SEASON.get(p[0], B.CAT_INFO[p[1]]["season"])

    ramadan = "".join(f'<li class="tilt3d"><b>{E(a)}</b><span>{E(b)}</span></li>' for a, b in B.RAMADAN)

    # ------------------------------------------------------------------ DRY FOOD
    faqs = [
     ("Which Bangladeshi dry foods are most in demand in the Gulf?", "Spices, dried fish, aromatic rice, puffed and flattened rice, semai, biscuits and snacks. The UAE is the largest buyer of Bangladeshi spices, followed by Malaysia, Kuwait and Oman, and the Middle East is the main market for Bangladeshi dried fish."),
     ("What is the minimum order for dry food?", "From 500 kg per product, or one mixed container that combines several products and suppliers. Dried fish and spices can also go by air in vacuum packs for trial orders."),
     ("Do the packs have Arabic labels?", "They can. Gulf markets require Arabic labelling with production and expiry dates. We check the label text against GCC rules before printing, and many suppliers already print bilingual packs."),
     ("When should I order for Ramadan 2027?", "Ramadan is expected to begin around 8 February 2027, depending on the moon sighting. To have stock on Gulf shelves in late January, confirm the order by 15 December 2026."),
     ("How do you check dried fish quality?", "We test moisture, salt and pesticide residues for every lot, because insecticide misuse during drying is a known risk. Only lots that pass are packed and shipped."),
    ]
    groups = "".join(f'''
      <article class="drygroup tilt3d" id="g{i}">
        <h3>{E(t)}</h3>
        <dl class="drydl"><div><dt>Who buys</dt><dd>{E(who)}</dd></div><div><dt>Peak demand</dt><dd>{E(peak)}</dd></div><div><dt>Typical shelf life</dt><dd>{E(life)}</dd></div><div><dt>Packs</dt><dd>{E(packs)}</dd></div></dl>
        <p class="related">{"".join(f'<a class="chip" href="{B.pslug(byid[pid])}">{E(byid[pid][2])}</a>' for pid in ids)}</p>
      </article>''' for i, (t, ids, who, peak, life, packs) in enumerate(DRY))
    all_dry = [pid for _, ids, *_ in DRY for pid in ids]
    page = B.head("Dry Food from Bangladesh: Dried Fish, Rice, Spices, Muri & Semai Wholesale | GFG",
                  "Wholesale dry food from Bangladesh for Gulf importers and Bengali grocers: shutki, aromatic rice, muri, chira, semai, spices, tea, biscuits and pulses. Arabic labels, lab-tested lots, Ramadan 2027 orders open.",
                  "dry-food.html", [B.crumbs_ld("Dry food", "dry-food.html"), B.faq_ld(faqs),
                                    {"@type": "ItemList", "name": "Dry food from Bangladesh", "itemListElement": [
                                        {"@type": "ListItem", "position": i + 1, "url": f"{SITE}/{B.pslug(byid[pid])}", "name": byid[pid][2]} for i, pid in enumerate(all_dry)]}],
                  "../img/dry-goods-sacks-lg.jpg") + B.header("dryfood") + "\n" + B.page_hero(
        "Dry food", "Dry food from Bangladesh, sourced for Gulf and Bengali grocery buyers",
        "Dried fish, aromatic rice, muri, chira, semai, spices, tea, biscuits and pulses: the dry foods your customers buy every week, checked lot by lot and packed with the labels your market needs.",
        None, image="dry-goods-sacks", extra='<div class="actions" style="margin-top:1.2rem"><a class="btn btn-primary" href="#ramadan">Ramadan 2027 timeline</a><a class="btn btn-wa" href="#" data-wa="Hello GoodBuy Foods Global, I want a dry-food price offer." data-track="whatsapp_click">' + WA + ' WhatsApp</a></div>') + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> Most Bangladeshi dry food is bought by Gulf importers and by Bengali grocery importers abroad. The UAE is the largest buyer of Bangladeshi spices, followed by Malaysia, Kuwait and Oman ({src(SRC_SPICE)}), and the Middle East, especially Saudi Arabia, the UAE and Kuwait, is the main market for dried fish ({src(SRC_SHUTKI)}). Dry food ships in ordinary dry containers, so several products and suppliers can share one container.</p>
      <div class="drygroups">{groups}
      </div>
      <p class="src">Shelf lives are typical values for well-packed product. We check each supplier's declared shelf life and the remaining shelf life at shipment against your market's rules.</p>
    </div>
  </section>

  <section id="ramadan" class="ramadan">
    <div class="wrap">
      <div class="ram-head"><p class="eyebrow">Ramadan 2027</p><h2>Stock on your shelves before Ramadan.</h2>
        <p class="lede">Ramadan is expected to begin around 8 February 2027 and Eid al-Fitr about a month later; exact dates depend on the moon sighting. Work back from the shelf date:</p></div>
      <ol class="ram-steps">{ramadan}</ol>
    </div>
  </section>

  <section id="mixed" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">Build a mixed container</p><h2>Pick the lines. We combine the suppliers.</h2></div>
        <p class="lede">Add products to your quote. We find the best-qualified supplier for each line, check every lot and load them together in one 20′ or 40′ container.</p></div>
      {rows(all_dry, [("HS", lambda p: p[5]), ("Forms", lambda p: p[6]), ("Main markets", lambda p: p[7])])}
      <div class="more"><a class="btn btn-primary" href="contact.html#rfq">Send my mixed-container request</a></div>
    </div>
  </section>

  <section>
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Gulf compliance</p>
        <h2 style="margin:.7rem 0 1.2rem">Cleared first time in the Gulf.</h2>
        <ul class="ticks">
          <li><b>Arabic labels</b> with product name, ingredients, net weight, origin, and production and expiry dates, checked before printing.</li>
          <li><b>Importer registration:</b> in Saudi Arabia the importer registers the establishment and products with the SFDA (Ghad platform) before clearance ({src(SRC_SFDA)}). We prepare the product data you need.</li>
          <li><b>Halal certificates</b> for products with animal-origin ingredients or a Halal claim, from a body your market accepts.</li>
          <li><b>Lab tests per lot:</b> pesticide residues and moisture in dried fish; aflatoxin, Sudan dyes and lead chromate in spices; moisture and foreign matter in rice.</li>
        </ul>
      </div>
      <div>
        <p class="eyebrow">Bengali grocery importers</p>
        <h2 style="margin:.7rem 0 1.2rem">The taste of home, on time for every festival.</h2>
        <ul class="ticks">
          <li><b>Ramadan and Eid:</b> muri, chira, semai, snacks and spices.</li>
          <li><b>Pohela Boishakh (14 April):</b> chira, muri, sweets and pickles.</li>
          <li><b>Winter pitha season:</b> rice flour, khejur gur and aromatic rice.</li>
          <li><b>Durga Puja:</b> spices, sweets and snacks.</li>
        </ul>
        <a class="btn btn-navy" style="margin-top:1.2rem" href="bangladeshi-grocery-importers.html">For Bengali grocery importers</a>
      </div>
    </div>
  </section>

{B.faq_html(faqs, "Dry food: common questions")}

{B.cta_band('iced-snapper', 'Dry food from Bangladesh', 'Tell us the lines and the port.', 'Send product names, packs and volumes. You receive one price offer within 24 hours, with each supplier qualified for your market.')}
''' + FOOT
    B.write("dry-food.html", page); out.append("dry-food.html")

    # ------------------------------------------------------------------ VEGETABLES
    veg = [p[0] for p in P if p[1] == "veg"]
    faqs = [
     ("How do you keep vegetable prices low?", "We buy from packhouses that pack for export, without middle traders; combine many vegetables in one air consignment; book freight at the best rate available for your airport; and move hardy vegetables such as potato, pumpkin, ash gourd, taro and cabbage by sea, which costs far less per kg than air."),
     ("How do you reduce losses on arrival?", "Vegetables are graded and checked at the packhouse on packing day, pre-cooled where needed, and trucked to the airport cargo shed with photos at each step. You receive an arrival report template and we settle shortage or quality claims with the packhouse."),
     ("What is the minimum order?", "From 500 kg per air consignment, mixed across several vegetables. Sea shipments of hardy vegetables start at one 20′ or 40′ reefer."),
     ("Which documents come with each shipment?", "A phytosanitary certificate from the Plant Protection Wing of the Department of Agricultural Extension, a certificate of origin, invoice, packing list and air waybill."),
     ("What does the Fresh service cost?", "US$120 per air consignment up to 3 tonnes, or US$400 per month for a weekly programme of four consignments. Pesticide tests are billed at lab cost."),
    ]
    vrows = rows(veg, [("Season", season), ("Shipped by", lambda p: "Air or sea (reefer)" if p[0] in AIR else "Air"), ("Main markets", lambda p: p[7])])
    page = B.head("Fresh Vegetables from Bangladesh by Air: Weekly Supply for Gulf & UK | GFG",
                  "Weekly fresh vegetables from Bangladesh by air to Gulf and UK buyers: gourds, okra, brinjal, beans, chilli, leafy greens, molokhia, taro and more. Checked on packing day, open costing, landed-cost calculator.",
                  "vegetables.html", [B.crumbs_ld("Fresh vegetables", "vegetables.html"), B.faq_ld(faqs)], "../img/pointed-gourd-brinjal-beans-lg.jpg") + B.header("vegetables") + "\n" + B.page_hero(
        "Fresh vegetables", "Fresh Bangladeshi vegetables, every week, at the best landed price",
        "Gourds, okra, brinjal, beans, green chilli, leafy greens, molokhia, kochur loti and more, checked at the packhouse on packing day and flown from Dhaka to your airport.",
        None, image="pointed-gourd-brinjal-beans") + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> We run weekly air consignments of fresh vegetables from Dhaka for Gulf and UK buyers, and sea shipments for hardy vegetables. You pay the packhouse price, the freight and a fixed QC fee, shown line by line, so you know your landed cost per kg before you order.</p>
      <div class="levers">
        <article class="lever tilt3d"><b>Direct from export packhouses</b><span>No middle traders between the farm group, the packhouse and you.</span></article>
        <article class="lever tilt3d"><b>Mixed consignments</b><span>Many vegetables share one air consignment, so small lines still travel at full-pallet rates.</span></article>
        <article class="lever tilt3d"><b>Sea for hardy lines</b><span>Potato, pumpkin, ash gourd, taro and cabbage go by reefer, at a fraction of the air cost.</span></article>
        <article class="lever tilt3d"><b>Buy in season</b><span>Winter vegetables November–March and gourds April–October cost least at their peak.</span></article>
        <article class="lever tilt3d"><b>Checked on packing day</b><span>Grading, freshness and residues checked before the truck leaves, so you do not pay to fly waste.</span></article>
        <article class="lever tilt3d"><b>Fixed, cost-covering fee</b><span>US$120 per consignment. No percentage mark-up on the vegetables.</span></article>
      </div>
    </div>
  </section>

  <section id="calc-veg" style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Landed cost per kg</p>
        <h2 style="margin:.7rem 0 1.2rem">Know your margin before you order.</h2>
        <p class="lede">Enter the packhouse price, air freight and your selling price. The calculator adds packing, our fee, clearance and an allowance for shrink, so the price you sell at covers every cost.</p>
        <p class="hint" style="margin-top:1rem">All figures are examples for planning, not a price offer. Your offer shows each figure for your airport and week.</p>
      </div>
      <form class="calc" id="vegCalc" onsubmit="return false" aria-labelledby="vegCalcTitle">
        <h3 id="vegCalcTitle">Per air consignment</h3>
        <div class="row">
          <div class="f"><label for="vKg">Consignment (kg)</label><input id="vKg" type="number" min="100" step="100" value="1500" inputmode="numeric"></div>
          <div class="f"><label for="vFob">Packhouse price (US$/kg)</label><input id="vFob" type="number" min="0" step="0.05" value="0.90" inputmode="decimal"></div>
          <div class="f"><label for="vAir">Air freight (US$/kg)</label><input id="vAir" type="number" min="0" step="0.05" value="1.40" inputmode="decimal"></div>
          <div class="f"><label for="vPack">Packing &amp; handling (US$/kg)</label><input id="vPack" type="number" min="0" step="0.01" value="0.15" inputmode="decimal"></div>
          <div class="f"><label for="vLocal">Clearance &amp; delivery (US$)</label><input id="vLocal" type="number" min="0" step="10" value="250" inputmode="numeric"></div>
          <div class="f"><label for="vShrink">Shrink allowance (%)</label><input id="vShrink" type="number" min="0" max="50" step="0.5" value="5" inputmode="decimal"></div>
          <div class="f"><label for="vSell">Your selling price (US$/kg)</label><input id="vSell" type="number" min="0" step="0.05" value="3.60" inputmode="decimal"></div>
        </div>
        <div class="out" aria-live="polite">
          <div><b id="vLanded">—</b><span>landed US$/kg</span></div>
          <div><b id="vMargin">—</b><span>gross margin</span></div>
          <div><b id="vProfit">—</b><span>gross profit per consignment</span></div>
        </div>
        <p class="hint" style="margin-top:.8rem">Includes the Fresh fee of US$120 per consignment. Shrink is the share of weight you expect to lose or discount on arrival.</p>
        <button class="btn btn-ghost" style="margin-top:.8rem" id="vegToRfq" type="button">Send these figures with my request</button>
      </form>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="sec-head"><div><p class="eyebrow">{len(veg)} vegetables</p><h2>What we ship, and when.</h2></div>
        <p class="lede">Add the vegetables you want to your quote. We confirm weekly availability and price every Thursday for the following week.</p></div>
      {vrows}
      <div class="more"><a class="btn btn-primary" href="contact.html#rfq">Request a weekly vegetable offer</a><a class="btn btn-navy" href="services.html#pkg-fresh">See the Fresh service</a></div>
    </div>
  </section>

{B.faq_html(faqs, "Fresh vegetables: common questions")}

{B.cta_band('catch-carp', 'Weekly from Dhaka', 'Start a weekly vegetable programme.', 'Tell us your airport, the vegetables and the weekly volume. We reply with a landed price per kg within 24 hours.')}
''' + FOOT
    B.write("vegetables.html", page); out.append("vegetables.html")

    # ------------------------------------------------------------------ GULF IMPORTERS
    gulf = [m for m in B.MARKETS if m[0] in ("saudi-arabia", "united-arab-emirates", "kuwait", "qatar", "oman")]
    faqs = [
     ("What do Gulf importers buy from Bangladesh?", "Mainly spices, dried fish, frozen fish, aromatic rice, puffed and flattened rice, semai, biscuits, snacks, juices and fresh vegetables, for supermarkets, wholesalers and the large Bangladeshi community in the region."),
     ("Do you support Arabic?", "Yes. Our site is available in Arabic, and we handle enquiries, offers and label checks in Arabic, English and Bangla, including on WhatsApp."),
     ("Who registers products with the SFDA?", "In Saudi Arabia the importer registers the establishment and the food products on the SFDA's Ghad platform before clearance. We prepare the product specifications, label text and certificates you need for registration."),
     ("Is Halal certification included?", "We source products with Halal certificates from bodies your market accepts wherever Halal is required or requested, and we verify each certificate with the issuing body."),
     ("How long does shipping take to the Gulf?", "About 12–25 days by sea from Chattogram, depending on the port and the transhipment hub, and one day by air from Dhaka for fresh vegetables and chilled products."),
    ]
    gtable = "".join(f'<tr><td><a href="import-from-bangladesh-to-{m[0]}.html">{E(m[1][0].upper() + m[1][1:])}</a></td><td>{E(m[3][0])}</td><td>{E(m[6])}</td></tr>' for m in gulf)
    gids = ["dm", "dl", "dpf", "ar", "mu", "ch", "se", "tu", "rc", "bi", "sn", "sp", "rh", "pg", "ok", "gc", "jl", "po"]
    page = B.head("Bangladeshi Food for Gulf Importers: Saudi Arabia, UAE, Kuwait, Qatar, Oman | GFG",
                  "Source Bangladeshi dried fish, rice, spices, snacks, vegetables and frozen fish for the GCC with Arabic labels, Halal certificates and SFDA-ready documents. Arabic-speaking support and Ramadan 2027 planning.",
                  "gulf-food-importers.html", [B.crumbs_ld("Gulf food importers", "gulf-food-importers.html"), B.faq_ld(faqs)], "../img/grain-sacks-market-lg.jpg") + B.header("gulf") + "\n" + B.page_hero(
        "Gulf food importers", "Bangladeshi food for Gulf importers, cleared first time",
        "Saudi Arabia, the UAE, Kuwait, Qatar, Oman and Bahrain: we buy dry food, vegetables and fish for you in Bangladesh and check Arabic labels, Halal certificates and market rules before the container is sealed.",
        None, image="grain-sacks-market", extra='<div class="actions" style="margin-top:1.2rem"><a class="btn btn-primary" href="ar/index.html" lang="ar">الموقع باللغة العربية</a><a class="btn btn-wa" href="#" data-wa="مرحباً GoodBuy Foods Global، أريد عرض سعر." data-track="whatsapp_click">' + WA + ' واتساب</a></div>') + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> The Gulf is the largest market for Bangladeshi dry food. The UAE is the top buyer of Bangladeshi spices, with Kuwait and Oman also in the top five ({src(SRC_SPICE)}), and Saudi Arabia, the UAE and Kuwait are the main markets for Bangladeshi dried fish ({src(SRC_SHUTKI)}). We make sure each shipment meets GCC labelling, Halal and registration rules before it leaves Bangladesh.</p>
      <div class="tbl" style="margin-top:1.5rem"><table class="dtable"><thead><tr><th>Market</th><th>Key rule</th><th>Transit</th></tr></thead><tbody>{gtable}
        <tr><td>Bahrain</td><td>GCC (GSO) standards apply, including Arabic labelling with production and expiry dates.</td><td>Usually via Jebel Ali or Dammam</td></tr></tbody></table></div>
      <p class="related" style="margin-top:1.5rem">{"".join(f'<a class="chip" href="{B.pslug(byid[i])}">{E(byid[i][2])}</a>' for i in gids if i in byid)} <a class="chip" href="products.html">All products →</a></p>
    </div>
  </section>

  <section class="ramadan">
    <div class="wrap">
      <div class="ram-head"><p class="eyebrow">Ramadan 2027</p><h2>Confirm by 15 December 2026 to be on shelves before Ramadan.</h2></div>
      <ol class="ram-steps">{ramadan}</ol>
    </div>
  </section>

{B.PROMISE_HTML}

{B.faq_html(faqs, "Gulf importers: common questions")}

{B.cta_band('school-underwater', 'For Gulf importers', 'Ask in Arabic, English or Bangla.', 'Send the products, packs and port. We reply with a price offer within 24 hours, with label and Halal checks included.')}
''' + FOOT
    B.write("gulf-food-importers.html", page); out.append("gulf-food-importers.html")

    # ------------------------------------------------------------------ BENGALI GROCERY IMPORTERS
    faqs = [
     ("Can I order a mixed container of Bangladeshi groceries?", "Yes. We combine dry food, spices, snacks, oil and sweets from several suppliers in one dry container, and frozen fish, paratha and snacks in one reefer. Each line is checked before loading."),
     ("Which countries do you ship to?", "Bengali grocery importers in the UK, USA, Canada, Italy and the rest of Europe, Malaysia, Australia and the Gulf. We check the rules of each market, such as UK labelling, US FDA prior notice, Canada's SFCR import licence and Australia's biosecurity conditions."),
     ("Can you supply my own brand?", "Yes. Many Bangladeshi processors pack under private label. We manage the artwork review, label compliance for your market and print approval."),
     ("Do you supply fresh vegetables and fish as well?", "Yes. Fresh vegetables go weekly by air from Dhaka, and freshwater and sea fish go frozen in reefer containers."),
     ("Can we talk in Bangla?", "Yes. You can write or call in Bangla, English or Arabic, including on WhatsApp."),
    ]
    mk = [("United Kingdom", "Pre-notification on IPAFFS for food of animal origin; UK labelling and allergen rules."),
          ("United States", "FDA Prior Notice for every shipment; the importer keeps Foreign Supplier Verification records."),
          ("Canada", "The importer needs a Safe Food for Canadians (SFCR) licence; bilingual English and French labels."),
          ("Italy and the EU", "Fish from EU-listed plants only; EU labelling, allergen and residue rules."),
          ("Malaysia", "Import permits for fish; Halal recognised by JAKIM expected for many foods."),
          ("Australia", "Strict biosecurity checks; some products need an import permit (check BICON)."),
          ("Gulf countries", "Arabic labels with production and expiry dates; Halal where required; importer registration.")]
    festivals = [("Ramadan & Eid (from about 8 February 2027)", "Muri, chira, semai, snacks, aromatic rice, spices"),
                 ("Pohela Boishakh (14 April)", "Chira, muri, sweets, pickles and hilsa"),
                 ("Durga Puja (autumn)", "Spices, sweets, snacks, hilsa"),
                 ("Winter pitha season (December–February)", "Rice flour, khejur gur, aromatic rice, winter vegetables")]
    groups = [("Dry food", ["ar", "mu", "ch", "se", "dl", "dm", "len"]), ("Spices & tea", ["tu", "rc", "nc", "pp", "sm", "te"]),
              ("Snacks, biscuits & sweets", ["sn", "bi", "rus", "pk", "sw", "rm"]), ("Oil, gur & honey", ["mo2", "jg", "hn"]),
              ("Frozen", ["fp", "fk", "fr", "rh", "hl", "pb"]), ("Fresh vegetables", ["pt", "tg2", "bg", "lg", "kl2", "sk"])]
    def gchip(i):
        return f'<a class="chip" href="{B.pslug(byid[i])}">{E(byid[i][2])} <span lang="bn">{E(B.BN_NAME.get(i, ""))}</span></a>'
    gl = "".join(f'<article class="drygroup tilt3d"><h3>{E(t)}</h3><p class="related">{"".join(gchip(i) for i in ids)}</p></article>' for t, ids in groups)
    page = B.head("Bangladeshi Grocery Wholesale for Bengali Importers Worldwide: UK, USA, Canada | GFG",
                  "One partner for Bengali grocery importers worldwide: shutki, chinigura rice, muri, chira, semai, mustard oil, spices, frozen fish and fresh vegetables in mixed containers, checked lot by lot. Bangla-speaking support.",
                  "bangladeshi-grocery-importers.html", [B.crumbs_ld("Bengali grocery importers", "bangladeshi-grocery-importers.html"), B.faq_ld(faqs)], "../img/vegetable-market-chillies-potatoes-lg.jpg") + B.header("grocery") + "\n" + B.page_hero(
        "Bengali grocery importers", "Bangladeshi groceries for Bengali importers worldwide",
        "From London to New York, Toronto, Rome, Kuala Lumpur, Sydney and the Gulf: the foods your customers grew up with, in one mixed container from one trusted partner.",
        None, image="vegetable-market-chillies-potatoes", extra='<div class="actions" style="margin-top:1.2rem"><a class="btn btn-primary" href="bn/index.html" lang="bn">বাংলায় দেখুন</a><a class="btn btn-wa" href="#" data-wa="আসসালামু আলাইকুম GoodBuy Foods Global, আমি দাম জানতে চাই।" data-track="whatsapp_click">' + WA + ' WhatsApp</a></div>') + f'''

  <section style="padding-top:1.5rem">
    <div class="wrap">
      <p class="answer"><b>In short:</b> Bengali grocery shops abroad sell hundreds of Bangladeshi lines, but each importer usually deals with many exporters, each with its own minimum order. We combine the lines you need from the best-qualified suppliers into one mixed container, check every lot and handle the documents for your country.</p>
      <div class="drygroups">{gl}</div>
    </div>
  </section>

  <section style="background:var(--surface);border-block:1px solid var(--line)">
    <div class="wrap cols2">
      <div>
        <p class="eyebrow">Festival calendar</p>
        <h2 style="margin:.7rem 0 1.2rem">Stock for every festival, on time.</h2>
        <div class="tbl"><table class="dtable"><thead><tr><th>Festival</th><th>Lines that sell</th></tr></thead><tbody>{"".join(f"<tr><td>{E(a)}</td><td>{E(b)}</td></tr>" for a, b in festivals)}</tbody></table></div>
      </div>
      <div>
        <p class="eyebrow">Rules by country</p>
        <h2 style="margin:.7rem 0 1.2rem">Checked for your market before loading.</h2>
        <div class="tbl"><table class="dtable"><tbody>{"".join(f"<tr><td><b>{E(a)}</b></td><td>{E(b)}</td></tr>" for a, b in mk)}</tbody></table></div>
        <p class="src">Rules change. This is a starting point, not customs advice; we confirm the requirements for each shipment.</p>
      </div>
    </div>
  </section>

{B.PROMISE_HTML}

{B.faq_html(faqs, "Bengali grocery importers: common questions")}

{B.cta_band('catch-carp', 'One container, every line', 'Send your grocery list.', 'Product names in Bangla or English are fine. You receive one price offer within 24 hours.')}
''' + FOOT
    B.write("bangladeshi-grocery-importers.html", page); out.append("bangladeshi-grocery-importers.html")
    return out
