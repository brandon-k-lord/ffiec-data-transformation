/*
 * FFIEC Relationships Load
 * 
 * DESCRIPTION: 
 * This file specifically includes scripts for attribute codes.
 * 
 * DEPENDENCIES:
 * - relationships.sql
 * - set search_path = 'transformations';
 * - deleting data from inst_relationships
 *
 * ASSUMPTIONS:
 * - assumes we will always replace all data in relationships table
 * - there is not enough data to assume feasibly otherwise
 * */


set search_path = 'transformations';


delete from inst_relationships;


insert into inst_relationships(
	parent_rssd_id,
	child_rssd_id,
	"start_date",
	end_date,
	rel_est_date,
	equity,
	equity_ind,
	equity_ind_cd,
	other_basis_ind,
	other_basis_ind_cd,
	other,
	creation_reason,
	creation_reason_cd,
	termination_reason,
	termination_reason_cd,
	merchant_banking_cost,
	financial_consol_ind,
	financial_consol_ind_cd,
	reg_k_inv,
	reg_k_inv_cd,
	reln_lvl)
select 
	parent_rssd_id,
	child_rssd_id,
	"start_date",
	end_date,
	rel_est_date,
	equity,
	equity_ind,
	equity_ind_cd,
	other_basis_ind,
	other_basis_ind_cd,
	other,
	creation_reason,
	creation_reason_cd,
	termination_reason,
	termination_reason_cd,
	merchant_banking_cost,
	financial_consol_ind,
	financial_consol_ind_cd,
	reg_k_inv,
	reg_k_inv_cd,
	reln_lvl
from tmp_inst_relationships
;