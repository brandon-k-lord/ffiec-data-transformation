/*
 * Translation and cleaning of FFIEC Institution Dates
 * 
 * DESCRIPTION: 
 * Dates are descriptive of the institution's lifecycle.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC attributes
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';


/* Setting inapplicable values to null */


-- casting an int to a date requires casting to a string first, but must be in a valid date format yyyymmdd
update tmp_attributes set dt_insur = null where dt_insur = 0;
update tmp_attributes set dt_exist_term = null where dt_exist_term = 0;
update tmp_attributes set dt_exist_cmnc = null where dt_exist_cmnc = 0;


insert into tmp_dates (rssd_id, start_date, end_date,open_date,commencement_date,termination_date,insured_date)
select  
id_rssd,
cast(d_dt_start as date),
cast(d_dt_end as date),
cast(d_dt_open as date),
cast(cast(dt_exist_cmnc as varchar(10)) as date),
cast(cast(dt_exist_term as varchar(10)) as date),
cast(cast(dt_insur as varchar(10)) as date)
from tmp_attributes;
