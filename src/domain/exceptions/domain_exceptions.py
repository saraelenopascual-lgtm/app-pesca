"""Excepciones del dominio de la aplicación."""


class DomainException(Exception):
    """Excepción base del dominio."""

    pass


class UserNotFoundError(DomainException):
    """Se lanzada cuando no se encuentra un usuario."""

    def __init__(self, email: str):
        """
        Inicializa la excepción.

        Args:
            email: Email del usuario no encontrado
        """
        self.email = email
        super().__init__(f"Usuario con email {email!r} no encontrado")


class UserAlreadyExistsError(DomainException):
    """Se lanza cuando se intenta crear un usuario que ya existe."""

    def __init__(self, email: str):
        """
        Inicializa la excepción.

        Args:
            email: Email del usuario duplicado
        """
        self.email = email
        super().__init__(f"Ya existe un usuario con email {email!r}")


class InvalidPasswordError(DomainException):
    """Se lanza cuando la contraseña es incorrecta."""

    def __init__(self):
        """Inicializa la excepción."""
        super().__init__("Contraseña incorrecta")


class SpeciesNotFoundError(DomainException):
    """Se lanza cuando no se encuentra una especie."""

    def __init__(self, species_id: int):
        """
        Inicializa la excepción.

        Args:
            species_id: ID de la especie no encontrada
        """
        self.species_id = species_id
        super().__init__(f"Especie con ID {species_id} no encontrada")


class SpeciesAlreadyExistsError(DomainException):
    """Se lanza cuando una especie con el mismo nombre ya existe."""

    def __init__(self, name: str):
        """
        Inicializa la excepción.

        Args:
            name: Nombre de la especie duplicada
        """
        self.name = name
        super().__init__(f"Ya existe una especie con nombre {name!r}")


class SpeciesHasCapturesError(DomainException):
    """Se lanza al intentar eliminar una especie con capturas."""

    def __init__(self, species_id: int):
        """
        Inicializa la excepción.

        Args:
            species_id: ID de la especie
        """
        self.species_id = species_id
        super().__init__(
            f"No se puede eliminar especie {species_id} "
            "porque tiene capturas asociadas"
        )


class CaptureNotFoundError(DomainException):
    """Se lanza cuando no se encuentra una captura."""

    def __init__(self, capture_id: int):
        """
        Inicializa la excepción.

        Args:
            capture_id: ID de la captura no encontrada
        """
        self.capture_id = capture_id
        super().__init__(f"Captura con ID {capture_id} no encontrada")


class InvalidCaptureDataError(DomainException):
    """Se lanza cuando los datos de captura son inválidos."""

    def __init__(self, message: str):
        """
        Inicializa la excepción.

        Args:
            message: Mensaje de error
        """
        super().__init__(f"Datos de captura inválidos: {message}")


class SparePartNotFoundError(DomainException):
    """Se lanza cuando no se encuentra un repuesto."""

    def __init__(self, spare_part_id: int):
        """
        Inicializa la excepción.

        Args:
            spare_part_id: ID del repuesto no encontrado
        """
        self.spare_part_id = spare_part_id
        super().__init__(f"Repuesto con ID {spare_part_id} no encontrado")


class InsufficientQuantityError(DomainException):
    """Se lanza cuando no hay suficiente cantidad."""

    def __init__(self, available: int, requested: int):
        """
        Inicializa la excepción.

        Args:
            available: Cantidad disponible
            requested: Cantidad solicitada
        """
        self.available = available
        self.requested = requested
        super().__init__(
            f"Cantidad insuficiente: disponible {available}, "
            f"solicitado {requested}"
        )


class UnauthorizedAccessError(DomainException):
    """Se lanza cuando hay acceso no autorizado."""

    def __init__(self, message: str = "Acceso no autorizado"):
        """
        Inicializa la excepción.

        Args:
            message: Mensaje de error
        """
        super().__init__(message)


class InvalidTokenError(DomainException):
    """Se lanza cuando un token es inválido o ha expirado."""

    def __init__(self):
        """Inicializa la excepción."""
        super().__init__("Token inválido o ha expirado")
