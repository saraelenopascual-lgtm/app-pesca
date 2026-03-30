"""Servicio de aplicación para User."""

from typing import List, Optional

from itsdangerous import URLSafeTimedSerializer

from src.application.ports import UserRepository
from src.domain.entities import User
from src.domain.exceptions import (
    InvalidPasswordError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserService:
    """
    Servicio de aplicación para gestionar usuarios.

    Principios SOLID:
    - Single Responsibility: Solo gestiona la lógica de usuarios
    - Dependency Inversion: Depende del puerto UserRepository, no de BD
    - Open/Closed: Puedo cambiar la BD sin tocar este servicio
    """

    def __init__(
        self,
        user_repository: UserRepository,
        secret_key: str,
    ):
        """
        Inicializa el servicio.

        Args:
            user_repository: Repositorio de usuarios
            secret_key: Clave para generar tokens
        """
        self.user_repository = user_repository
        self.secret_key = secret_key

    def register_user(
        self,
        email: str,
        password: str,
        name: Optional[str] = None,
    ) -> User:
        """
        Registra un nuevo usuario.

        Args:
            email: Email del usuario
            password: Contraseña
            name: Nombre del usuario

        Returns:
            Usuario creado

        Raises:
            UserAlreadyExistsError: Si el email ya existe
        """
        if self.user_repository.exists_by_email(email):
            raise UserAlreadyExistsError(email)

        user = User(
            id=None,
            email=email,
            name=name,
            is_admin=False,
        )
        user.set_password(password)
        return self.user_repository.save(user)

    def authenticate_user(
        self,
        email: str,
        password: str,
    ) -> User:
        """
        Autentica un usuario.

        Args:
            email: Email del usuario
            password: Contraseña

        Returns:
            Usuario autenticado

        Raises:
            UserNotFoundError: Si el usuario no existe
            InvalidPasswordError: Si la contraseña es incorrecta
        """
        user = self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundError(email)

        if not user.check_password(password):
            raise InvalidPasswordError()

        return user

    def get_user_by_id(self, user_id: int) -> User:
        """
        Obtiene un usuario por ID.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario encontrado

        Raises:
            UserNotFoundError: Si no existe
        """
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"ID {user_id}")
        return user

    def get_user_by_email(self, email: str) -> User:
        """
        Obtiene un usuario por email.

        Args:
            email: Email del usuario

        Returns:
            Usuario encontrado

        Raises:
            UserNotFoundError: Si no existe
        """
        user = self.user_repository.find_by_email(email)
        if not user:
            raise UserNotFoundError(email)
        return user

    def get_all_users(self) -> List[User]:
        """
        Obtiene todos los usuarios.

        Returns:
            Lista de usuarios
        """
        return self.user_repository.find_all()

    def update_profile(
        self,
        user_id: int,
        name: Optional[str] = None,
    ) -> User:
        """
        Actualiza el perfil de un usuario.

        Args:
            user_id: ID del usuario
            name: Nuevo nombre

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si no existe
        """
        user = self.get_user_by_id(user_id)
        if name is not None:
            user.update_profile(name)
        return self.user_repository.save(user)

    def change_password(
        self,
        user_id: int,
        old_password: str,
        new_password: str,
    ) -> User:
        """
        Cambia la contraseña de un usuario.

        Args:
            user_id: ID del usuario
            old_password: Contraseña actual
            new_password: Nueva contraseña

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si no existe
            InvalidPasswordError: Si la contraseña actual es incorrecta
        """
        user = self.get_user_by_id(user_id)

        if not user.check_password(old_password):
            raise InvalidPasswordError()

        user.set_password(new_password)
        return self.user_repository.save(user)

    def reset_password(
        self,
        email: str,
        new_password: str,
    ) -> User:
        """
        Restablece la contraseña de un usuario.

        Args:
            email: Email del usuario
            new_password: Nueva contraseña

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si no existe
        """
        user = self.get_user_by_email(email)
        user.set_password(new_password)
        return self.user_repository.save(user)

    def toggle_admin(self, user_id: int) -> User:
        """
        Alterna los permisos de admin de un usuario.

        Args:
            user_id: ID del usuario

        Returns:
            Usuario actualizado

        Raises:
            UserNotFoundError: Si no existe
        """
        user = self.get_user_by_id(user_id)
        user.toggle_admin() if hasattr(user, 'toggle_admin') else (
            user.make_admin()
            if not user.is_admin_user()
            else user.remove_admin()
        )
        return self.user_repository.save(user)

    def delete_user(self, user_id: int) -> None:
        """
        Elimina un usuario.

        Args:
            user_id: ID del usuario

        Raises:
            UserNotFoundError: Si no existe
        """
        self.get_user_by_id(user_id)  # Verifica que existe
        self.user_repository.delete(user_id)

    def generate_reset_password_token(
        self,
        email: str,
        expires_sec: int = 3600,
    ) -> str:
        """
        Genera un token de restablecimiento.

        Args:
            email: Email del usuario
            expires_sec: Segundos de expiración

        Returns:
            Token generado

        Raises:
            UserNotFoundError: Si no existe
        """
        user = self.get_user_by_email(email)
        serializer = URLSafeTimedSerializer(self.secret_key)
        return serializer.dumps({"user_id": user.id})

    def verify_reset_password_token(
        self,
        token: str,
        expires_sec: int = 3600,
    ) -> User:
        """
        Verifica un token de restablecimiento.

        Args:
            token: Token a verificar
            expires_sec: Segundos de expiración

        Returns:
            Usuario asociado al token

        Raises:
            InvalidTokenError: Si es inválido o expiró
        """
        serializer = URLSafeTimedSerializer(self.secret_key)
        try:
            data = serializer.loads(token, max_age=expires_sec)
        except Exception:
            raise InvalidTokenError()

        user_id = data.get("user_id")
        return self.get_user_by_id(user_id)
