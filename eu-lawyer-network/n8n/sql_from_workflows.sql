-- Generated: every SQL statement used by the n8n Postgres nodes (for review/testing).

-- [LAWNET · 01 Lawyer self-registration] Claim Register Record
update lawnet.lawyers set email = $1
where country_iso2 = $2 and bar_number = nullif($3,'') and (email is null or lower(email) = $1)
returning id;

-- [LAWNET · 01 Lawyer self-registration] Upsert Lawyer
with f as (
  insert into lawnet.firms(name, country_iso2, city, website, source)
  select $8, $6, nullif($7,''), nullif($9,''), 'self_registration' where nullif($8,'') is not null
  on conflict (country_iso2, name) do update set website = coalesce(excluded.website, lawnet.firms.website)
  returning id),
ba as (select id from lawnet.bar_authorities where country_iso2 = $6
       order by similarity(name_en || ' ' || name_local, $10::text) desc limit 1),
l as (
  insert into lawnet.lawyers(full_name, title, email, phone_e164, whatsapp_e164, country_iso2, city, firm_id,
     bar_authority_id, bar_number, admitted_year, website, linkedin_url, bio, fixed_fee_permit_eur, hourly_rate_eur,
     capacity_per_month, source, lawful_basis, marketing_opt_in, verification)
  values ($1, nullif($2,''), $3, nullif($4,''), nullif($5,''), $6, nullif($7,''),
     (select id from f), (select id from ba), nullif($11,''), nullif($12,'')::smallint, nullif($13,''),
     nullif($14,''), nullif($15,''), nullif($16,'')::numeric, nullif($17,'')::numeric, $18::smallint,
     'self_registration', 'consent', $19::boolean, 'pending_review')
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
c  as (insert into lawnet.lawyer_countries select (select id from l), x, x = $6 from jsonb_array_elements_text($20::jsonb) x
       where exists (select 1 from lawnet.countries where iso2 = x) on conflict do nothing),
p  as (insert into lawnet.lawyer_practice_areas(lawyer_id, practice_code) select (select id from l), x from jsonb_array_elements_text($21::jsonb) x
       where exists (select 1 from lawnet.practice_areas where code = x) on conflict do nothing),
r  as (insert into lawnet.lawyer_routes(lawyer_id, route_code) select (select id from l), x from jsonb_array_elements_text($22::jsonb) x
       where exists (select 1 from lawnet.work_routes where code = x) on conflict do nothing),
g  as (insert into lawnet.lawyer_languages(lawyer_id, lang) select (select id from l), x from jsonb_array_elements_text($23::jsonb) x
       where length(x) = 2 on conflict do nothing),
k  as (insert into lawnet.consents(lawyer_id, purpose, granted, text_version, ip, user_agent)
       select (select id from l), e->>'purpose', (e->>'granted')::boolean, $24, nullif($25,'')::inet, $26
       from jsonb_array_elements($27::jsonb) e)
select l.id, l.public_ref, l.verification, bar.register_search_url, bar.website as bar_website, bar.name_en as bar
from l left join lawnet.bar_authorities bar on bar.id = l.bar_authority_id;

-- [LAWNET · 02 Verification decision (HITL)] Apply Decision
with u as (
  update lawnet.lawyers set verification = $2::lawnet.verification_status, verified_by = $3,
         verified_at = case when $2 = 'verified' then now() else verified_at end
  where id = $1::uuid returning id, public_ref, full_name, email, whatsapp_e164, hubspot_contact_id, verification)
, v as (insert into lawnet.verifications(lawyer_id, method, result, checked_by)
        select id, 'bar_register_lookup', verification, $3 from u)
select * from u;

-- [LAWNET · 03 Case → lawyer matcher] Match Lawyers
select * from lawnet.match_lawyers($1, nullif($2,''), $3, $4::int);

-- [LAWNET · 03 Case → lawyer matcher] Create Engagement
insert into lawnet.engagements(candidate_ref, lawyer_id, route_code, country_iso2, employer_ref, status, match_score, sla_due_at)
values ($1, $2::uuid, nullif($3,''), $4, nullif($5,''), 'lawyer_notified', $6::numeric, now() + ($7 || ' hours')::interval)
returning id as engagement_id, lawyer_id, sla_due_at,
  (select email from lawnet.lawyers where id = $2::uuid) as lawyer_email,
  (select whatsapp_e164 from lawnet.lawyers where id = $2::uuid) as lawyer_wa,
  (select full_name from lawnet.lawyers where id = $2::uuid) as lawyer_name;

-- [LAWNET · 04 Daily governance] Mark SLA Breaches
update lawnet.engagements set status = 'sla_breached'
where status in ('proposed','lawyer_notified') and sla_due_at < now()
returning id, candidate_ref, country_iso2, route_code, lawyer_id;

-- [LAWNET · 04 Daily governance] Review Queue > SLA
select public_ref, full_name, country_iso2, bar_number, verification, round(extract(epoch from waiting)/3600) as hours from lawnet.v_verification_queue where waiting > ($1 || ' hours')::interval or verification = 'verified';

-- [LAWNET · 04 Daily governance] GDPR Purge
select lawnet.purge_unanswered_register_records() as erased;

-- [LAWNET · 04 Daily governance] Coverage
select * from lawnet.v_country_coverage where priority <= 5;

-- [LAWNET · 04 Daily governance] URLs To Check
select 'bar' as kind, id, coalesce(register_search_url, website) as url from lawnet.bar_authorities where coalesce(register_search_url, website) is not null
union all select 'permit', id, website from lawnet.permit_authorities where website is not null;

-- [LAWNET · 04 Daily governance] Save URL Status
update lawnet.bar_authorities set url_last_status = $3::int, url_verified_at = case when $3::int between 200 and 399 then now() else url_verified_at end where $1 = 'bar' and id = $2::uuid;
update lawnet.permit_authorities set url_last_status = $3::int, url_verified_at = case when $3::int between 200 and 399 then now() else url_verified_at end where $1 = 'permit' and id = $2::uuid;

-- [LAWNET · 05 Register import + Art.14 notice] Upsert Register Record
with f as (
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
select * from l;

-- [LAWNET · 05 Register import + Art.14 notice] Mark Notice Sent
update lawnet.lawyers set art14_notice_sent_at = now() where id = $1::uuid;
