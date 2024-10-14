/*
 * Loading of cleaned data
 * 
 * DESCRIPTION: 
 * This file concentrates on the load scripts, no further transformations happend here.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC attributes
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - execution of attributes_codes.sql
 * - execution of attributes_dates.sql
 * - execution of attributes_ids.sql
 * - execution of attributes_inds.sql
 * - execution of attributes_inst.sql
 * - setting search_path = 'transformations'
 *
 * */


/* 
 * insert / update on conflict institution data
 * 
 * assumes that table will never be dropped and there will never be duplicate rssd_id
 * 
 * other tables dependent upon this table join on id and rssd_id
 * 
*/

commit;
set search_path = 'transformations';

insert
	into
	transformations.institutions ( rssd_id,
	"name",
	legal_name,
	primary_naics,
	entity_type_abbr,
	website_url,
	entity_type,
	fiscal_year_end,
	rssd_id_hd_off)
select 
	rssd_id,
	"name",
	legal_name,
	primary_naics,
	entity_type_abbr,
	website_url,
	entity_type,
	fiscal_year_end,
	rssd_id_hd_off
from transformations.tmp_inst
on conflict (rssd_id)
do update 
set 
	"name" = excluded."name",
	legal_name = excluded.legal_name,
	primary_naics = excluded.primary_naics,
	entity_type_abbr = excluded.entity_type_abbr,
	website_url = excluded.website_url,
	entity_type = excluded.entity_type,
	fiscal_year_end = excluded.fiscal_year_end,
	rssd_id_hd_off = excluded.rssd_id_hd_off
;


/* 
 * insert / update on conflict institution ids
 * 
 * assumes that table will never be dropped and there will never be duplicate rssd_id
 * 
*/


insert
	into
	transformations.inst_ids ( 
	institution_id,
	rssd_id,
	tin,
	lei,
	prim_aba_num,
	fdic_cert_id,
	ncua_id,
	thrift_hc_id,
	thrift_id,
	cusip_id,
	occ_id)
select 
	i.id,
	ti.rssd_id,
	ti.tin,
	ti.lei,
	ti.prim_aba_num,
	ti.fdic_cert_id,
	ti.ncua_id,
	ti.thrift_hc_id,
	ti.thrift_id,
	ti.cusip_id,
	ti.occ_id
from transformations.tmp_ids ti
join transformations.institutions i on ti.rssd_id = i.rssd_id 
on conflict (rssd_id)
do update 
set 
	tin = excluded.tin,
	lei = excluded.lei,
	prim_aba_num = excluded.prim_aba_num,
	fdic_cert_id = excluded.fdic_cert_id,
	ncua_id = excluded.ncua_id,
	thrift_hc_id = excluded.thrift_hc_id,
	thrift_id = excluded.thrift_id,
	cusip_id = excluded.cusip_id,
	occ_id = excluded.occ_id;


/* 
 * insert / update on conflict institution dates
 * 
 * assumes that table will never be dropped and there will never be duplicate rssd_id
 * 
*/


insert
	into
	transformations.inst_attr_dates(institution_id,
	rssd_id,
	start_date,
	end_date,
	open_date,
	commencement_date,
	termination_date,
	insured_date)
select
	i.id,
	td.rssd_id,
	td.start_date,
	td.end_date,
	td.open_date,
	td.commencement_date,
	td.termination_date,
	td.insured_date
from tmp_dates td
join institutions i on td.rssd_id  = i.rssd_id
on conflict (rssd_id)
do update 
set 
	start_date = excluded.start_date,
	end_date = excluded.end_date,
	open_date = excluded.open_date,
	commencement_date = excluded.commencement_date,
	termination_date = excluded.termination_date,
	insured_date = excluded.insured_date;


/* insert / update on conflict institution indicators */


insert
	into
	inst_attr_indicators(institution_id,
	rssd_id,
	bnk_holding_co_ind_cd,
	bnk_holding_co_ind,
	domestic_ind_cd,
	fbo_4c9_ind,
	financial_sub_ind,
	financial_sub_ind_cd,
	fhc_ind,
	fhc_ind_cd,
	fhlbs_mbr_ind,
	fhlbs_mbr_ind_cd,
	int_hc_ind,
	int_hc_ind_cd,
	intl_bnk_fac_ind,
	intl_bnk_fac_ind_cd,
	sav_loan_hc_ind,
	sav_loan_hc_ind_cd)
select 
	i.id,
	ti.rssd_id,
	ti.bnk_holding_co_ind_cd,
	ti.bnk_holding_co_ind,
	ti.domestic_ind_cd,
	ti.fbo_4c9_ind,
	ti.financial_sub_ind,
	ti.financial_sub_ind_cd,
	ti.fhc_ind,
	ti.fhc_ind_cd,
	ti.fhlbs_mbr_ind,
	ti.fhlbs_mbr_ind_cd,
	ti.int_hc_ind,
	ti.int_hc_ind_cd,
	ti.intl_bnk_fac_ind,
	ti.intl_bnk_fac_ind_cd,
	ti.sav_loan_hc_ind,
	ti.sav_loan_hc_ind_cd
from tmp_inds ti 
join institutions i on ti.rssd_id = i.rssd_id 
on conflict (rssd_id)
do update 
set 
	bnk_holding_co_ind_cd = excluded.bnk_holding_co_ind_cd,
	bnk_holding_co_ind = excluded.bnk_holding_co_ind,
	domestic_ind_cd = excluded.domestic_ind_cd,
	fbo_4c9_ind = excluded.fbo_4c9_ind,
	financial_sub_ind = excluded.financial_sub_ind,
	financial_sub_ind_cd = excluded.financial_sub_ind_cd,
	fhc_ind = excluded.fhc_ind,
	fhc_ind_cd = excluded.fhc_ind_cd,
	fhlbs_mbr_ind = excluded.fhlbs_mbr_ind,
	fhlbs_mbr_ind_cd = excluded.fhlbs_mbr_ind_cd,
	int_hc_ind = excluded.int_hc_ind,
	int_hc_ind_cd = excluded.int_hc_ind_cd,
	intl_bnk_fac_ind = excluded.intl_bnk_fac_ind,
	intl_bnk_fac_ind_cd = excluded.intl_bnk_fac_ind_cd,
	sav_loan_hc_ind = excluded.sav_loan_hc_ind,
	sav_loan_hc_ind_cd = excluded.sav_loan_hc_ind_cd;


/* insert / update on conflict institution cds */


insert
	into
	inst_attr_cds(institution_id,
	rssd_id,
	auth_charter,
	auth_charter_cd,
	bank_type_analysis,
	bank_type_analysis_cd,
	conservatorship,
	conservatorship_cd,
	broad_reg,
	broad_reg_cd,
	charter_type,
	charter_type_cd,
	est_type,
	est_type_cd,
	financial_sub_holder,
	financial_sub_holder_cd,
	func_reg,
	func_reg_cd,
	mjr_mnrty_owned,
	mjr_mnrty_owned_cd,
	org_type,
	org_type_cd,
	primary_insurer,
	primary_insurer_cd,
	primary_reg,
	primary_reg_cd,
	sav_loan_hc_type,
	sav_loan_hc_type_cd,
	sec_reporting_status,
	sec_reporting_status_cd,
	termination_reason,
	termination_reason_cd)
select
i.id,
cds.rssd_id,
cds.auth_charter,
cds.auth_charter_cd,
cds.bank_type_analysis,
cds.bank_type_analysis_cd,
cds.conservatorship,
cds.conservatorship_cd,
cds.broad_reg,
cds.broad_reg_cd,
cds.charter_type,
cds.charter_type_cd,
cds.est_type,
cds.est_type_cd,
cds.financial_sub_holder,
cds.financial_sub_holder_cd,
cds.func_reg,
cds.func_reg_cd,
cds.mjr_mnrty_owned,
cds.mjr_mnrty_owned_cd,
cds.org_type,
cds.org_type_cd,
cds.primary_insurer,
cds.primary_insurer_cd,
cds.primary_reg, 
cds.primary_reg_cd,
cds.sav_loan_hc_type,
cds.sav_loan_hc_type_cd,
cds.sec_reporting_status,
cds.sec_reporting_status_cd,
cds.termination_reason,
cds.termination_reason_cd
from transformations.tmp_cds cds
join transformations.institutions i on cds.rssd_id = i.rssd_id
on conflict (rssd_id)
do update 
set 
	auth_charter = excluded.auth_charter,
	auth_charter_cd = excluded.auth_charter_cd,
	bank_type_analysis = excluded.bank_type_analysis,
	bank_type_analysis_cd = excluded.bank_type_analysis_cd,
	conservatorship = excluded.conservatorship,
	conservatorship_cd = excluded.conservatorship_cd,
	broad_reg = excluded.broad_reg,
	broad_reg_cd = excluded.broad_reg_cd,
	charter_type = excluded.charter_type,
	charter_type_cd = excluded.charter_type_cd,
	est_type = excluded.est_type,
	est_type_cd = excluded.est_type_cd,
	financial_sub_holder = excluded.financial_sub_holder,
	financial_sub_holder_cd = excluded.financial_sub_holder_cd,
	func_reg = excluded.func_reg,
	func_reg_cd = excluded.func_reg_cd,
	mjr_mnrty_owned = excluded.mjr_mnrty_owned,
	mjr_mnrty_owned_cd = excluded.mjr_mnrty_owned_cd,
	org_type = excluded.org_type,
	org_type_cd = excluded.org_type_cd,
	primary_insurer = excluded.primary_insurer,
	primary_insurer_cd = excluded.primary_insurer_cd,
	primary_reg = excluded.primary_reg, 
	primary_reg_cd = excluded.primary_reg_cd,
	sav_loan_hc_type = excluded.sav_loan_hc_type,
	sav_loan_hc_type_cd = excluded.sav_loan_hc_type_cd,
	sec_reporting_status = excluded.sec_reporting_status,
	sec_reporting_status_cd = excluded.sec_reporting_status_cd,
	termination_reason = excluded.termination_reason,
	termination_reason_cd = excluded.termination_reason_cd;
