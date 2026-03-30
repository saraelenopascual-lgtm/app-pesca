"""Punto de entrada de la aplicación Flask."""

import os

from dotenv import load_dotenv

from src.app_factory import create_app

load_dotenv()

if __name__ == "__main__":
    app = create_app()

    # Modo debug: `set FLASK_DEBUG=1` (Windows)
    debug = os.environ.get("FLASK_DEBUG", "0").lower() in (
        "1",
        "true",
        "yes",
    )
    app.run(debug=debug)
