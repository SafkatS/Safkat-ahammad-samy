-- =====================================================================
-- Reference data. Priority-1 markets (fully seeded):
--   RO Romania · BG Bulgaria · MK North Macedonia · BA Bosnia & Herzegovina
--   LT Lithuania · LV Latvia · SI Slovenia · SK Slovakia
-- All other European countries are listed (priority 9) for later expansion.
--
-- ⚠ Immigration rules change every year (quotas, fees, lists of shortage
-- occupations). Every work_routes row ships with needs_legal_review = true;
-- the EU Legal Compliance Officer confirms each one and sets reviewed_at.
-- Authority URLs are checked daily by n8n workflow 04 (url_verified_at).
-- =====================================================================
set search_path = lawnet, public;

-- ---------- countries ----------
insert into countries (iso2,name,local_name,status,schengen,currency,official_languages,eu_blue_card,priority,notes) values
('RO','Romania','România','eu',true,'RON','{ro}',true,1,'Full Schengen member since 1 Jan 2025. Annual quota of newly admitted non-EU workers set by Government Decision.'),
('BG','Bulgaria','България','eu',true,'EUR','{bg}',true,1,'Full Schengen member since 1 Jan 2025; euro adopted 1 Jan 2026.'),
('MK','North Macedonia','Северна Македонија','candidate',false,'MKD','{mk,sq}',false,1,'EU candidate. Work permits for foreigners issued by the Employment Service Agency, within an annual quota.'),
('BA','Bosnia and Herzegovina','Bosna i Hercegovina','candidate',false,'BAM','{bs,hr,sr}',false,1,'EU candidate. Two entities (FBiH, Republika Srpska) + Brčko District: separate bars and employment services; residence handled at state level.'),
('LT','Lithuania','Lietuva','eu',true,'EUR','{lt}',true,1,'Applications via MIGRIS portal. Shortage-occupation list exempts some roles from labour market test.'),
('LV','Latvia','Latvija','eu',true,'EUR','{lv}',true,1,'Vacancy must be registered with State Employment Agency before employer invites a non-EU worker.'),
('SI','Slovenia','Slovenija','eu',true,'EUR','{sl}',true,1,'Single permit issued by the administrative unit with consent of the Employment Service of Slovenia.'),
('SK','Slovakia','Slovensko','eu',true,'EUR','{sk}',true,1,'Temporary residence for employment = single permit; shortage occupations list lowers the labour market test.'),
-- rest of the EU
('AT','Austria','Österreich','eu',true,'EUR','{de}',true,9,null),
('BE','Belgium','België / Belgique','eu',true,'EUR','{nl,fr,de}',true,9,null),
('HR','Croatia','Hrvatska','eu',true,'EUR','{hr}',true,5,'Large non-EU worker intake; candidate for phase 2.'),
('CY','Cyprus','Κύπρος','eu',false,'EUR','{el,tr}',true,9,null),
('CZ','Czechia','Česko','eu',true,'CZK','{cs}',true,5,'Employee Card system; candidate for phase 2.'),
('DK','Denmark','Danmark','eu',true,'DKK','{da}',false,9,'EU Blue Card directive does not apply (opt-out).'),
('EE','Estonia','Eesti','eu',true,'EUR','{et}',true,9,null),
('FI','Finland','Suomi','eu',true,'EUR','{fi,sv}',true,9,null),
('FR','France','France','eu',true,'EUR','{fr}',true,9,null),
('DE','Germany','Deutschland','eu',true,'EUR','{de}',true,5,'Chancenkarte / Opportunity Card, skilled-worker routes.'),
('GR','Greece','Ελλάδα','eu',true,'EUR','{el}',true,9,null),
('HU','Hungary','Magyarország','eu',true,'HUF','{hu}',true,5,'Guest-worker residence permit regime; candidate for phase 2.'),
('IE','Ireland','Éire','eu',false,'EUR','{en,ga}',false,9,'Not in Schengen; EU Blue Card does not apply (own employment permits).'),
('IT','Italy','Italia','eu',true,'EUR','{it}',true,9,null),
('LU','Luxembourg','Lëtzebuerg','eu',true,'EUR','{lb,fr,de}',true,9,null),
('MT','Malta','Malta','eu',true,'EUR','{mt,en}',true,9,null),
('NL','Netherlands','Nederland','eu',true,'EUR','{nl}',true,9,null),
('PL','Poland','Polska','eu',true,'PLN','{pl}',true,5,'Large non-EU worker intake; candidate for phase 2.'),
('PT','Portugal','Portugal','eu',true,'EUR','{pt}',true,9,null),
('ES','Spain','España','eu',true,'EUR','{es}',true,9,null),
('SE','Sweden','Sverige','eu',true,'SEK','{sv}',true,9,null),
-- EEA / EFTA / UK
('IS','Iceland','Ísland','eea',true,'ISK','{is}',false,9,null),
('LI','Liechtenstein','Liechtenstein','eea',true,'CHF','{de}',false,9,null),
('NO','Norway','Norge','eea',true,'NOK','{no}',false,9,null),
('CH','Switzerland','Schweiz / Suisse / Svizzera','third_country',true,'CHF','{de,fr,it,rm}',false,9,'EFTA, not EEA; Schengen member.'),
('GB','United Kingdom','United Kingdom','third_country',false,'GBP','{en}',false,9,'Immigration advice is regulated (solicitors / IAA-registered advisers).'),
-- Western Balkans & eastern candidates
('RS','Serbia','Србија','candidate',false,'RSD','{sr}',false,5,'Single permit since 2024; candidate for phase 2.'),
('ME','Montenegro','Crna Gora','candidate',false,'EUR','{cnr}',false,9,null),
('AL','Albania','Shqipëria','candidate',false,'ALL','{sq}',false,9,null),
('XK','Kosovo','Kosova / Kosovo','candidate',false,'EUR','{sq,sr}',false,9,'Potential candidate.'),
('MD','Moldova','Moldova','candidate',false,'MDL','{ro}',false,9,null),
('UA','Ukraine','Україна','candidate',false,'UAH','{uk}',false,9,null),
('GE','Georgia','საქართველო','candidate',false,'GEL','{ka}',false,9,null),
('TR','Türkiye','Türkiye','candidate',false,'TRY','{tr}',false,9,null)
on conflict (iso2) do update set name=excluded.name, local_name=excluded.local_name, status=excluded.status,
  schengen=excluded.schengen, currency=excluded.currency, official_languages=excluded.official_languages,
  eu_blue_card=excluded.eu_blue_card, priority=excluded.priority, notes=excluded.notes, updated_at=now();

-- ---------- bar authorities (who can confirm a lawyer is admitted) ----------
insert into bar_authorities (country_iso2,name_local,name_en,jurisdiction,website,register_search_url,notes) values
('RO','Uniunea Națională a Barourilor din România (UNBR)','National Union of Romanian Bars','National','https://www.unbr.ro',null,
 'Verify ONLY against UNBR / its member bars (e.g. Baroul București). Parallel "constitutional" bars outside UNBR are not lawful — reject lawyers registered only there.'),
('BG','Висш адвокатски съвет','Supreme Bar Council of Bulgaria','National','https://www.vas.bg',null,
 'Keeps the Unified Register of Lawyers; local bar = адвокатска колегия (e.g. Sofia Bar).'),
('MK','Адвокатска комора на Република Северна Македонија','Bar Association of the Republic of North Macedonia','National','https://www.mba.org.mk',null,
 'Confirm membership / licence number with the Bar.'),
('BA','Advokatska/Odvjetnička komora Federacije BiH','Bar Association of the Federation of BiH','Federation of BiH',null,null,
 'Entity-level bar. Website to be confirmed by link checker / compliance officer.'),
('BA','Advokatska komora Republike Srpske','Bar Association of Republika Srpska','Republika Srpska',null,null,
 'Entity-level bar. Website to be confirmed.'),
('BA','Advokatska komora Brčko distrikta','Bar Association of Brčko District','Brčko District',null,null,
 'Website to be confirmed.'),
('LT','Lietuvos advokatūra','Lithuanian Bar Association','National','https://www.advoco.lt',null,
 'Public search of practising advocates on the Bar website.'),
('LV','Latvijas Zvērinātu advokātu padome','Latvian Council of Sworn Advocates','National','https://www.advokatura.lv',null,
 'Only "zvērināts advokāts" (sworn advocate) may represent in court; check the Council list.'),
('SI','Odvetniška zbornica Slovenije','Bar Association of Slovenia','National','https://www.odv-zb.si',null,
 'Public directory of attorneys (imenik odvetnikov) on the Bar website.'),
('SK','Slovenská advokátska komora','Slovak Bar Association','National','https://www.sak.sk',null,
 'Public search of advocates (vyhľadávanie advokátov) on the Bar website.')
on conflict (country_iso2,name_en) do update set name_local=excluded.name_local, jurisdiction=excluded.jurisdiction,
  website=excluded.website, notes=excluded.notes;

-- ---------- permit authorities ----------
insert into permit_authorities (country_iso2,name_local,name_en,role,website) values
('RO','Inspectoratul General pentru Imigrări (IGI)','General Inspectorate for Immigration','work_permit','https://igi.mai.gov.ro'),
('RO','Inspectoratul General pentru Imigrări (IGI)','General Inspectorate for Immigration','residence','https://igi.mai.gov.ro'),
('RO','Ministerul Afacerilor Externe – eViza','Ministry of Foreign Affairs – eVisa','visa','https://evisa.mae.ro'),
('RO','Agenția Națională pentru Ocuparea Forței de Muncă (ANOFM)','National Employment Agency','labour_market_test','https://www.anofm.ro'),
('RO','Inspecția Muncii','Labour Inspectorate','labour_inspection','https://www.inspectiamuncii.ro'),
('BG','Агенция по заетостта','Employment Agency','work_permit','https://www.az.government.bg'),
('BG','Дирекция „Миграция“ – МВР','Migration Directorate, Ministry of Interior','residence','https://www.mvr.bg'),
('BG','Министерство на външните работи','Ministry of Foreign Affairs','visa','https://www.mfa.bg'),
('MK','Агенција за вработување','Employment Service Agency','work_permit','https://av.gov.mk'),
('MK','Министерство за внатрешни работи','Ministry of Interior','residence','https://mvr.gov.mk'),
('MK','Министерство за надворешни работи','Ministry of Foreign Affairs','visa','https://www.mfa.gov.mk'),
('BA','Služba za poslove sa strancima','Service for Foreigners'' Affairs','residence','https://www.sps.gov.ba'),
('BA','Ministarstvo sigurnosti BiH','Ministry of Security of BiH','quota','https://www.msb.gov.ba'),
('BA','Federalni zavod za zapošljavanje','Federal Employment Institute (FBiH)','work_permit','https://www.fzzz.ba'),
('BA','Zavod za zapošljavanje Republike Srpske','Employment Institute of Republika Srpska','work_permit','https://www.zzzrs.net'),
('BA','Ministarstvo vanjskih poslova BiH','Ministry of Foreign Affairs of BiH','visa','https://www.mvp.gov.ba'),
('LT','Migracijos departamentas (MIGRIS)','Migration Department','residence','https://www.migracija.lt'),
('LT','Migracijos departamentas (MIGRIS)','Migration Department','work_permit','https://www.migracija.lt'),
('LT','Užimtumo tarnyba','Employment Service','labour_market_test','https://uzt.lt'),
('LV','Pilsonības un migrācijas lietu pārvalde (PMLP)','Office of Citizenship and Migration Affairs','residence','https://www.pmlp.gov.lv'),
('LV','Pilsonības un migrācijas lietu pārvalde (PMLP)','Office of Citizenship and Migration Affairs','visa','https://www.pmlp.gov.lv'),
('LV','Nodarbinātības valsts aģentūra (NVA)','State Employment Agency','labour_market_test','https://www.nva.gov.lv'),
('SI','Upravne enote','Administrative Units','work_permit','https://www.gov.si'),
('SI','Zavod RS za zaposlovanje (ZRSZ)','Employment Service of Slovenia','labour_market_test','https://www.ess.gov.si'),
('SI','Info točka za tujce','Info Point for Foreigners','info_portal','https://www.infotujci.si'),
('SK','Úrad hraničnej a cudzineckej polície','Bureau of Border and Foreign Police','residence','https://www.minv.sk'),
('SK','Ústredie práce, sociálnych vecí a rodiny (ÚPSVaR)','Central Office of Labour, Social Affairs and Family','labour_market_test','https://www.upsvr.gov.sk')
on conflict (country_iso2,name_en,role) do update set name_local=excluded.name_local, website=excluded.website;

-- ---------- practice areas ----------
insert into practice_areas (code,name,description) values
('work_permits','Work permits & labour market tests','Employer-side work authorisation files, quota applications, vacancy registration.'),
('residence_permits','Residence permits & renewals','Temporary/long-term residence, single permits, renewals, change of employer.'),
('eu_blue_card','EU Blue Card / highly skilled','Highly qualified worker routes, salary thresholds, degree recognition.'),
('visa_d','Long-stay (D) visas','Consular D-visa applications and embassy appointments.'),
('appeals_refusals','Refusals, appeals & judicial review','Challenging refused permits/visas, administrative courts.'),
('recruitment_agency_licensing','Recruitment / staffing agency licensing','Licences for placement and temporary-work agencies, cross-border recruitment.'),
('posted_workers','Posted workers & A1','Posting of Workers Directive, A1 social-security certificates, notifications.'),
('employment_law','Employment contracts & labour law','Contracts, wages, working time, terminations for foreign staff.'),
('labour_inspection_defence','Labour inspection defence','Inspections, fines, illegal-employment allegations.'),
('worker_rights','Worker rights & disputes','Representing workers in wage, accommodation or exploitation disputes.'),
('family_reunification','Family reunification','Spouse/children residence for permit holders.'),
('qualification_recognition','Recognition of qualifications','Diploma/trade recognition, regulated professions.'),
('document_legalisation','Documents, apostille & translations','Legalisation, apostille, sworn translations, criminal-record checks.'),
('corporate_immigration','Corporate immigration compliance','Employer registration, sponsor duties, audits, ICT.'),
('long_term_citizenship','Long-term residence & citizenship','EU long-term resident status, naturalisation.')
on conflict (code) do update set name=excluded.name, description=excluded.description;

-- ---------- work routes (priority markets) ----------
insert into work_routes (code,country_iso2,name,local_term,category,quota_based,labour_market_test,description) values
-- Romania
('RO-PERMANENT','RO','Permanent worker','lucrător permanent','skilled',true,true,'Work authorisation from IGI requested by the employer, then long-stay D/AM visa, then residence permit for work.'),
('RO-SEASONAL','RO','Seasonal worker','lucrător sezonier','seasonal',true,true,'Seasonal work authorisation, limited months per year.'),
('RO-POSTED','RO','Posted worker','lucrător detașat','posted',true,false,'Worker posted to Romania by a foreign employer.'),
('RO-TRAINEE','RO','Trainee','lucrător stagiar','skilled',true,null,'Traineeship work authorisation.'),
('RO-ICT','RO','Intra-corporate transferee','transfer intra-corporativ','ict',false,false,'ICT Directive route.'),
('RO-BLUECARD','RO','EU Blue Card','Cartea albastră a UE','highly_skilled',false,null,'Highly qualified employment.'),
('RO-FAMILY','RO','Family reunification','reîntregirea familiei','family',false,false,'Family members of permit holders.'),
-- Bulgaria
('BG-SINGLE','BG','Single permit (residence + work)','единно разрешение за пребиваване и работа','skilled',false,true,'Employer applies to Employment Agency; Migration Directorate issues the permit.'),
('BG-SEASONAL','BG','Seasonal work','сезонна заетост','seasonal',false,true,'Short seasonal registration or seasonal work permit.'),
('BG-BLUECARD','BG','EU Blue Card','синя карта на ЕС','highly_skilled',false,null,'Highly qualified employment.'),
('BG-ICT','BG','Intra-corporate transferee','вътрешнокорпоративен трансфер','ict',false,false,'ICT Directive route.'),
('BG-FAMILY','BG','Family reunification','събиране на семейство','family',false,false,null),
-- North Macedonia
('MK-WORK-PERMIT','MK','Work permit for employment','работна дозвола за вработување','skilled',true,true,'Issued by the Employment Service Agency within the annual quota.'),
('MK-SEASONAL','MK','Seasonal work permit','работна дозвола за сезонска работа','seasonal',true,true,null),
('MK-POSTED','MK','Posted / assigned worker','упатени работници','posted',true,false,null),
('MK-TEMP-RES','MK','Temporary residence for work','привремен престој заради работа','skilled',false,false,'Residence permit from the Ministry of Interior linked to the work permit.'),
-- Bosnia & Herzegovina
('BA-WORK-PERMIT','BA','Work permit','radna dozvola','skilled',true,true,'Issued by the entity/Brčko employment service within the annual quota set at state level.'),
('BA-TEMP-RES','BA','Temporary residence for work','privremeni boravak po osnovu rada','skilled',false,false,'Approved by the Service for Foreigners'' Affairs.'),
('BA-FAMILY','BA','Family reunification','spajanje porodice','family',false,false,null),
-- Lithuania
('LT-TRP-WORK','LT','Temporary residence permit for work','leidimas laikinai gyventi (darbas)','skilled',false,true,'Via MIGRIS; Employment Service decision unless on the shortage list.'),
('LT-WORK-PERMIT','LT','Work permit','leidimas dirbti','skilled',false,true,null),
('LT-D-VISA','LT','National D visa for work','nacionalinė viza (D)','skilled',false,true,null),
('LT-BLUECARD','LT','EU Blue Card','ES mėlynoji kortelė','highly_skilled',false,null,null),
('LT-SEASONAL','LT','Seasonal work','sezoninis darbas','seasonal',false,true,null),
('LT-ICT','LT','Intra-corporate transferee','perkeltas įmonės viduje','ict',false,false,null),
-- Latvia
('LV-RP-WORK','LV','Residence permit for employment','uzturēšanās atļauja nodarbinātībai','skilled',false,true,'Vacancy registered with NVA first; employer invitation approved by PMLP.'),
('LV-WORK-VISA','LV','Long-stay visa with work rights','ilgtermiņa vīza (D) ar tiesībām strādāt','skilled',false,true,null),
('LV-BLUECARD','LV','EU Blue Card','ES zilā karte','highly_skilled',false,null,null),
('LV-SEASONAL','LV','Seasonal work','sezonas darbs','seasonal',false,true,null),
-- Slovenia
('SI-SINGLE','SI','Single permit for residence and work','enotno dovoljenje za prebivanje in delo','skilled',false,true,'Issued by the administrative unit with ESS consent.'),
('SI-BLUECARD','SI','EU Blue Card','modra karta EU','highly_skilled',false,null,null),
('SI-SEASONAL','SI','Seasonal work','sezonsko delo','seasonal',false,true,null),
('SI-POSTED','SI','Posted worker','napotitev na delo','posted',false,false,null),
('SI-ICT','SI','Intra-corporate transferee','premestitev znotraj gospodarske družbe','ict',false,false,null),
-- Slovakia
('SK-TRP-EMPLOY','SK','Temporary residence for employment (single permit)','prechodný pobyt na účel zamestnania','skilled',false,true,'Labour office confirmation of vacancy; reduced test for shortage occupations.'),
('SK-BLUECARD','SK','EU Blue Card','modrá karta EÚ','highly_skilled',false,null,null),
('SK-SEASONAL','SK','Seasonal employment','sezónne zamestnanie','seasonal',false,true,null),
('SK-ICT','SK','Intra-corporate transferee','vnútropodnikový presun','ict',false,false,null)
on conflict (code) do update set name=excluded.name, local_term=excluded.local_term, category=excluded.category,
  quota_based=excluded.quota_based, labour_market_test=excluded.labour_market_test, description=excluded.description;
