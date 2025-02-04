""" 
PREFLIGHT 
Drops potential duplicated data in case stopped mid proces and rebooted.
Due to how pandas is `appending` data instead of `failing` or `replacing`.
This was done for simplicity since all of the csv_attribute files are the same data structure.

Keys:
- filename: key for file comparision
- description: informational
- allow_exe: boolean flag for allowing file to be executed
"""

from typing import List

from .dicts import ScriptsConfig

PREFLIGHT: List[ScriptsConfig] = [
    {
        "name": "001_preflight",
        "description": "preflight is a fail safe mechanism to ensure there is no chance of duplicate data",
        "allow_exe": True,
    }
]

"""  
SCRIPT_TRANS_LOAD
This json acts as a configuration mechanism for sequential ordering of script execution.
There are better ways to do this but this was intended to be quick lightweight solution.
If `allow_exe` set to Fale, it will be excluded during execution.
"""

DEPENDENCIES: List[ScriptsConfig] = [
    {
        "name": "002_functions",
        "description": "creates resusable functions that are a dependency",
        "allow_exe": True,
    },
    {
        "name": "003_tables",
        "description": "creation of production tables if not exist",
        "allow_exe": True,
    },
    {
        "name": "004_tmp_tables",
        "description": "creation of tmp tables for transformation",
        "allow_exe": True,
    },
]
ATTRIBUTES: List[ScriptsConfig] = [
    {
        "name": "005_attributes_inst",
        "description": "transformation of csv_attributes",
        "allow_exe": True,
    },
    {
        "name": "006_attributes_ids",
        "description": "transformation of csv_attributes",
        "allow_exe": True,
    },
    {
        "name": "007_attributes_dates",
        "description": "transformation of csv_attributes",
        "allow_exe": True,
    },
    {
        "name": "008_attributes_inds",
        "description": "transformation of csv_attributes",
        "allow_exe": True,
    },
    {
        "name": "009_attributes_codes",
        "description": "transformation of csv_attributes",
        "allow_exe": True,
    },
    {
        "name": "010_attributes_load",
        "description": "loads transformed data into production tables",
        "allow_exe": True,
    },
    {
        "name": "014_inst_addresses_load",
        "description": "transformation of institution physical addresses and loads to target table",
        "allow_exe": True,
    },
]
RELATIONSHIPS: List[ScriptsConfig] = [
    {
        "name": "011_relationships",
        "description": "transformation of csv_relationships",
        "allow_exe": True,
    },
    {
        "name": "012_relationships_load",
        "description": "loads transformed data into target table",
        "allow_exe": True,
    },
]
TRANSFORMATIONS: List[ScriptsConfig] = [
    {
        "name": "013_transformations",
        "description": "transformation of csv_transformations and loading to target table",
        "allow_exe": True,
    },
]
GOV_IDENTIFIERS: List[ScriptsConfig] = [
    {
        "name": "015_fips_load",
        "description": "transformation and load of statistical identification codes for county, state, and country",
        "allow_exe": True,
    },
    {
        "name": "016_naics",
        "description": "transformation and load of naics codes",
        "allow_exe": True,
    },
]
CALL_REPORTS: List[ScriptsConfig] = [
    {
        "name": "017_call_reports",
        "description": "loading of call report data",
        "allow_exe": True,
    },
    {
        "name": "099_cleanup",
        "description": "post script for dropping tmp tables and functions",
        "allow_exe": False,
    },
]
