"""Entidad SparePart del dominio."""

from typing import Optional


class SparePart:
    """
    Entidad que representa un repuesto.

    Principios SOLID:
    - Single Responsibility: Gestiona solo la lógica de un repuesto
    """

    def __init__(
        self,
        id: Optional[int],
        name: str,
        quantity: int = 0,
        needed: bool = False,
        notes: Optional[str] = None,
    ):
        """
        Inicializa un repuesto.

        Args:
            id: Identificador único (None si es nuevo)
            name: Nombre del repuesto
            quantity: Cantidad disponible
            needed: Si es necesario comprar
            notes: Notas adicionales
        """
        self.id = id
        self.name = name
        self.quantity = quantity
        self.needed = needed
        self.notes = notes

    def mark_as_needed(self) -> None:
        """Marca el repuesto como necesario."""
        self.needed = True

    def mark_as_not_needed(self) -> None:
        """Marca el repuesto como no necesario."""
        self.needed = False

    def toggle_needed(self) -> None:
        """Alterna si es necesario o no."""
        self.needed = not self.needed

    def update_quantity(self, quantity: int) -> None:
        """
        Actualiza la cantidad.

        Args:
            quantity: Nueva cantidad
        """
        if quantity < 0:
            raise ValueError("La cantidad no puede ser negativa")
        self.quantity = quantity

    def add_quantity(self, amount: int) -> None:
        """
        Añade cantidad.

        Args:
            amount: Cantidad a añadir
        """
        if amount < 0:
            raise ValueError("La cantidad a añadir no puede ser negativa")
        self.quantity += amount

    def subtract_quantity(self, amount: int) -> None:
        """
        Resta cantidad.

        Args:
            amount: Cantidad a restar
        """
        if amount < 0:
            raise ValueError("La cantidad a restar no puede ser negativa")
        if amount > self.quantity:
            raise ValueError("No hay suficiente cantidad")
        self.quantity -= amount

    def __repr__(self) -> str:
        """Representación en string."""
        return f"<SparePart id={self.id} name={self.name!r}>"
