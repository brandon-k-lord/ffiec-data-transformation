from .containers.containers import get_dependency_container


def main():
    dependencies = get_dependency_container()
    database = dependencies.database()
    database.create_transformation_schema()
    process_registry = dependencies.registry()
    process_registry.process()


if __name__ == "__main__":
    main()
