#!/usr/bin/env python3
"""Generates the importable n8n workflow JSON files in ./n8n.

Run:  python3 automation/build_workflows.py
Edit the CONFIG values inside each workflow's "Config" node after import
(or here, then re-run) — no secrets live in these files; credentials are
attached in n8n.
"""
import json, os, uuid

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "n8n")
os.makedirs(OUT, exist_ok=True)

GRAPH = "https://graph.facebook.com/v21.0"
HUBSPOT = "https://api.hubapi.com"

CRED_HUBSPOT = {"hubspotAppToken": {"id": "REPLACE_ME", "name": "HubSpot Private App"}}
CRED_WA = {"httpHeaderAuth": {"id": "REPLACE_ME", "name": "WhatsApp Cloud API (Bearer)"}}
CRED_PAGE = {"httpHeaderAuth": {"id": "REPLACE_ME", "name": "Meta Page Token (Bearer)"}}
CRED_SMTP = {"smtp": {"id": "REPLACE_ME", "name": "SMTP export desk"}}
CRED_SHEETS = {"googleSheetsOAuth2Api": {"id": "REPLACE_ME", "name": "Google Sheets"}}

CONFIG_JS = r"""// ⚙ Edit once after import. Read by every node via $('Config').first().json
return [{ json: {
  ...$input.first().json,
  cfg: {
    brand: 'GoodBuy Foods Global',
    salesEmail: 'sales@goodbuyfood.com',
    managerEmail: 'manager@goodbuyfood.com',
    fromEmail: 'GoodBuy Foods Global <sales@goodbuyfood.com>',
    waPhoneNumberId: 'REPLACE_WA_PHONE_NUMBER_ID',
    salesWhatsApp: '8801700000000',
    sheetId: 'REPLACE_GOOGLE_SHEET_ID',
    hubspotPipeline: 'default',
    hubspotStage: 'appointmentscheduled',
    hotScore: 60,
    catalogueUrl: 'https://www.goodbuyfood.com/products.html'
  }
}}];"""


class WF:
    def __init__(self, name):
        self.name, self.nodes, self.conn, self.x = name, [], {}, 0

    def node(self, name, type_, params, pos, version, creds=None, on_error=None, **extra):
        n = {"parameters": params, "id": str(uuid.uuid4()), "name": name,
             "type": type_, "typeVersion": version, "position": pos}
        if creds:
            n["credentials"] = creds
        if on_error:
            n["onError"] = on_error
        n.update(extra)
        self.nodes.append(n)
        return name

    def link(self, a, b, out=0):
        outs = self.conn.setdefault(a, {"main": []})["main"]
        while len(outs) <= out:
            outs.append([])
        outs[out].append({"node": b, "type": "main", "index": 0})

    def save(self, fname, tags):
        data = {"name": self.name, "nodes": self.nodes, "connections": self.conn,
                "active": False, "settings": {"executionOrder": "v1", "saveManualExecutions": True},
                "pinData": {}, "meta": {"templateCredsSetupCompleted": False},
                "tags": [{"name": t} for t in tags]}
        with open(os.path.join(OUT, fname), "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("wrote", fname, len(self.nodes), "nodes")


# ---------- shared node builders ----------
def webhook(wf, name, path, method, pos, mode):
    return wf.node(name, "n8n-nodes-base.webhook",
                   {"httpMethod": method, "path": path, "responseMode": mode,
                    "options": {"allowedOrigins": "*"} if method == "POST" else {}},
                   pos, 2, webhookId=str(uuid.uuid4()))


def code(wf, name, js, pos, mode="runOnceForAllItems"):
    p = {"jsCode": js}
    if mode != "runOnceForAllItems":
        p["mode"] = mode
    return wf.node(name, "n8n-nodes-base.code", p, pos, 2)


def http(wf, name, method, url, body_expr, pos, creds, cred_type=None, query=None):
    p = {"method": method, "url": url, "sendBody": True, "specifyBody": "json",
         "jsonBody": body_expr, "options": {"timeout": 15000}}
    if cred_type == "hubspot":
        p.update({"authentication": "predefinedCredentialType", "nodeCredentialType": "hubspotAppToken"})
    else:
        p.update({"authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth"})
    if query:
        p["sendQuery"] = True
        p["queryParameters"] = {"parameters": [{"name": k, "value": v} for k, v in query.items()]}
    return wf.node(name, "n8n-nodes-base.httpRequest", p, pos, 4.2, creds=creds,
                   on_error="continueRegularOutput", retryOnFail=True, maxTries=3, waitBetweenTries=2000)


def email(wf, name, to, subject, html, pos):
    return wf.node(name, "n8n-nodes-base.emailSend",
                   {"fromEmail": "={{ $('Config').first().json.cfg.fromEmail }}", "toEmail": to,
                    "subject": subject, "emailFormat": "html", "html": html,
                    "options": {"appendAttribution": False}},
                   pos, 2.1, creds=CRED_SMTP, on_error="continueRegularOutput")


def if_node(wf, name, left, op, right, pos, rtype="number"):
    cond = {"id": str(uuid.uuid4()), "leftValue": left, "operator": op}
    if right is not None:
        cond["rightValue"] = right
    return wf.node(name, "n8n-nodes-base.if",
                   {"conditions": {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose"},
                                   "conditions": [cond], "combinator": "and"}, "options": {}},
                   pos, 2)


def sheets_append(wf, name, sheet, pos):
    return wf.node(name, "n8n-nodes-base.googleSheets",
                   {"operation": "append",
                    "documentId": {"__rl": True, "mode": "id", "value": "={{ $('Config').first().json.cfg.sheetId }}"},
                    "sheetName": {"__rl": True, "mode": "name", "value": sheet},
                    "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": []},
                    "options": {}},
                   pos, 4.5, creds=CRED_SHEETS, on_error="continueRegularOutput")


def wa_body(to_expr, template, params_exprs):
    """WhatsApp Cloud API template message body as an n8n expression."""
    params = ", ".join("{ type: 'text', text: String(%s) }" % p for p in params_exprs)
    return ("={{ JSON.stringify({ messaging_product: 'whatsapp', to: %s, type: 'template', "
            "template: { name: '%s', language: { code: 'en' }, components: [ { type: 'body', parameters: [ %s ] } ] } }) }}"
            % (to_expr, template, params))


# =====================================================================
# 01 — Website RFQ → HubSpot + WhatsApp + Email + Sheets
# =====================================================================
wf = WF("GFG · 01 Website RFQ intake")
webhook(wf, "RFQ Webhook", "gfg-rfq", "POST", [0, 300], "responseNode")
code(wf, "Config", CONFIG_JS, [220, 300])
code(wf, "Normalize & Score", r"""const cfg = $('Config').first().json.cfg;
const b = $('RFQ Webhook').first().json.body || {};
const clean = s => String(s ?? '').trim().slice(0, 2000);
const email = clean(b.email).toLowerCase();
if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) throw new Error('Invalid email');
if (b.website) throw new Error('Honeypot triggered');            // bot

const [firstname, ...rest] = clean(b.name).split(/\s+/);
const wa = clean(b.whatsapp).replace(/[^\d]/g, '');
const products = Array.isArray(b.products) ? b.products : [];

// Lead score 0–100: volume, buyer type, completeness, intent
const volScore = { 'sample': 5, 'lcl': 10, '1': 25, '2-4': 40, '5+': 50 }[b.volume] ?? 10;
const typeScore = /retail|importer/i.test(b.buyerType) ? 15 : /food service|processor/i.test(b.buyerType) ? 10 : 5;
const freeMail = /@(gmail|yahoo|hotmail|outlook|icloud|aol|mail)\./i.test(email) ? 0 : 10;
const detail = clean(b.details).length > 40 ? 10 : 0;
const score = Math.min(100, volScore + typeScore + freeMail + detail + (wa ? 5 : 0) + Math.min(products.length * 3, 10));
const tier = score >= cfg.hotScore ? 'HOT' : score >= 35 ? 'WARM' : 'COLD';

// Rough deal value in USD (FOB-ish blended $/kg × MT) — refined by sales later
const mt = { 'sample': 0, 'lcl': 8, '1': 21, '2-4': 63, '5+': 105 }[b.volume] ?? 0;
const estValue = Math.round(mt * 1000 * 7.5);

const ref = 'RFQ-' + new Date().toISOString().slice(2, 10).replace(/-/g, '') + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
return [{ json: {
  ref, score, tier, estValue,
  email, firstname: firstname || '', lastname: rest.join(' '),
  name: clean(b.name), company: clean(b.company), country: clean(b.country), port: clean(b.port),
  whatsapp: wa, incoterm: clean(b.incoterm), volume: clean(b.volume), buyerType: clean(b.buyerType),
  shipMonth: clean(b.shipMonth), details: clean(b.details), servicePackage: clean(b.servicePackage) || 'not stated',
  productList: products.map(p => p.name).join(', ') || 'Not specified',
  utmSource: b.utm?.utm_source || '', utmCampaign: b.utm?.utm_campaign || '', gclid: b.utm?.gclid || '',
  visitorId: clean(b.visitorId), page: clean(b.page), submittedAt: b.submittedAt || new Date().toISOString()
}}];""", [440, 300])
wf.node("Respond 200", "n8n-nodes-base.respondToWebhook",
        {"respondWith": "json", "responseBody": "={{ JSON.stringify({ ok: true, ref: $json.ref }) }}",
         "options": {"responseCode": 200}}, [660, 300], 1.1)

http(wf, "HubSpot · Upsert contact", "POST", HUBSPOT + "/crm/v3/objects/contacts/batch/upsert",
     "={{ JSON.stringify({ inputs: [ { idProperty: 'email', id: $('Normalize & Score').first().json.email, properties: {"
     " email: $('Normalize & Score').first().json.email, firstname: $('Normalize & Score').first().json.firstname,"
     " lastname: $('Normalize & Score').first().json.lastname, company: $('Normalize & Score').first().json.company,"
     " country: $('Normalize & Score').first().json.country, phone: $('Normalize & Score').first().json.whatsapp ? '+' + $('Normalize & Score').first().json.whatsapp : '',"
     " hs_lead_status: 'NEW' } } ] }) }}",
     [900, 60], CRED_HUBSPOT, "hubspot")
http(wf, "HubSpot · Create deal", "POST", HUBSPOT + "/crm/v3/objects/deals",
     "={{ JSON.stringify({ properties: { dealname: $('Normalize & Score').first().json.company + ' · ' + $('Normalize & Score').first().json.productList.slice(0,60) + ' (' + $('Normalize & Score').first().json.ref + ')',"
     " pipeline: $('Config').first().json.cfg.hubspotPipeline, dealstage: $('Config').first().json.cfg.hubspotStage,"
     " amount: String($('Normalize & Score').first().json.estValue),"
     " description: 'Tier ' + $('Normalize & Score').first().json.tier + ' (score ' + $('Normalize & Score').first().json.score + ') · Package: ' + $('Normalize & Score').first().json.servicePackage + '\\nProducts: ' + $('Normalize & Score').first().json.productList + '\\nVolume: ' + $('Normalize & Score').first().json.volume + ' · ' + $('Normalize & Score').first().json.incoterm + ' ' + $('Normalize & Score').first().json.port + '\\nShip: ' + $('Normalize & Score').first().json.shipMonth + '\\n\\n' + $('Normalize & Score').first().json.details },"
     " associations: [ { to: { id: $json.results[0].id }, types: [ { associationCategory: 'HUBSPOT_DEFINED', associationTypeId: 3 } ] } ] }) }}",
     [1120, 60], CRED_HUBSPOT, "hubspot")

email(wf, "Email · Buyer confirmation", "={{ $('Normalize & Score').first().json.email }}",
      "=Your quote request {{ $('Normalize & Score').first().json.ref }} — {{ $('Config').first().json.cfg.brand }}",
      "=<div style=\"font-family:Arial,sans-serif;max-width:560px;color:#0A2730\">"
      "<h2 style=\"margin:0 0 12px\">Thank you, {{ $('Normalize & Score').first().json.firstname }}.</h2>"
      "<p>We received your request <b>{{ $('Normalize & Score').first().json.ref }}</b>. Our export desk will send a price offer within 24 hours.</p>"
      "<table style=\"border-collapse:collapse;width:100%;font-size:14px\">"
      "<tr><td style=\"padding:6px 0;color:#4F6B70\">Products</td><td>{{ $('Normalize & Score').first().json.productList }}</td></tr>"
      "<tr><td style=\"padding:6px 0;color:#4F6B70\">Terms</td><td>{{ $('Normalize & Score').first().json.incoterm }} {{ $('Normalize & Score').first().json.port }}</td></tr>"
      "<tr><td style=\"padding:6px 0;color:#4F6B70\">Volume</td><td>{{ $('Normalize & Score').first().json.volume }}</td></tr></table>"
      "<p>Need an answer faster? Reply on WhatsApp: <a href=\"https://wa.me/{{ $('Config').first().json.cfg.salesWhatsApp }}\">chat with the export desk</a>.</p>"
      "<p style=\"color:#4F6B70;font-size:12px\">You received this because you requested a quote. Reply STOP to be removed.</p></div>",
      [900, 220])

if_node(wf, "Has WhatsApp?", "={{ $('Normalize & Score').first().json.whatsapp }}",
        {"type": "string", "operation": "notEmpty", "singleValue": True}, None, [900, 380])
http(wf, "WhatsApp · Buyer confirmation", "POST",
     "=" + GRAPH + "/{{ $('Config').first().json.cfg.waPhoneNumberId }}/messages",
     wa_body("$('Normalize & Score').first().json.whatsapp", "rfq_received",
             ["$('Normalize & Score').first().json.firstname || 'there'",
              "$('Normalize & Score').first().json.ref"]),
     [1120, 360], CRED_WA)

if_node(wf, "Hot lead?", "={{ $('Normalize & Score').first().json.score }}",
        {"type": "number", "operation": "gte"}, "={{ $('Config').first().json.cfg.hotScore }}", [900, 540])
http(wf, "WhatsApp · Alert sales lead", "POST",
     "=" + GRAPH + "/{{ $('Config').first().json.cfg.waPhoneNumberId }}/messages",
     wa_body("$('Config').first().json.cfg.salesWhatsApp", "new_lead_alert",
             ["$('Normalize & Score').first().json.tier + ' ' + $('Normalize & Score').first().json.score",
              "$('Normalize & Score').first().json.company + ' (' + $('Normalize & Score').first().json.country + ')'",
              "$('Normalize & Score').first().json.productList.slice(0,120)",
              "$('Normalize & Score').first().json.ref"]),
     [1120, 520], CRED_WA)
email(wf, "Email · Sales desk", "={{ $('Config').first().json.cfg.salesEmail }}",
      "=[{{ $('Normalize & Score').first().json.tier }}] {{ $('Normalize & Score').first().json.company }} · {{ $('Normalize & Score').first().json.ref }}",
      "=<pre style=\"font:13px/1.5 monospace\">{{ JSON.stringify($('Normalize & Score').first().json, null, 2) }}</pre>"
      "<p>SLA: first price offer within 24 h (HOT: call or WhatsApp within 15 min).</p>",
      [900, 700])

code(wf, "Flatten for sheet", r"""const l = $('Normalize & Score').first().json;
return [{ json: { Ref: l.ref, Submitted: l.submittedAt, Tier: l.tier, Score: l.score, Company: l.company,
  Name: l.name, Email: l.email, WhatsApp: l.whatsapp, Country: l.country, Port: l.port, Incoterm: l.incoterm,
  Volume: l.volume, BuyerType: l.buyerType, Products: l.productList, ShipMonth: l.shipMonth,
  Details: l.details, Package: l.servicePackage, UTMSource: l.utmSource, UTMCampaign: l.utmCampaign, VisitorId: l.visitorId, Status: 'NEW' } }];""",
     [900, 860])
sheets_append(wf, "Sheets · RFQ log", "RFQ", [1120, 860])

for a, b in [("RFQ Webhook", "Config"), ("Config", "Normalize & Score"), ("Normalize & Score", "Respond 200"),
             ("HubSpot · Upsert contact", "HubSpot · Create deal"), ("Has WhatsApp?", "WhatsApp · Buyer confirmation"),
             ("Hot lead?", "WhatsApp · Alert sales lead"), ("Flatten for sheet", "Sheets · RFQ log")]:
    wf.link(a, b)
for b in ["HubSpot · Upsert contact", "Email · Buyer confirmation", "Has WhatsApp?", "Hot lead?",
          "Email · Sales desk", "Flatten for sheet"]:
    wf.link("Respond 200", b)
wf.save("01-website-rfq-intake.json", ["gfg", "rfq", "hubspot", "whatsapp"])


# =====================================================================
# 02 — Meta inbox: WhatsApp + Messenger auto-reply, CRM, human hand-off
# =====================================================================
wf = WF("GFG · 02 WhatsApp & Messenger inbox")
webhook(wf, "Meta verify (GET)", "gfg-meta", "GET", [0, 0], "responseNode")
code(wf, "Check verify token", r"""const VERIFY_TOKEN = 'REPLACE_WITH_YOUR_VERIFY_TOKEN';   // same value you enter in Meta App → Webhooks
const q = $input.first().json.query || {};
const ok = q['hub.mode'] === 'subscribe' && q['hub.verify_token'] === VERIFY_TOKEN;
return [{ json: { ok, challenge: ok ? String(q['hub.challenge']) : 'forbidden' } }];""", [220, 0])
wf.node("Return challenge", "n8n-nodes-base.respondToWebhook",
        {"respondWith": "text", "responseBody": "={{ $json.challenge }}",
         "options": {"responseCode": "={{ $json.ok ? 200 : 403 }}"}}, [440, 0], 1.1)
wf.link("Meta verify (GET)", "Check verify token")
wf.link("Check verify token", "Return challenge")

webhook(wf, "Meta events (POST)", "gfg-meta", "POST", [0, 300], "onReceived")
code(wf, "Config", CONFIG_JS, [220, 300])
code(wf, "Parse & detect intent", r"""const cfg = $('Config').first().json.cfg;
const body = $('Meta events (POST)').first().json.body || {};
const out = [];
const intentOf = t => {
  const s = (t || '').toLowerCase();
  if (/(human|agent|call me|talk to|someone|person)/.test(s)) return 'human';
  if (/(price|rate|quote|offer|cfr|fob|cif|\$|usd|eur|দাম)/.test(s)) return 'price';
  if (/(sample)/.test(s)) return 'sample';
  if (/(catalog|catalogue|product|list|spec|size|grade)/.test(s)) return 'catalog';
  if (/(certif|haccp|brc|eu approv|fda|halal|asc|bap)/.test(s)) return 'compliance';
  if (/^(hi|hello|hey|salam|assalam|good (morning|evening))/.test(s)) return 'greeting';
  return 'other';
};
const replies = {
  greeting: `Hello from ${cfg.brand} 👋 We source Bangladeshi seafood and food for importers, with QC on every lot. Reply with:\n1️⃣ CATALOGUE\n2️⃣ PRICE + product, size and port\n3️⃣ SAMPLE\n4️⃣ HUMAN to talk to the export desk`,
  catalog: `Our export product directory (100+ products with HS codes and markets): ${cfg.catalogueUrl}\nTell us the product, size and destination port and we will quote.`,
  price: `Thanks! To quote CFR/FOB we need: product & cut, count grade, pack, quantity (MT or containers) and destination port. A trader will reply with today's price shortly.`,
  sample: `We send frozen samples on dry ice by courier. Please share company name, delivery address and products. A trader will confirm cost and timing.`,
  compliance: `We work with plants approved for your market (EU, SFDA, GACC, US FDA) and certified to HACCP, BRCGS or Halal as required. A trader will send the relevant certificates.`,
  human: `Connecting you to our export desk now. Hours: Sun–Thu 09:00–18:00 Bangladesh time (UTC+6).`,
  other: `Thanks for your message. A member of our export desk will reply shortly. Meanwhile, browse our catalogue: ${cfg.catalogueUrl}`
};
for (const entry of body.entry || []) {
  if (body.object === 'whatsapp_business_account') {
    for (const ch of entry.changes || []) {
      const v = ch.value || {};
      const contact = (v.contacts || [])[0] || {};
      for (const m of v.messages || []) {
        const text = m.text?.body || m.button?.text || m.interactive?.button_reply?.title || m.interactive?.list_reply?.title || `[${m.type}]`;
        const intent = intentOf(text);
        out.push({ json: { channel: 'whatsapp', from: m.from, name: contact.profile?.name || '', text, msgId: m.id, intent, reply: replies[intent], ts: m.timestamp } });
      }
    }
  } else if (body.object === 'page') {
    for (const ev of entry.messaging || []) {
      if (!ev.message || ev.message.is_echo) continue;
      const text = ev.message.text || '[attachment]';
      const intent = intentOf(text);
      out.push({ json: { channel: 'messenger', from: ev.sender.id, name: '', text, msgId: ev.message.mid, intent, reply: replies[intent], ts: ev.timestamp } });
    }
  }
}
return out;   // status callbacks (delivered/read) produce no items and stop here""", [440, 300])

wf.node("Route by channel", "n8n-nodes-base.switch",
        {"rules": {"values": [
            {"conditions": {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                            "conditions": [{"id": str(uuid.uuid4()), "leftValue": "={{ $json.channel }}", "rightValue": "whatsapp",
                                            "operator": {"type": "string", "operation": "equals"}}], "combinator": "and"},
             "renameOutput": True, "outputKey": "WhatsApp"},
            {"conditions": {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "strict"},
                            "conditions": [{"id": str(uuid.uuid4()), "leftValue": "={{ $json.channel }}", "rightValue": "messenger",
                                            "operator": {"type": "string", "operation": "equals"}}], "combinator": "and"},
             "renameOutput": True, "outputKey": "Messenger"}]},
         "options": {}}, [660, 300], 3.2)

wa_reply = wf.node("WhatsApp · Auto-reply", "n8n-nodes-base.httpRequest",
                   {"method": "POST", "url": "=" + GRAPH + "/{{ $('Config').first().json.cfg.waPhoneNumberId }}/messages",
                    "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth",
                    "sendBody": True, "specifyBody": "json",
                    "jsonBody": "={{ JSON.stringify({ messaging_product: 'whatsapp', to: $json.from, type: 'text', text: { preview_url: true, body: $json.reply } }) }}",
                    "options": {}}, [900, 200], 4.2, creds=CRED_WA, on_error="continueRegularOutput")
wf.node("Messenger · Auto-reply", "n8n-nodes-base.httpRequest",
        {"method": "POST", "url": GRAPH + "/me/messages",
         "authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth",
         "sendBody": True, "specifyBody": "json",
         "jsonBody": "={{ JSON.stringify({ recipient: { id: $json.from }, messaging_type: 'RESPONSE', message: { text: $json.reply } }) }}",
         "options": {}}, [900, 400], 4.2, creds=CRED_PAGE, on_error="continueRegularOutput")

code(wf, "Build CRM record", r"""// Needs two custom UNIQUE contact properties in HubSpot: whatsapp_id and messenger_psid (single-line text, "unique value" ticked)
return $input.all().map(({ json: m }) => {
  const idProperty = m.channel === 'whatsapp' ? 'whatsapp_id' : 'messenger_psid';
  const properties = { [idProperty]: m.from, hs_lead_status: 'NEW' };
  if (m.channel === 'whatsapp') { properties.phone = '+' + m.from; if (m.name) properties.firstname = m.name; }
  return { json: { ...m, crm: { inputs: [{ idProperty, id: m.from, properties }] } } };
});""", [1120, 300])
http(wf, "HubSpot · Upsert by channel id", "POST", HUBSPOT + "/crm/v3/objects/contacts/batch/upsert",
     "={{ JSON.stringify($json.crm) }}", [1340, 300], CRED_HUBSPOT, "hubspot")

if_node(wf, "Needs a trader?", "={{ ['human','price','sample','compliance'].includes($('Build CRM record').item.json.intent) }}",
        {"type": "boolean", "operation": "true", "singleValue": True}, None, [1560, 300])
email(wf, "Email · Hand-off to export desk", "={{ $('Config').first().json.cfg.salesEmail }}",
      "=[{{ $('Build CRM record').item.json.channel.toUpperCase() }} · {{ $('Build CRM record').item.json.intent }}] {{ $('Build CRM record').item.json.name || $('Build CRM record').item.json.from }}",
      "=<p><b>{{ $('Build CRM record').item.json.name || 'Unknown' }}</b> ({{ $('Build CRM record').item.json.from }}) wrote on {{ $('Build CRM record').item.json.channel }}:</p>"
      "<blockquote style=\"border-left:3px solid #E0522F;padding-left:10px\">{{ $('Build CRM record').item.json.text }}</blockquote>"
      "<p>Auto-reply sent. Reply from the WhatsApp Business inbox / Meta Business Suite within 15 minutes.</p>",
      [1780, 280])
sheets_append(wf, "Sheets · Chat log", "Chats", [1560, 480])

for a, b in [("Meta events (POST)", "Config"), ("Config", "Parse & detect intent"), ("Parse & detect intent", "Route by channel"),
             ("Parse & detect intent", "Build CRM record"),
             ("Build CRM record", "HubSpot · Upsert by channel id"), ("HubSpot · Upsert by channel id", "Needs a trader?"),
             ("Needs a trader?", "Email · Hand-off to export desk")]:
    wf.link(a, b)
wf.link("Route by channel", "WhatsApp · Auto-reply", 0)
wf.link("Route by channel", "Messenger · Auto-reply", 1)
wf.link("Parse & detect intent", "Sheets · Chat log")
wf.save("02-whatsapp-messenger-inbox.json", ["gfg", "whatsapp", "messenger", "hubspot"])


# =====================================================================
# 03 — Website visitor events → log + hot-visitor alert
# =====================================================================
wf = WF("GFG · 03 Website visitor intent")
wf.node("Events Webhook", "n8n-nodes-base.webhook",
        {"httpMethod": "POST", "path": "gfg-events", "responseMode": "onReceived",
         "options": {"allowedOrigins": "*", "rawBody": True}}, [0, 300], 2, webhookId=str(uuid.uuid4()))
code(wf, "Config", CONFIG_JS, [220, 300])
code(wf, "Parse, filter bots, score", r"""const cfg = $('Config').first().json.cfg;
const item = $('Events Webhook').first();
let b = item.json.body;
// sendBeacon posts text/plain — parse whichever shape arrives
if (typeof b === 'string') { try { b = JSON.parse(b); } catch (e) { b = {}; } }
if ((!b || !b.event) && item.binary?.data) {
  try { b = JSON.parse(Buffer.from(item.binary.data.data, 'base64').toString('utf8')); } catch (e) { b = {}; }
}
if (!b || !b.event) return [];
const h = item.json.headers || {};
const ua = h['user-agent'] || '';
if (/bot|crawl|spider|slurp|headless|lighthouse/i.test(ua)) return [];

const WEIGHTS = { page_view: 1, catalogue_filter: 3, lot_trace: 8, rfq_item_added: 12, load_planner: 15,
                  whatsapp_click: 25, messenger_click: 20, email_click: 15, rfq_started: 25, cta_hero: 5, cta_header: 5 };
const s = $getWorkflowStaticData('global');
s.visitors = s.visitors || {};
const v = s.visitors[b.visitorId] || { score: 0, events: [], alerted: false, first: b.ts };
v.score += WEIGHTS[b.event] ?? 1;
v.events = [...v.events, b.event + (b.data?.product ? ':' + b.data.product : '')].slice(-25);
v.last = b.ts;
// prune visitors idle > 7 days (keeps static data small; GDPR data-minimisation)
const weekAgo = Date.now() - 7 * 864e5;
for (const [id, x] of Object.entries(s.visitors)) if (new Date(x.last).getTime() < weekAgo) delete s.visitors[id];
const alert = v.score >= 50 && !v.alerted;
if (alert) v.alerted = true;
s.visitors[b.visitorId] = v;

return [{ json: {
  Timestamp: b.ts, Event: b.event, Data: JSON.stringify(b.data || {}), VisitorId: b.visitorId, Page: b.page,
  Referrer: b.referrer || '', UTMSource: b.utm?.utm_source || '', UTMCampaign: b.utm?.utm_campaign || '',
  Country: h['cf-ipcountry'] || h['x-vercel-ip-country'] || '', Language: b.lang || '',
  IntentScore: v.score, Alert: alert, Journey: v.events.join(' → ')
} }];""", [440, 300])
sheets_append(wf, "Sheets · Events", "Events", [680, 200])
if_node(wf, "High-intent visitor?", "={{ $json.Alert }}", {"type": "boolean", "operation": "true", "singleValue": True}, None, [680, 420])
email(wf, "Email · Hot visitor alert", "={{ $('Config').first().json.cfg.salesEmail }}",
      "=🔥 High-intent visitor ({{ $json.Country || 'unknown country' }}) — score {{ $json.IntentScore }}",
      "=<p>An anonymous visitor just crossed the intent threshold.</p><p><b>Journey:</b> {{ $json.Journey }}</p>"
      "<p><b>Source:</b> {{ $json.UTMSource || $json.Referrer || 'direct' }} {{ $json.UTMCampaign }}</p>"
      "<p>Tip: if they started an RFQ but did not submit, it will appear in the Events sheet as rfq_started with no RFQ row. "
      "Consider a retargeting audience for this campaign.</p>", [900, 420])
for a, b in [("Events Webhook", "Config"), ("Config", "Parse, filter bots, score"),
             ("Parse, filter bots, score", "Sheets · Events"), ("Parse, filter bots, score", "High-intent visitor?"),
             ("High-intent visitor?", "Email · Hot visitor alert")]:
    wf.link(a, b)
wf.save("03-website-visitor-intent.json", ["gfg", "analytics"])


# =====================================================================
# 04 — Hourly SLA watchdog: RFQs with no quote after 4 h
# =====================================================================
wf = WF("GFG · 04 Quote SLA watchdog")
wf.node("Every hour", "n8n-nodes-base.scheduleTrigger",
        {"rule": {"interval": [{"field": "hours", "hoursInterval": 1}]}}, [0, 300], 1.2)
code(wf, "Config", CONFIG_JS, [220, 300])
http(wf, "HubSpot · Stale RFQ deals", "POST", HUBSPOT + "/crm/v3/objects/deals/search",
     "={{ JSON.stringify({ filterGroups: [ { filters: ["
     " { propertyName: 'dealstage', operator: 'EQ', value: $('Config').first().json.cfg.hubspotStage },"
     " { propertyName: 'pipeline', operator: 'EQ', value: $('Config').first().json.cfg.hubspotPipeline },"
     " { propertyName: 'createdate', operator: 'LT', value: String(Date.now() - 4*3600*1000) },"
     " { propertyName: 'createdate', operator: 'GT', value: String(Date.now() - 7*24*3600*1000) } ] } ],"
     " properties: ['dealname','amount','createdate','hubspot_owner_id'], sorts: [ { propertyName: 'createdate', direction: 'ASCENDING' } ], limit: 50 }) }}",
     [440, 300], CRED_HUBSPOT, "hubspot")
code(wf, "Any breaches?", r"""const r = $input.first().json.results || [];
if (!r.length) return [];
const rows = r.map(d => {
  const hrs = Math.round((Date.now() - new Date(d.properties.createdate).getTime()) / 36e5);
  return `<tr><td>${d.properties.dealname}</td><td style="text-align:right">${hrs} h</td><td style="text-align:right">$${Number(d.properties.amount || 0).toLocaleString()}</td></tr>`;
}).join('');
return [{ json: { count: r.length, html: `<p>${r.length} quote request(s) are past the 4-hour first-response target and still in the first stage.</p><table cellpadding="6" style="border-collapse:collapse;font:14px Arial">${rows}</table><p>Move the deal stage once a price offer is sent to clear it from this list.</p>` } }];""",
     [660, 300])
email(wf, "Email · SLA breach to manager", "={{ $('Config').first().json.cfg.managerEmail }}",
      "=⏱ {{ $json.count }} RFQ(s) waiting > 4 h for a price offer", "={{ $json.html }}", [880, 300])
for a, b in [("Every hour", "Config"), ("Config", "HubSpot · Stale RFQ deals"),
             ("HubSpot · Stale RFQ deals", "Any breaches?"), ("Any breaches?", "Email · SLA breach to manager")]:
    wf.link(a, b)
wf.save("04-quote-sla-watchdog.json", ["gfg", "hubspot", "sla"])


# =====================================================================
# 05 — Supplier (exporter) application → score → WBF_Exporter_List + HubSpot
# =====================================================================
wf = WF("GFG · 05 Supplier onboarding")
webhook(wf, "Supplier Webhook", "gfg-supplier", "POST", [0, 300], "responseNode")
code(wf, "Config", CONFIG_JS.replace("REPLACE_GOOGLE_SHEET_ID", "1JyiuxvECPbww8jFOmU0Bf-TR6JToa4XhYi_iQhXa0eA"), [220, 300])
code(wf, "Validate & rate supplier", r"""const b = $('Supplier Webhook').first().json.body || {};
const clean = s => String(s ?? '').trim().slice(0, 1500);
const email = clean(b.email).toLowerCase();
if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) throw new Error('Invalid email');
if (b.website) throw new Error('Honeypot');
const approvals = Array.isArray(b.approvals) ? b.approvals : [];
const cats = Array.isArray(b.categories) ? b.categories : [];
const licence = clean(b.licence);
// Same tiers as the GFG exporter list: A = official approval list / leadership, B = credible to confirm, C = verify first
let score = 0;
if (licence) score += 25;                                             // DoF approval / export licence number given
score += ['EU approved list','SFDA (Saudi)','GACC (China)','US FDA'].filter(a => approvals.includes(a)).length * 12;
score += ['HACCP','BRCGS','ISO 22000','FSSC 22000','GLOBALG.A.P.','BAP','ASC','Organic','BSTI','Halal'].filter(a => approvals.includes(a)).length * 4;
const FISH = ['shrimp','shell','marine','fresh','live','dried'];
const isFish = cats.length === 0 || cats.some(c => FISH.includes(c));   // fish/seafood → Exporter List, food & crops → Food Exporter List
score += ({ '<20': 0, '20-100': 8, '100-500': 15, '500+': 20 })[b.capacity] ?? 0;
if (/^https?:\/\//.test(clean(b.website_url))) score += 5;
const priority = score >= 60 ? 'A' : score >= 35 ? 'B' : 'C';
const ref = 'SUP-' + new Date().toISOString().slice(2, 10).replace(/-/g, '') + '-' + Math.random().toString(36).slice(2, 6).toUpperCase();
return [{ json: { ref, score, priority, isFish, email, company: clean(b.company), name: clean(b.name), designation: clean(b.designation),
  phone: clean(b.phone), district: clean(b.district), licence, capacity: clean(b.capacity), approvals, categories: cats,
  website: clean(b.website_url), notes: clean(b.notes), submittedAt: b.submittedAt || new Date().toISOString() } }];""", [440, 300])
wf.node("Respond 200", "n8n-nodes-base.respondToWebhook",
        {"respondWith": "json", "responseBody": "={{ JSON.stringify({ ok: true, ref: $json.ref }) }}", "options": {"responseCode": 200}}, [660, 300], 1.1)
code(wf, "Map to Exporter List columns", r"""const s = $('Validate & rate supplier').first().json;
// Keys match the header row of WBF_Exporter_List → 'Exporter List' exactly
return [{ json: {
  'Bangladesh Fish exporter Company': s.company,
  'Location': s.district, 'Region': s.district,
  'DoF Approval No.': s.licence,
  'Products': s.categories.join(', ') + (s.notes ? ' | ' + s.notes : ''),
  'Evidence / Source': 'Website application ' + s.ref + ' · approvals: ' + (s.approvals.join(', ') || 'none stated'),
  'Website': s.website, 'Priority': s.priority, 'Status': 'Applied via website',
  'Contact Name of the Bangladeshi fish exporter ': s.name + (s.designation ? ' (' + s.designation + ')' : ''),
  'Phone / WhatsApp': s.phone, 'Email': s.email, 'NCNDA Signed': 'No',
  'Notes': 'Capacity ' + s.capacity + ' MT/month · score ' + s.score + (s.isFish ? ' · verify licence with DoF FIQC before any deal' : ' · verify ERC, phytosanitary registration and factory certificates before any deal')
} }];""", [900, 160])
wf.node("Sheets · Add to Exporter List", "n8n-nodes-base.googleSheets",
        {"operation": "append",
         "documentId": {"__rl": True, "mode": "id", "value": "={{ $('Config').first().json.cfg.sheetId }}"},
         "sheetName": {"__rl": True, "mode": "name", "value": "={{ $('Validate & rate supplier').first().json.isFish ? 'Exporter List' : 'Food Exporter List' }}"},
         "columns": {"mappingMode": "autoMapInputData", "value": {}, "matchingColumns": [], "schema": []}, "options": {}},
        [1120, 160], 4.5, creds=CRED_SHEETS, on_error="continueRegularOutput")
http(wf, "HubSpot · Create supplier company", "POST", HUBSPOT + "/crm/v3/objects/companies",
     "={{ JSON.stringify({ properties: { name: $('Validate & rate supplier').first().json.company, phone: $('Validate & rate supplier').first().json.phone,"
     " city: $('Validate & rate supplier').first().json.district, country: 'Bangladesh', domain: ($('Validate & rate supplier').first().json.website || '').replace(/^https?:\\/\\//,'').replace(/\\/.*$/,''),"
     " type: 'VENDOR', description: 'GFG supplier application ' + $('Validate & rate supplier').first().json.ref + ' · Priority ' + $('Validate & rate supplier').first().json.priority + ' · ' + $('Validate & rate supplier').first().json.categories.join(', ') } }) }}",
     [900, 320], CRED_HUBSPOT, "hubspot")
email(wf, "Email · Acknowledge supplier", "={{ $('Validate & rate supplier').first().json.email }}",
      "=Your GFG supplier application {{ $('Validate & rate supplier').first().json.ref }}",
      "=<div style=\"font-family:Arial,sans-serif;max-width:560px;color:#0A2540\"><p>Dear {{ $('Validate & rate supplier').first().json.name }},</p>"
      "<p>Thank you for applying to join the GoodBuy Foods Global supplier network. Your reference is <b>{{ $('Validate & rate supplier').first().json.ref }}</b>.</p>"
      "<p>Next steps:</p><ol><li>We call you within 3 working days to confirm your details.</li><li>Please have ready: your Export Registration Certificate (ERC); for fish, your DoF FIQC licence and plant approval number; for fresh produce, your phytosanitary registration; and any certificates or market listings (EU, SFDA, GACC, FDA, HACCP, BRCGS, FSSC 22000, Halal).</li>"
      "<li>We sign an NCNDA and our supplier code of conduct, then introduce verified buyers. Joining is free and we take no commission from suppliers.</li></ol><p>GoodBuy Foods Global</p></div>", [900, 480])
email(wf, "Email · Notify sourcing team", "={{ $('Config').first().json.cfg.salesEmail }}",
      "=[Supplier {{ $('Validate & rate supplier').first().json.priority }}] {{ $('Validate & rate supplier').first().json.company }} · {{ $('Validate & rate supplier').first().json.district }}",
      "=<pre style=\"font:13px/1.5 monospace\">{{ JSON.stringify($('Validate & rate supplier').first().json, null, 2) }}</pre><p>Before any deal: verify the DoF licence with FIQC and the plant's listing for the buyer's market.</p>", [900, 640])
for a, b in [("Supplier Webhook", "Config"), ("Config", "Validate & rate supplier"), ("Validate & rate supplier", "Respond 200"),
             ("Map to Exporter List columns", "Sheets · Add to Exporter List")]:
    wf.link(a, b)
for b in ["Map to Exporter List columns", "HubSpot · Create supplier company", "Email · Acknowledge supplier", "Email · Notify sourcing team"]:
    wf.link("Respond 200", b)
wf.save("05-supplier-onboarding.json", ["gfg", "suppliers", "hubspot", "sheets"])
