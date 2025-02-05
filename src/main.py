import asyncio
from .containers import DependencyManager


async def main():
    registry = DependencyManager.registry()
    await registry.create_schema()
    await registry.process()


if __name__ == "__main__":
    asyncio.run(main())
