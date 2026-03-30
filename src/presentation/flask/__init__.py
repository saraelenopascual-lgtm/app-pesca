"""Módulo de presentación Flask."""

from .routes import (
    create_auth_routes,
    create_capture_routes,
    create_spare_part_routes,
    create_species_routes,
    create_user_routes,
)

__all__ = [
    "create_auth_routes",
    "create_user_routes",
    "create_species_routes",
    "create_capture_routes",
    "create_spare_part_routes",
]
