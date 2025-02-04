from typing import List

from .dicts import FFEICConfig

FFIEC_BHCF_IMPORT: List[FFEICConfig] = [
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
