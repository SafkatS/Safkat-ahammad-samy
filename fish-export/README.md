# Worldclass Bengal Fishers: buyer's-broker website and n8n automation

The website for **Worldclass Bengal Fishers (WBF)**, a Bangladesh-based buyer's broker for seafood and food. WBF's mission is to be the best broker in the world for food importers. The site is written from the buyer's side: better landed cost, lower risk, compliance for the buyer's market and strict QC on every lot. Five n8n workflows capture every buyer and supplier enquiry from the website, WhatsApp and Messenger and send it into HubSpot, email and Google Sheets.

## Pages
| Page | Purpose |
|---|---|
| `index.html` | Buyer value (price, risk, compliance, QC), WBF vs a typical broker, landed-cost and margin calculator, catch videos, best sellers, process, FAQ |
| `products.html` | **Bangladesh export product directory**: 103 products (63 seafood, 40 food) with scientific name, Bangla name, HS heading, forms and markets. Searchable and filterable |
| `quality.html` | Five QC gates, a 13-risk import control matrix with the evidence for each, lab testing, lot trace, cold chain |
| `sourcing.html` | Supplier network (148 exporters mapped, priority tiers, verification steps) and the **supplier application form** |
| `markets.html` | Transit times, reefer load planner, ordering steps, shipping FAQ |
| `guide.html` | Bangladesh seafood and food export guide: the main page for search and AI answers |
| `contact.html` | Quote request form (sent to n8n) plus WhatsApp, Messenger and email |

## Editing
- **Products:** edit `tools/catalog.py`, then run `python3 tools/build_site.py`. This rebuilds every page, `assets/js/catalog.js`, `sitemap.xml`, `robots.txt` and `llms.txt`.
- **Page text, FAQs, network figures and domain:** edit `tools/build_site.py` (`SITE`, `NET`, the FAQ lists, `RISKS`), then rebuild.
- **Contacts and webhooks:** edit the `CONFIG` block at the top of `assets/js/site.js`. Set the WhatsApp number, email, Messenger page and the three n8n webhook URLs (`rfqWebhook`, `eventsWebhook`, `supplierWebhook`). Any webhook left empty runs in demo mode.
- **Domain:** set `SITE` in `tools/build_site.py` to your live domain, then rebuild so canonical URLs, the sitemap and structured data are correct.

## SEO and AI-search (AEO) setup
- A unique title, description, canonical URL, Open Graph tags and Twitter card on every page.
- JSON-LD structured data: Organization, WebSite, BreadcrumbList, FAQPage, Article (guide) and ItemList of 103 Products (directory).
- The directory is plain HTML rather than built by JavaScript, so search engines and AI crawlers can read every product.
- Each section opens with a direct answer, and the guide has a contents list, sources and a last-updated date.
- `llms.txt` gives AI assistants a plain-text summary. `robots.txt` explicitly allows GPTBot, ClaudeBot, PerplexityBot, Google-Extended and other AI crawlers. `sitemap.xml` lists every page.
- **After launch:** submit the sitemap in Google Search Console and Bing Webmaster Tools, create a Google Business Profile, and get listed on the BFFEA and EPB directories, Alibaba, Tridge, Seafood Source, Europages and Kompass. Those backlinks drive ranking.

## n8n workflows (`automation/n8n/`)
| # | Workflow | Trigger | Does |
|---|---|---|---|
| 01 | Website RFQ intake | `POST /webhook/wbf-rfq` | Scores the lead; HubSpot contact and deal; email and WhatsApp confirmation; hot-lead WhatsApp alert; Sheets log |
| 02 | WhatsApp & Messenger inbox | `GET/POST /webhook/wbf-meta` | Meta verification; detects intent; auto-reply on the same channel; HubSpot upsert; hand-off to a trader |
| 03 | Website visitor intent | `POST /webhook/wbf-events` | Logs consented events; scores each visitor's journey; alerts on a high-intent visitor |
| 04 | Quote SLA watchdog | Hourly | Flags HubSpot RFQ deals left without a quote for more than 4 hours |
| 05 | Supplier onboarding | `POST /webhook/wbf-supplier` | Validates and rates the exporter A/B/C; **appends to the WBF_Exporter_List sheet**; HubSpot company; acknowledgement email with NCNDA steps; team alert |

Import each one with **n8n → Import from file**, then edit its **Config** node and attach credentials. Setup details for HubSpot, the WhatsApp Cloud API and Messenger are in `automation/SETUP.md`. Regenerate the workflow files with `python3 automation/build_workflows.py`.

## Images and video still needed
See `assets/ASSET-BRIEF.md` for the shot list with sizes and formats.

## Before going live
- Replace the contact details and email domain, which are placeholders.
- Show only approvals your partner plants actually hold, and keep the network figures in `NET` up to date.
- HS headings are indicative 4-digit codes. Confirm the full code for each shipment.
- The "best broker in the world" line is phrased as WBF's mission. Keep it that way unless you have independent evidence (awards, rankings) to back a factual claim.
