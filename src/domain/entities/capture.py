"""Entidad Capture del dominio."""

from datetime import datetime
from typing import Optional


class Capture:
    """
    Entidad que representa una captura de pez.

    Principios SOLID:
    - Single Responsibility: Gestiona solo la lógica de una captura
    """

    def __init__(
        self,
        id: Optional[int],
        species_id: Optional[int],
        date: datetime,
        location: Optional[str] = None,
        length_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        bait: Optional[str] = None,
        hook: Optional[str] = None,
        notes: Optional[str] = None,
        media_path: Optional[str] = None,
    ):
        """
        Inicializa una captura.

        Args:
            id: Identificador único (None si es nueva)
            species_id: ID de la especie capturada
            date: Fecha de captura
            location: Ubicación
            length_cm: Largo en cm
            weight_kg: Peso en kg
            bait: Cebo utilizado
            hook: Anzuelo utilizado
            notes: Notas adicionales
            media_path: Ruta de media (foto/video)
        """
        self.id = id
        self.species_id = species_id
        self.date = date
        self.location = location
        self.length_cm = length_cm
        self.weight_kg = weight_kg
        self.bait = bait
        self.hook = hook
        self.notes = notes
        self.media_path = media_path

    def update_details(
        self,
        location: Optional[str] = None,
        length_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        bait: Optional[str] = None,
        hook: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> None:
        """
        Actualiza los detalles de la captura.

        Args:
            location: Nueva ubicación
            length_cm: Nuevo largo
            weight_kg: Nuevo peso
            bait: Nuevo cebo
            hook: Nuevo anzuelo
            notes: Nuevas notas
        """
        if location is not None:
            self.location = location
        if length_cm is not None:
            self.length_cm = length_cm
        if weight_kg is not None:
            self.weight_kg = weight_kg
        if bait is not None:
            self.bait = bait
        if hook is not None:
            self.hook = hook
        if notes is not None:
            self.notes = notes

    def set_media(self, media_path: str) -> None:
        """
        Establece el media de la captura.

        Args:
            media_path: Ruta del media
        """
        self.media_path = media_path

    def has_media(self) -> bool:
        """Indica si la captura tiene media asociado."""
        return self.media_path is not None

    def __repr__(self) -> str:
        """Representación en string."""
        return (
            f"<Capture id={self.id} species_id={self.species_id} "
            f"date={self.date}>"
        )
