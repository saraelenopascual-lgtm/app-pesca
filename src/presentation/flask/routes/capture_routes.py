"""Rutas para gestión de capturas."""

import logging
import os
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename

from src.application.services import (
    CaptureService,
    SpeciesService,
)
from src.domain.exceptions import (
    CaptureNotFoundError,
    InvalidCaptureDataError,
)

logger = logging.getLogger(__name__)

capture_bp = Blueprint("capture", __name__, url_prefix="/capture")

MEDIA_FOLDER = "static/media"


def create_capture_routes(
    capture_service: CaptureService,
    species_service: SpeciesService,
) -> Blueprint:
    """
    Factory para crear rutas de capturas.

    Args:
        capture_service: Servicio de capturas
        species_service: Servicio de especies

    Returns:
        Blueprint configurado
    """

    @capture_bp.route("/nueva-captura",
                      methods=["GET", "POST"])
    @login_required
    def nueva_captura():
        """Ruta para registrar nueva captura."""
        species_list = species_service.get_all_species()

        if request.method == "POST":
            try:
                species_id = (request.form.get("species_id")
                              or None)
                date_str = request.form.get("date", "")
                location = request.form.get("location")
                length_cm = request.form.get("length_cm") or None
                weight_kg = request.form.get("weight_kg") or None
                bait = request.form.get("bait")
                hook = request.form.get("hook")
                notes = request.form.get("notes")

                # Parsear fecha
                date = datetime.now()
                if date_str:
                    try:
                        date = datetime.fromisoformat(date_str)
                    except ValueError:
                        date = datetime.now()

                # Convertir numeros
                if species_id:
                    species_id = int(species_id)
                if length_cm:
                    length_cm = float(length_cm)
                if weight_kg:
                    weight_kg = float(weight_kg)

                # Manejar media
                media_file = request.files.get("media")
                media_path = None

                if media_file and media_file.filename:
                    os.makedirs(MEDIA_FOLDER, exist_ok=True)
                    filename = secure_filename(media_file.filename)
                    save_path = os.path.join(MEDIA_FOLDER, filename)
                    media_file.save(save_path)
                    media_path = os.path.join("media", filename)

                capture_service.create_capture(
                    species_id=species_id,
                    date=date,
                    location=location,
                    length_cm=length_cm,
                    weight_kg=weight_kg,
                    bait=bait,
                    hook=hook,
                    notes=notes,
                    media_path=media_path,
                )

                flash("Captura guardada correctamente",
                      "success")
                return redirect(
                    url_for("capture.nueva_captura")
                )

            except InvalidCaptureDataError as e:
                flash(str(e), "error")
                return redirect(
                    url_for("capture.nueva_captura")
                )
            except Exception as e:
                logger.error(f"Error al crear captura: {str(e)}")
                flash("Error al guardar captura", "error")
                return redirect(
                    url_for("capture.nueva_captura")
                )

        return render_template(
            "nueva_captura.html",
            species=species_list,
        )

    @capture_bp.route("/galeria")
    @login_required
    def galeria():
        """Ruta para ver galería de capturas."""
        try:
            captures = capture_service.get_all_captures()
            return render_template(
                "galeria.html",
                captures=captures,
            )
        except Exception as e:
            logger.error(f"Error en galería: {str(e)}")
            flash("Error al cargar galería", "error")
            return redirect(url_for("main.index"))

    @capture_bp.route("/estadisticas")
    @login_required
    def estadisticas():
        """Ruta para ver estadísticas."""
        try:
            captures = capture_service.get_all_captures()
            return render_template(
                "estadisticas.html",
                captures=captures,
            )
        except Exception as e:
            logger.error(f"Error en estadísticas: {str(e)}")
            flash("Error al cargar estadísticas", "error")
            return redirect(url_for("main.index"))

    return capture_bp
