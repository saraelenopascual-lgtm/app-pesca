"""Puerto que define las operaciones para User (Repositorio)."""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities import User


class UserRepository(ABC):
    """
    Interfaz que define las operaciones de persistencia para User.

    Principio SOLID: Dependency Inversion - Los servicios dependen de esta
    interfaz, no de la implementación específica.
    """

    @abstractmethod
    def save(self, user: User) -> User:
        """
        Guarda un usuario (crea o actualiza).

        Args:
            user: Usuario a guardar

        Returns:
            Usuario guardado con ID asignado
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        """
        Busca un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario encontrado o None
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        Busca un usuario por email.

        Args:
            email: Email del usuario

        Returns:
            Usuario encontrado o None
        """
        pass

    @abstractmethod
    def find_all(self) -> List[User]:
        """
        Obtiene todos los usuarios.

        Returns:
            Lista de usuarios
        """
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario a eliminar
        """
        pass

    @abstractmethod
    def exists_by_email(self, email: str) -> bool:
        """
        Verifica si existe un usuario con ese email.

        Args:
            email: Email a verificar

        Returns:
            True si existe, False en caso contrario
        """
        pass
