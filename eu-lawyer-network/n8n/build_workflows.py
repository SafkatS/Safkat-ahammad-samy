#!/usr/bin/env python3
"""Generates importable n8n workflows for the European Manpower Lawyer Network.

Run:  python3 eu-lawyer-network/n8n/build_workflows.py
No secrets live in these files: credentials are attached in n8n, the HMAC
secret is read from the env var LAWNET_HMAC_SECRET.

n8n instance env needed:
  NODE_FUNCTION_ALLOW_BUILTIN=crypto      (signed approve/reject links)
  N8N_BLOCK_ENV_ACCESS_IN_NODE=false      (read LAWNET_HMAC_SECRET)
  LAWNET_HMAC_SECRET=<long random string>
"""
import json, os, re, uuid

SQL_LOG = []  # (workflow, node, sql) — dumped to sql_from_workflows.sql for testing

OUT = os.path.dirname(os.path.abspath(__file__))
GRAPH = "https://graph.facebook.com/v21.0"
HUBSPOT = "https://api.hubapi.com"

CRED_PG = {"postgres": {"id": "REPLACE_ME", "name": "Supabase Postgres (lawnet)"}}
CRED_HUBSPOT = {"hubspotAppToken": {"id": "REPLACE_ME", "name": "HubSpot Private App"}}
CRED_WA = {"httpHeaderAuth": {"id": "REPLACE_ME", "name": "WhatsApp Cloud API (Bearer)"}}
CRED_AGENT = {"httpHeaderAuth": {"id": "REPLACE_ME", "name": "LangGraph agent → n8n (X-Api-Key)"}}
CRED_SMTP = {"smtp": {"id": "REPLACE_ME", "name": "SMTP legal desk"}}

CONFIG_JS = r"""// ⚙ Edit once after import. Read by every node via $('Config').first().json.cfg
return [{ json: {
  ...$input.first().json,
  cfg: {
    brand: 'Global Node Legal Network',
    n8nBase: 'https://n8n.example.com/webhook',          // your n8n production webhook base
    complianceEmail: 'compliance@example.com',          // EU Legal Compliance Officer
    opsEmail: 'ops@example.com',
    fromEmail: 'Global Node Legal <legal@example.com>',
    waPhoneNumberId: 'REPLACE_WA_PHONE_NUMBER_ID',
    privacyUrl: 'https://example.com/privacy',
    consentVersion: 'lawnet-consent-2026-11',
    lawyerSlaHours: 24,          // lawyer must accept a referral within
    reviewSlaHours: 4,           // SOP §4: nothing stuck in review > 4h
    priorityCountries: ['RO','BG','MK','BA','LT','LV','SI','SK']
  }
}}];"""

SIGN_JS = r"""const crypto = require('crypto');
const secret = $env.LAWNET_HMAC_SECRET;
if (!secret) throw new Error('LAWNET_HMAC_SECRET not set');
const sign = (id, d) => crypto.createHmac('sha256', secret).update(id + '|' + d).digest('hex').slice(0, 32);"""


class WF:
    def __init__(self, name):
        self.name, self.nodes, self.conn = name, [], {}

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

    def chain(self, *names):
        for a, b in zip(names, names[1:]):
            self.link(a, b)

    def save(self, fname, tags):
        data = {"name": self.name, "nodes": self.nodes, "connections": self.conn,
                "active": False, "settings": {"executionOrder": "v1", "saveManualExecutions": True},
                "pinData": {}, "meta": {"templateCredsSetupCompleted": False},
                "tags": [{"name": t} for t in tags]}
        with open(os.path.join(OUT, fname), "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("wrote", fname, len(self.nodes), "nodes")


# ---------- node builders ----------
def webhook(wf, name, path, method, pos, creds=None):
    p = {"httpMethod": method, "path": path, "responseMode": "responseNode", "options": {}}
    if method == "POST":
        p["options"]["allowedOrigins"] = "*"
    if creds:
        p["authentication"] = "headerAuth"
    return wf.node(name, "n8n-nodes-base.webhook", p, pos, 2, creds=creds, webhookId=str(uuid.uuid4()))


def config(wf, pos):
    return code(wf, "Config", CONFIG_JS, pos)


def code(wf, name, js, pos):
    return wf.node(name, "n8n-nodes-base.code", {"jsCode": js}, pos, 2)


def pg(wf, name, sql, params_expr, pos, always=False):
    """params_expr: None, an n8n array expression, or a dict {placeholder: js_expr} used with {placeholder} in sql."""
    if isinstance(params_expr, dict):
        keys = list(params_expr)
        sql = re.sub(r"\{(\w+)\}", lambda m: "$%d" % (keys.index(m.group(1)) + 1), sql)
        params_expr = "={{ [" + ", ".join(params_expr[k] for k in keys) + "] }}"
    SQL_LOG.append((wf.name, name, sql))
    p = {"operation": "executeQuery", "query": sql, "options": {}}
    if params_expr:
        p["options"]["queryReplacement"] = params_expr
    extra = {"alwaysOutputData": True} if always else {}
    return wf.node(name, "n8n-nodes-base.postgres", p, pos, 2.5, creds=CRED_PG, **extra)


def http(wf, name, method, url, body_expr, pos, creds, hubspot=False):
    p = {"method": method, "url": url, "options": {"timeout": 15000}}
    if body_expr:
        p.update({"sendBody": True, "specifyBody": "json", "jsonBody": body_expr})
    if hubspot:
        p.update({"authentication": "predefinedCredentialType", "nodeCredentialType": "hubspotAppToken"})
    else:
        p.update({"authentication": "genericCredentialType", "genericAuthType": "httpHeaderAuth"})
    return wf.node(name, "n8n-nodes-base.httpRequest", p, pos, 4.2, creds=creds,
                   on_error="continueRegularOutput", retryOnFail=True, maxTries=3, waitBetweenTries=2000)


def email(wf, name, to, subject, html, pos):
    return wf.node(name, "n8n-nodes-base.emailSend",
                   {"fromEmail": "={{ $('Config').first().json.cfg.fromEmail }}", "toEmail": to,
                    "subject": subject, "emailFormat": "html", "html": html,
                    "options": {"appendAttribution": False}},
                   pos, 2.1, creds=CRED_SMTP, on_error="continueRegularOutput")


def if_node(wf, name, left, op, right, pos):
    cond = {"id": str(uuid.uuid4()), "leftValue": left, "operator": op}
    if right is not None:
        cond["rightValue"] = right
    return wf.node(name, "n8n-nodes-base.if",
                   {"conditions": {"options": {"caseSensitive": True, "leftValue": "", "typeValidation": "loose"},
                                   "conditions": [cond], "combinator": "and"}, "options": {}}, pos, 2)


def respond(wf, name, body_expr, pos, kind="json", code_=200):
    p = {"respondWith": kind, "options": {"responseCode": code_}}
    if kind == "json":
        p["responseBody"] = body_expr
    else:
        p["responseBody"] = body_expr
        p["options"]["responseHeaders"] = {"entries": [{"name": "Content-Type", "value": "text/html; charset=utf-8"}]}
    return wf.node(name, "n8n-nodes-base.respondToWebhook", p, pos, 1.1)


def wa_template(to_expr, template, params_exprs, lang="en"):
    params = ", ".join("{ type: 'text', text: String(%s) }" % p for p in params_exprs)
    return ("={{ JSON.stringify({ messaging_product: 'whatsapp', to: %s, type: 'template', "
            "template: { name: '%s', language: { code: '%s' }, components: [ { type: 'body', parameters: [ %s ] } ] } }) }}"
            % (to_expr, template, lang, params))


NUM_GT = {"type": "number", "operation": "gt"}
NOT_EMPTY = {"type": "string", "operation": "notEmpty", "singleValue": True}
TRUE = {"type": "boolean", "operation": "true", "singleValue": True}

# =====================================================================
# 01 — Lawyer self-registration (web form) → Postgres + HubSpot + review alert
# =====================================================================
wf = WF("LAWNET · 01 Lawyer self-registration")
webhook(wf, "Signup Webhook", "lawnet-lawyer-signup", "POST", [0, 300])
config(wf, [220, 300])
code(wf, "Validate & Normalise", r"""const b = $('Signup Webhook').first().json.body || {};
const h = $('Signup Webhook').first().json.headers || {};
const cfg = $('Config').first().json.cfg;
const clean = (s, n = 300) => String(s ?? '').trim().slice(0, n);
const arr = v => (Array.isArray(v) ? v : String(v ?? '').split(',')).map(x => clean(x, 40)).filter(Boolean);
if (b.website_hp) throw new Error('Honeypot');
const email = clean(b.email).toLowerCase();
if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) throw new Error('Invalid email');
const country = clean(b.country, 2).toUpperCase();
if (!/^[A-Z]{2}$/.test(country)) throw new Error('Invalid country');
const e164 = p => { const d = clean(p, 25).replace(/[^\d+]/g, ''); if (!d) return null;
  const v = d.startsWith('+') ? d : '+' + d; return /^\+[1-9]\d{6,14}$/.test(v) ? v : null; };
if (b.consent_directory !== true && b.consent_directory !== 'on' && b.consent_directory !== 'true')
  throw new Error('Directory consent is required');
const yes = v => v === true || v === 'on' || v === 'true';
return [{ json: {
  full_name: clean(b.full_name, 120), title: clean(b.title, 60), email,
  phone: e164(b.phone), whatsapp: e164(b.whatsapp || b.phone),
  country, city: clean(b.city, 80), firm: clean(b.firm, 160), firm_website: clean(b.firm_website, 200),
  bar_name: clean(b.bar_name, 160), bar_number: clean(b.bar_number, 60), admitted_year: parseInt(b.admitted_year) || null,
  website: clean(b.website, 200), linkedin: clean(b.linkedin, 200), bio: clean(b.bio, 2000),
  fee_permit_eur: parseFloat(b.fee_permit_eur) || null, hourly_eur: parseFloat(b.hourly_eur) || null,
  capacity: parseInt(b.capacity) || 10,
  countries_served: JSON.stringify([...new Set([country, ...arr(b.countries_served).map(c => c.toUpperCase())])]),
  practice: JSON.stringify(arr(b.practice_areas)), routes: JSON.stringify(arr(b.routes)),
  languages: JSON.stringify(arr(b.languages).map(l => l.toLowerCase().slice(0, 2))),
  consents: JSON.stringify([
    { purpose: 'directory_listing', granted: true },
    { purpose: 'referrals', granted: yes(b.consent_referrals) },
    { purpose: 'marketing', granted: yes(b.consent_marketing) },
    { purpose: 'b2b_portal_visibility', granted: yes(b.consent_b2b) }]),
  marketing: yes(b.consent_marketing),
  ip: String(h['x-forwarded-for'] || '').split(',')[0].trim() || null,
  ua: clean(h['user-agent'], 300), consentVersion: cfg.consentVersion,
  priority: cfg.priorityCountries.includes(country)
}}];""", [440, 300])
pg(wf, "Claim Register Record", r"""update lawnet.lawyers set email = {email}
where country_iso2 = {country} and bar_number = nullif({bar_number},'') and (email is null or lower(email) = {email})
returning id;""", {"email": "$json.email", "country": "$json.country", "bar_number": "$json.bar_number"}, [550, 300], always=True)
pg(wf, "Upsert Lawyer", r"""with f as (
  insert into lawnet.firms(name, country_iso2, city, website, source)
  select {firm}, {country}, nullif({city},''), nullif({firm_website},''), 'self_registration' where nullif({firm},'') is not null
  on conflict (country_iso2, name) do update set website = coalesce(excluded.website, lawnet.firms.website)
  returning id),
ba as (select id from lawnet.bar_authorities where country_iso2 = {country}
       order by similarity(name_en || ' ' || name_local, {bar_name}::text) desc limit 1),
l as (
  insert into lawnet.lawyers(full_name, title, email, phone_e164, whatsapp_e164, country_iso2, city, firm_id,
     bar_authority_id, bar_number, admitted_year, website, linkedin_url, bio, fixed_fee_permit_eur, hourly_rate_eur,
     capacity_per_month, source, lawful_basis, marketing_opt_in, verification)
  values ({full_name}, nullif({title},''), {email}, nullif({phone},''), nullif({whatsapp},''), {country}, nullif({city},''),
     (select id from f), (select id from ba), nullif({bar_number},''), nullif({admitted_year},'')::smallint, nullif({website},''),
     nullif({linkedin},''), nullif({bio},''), nullif({fee},'')::numeric, nullif({hourly},'')::numeric, {capacity}::smallint,
     'self_registration', 'consent', {marketing}::boolean, 'pending_review')
  on conflict (lower(email)) where email is not null do update set
     full_name = excluded.full_name, title = excluded.title, phone_e164 = excluded.phone_e164, whatsapp_e164 = excluded.whatsapp_e164,
     city = excluded.city, firm_id = coalesce(excluded.firm_id, lawnet.lawyers.firm_id), bio = excluded.bio,
     bar_authority_id = coalesce(lawnet.lawyers.bar_authority_id, excluded.bar_authority_id),
     bar_number = coalesce(excluded.bar_number, lawnet.lawyers.bar_number), admitted_year = excluded.admitted_year,
     website = excluded.website, linkedin_url = excluded.linkedin_url,
     fixed_fee_permit_eur = excluded.fixed_fee_permit_eur, hourly_rate_eur = excluded.hourly_rate_eur,
     capacity_per_month = excluded.capacity_per_month, marketing_opt_in = excluded.marketing_opt_in,
     source = 'self_registration', lawful_basis = 'consent', is_active = true,
     verification = case when lawnet.lawyers.verification = 'verified' then 'verified'::lawnet.verification_status else 'pending_review' end
  returning id, public_ref, verification, bar_authority_id),
c  as (insert into lawnet.lawyer_countries select (select id from l), x, x = {country} from jsonb_array_elements_text({countries}::jsonb) x
       where exists (select 1 from lawnet.countries where iso2 = x) on conflict do nothing),
p  as (insert into lawnet.lawyer_practice_areas(lawyer_id, practice_code) select (select id from l), x from jsonb_array_elements_text({practice}::jsonb) x
       where exists (select 1 from lawnet.practice_areas where code = x) on conflict do nothing),
r  as (insert into lawnet.lawyer_routes(lawyer_id, route_code) select (select id from l), x from jsonb_array_elements_text({routes}::jsonb) x
       where exists (select 1 from lawnet.work_routes where code = x) on conflict do nothing),
g  as (insert into lawnet.lawyer_languages(lawyer_id, lang) select (select id from l), x from jsonb_array_elements_text({languages}::jsonb) x
       where length(x) = 2 on conflict do nothing),
k  as (insert into lawnet.consents(lawyer_id, purpose, granted, text_version, ip, user_agent)
       select (select id from l), e->>'purpose', (e->>'granted')::boolean, {consent_version}, nullif({ip},'')::inet, {ua}
       from jsonb_array_elements({consents}::jsonb) e)
select l.id, l.public_ref, l.verification, bar.register_search_url, bar.website as bar_website, bar.name_en as bar
from l left join lawnet.bar_authorities bar on bar.id = l.bar_authority_id;""",
   {k: "$('Validate & Normalise').first().json." + v for k, v in [
     ("full_name", "full_name"), ("title", "title"), ("email", "email"), ("phone", "phone ?? ''"), ("whatsapp", "whatsapp ?? ''"),
     ("country", "country"), ("city", "city"), ("firm", "firm"), ("firm_website", "firm_website"), ("bar_name", "bar_name"),
     ("bar_number", "bar_number"), ("admitted_year", "admitted_year ? String($('Validate & Normalise').first().json.admitted_year) : ''"),
     ("website", "website"), ("linkedin", "linkedin"), ("bio", "bio"),
     ("fee", "fee_permit_eur ? String($('Validate & Normalise').first().json.fee_permit_eur) : ''"),
     ("hourly", "hourly_eur ? String($('Validate & Normalise').first().json.hourly_eur) : ''"),
     ("capacity", "capacity"), ("marketing", "marketing"), ("countries", "countries_served"), ("practice", "practice"),
     ("routes", "routes"), ("languages", "languages"), ("consent_version", "consentVersion"), ("ip", "ip ?? ''"),
     ("ua", "ua"), ("consents", "consents")]}, [660, 300])
code(wf, "Sign Review Links", SIGN_JS + r"""
const row = $input.first().json, cfg = $('Config').first().json.cfg, v = $('Validate & Normalise').first().json;
const link = d => `${cfg.n8nBase}/lawnet-verify?id=${row.id}&d=${d}&t=${sign(row.id, d)}`;
return [{ json: { ...v, ...row, approveUrl: link('verified'), rejectUrl: link('rejected') } }];""", [880, 300])
http(wf, "HubSpot Upsert Contact", "POST", f"{HUBSPOT}/crm/v3/objects/contacts/batch/upsert",
     "={{ JSON.stringify({ inputs: [ { idProperty: 'email', id: $json.email, properties: { email: $json.email, "
     "firstname: $json.full_name.split(' ')[0], lastname: $json.full_name.split(' ').slice(1).join(' ') || '-', "
     "phone: $json.phone || '', company: $json.firm || '', country: $json.country, city: $json.city, jobtitle: 'Lawyer', "
     "lifecyclestage: 'other', hs_lead_status: 'NEW' } } ] }) }}",
     [1100, 160], CRED_HUBSPOT, hubspot=True)
email(wf, "Alert Compliance Officer",
      "={{ $('Config').first().json.cfg.complianceEmail }}",
      "={{ ($json.priority ? '🔴 PRIORITY ' : '') + 'Verify lawyer ' + $json.public_ref + ' · ' + $json.country + ' · ' + $json.full_name }}",
      "={{ `<h3>New lawyer awaiting verification (SLA ${$('Config').first().json.cfg.reviewSlaHours}h)</h3>"
      "<p><b>${$json.full_name}</b> — ${$json.title || ''} ${$json.firm ? '· ' + $json.firm : ''}<br>${$json.city}, ${$json.country}</p>"
      "<p>Bar: ${$json.bar || $json.bar_name || '?'} · No. <b>${$json.bar_number || 'not given'}</b><br>"
      "Check register: <a href=\"${$json.register_search_url || $json.bar_website || '#'}\">${$json.register_search_url || $json.bar_website || 'no URL on file'}</a></p>"
      "<p>Routes: ${JSON.parse($json.routes).join(', ') || '-'}<br>Languages: ${JSON.parse($json.languages).join(', ')}</p>"
      "<p><a href=\"${$json.approveUrl}\">✅ Approve (verified)</a> &nbsp; | &nbsp; <a href=\"${$json.rejectUrl}\">❌ Reject</a></p>` }}",
      [1100, 300])
email(wf, "Confirm to Lawyer", "={{ $json.email }}",
      "={{ 'Your listing request – ' + $('Config').first().json.cfg.brand }}",
      "={{ `<p>Dear ${$json.full_name},</p><p>Thank you for joining the ${$('Config').first().json.cfg.brand}. "
      "Your reference is <b>${$json.public_ref}</b>. Our compliance team will check your bar admission"
      " (normally within one working day) before referrals start.</p>"
      "<p>You can withdraw consent or ask for erasure at any time by replying to this e-mail. "
      "Privacy notice: ${$('Config').first().json.cfg.privacyUrl}</p>` }}",
      [1100, 440])
respond(wf, "Respond OK", "={{ JSON.stringify({ ok: true, ref: $('Sign Review Links').first().json.public_ref }) }}", [1320, 300])
wf.chain("Signup Webhook", "Config", "Validate & Normalise", "Claim Register Record", "Upsert Lawyer", "Sign Review Links")
for n in ("HubSpot Upsert Contact", "Alert Compliance Officer", "Confirm to Lawyer"):
    wf.link("Sign Review Links", n)
wf.link("Confirm to Lawyer", "Respond OK")
wf.save("01-lawyer-self-registration.json", ["lawnet", "intake"])

# =====================================================================
# 02 — HITL verification decision (signed link from e-mail)
# =====================================================================
wf = WF("LAWNET · 02 Verification decision (HITL)")
webhook(wf, "Verify Link", "lawnet-verify", "GET", [0, 300])
config(wf, [220, 300])
code(wf, "Check Signature", SIGN_JS + r"""
const q = $('Verify Link').first().json.query || {};
if (!['verified','rejected','suspended'].includes(q.d)) throw new Error('bad decision');
if (!/^[0-9a-f-]{36}$/.test(q.id || '')) throw new Error('bad id');
const ok = crypto.timingSafeEqual(Buffer.from(sign(q.id, q.d)), Buffer.from(String(q.t || '').padEnd(32).slice(0, 32)));
if (!ok) throw new Error('invalid signature');
return [{ json: { id: q.id, decision: q.d, by: q.by || $('Config').first().json.cfg.complianceEmail } }];""", [440, 300])
pg(wf, "Apply Decision", r"""with u as (
  update lawnet.lawyers set verification = $2::lawnet.verification_status, verified_by = $3,
         verified_at = case when $2 = 'verified' then now() else verified_at end
  where id = $1::uuid returning id, public_ref, full_name, email, whatsapp_e164, hubspot_contact_id, verification)
, v as (insert into lawnet.verifications(lawyer_id, method, result, checked_by)
        select id, 'bar_register_lookup', verification, $3 from u)
select * from u;""", "={{ [$json.id, $json.decision, $json.by] }}", [660, 300])
if_node(wf, "Verified?", "={{ $json.verification }}", {"type": "string", "operation": "equals"}, "verified", [880, 300])
http(wf, "WhatsApp Welcome", "POST",
     "={{ 'https://graph.facebook.com/v21.0/' + $('Config').first().json.cfg.waPhoneNumberId + '/messages' }}",
     wa_template("$json.whatsapp_e164.replace('+','')", "lawnet_lawyer_verified", ["$json.full_name", "$json.public_ref"]),
     [1100, 200], CRED_WA)
email(wf, "Email Welcome", "={{ $json.email }}", "You are verified – referrals are now open",
      "={{ `<p>Dear ${$json.full_name},</p><p>Your bar admission is confirmed (ref <b>${$json.public_ref}</b>). "
      "You will now receive anonymised candidate/employer cases that match your countries, routes and languages. "
      "Please accept or decline each case within ${$('Config').first().json.cfg.lawyerSlaHours} hours.</p>` }}",
      [1100, 360])
respond(wf, "Respond Page", "={{ `<html><body style=\"font-family:system-ui;padding:40px\"><h2>Saved</h2>"
        "<p>${$('Apply Decision').first().json.public_ref} → <b>${$('Apply Decision').first().json.verification}</b></p></body></html>` }}",
        [1320, 300], kind="text")
wf.chain("Verify Link", "Config", "Check Signature", "Apply Decision", "Verified?")
wf.link("Verified?", "WhatsApp Welcome", 0)
wf.link("Verified?", "Email Welcome", 0)
wf.link("Verified?", "Respond Page", 1)
wf.link("Email Welcome", "Respond Page")
wf.save("02-verification-decision.json", ["lawnet", "hitl"])

# =====================================================================
# 03 — Candidate/employer case → best lawyer (called by EU Compliance Agent)
# =====================================================================
wf = WF("LAWNET · 03 Case → lawyer matcher")
webhook(wf, "Case Webhook", "lawnet-match", "POST", [0, 300], creds=CRED_AGENT)
config(wf, [220, 300])
code(wf, "Validate Case", r"""const b = $('Case Webhook').first().json.body || {};
const ref = String(b.candidate_ref || '').toUpperCase();
if (!/^CAND-[A-Z0-9]{5,}$/.test(ref)) throw new Error('candidate_ref must be anonymised CAND-XXXXX (no PII)');
const country = String(b.country || '').toUpperCase().slice(0, 2);
return [{ json: {
  candidate_ref: ref, country, route: String(b.route || '') || null,
  lang: String(b.lang || 'en').toLowerCase().slice(0, 2), employer_ref: b.employer_ref || null,
  trade: String(b.trade || '').slice(0, 80), blocks: (b.blocks || []).slice(0, 10).map(String),
  limit: Math.min(parseInt(b.limit) || 1, 3)
}}];""", [440, 300])
pg(wf, "Match Lawyers", "select * from lawnet.match_lawyers($1, nullif($2,''), $3, $4::int);",
   "={{ [$json.country, $json.route ?? '', $json.lang, $json.limit] }}", [660, 300], always=True)
if_node(wf, "Found?", "={{ $json.lawyer_id }}", NOT_EMPTY, None, [880, 300])
pg(wf, "Create Engagement", r"""insert into lawnet.engagements(candidate_ref, lawyer_id, route_code, country_iso2, employer_ref, status, match_score, sla_due_at)
values ($1, $2::uuid, nullif($3,''), $4, nullif($5,''), 'lawyer_notified', $6::numeric, now() + ($7 || ' hours')::interval)
returning id as engagement_id, lawyer_id, sla_due_at,
  (select email from lawnet.lawyers where id = $2::uuid) as lawyer_email,
  (select whatsapp_e164 from lawnet.lawyers where id = $2::uuid) as lawyer_wa,
  (select full_name from lawnet.lawyers where id = $2::uuid) as lawyer_name;""",
   "={{ [$('Validate Case').first().json.candidate_ref, $json.lawyer_id, $('Validate Case').first().json.route ?? '', "
   "$('Validate Case').first().json.country, $('Validate Case').first().json.employer_ref ?? '', $json.score, "
   "String($('Config').first().json.cfg.lawyerSlaHours)] }}", [1100, 200])
email(wf, "Brief Lawyer", "={{ $json.lawyer_email }}",
      "={{ 'New case ' + $('Validate Case').first().json.candidate_ref + ' · ' + ($('Validate Case').first().json.route || $('Validate Case').first().json.country) }}",
      "={{ `<p>Dear ${$json.lawyer_name},</p><p>An anonymised case matches your profile:</p><ul>"
      "<li>Case: <b>${$('Validate Case').first().json.candidate_ref}</b></li>"
      "<li>Country / route: ${$('Validate Case').first().json.country} · ${$('Validate Case').first().json.route || 'to be advised'}</li>"
      "<li>Trade: ${$('Validate Case').first().json.trade || '-'}</li>"
      "<li>Flagged blocks: ${$('Validate Case').first().json.blocks.join(', ') || 'none'}</li></ul>"
      "<p>Please reply ACCEPT or DECLINE (with fee quote) before ${new Date($json.sla_due_at).toUTCString()}.</p>` }}",
      [1320, 120])
http(wf, "WhatsApp Lawyer", "POST",
     "={{ 'https://graph.facebook.com/v21.0/' + $('Config').first().json.cfg.waPhoneNumberId + '/messages' }}",
     wa_template("$json.lawyer_wa.replace('+','')", "lawnet_new_case",
                 ["$json.lawyer_name", "$('Validate Case').first().json.candidate_ref", "$('Validate Case').first().json.country"]),
     [1320, 280], CRED_WA)
respond(wf, "Respond Matched", "={{ JSON.stringify({ ok: true, engagement_id: $('Create Engagement').first().json.engagement_id, "
        "lawyer_ref: $('Match Lawyers').first().json.public_ref, sla_due_at: $('Create Engagement').first().json.sla_due_at }) }}",
        [1540, 200])
email(wf, "Coverage Gap Alert", "={{ $('Config').first().json.cfg.complianceEmail }}",
      "={{ '⚠ No verified lawyer for ' + $('Validate Case').first().json.country + ' ' + ($('Validate Case').first().json.route || '') }}",
      "={{ `<p>Case ${$('Validate Case').first().json.candidate_ref} needs a lawyer in <b>${$('Validate Case').first().json.country}</b>"
      " for route <b>${$('Validate Case').first().json.route || 'any'}</b> (language ${$('Validate Case').first().json.lang}). "
      "No verified lawyer with referral consent and free capacity. Recruit one via workflow 05 / sign-up form.</p>` }}",
      [1100, 420])
respond(wf, "Respond Gap", "={{ JSON.stringify({ ok: false, reason: 'no_lawyer_available', escalated: true }) }}", [1320, 420], code_=202)
wf.chain("Case Webhook", "Config", "Validate Case", "Match Lawyers", "Found?")
wf.link("Found?", "Create Engagement", 0)
wf.link("Found?", "Coverage Gap Alert", 1)
wf.link("Create Engagement", "Brief Lawyer")
wf.link("Create Engagement", "WhatsApp Lawyer")
wf.link("Brief Lawyer", "Respond Matched")
wf.link("Coverage Gap Alert", "Respond Gap")
wf.save("03-case-lawyer-matcher.json", ["lawnet", "matching", "langgraph"])

# =====================================================================
# 04 — Daily governance (SOP §4): SLA, review queue, URL health, GDPR purge
# =====================================================================
wf = WF("LAWNET · 04 Daily governance")
wf.node("Every Morning 07:00", "n8n-nodes-base.scheduleTrigger",
        {"rule": {"interval": [{"field": "cronExpression", "expression": "0 7 * * *"}]}}, [0, 300], 1.2)
config(wf, [220, 300])
pg(wf, "Mark SLA Breaches", r"""update lawnet.engagements set status = 'sla_breached'
where status in ('proposed','lawyer_notified') and sla_due_at < now()
returning id, candidate_ref, country_iso2, route_code, lawyer_id;""", None, [440, 80], always=True)
pg(wf, "Review Queue > SLA", "select public_ref, full_name, country_iso2, bar_number, verification, round(extract(epoch from waiting)/3600) as hours "
   "from lawnet.v_verification_queue where waiting > ($1 || ' hours')::interval or verification = 'verified';",
   "={{ [String($('Config').first().json.cfg.reviewSlaHours)] }}", [440, 220], always=True)
pg(wf, "GDPR Purge", "select lawnet.purge_unanswered_register_records() as erased;", None, [440, 360])
pg(wf, "Coverage", "select * from lawnet.v_country_coverage where priority <= 5;", None, [440, 500])
pg(wf, "URLs To Check", r"""select 'bar' as kind, id, coalesce(register_search_url, website) as url from lawnet.bar_authorities where coalesce(register_search_url, website) is not null
union all select 'permit', id, website from lawnet.permit_authorities where website is not null;""", None, [440, 640])
http(wf, "Ping URL", "GET", "={{ $json.url }}", None, [660, 640], None)
wf.nodes[-1]["parameters"]["authentication"] = "none"
wf.nodes[-1]["parameters"]["options"] = {"timeout": 15000, "redirect": {"redirect": {"followRedirects": True}},
                                        "response": {"response": {"fullResponse": True, "neverError": True}}}
wf.nodes[-1].pop("credentials", None)
code(wf, "URL Results", r"""const src = $('URLs To Check').all();
return $input.all().map((it, i) => ({ json: { kind: src[i].json.kind, id: src[i].json.id, url: src[i].json.url,
  status: it.json.statusCode || (it.json.error ? 0 : 200) } }));""", [880, 640])
pg(wf, "Save URL Status", r"""update lawnet.bar_authorities set url_last_status = $3::int, url_verified_at = case when $3::int between 200 and 399 then now() else url_verified_at end where $1 = 'bar' and id = $2::uuid;
update lawnet.permit_authorities set url_last_status = $3::int, url_verified_at = case when $3::int between 200 and 399 then now() else url_verified_at end where $1 = 'permit' and id = $2::uuid;""",
   "={{ [$json.kind, $json.id, $json.status] }}", [1100, 640])
wf.node("Wait All", "n8n-nodes-base.merge", {"mode": "chooseBranch", "numberInputs": 4}, [880, 300], 3)
code(wf, "Build Report", r"""const rows = n => { try { return $(n).all().map(i => i.json).filter(j => Object.keys(j).length); } catch { return []; } };
const breaches = rows('Mark SLA Breaches'), queue = rows('Review Queue > SLA'), cov = rows('Coverage');
const erased = (rows('GDPR Purge')[0] || {}).erased || 0;
const t = (list, cols) => list.length ? `<table border=1 cellpadding=4 style="border-collapse:collapse">` +
  `<tr>${cols.map(c => `<th>${c}</th>`).join('')}</tr>` + list.map(r => `<tr>${cols.map(c => `<td>${r[c] ?? ''}</td>`).join('')}</tr>`).join('') + '</table>' : '<p>None ✅</p>';
const html = `<h2>Legal network – daily governance</h2>
<h3>Referral SLA breaches (${breaches.length})</h3>${t(breaches, ['candidate_ref','country_iso2','route_code'])}
<h3>Verification queue over SLA / re-verification due (${queue.length})</h3>${t(queue, ['public_ref','full_name','country_iso2','bar_number','verification','hours'])}
<h3>Coverage – priority markets</h3>${t(cov, ['iso2','name','lawyers_total','lawyers_verified','routes_covered','routes_total'])}
<p>GDPR: ${erased} unanswered public-register record(s) erased (30-day rule).</p>`;
return [{ json: { html, alert: breaches.length + queue.length > 0 } }];""", [1100, 300])
email(wf, "Email Ops", "={{ $('Config').first().json.cfg.opsEmail + ',' + $('Config').first().json.cfg.complianceEmail }}",
      "={{ ($json.alert ? '⚠ ' : '✅ ') + 'Legal network daily report ' + $now.toFormat('yyyy-LL-dd') }}", "={{ $json.html }}", [1320, 300])
for n in ("Mark SLA Breaches", "Review Queue > SLA", "GDPR Purge", "Coverage", "URLs To Check"):
    wf.link("Config", n)
wf.chain("Every Morning 07:00", "Config")
for i, n in enumerate(("Mark SLA Breaches", "Review Queue > SLA", "GDPR Purge", "Coverage")):
    wf.conn.setdefault(n, {"main": [[]]})["main"][0].append({"node": "Wait All", "type": "main", "index": i})
wf.chain("Wait All", "Build Report", "Email Ops")
wf.chain("URLs To Check", "Ping URL", "URL Results", "Save URL Status")
wf.save("04-daily-governance.json", ["lawnet", "governance", "gdpr"])

# =====================================================================
# 05 — Public bar-register sourcing import (staff upload) + GDPR Art.14 notice
# =====================================================================
wf = WF("LAWNET · 05 Register import + Art.14 notice")
webhook(wf, "Import Webhook", "lawnet-import", "POST", [0, 300], creds=CRED_AGENT)
config(wf, [220, 300])
code(wf, "Normalise Rows", r"""// Body: { rows: [ {full_name, country, city, firm, bar_number, email, phone, website, source_url, routes, languages, practice_areas} ] }
// Rows come from staff copying PUBLIC bar-register / firm-website data (legitimate interest, SOP §5).
const rows = ($('Import Webhook').first().json.body || {}).rows || [];
const clean = (s, n = 200) => String(s ?? '').trim().slice(0, n);
const list = v => JSON.stringify((Array.isArray(v) ? v : String(v ?? '').split(/[;,]/)).map(x => clean(x, 40)).filter(Boolean));
return rows.slice(0, 500).filter(r => clean(r.full_name) && /^[A-Za-z]{2}$/.test(clean(r.country))).map(r => ({ json: {
  full_name: clean(r.full_name, 120), country: clean(r.country, 2).toUpperCase(), city: clean(r.city, 80),
  firm: clean(r.firm, 160), bar_number: clean(r.bar_number, 60),
  email: /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(clean(r.email)) ? clean(r.email).toLowerCase() : '',
  phone: clean(r.phone, 25).replace(/[^\d+]/g, ''), website: clean(r.website), source_url: clean(r.source_url, 500),
  routes: list(r.routes), languages: list(r.languages), practice: list(r.practice_areas)
}}));""", [440, 300])
pg(wf, "Upsert Register Record", r"""with f as (
  insert into lawnet.firms(name, country_iso2, city, source, source_url) select $5, $2, nullif($3,''), 'public_bar_register', nullif($10,'')
  where nullif($5,'') is not null on conflict (country_iso2, name) do update set city = coalesce(lawnet.firms.city, excluded.city) returning id),
l as (
  insert into lawnet.lawyers(full_name, country_iso2, city, firm_id, bar_number, email, phone_e164, website, source, source_url, lawful_basis, verification,
     bar_authority_id)
  values ($1, $2, nullif($3,''), (select id from f), nullif($4,''), nullif($6,''),
     case when $7 ~ '^\+[1-9][0-9]{6,14}$' then $7 end, nullif($8,''), 'public_bar_register', nullif($10,''), 'legitimate_interest', 'unverified',
     (select id from lawnet.bar_authorities where country_iso2 = $2 order by jurisdiction = 'National' desc limit 1))
  on conflict (country_iso2, bar_number) do update set city = coalesce(excluded.city, lawnet.lawyers.city),
     email = coalesce(lawnet.lawyers.email, excluded.email), website = coalesce(lawnet.lawyers.website, excluded.website)
  returning id, public_ref, email, full_name, art14_notice_sent_at, (xmax = 0) as inserted),
r as (insert into lawnet.lawyer_routes(lawyer_id, route_code) select (select id from l), x from jsonb_array_elements_text($9::jsonb) x
      where exists (select 1 from lawnet.work_routes where code = x) on conflict do nothing),
g as (insert into lawnet.lawyer_languages(lawyer_id, lang) select (select id from l), lower(x) from jsonb_array_elements_text($11::jsonb) x
      where length(x) = 2 on conflict do nothing),
p as (insert into lawnet.lawyer_practice_areas(lawyer_id, practice_code) select (select id from l), x from jsonb_array_elements_text($12::jsonb) x
      where exists (select 1 from lawnet.practice_areas where code = x) on conflict do nothing)
select * from l;""",
   "={{ [$json.full_name, $json.country, $json.city, $json.bar_number, $json.firm, $json.email, $json.phone, $json.website, "
   "$json.routes, $json.source_url, $json.languages, $json.practice] }}", [660, 300])
code(wf, "Needs Art.14 Notice", SIGN_JS + r"""const cfg = $('Config').first().json.cfg;
return $input.all().filter(i => i.json.email && !i.json.art14_notice_sent_at).map(i => ({ json: { ...i.json,
  joinUrl: `${cfg.n8nBase.replace('/webhook','')}/lawyer-signup.html?ref=${i.json.public_ref}`,
  eraseUrl: `${cfg.n8nBase}/lawnet-verify?id=${i.json.id}&d=suspended&t=${sign(i.json.id, 'suspended')}` } }));""", [880, 300])
email(wf, "Send Art.14 Notice", "={{ $json.email }}",
      "={{ 'Invitation & privacy notice – ' + $('Config').first().json.cfg.brand }}",
      "={{ `<p>Dear ${$json.full_name},</p><p>We operate a referral network that connects employers and foreign workers with "
      "local immigration and employment lawyers. We found your professional details in a public bar register / your firm website "
      "and hold: name, city, firm, bar number and business contact (legal basis: legitimate interest, GDPR Art. 6(1)(f); notice under Art. 14).</p>"
      "<p><a href=\"${$json.joinUrl}\">Join the network and receive paid referrals</a></p>"
      "<p>If you do not want this, <a href=\"${$json.eraseUrl}\">click here</a> or simply ignore this e-mail – "
      "your record is erased automatically after 30 days. Privacy notice: ${$('Config').first().json.cfg.privacyUrl}</p>` }}",
      [1100, 300])
pg(wf, "Mark Notice Sent", "update lawnet.lawyers set art14_notice_sent_at = now() where id = $1::uuid;",
   "={{ [$('Needs Art.14 Notice').item.json.id] }}", [1320, 300])
respond(wf, "Respond Import", "={{ JSON.stringify({ ok: true, imported: $('Upsert Register Record').all().length }) }}", [1540, 300])
wf.chain("Import Webhook", "Config", "Normalise Rows", "Upsert Register Record", "Needs Art.14 Notice",
         "Send Art.14 Notice", "Mark Notice Sent", "Respond Import")
wf.save("05-register-import-art14.json", ["lawnet", "sourcing", "gdpr"])

with open(os.path.join(OUT, "sql_from_workflows.sql"), "w") as f:
    f.write("-- Generated: every SQL statement used by the n8n Postgres nodes (for review/testing).\n")
    for w, n, q in SQL_LOG:
        f.write(f"\n-- [{w}] {n}\n{q}\n")
