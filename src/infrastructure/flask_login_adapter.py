"""Adaptador para Flask-Login usando modelos ORM."""

from flask_login import UserMixin

from src.infrastructure.orm import UserORM


# Hacer que UserORM sea compatible con Flask-Login
UserORM.is_authenticated = property(lambda self: True)
UserORM.is_active = property(lambda self: True)
UserORM.is_anonymous = property(lambda self: False)
UserORM.get_id = lambda self: str(self.id)


__all__ = ["UserORM"]
