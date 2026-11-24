# European Manpower Lawyer Network (Project Global Node)

A database of immigration and employment lawyers, plus the automation that runs it. It connects foreign workers and EU employers with **verified local lawyers** for work permits, residence permits and labour‑law files.

**Priority markets (fully seeded):** 🇷🇴 Romania · 🇧🇬 Bulgaria · 🇲🇰 North Macedonia · 🇧🇦 Bosnia & Herzegovina · 🇱🇹 Lithuania · 🇱🇻 Latvia · 🇸🇮 Slovenia · 🇸🇰 Slovakia
**Also listed (ready to expand):** all EU‑27, EEA, Switzerland, UK and the other candidate countries (42 countries in total).

```
eu-lawyer-network/
├── db/
│   ├── 01_schema.sql            tables, views, matching function, GDPR erase/purge, audit trail
│   ├── 02_reference_data.sql    42 countries, 10 bar authorities, 27 permit authorities, 38 work routes, 15 practice areas
│   └── 03_supabase_security.sql row-level security (compliance / counselor / employer roles)
├── n8n/                         importable workflows (+ build_workflows.py generator)
│   ├── 01-lawyer-self-registration.json
│   ├── 02-verification-decision.json
│   ├── 03-case-lawyer-matcher.json
│   ├── 04-daily-governance.json
│   ├── 05-register-import-art14.json
│   └── sql_from_workflows.sql   every SQL statement the workflows run (for review)
├── web/lawyer-signup.html       lawyer sign-up form that posts to workflow 01
└── data/
    ├── register_import_template.csv   columns for bulk import (workflow 05)
    └── sourcing_checklist.csv         per-country sourcing plan + local search terms
```

## What the data model holds

| Table | Purpose |
|---|---|
| `countries` | EU/EEA/candidate status, Schengen, currency, Blue Card applicability, `priority` (1 = active market) |
| `bar_authorities` | The bar that can confirm a lawyer is admitted. Bosnia has three: FBiH, Republika Srpska and Brčko |
| `permit_authorities` | Who issues work permits, residence permits and visas, and who runs the labour‑market test (IGI, Employment Agency, MIGRIS, PMLP, ZRSZ, ÚPSVaR…) |
| `work_routes` | Permit routes per country, e.g. `RO-PERMANENT`, `BG-SINGLE`, `SK-TRP-EMPLOY`, with quota and labour‑market‑test flags |
| `firms`, `lawyers` | Directory records: bar number, fees, capacity, verification state, source, GDPR lawful basis |
| `lawyer_countries / _routes / _languages / _practice_areas` | What each lawyer covers, used for matching |
| `verifications`, `consents` | Evidence trail for the human‑in‑the‑loop check, and consent log with text version, IP and time |
| `engagements` | Case → lawyer referrals. Only anonymised `CAND-XXXXX` ids are accepted (enforced by a CHECK constraint) |
| `audit_log` | Every change to firms, lawyers and engagements |

Views:
- `v_lawyer_directory`: masked profiles (no e‑mail or phone) for the B2B portal and AI agents.
- `v_verification_queue`: lawyers waiting for verification or due for re‑verification.
- `v_country_coverage`: lawyers and routes covered per country.

Function: `match_lawyers(country, route, lang, limit)` scores each lawyer out of 100:
- 40 for verified
- 25 for handling the route
- 15 for speaking the language
- 10 for rating
- 10 for free capacity

Only lawyers who consented to referrals are returned.

## Automation flow

```
Lawyer sign-up form ──► 01 Registration ──► Postgres + HubSpot ──► e-mail to Compliance Officer
                                                                    │ signed Approve/Reject link
                                                                    ▼
                                             02 Verification (HITL) ──► WhatsApp + e-mail welcome
EU Compliance Agent (LangGraph) ──► 03 Matcher ──► engagement + masked brief to lawyer (24h SLA)
                                            └─► no lawyer? coverage-gap alert to Compliance
Staff register research ──► 05 Import ──► GDPR Art.14 notice ──► auto-erase after 30 days without reply
07:00 daily ──► 04 Governance: SLA breaches · review queue > 4h · yearly re-verification · URL health · GDPR purge
```

## Setup

1. **Database:** in Supabase SQL editor (or `psql`), run `db/01_schema.sql`, then `db/02_reference_data.sql`, then `db/03_supabase_security.sql`. All three can be re‑run safely.
2. **n8n environment:**
   ```
   NODE_FUNCTION_ALLOW_BUILTIN=crypto
   N8N_BLOCK_ENV_ACCESS_IN_NODE=false
   LAWNET_HMAC_SECRET=<64 random chars>
   ```
3. **Import** the five JSON files from `n8n/`. Then attach these credentials:
   - **Postgres:** the Supabase connection string. Use the service role or a dedicated `lawnet` role.
   - **HubSpot** Private App.
   - **WhatsApp Cloud API:** Bearer token.
   - **SMTP.**
   - **Header Auth `X-Api-Key`:** used by workflows 03 and 05, which only your agents and staff call.
4. Edit the **Config** node in each workflow: e‑mails, `n8nBase`, `waPhoneNumberId`, privacy URL.
5. Create two **WhatsApp templates** in Meta Business Manager:
   - `lawnet_lawyer_verified`: body params `{{1}}` name, `{{2}}` ref.
   - `lawnet_new_case`: body params `{{1}}` name, `{{2}}` case ref, `{{3}}` country.
6. Put `ENDPOINT` in `web/lawyer-signup.html` and host the page, e.g. on the existing Cloudflare site.
7. **Calling the matcher** from the EU Compliance Agent:
   ```http
   POST /webhook/lawnet-match
   X-Api-Key: …
   {"candidate_ref":"CAND-7QX2P","country":"RO","route":"RO-PERMANENT","lang":"en","trade":"Welder","blocks":["A2 language"]}
   ```

Regenerate workflows after editing: `python3 n8n/build_workflows.py`.

## Filling the database with real lawyers

No individual lawyer records are shipped. Every record must come from one of these sources:
- **The lawyer**, via the sign‑up form. Lawful basis: consent.
- **A public bar register or firm website**, entered by staff into `register_import_template.csv` and posted to workflow 05. Lawful basis: legitimate interest. The lawyer gets an Art. 14 notice and an opt‑out link, and the record is erased after 30 days if they don't join.

`data/sourcing_checklist.csv` lists, for each priority country:
- the bar to search,
- local‑language search terms,
- a starting target (65 lawyers across the 8 markets).

Every lawyer must be verified against the bar before matching. In **Romania**, accept only lawyers registered with UNBR member bars. Lawyers who appear only in the parallel "constitutional" bars outside UNBR are not lawfully admitted.

## Compliance notes

- **Work‑route rules change every year** (quotas, salary thresholds, shortage lists). Every route row ships with `needs_legal_review = true`. The EU Legal Compliance Officer must confirm each one and set `reviewed_at` / `reviewed_by` before it is shown to candidates.
- **Unconfirmed links:** websites for the Bosnia & Herzegovina entity bars are left blank until confirmed. Workflow 04 checks every authority URL daily (`url_verified_at`, `url_last_status`).
- **No candidate personal data** is stored here, only `CAND-` references (SOP §5).
- **Right to erasure:** `select lawnet.forget_lawyer('<uuid>', 'who');`
