from .containers.containers import get_dependency_container


def main():
    dependencies = get_dependency_container()
    process_registry = dependencies.registry()
    process_registry.process()


if __name__ == "__main__":
    main()
