import src.constants as cnst
from src.database import intit_engine, init_table_schema
from src.import_config import ImportConfig


engine = intit_engine()
import_config = ImportConfig()


if __name__ == "__main__":
    script_preflight_config = import_config.script_configuration(
        directory=cnst.SCRIPTS, config=cnst.SCRIPTS_PREFLIGHT
    )
    bhcf_config = import_config.import_configuration(
        directory=cnst.IMPORT, config=cnst.FFIEC_BHCF_IMPORT
    )
    ffiec_config = import_config.import_configuration(
        directory=cnst.IMPORT, config=cnst.FFIEC_FI_IMPORT
    )
    script_config = import_config.script_configuration(
        directory=cnst.SCRIPTS, config=cnst.SCRIPTS_TRANS_LOAD
    )
    init_table_schema(engine=engine, schema=cnst.TABLE_SCHEMA)
    import_config.intit_scripts(engine=engine, config=cnst.SCRIPTS_PREFLIGHT)
    import_config.init_import(engine=engine, config=bhcf_config)
    import_config.init_import(engine=engine, config=ffiec_config)
    import_config.intit_scripts(engine=engine, config=cnst.SCRIPTS_TRANS_LOAD)
