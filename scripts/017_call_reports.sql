/*
 * Loading of Call Reports
 * 
 * DESCRIPTION: 
 * Insert from tmp table to production table.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC call report data
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */

set search_path = 'transformations';


-- where statement will not allow for duplication of data since do not have any good validation
insert into call_reports(rssd_id, reporting_pd, tot_assets)
select 
"RSSD9001",
cast(cast("RSSD9999" as varchar(20))as date),
"BHCA2170"
from tmp_bhcf b
where not exists (
select
	1
from
	call_reports c
where
	b."RSSD9001" = c.rssd_id
	and cast(cast(b."RSSD9999"as varchar(20))as date) = c.reporting_pd);
