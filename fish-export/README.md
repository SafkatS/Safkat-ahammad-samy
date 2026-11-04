# Oceanora Seafood: export website and n8n automation

A ready-to-deploy website for a seafood export company, plus four n8n workflows that capture every enquiry from the website, WhatsApp and Messenger and send it into HubSpot, email and Google Sheets.

"Oceanora" is a placeholder brand. Change the name, contacts, stats, approvals and registration numbers to your own before going live, and list only the certificates you actually hold.

```
fish-export/
├── index.html                      # the whole site (HTML + CSS + JS, no build step)
└── automation/
    ├── build_workflows.py          # regenerates the workflow JSON
    └── n8n/
        ├── 01-website-rfq-intake.json
        ├── 02-whatsapp-messenger-inbox.json
        ├── 03-website-visitor-intent.json
        └── 04-quote-sla-watchdog.json
```

## Website features

| Section | What it does |
|---|---|
| Hero + reefer readout | Value proposition, example container telemetry, WhatsApp CTA |
| Catalogue | 13 species as spec sheets (cut, count grade, pack, HS code), filterable. **Add to quote** puts them into the RFQ |
| Cold chain | 6 temperature-logged steps, pond to port |
| Quality | Lab test matrix + lot-trace demo (`OCN-26-1187`) |
| Markets | Ports and transit times + **reefer load planner** (cartons / MT per 20′ or 40′) |
| RFQ form | Validated quote request → n8n webhook. Saves a draft locally, has a honeypot, GDPR consent and UTM capture |
| Channels | Floating WhatsApp button, wa.me / m.me / email links |
| Analytics | Visitor events (page views, products added, WhatsApp clicks, RFQ started) sent to n8n, **only after the cookie banner is accepted** |
| SEO | Meta and OG tags, JSON-LD Organization |

### Go live
1. Edit the `CONFIG` block at the top of the `<script>` in `index.html`: WhatsApp number, email, Messenger page, and the two n8n **production** webhook URLs.
2. If the webhook URLs are left empty, the form runs in demo mode.
3. Deploy the folder to any static host: Netlify, Vercel, Cloudflare Pages, GitHub Pages or cPanel.

## n8n workflows

Import: **n8n → Workflows → Import from file**. Then edit the **Config** node in each workflow and attach the credentials (marked `REPLACE_ME`).

### 01 · Website RFQ intake
`POST /webhook/oceanora-rfq`

```
Webhook → Config → Normalize & Score → Respond {ok, ref}
                                        ├─ HubSpot upsert contact → create deal (associated)
                                        ├─ Email confirmation to buyer
                                        ├─ Has WhatsApp? → WhatsApp template "rfq_received"
                                        ├─ Hot lead (score ≥ 60)? → WhatsApp template "new_lead_alert" to sales
                                        ├─ Email to sales desk (full payload)
                                        └─ Google Sheets "RFQ" log
```
The lead score (0–100) is based on volume, buyer type, a business email domain, how much detail the buyer gave, a WhatsApp number, and how many products they picked. Leads are tiered HOT / WARM / COLD, and each gets an estimated deal value.

### 02 · WhatsApp & Messenger inbox
`GET + POST /webhook/oceanora-meta`. Use the same URL for the WhatsApp Business Account and Page webhooks in your Meta App.

```
GET  → verify token → return hub.challenge
POST → parse (WA + Messenger) → intent: greeting | catalog | price | sample | compliance | human | other
       → auto-reply on the same channel → HubSpot upsert (by whatsapp_id / messenger_psid)
       → price/sample/compliance/human? → email hand-off to the export desk
       → Google Sheets "Chats" log
```

### 03 · Website visitor intent
`POST /webhook/oceanora-events`

```
Webhook → parse beacon → drop bots → score the visitor's journey (static data, 7-day TTL)
        → Google Sheets "Events"
        → score ≥ 50 (once per visitor)? → "hot visitor" email to sales
```

### 04 · Quote SLA watchdog
This runs hourly. It finds HubSpot deals that have been in the first stage for more than 4 hours, from the last 7 days, and emails the manager a breach list.

## One-time setup checklist

**HubSpot**
- Create a private app with these scopes: `crm.objects.contacts.read/write` and `crm.objects.deals.read/write`. In n8n, add it as a *HubSpot App Token* credential.
- Create two contact properties as single-line text with **Unique value** ticked: `whatsapp_id` and `messenger_psid`.
- Set `hubspotPipeline` and `hubspotStage` in Config. The defaults are `default` and `appointmentscheduled`.

**WhatsApp Cloud API (Meta)**
- Get a permanent System User token and add it in n8n as *Header Auth*: `Authorization: Bearer <token>`.
- Put the phone number ID into `waPhoneNumberId` in Config.
- Submit these templates for approval (language `en`):
  - `rfq_received` (Utility): "Hi {{1}}, thank you for your quote request {{2}}. Our export desk will send your price offer within 24 hours."
  - `new_lead_alert` (Utility): "New {{1}} lead: {{2}}. Products: {{3}}. Ref {{4}}."
- Webhook: callback URL `…/webhook/oceanora-meta`. The verify token must match `VERIFY_TOKEN` in "Check verify token". Subscribe to the `messages` field.

**Messenger**
- Add a Page access token as *Header Auth* (`Authorization: Bearer <page token>`). Subscribe the Page webhook to `messages`.

**Email / Sheets**
- Add an SMTP credential (Google Workspace, SES, Brevo, etc.).
- Create a Google Sheet with three tabs: `RFQ`, `Chats`, `Events`. Columns are auto-mapped from the first row. Put the sheet ID in Config.

**Webhook CORS**: the webhooks allow `*`. Set `allowedOrigins` to your domain in production.

## GDPR and data handling
- Analytics only start after the visitor accepts the cookie banner.
- The RFQ form needs explicit consent before it submits.
- Visitor intent data in n8n expires after 7 days. For RFQ and chat rows, add a scheduled purge of unconverted leads, for example after 30 days.

## Regenerating the workflows
```bash
python3 automation/build_workflows.py
```
