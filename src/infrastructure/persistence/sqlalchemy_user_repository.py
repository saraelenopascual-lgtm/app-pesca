"""Adaptador SQLAlchemy para UserRepository."""

from typing import List, Optional

from src.application.ports import UserRepository
from src.domain.entities import User
from src.infrastructure.orm import UserORM


class SQLAlchemyUserRepository(UserRepository):
    """
    Implementación de UserRepository usando SQLAlchemy.

    Principio SOLID: Liskov Substitution - Puede reemplazar cualquier
    implementación de UserRepository.
    """

    def __init__(self, db):
        """
        Inicializa el repositorio.

        Args:
            db: Instancia de SQLAlchemy
        """
        self.db = db

    def save(self, user: User) -> User:
        """Guarda un usuario."""
        user_orm = UserORM.query.filter_by(email=user.email).first()

        if user_orm:
            # Actualizar existente
            user_orm.name = user.name
            user_orm.password_hash = user.password_hash
            user_orm.is_admin = user.is_admin
        else:
            # Crear nuevo
            user_orm = UserORM(
                email=user.email,
                name=user.name,
                password_hash=user.password_hash,
                is_admin=user.is_admin,
            )
            self.db.session.add(user_orm)

        self.db.session.commit()
        user.id = user_orm.id
        return user

    def find_by_id(self, user_id: int) -> Optional[User]:
        """Busca user por ID."""
        user_orm = UserORM.query.get(user_id)
        return self._orm_to_entity(user_orm) if user_orm else None

    def find_by_email(self, email: str) -> Optional[User]:
        """Busca user por email."""
        user_orm = UserORM.query.filter_by(email=email).first()
        return self._orm_to_entity(user_orm) if user_orm else None

    def find_all(self) -> List[User]:
        """Obtiene todos los usuarios."""
        users_orm = UserORM.query.order_by(UserORM.email).all()
        return [self._orm_to_entity(u) for u in users_orm]

    def delete(self, user_id: int) -> None:
        """Elimina un usuario."""
        user_orm = UserORM.query.get(user_id)
        if user_orm:
            self.db.session.delete(user_orm)
            self.db.session.commit()

    def exists_by_email(self, email: str) -> bool:
        """Verifica si existe user con ese email."""
        return (
            UserORM.query.filter_by(email=email).first() is not None
        )

    @staticmethod
    def _orm_to_entity(user_orm: UserORM) -> User:
        """Convierte ORM a entidad de dominio."""
        return User(
            id=user_orm.id,
            email=user_orm.email,
            name=user_orm.name,
            password_hash=user_orm.password_hash,
            is_admin=user_orm.is_admin,
        )
