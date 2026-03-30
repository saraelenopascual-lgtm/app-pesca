"""
Entidad User del dominio.

Esta clase representa un usuario en el sistema sin acoplamiento
a tecnología específica (BD, ORM, etc.).
"""

from typing import Optional
from werkzeug.security import check_password_hash, generate_password_hash


class User:
    """
    Entidad que representa un usuario de la aplicación.

    Principios SOLID:
    - Single Responsibility: Solo gestiona la lógica de un usuario
    - Open/Closed: Abierto a extensión, cerrado a modificación
    - Liskov Substitution: Puede ser reemplazada por subclases sin problemas
    """

    def __init__(
        self,
        id: Optional[int],
        email: str,
        name: Optional[str],
        password_hash: Optional[str] = None,
        is_admin: bool = False,
    ):
        """
        Inicializa un usuario.

        Args:
            id: Identificador único (None si es nuevo)
            email: Email único del usuario
            name: Nombre completo
            password_hash: Hash de la contraseña
            is_admin: Si es administrador
        """
        self.id = id
        self.email = email
        self.name = name
        self.password_hash = password_hash
        self.is_admin = is_admin

    def set_password(self, password: str) -> None:
        """
        Establece la contraseña (la hashea automáticamente).

        Args:
            password: Contraseña en texto plano
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """
        Verifica si la contraseña es correcta.

        Args:
            password: Contraseña a verificar

        Returns:
            True si es correcta, False en caso contrario
        """
        return check_password_hash(self.password_hash, password)

    def is_admin_user(self) -> bool:
        """
        Indica si el usuario es administrador.

        Returns:
            True si es admin, False en caso contrario
        """
        return self.is_admin

    def make_admin(self) -> None:
        """Eleva los permisos del usuario a administrador."""
        self.is_admin = True

    def remove_admin(self) -> None:
        """Revoca los permisos de administrador."""
        self.is_admin = False

    def update_profile(self, name: str) -> None:
        """
        Actualiza el perfil del usuario.

        Args:
            name: Nuevo nombre
        """
        self.name = name

    def __repr__(self) -> str:
        """Representación en string."""
        return f"<User id={self.id} email={self.email!r}>"

    def __eq__(self, other: object) -> bool:
        """Comparación por email (único)."""
        if not isinstance(other, User):
            return False
        return self.email == other.email
