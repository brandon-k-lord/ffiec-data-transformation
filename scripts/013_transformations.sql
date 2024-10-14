/*
 * Translation and cleaning of FFIEC reported Transformations
 * 
 * DESCRIPTION: 
 * This file specifically includes scripts for FFIEC reported transformations.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC transformations
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';


insert into tmp_inst_transformations(
rssd_id_predecessor,
rssd_id_successor,
transformation_date,
transformation_cd,
acct_method_cd
)
select 
id_rssd_predecessor,
id_rssd_successor,
cast(d_dt_trans as date),
trnsfm_cd,
acct_method
from tmp_transformations;


update tmp_inst_transformations
set transformation = 
case 
	when transformation_cd = 1 then 'Charter Discontinued'
	when transformation_cd = 2 then 'Split'
	when transformation_cd = 3 then 'Sale of Assets'
	when transformation_cd = 9 then 'Charter Retained'
	when transformation_cd = 50 then 'Failure'
end;


update tmp_inst_transformations
set acct_method = 
case 
	when acct_method_cd = 1 then 'Pooling of interests or entities under common control.'
	when acct_method_cd = 2 then 'Purchase/Acquisition'
end
where acct_method_cd <> 0;

insert into inst_transformations(
rssd_id_predecessor,
rssd_id_successor,
transformation_date,
transformation,
transformation_cd,
acct_method,
acct_method_cd
)
select
rssd_id_predecessor,
rssd_id_successor,
transformation_date,
transformation,
transformation_cd,
acct_method,
acct_method_cd
from tmp_inst_transformations;
