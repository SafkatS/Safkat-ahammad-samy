#!/usr/bin/env python3
"""Builds the media collection checklist (Excel) from the product catalogue.

  python3 tools/media_checklist.py [output.xlsx]
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from catalog import CATEGORIES, P
import build_site as site
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.worksheet.datavalidation import DataValidation

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(site.ROOT, "GFG_media_checklist.xlsx")
CAT = {c[0]: c for c in CATEGORIES}
HEAD = Font(bold=True, color="FFFFFF"); FILL = PatternFill("solid", fgColor="0A2540")
HAVE = PatternFill("solid", fgColor="DFF3E6"); SHARED = PatternFill("solid", fgColor="FFF4D6"); NEED = PatternFill("solid", fgColor="FBE3DD")

SHOTS = {
 "shrimp": ("1) Raw product on crushed ice or white board (HOSO and HLSO side by side). 2) A row of pieces showing the count grade. 3) Packed: 6×1.8 kg block or 1 kg IQF retail bag with label.",
            "10–15 s: grading or peeling on the line, or a frozen block coming out of the plate freezer."),
 "shell":  ("1) Live or whole product in a crate or on deck. 2) Cleaned or frozen form (tubes, rings, soft-shell). 3) Export pack.",
            "10 s: live crab being graded and packed, or squid being cleaned."),
 "marine": ("1) Whole fish on ice, full side view, eye and gills visible. 2) Steaks or gutted form if sold. 3) Master carton or frozen block.",
            "8–10 s: landing at the fish harbour, or fish being iced and boxed."),
 "fresh":  ("1) Whole fish on ice, full side view. 2) Steaks or curry cut if sold. 3) Frozen pack or chilled carton.",
            "8–10 s: pond harvest net or grading at the depot."),
 "live":   ("1) Live product in tank or crate. 2) Air-freight styrofoam pack with label.",
            "8 s: live eel or crab being packed for air freight."),
 "dried":  ("1) Close-up of texture on a neutral surface. 2) Retail vacuum pack and master carton.",
            "8 s: sun-drying racks at Cox's Bazar or Chattogram."),
 "rice":   ("1) Grain macro on dark or neutral background. 2) Bags: 1 kg retail and 25 kg export.",
            "8 s: milling, sorting or bag filling."),
 "spice":  ("1) Whole and powdered forms side by side. 2) Retail pack and bulk bag.",
            "8 s: drying in the yard, grinding, or tea plucking (for tea)."),
 "veg":    ("1) Fresh product at farm or packhouse. 2) Graded and packed in an export carton with label.",
            "8 s: washing, grading or packing at a packhouse."),
 "fruit":  ("1) On the tree or in the orchard. 2) Graded fruit in an export carton with label. 3) Cut fruit, optional.",
            "8 s: harvest and grading at the orchard."),
 "frozen": ("1) Product cooked or plated. 2) Frozen retail pack front.",
            "8 s: production line or the product being cooked."),
 "sweet":  ("1) Product close-up (block, jar, pour). 2) Retail pack.",
            "8 s: jaggery being boiled, or honey being harvested."),
 "processed": ("1) Retail pack front on white (brand visible, with the brand owner's permission). 2) Outer carton. 3) Product served.",
            "Optional: production line, with the factory's permission."),
}


def priority(p):
    pid, cat, *_, featured = p
    if featured: return "A"
    if cat in ("shrimp", "marine", "rice", "fruit", "shell"): return "B"
    return "C"


def main():
    wb = Workbook()
    # ---------------- Sheet 1: products
    ws = wb.active; ws.title = "1 Product media"
    cols = ["#", "Sector", "Category", "Product", "Bangla name", "Scientific name", "HS", "Priority",
            "Photo on site now", "Photo shots to collect", "Video idea (optional)", "File name to use", "Collected? (Yes/No)", "Your notes"]
    ws.append(cols)
    for i, p in enumerate(P, 1):
        pid, cat, name, local, sci, hs, forms, markets, note, featured = p
        img = site.PROD_IMG.get(pid)
        shared = img and sum(1 for v in site.PROD_IMG.values() if v == img) > 1
        status = ("No" if not img else f"Shared photo ({img})" if shared else f"Yes ({img})")
        shots, video = SHOTS[cat]
        slug = name.lower().replace("&", "and").replace("(", "").replace(")", "").replace(",", "").replace("/", "-").replace(" ", "-")
        ws.append([i, "Seafood" if CAT[cat][2] == "fish" else "Food & crops", CAT[cat][1], name, local, sci, hs, priority(p),
                   status, shots, video, f"{pid}_{slug}_1.jpg", "", ""])
        fill = NEED if not img else SHARED if shared else HAVE
        ws.cell(row=i + 1, column=9).fill = fill
    dv = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True); ws.add_data_validation(dv); dv.add(f"M2:M{len(P)+1}")

    # ---------------- Sheet 2: page & brand media
    ws2 = wb.create_sheet("2 Page & brand media")
    ws2.append(["#", "Page / use", "Media needed", "Type", "Spec", "On site now", "Priority", "Collected? (Yes/No)", "Your notes"])
    pages = [
     ("All pages", "Logo: full colour and white versions", "Image", "SVG preferred, or PNG with transparent background, at least 1000 px wide", "No (temporary fish-and-leaf mark)", "A"),
     ("All pages", "Favicon / app icon", "Image", "Square PNG, 512×512", "No", "A"),
     ("All pages (link previews)", "Social share image with brand and tagline", "Image", "1200×630 JPG", "No (uses a product photo)", "A"),
     ("Home: Chairman section", "Chairman portrait (Safkat Ahammad Samy)", "Image", "Head and shoulders, plain light background, formal dress, 1200×1500 JPG, natural light", "No (initials placeholder)", "A"),
     ("Home: Chairman section", "Chairman signature", "Image", "Black ink on white paper, scanned or photographed, PNG", "No", "B"),
     ("Home: Chairman section", "Chairman video message", "Video", "30–60 s, landscape 1920×1080, speaking to camera in English, with subtitles", "No", "B"),
     ("Home hero", "Signature brand video: sea to container", "Video", "10–15 s loop, 1920×1080 or 4K, no music needed", "Yes (red snapper on ice)", "B"),
     ("Food & crops hero", "Field or packhouse video, e.g. export-quality carrot", "Video", "10–15 s loop, landscape", "Pending (your carrot video: please upload in chat)", "A"),
     ("Seafood / Products hero", "Fish landing or grading video, e.g. Ritha & Laal Poa", "Video", "10–15 s loop, landscape", "Pending (your Ritha & Laal Poa video: please upload in chat)", "A"),
     ("Quality & risk", "QC officer checking count, glaze or weight", "Image + video", "Landscape photo 1600 px; 10 s video", "No", "A"),
     ("Quality & risk", "Lab technician testing samples", "Image", "Landscape 1600 px, lab coat, clean bench", "No", "A"),
     ("Quality & risk", "Reefer container loading, with temperature display visible", "Image + video", "Landscape; 10 s video", "No", "A"),
     ("Quality & risk", "Sample inspection report and lab certificate (personal data blurred)", "Image / PDF", "Scan or clear photo", "No", "B"),
     ("Services & fees", "GFG team member inspecting product for a buyer (video call or on site)", "Image", "Landscape 1600 px", "Shared (buyer checking greens)", "B"),
     ("Suppliers", "Supplier plant or packhouse exterior with signage (with permission)", "Image", "Landscape 1600 px", "No", "B"),
     ("Suppliers", "Meeting with exporters or an association", "Image", "Landscape 1600 px", "No", "C"),
     ("Markets & logistics", "Chattogram port or a container vessel", "Image + video", "Landscape; 10 s video", "No", "B"),
     ("Markets & logistics", "Air-freight cargo at Dhaka airport (live crab, vegetables)", "Image", "Landscape 1600 px", "No", "C"),
     ("Guide", "Map of sourcing regions (we can design this)", "Graphic", "We create it from the region table", "No", "C"),
     ("Contact", "Office or warehouse exterior with signage", "Image", "Landscape 1600 px", "No", "B"),
     ("About (future page)", "Team photos: QC lead, sourcing lead, sales", "Image", "Same style as the Chairman portrait, 1200×1500", "No", "B"),
     ("Trust", "Certificates and registrations: trade licence, ERC, memberships", "Image / PDF", "Clear scans; we display logos or extracts only", "No", "A"),
     ("Sugar & sweeteners sector card", "Date-palm jaggery or honey", "Image", "Landscape 1600 px", "No (placeholder colour)", "A"),
    ]
    for i, r in enumerate(pages, 1):
        ws2.append([i, *r, "", ""])
    dv2 = DataValidation(type="list", formula1='"Yes,No"', allow_blank=True); ws2.add_data_validation(dv2); dv2.add(f"H2:H{len(pages)+1}")

    # ---------------- Sheet 3: Chairman profile
    ws3 = wb.create_sheet("3 Chairman profile")
    ws3.append(["Field", "Draft on site now (please confirm or correct)", "Your final text"])
    for row in [
     ("Full name", "Safkat Ahammad Samy", ""),
     ("Title", "Chairman, GoodBuy Foods Global", ""),
     ("Education", "International business specialist; Master of International Trade and Business (MITB), University of Dhaka", ""),
     ("Years of experience in trade / sourcing", "(please add)", ""),
     ("Short bio (2–3 sentences)", "Safkat Ahammad Samy is an international business specialist with a Master of International Trade and Business (MITB) from the University of Dhaka. He leads GoodBuy Foods Global with a single rule: the buyer wins first, and built GFG to give importers one accountable partner in Bangladesh for price, quality and compliance.", ""),
     ("Chairman's message", "See the home page. Three short paragraphs on buyer-first sourcing, strict QC and long-term partnership.", ""),
     ("LinkedIn profile URL", "(please add)", ""),
     ("Photo", "Head and shoulders, 1200×1500 JPG", ""),
     ("Signature", "PNG, optional", ""),
    ]:
        ws3.append(row)

    # ---------------- Sheet 4: already received
    ws4 = wb.create_sheet("4 Media received")
    ws4.append(["File (site name)", "Description", "Used on"])
    used = {}
    for page in ["index", "products", "food", "services", "sourcing", "quality", "guide"]:
        html = open(os.path.join(site.ROOT, page + ".html")).read()
        for n in site.PHOTO:
            if f"assets/img/{n}-" in html:
                used.setdefault(n, []).append(page)
    for n, d in site.PHOTO.items():
        ws4.append([n, d, ", ".join(used.get(n, [])) or "—"])
    for v, d in [("iced-snapper.mp4", "Red snapper on ice"), ("catch-carp.mp4", "Cultivated carp harvest"), ("catch-pangasius.mp4", "Pangasius harvest"),
                 ("ice-holding.mp4", "Frozen snapper, organised"), ("school-underwater.mp4", "School of fish underwater")]:
        ws4.append([v, d, "Video headers and catch reel"])

    for w in wb.worksheets:
        for c in w[1]:
            c.font = HEAD; c.fill = FILL; c.alignment = Alignment(wrap_text=True, vertical="center")
        w.freeze_panes = "A2"
        for col in w.columns:
            letter = col[0].column_letter
            longest = max(len(str(c.value or "")) for c in col)
            w.column_dimensions[letter].width = min(max(10, longest * 0.9), 60)
            for c in col[1:]:
                c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(OUT)
    n_no = sum(1 for p in P if p[0] not in site.PROD_IMG)
    print(f"saved {OUT}: {len(P)} products, {len(P) - n_no} with a photo, {n_no} need one; {len(pages)} page/brand items")


if __name__ == "__main__":
    main()
