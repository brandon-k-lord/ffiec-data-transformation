from .containers.containers import dependency_container

if __name__ == "__main__":
    dependencies = dependency_container()
    workers = dependencies.registery()
    workers.process_registery()
