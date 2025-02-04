from typing import List, TypedDict


class FFEICConfig(TypedDict):
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
    allow_exe: bool
    description: str
    file_path: str
    name: str
