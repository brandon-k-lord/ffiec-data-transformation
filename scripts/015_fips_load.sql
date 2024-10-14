/*
 * FIPS Codes
 * 
 * DESCRIPTION: 
 * Not all location information is reported in FFIEC data as most is reported in FIPS codes
 * 
 * DEPENDENCIES:
 * - loading of place, country, state, and country codes
 * - execution of tables.sql
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';
commit;


/*
 * I doubt this information will be changed but updates are published every few year as territories grow.
 * */


insert into state_cds ("name", abbr, fips, ns)
select state_name, state, lpad(cast(statefp as varchar),2,'0'), lpad(cast(statens as varchar),8,'0')
from tmp_state_codes
on conflict (fips)
do update 
set
"name" = excluded."name",
abbr = excluded.abbr,
ns = excluded.ns
;


/*
 * County Codes
 * 
 * data provided was by place code, to normalize we had to assign a unique key and remove duplicates for nomalization
 * 
 * */


alter table tmp_county_codes add column "uuid" uuid default gen_random_uuid();


with duplicates as (
select uuid, row_number() over (partition by countyfp order by countyfp) rw from tmp_county_codes)
delete from tmp_county_codes
where uuid in (select uuid from duplicates where rw >1);


insert into county_cds (state_fp, fips, "name")
select lpad(cast(statefp as varchar),2,'0'), lpad(cast(countyfp as varchar),3,'0'), countyname 
from tmp_county_codes 
on conflict (fips)
do update 
set
state_fp = excluded.state_fp,
"name" = excluded."name";

 
-- dirty data
delete from tmp_country_codes where country = 'Curacao 36188';
update tmp_country_codes set country = trim(country);


insert into country_cds ("name", cd)
select country, code
from tmp_country_codes
on conflict (cd)
do update 
set
"name" = excluded."name"
;

