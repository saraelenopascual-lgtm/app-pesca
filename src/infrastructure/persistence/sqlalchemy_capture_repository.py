"""Adaptador SQLAlchemy para CaptureRepository."""

from typing import List, Optional

from src.application.ports import CaptureRepository
from src.domain.entities import Capture
from src.infrastructure.orm import CaptureORM


class SQLAlchemyCaptureRepository(CaptureRepository):
    """Implementación de CaptureRepository usando SQLAlchemy."""

    def __init__(self, db):
        """
        Inicializa el repositorio.

        Args:
            db: Instancia de SQLAlchemy
        """
        self.db = db

    def save(self, capture: Capture) -> Capture:
        """Guarda una captura."""
        if capture.id:
            # Actualizar existente
            capture_orm = CaptureORM.query.get(capture.id)
            capture_orm.species_id = capture.species_id
            capture_orm.date = capture.date
            capture_orm.location = capture.location
            capture_orm.length_cm = capture.length_cm
            capture_orm.weight_kg = capture.weight_kg
            capture_orm.bait = capture.bait
            capture_orm.hook = capture.hook
            capture_orm.notes = capture.notes
            capture_orm.media_path = capture.media_path
        else:
            # Crear nuevo
            capture_orm = CaptureORM(
                species_id=capture.species_id,
                date=capture.date,
                location=capture.location,
                length_cm=capture.length_cm,
                weight_kg=capture.weight_kg,
                bait=capture.bait,
                hook=capture.hook,
                notes=capture.notes,
                media_path=capture.media_path,
            )
            self.db.session.add(capture_orm)

        self.db.session.commit()
        capture.id = capture_orm.id
        return capture

    def find_by_id(self, capture_id: int) -> Optional[Capture]:
        """Busca captura por ID."""
        capture_orm = CaptureORM.query.get(capture_id)
        return (
            self._orm_to_entity(capture_orm) if capture_orm else None
        )

    def find_all(self) -> List[Capture]:
        """Obtiene todas las capturas."""
        captures_orm = CaptureORM.query.all()
        return [self._orm_to_entity(c) for c in captures_orm]

    def find_all_ordered_by_date_desc(self) -> List[Capture]:
        """Obtiene capturas ordenadas por fecha descendente."""
        captures_orm = CaptureORM.query.order_by(
            CaptureORM.date.desc()
        ).all()
        return [self._orm_to_entity(c) for c in captures_orm]

    def find_by_species_id(self, species_id: int) -> List[Capture]:
        """Obtiene capturas de una especie."""
        captures_orm = CaptureORM.query.filter_by(
            species_id=species_id
        ).order_by(CaptureORM.date.desc()).all()
        return [self._orm_to_entity(c) for c in captures_orm]

    def delete(self, capture_id: int) -> None:
        """Elimina una captura."""
        capture_orm = CaptureORM.query.get(capture_id)
        if capture_orm:
            self.db.session.delete(capture_orm)
            self.db.session.commit()

    @staticmethod
    def _orm_to_entity(capture_orm: CaptureORM) -> Capture:
        """Convierte ORM a entidad."""
        return Capture(
            id=capture_orm.id,
            species_id=capture_orm.species_id,
            date=capture_orm.date,
            location=capture_orm.location,
            length_cm=capture_orm.length_cm,
            weight_kg=capture_orm.weight_kg,
            bait=capture_orm.bait,
            hook=capture_orm.hook,
            notes=capture_orm.notes,
            media_path=capture_orm.media_path,
        )
