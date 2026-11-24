-- =====================================================================
-- Supabase row-level security. n8n connects with the service role
-- (bypasses RLS). Portal users get roles via JWT app_metadata.role:
--   'compliance'  – EU Legal Compliance Officer: full read/write
--   'counselor'   – reads directory + engagements, no raw contacts
--   'employer'    – B2B portal: masked directory only (SOP §5)
-- Skip this file on plain Postgres.
-- =====================================================================
set search_path = lawnet, public;

create or replace function lawnet.jwt_role() returns text language sql stable as $$
  select coalesce(current_setting('request.jwt.claims', true)::jsonb -> 'app_metadata' ->> 'role', 'anon')
$$;

do $$ declare t text; begin
  foreach t in array array['lawyers','firms','consents','verifications','engagements','lawyer_countries',
                           'lawyer_practice_areas','lawyer_routes','lawyer_languages','audit_log'] loop
    execute format('alter table lawnet.%I enable row level security', t);
    execute format('drop policy if exists compliance_all on lawnet.%I', t);
    execute format('create policy compliance_all on lawnet.%I for all using (lawnet.jwt_role() = ''compliance'') with check (lawnet.jwt_role() = ''compliance'')', t);
  end loop;
end $$;

drop policy if exists counselor_read on lawnet.engagements;
create policy counselor_read on lawnet.engagements for select using (lawnet.jwt_role() in ('counselor','compliance'));

-- reference tables are public-read
do $$ declare t text; begin
  foreach t in array array['countries','bar_authorities','permit_authorities','work_routes','practice_areas'] loop
    execute format('alter table lawnet.%I enable row level security', t);
    execute format('drop policy if exists read_all on lawnet.%I', t);
    execute format('create policy read_all on lawnet.%I for select using (true)', t);
  end loop;
end $$;

-- masked view runs with owner rights so employers/counselors never touch raw contact columns
alter view lawnet.v_lawyer_directory set (security_invoker = false);
grant usage on schema lawnet to authenticated;
grant select on lawnet.v_lawyer_directory, lawnet.v_country_coverage to authenticated;
grant select on lawnet.countries, lawnet.bar_authorities, lawnet.permit_authorities, lawnet.work_routes, lawnet.practice_areas to anon, authenticated;
