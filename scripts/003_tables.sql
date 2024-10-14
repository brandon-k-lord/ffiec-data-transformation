

create table if not exists transformations.institutions(
id serial primary key,
rssd_id int unique not null,
"name" varchar(255) null,
legal_name varchar(255) null,
entity_type_abbr varchar(10) null,
entity_type varchar(100),
primary_naics varchar(20),
website_url varchar (255),
fiscal_year_end varchar(4),
rssd_id_hd_off int
);


create table if not exists transformations.inst_ids(
id serial primary key,
institution_id int not null,
rssd_id int unique not null,
tin varchar(12) null,
lei varchar(20) null, 
prim_aba_num int null,
fdic_cert_id int null,
ncua_id int null,
thrift_hc_id varchar(20) null,
thrift_id int null,
cusip_id varchar(15) null,
occ_id int null,
foreign key (institution_id) references transformations.institutions(id)
);


create table if not exists transformations.inst_attr_dates(
id serial primary key,
institution_id int not null,
rssd_id int unique not null,
start_date date null,
end_date date null,
open_date date null,
commencement_date date null,
termination_date date null,
insured_date date null,
foreign key (institution_id) references transformations.institutions(id)
);


create table if not exists transformations.inst_attr_indicators(
id serial primary key,
institution_id int unique not null,
rssd_id int unique not null,
bnk_holding_co_ind_cd int null,
bnk_holding_co_ind varchar(100) null,
domestic_ind_cd varchar(10) null,
fbo_4c9_ind int null,
financial_sub_ind varchar(50) null,
financial_sub_ind_cd int null,
fhc_ind varchar(50) null,
fhc_ind_cd int null,
fhlbs_mbr_ind varchar(50) null,
fhlbs_mbr_ind_cd int null,
int_hc_ind varchar(50) null,
int_hc_ind_cd int null,
intl_bnk_fac_ind varchar(50) null,
intl_bnk_fac_ind_cd int null,
sav_loan_hc_ind varchar(50) null,
sav_loan_hc_ind_cd int null,
foreign key (institution_id) references transformations.institutions(id)
);


create table if not exists transformations.inst_attr_cds(
id serial primary key,
institution_id int not null,
rssd_id int unique not null,
auth_charter varchar(50) null,
auth_charter_cd int null,
bank_type_analysis varchar(100) null,
bank_type_analysis_cd int null,
conservatorship varchar(50) null,
conservatorship_cd int null,
broad_reg varchar(255) null,
broad_reg_cd int null,
charter_type varchar(255) null,
charter_type_cd int null,
est_type varchar(255) null,
est_type_cd int,
financial_sub_holder varchar(50) null,
financial_sub_holder_cd int null,
func_reg varchar(50) null,
func_reg_cd int null,
mjr_mnrty_owned varchar(50) null,
mjr_mnrty_owned_cd int null,
org_type varchar(50) null,
org_type_cd int null,
primary_insurer varchar(50) null,
primary_insurer_cd int null,
primary_reg varchar(50), 
primary_reg_cd varchar(10),
sav_loan_hc_type varchar(255) null,
sav_loan_hc_type_cd int null,
sec_reporting_status varchar(255) null,
sec_reporting_status_cd int null,
termination_reason varchar(100) null,
termination_reason_cd int null,
foreign key (institution_id) references transformations.institutions(id)
);


create table if not exists transformations.inst_relationships(
uuid uuid primary key default gen_random_uuid(),
parent_rssd_id int null,
child_rssd_id int null,
start_date date null,
end_date date null,
rel_est_date date null,
equity decimal(5,4) null,
equity_ind varchar(50) null, 
equity_ind_cd int null,
other_basis_ind varchar(100) null,
other_basis_ind_cd int null,
other decimal(5,4) null,
creation_reason varchar(100),
creation_reason_cd int null,
termination_reason varchar(255) null,
termination_reason_cd int null,
merchant_banking_cost decimal(12,4) null,
financial_consol_ind varchar(50) null,
financial_consol_ind_cd int null,
reg_k_inv varchar(50) null,
reg_k_inv_cd int null,
reln_lvl int
);


create table if not exists transformations.inst_transformations(
uuid uuid primary key default gen_random_uuid(),
rssd_id_predecessor int null,
rssd_id_successor int null,
transformation_date date null,
transformation varchar(50) null,
transformation_cd int null,
acct_method varchar(100) null,
acct_method_cd int null
) ;


create table if not exists transformations.inst_addresses(
id serial primary key,
rssd_id int,
address_line1 varchar(255),
address_line2 varchar(255),
city varchar(255),
county_cd varchar(10),
country_cd varchar(10),
zip_cd varchar(5),
zip_plus4 varchar(4)
);


create table if not exists transformations.country_cds(
id serial primary key,
"name" varchar(255),
cd varchar(100) unique not null
) ;


create table if not exists transformations.state_cds(
id serial primary key, 
abbr varchar(2),
"name" varchar(255),
fips varchar(2) unique not null,
ns varchar(8)
);


create table if not exists transformations.county_cds(
id serial primary key, 
state_fp varchar(2),
fips varchar(3) unique not null,
"name" varchar(255) 
);


create table if not exists transformations.naics (
"sequence" int primary key,
cd varchar(20),
title varchar(255)
) ;


create table if not exists transformations.call_reports(
id serial primary key,
rssd_id int null,
reporting_pd date null,
tot_assets decimal (20,4)
);

