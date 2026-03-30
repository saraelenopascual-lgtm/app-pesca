"""Modelos ORM para la persistencia con SQLAlchemy."""

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class UserORM(UserMixin, db.Model):
    """
    Modelo ORM para User.

    IMPORTANTE: Este modelo está acoplado a SQLAlchemy.
    Se mapea a User de dominio sin exponer la implementación.
    Hereda de UserMixin para compatibilidad con Flask-Login.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
    name = db.Column(db.String(256), nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """Representación en string."""
        return f"<UserORM {self.email!r}>"


class SpeciesORM(db.Model):
    """Modelo ORM para Species."""

    __tablename__ = "species"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(1024), nullable=True)
    fishing_tips = db.Column(db.Text, nullable=True)
    is_caught = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self) -> str:
        """Representación en string."""
        return f"<SpeciesORM {self.name!r}>"


class CaptureORM(db.Model):
    """Modelo ORM para Capture."""

    __tablename__ = "captures"

    id = db.Column(db.Integer, primary_key=True)
    species_id = db.Column(
        db.Integer,
        db.ForeignKey("species.id"),
        nullable=True,
    )
    species = db.relationship("SpeciesORM", backref="captures")
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    length_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    bait = db.Column(db.String(255), nullable=True)
    hook = db.Column(db.String(255), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    media_path = db.Column(db.String(1024), nullable=True)

    def __repr__(self) -> str:
        """Representación en string."""
        return (
            f"<CaptureORM id={self.id} "
            f"species={self.species.name if self.species else None}>"
        )


class SparePartORM(db.Model):
    """Modelo ORM para SparePart."""

    __tablename__ = "spare_parts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, default=0, nullable=False)
    needed = db.Column(db.Boolean, default=False, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self) -> str:
        """Representación en string."""
        return f"<SparePartORM {self.name!r}>"
