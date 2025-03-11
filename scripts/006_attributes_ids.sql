/*
 * Translation and cleaning of FFIEC Institution Identifers
 * 
 * DESCRIPTION: 
 * There are many possible identifers for an institutuion, rssd_id is the primary key Institution identification.
 * 
 * DEPENDENCIES:
 * - loading of FFIEC attributes
 * - execution of tables.sql
 * - execution of tmp_tables.sql
 * - setting search_path = 'transformations'
 *
 * */
set
	search_path = 'transformations';

insert into
	tmp_ids (
		rssd_id,
		tin,
		lei,
		prim_aba_num,
		fdic_cert_id,
		ncua_id,
		thrift_hc_id,
		thrift_id,
		cusip_id,
		occ_id
	)
select
	id_rssd,
	cast(id_tax as varchar(15)),
	id_lei,
	id_aba_prim,
	id_fdic_cert,
	id_ncua,
	id_thrift_hc,
	id_thrift,
	id_cusip,
	id_occ
from
	tmp_attributes att;

/*
 * In applicable values or when a value is not known is reported as 0.
 * These values are being set to null for exclusion in lookups and indexing if indexes are planed to be added later.
 * 
 * */
update
	tmp_ids
set
	tin = null
where
	tin = '0';

update
	tmp_ids
set
	prim_aba_num = null
where
	prim_aba_num = '0';

update
	tmp_ids
set
	lei = null
where
	lei = '0';

update
	tmp_ids
set
	fdic_cert_id = null
where
	fdic_cert_id = 0;

update
	tmp_ids
set
	ncua_id = null
where
	ncua_id = 0;

update
	tmp_ids
set
	thrift_hc_id = null
where
	thrift_hc_id = '0';

update
	tmp_ids
set
	thrift_id = null
where
	thrift_id = 0;

update
	tmp_ids
set
	cusip_id = null
where
	cusip_id = '0';

update
	tmp_ids
set
	occ_id = null
where
	occ_id = '0';