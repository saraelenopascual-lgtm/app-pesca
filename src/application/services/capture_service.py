"""Servicio de aplicación para Capture."""

from datetime import datetime
from typing import List, Optional

from src.application.ports import CaptureRepository
from src.domain.entities import Capture
from src.domain.exceptions import CaptureNotFoundError, InvalidCaptureDataError


class CaptureService:
    """
    Servicio de aplicación para gestionar capturas.

    Principios SOLID:
    - Single Responsibility: Solo gestiona lógica de capturas
    - Dependency Inversion: Depende de puertos
    """

    def __init__(self, capture_repository: CaptureRepository):
        """
        Inicializa el servicio.

        Args:
            capture_repository: Repositorio de capturas
        """
        self.capture_repository = capture_repository

    def create_capture(
        self,
        species_id: Optional[int],
        date: datetime,
        location: Optional[str] = None,
        length_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        bait: Optional[str] = None,
        hook: Optional[str] = None,
        notes: Optional[str] = None,
        media_path: Optional[str] = None,
    ) -> Capture:
        """
        Crea una nueva captura.

        Args:
            species_id: ID de la especie
            date: Fecha de captura
            location: Ubicación
            length_cm: Largo en cm
            weight_kg: Peso en kg
            bait: Cebo utilizado
            hook: Anzuelo utilizado
            notes: Notas
            media_path: Ruta del media

        Returns:
            Captura creada

        Raises:
            InvalidCaptureDataError: Si los datos son inválidos
        """
        # Validaciones de negocio
        if length_cm is not None and length_cm < 0:
            raise InvalidCaptureDataError("El largo no puede ser negativo")
        if weight_kg is not None and weight_kg < 0:
            raise InvalidCaptureDataError("El peso no puede ser negativo")

        capture = Capture(
            id=None,
            species_id=species_id,
            date=date,
            location=location,
            length_cm=length_cm,
            weight_kg=weight_kg,
            bait=bait,
            hook=hook,
            notes=notes,
            media_path=media_path,
        )
        return self.capture_repository.save(capture)

    def get_capture_by_id(self, capture_id: int) -> Capture:
        """
        Obtiene una captura por ID.

        Args:
            capture_id: ID de la captura

        Returns:
            Captura encontrada

        Raises:
            CaptureNotFoundError: Si no existe
        """
        capture = self.capture_repository.find_by_id(capture_id)
        if not capture:
            raise CaptureNotFoundError(capture_id)
        return capture

    def get_all_captures(self) -> List[Capture]:
        """
        Obtiene todas las capturas ordenadas por fecha.

        Returns:
            Lista de capturas
        """
        return self.capture_repository.find_all_ordered_by_date_desc()

    def get_captures_by_species(self, species_id: int) -> List[Capture]:
        """
        Obtiene las capturas de una especie.

        Args:
            species_id: ID de la especie

        Returns:
            Lista de capturas
        """
        return self.capture_repository.find_by_species_id(species_id)

    def update_capture(
        self,
        capture_id: int,
        location: Optional[str] = None,
        length_cm: Optional[float] = None,
        weight_kg: Optional[float] = None,
        bait: Optional[str] = None,
        hook: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> Capture:
        """
        Actualiza una captura.

        Args:
            capture_id: ID de la captura
            location: Nueva ubicación
            length_cm: Nuevo largo
            weight_kg: Nuevo peso
            bait: Nuevo cebo
            hook: Nuevo anzuelo
            notes: Nuevas notas

        Returns:
            Captura actualizada

        Raises:
            CaptureNotFoundError: Si no existe
            InvalidCaptureDataError: Si los datos son inválidos
        """
        capture = self.get_capture_by_id(capture_id)

        if length_cm is not None and length_cm < 0:
            raise InvalidCaptureDataError("El largo no puede ser negativo")
        if weight_kg is not None and weight_kg < 0:
            raise InvalidCaptureDataError("El peso no puede ser negativo")

        capture.update_details(
            location=location,
            length_cm=length_cm,
            weight_kg=weight_kg,
            bait=bait,
            hook=hook,
            notes=notes,
        )
        return self.capture_repository.save(capture)

    def delete_capture(self, capture_id: int) -> None:
        """
        Elimina una captura.

        Args:
            capture_id: ID de la captura

        Raises:
            CaptureNotFoundError: Si no existe
        """
        self.get_capture_by_id(capture_id)
        self.capture_repository.delete(capture_id)

    def add_media_to_capture(
        self,
        capture_id: int,
        media_path: str,
    ) -> Capture:
        """
        Agrega media a una captura.

        Args:
            capture_id: ID de la captura
            media_path: Ruta del media

        Returns:
            Captura actualizada

        Raises:
            CaptureNotFoundError: Si no existe
        """
        capture = self.get_capture_by_id(capture_id)
        capture.set_media(media_path)
        return self.capture_repository.save(capture)
