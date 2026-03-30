"""Rutas de autenticación y gestión de usuarios."""

from functools import wraps
from typing import Optional
from urllib.parse import urlparse

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from src.application.services import UserService
from src.domain.exceptions import (
    InvalidPasswordError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

auth_bp = Blueprint("auth", __name__)


def create_auth_routes(user_service: UserService) -> Blueprint:
    """
    Factory para crear rutas de autenticación.

    Args:
        user_service: Servicio de usuarios

    Returns:
        Blueprint configurado

    Principio SOLID: Injection - Los servicios se inyectan
    """

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

    @auth_bp.route("/login", methods=["GET", "POST"])
    def login():
        """Ruta para login."""
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))

        if request.method == "POST":
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            remember = bool(request.form.get("remember"))

            try:
                user = user_service.authenticate_user(email, password)
                login_user(user, remember=remember)
                flash("Sesión iniciada correctamente", "success")

                next_page = request.args.get("next")
                if next_page:
                    next_url = urlparse(next_page)
                    if next_url.netloc == "":
                        return redirect(next_page)

                return redirect(url_for("main.index"))
            except UserNotFoundError:
                flash("Email o contraseña incorrectos", "error")
                return redirect(url_for("auth.login"))
            except InvalidPasswordError:
                flash("Email o contraseña incorrectos", "error")
                return redirect(url_for("auth.login"))

        return render_template("login.html")

    @auth_bp.route("/register", methods=["GET", "POST"])
    def register():
        """Ruta para registro."""
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")

            if not email or not password:
                flash("Debes completar email y contraseña", "error")
                return redirect(url_for("auth.register"))

            try:
                user = user_service.register_user(email, password, name)
                login_user(user)
                flash("Cuenta creada y sesión iniciada", "success")
                return redirect(url_for("main.index"))
            except UserAlreadyExistsError:
                flash("Ya existe un usuario con ese email", "error")
                return redirect(url_for("auth.register"))

        return render_template("register.html")

    @auth_bp.route("/logout")
    def logout():
        """Ruta para logout."""
        logout_user()
        flash("Sesión cerrada", "success")
        return redirect(url_for("main.index"))

    @auth_bp.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        """Ruta para recuperación de contraseña."""
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))

        reset_link: Optional[str] = None
        if request.method == "POST":
            email = request.form.get("email", "").strip()
            try:
                token = user_service.generate_reset_password_token(email)
                reset_link = url_for(
                    "auth.reset_password",
                    token=token,
                    _external=True,
                )
                flash(
                    "Se ha generado un enlace de restablecimiento. "
                    "Copia y pega el enlace en tu navegador.",
                    "info",
                )
            except UserNotFoundError:
                flash("No se encontró un usuario con ese email.",
                      "error")

        return render_template(
            "forgot_password.html",
            reset_link=reset_link,
        )

    @auth_bp.route("/reset-password/<token>", methods=["GET", "POST"])
    def reset_password(token: str):
        """Ruta para restablecer contraseña."""
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))

        try:
            user = user_service.verify_reset_password_token(token)
        except InvalidTokenError:
            flash("Token inválido o caducado.", "error")
            return redirect(url_for("auth.forgot_password"))

        if request.method == "POST":
            password = request.form.get("password", "")
            password2 = request.form.get("password2", "")
            if not password or password != password2:
                flash("Las contraseñas no coinciden.", "error")
                return redirect(
                    url_for("auth.reset_password", token=token)
                )

            user_service.reset_password(user.email, password)
            flash(
                "Contraseña actualizada. "
                "Ya puedes iniciar sesión.",
                "success",
            )
            return redirect(url_for("auth.login"))

        return render_template("reset_password.html")

    return auth_bp
