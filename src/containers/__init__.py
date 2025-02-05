"""
containers package

This package provides containerized dependency management for the application.

Attributes:
    DependencyManager: A globally accessible instance of the dependency container,
        created using `get_dependency_container()`. This is intended to be imported
        and used throughout the application.
"""

from .dependency import get_dependency_container

# Dependency object to be imported throughout the application to simplify object creation.
DependencyManager = get_dependency_container()
