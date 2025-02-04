/*
 * Translation and cleaning of FFIEC FI Indicators
 * 
 * DESCRIPTION: 
 * This file specifically includes scripts for attribute indicators.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC attributes
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';


/* inserting data into a tmp table that mirrors the production target table */


insert
	into
	tmp_inds (rssd_id,
	bnk_holding_co_ind_cd,
	domestic_ind_cd,
	financial_sub_ind_cd,
	fhc_ind_cd,
	fhlbs_mbr_ind_cd,
	int_hc_ind_cd,
	intl_bnk_fac_ind_cd,
	sav_loan_hc_ind_cd,
	fbo_4c9_ind)
select
	id_rssd,
	bhc_ind,
	domestic_ind,
	fncl_sub_holder,
	fhc_ind,
	mbr_fhlbs_ind,
	ihc_ind,
	ibf_ind,
	slhc_ind,
	fbo_4c9_ind
from tmp_attributes;


/*
 * Indicators are reported in integer values.
 * Column to store the descriptive values for the codes were created for analytical and reporting purposes.
 * The following section includes the update statements for this translation.
 * 
 * Note: 0 is defined as inapplicable and this was translated to a null value
 * */


update tmp_inds
set bnk_holding_co_ind =  
case 
	when bnk_holding_co_ind_cd = 1 then 'Entity is a BHC'
	when bnk_holding_co_ind_cd = 2 then 'Entity is not a BHC but it directly or indirectly controls a grandfathered non-bank bank'
end
where bnk_holding_co_ind_cd <> 0 ;


update tmp_inds
set financial_sub_ind =
case 
when financial_sub_ind_cd = 1 then 'Holds one or more financial subsidiaries'
	when financial_sub_ind_cd = 2 then 'Other'
end
where financial_sub_ind_cd <> 0;


update tmp_inds
set fhc_ind =
case 
	when fhc_ind_cd = 1 then 'Entity is an FHC'
	when fhc_ind_cd = 2 then 'Entity is an SLHC which has been designated an FHC'
end
where fhc_ind_cd <> 0;


update tmp_inds
set fhlbs_mbr_ind =
case 
	when fhlbs_mbr_ind_cd = 1 then 'Member'
end
where fhlbs_mbr_ind_cd <> 0;


update tmp_inds
set int_hc_ind =
case 
	when int_hc_ind_cd = 1 then 'Entity is an IHC'
end
where int_hc_ind_cd <> 0;


update tmp_inds
set intl_bnk_fac_ind =
case 
	when intl_bnk_fac_ind_cd = 1 then 'Entity operates an IBF'
end
where intl_bnk_fac_ind_cd <> 0;


update tmp_inds
set sav_loan_hc_ind =
case 
	when sav_loan_hc_ind_cd = 1 then 'Entity is a savings and loan holding company'
end
where sav_loan_hc_ind_cd <> 0;
