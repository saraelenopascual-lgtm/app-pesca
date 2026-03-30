"""Factory para crear la aplicación Flask."""

import logging
import os
from typing import Tuple

from flask import Flask
from flask_login import LoginManager, UserMixin

from src.application.services import (
    CaptureService,
    SpeciesService,
    SparePartService,
    UserService,
)
from src.infrastructure import (
    SQLAlchemyCaptureRepository,
    SQLAlchemySpeciesRepository,
    SQLAlchemySparePartRepository,
    SQLAlchemyUserRepository,
    db,
)
from src.infrastructure.orm import (
    CaptureORM,
    SpeciesORM,
    SparePartORM,
    UserORM,
)
from src.presentation.flask.routes import (
    create_auth_routes,
    create_capture_routes,
    create_spare_part_routes,
    create_species_routes,
    create_user_routes,
)
from src.presentation.flask.routes.main_routes import main_bp

logger = logging.getLogger(__name__)


def create_app() -> Flask:
    """
    Factory para crear la aplicación Flask.

    Principios SOLID:
    - Factory Pattern para organizar la inicialización
    - Dependency Injection para los servicios
    - Separación de capas

    Returns:
        Aplicación Flask configurada
    """
    app = Flask(__name__, template_folder="templates")

    # Configuración
    app.config["SECRET_KEY"] = os.environ.get(
        "FLASK_SECRET",
        "change-me",
    )
    data_folder = os.path.join(app.root_path, "data")
    os.makedirs(data_folder, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"sqlite:///{os.path.join(data_folder, 'capturo.db')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializar BD
    db.init_app(app)

    # Inicializar autenticación
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        """Cargador de usuario para Flask-Login."""
        return UserORM.query.get(int(user_id))

    # Contexto de aplicación y datos iniciales
    with app.app_context():
        db.create_all()
        _initialize_database()

    # Crear repositorios (Dependency Injection)
    user_repo = SQLAlchemyUserRepository(db)
    species_repo = SQLAlchemySpeciesRepository(db)
    capture_repo = SQLAlchemyCaptureRepository(db)
    spare_part_repo = SQLAlchemySparePartRepository(db)

    # Crear servicios (Dependency Injection)
    user_service = UserService(
        user_repository=user_repo,
        secret_key=app.config["SECRET_KEY"],
    )
    species_service = SpeciesService(
        species_repository=species_repo,
        capture_repository=capture_repo,
    )
    capture_service = CaptureService(
        capture_repository=capture_repo,
    )
    spare_part_service = SparePartService(
        spare_part_repository=spare_part_repo,
    )

    # Registrar blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(
        create_auth_routes(user_service)
    )
    app.register_blueprint(
        create_user_routes(user_service)
    )
    app.register_blueprint(
        create_species_routes(species_service)
    )
    app.register_blueprint(
        create_capture_routes(capture_service, species_service)
    )
    app.register_blueprint(
        create_spare_part_routes(spare_part_service)
    )

    return app


def _initialize_database() -> None:
    """
    Inicializa la base de datos con datos por defecto.

    Operaciones:
    - Agregar columnas faltantes (migrations simples)
    - Crear usuario admin si no existe
    - Cargar especies por defecto
    """
    # Crear tablas si no existen
    db.create_all()

    # Intentar agregar columnas que pueden faltar
    _try_add_column("species", "image_url", "TEXT")
    _try_add_column("species", "fishing_tips", "TEXT")
    _try_add_column("users", "password_hash", "TEXT")
    _try_add_column(
        "users",
        "is_admin",
        "INTEGER DEFAULT 0",
    )

    # Crear usuario admin
    _create_admin_user()

    # Cargar especies por defecto
    _load_default_species()


def _try_add_column(
    table_name: str,
    column_name: str,
    column_type: str,
) -> None:
    """
    Intenta agregar una columna de forma segura.

    Args:
        table_name: Nombre de la tabla
        column_name: Nombre de la columna
        column_type: Tipo de la columna
    """
    try:
        statement = (
            f"ALTER TABLE {table_name} "
            f"ADD COLUMN {column_name} {column_type}"
        )
        db.session.execute(statement)
        db.session.commit()
    except Exception:
        db.session.rollback()


def _create_admin_user() -> None:
    """Crea el usuario admin si no existe."""
    admin_email = "sara.eleno.pascual@gmail.com"
    admin_user = UserORM.query.filter_by(
        email=admin_email
    ).first()

    if not admin_user:
        admin_user = UserORM(
            email=admin_email,
            name="Admin",
            password_hash="",  # Se debe establecer luego
            is_admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()
    elif not admin_user.is_admin:
        admin_user.is_admin = True
        db.session.commit()


def _load_default_species() -> None:
    """Carga las especies por defecto."""
    if SpeciesORM.query.count() > 0:
        return

    species_data = [
        {
            "name": "Dorado",
            "description": "También conocido como lampuga",
            "image_url": (
                "https://via.placeholder.com/220x140?text=Dorado"
            ),
            "fishing_tips": (
                "Suele encontrarse en superficie "
                "en días soleados; cebo: peces pequeños, artificiales"
            ),
        },
        {
            "name": "Sargo",
            "description": "Común en costas rocosas",
            "image_url": (
                "https://via.placeholder.com/220x140?text=Sargo"
            ),
            "fishing_tips": (
                "Buena época: primavera/verano. "
                "Cebo: gusanos, gambas."
            ),
        },
        {
            "name": "Lubina",
            "description": "Muy apreciada",
            "image_url": (
                "https://via.placeholder.com/220x140?text=Lubina"
            ),
            "fishing_tips": (
                "Buscarlas al amanecer o atardecer "
                "cerca de rompeolas."
            ),
        },
        {
            "name": "Anjova",
            "description": "Típica de alta mar",
            "image_url": (
                "https://via.placeholder.com/220x140?text=Anjova"
            ),
            "fishing_tips": (
                "Requiere barco; "
                "buen cebo: sardina, calamar."
            ),
        },
        {
            "name": "Bonito",
            "description": "Excelente para conservas",
            "image_url": (
                "https://via.placeholder.com/220x140?text=Bonito"
            ),
            "fishing_tips": (
                "Pesca en banco; "
                "usa señuelos rápidos o cucharillas."
            ),
        },
    ]

    for species_dict in species_data:
        species = SpeciesORM(
            name=species_dict["name"],
            description=species_dict["description"],
            image_url=species_dict["image_url"],
            fishing_tips=species_dict["fishing_tips"],
            is_caught=False,
        )
        db.session.add(species)

    db.session.commit()
