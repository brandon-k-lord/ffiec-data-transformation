/*
 * NAICS
 * 
 * DESCRIPTION: 
 * - North American Industry Classification System
 * - The numerical identifier is recored in the FFIEC data set, for further analysis, we need to know their classification.
 * 
 * DEPENDENCIES:
  * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */

set search_path = 'transformations';


-- the sequence is designed to order list, strings do not follow sequential ordering rules
alter table tmp_naics alter column sequence type int;

-- data set included an empty row
delete from tmp_naics where sequence is null;


insert into naics 
select * from tmp_naics;
