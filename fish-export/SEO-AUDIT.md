# SEO, AI-search and organic discovery audit (24 November 2026)

Scope: every generated page of goodbuyfoods.com (English, Arabic and Bangla), checked by an automated crawler over the site files and in Chromium at desktop (1366 px) and phone (390 px) widths. Targets: Gulf food importers and Bengali grocery buyers worldwide.

What this audit could not measure, and why:
- **Live speed (Core Web Vitals), rankings and backlinks.** The site is not reachable from the audit environment, and the Cloudflare build is failing (see "Do first").
- **Search volumes.** The connected Semrush account has no API units left, so the keyword map below lists target searches, not measured volumes. Check them in Google Search Console after launch.

## Results: before and after

| Check | Live `main` branch (before) | This update (after) |
|---|---|---|
| Pages | 158, English only | 348: 179 English, 165 Arabic, 4 Bangla |
| Titles over 70 characters (cut off in search results) | 74 | 0 |
| Meta descriptions over 175 characters | 64 | 0 |
| Arabic pages for Gulf buyers | none | home, dry food, vegetables, products, services, contact, 5 Gulf import guides, 154 product pages |
| Bangla pages for Bengali buyers | none | home, dry food, vegetables, contact |
| hreflang language links | none | on every page that has a translation; all pairs reciprocal; `x-default` to English |
| Sitemap | English only | 348 URLs with `xhtml:link` language alternates |
| Organisation logo in structured data | pointed to a missing `logo.png` | `assets/img/logo.png` added |
| Broken internal links and assets | 0 | 0 (18,342 references checked) |
| Invalid JSON-LD | 0 | 0 |
| Canonical tags | correct | correct on all 348 pages |
| Pages with 0 or 2+ `<h1>` | 0 | 0 |
| Console errors / horizontal scroll (21 key pages × 2 widths) | n/a | none |
| Outdated fact | "LDC graduation 24 November 2026, deferral requested" | corrected: the UN deferred graduation to 24 November 2029 (General Assembly, 30 October 2026) |

## What changed for organic and AI discovery

1. **Pages for the searches buyers actually make.** New English pages: Dry food, Fresh vegetables, For Gulf food importers, For Bengali grocery importers, and import guides for Kuwait, Qatar and Oman. Each one opens with a short answer to the question it targets, which is the passage search engines and AI assistants quote.
2. **Arabic and Bangla versions** written for the buyer, not machine-translated word for word. Arabic pages use right-to-left layout, Arabic product names (Gulf trade names where they exist, such as الزبيدي, الهامور, الكنعد and الملوخية) and Arabic FAQ structured data.
3. **Structured data** on every page: Organization (now listing GCC and diaspora markets served), WebSite, BreadcrumbList, FAQPage, Product (in Arabic on Arabic product pages) and ItemList on the dry-food page.
4. **llms.txt** updated with the buyer focus, new pages, fees, WhatsApp contact, Arabic and Bangla sections, and the corrected LDC date. `robots.txt` still welcomes the main AI crawlers.
5. **Length fitting.** Titles and descriptions are trimmed automatically so the main keywords come first and nothing is cut off in search results.
6. **Sources cited in the text.** Claims about demand link to their source: OEC for spice destinations, The Financial Express for dried-fish markets, and SFDA for Saudi clearance rules. AI assistants prefer to cite pages that cite evidence.

## Do first (blocks all organic traffic)

1. **Fix the Cloudflare build.** Pull requests still fail `Workers Builds: food-export`. In Cloudflare, open Workers & Pages → food-export → Settings → Build and set root directory `fish-export`, build command empty, deploy command `npx wrangler deploy`. Until a build passes, buyers and search engines cannot see the site.
2. **Google Search Console and Bing Webmaster Tools.** Verify `goodbuyfoods.com` in both (DNS record in Cloudflare) and submit `https://www.goodbuyfoods.com/sitemap.xml`. Bing's index also feeds Microsoft Copilot and other AI assistants.
3. **Google Business Profile.** Set it up with the details in the earlier profile brief, the website and the WhatsApp number.

## Next 30 days

| Priority | Action | Why |
|---|---|---|
| High | A native Arabic speaker reviews the Arabic home, dry-food, vegetables and Saudi guide pages | Gulf buyers judge trust by language quality; check fish trade names for your target ports |
| High | Real photos for top Gulf and Bengali lines: shutki, muri, chira, semai, chinigura rice, molokhia, gourds | Most product pages use placeholder thumbnails; photos also bring image-search traffic |
| High | Confirm `sales@` and `manager@goodbuyfoods.com` exist; connect the n8n webhooks | Every form and email link depends on them |
| Medium | Serve the hero video only on desktop and fast connections (poster image on phones) | The 1.6 MB hero video autoplays on mobile; this is the largest speed cost |
| Medium | Add `sameAs` links (LinkedIn, Facebook page, WhatsApp Business) to the Organization schema once the profiles exist | Helps search engines and AI assistants confirm the company is real |
| Medium | Publish one buyer case study after the first Gulf shipment | Evidence beats claims for both buyers and AI answers |

## Earn links and mentions (off-site)

- **Gulf:** Bangladesh embassy commercial wings in Riyadh, Abu Dhabi, Kuwait City, Doha and Muscat; Bangladesh Business Council Dubai; chambers of commerce in Dubai, Riyadh and Jeddah.
- **Trade fairs:** Gulfood (Dubai) and the Saudi Food Show (Riyadh). Exhibit or visit with a one-page Arabic and English offer and a QR code to `/ar/`.
- **Bengali diaspora:** UK and US Bangladeshi grocery and caterer associations, community business directories, and Facebook and WhatsApp groups of Bengali shop owners in London, New York, Toronto, Rome and Kuala Lumpur.
- **Bangladesh:** EPB exporter directory and BAPA or BFVAPEA channels where eligible, plus LinkedIn posts by the Chairman.

## Keyword map (targets to confirm in Search Console)

| Buyer search (examples) | Language | Page |
|---|---|---|
| dried fish supplier Bangladesh, shutki wholesale, import dried fish to Saudi Arabia | English | `/dry-food.html` and dried-fish product pages |
| استيراد السمك المجفف من بنغلاديش، مورد أرز بنغلاديشي، توابل بنغلاديش بالجملة | Arabic | `/ar/dry-food.html`, `/ar/index.html` |
| خضروات طازجة من بنغلاديش، ملوخية بنغلاديش | Arabic | `/ar/vegetables.html`, `/ar/jute-leaves-molokhia-bangladesh.html` |
| import food from Bangladesh to UAE / Kuwait / Qatar / Oman | English and Arabic | `/import-from-bangladesh-to-*.html`, `/ar/import-from-bangladesh-to-*.html` |
| Bangladeshi grocery wholesale UK / USA / Canada, Bangladeshi food importer | English | `/bangladeshi-grocery-importers.html` |
| বাংলাদেশি গ্রোসারি পাইকারি বিদেশে, শুঁটকি রপ্তানি, তাজা সবজি বিদেশে পাঠানো | Bangla | `/bn/index.html`, `/bn/dry-food.html`, `/bn/vegetables.html` |
| fresh vegetables from Bangladesh by air, Bangladeshi vegetables wholesale | English | `/vegetables.html` |

## How to re-run this audit

From `fish-export/`, rebuild the site and then run the audit:

```bash
python3 tools/build_site.py
```

```bash
python3 tools/audit_site.py .
```

The audit prints a JSON summary. `"issues": {}` means every page passed.
