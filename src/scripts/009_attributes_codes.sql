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
 * - setting search_path = 'transformations'
 *
 * */

set search_path = 'transformations';


/* inserting into a tmp table that mirrors the production table */


insert into tmp_cds (
	rssd_id, 
	auth_charter_cd,
	bank_type_analysis_cd,
	conservatorship_cd,
	broad_reg_cd, 
	charter_type_cd, 
	est_type_cd, 
	financial_sub_holder_cd, 
	func_reg_cd, 
	mjr_mnrty_owned_cd,
	org_type_cd, 
	primary_insurer_cd, 
	primary_reg_cd, 
	sav_loan_hc_type_cd, 
	sec_reporting_status_cd, 
	termination_reason_cd )
select 
	id_rssd,
	chtr_auth_cd,
	bnk_type_analys_cd,
	cnsrvtr_cd,
	broad_reg_cd,
	chtr_type_cd,
	est_type_cd,
	fncl_sub_holder,
	func_reg,
	mjr_own_mnrty,
	org_type_cd,
	insur_pri_cd,
	prim_fed_reg,
	slhc_type_ind,
	sec_rptg_status,
	reason_term_cd
from tmp_attributes;


/*
 * Codes are reported in integer values.
 * Column to store the descriptive values for the codes were created for analytical and reporting purposes.
 * The following section includes the update statements for this translation.
 * 
 * Note: 0 is defined as inapplicable and this was translated to a null value
 * */


update tmp_cds 
set auth_charter = 
case 
	when auth_charter_cd = 1 then 'Federal'
	when auth_charter_cd = 2 then 'State'
end
where auth_charter_cd <> 0;


update tmp_cds
set bank_type_analysis =
case 
	when bank_type_analysis_cd = 1 then 'A bankers bank that is subject to reserve requirements'
	when bank_type_analysis_cd = 2 then 'A bankers bank that is not subject to reserve requirements'
	when bank_type_analysis_cd = 3 then 'Grandfathered non-bank bank'
	when bank_type_analysis_cd = 4 then 'Entity is primarily conducting credit card activities'
	when bank_type_analysis_cd = 5 then 'Wholesale bank (with commercial bank charter)'
	when bank_type_analysis_cd = 6 then 'Standalone Internet Bank (SAIB)'
	when bank_type_analysis_cd = 7 then 'Workout entity'
	when bank_type_analysis_cd = 8 then 'Depository Institution National Bank'
	when bank_type_analysis_cd = 9 then 'Depository trust company'
	when bank_type_analysis_cd = 10 then 'Bridge entity'
	when bank_type_analysis_cd = 11 then 'Banking Edge or Agreement Corporation'
	when bank_type_analysis_cd = 12 then 'Investment Edge or Agreement Corporation'
	when bank_type_analysis_cd = 13 then 'Data processing services'
	when bank_type_analysis_cd = 14 then 'Trust preferred securities subsidiary'
	when bank_type_analysis_cd = 15 then 'Cash management banks'
	when bank_type_analysis_cd = 16 then 'Farm credit system institution'
	when bank_type_analysis_cd = 17 then '10L Election'
	when bank_type_analysis_cd = 18 then 'Grandfathered SLHC'
	when bank_type_analysis_cd = 19 then 'Securities Holding Company'
	when bank_type_analysis_cd = 20 then 'Designated Financial Market Utility'
end
where bank_type_analysis_cd <> 0;


update tmp_cds
set conservatorship = 
case 
	when conservatorship_cd = 1 then 'RTC'
	when conservatorship_cd = 2 then 'OCC'
	when conservatorship_cd = 3 then 'FDIC'
	when conservatorship_cd = 4 then 'STATE'
	when conservatorship_cd = 5 then 'NCUA'
end
where conservatorship_cd <> 0;


update tmp_cds
set broad_reg = 
case 
	when broad_reg_cd = 1 then 'Denotes entities that are defined as banks in the Bank Holding Company Act, as 
amended and implemented in the Federal Reserve''s Regulation Y'
	when broad_reg_cd = 2 then 'Other depository institution'
	when broad_reg_cd = 3 then 'Non-depository institution'
	when broad_reg_cd = 4 then 'Inactive institution'
end
where broad_reg_cd <> 0;


update tmp_cds
set charter_type = 
case
	when charter_type_cd = 110 then 'Government Agency'
	when charter_type_cd = 200 then 'Commercial Bank'
	when charter_type_cd = 250 then 'Non-deposit Trust Company'
	when charter_type_cd = 300 then 'Savings Bank'
	when charter_type_cd = 310 then 'Savings & Loan Association'
	when charter_type_cd = 320 then 'Cooperative Bank'
	when charter_type_cd = 330 then 'Credit Union'
	when charter_type_cd = 340 then 'Industrial Bank'
	when charter_type_cd = 400 then 'Edge or Agreement Corporation'
	when charter_type_cd = 500 then 'Holding Company only, not itself any other charter type'
	when charter_type_cd = 550 then 'Insurance Broker or Agent and/or Insurance Company'
	when charter_type_cd = 610 then 'Employee Stock Ownership Plan/Trust'
	when charter_type_cd = 700 then 'Securities Broker and/or Dealer'
	when charter_type_cd = 710 then 'Utility Company or Electric Power Co-generator'
	when charter_type_cd = 720 then 'Other Non-Depository Institution'
end
where charter_type_cd <> 0;


update tmp_cds 
set financial_sub_holder = 
case
	when financial_sub_holder_cd = 1 then 'Holds one or more financial subsidiaries'
	when financial_sub_holder_cd = 2 then 'Other'
end
where financial_sub_holder_cd <> 0;


update tmp_cds
set est_type = 
case
	when est_type_cd = 1	then 'Headquarters'
	when est_type_cd = 2	then 'Full service branch or regional office of regulatory agency'
	when est_type_cd = 3	then 'Limited service branch'
	when est_type_cd = 5	then 'Agency'
	when est_type_cd = 6	then 'Back office money operation'
	when est_type_cd = 7	then 'Military facility'
	when est_type_cd = 8	then 'Super agency'
	when est_type_cd = 9	then 'Limited super agency'
	when est_type_cd = 11 then 'Check processing center, regional or otherwise'
	when est_type_cd = 12 then 'Other branch or non-independent facility'
	when est_type_cd = 13 then 'Loan production office'
	when est_type_cd = 14 then 'Representative office of a foreign bank'
	when est_type_cd = 15 then 'Non-U.S. branch that is managed or controlled by a U.S. branch or agency of a foreign bank'
	when est_type_cd = 16 then 'Non-U.S. branch that is managed or controlled by more than one U.S. branch or agency of a foreign bank'
	when est_type_cd = 17 then 'Office, division or branch of a non-bank entity'
	when est_type_cd = 18 then 'Trust'
	when est_type_cd = 19 then 'Electronic Banking'
end;


update tmp_cds 
set financial_sub_holder = 
case
	when financial_sub_holder_cd = 1 then 'Holds one or more financial subsidiaries'
	when financial_sub_holder_cd = 2 then 'Other'
end
where financial_sub_holder_cd <> 0;


update tmp_cds
set func_reg = 
case
	when func_reg_cd = 1 then 'SEC/CFTC'
	when func_reg_cd = 2 then 'SEC'
	when func_reg_cd = 3 then 'State Securities Department'
	when func_reg_cd = 4 then 'State Insurance Regulator'
	when func_reg_cd = 5 then 'CFTC'
	when func_reg_cd = 6 then 'Other'
end
where func_reg_cd <> 0;


update tmp_cds
set mjr_mnrty_owned = 
case
	when mjr_mnrty_owned_cd = 1 then 'African American'
	when mjr_mnrty_owned_cd = 5 then 'Caucasian Women'
	when mjr_mnrty_owned_cd = 10 then 'Hispanic'
	when mjr_mnrty_owned_cd = 20 then 'Asian American'
	when mjr_mnrty_owned_cd = 30 then 'Native American'
	when mjr_mnrty_owned_cd = 35 then 'Eskimo'
	when mjr_mnrty_owned_cd = 37 then 'Aleuts'
	when mjr_mnrty_owned_cd = 39 then 'Low Income Credit Union'
	when mjr_mnrty_owned_cd = 99 then 'Other Minorities'
end
where mjr_mnrty_owned_cd <> 0;


update tmp_cds
set org_type = 
case
	when org_type_cd = 1 then 'Corporation'
	when org_type_cd = 2 then 'General Partnership'
	when org_type_cd = 3 then 'Limited Partnership'
	when org_type_cd = 4 then 'Business Trust'
	when org_type_cd = 5 then 'Sole Proprietorship'
	when org_type_cd = 6 then 'Mutual'
	when org_type_cd = 9 then 'Cooperative'
	when org_type_cd = 10 then 'LLP'
	when org_type_cd = 11 then 'LLC/C'
	when org_type_cd = 12 then 'Estate Trust'
	when org_type_cd = 13 then 'Limited Liability Limited Partnership'
	when org_type_cd = 99 then 'Other'
end
where org_type_cd <> 0;


update tmp_cds
set primary_insurer = 
case
	when primary_insurer_cd = 1 then 'FDIC/BIF'
	when primary_insurer_cd = 2 then 'FDIC/SAIF'
	when primary_insurer_cd = 3 then 'NCUSIF'
	when primary_insurer_cd = 4 then 'State'
	when primary_insurer_cd = 5 then 'Other'
	when primary_insurer_cd = 6 then 'FDIC/BIF and FDIC/SAIF'
	when primary_insurer_cd = 7 then 'DIF'
end
where primary_insurer_cd <> 0;


update tmp_cds
set primary_reg = 
case
	when primary_reg_cd = 'FCA' then 'Farm Credit Administration'
	when primary_reg_cd = 'FDIC' then 'Federal Deposit Insurance Corporation'
	when primary_reg_cd = 'FHFA' then 'Federal Housing Finance Agency'
	when primary_reg_cd = 'FRS' then 'Federal Reserve System'
	when primary_reg_cd = 'NCUA' then 'National Credit Union Administration'
	when primary_reg_cd = 'OCC' then 'Office of the Comptroller of the Currency'
	when primary_reg_cd = 'OTS' then 'Office of Thrift Supervision'
end;


update tmp_cds
set sec_reporting_status = 
case
	when sec_reporting_status_cd = 1 then 'Registered with the SEC'
	when sec_reporting_status_cd = 2 then 'Not registered with the SEC'
	when sec_reporting_status_cd = 3 then 'Subject to section 13(a) or 15(d) of the Securities Exchange Act of 1934 and section 404 of the Sarbanes-Oxley Act of 2002'
	when sec_reporting_status_cd = 4 then 'Subject to section 13(a) or 15(d) of the Securities Exchange Act of 1934 and NOT section 404 of the Sarbanes-Oxley Act of 2002'
	when sec_reporting_status_cd = 5 then 'Terminated or suspended its reporting requirements under section 13(a) or 15(d) of the Securities Exchange Act of 1934'
end
where sec_reporting_status_cd <> 0;


update tmp_cds
set termination_reason = 
case
	when termination_reason_cd = 1 then 'Voluntary liquidation'
	when termination_reason_cd = 2 then 'Closure'
	when termination_reason_cd = 3 then 'Entity is either inactive or no longer regulated by the Federal Reserve.'
	when termination_reason_cd = 4 then 'Failure, entity continues to exist'
	when termination_reason_cd = 5 then 'Failure, entity ceases to exist'
end
where termination_reason_cd <> 0;


update tmp_cds 
set sav_loan_hc_type = 
case 
	when sav_loan_hc_type_cd = 1 then 'Entity is a Home Owners Loan Act Mutual Holding Company that holds a savings bank that has made a 10L election to be treated as a thrift'
	when sav_loan_hc_type_cd = 2 then 'Entity is a Home Owners Loan Act Stock Holding Company that holds a savings bank that has made a 10L election to be treated as a thrift'
	when sav_loan_hc_type_cd = 3 then 'Entity is a Mutual Holding Company (non- Home Owners Loan Act) that holds a savings association'
	when sav_loan_hc_type_cd = 4 then 'Entity is a Stock Holding Company (non- Home Owners Loan Act) that holds a savings association'
	when sav_loan_hc_type_cd = 5 then 'Entity is a Trust (family or estate) Holding Company. These entities are registered savings and loan holding companies.'
end
where sav_loan_hc_type_cd <> 0;
