import src.constants as cnst
from src.database import intit_engine, init_table_schema
from src.import_config import ImportConfig


engine = intit_engine()
import_config = ImportConfig()


if __name__ == "__main__":

    # pre-execution
    # configures script JSON
    script_preflight_config = import_config.script_configuration(
        directory=cnst.SCRIPTS, config=cnst.SCRIPTS_PREFLIGHT
    )

    # configures bhcf json config, bhcf files are handled differently for date naming convention
    bhcf_config = import_config.import_configuration(
        directory=cnst.IMPORT, config=cnst.FFIEC_BHCF_IMPORT
    )

    # configures ffiec json config
    ffiec_config = import_config.import_configuration(
        directory=cnst.IMPORT, config=cnst.FFIEC_FI_IMPORT
    )

    # configures script JSON
    script_config = import_config.script_configuration(
        directory=cnst.SCRIPTS, config=cnst.SCRIPTS_TRANS_LOAD
    )

    # validates table schema exists, creates if not
    init_table_schema(engine=engine, schema=cnst.TABLE_SCHEMA)

    # execution
    import_config.intit_scripts(engine=engine, config=cnst.SCRIPTS_PREFLIGHT)
    import_config.init_import(engine=engine, config=bhcf_config)
    import_config.init_import(engine=engine, config=ffiec_config)
    import_config.intit_scripts(engine=engine, config=cnst.SCRIPTS_TRANS_LOAD)
