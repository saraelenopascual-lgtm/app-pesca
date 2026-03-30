"""Rutas para gestión de usuarios."""

from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from src.application.services import UserService
from src.domain.exceptions import (
    InvalidPasswordError,
    UserNotFoundError,
)

user_bp = Blueprint("user", __name__, url_prefix="/user")


def admin_required(func):
    """Decorador para rutas que requieren admin."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if (
            not current_user.is_authenticated
            or not getattr(current_user, "is_admin", False)
        ):
            flash("Acceso denegado. Solo administradores.", "error")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return wrapper


def create_user_routes(user_service: UserService) -> Blueprint:
    """
    Factory para crear rutas de usuario.

    Args:
        user_service: Servicio de usuarios

    Returns:
        Blueprint configurado
    """

    @user_bp.route("/perfil", methods=["GET", "POST"])
    @login_required
    def perfil():
        """Ruta para actualizar perfil."""
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            if name:
                try:
                    user_service.update_profile(
                        current_user.id,
                        name=name,
                    )
                    flash("Perfil actualizado", "success")
                except UserNotFoundError:
                    flash("Error al actualizar perfil", "error")

            return redirect(url_for("user.perfil"))

        return render_template("perfil.html")

    @user_bp.route("/change-password", methods=["GET", "POST"])
    @login_required
    def change_password():
        """Ruta para cambiar contraseña."""
        if request.method == "POST":
            old_password = request.form.get("old_password", "")
            new_password = request.form.get("new_password", "")
            password2 = request.form.get("password2", "")

            if not old_password or not new_password:
                flash(
                    "Debes completar todos los campos",
                    "error",
                )
                return redirect(url_for("user.change_password"))

            if new_password != password2:
                flash("Las contraseñas nuevas no coinciden",
                      "error")
                return redirect(url_for("user.change_password"))

            try:
                user_service.change_password(
                    current_user.id,
                    old_password,
                    new_password,
                )
                flash("Contraseña cambiada correctamente",
                      "success")
                return redirect(url_for("user.perfil"))
            except InvalidPasswordError:
                flash("Contraseña actual incorrecta", "error")
                return redirect(url_for("user.change_password"))
            except UserNotFoundError:
                flash("Error al cambiar contraseña", "error")
                return redirect(url_for("user.change_password"))

        return render_template("change_password.html")

    @user_bp.route("/admin/users", methods=["GET", "POST"])
    @login_required
    @admin_required
    def admin_users():
        """Ruta para gestión de usuarios (admin)."""
        users = user_service.get_all_users()

        if request.method == "POST":
            user_id = request.form.get("user_id")
            action = request.form.get("action")

            if not user_id or not action:
                flash("Datos inválidos", "error")
                return redirect(url_for("user.admin_users"))

            try:
                user_id = int(user_id)

                if action == "toggle_admin":
                    user_service.toggle_admin(user_id)
                    flash(
                        "Permiso de administrador actualizado.",
                        "success",
                    )
                elif action == "delete_user":
                    if user_id == current_user.id:
                        flash(
                            "No puedes eliminarte a ti mismo",
                            "error",
                        )
                    else:
                        user_service.delete_user(user_id)
                        flash("Usuario eliminado.", "success")
            except UserNotFoundError:
                flash("Usuario no encontrado", "error")
            except ValueError:
                flash("ID de usuario inválido", "error")

            return redirect(url_for("user.admin_users"))

        return render_template("admin_users.html", users=users)

    return user_bp
