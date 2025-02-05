"""
objects 

Defines schema structures for configuration objects used in the application. 

Classes:
- FFEICConfig: Represents the configuration schema for data imports, specifying
  file handling rules, table mappings, and allowed columns.
- ScriptsConfig: Represents the configuration schema for script executions, 
  defining execution permissions and metadata.
"""

from typing import List, TypedDict


class FFEICConfig(TypedDict):
    """Schema definition for import configuration objects.

    Attributes:
    - allow_import (bool): Indicates whether the file should be imported.
    - cols (List[str]): List of column names to be imported (empty means all columns).
    - file_path (str): Path to the source file.
    - if_exists (str): Action to take if the target table already exists.
    - key_type (str): Defines how the filename is matched (e.g., prefix, full).
    - name (str): Identifier for the configuration.
    - sep (str): Delimiter used in the file (e.g., ',', '^').
    - table_schema (str): Target schema for the import.
    - table_name (str): Target table for storing the imported data.
    """

    allow_import: bool
    cols: List[str]
    file_path: str
    if_exists: str
    key_type: str
    name: str
    sep: str
    table_schema: str
    table_name: str


class ScriptsConfig(TypedDict):
    """Schema definition for script execution configuration.

    Attributes:
    - allow_exe (bool): Determines whether execution of the script is allowed.
    - description (str): Brief description of the script's purpose.
    - file_path (str): Path to the script file.
    - name (str): Identifier for the script configuration.
    """

    allow_exe: bool
    description: str
    file_path: str
    name: str
