"""Rutas para gestión de repuestos."""

import logging
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.application.services import SparePartService
from src.domain.exceptions import (
    InsufficientQuantityError,
    SparePartNotFoundError,
)

logger = logging.getLogger(__name__)

spare_part_bp = Blueprint(
    "spare_part",
    __name__,
    url_prefix="/spare-parts",
)


def admin_required(func):
    """Decorador para rutas que requieren admin."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            not current_user.is_authenticated
            or not getattr(current_user, "is_admin", False)
        ):
            flash("Acceso denegado. Solo administradores.",
                  "error")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return wrapper


def create_spare_part_routes(
    spare_part_service: SparePartService,
) -> Blueprint:
    """
    Factory para crear rutas de repuestos.

    Args:
        spare_part_service: Servicio de repuestos

    Returns:
        Blueprint configurado
    """

    @spare_part_bp.route("/", methods=["GET", "POST"])
    @login_required
    @admin_required
    def repuestos():
        """Ruta para gestión de repuestos."""
        if request.method == "POST":
            try:
                name = request.form.get("name", "").strip()
                quantity = request.form.get("quantity") or 0
                needed = bool(request.form.get("needed"))
                notes = request.form.get("notes", "")

                spare_part_service.create_spare_part(
                    name=name,
                    quantity=int(quantity),
                    needed=needed,
                    notes=notes or None,
                )
                flash("Repuesto guardado", "success")
            except ValueError:
                flash("Cantidad debe ser un número", "error")
            except Exception as e:
                logger.error(f"Error al crear repuesto: {str(e)}")
                flash("Error al crear repuesto", "error")

            return redirect(url_for("spare_part.repuestos"))

        try:
            parts = spare_part_service.get_all_spare_parts()
            return render_template(
                "repuestos.html",
                parts=parts,
            )
        except Exception as e:
            logger.error(f"Error al cargar repuestos: {str(e)}")
            flash("Error al cargar repuestos", "error")
            return redirect(url_for("main.index"))

    @spare_part_bp.route(
        "/<int:spare_part_id>/toggle-needed",
        methods=["POST"],
    )
    @login_required
    @admin_required
    def toggle_needed(spare_part_id: int):
        """Ruta para alternar estado de necesidad."""
        try:
            spare_part_service.toggle_needed(spare_part_id)
            flash("Estado actualizado", "success")
        except SparePartNotFoundError:
            flash("Repuesto no encontrado", "error")
        except Exception as e:
            logger.error(f"Error al alternar estado: {str(e)}")
            flash("Error al actualizar estado", "error")

        return redirect(url_for("spare_part.repuestos"))

    @spare_part_bp.route(
        "/<int:spare_part_id>/delete",
        methods=["POST"],
    )
    @login_required
    @admin_required
    def delete_spare_part(spare_part_id: int):
        """Ruta para eliminar repuesto."""
        try:
            spare_part_service.delete_spare_part(spare_part_id)
            flash("Repuesto eliminado", "success")
        except SparePartNotFoundError:
            flash("Repuesto no encontrado", "error")
        except Exception as e:
            logger.error(f"Error al eliminar: {str(e)}")
            flash("Error al eliminar repuesto", "error")

        return redirect(url_for("spare_part.repuestos"))

    return spare_part_bp
