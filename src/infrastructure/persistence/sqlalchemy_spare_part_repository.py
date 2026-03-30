"""Adaptador SQLAlchemy para SparePartRepository."""

from typing import List, Optional

from src.application.ports import SparePartRepository
from src.domain.entities import SparePart
from src.infrastructure.orm import SparePartORM


class SQLAlchemySparePartRepository(SparePartRepository):
    """Implementación de SparePartRepository usando SQLAlchemy."""

    def __init__(self, db):
        """
        Inicializa el repositorio.

        Args:
            db: Instancia de SQLAlchemy
        """
        self.db = db

    def save(self, spare_part: SparePart) -> SparePart:
        """Guarda un repuesto."""
        if spare_part.id:
            # Actualizar existente
            spare_part_orm = SparePartORM.query.get(spare_part.id)
            spare_part_orm.name = spare_part.name
            spare_part_orm.quantity = spare_part.quantity
            spare_part_orm.needed = spare_part.needed
            spare_part_orm.notes = spare_part.notes
        else:
            # Crear nuevo
            spare_part_orm = SparePartORM(
                name=spare_part.name,
                quantity=spare_part.quantity,
                needed=spare_part.needed,
                notes=spare_part.notes,
            )
            self.db.session.add(spare_part_orm)

        self.db.session.commit()
        spare_part.id = spare_part_orm.id
        return spare_part

    def find_by_id(self, spare_part_id: int) -> Optional[SparePart]:
        """Busca repuesto por ID."""
        spare_part_orm = SparePartORM.query.get(spare_part_id)
        return (
            self._orm_to_entity(spare_part_orm)
            if spare_part_orm
            else None
        )

    def find_all(self) -> List[SparePart]:
        """Obtiene todos los repuestos."""
        spare_parts_orm = SparePartORM.query.all()
        return [self._orm_to_entity(sp) for sp in spare_parts_orm]

    def find_all_ordered_by_needed(self) -> List[SparePart]:
        """Obtiene repuestos ordenados por necesidad."""
        spare_parts_orm = SparePartORM.query.order_by(
            SparePartORM.needed.desc(),
            SparePartORM.name,
        ).all()
        return [self._orm_to_entity(sp) for sp in spare_parts_orm]

    def delete(self, spare_part_id: int) -> None:
        """Elimina un repuesto."""
        spare_part_orm = SparePartORM.query.get(spare_part_id)
        if spare_part_orm:
            self.db.session.delete(spare_part_orm)
            self.db.session.commit()

    @staticmethod
    def _orm_to_entity(spare_part_orm: SparePartORM) -> SparePart:
        """Convierte ORM a entidad."""
        return SparePart(
            id=spare_part_orm.id,
            name=spare_part_orm.name,
            quantity=spare_part_orm.quantity,
            needed=spare_part_orm.needed,
            notes=spare_part_orm.notes,
        )
