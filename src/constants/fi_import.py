""" 
FFIEC_FI_IMPORT

JSON acts as configuration mechanism for the loading of csvs in the import folder.
If `allow_import` set to false, it will be skipped in the load process.

Note: I would prefer this to be table driven but for simplicity we are defining all the conditions in the code.

Keys:
- key_type: Signals how the filename will be compared with key; prefix == partial comparision for date naming convention; full == as is comparison
- table_schema: Name of target table schema
- table_name: Name of target table to be created if not exists
- if_exists: Action to take if table exists
- sep: Seperator for reading file e.g., ",", "^"
- allow_import: Boolean flag for allowing file to be imported
- cols: List of column names, restricts import to specified list, if empty, import full list

"""

from typing import List

from .dicts import FFEICConfig


FFIEC_FI_IMPORT: List[FFEICConfig] = [
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
        "name": "csv_relationships",
        "key_type": "full",
        "table_schema": "transformations",
        "table_name": "tmp_relationships",
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
