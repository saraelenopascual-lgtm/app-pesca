"""Puerto que define las operaciones para SparePart."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import SparePart


class SparePartRepository(ABC):
    """
    Interfaz que define las operaciones de persistencia para SparePart.

    Principio SOLID: Dependency Inversion
    """

    @abstractmethod
    def save(self, spare_part: SparePart) -> SparePart:
        """
        Guarda un repuesto (crea o actualiza).

        Args:
            spare_part: Repuesto a guardar

        Returns:
            Repuesto guardado con ID asignado
        """
        pass

    @abstractmethod
    def find_by_id(self, spare_part_id: int) -> Optional[SparePart]:
        """
        Busca un repuesto por ID.

        Args:
            spare_part_id: ID del repuesto

        Returns:
            Repuesto encontrado o None
        """
        pass

    @abstractmethod
    def find_all(self) -> List[SparePart]:
        """
        Obtiene todos los repuestos.

        Returns:
            Lista de repuestos
        """
        pass

    @abstractmethod
    def find_all_ordered_by_needed(self) -> List[SparePart]:
        """
        Obtiene todos los repuestos ordenados por estado necesario.

        Returns:
            Lista de repuestos ordenada
        """
        pass

    @abstractmethod
    def delete(self, spare_part_id: int) -> None:
        """
        Elimina un repuesto.

        Args:
            spare_part_id: ID del repuesto a eliminar
        """
        pass
