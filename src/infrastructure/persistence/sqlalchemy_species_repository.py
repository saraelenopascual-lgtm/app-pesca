"""Adaptador SQLAlchemy para SpeciesRepository."""

from typing import List, Optional

from src.application.ports import SpeciesRepository
from src.domain.entities import Species
from src.infrastructure.orm import SpeciesORM


class SQLAlchemySpeciesRepository(SpeciesRepository):
    """Implementación de SpeciesRepository usando SQLAlchemy."""

    def __init__(self, db):
        """
        Inicializa el repositorio.

        Args:
            db: Instancia de SQLAlchemy
        """
        self.db = db

    def save(self, species: Species) -> Species:
        """Guarda una especie."""
        species_orm = SpeciesORM.query.filter_by(name=species.name).first()

        if species_orm:
            # Actualizar existente
            species_orm.description = species.description
            species_orm.image_url = species.image_url
            species_orm.fishing_tips = species.fishing_tips
            species_orm.is_caught = species.is_caught
        else:
            # Crear nuevo
            species_orm = SpeciesORM(
                name=species.name,
                description=species.description,
                image_url=species.image_url,
                fishing_tips=species.fishing_tips,
                is_caught=species.is_caught,
            )
            self.db.session.add(species_orm)

        self.db.session.commit()
        species.id = species_orm.id
        return species

    def find_by_id(self, species_id: int) -> Optional[Species]:
        """Busca especie por ID."""
        species_orm = SpeciesORM.query.get(species_id)
        return (
            self._orm_to_entity(species_orm) if species_orm else None
        )

    def find_by_name(self, name: str) -> Optional[Species]:
        """Busca especie por nombre."""
        species_orm = SpeciesORM.query.filter_by(name=name).first()
        return (
            self._orm_to_entity(species_orm) if species_orm else None
        )

    def find_all(self) -> List[Species]:
        """Obtiene todas las especies."""
        species_orm_list = SpeciesORM.query.all()
        return [self._orm_to_entity(s) for s in species_orm_list]

    def find_all_ordered_by_name(self) -> List[Species]:
        """Obtiene especies ordenadas por nombre."""
        species_orm_list = SpeciesORM.query.order_by(
            SpeciesORM.name
        ).all()
        return [self._orm_to_entity(s) for s in species_orm_list]

    def find_caught(self) -> List[Species]:
        """Obtiene especies capturadas."""
        species_orm_list = SpeciesORM.query.filter_by(
            is_caught=True
        ).order_by(SpeciesORM.name).all()
        return [self._orm_to_entity(s) for s in species_orm_list]

    def find_not_caught(self) -> List[Species]:
        """Obtiene especies no capturadas."""
        species_orm_list = SpeciesORM.query.filter_by(
            is_caught=False
        ).order_by(SpeciesORM.name).all()
        return [self._orm_to_entity(s) for s in species_orm_list]

    def find_by_name_contains(self, query: str) -> List[Species]:
        """Busca especies cuyo nombre contiene la query."""
        species_orm_list = SpeciesORM.query.filter(
            SpeciesORM.name.ilike(f"%{query}%")
        ).order_by(SpeciesORM.name).all()
        return [self._orm_to_entity(s) for s in species_orm_list]

    def delete(self, species_id: int) -> None:
        """Elimina una especie."""
        species_orm = SpeciesORM.query.get(species_id)
        if species_orm:
            self.db.session.delete(species_orm)
            self.db.session.commit()

    def exists_by_name(self, name: str) -> bool:
        """Verifica si existe especie con ese nombre."""
        return (
            SpeciesORM.query.filter(
                self.db.func.lower(SpeciesORM.name)
                == name.lower()
            ).first() is not None
        )

    def count_captures(self, species_id: int) -> int:
        """Cuenta capturas de una especie."""
        return len(
            SpeciesORM.query.get(species_id).captures
            if SpeciesORM.query.get(species_id)
            else []
        )

    @staticmethod
    def _orm_to_entity(species_orm: SpeciesORM) -> Species:
        """Convierte ORM a entidad."""
        return Species(
            id=species_orm.id,
            name=species_orm.name,
            description=species_orm.description,
            image_url=species_orm.image_url,
            fishing_tips=species_orm.fishing_tips,
            is_caught=species_orm.is_caught,
        )
