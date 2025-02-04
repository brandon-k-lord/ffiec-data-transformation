/*
 * FFIEC physical addresses for institutions
 * 
 * DESCRIPTION: 
 * 
 * 
 * DEPENDENCIES:
 * - loading attributes
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 *
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';


select	*
from
	rm_col_whitespace('tmp_attributes',
	array[
	'street_line1',
	'street_line2',
	'zip_cd'
	]);

delete from inst_addresses;

insert into inst_addresses (rssd_id, address_line1, address_line2, city, county_cd, country_cd, zip_cd, zip_plus4)
select
	id_rssd,
	street_line1,
	street_line2,
	city,
	county_cd,
	cntry_cd,
	trim(substring(zip_cd from 0 for 6)),
	trim(substring(zip_cd from 6 for 9))
from
	tmp_attributes; 


update inst_addresses set county_cd = null where county_cd = '0';
update inst_addresses set country_cd = null where country_cd = '0';
update inst_addresses set zip_cd = null where zip_cd = '0';
update inst_addresses set zip_plus4 = null where zip_plus4 = '';
update inst_addresses set address_line1 = null where address_line1 = '0';

