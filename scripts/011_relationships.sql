/*
 * FFIEC Relationships
 * 
 * DESCRIPTION: 
 * .
 * 
 * DEPENDENCIES:
 * - loading of FFIEC relationships csv
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';


insert into tmp_inst_relationships (
	parent_rssd_id,
	child_rssd_id,
	"start_date",
	end_date,
	rel_est_date,
	equity,
	equity_ind_cd,
	other_basis_ind_cd,
	other,
	creation_reason_cd,
	termination_reason_cd,
	merchant_banking_cost,
	financial_consol_ind_cd,
	reg_k_inv_cd,
	reln_lvl
	)
select 
	id_rssd_parent,
	id_rssd_offspring,
	cast(d_dt_start as date),
	cast(d_dt_end as date),
	cast(d_dt_reln_est as date),
	(pct_equity/100),
	equity_ind,
	other_basis_ind,
	(pct_other/100),
	reason_row_crtd,
	reason_term_reln,
	mb_cost,
	fc_ind,
	regk_inv,
	reln_lvl
from tmp_relationships; 


/*
 * Codes are reported in integer values.
 * Column to store the descriptive values for the codes were created for analytical and reporting purposes.
 * The following section includes the update statements for this translation.
 * 
  * */


update tmp_inst_relationships
set equity_ind = 
case 
	when equity_ind_cd = 1 then 'Ownership / control is in a BHC, SLHC, bank or FBO'
	when equity_ind_cd = 2 then 'Ownership / control is in a non-banking company'
end
where equity_ind_cd <> 0;


update tmp_inst_relationships
set other_basis_ind = 
case 
	when other_basis_ind_cd = 1 then 'Other basis of ownership/control'
	when other_basis_ind_cd = 2 then 'Non-voting equity'
	when other_basis_ind_cd = 3 then 'Voting securities in a merchant banking or insurance company investment'
	when other_basis_ind_cd = 4 then 'Subordinated debt'
	when other_basis_ind_cd = 5 then 'Limited partnership'
	when other_basis_ind_cd = 6 then 'Subordinated debt and non-voting equity'
	when other_basis_ind_cd = 7 then 'Subordinated debt and limited partnership'
	when other_basis_ind_cd = 8 then 'Assets'
	when other_basis_ind_cd = 9 then 'Total equity in a merchant banking or insurance company investment'
end
where other_basis_ind_cd <> 0;


update tmp_inst_relationships
set creation_reason = 
case 
	when creation_reason_cd = 1 then 'Initial relationship record'
	when creation_reason_cd = 2 then 'Increase/Decrease in voting rights including non-participation in capital increase'
	when creation_reason_cd = 3 then 'Reestablishment of a relationship'
	when creation_reason_cd = 4 then 'Change in basis for relationship or change in relationship'
	when creation_reason_cd = 5 then 'Change in Control Indicator'
	when creation_reason_cd = 6 then 'Change in Regulatory Indicator'
	when creation_reason_cd = 7 then 'Change in Regulatory Indicator along with reasons 2 and/or 4 above'
	when creation_reason_cd = 8 then 'Other'
end;


update tmp_inst_relationships
set termination_reason =
case
	when termination_reason_cd = 1 then 'Termination of relationship between Parent and Offspring for reasons other than 2 through 6 with no remaining basis for a relationship'
	when termination_reason_cd = 2 then 'Parent terminates relationship with Offspring by selling or transferring all the control it (Parent) has over Offspring'
	when termination_reason_cd = 3 then 'Relationship between Parent and Offspring is terminated because Offspring is liquidated or merged.'
	when termination_reason_cd = 4 then 'Termination of regulation of relationship between Parent and Offspring because control criteria of Offspring fell below regulatory reportable level.'
	when termination_reason_cd = 5 then 'Termination of regulation of relationship between Parent and Offspring because Parent ceased to be controlled or reportable.'
	when termination_reason_cd = 6 then 'Termination of regulation of relationship between Parent and Offspring because of change to regulatory reporting criteria.'
end;


update tmp_inst_relationships
set financial_consol_ind = 
case 
	when financial_consol_ind_cd = 1 then 'Yes'
	when financial_consol_ind_cd = 2 then 'No'
end;


update tmp_inst_relationships
set reg_k_inv = 
case 
	when reg_k_inv_cd = 1 then 'Portfolio Investment'
	when reg_k_inv_cd = 2  then 'Joint Venture'
	when reg_k_inv_cd = 3  then 'Subsidiary'
end
where reg_k_inv_cd <> 0;


