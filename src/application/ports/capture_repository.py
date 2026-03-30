"""Puerto que define las operaciones para Capture."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import Capture


class CaptureRepository(ABC):
    """
    Interfaz que define las operaciones de persistencia para Capture.

    Principio SOLID: Dependency Inversion
    """

    @abstractmethod
    def save(self, capture: Capture) -> Capture:
        """
        Guarda una captura (crea o actualiza).

        Args:
            capture: Captura a guardar

        Returns:
            Captura guardada con ID asignado
        """
        pass

    @abstractmethod
    def find_by_id(self, capture_id: int) -> Optional[Capture]:
        """
        Busca una captura por ID.

        Args:
            capture_id: ID de la captura

        Returns:
            Captura encontrada o None
        """
        pass

    @abstractmethod
    def find_all(self) -> List[Capture]:
        """
        Obtiene todas las capturas.

        Returns:
            Lista de capturas
        """
        pass

    @abstractmethod
    def find_all_ordered_by_date_desc(self) -> List[Capture]:
        """
        Obtiene todas las capturas ordenadas por fecha descendente.

        Returns:
            Lista de capturas ordenada
        """
        pass

    @abstractmethod
    def find_by_species_id(self, species_id: int) -> List[Capture]:
        """
        Obtiene capturas de una especie.

        Args:
            species_id: ID de la especie

        Returns:
            Lista de capturas de esa especie
        """
        pass

    @abstractmethod
    def delete(self, capture_id: int) -> None:
        """
        Elimina una captura.

        Args:
            capture_id: ID de la captura a eliminar
        """
        pass
