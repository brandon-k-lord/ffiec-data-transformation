from .containers import DependencyManager


def main():
    registry = DependencyManager.registry()
    registry.create_schema()
    registry.process()


if __name__ == "__main__":
    main()
