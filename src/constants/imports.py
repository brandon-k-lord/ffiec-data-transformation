"""
imports 

This module defines configuration objects for importing CSV files from the 
import folder. The configuration is specified in JSON-like dictionaries, 
which control how each file is processed, including schema, table handling, 
and filtering.

If `allow_import` is set to False, the corresponding file will be skipped 
during the load process.

Note: While a table-driven approach would be preferable, for simplicity, all 
conditions are defined in the code.

Keys:
- name: Identifier for the import configuration.
- key_type: Specifies filename comparison method.
  - "prefix": Partial match (useful for date-based naming conventions).
  - "full": Exact match.
- table_schema: Target schema for the imported data.
- table_name: Target table for storing imported data; created if it does not exist.
- if_exists: Action to take if the target table already exists (e.g., "fail", "replace", "append").
- sep: Delimiter used in the CSV file (e.g., ",", "^").
- allow_import: Boolean flag indicating whether the file should be imported.
- cols: List of column names to import. If empty, all columns are included.
"""

from typing import List

from .objects import FFEICConfig

BHCF: List[FFEICConfig] = [
    {
        "name": "bhcf",
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
]


ATTRIBUTES: List[FFEICConfig] = [
    {
        "name": "csv_attributes_active",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_attributes",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    {
        "name": "csv_attributes_branches",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_attributes",
        "if_exists": "append",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    {
        "name": "csv_attributes_closed",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_attributes",
        "if_exists": "append",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
]

RELATIONSHIPS: List[FFEICConfig] = [
    {
        "name": "csv_relationships",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_relationships",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
]

TRANSFORMATIONS: List[FFEICConfig] = [
    {
        "name": "csv_transformations",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_transformations",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
]

GOV_IDENTIFIERS: List[FFEICConfig] = [
    {
        "name": "csv_country_codes",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_country_codes",
        "if_exists": "fail",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    {
        "name": "csv_county_codes",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_county_codes",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    {
        "name": "csv_naics",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_naics",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
    {
        "name": "csv_state_codes",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_state_codes",
        "if_exists": "replace",
        "sep": ",",
        "allow_import": True,
        "cols": [],
    },
]
