"""Rutas para gestión de especies."""

import logging
import os
from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from src.application.services import SpeciesService
from src.domain.exceptions import (
    SpeciesAlreadyExistsError,
    SpeciesHasCapturesError,
    SpeciesNotFoundError,
)

logger = logging.getLogger(__name__)

species_bp = Blueprint("species", __name__, url_prefix="/species")


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


def create_species_routes(
    species_service: SpeciesService,
) -> Blueprint:
    """
    Factory para crear rutas de especies.

    Args:
        species_service: Servicio de especies

    Returns:
        Blueprint configurado
    """

    @species_bp.route("/capturopedia", methods=["GET"])
    @login_required
    def capturopedia():
        """Ruta para ver especies (capturopedia)."""
        q = request.args.get("q", "", type=str).strip()
        status = request.args.get("status", "all")

        try:
            if status == "caught":
                species_list = species_service.get_caught_species()
            elif status == "not_caught":
                species_list = species_service.get_not_caught_species()
            else:
                species_list = species_service.get_all_species()

            if q:
                species_list = species_service.search_species(q)

            return render_template(
                "capturopedia.html",
                species=species_list,
                current_status=status,
                current_query=q,
            )
        except Exception as e:
            logger.error(f"Error en capturopedia: {str(e)}")
            flash("Error al cargar especies", "error")
            return redirect(url_for("main.index"))

    @species_bp.route("/toggle/<int:species_id>", methods=["POST"])
    @login_required
    @admin_required
    def toggle_catch_status(species_id: int):
        """Ruta para alternar estado de captura."""
        try:
            species_service.toggle_catch_status(species_id)
            flash("Estado actualizado", "success")
        except SpeciesNotFoundError:
            flash("Especie no encontrada",  "error")
        except Exception as e:
            logger.error(f"Error al alternar estado: {str(e)}")
            flash("Error al actualizar estado", "error")

        return redirect(url_for("species.capturopedia"))

    @species_bp.route("/editar/<int:species_id>",
                      methods=["GET", "POST"])
    @login_required
    @admin_required
    def edit_species(species_id: int):
        """Ruta para editar especie."""
        try:
            species = species_service.get_species_by_id(species_id)

            if request.method == "POST":
                name = request.form.get("name", "").strip()
                description = request.form.get("description",
                                              "").strip()
                fishing_tips = request.form.get("fishing_tips",
                                               "").strip()

                image_file = request.files.get("image_file")
                image_url = species.image_url

                if image_file and image_file.filename:
                    os.makedirs("static/images", exist_ok=True)
                    filename = secure_filename(image_file.filename)
                    save_path = os.path.join("static/images", filename)
                    image_file.save(save_path)
                    image_url = url_for(
                        "static",
                        filename=f"images/{filename}",
                    )

                try:
                    species_service.update_species(
                        species_id,
                        name=name or None,
                        description=description or None,
                        image_url=image_url,
                        fishing_tips=fishing_tips or None,
                    )
                    flash("Especie actualizada", "success")
                    return redirect(url_for(
                        "species.capturopedia"
                    ))
                except SpeciesAlreadyExistsError:
                    flash(
                        "Ya existe una especie con ese nombre.",
                        "error",
                    )
                    return redirect(
                        url_for("species.edit_species",
                               species_id=species_id)
                    )

            return render_template(
                "capturopedia_edit.html",
                specie=species,
            )
        except SpeciesNotFoundError:
            flash("Especie no encontrada", "error")
            return redirect(url_for("species.capturopedia"))
        except Exception as e:
            logger.error(f"Error en edit_species: {str(e)}")
            flash(f"Error al editar: {str(e)}", "error")
            return redirect(url_for("species.capturopedia"))

    @species_bp.route("/add", methods=["GET", "POST"])
    @login_required
    @admin_required
    def add_species():
        """Ruta para agregar especie."""
        if request.method == "POST":
            try:
                name = request.form.get("name", "").strip()
                description = request.form.get("description",
                                              "").strip()
                fishing_tips = request.form.get("fishing_tips",
                                               "").strip()

                if not name:
                    flash("El nombre es obligatorio.", "error")
                    return redirect(url_for(
                        "species.add_species"
                    ))

                image_file = request.files.get("image_file")
                image_url = None

                if image_file and image_file.filename:
                    os.makedirs("static/images", exist_ok=True)
                    filename = secure_filename(image_file.filename)
                    save_path = os.path.join("static/images", filename)
                    image_file.save(save_path)
                    image_url = url_for(
                        "static",
                        filename=f"images/{filename}",
                    )

                species_service.create_species(
                    name,
                    description=description or None,
                    image_url=image_url,
                    fishing_tips=fishing_tips or None,
                )
                flash("Especie agregada", "success")
                return redirect(url_for("species.capturopedia"))

            except SpeciesAlreadyExistsError:
                flash("Ya existe una especie con ese nombre.",
                      "error")
                return redirect(url_for("species.add_species"))
            except Exception as e:
                logger.error(f"Error al agregar especie: {str(e)}")
                flash(f"Error al agregar especie: {str(e)}", "error")
                return redirect(url_for("species.add_species"))

        return render_template("admin_species_add.html")

    @species_bp.route("/delete/<int:species_id>",
                      methods=["POST"])
    @login_required
    @admin_required
    def delete_species(species_id: int):
        """Ruta para eliminar especie."""
        try:
            species_service.delete_species(species_id)
            flash("Especie eliminada", "success")
        except SpeciesNotFoundError:
            flash("Especie no encontrada", "error")
        except SpeciesHasCapturesError:
            flash(
                "No se puede eliminar una especie "
                "que tiene capturas asociadas.",
                "error",
            )
        except Exception as e:
            logger.error(f"Error al eliminar especie: {str(e)}")
            flash(f"Error al eliminar especie: {str(e)}", "error")

        return redirect(url_for("species.capturopedia"))

    return species_bp
