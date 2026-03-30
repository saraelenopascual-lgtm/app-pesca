"""Puerto que define las operaciones para Species."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import Species


class SpeciesRepository(ABC):
    """
    Interfaz que define las operaciones de persistencia para Species.

    Principio SOLID: Dependency Inversion
    """

    @abstractmethod
    def save(self, species: Species) -> Species:
        """
        Guarda una especie (crea o actualiza).

        Args:
            species: Especie a guardar

        Returns:
            Especie guardada con ID asignado
        """
        pass

    @abstractmethod
    def find_by_id(self, species_id: int) -> Optional[Species]:
        """
        Busca una especie por ID.

        Args:
            species_id: ID de la especie

        Returns:
            Especie encontrada o None
        """
        pass

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Species]:
        """
        Busca una especie por nombre.

        Args:
            name: Nombre de la especie

        Returns:
            Especie encontrada o None
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Species]:
        """
        Obtiene todas las especies.

        Returns:
            Lista de especies
        """
        pass

    @abstractmethod
    def find_all_ordered_by_name(self) -> List[Species]:
        """
        Obtiene todas las especies ordenadas por nombre.

        Returns:
            Lista de especies ordenada
        """
        pass

    @abstractmethod
    def find_caught(self) -> List[Species]:
        """
        Obtiene todas las especies capturadas.

        Returns:
            Lista de especies capturadas
        """
        pass

    @abstractmethod
    def find_not_caught(self) -> List[Species]:
        """
        Obtiene todas las especies no capturadas.

        Returns:
            Lista de especies no capturadas
        """
        pass

    @abstractmethod
    def find_by_name_contains(self, query: str) -> List[Species]:
        """
        Busca especies cuyo nombre contiene la query.

        Args:
            query: Término de búsqueda

        Returns:
            Lista de especies coincidentes
        """
        pass

    @abstractmethod
    def delete(self, species_id: int) -> None:
        """
        Elimina una especie.

        Args:
            species_id: ID de la especie a eliminar
        """
        pass

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        """
        Verifica si existe una especie con ese nombre.

        Args:
            name: Nombre a verificar

        Returns:
            True si existe, False en caso contrario
        """
        pass

    @abstractmethod
    def count_captures(self, species_id: int) -> int:
        """
        Cuenta las capturas de una especie.

        Args:
            species_id: ID de la especie

        Returns:
            Número de capturas
        """
        pass
