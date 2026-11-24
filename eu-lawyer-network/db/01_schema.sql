-- =====================================================================
-- Project Global Node · European Manpower Lawyer Network
-- PostgreSQL 15+ / Supabase. Run files in order: 01 → 02 → 03.
-- PII rules (SOP §5): candidate data never stored here except the
-- anonymised CAND-XXXXX id. Lawyer contact data is gated by consent.
-- =====================================================================
create extension if not exists pgcrypto;
create extension if not exists pg_trgm;

create schema if not exists lawnet;
set search_path = lawnet, public;

-- ---------- enums ----------
do $$ begin
  create type verification_status as enum ('unverified','pending_review','verified','rejected','expired','suspended');
  create type lawful_basis       as enum ('consent','legitimate_interest','contract');
  create type source_type        as enum ('self_registration','public_bar_register','referral','partner_import','manual');
  create type engagement_status  as enum ('proposed','lawyer_notified','accepted','declined','in_progress','completed','cancelled','sla_breached');
  create type eu_status          as enum ('eu','eea','candidate','third_country');
exception when duplicate_object then null; end $$;

-- ---------- reference: countries ----------
create table if not exists countries (
  iso2                  char(2) primary key,
  name                  text not null,
  local_name            text,
  status                eu_status not null,
  schengen              boolean not null default false,
  currency              char(3) not null,
  official_languages    text[] not null,
  eu_blue_card          boolean not null default false,
  priority              smallint not null default 9,     -- 1 = active sourcing market
  notes                 text,
  updated_at            timestamptz not null default now()
);

-- Bar associations / law societies (some countries have several, e.g. BA entities)
create table if not exists bar_authorities (
  id                    uuid primary key default gen_random_uuid(),
  country_iso2          char(2) not null references countries(iso2),
  name_local            text not null,
  name_en               text not null,
  jurisdiction          text,                           -- e.g. 'Federation of BiH'
  website               text,
  register_search_url   text,                           -- public lawyer register, if any
  url_verified_at       timestamptz,                    -- set by n8n link checker
  url_last_status       int,
  notes                 text,
  unique (country_iso2, name_en)
);

-- Immigration / labour authorities that issue permits
create table if not exists permit_authorities (
  id                    uuid primary key default gen_random_uuid(),
  country_iso2          char(2) not null references countries(iso2),
  name_local            text not null,
  name_en               text not null,
  role                  text not null,                  -- 'work_permit','residence','visa','labour_market_test','info_portal'
  website               text,
  url_verified_at       timestamptz,
  url_last_status       int,
  unique (country_iso2, name_en, role)
);

-- Work / residence routes per country (what a lawyer may handle)
create table if not exists work_routes (
  code                  text primary key,               -- 'RO-WORK-PERMANENT'
  country_iso2          char(2) not null references countries(iso2),
  name                  text not null,
  local_term            text,
  category              text not null,                  -- 'skilled','seasonal','posted','highly_skilled','ict','family','job_seeker'
  quota_based           boolean not null default false,
  labour_market_test    boolean,
  description           text,
  needs_legal_review    boolean not null default true,  -- HITL: Legal Compliance Officer confirms yearly
  reviewed_at           timestamptz,
  reviewed_by           text
);

create table if not exists practice_areas (
  code                  text primary key,
  name                  text not null,
  description           text
);

-- ---------- core: firms & lawyers ----------
create table if not exists firms (
  id                    uuid primary key default gen_random_uuid(),
  name                  text not null,
  country_iso2          char(2) not null references countries(iso2),
  city                  text,
  website               text,
  general_email         text,                           -- business contact, not personal
  general_phone         text,
  registration_no       text,                           -- company / bar firm registration
  hubspot_company_id    text,
  source                source_type not null default 'manual',
  source_url            text,
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now(),
  unique (country_iso2, name)
);

create table if not exists lawyers (
  id                    uuid primary key default gen_random_uuid(),
  public_ref            text unique not null default ('LAW-' || upper(substr(md5(random()::text),1,6))),
  firm_id               uuid references firms(id) on delete set null,
  full_name             text not null,
  title                 text,                           -- 'Avocat', 'Advokat', 'Odvetnik'
  country_iso2          char(2) not null references countries(iso2),   -- main admission
  city                  text,
  bar_authority_id      uuid references bar_authorities(id),
  bar_number            text,
  admitted_year         smallint check (admitted_year between 1950 and 2100),
  email                 text,
  phone_e164            text check (phone_e164 is null or phone_e164 ~ '^\+[1-9][0-9]{6,14}$'),
  whatsapp_e164         text check (whatsapp_e164 is null or whatsapp_e164 ~ '^\+[1-9][0-9]{6,14}$'),
  website               text,
  linkedin_url          text,
  bio                   text,
  hourly_rate_eur       numeric(8,2),
  fixed_fee_permit_eur  numeric(8,2),                   -- typical fee for a single work-permit file
  accepts_remote        boolean not null default true,
  capacity_per_month    smallint default 10,
  rating                numeric(3,2) check (rating between 0 and 5),
  verification          verification_status not null default 'unverified',
  verified_at           timestamptz,
  verified_by           text,
  next_reverify_at      timestamptz,
  source                source_type not null,
  source_url            text,
  lawful_basis          lawful_basis not null,
  art14_notice_sent_at  timestamptz,                    -- GDPR Art.14 when data came from a public register
  marketing_opt_in      boolean not null default false,
  is_active             boolean not null default true,
  hubspot_contact_id    text,
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now(),
  constraint uq_bar_number unique (country_iso2, bar_number),
  -- self-registered lawyers must be on consent; register-sourced ones on legitimate interest
  constraint chk_basis check (source <> 'self_registration' or lawful_basis = 'consent')
);
create index if not exists ix_lawyers_country on lawyers(country_iso2) where is_active;
create index if not exists ix_lawyers_name_trgm on lawyers using gin (full_name gin_trgm_ops);
create unique index if not exists uq_lawyers_email on lawyers(lower(email)) where email is not null;

-- Lawyers can be admitted / active in several countries
create table if not exists lawyer_countries (
  lawyer_id             uuid references lawyers(id) on delete cascade,
  country_iso2          char(2) references countries(iso2),
  admitted              boolean not null default false,  -- true = bar admission, false = handles via partner
  primary key (lawyer_id, country_iso2)
);

create table if not exists lawyer_practice_areas (
  lawyer_id             uuid references lawyers(id) on delete cascade,
  practice_code         text references practice_areas(code),
  years_experience      smallint,
  primary key (lawyer_id, practice_code)
);

create table if not exists lawyer_routes (
  lawyer_id             uuid references lawyers(id) on delete cascade,
  route_code            text references work_routes(code),
  files_handled_12m     int default 0,
  primary key (lawyer_id, route_code)
);

create table if not exists lawyer_languages (
  lawyer_id             uuid references lawyers(id) on delete cascade,
  lang                  char(2) not null,                -- ISO 639-1: en, bn, hi, ne, ur, ro, bg ...
  level                 text not null default 'fluent' check (level in ('native','fluent','working')),
  primary key (lawyer_id, lang)
);

-- ---------- verification & GDPR ----------
create table if not exists verifications (
  id                    uuid primary key default gen_random_uuid(),
  lawyer_id             uuid not null references lawyers(id) on delete cascade,
  method                text not null,                   -- 'bar_register_lookup','document_upload','video_call','bar_letter'
  evidence_url          text,                            -- private storage link
  result                verification_status not null,
  checked_by            text not null,
  note                  text,
  checked_at            timestamptz not null default now()
);

create table if not exists consents (
  id                    uuid primary key default gen_random_uuid(),
  lawyer_id             uuid not null references lawyers(id) on delete cascade,
  purpose               text not null,                   -- 'directory_listing','referrals','marketing','b2b_portal_visibility'
  granted               boolean not null,
  text_version          text not null,
  ip                    inet,
  user_agent            text,
  captured_at           timestamptz not null default now()
);

-- ---------- operations: candidate → lawyer engagements ----------
create table if not exists engagements (
  id                    uuid primary key default gen_random_uuid(),
  candidate_ref         text not null check (candidate_ref ~ '^CAND-[A-Z0-9]{5,}$'),  -- anonymised only
  lawyer_id             uuid references lawyers(id),
  route_code            text references work_routes(code),
  country_iso2          char(2) references countries(iso2),
  employer_ref          text,                            -- B2B employer anonymised id
  status                engagement_status not null default 'proposed',
  match_score           numeric(5,2),
  fee_quoted_eur        numeric(10,2),
  sla_due_at            timestamptz,
  outcome               text,                            -- 'permit_granted','refused','appeal' ...
  created_at            timestamptz not null default now(),
  updated_at            timestamptz not null default now()
);
create index if not exists ix_engagements_open on engagements(status, sla_due_at)
  where status in ('proposed','lawyer_notified','accepted','in_progress');

create table if not exists audit_log (
  id                    bigserial primary key,
  table_name            text not null,
  row_id                text not null,
  action                text not null,
  actor                 text not null default current_user,
  diff                  jsonb,
  at                    timestamptz not null default now()
);

-- ---------- triggers ----------
create or replace function touch_updated_at() returns trigger language plpgsql set search_path = lawnet, public as $$
begin new.updated_at := now(); return new; end $$;

create or replace function audit_row() returns trigger language plpgsql set search_path = lawnet, public as $$
begin
  insert into audit_log(table_name,row_id,action,diff)
  values (tg_table_name, coalesce((case when tg_op='DELETE' then old.id else new.id end)::text,'?'), tg_op,
          case when tg_op='DELETE' then to_jsonb(old) else to_jsonb(new) end);
  return coalesce(new, old);
end $$;

do $$ declare t text; begin
  foreach t in array array['firms','lawyers','engagements'] loop
    execute format('drop trigger if exists trg_touch on %I; create trigger trg_touch before update on %I for each row execute function touch_updated_at();', t, t);
    execute format('drop trigger if exists trg_audit on %I; create trigger trg_audit after insert or update or delete on %I for each row execute function audit_row();', t, t);
  end loop;
end $$;

-- Re-verify yearly
create or replace function set_reverify() returns trigger language plpgsql set search_path = lawnet, public as $$
begin
  if new.verification = 'verified' and (old is null or old.verification is distinct from 'verified') then
    new.verified_at := coalesce(new.verified_at, now());
    new.next_reverify_at := new.verified_at + interval '365 days';
  end if;
  return new;
end $$;
drop trigger if exists trg_reverify on lawyers;
create trigger trg_reverify before insert or update of verification on lawyers
  for each row execute function set_reverify();

-- ---------- views ----------
-- Masked directory for the B2B portal and AI agents: no email / phone.
create or replace view v_lawyer_directory as
select l.public_ref, l.full_name, l.title, c.name as country, l.city, f.name as firm,
       l.verification, l.accepts_remote, l.fixed_fee_permit_eur, l.rating,
       (select array_agg(practice_code order by practice_code) from lawyer_practice_areas p where p.lawyer_id = l.id) as practice_areas,
       (select array_agg(route_code order by route_code) from lawyer_routes r where r.lawyer_id = l.id) as routes,
       (select array_agg(lang order by lang) from lawyer_languages g where g.lawyer_id = l.id) as languages,
       (select array_agg(country_iso2 order by country_iso2) from lawyer_countries x where x.lawyer_id = l.id) as countries_served
from lawyers l
join countries c on c.iso2 = l.country_iso2
left join firms f on f.id = l.firm_id
where l.is_active
  and exists (select 1 from consents k where k.lawyer_id = l.id and k.purpose = 'directory_listing' and k.granted);

create or replace view v_verification_queue as
select l.id, l.public_ref, l.full_name, l.country_iso2, l.bar_number, b.name_en as bar, b.register_search_url,
       l.verification, l.created_at, now() - l.created_at as waiting
from lawyers l left join bar_authorities b on b.id = l.bar_authority_id
where l.verification in ('unverified','pending_review')
   or (l.verification = 'verified' and l.next_reverify_at < now())
order by l.created_at;

create or replace view v_country_coverage as
select c.iso2, c.name, c.priority,
       count(l.id) filter (where l.is_active)                          as lawyers_total,
       count(l.id) filter (where l.verification = 'verified')          as lawyers_verified,
       count(distinct lr.route_code)                                   as routes_covered,
       (select count(*) from work_routes w where w.country_iso2 = c.iso2) as routes_total
from countries c
left join lawyers l on l.country_iso2 = c.iso2
left join lawyer_routes lr on lr.lawyer_id = l.id
group by c.iso2, c.name, c.priority
order by c.priority, c.name;

-- ---------- matching (called by n8n / EU Compliance Agent) ----------
create or replace function match_lawyers(p_country char(2), p_route text default null,
                                         p_lang char(2) default 'en', p_limit int default 3)
returns table (lawyer_id uuid, public_ref text, full_name text, score numeric, open_files bigint)
language sql stable set search_path = lawnet, public as $$
  with open_load as (
    select lawyer_id, count(*) n from engagements
    where status in ('lawyer_notified','accepted','in_progress') group by lawyer_id)
  select l.id, l.public_ref, l.full_name,
         ( 40 * (l.verification = 'verified')::int
         + 25 * (exists (select 1 from lawyer_routes r where r.lawyer_id = l.id and r.route_code = p_route))::int
         + 15 * (exists (select 1 from lawyer_languages g where g.lawyer_id = l.id and g.lang = p_lang))::int
         + 10 * coalesce(l.rating,3) / 5
         + 10 * greatest(0, 1 - coalesce(o.n,0)::numeric / greatest(l.capacity_per_month,1))
         )::numeric(5,2) as score,
         coalesce(o.n,0)
  from lawyers l
  left join open_load o on o.lawyer_id = l.id
  where l.is_active
    and l.verification = 'verified'
    and (l.country_iso2 = p_country or exists (select 1 from lawyer_countries x where x.lawyer_id = l.id and x.country_iso2 = p_country))
    and exists (select 1 from consents k where k.lawyer_id = l.id and k.purpose = 'referrals' and k.granted)
    and coalesce(o.n,0) < coalesce(l.capacity_per_month, 10)
  order by score desc, coalesce(o.n,0) asc
  limit p_limit
$$;

-- ---------- GDPR: right to be forgotten ----------
create or replace function forget_lawyer(p_id uuid, p_actor text) returns void language plpgsql set search_path = lawnet, public as $$
begin
  update lawyers set full_name = 'ERASED', email = null, phone_e164 = null, whatsapp_e164 = null,
         linkedin_url = null, bio = null, website = null, bar_number = null, is_active = false,
         hubspot_contact_id = null
  where id = p_id;
  delete from consents where lawyer_id = p_id;
  delete from verifications where lawyer_id = p_id;
  insert into audit_log(table_name,row_id,action,actor) values ('lawyers', p_id::text, 'ERASE', p_actor);
end $$;

-- Public-register records with no reply 30 days after the Art.14 notice are erased (SOP §5)
create or replace function purge_unanswered_register_records() returns int language plpgsql set search_path = lawnet, public as $$
declare n int := 0; r record;
begin
  for r in select id from lawyers
           where source = 'public_bar_register' and lawful_basis = 'legitimate_interest'
             and art14_notice_sent_at < now() - interval '30 days'
             and not exists (select 1 from consents k where k.lawyer_id = lawyers.id and k.granted)
             and is_active
  loop perform forget_lawyer(r.id, 'purge_job'); n := n + 1; end loop;
  return n;
end $$;
