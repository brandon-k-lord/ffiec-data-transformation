/*
 * Translation and cleaning of FFIEC Attributes
 * 
 * DESCRIPTION: 
 * This file specifically includes scripts for attribute codes.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC attributes
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - execution of functions.sql
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';


/* 
 * Removing whitespace that is most likely the result of forced with columns with the char in the data source.
 * 
 * Since there are several column in this state, a reusable function that will dynamicall do this on loop was implemented.
 * 
 * Address fields were intentionally excluded from the rm_col_whitespace cleaning to ensure no dependencies exists between this file and the loading of addresses
 *  
 * */


select	*
from
	rm_col_whitespace('tmp_attributes',
	array['nm_short','nm_lgl','act_prim_cd']);


/* inserting into a tmp table that mirrors the production table */


insert
	into
	tmp_inst (rssd_id,
	"name",
	legal_name,
	primary_naics,
	entity_type_abbr,
	website_url,
	fiscal_year_end,
	rssd_id_hd_off)
select 
	id_rssd,
	nm_short,
	nm_lgl,
	act_prim_cd,
	entity_type,
	url,
    cast(fisc_yrend_mmdd as varchar(10)),
	id_rssd_hd_off
from tmp_attributes att;


/*
 * In applicable values or when a value is not known is reported as 0.
 * These values are being set to null for exclusion in lookups and indexing if indexes are planed to be added later.
 * Only applicable conlumns to this script file was handled here.
 * 
 * */


update tmp_inst set website_url = null where website_url = '0';
update tmp_inst set primary_naics = null where primary_naics = '0';
update tmp_inst set rssd_id_hd_off = null where rssd_id_hd_off = 0;
update tmp_inst set fiscal_year_end = null where fiscal_year_end = '0';


update tmp_inst
set fiscal_year_end = lpad(fiscal_year_end,4,'0')
where length(fiscal_year_end) <4;


update tmp_inst 
set entity_type =
case 
	when entity_type_abbr = 'AGB' then 	'Agreement Corporation - Banking'
	when entity_type_abbr = 'AGI' then 	'Agreement Corporation - Investment'
	when entity_type_abbr = 'BHC' then 	'Bank Holding Company'
	when entity_type_abbr = 'CPB' then 	'Cooperative Bank'
	when entity_type_abbr = 'CSA' then 	'Covered Savings Institution'
	when entity_type_abbr = 'DBR' then 	'Domestic Branch of a Domestic Bank'
	when entity_type_abbr = 'DEO' then 	'Domestic Entity Other'
	when entity_type_abbr = 'DPS' then 	'Data Processing Servicer'
	when entity_type_abbr = 'EBR' then 	'Edge Corporation - Domestic Branch'
	when entity_type_abbr = 'EDB' then 	'Edge Corporation - Banking'
	when entity_type_abbr = 'EDI' then 	'Edge Corporation - Investment'
	when entity_type_abbr = 'FBH' then 	'Foreign Banking Organization as a BHC'
	when entity_type_abbr = 'FBK' then 	'Foreign Bank'
	when entity_type_abbr = 'FBO' then 	'Foreign Banking Organization'
	when entity_type_abbr = 'FCU' then 	'Federal Credit Union'
	when entity_type_abbr = 'FEO' then 	'Foreign Entity Other'
	when entity_type_abbr = 'FHD' then 	'Financial Holding Company / BHC'
	when entity_type_abbr = 'FHF' then 	'Financial Holding Company / FBO'
	when entity_type_abbr = 'FNC' then 	'Finance Company'
	when entity_type_abbr = 'FSB' then 	'Federal Savings Bank'
	when entity_type_abbr = 'IBK' then 	'International Bank of a U.S. Depository - Edge or Trust Co.'
	when entity_type_abbr = 'IBR' then 	'Foreign Branch of a U.S. Bank'
	when entity_type_abbr = 'IHC' then 	'Intermediate Holding Company'
	when entity_type_abbr = 'IFB' then 	'Insured Federal Branch of an FBO'
	when entity_type_abbr = 'INB' then 	'International Non-bank Subs of Domestic Entities'
	when entity_type_abbr = 'ISB' then 	'Insured State Branch of an FBO'
	when entity_type_abbr = 'MTC' then 	'Non-deposit Trust Company - Member'
	when entity_type_abbr = 'NAT' then 	'National Bank'
	when entity_type_abbr = 'NMB' then 	'Non-member Bank'
	when entity_type_abbr = 'NTC' then 	'Non-deposit Trust Company - Non-member'
	when entity_type_abbr = 'NYI' then 	'New York Investment Company'
	when entity_type_abbr = 'PST' then 	'Non-U.S. Branch managed by a U.S. Branch/Agency of a Foreign Bank for 002’s reporting'
	when entity_type_abbr = 'REP' then 	'Representative Office'
	when entity_type_abbr = 'SAL' then 	'Savings & Loan Association'
	when entity_type_abbr = 'SBD' then 	'Securities Broker / Dealer'
	when entity_type_abbr = 'SCU' then 	'State Credit Union'
	when entity_type_abbr = 'SLHC' then  'Savings and Loan Holding Company'
	when entity_type_abbr = 'SMB' then 	'State Member Bank'
	when entity_type_abbr = 'SSB' then 	'State Savings Bank'
	when entity_type_abbr = 'TWG' then 	'Non-U.S. Branch managed by a U.S. Branch/Agency of a Foreign Bank'
	when entity_type_abbr = 'UFA' then 	'Uninsured Federal Agency of an FBO'
	when entity_type_abbr = 'UFB' then 	'Uninsured Federal Branch of an FBO'
	when entity_type_abbr = 'USA' then 	'Uninsured State Agency of an FBO'
	when entity_type_abbr = 'USB' then 	'Uninsured State Branch of an FBO'
end;