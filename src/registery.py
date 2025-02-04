from .containers.containers import master_container


def import_registery() -> None:
    container = master_container()

    imports = container.import_container()

    imports.preflight_script()
    imports.bhcf_import()
    imports.fi_import()
    imports.transformation_script()
