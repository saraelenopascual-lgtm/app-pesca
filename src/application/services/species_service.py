"""Servicio de aplicación para Species."""

from typing import List

from src.application.ports import CaptureRepository, SpeciesRepository
from src.domain.entities import Species
from src.domain.exceptions import (
    SpeciesAlreadyExistsError,
    SpeciesHasCapturesError,
    SpeciesNotFoundError,
)


class SpeciesService:
    """
    Servicio de aplicación para gestionar especies.

    Principios SOLID:
    - Single Responsibility: Solo gestiona lógica de especies
    - Dependency Inversion: Depende de puertos, no de BD
    """

    def __init__(
        self,
        species_repository: SpeciesRepository,
        capture_repository: CaptureRepository,
    ):
        """
        Inicializa el servicio.

        Args:
            species_repository: Repositorio de especies
            capture_repository: Repositorio de capturas
        """
        self.species_repository = species_repository
        self.capture_repository = capture_repository

    def create_species(
        self,
        name: str,
        description: str = None,
        image_url: str = None,
        fishing_tips: str = None,
    ) -> Species:
        """
        Crea una nueva especie.

        Args:
            name: Nombre de la especie
            description: Descripción
            image_url: URL de la imagen
            fishing_tips: Consejos de pesca

        Returns:
            Especie creada

        Raises:
            SpeciesAlreadyExistsError: Si el nombre ya existe
        """
        if self.species_repository.exists_by_name(name):
            raise SpeciesAlreadyExistsError(name)

        species = Species(
            id=None,
            name=name,
            description=description,
            image_url=image_url,
            fishing_tips=fishing_tips,
            is_caught=False,
        )
        return self.species_repository.save(species)

    def get_species_by_id(self, species_id: int) -> Species:
        """
        Obtiene una especie por ID.

        Args:
            species_id: ID de la especie

        Returns:
            Especie encontrada

        Raises:
            SpeciesNotFoundError: Si no existe
        """
        species = self.species_repository.find_by_id(species_id)
        if not species:
            raise SpeciesNotFoundError(species_id)
        return species

    def get_species_by_name(self, name: str) -> Species:
        """
        Obtiene una especie por nombre.

        Args:
            name: Nombre de la especie

        Returns:
            Especie encontrada

        Raises:
            SpeciesNotFoundError: Si no existe
        """
        species = self.species_repository.find_by_name(name)
        if not species:
            raise SpeciesNotFoundError(f"name={name}")
        return species

    def get_all_species(self) -> List[Species]:
        """
        Obtiene todas las especies.

        Returns:
            Lista de especies ordenada por nombre
        """
        return self.species_repository.find_all_ordered_by_name()

    def get_caught_species(self) -> List[Species]:
        """
        Obtiene las especies capturadas.

        Returns:
            Lista de especies capturadas
        """
        return self.species_repository.find_caught()

    def get_not_caught_species(self) -> List[Species]:
        """
        Obtiene las especies no capturadas.

        Returns:
            Lista de especies no capturadas
        """
        return self.species_repository.find_not_caught()

    def search_species(self, query: str) -> List[Species]:
        """
        Busca especies por nombre.

        Args:
            query: Término de búsqueda

        Returns:
            Lista de especies coincidentes
        """
        if not query.strip():
            return self.get_all_species()
        return self.species_repository.find_by_name_contains(query)

    def update_species(
        self,
        species_id: int,
        name: str = None,
        description: str = None,
        image_url: str = None,
        fishing_tips: str = None,
    ) -> Species:
        """
        Actualiza una especie.

        Args:
            species_id: ID de la especie
            name: Nuevo nombre
            description: Nueva descripción
            image_url: Nueva URL de imagen
            fishing_tips: Nuevos consejos

        Returns:
            Especie actualizada

        Raises:
            SpeciesNotFoundError: Si no existe
            SpeciesAlreadyExistsError: Si el nombre ya existe
        """
        species = self.get_species_by_id(species_id)

        # Verificar nombre único si se cambió
        if name and name != species.name:
            if self.species_repository.exists_by_name(name):
                raise SpeciesAlreadyExistsError(name)

        species.update_info(
            name=name or species.name,
            description=description,
            image_url=image_url,
            fishing_tips=fishing_tips,
        )
        return self.species_repository.save(species)

    def delete_species(self, species_id: int) -> None:
        """
        Elimina una especie.

        Args:
            species_id: ID de la especie

        Raises:
            SpeciesNotFoundError: Si no existe
            SpeciesHasCapturesError: Si tiene capturas
        """
        species = self.get_species_by_id(species_id)

        # Verificar que no tenga capturas
        capture_count = self.species_repository.count_captures(species_id)
        if capture_count > 0:
            raise SpeciesHasCapturesError(species_id)

        self.species_repository.delete(species_id)

    def toggle_catch_status(self, species_id: int) -> Species:
        """
        Alterna el estado de captura de una especie.

        Args:
            species_id: ID de la especie

        Returns:
            Especie actualizada

        Raises:
            SpeciesNotFoundError: Si no existe
        """
        species = self.get_species_by_id(species_id)
        species.toggle_catch_status()
        return self.species_repository.save(species)

    def mark_as_caught(self, species_id: int) -> Species:
        """
        Marca una especie como capturada.

        Args:
            species_id: ID de la especie

        Returns:
            Especie actualizada

        Raises:
            SpeciesNotFoundError: Si no existe
        """
        species = self.get_species_by_id(species_id)
        species.mark_as_caught()
        return self.species_repository.save(species)
