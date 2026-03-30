"""Servicio de aplicación para SparePart."""

from typing import List

from src.application.ports import SparePartRepository
from src.domain.entities import SparePart
from src.domain.exceptions import (
    InsufficientQuantityError,
    SparePartNotFoundError,
)


class SparePartService:
    """
    Servicio de aplicación para gestionar repuestos.

    Principios SOLID:
    - Single Responsibility: Solo gestiona lógica de repuestos
    - Dependency Inversion: Depende de puertos
    """

    def __init__(self, spare_part_repository: SparePartRepository):
        """
        Inicializa el servicio.

        Args:
            spare_part_repository: Repositorio de repuestos
        """
        self.spare_part_repository = spare_part_repository

    def create_spare_part(
        self,
        name: str,
        quantity: int = 0,
        needed: bool = False,
        notes: str = None,
    ) -> SparePart:
        """
        Crea un nuevo repuesto.

        Args:
            name: Nombre del repuesto
            quantity: Cantidad inicial
            needed: Si es necesario
            notes: Notas

        Returns:
            Repuesto creado
        """
        spare_part = SparePart(
            id=None,
            name=name,
            quantity=quantity,
            needed=needed,
            notes=notes,
        )
        return self.spare_part_repository.save(spare_part)

    def get_spare_part_by_id(self, spare_part_id: int) -> SparePart:
        """
        Obtiene un repuesto por ID.

        Args:
            spare_part_id: ID del repuesto

        Returns:
            Repuesto encontrado

        Raises:
            SparePartNotFoundError: Si no existe
        """
        spare_part = self.spare_part_repository.find_by_id(spare_part_id)
        if not spare_part:
            raise SparePartNotFoundError(spare_part_id)
        return spare_part

    def get_all_spare_parts(self) -> List[SparePart]:
        """
        Obtiene todos los repuestos.

        Returns:
            Lista de repuestos ordenada por necesidad
        """
        return self.spare_part_repository.find_all_ordered_by_needed()

    def update_spare_part(
        self,
        spare_part_id: int,
        name: str = None,
        needed: bool = None,
        notes: str = None,
    ) -> SparePart:
        """
        Actualiza un repuesto.

        Args:
            spare_part_id: ID del repuesto
            name: Nuevo nombre
            needed: Nuevo estado de necesidad
            notes: Nuevas notas

        Returns:
            Repuesto actualizado

        Raises:
            SparePartNotFoundError: Si no existe
        """
        spare_part = self.get_spare_part_by_id(spare_part_id)

        if name is not None:
            spare_part.name = name
        if needed is not None:
            if needed:
                spare_part.mark_as_needed()
            else:
                spare_part.mark_as_not_needed()
        if notes is not None:
            spare_part.notes = notes

        return self.spare_part_repository.save(spare_part)

    def delete_spare_part(self, spare_part_id: int) -> None:
        """
        Elimina un repuesto.

        Args:
            spare_part_id: ID del repuesto

        Raises:
            SparePartNotFoundError: Si no existe
        """
        self.get_spare_part_by_id(spare_part_id)
        self.spare_part_repository.delete(spare_part_id)

    def add_quantity(
        self,
        spare_part_id: int,
        amount: int,
    ) -> SparePart:
        """
        Agrega cantidad a un repuesto.

        Args:
            spare_part_id: ID del repuesto
            amount: Cantidad a agregar

        Returns:
            Repuesto actualizado

        Raises:
            SparePartNotFoundError: Si no existe
        """
        spare_part = self.get_spare_part_by_id(spare_part_id)
        spare_part.add_quantity(amount)
        return self.spare_part_repository.save(spare_part)

    def subtract_quantity(
        self,
        spare_part_id: int,
        amount: int,
    ) -> SparePart:
        """
        Resta cantidad de un repuesto.

        Args:
            spare_part_id: ID del repuesto
            amount: Cantidad a restar

        Returns:
            Repuesto actualizado

        Raises:
            SparePartNotFoundError: Si no existe
            InsufficientQuantityError: Si no hay suficiente cantidad
        """
        spare_part = self.get_spare_part_by_id(spare_part_id)
        spare_part.subtract_quantity(amount)
        return self.spare_part_repository.save(spare_part)

    def toggle_needed(self, spare_part_id: int) -> SparePart:
        """
        Alterna si un repuesto es necesario.

        Args:
            spare_part_id: ID del repuesto

        Returns:
            Repuesto actualizado

        Raises:
            SparePartNotFoundError: Si no existe
        """
        spare_part = self.get_spare_part_by_id(spare_part_id)
        spare_part.toggle_needed()
        return self.spare_part_repository.save(spare_part)
