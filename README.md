# Capturo

App web de pesca para guardar capturas, fotos, notas y estadísticas.

## 🚀 Inicio rápido

1. Crear un entorno virtual e instalar dependencias:

```bash
python -m venv .venv
source .venv/bin/activate  # o `.venv\Scripts\activate` en Windows
pip install -r requirements.txt
```

2. Configurar variables de entorno (opcional):

1) Crea un archivo `.env` en la raíz del proyecto (puedes copiar `.env.example`):

```powershell
copy .env.example .env
```

2) Ajusta `FLASK_SECRET` en `.env` para algo seguro.

> Nota: la app usa `python-dotenv` para cargar automáticamente las variables de `.env`.

3. Iniciar la base de datos (solo la primera vez):

```bash
python init_db.py
```

4. Ejecutar la app:

```bash
python app.py
```

5. Abrir en el navegador:

http://127.0.0.1:5000

> La aplicación usa autenticación local (usuario/contraseña); deberás iniciar sesión para ver las secciones principales (capturas, galería, capturopedia, etc.). Puedes recuperar tu contraseña desde la pantalla de inicio de sesión si la olvidas.

## 📦 Estructura

## �📦 Estructura

- `app.py`: punto de entrada de la aplicación
- `models.py`: modelo de datos (SQLite)
- `templates/`: plantillas HTML
- `static/`: CSS, imágenes y archivos estáticos

## 📝 Funcionalidades previstas

- Registrar capturas con foto, medidas, cebo y anzuelo
- Galería de fotos/videos de capturas
- Notas de repuestos/material faltante
- Estadísticas básicas (comparativas, tablas)
- "Capturopedia": lista de especies con seguimiento de si ya se ha pescado
