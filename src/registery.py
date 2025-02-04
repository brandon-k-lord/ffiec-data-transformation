from concurrent.futures import ProcessPoolExecutor

from .containers.containers import master_container


def import_registery() -> None:
    container = master_container()
    imports = container.import_container()

    imports.preflight_script()

    with ProcessPoolExecutor() as executer:
        executer.map(lambda func: func(), [imports.bhcf_import, imports.fi_import])

    imports.transformation_script()
