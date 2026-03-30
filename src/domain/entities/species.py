"""Entidad Species del dominio."""

from typing import Optional


class Species:
    """
    Entidad que representa una especie de pez.

    Principios SOLID:
    - Single Responsibility: Gestiona solo la lógica de una especie
    """

    def __init__(
        self,
        id: Optional[int],
        name: str,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        fishing_tips: Optional[str] = None,
        is_caught: bool = False,
    ):
        """
        Inicializa una especie.

        Args:
            id: Identificador único (None si es nueva)
            name: Nombre de la especie
            description: Descripción
            image_url: URL de la imagen
            fishing_tips: Consejos de pesca
            is_caught: Si ha sido capturada
        """
        self.id = id
        self.name = name
        self.description = description
        self.image_url = image_url
        self.fishing_tips = fishing_tips
        self.is_caught = is_caught

    def mark_as_caught(self) -> None:
        """Marca la especie como capturada."""
        self.is_caught = True

    def mark_as_not_caught(self) -> None:
        """Marca la especie como no capturada."""
        self.is_caught = False

    def toggle_catch_status(self) -> None:
        """Alterna el estado de captura."""
        self.is_caught = not self.is_caught

    def update_info(
        self,
        name: str,
        description: Optional[str] = None,
        image_url: Optional[str] = None,
        fishing_tips: Optional[str] = None,
    ) -> None:
        """
        Actualiza la información de la especie.

        Args:
            name: Nuevo nombre
            description: Nueva descripción
            image_url: Nueva URL de imagen
            fishing_tips: Nuevos consejos
        """
        self.name = name
        if description is not None:
            self.description = description
        if image_url is not None:
            self.image_url = image_url
        if fishing_tips is not None:
            self.fishing_tips = fishing_tips

    def __repr__(self) -> str:
        """Representación en string."""
        return f"<Species id={self.id} name={self.name!r}>"

    def __eq__(self, other: object) -> bool:
        """Comparación por nombre (único)."""
        if not isinstance(other, Species):
            return False
        return self.name.lower() == other.name.lower()
