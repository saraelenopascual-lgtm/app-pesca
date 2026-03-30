"""Data Transfer Objects para la aplicación."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class UserDTO:
    """DTO para User."""

    id: Optional[int]
    email: str
    name: Optional[str]
    is_admin: bool = False


@dataclass
class SpeciesDTO:
    """DTO para Species."""

    id: Optional[int]
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    fishing_tips: Optional[str] = None
    is_caught: bool = False


@dataclass
class CaptureDTO:
    """DTO para Capture."""

    id: Optional[int]
    species_id: Optional[int]
    date: datetime
    location: Optional[str] = None
    length_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    bait: Optional[str] = None
    hook: Optional[str] = None
    notes: Optional[str] = None
    media_path: Optional[str] = None


@dataclass
class SparePartDTO:
    """DTO para SparePart."""

    id: Optional[int]
    name: str
    quantity: int = 0
    needed: bool = False
    notes: Optional[str] = None


__all__ = ["UserDTO", "SpeciesDTO", "CaptureDTO", "SparePartDTO"]
