"""
script

This module defines a structured list of script execution configurations used for data transformation,
loading, and processing tasks. Each script is categorized based on its function and execution order.

Categories:
- PREFLIGHT: Ensures no duplicate data before execution.
- DEPENDENCIES: Creates reusable functions and tables needed for later transformations.
- ATTRIBUTES: Transforms and loads CSV-based attributes into the production system.
- RELATIONSHIPS: Processes and loads relationship-based transformations.
- TRANSFORMATIONS: Handles general data transformations before final loading.
- GOV_IDENTIFIERS: Loads and transforms government statistical identifiers like FIPS and NAICS codes.
- CALL_REPORTS: Processes financial call reports and handles cleanup operations.

Keys:
- name (str): Unique script identifier for execution ordering.
- description (str): Descriptive metadata explaining the purpose of the script.
- allow_exe (bool): Flag indicating if execution is permitted.

Each script configuration is stored in a categorized list, ensuring modular execution
and streamlined dependency management.

"""

from typing import List

from .objects import ScriptsConfig

PREFLIGHT: List[ScriptsConfig] = [
    {
        "name": "001_preflight",
        "description": "preflight is a fail safe mechanism to ensure there is no chance of duplicate data",
        "allow_exe": True,
    }
]

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
        "allow_exe": True,
    },
]
