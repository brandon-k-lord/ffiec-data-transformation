IMPORT = "imports"
SCRIPTS = "scripts"
TABLE_SCHEMA = "transformations"


""" 
FFIEC_FI_IMPORT

JSON acts as configuration mechanism for the loading of csvs in the import folder.
If `allow_import` set to false, it will be skipped in the load process.

Note: I would prefer this to be table driven but for simplicity we are defining all the conditions in the code.
"""
FFIEC_BHCF_IMPORT = {
    "bhcf": {
        "key_type": "prefix",
        "table_schema": "transformations",
        "table_name": "tmp_bhcf",
        "if_exists": "fail",
        "sep": "^",
        "allow_import": True,
        "cols": [
            "RSSD9001",  # rssd_id
            "RSSD9999",  # reporting_date
            "BHCA2170",  # total assets
        ],
    }
}

FFIEC_FI_IMPORT = {
    "csv_attributes_active": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_attributes",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_attributes_branches": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_attributes",
        "if_exists": "append",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_attributes_closed": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_attributes",
        "if_exists": "append",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_country_codes": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_country_codes",
        "if_exists": "fail",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_county_codes": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_county_codes",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_naics": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_naics",
        "if_exists": "replace",
        "sep": ",",
        "load_type": "partial",
        "cols": [],
    },
    "csv_relationships": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_relationships",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_state_codes": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_state_codes",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    "csv_transformations": {
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_transformations",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
}

""" 
PREFLIGHT 
Drops potential duplicated data in case stopped mid proces and rebooted.
Due to how pandas is `appending` data instead of `failing` or `replacing`.
This was done for simplicity since all of the csv_attribute files are the same data structure.
"""
SCRIPTS_PREFLIGHT = {
    "scripts": [
        {
            "filename": "001_preflight.sql",
            "description": "preflight is a fail safe mechanism to ensure there is no chance of duplicate data",
            "allow_exe": True,
        }
    ]
}

"""  
SCRIPT_TRANS_LOAD
This json acts as a configuration mechanism for sequential ordering of script execution.
There are better ways to do this but this was intended to be quick lightweight solution.
If `allow_exe` set to Fale, it will be excluded during execution.
"""
SCRIPTS_TRANS_LOAD = {
    "scripts": [
        {
            "filename": "002_functions.sql",
            "description": "creates resusable functions that are a dependency",
            "allow_exe": True,
        },
        {
            "filename": "003_tables.sql",
            "description": "creation of production tables if not exist",
            "allow_exe": True,
        },
        {
            "filename": "004_tmp_tables.sql",
            "description": "creation of tmp tables for transformation",
            "allow_exe": True,
        },
        {
            "filename": "005_attributes_inst.sql",
            "description": "transformation of csv_attributes",
            "allow_exe": True,
        },
        {
            "filename": "006_attributes_ids.sql",
            "description": "transformation of csv_attributes",
            "allow_exe": True,
        },
        {
            "filename": "007_attributes_dates.sql",
            "description": "transformation of csv_attributes",
            "allow_exe": True,
        },
        {
            "filename": "008_attributes_inds.sql",
            "description": "transformation of csv_attributes",
            "allow_exe": True,
        },
        {
            "filename": "009_attributes_codes.sql",
            "description": "transformation of csv_attributes",
            "allow_exe": True,
        },
        {
            "filename": "010_attributes_load.sql",
            "description": "loads transformed data into production tables",
            "allow_exe": True,
        },
        {
            "filename": "011_relationships.sql",
            "description": "transformation of csv_relationships",
            "allow_exe": True,
        },
        {
            "filename": "012_relationships_load.sql",
            "description": "loads transformed data into target table",
            "allow_exe": True,
        },
        {
            "filename": "013_transformations.sql",
            "description": "transformation of csv_transformations and loading to target table",
            "allow_exe": True,
        },
        {
            "filename": "014_inst_addresses_load.sql",
            "description": "transformation of institution physical addresses and loads to target table",
            "allow_exe": True,
        },
        {
            "filename": "015_fips_load.sql",
            "description": "transformation and load of statistical identification codes for county, state, and country",
            "allow_exe": True,
        },
        {
            "filename": "016_naics.sql",
            "description": "transformation and load of naics codes",
            "allow_exe": True,
        },
        {
            "filename": "017_call_reports.sql",
            "description": "loading of call report data",
            "allow_exe": True,
        },
        {
            "filename": "099_cleanup.sql",
            "description": "post script for dropping tmp tables and functions",
            "allow_exe": False,
        },
    ]
}
