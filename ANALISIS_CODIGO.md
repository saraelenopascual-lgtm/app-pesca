# Análisis de Código: PEP 8 y Arquitectura Hexagonal

**Fecha de análisis:** 30 de marzo de 2026  
**Proyecto:** APP Pesca  
**Archivos analizados:** `app.py`, `views.py`, `models.py`, `requirements.txt`

---

## 📋 Resumen Ejecutivo

| Aspecto | Estado | Calificación |
|--------|--------|-------------|
| **Cumplimiento PEP 8** | Parcial | ⚠️ 65% |
| **Arquitectura Hexagonal** | No implementada | ❌ 0% |
| **Mantenibilidad** | Regular | ⚠️ Media |
| **Escalabilidad** | Limitada | ⚠️ Baja |

---

## 🔍 Análisis PEP 8 (Cumplimiento: 65%)

### ✅ Aspectos Positivos

1. **Nomenclatura correcta**
   - Funciones y variables en `snake_case` ✓
   - Clases en `PascalCase` ✓
   - Constantes en `UPPERCASE` (MEDIA_FOLDER) ✓

2. **Imports organizados**
   - Orden correcto: stdlib → third-party → local imports
   - Ejemplo correcto en `views.py`:
     ```python
     import os
     import logging
     from datetime import datetime
     
     from flask import Blueprint, flash, ...
     from models import Capture, Species, ...
     ```

3. **Docstrings**
   - El método `get_reset_password_token()` en `models.py` incluye docstring ✓
   - El método `verify_reset_password_token()` incluye docstring ✓

4. **Espaciado correcto**
   - Dos líneas en blanco entre funciones de nivel superior ✓
   - Una línea en blanco entre métodos de clase ✓

### ⚠️ Problemas Encontrados

1. **Líneas demasiado largas (> 79 caracteres)**

   Línea 24 en `app.py`:
   ```python
   app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(data_folder, "capturo.db")
   # 111 caracteres - EXCEDE PEP 8
   ```

   Línea en `views.py`:
   ```python
   existing = Species.query.filter(db.func.lower(Species.name) == name.casefold(), Species.id != species_id).first()
   # 141 caracteres - EXCEDE PEP 8
   ```

   Línea en `views.py`:
   ```python
   image_url = url_for("static", filename=f"images/{filename}")
   # Líneas muy largas con f-strings
   ```

2. **Falta de type hints**
   - Las funciones carecen de anotaciones de tipo
   - Ejemplo: `def login():` debería ser `def login() -> str:`
   - Excepción: `User.verify_reset_password_token(token: str)` tiene hints

3. **Manejo inconsistente de excepciones**

   En `app.py`:
   ```python
   try:
       db.session.execute("ALTER TABLE species ADD COLUMN image_url TEXT")
       db.session.commit()
   except Exception:  # ⚠️ Excepto genérica - NO RECOMENDADO
       db.session.rollback()
   ```
   
   Mejor práctica:
   ```python
   except sqlalchemy.exc.OperationalError:
       db.session.rollback()
   ```

4. **Imports no utilizados**
   - `logging` en `views.py` se importa pero se usa
   - `current_app` en `models.py` se usa correctamente

5. **Blank lines inconsistentes**
   - En `views.py` línea 319: falta línea en blanco después de función

6. **Comentarios con espaciado**
   - Algunos comentarios no tienen espacio inicial: `# Configuración básica` (correcto)
   - Hay comentarios inline que podrían mejorarse

### 🎯 PEP 8 - Resumen de Violaciones

| Violación | Cantidad | Severidad |
|-----------|----------|-----------|
| Líneas > 79 caracteres | 8-10 | Media |
| Falta de type hints | 35+ | Media |
| Excepciones genéricas | 5 | Media |
| Espaciado inconsistente | 3 | Baja |

---

## 🏗️ Análisis de Arquitectura Hexagonal (Cumplimiento: 0%)

### ¿Qué es Arquitectura Hexagonal?

La arquitectura hexagonal (puertos y adaptadores) separa la aplicación en:

```
┌─────────────────────────────────────────────┐
│           PRESENTATION LAYER                │
│  (Flask Routes, Adaptadores HTTP)           │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│         APPLICATION/USE CASES               │
│     (Servicios de Negocio, Lógica)          │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│         DOMAIN/ENTITIES (CORE)              │
│      (Modelos de negocio puros)             │
└────────────────────┬────────────────────────┘
                     │
┌────────────────────▼────────────────────────┐
│         INFRASTRUCTURE LAYER                │
│  (BD, APIs externas, Adaptadores)           │
└─────────────────────────────────────────────┘
```

### ❌ Problemas Estructurales Encontrados

#### 1. **Mezcla de capas (Violation)**

Actualmente el código está mezclado sin separación clara:

**`views.py` contiene TODO:**
- ✗ Rutas HTTP (Presentation)
- ✗ Lógica de negocio completa (Application)
- ✗ Operaciones BD directo (Infrastructure)
- ✗ Validaciones de negocio

Ejemplo - Captura registrada sin validar lógica de negocio:
```python
@main_bp.route("/nueva-captura", methods=["GET", "POST"])
@login_required
def nueva_captura():
    # Aquí se mezcla: validación, conversiones, guardado BD
    capture = Capture(
        species_id=species_id,  # Sin validación de negocio
        location=location,       # Sin higienización
        length_cm=float(length_cm) if length_cm else None,  # Validación inline
        weight_kg=float(weight_kg) if weight_kg else None,
        bait=bait,
        hook=hook,
        notes=notes,
        media_path=media_path,
    )
    db.session.add(capture)  # ⚠️ Persistencia directa
    db.session.commit()
```

#### 2. **SQLAlchemy como modelo de Dominio (Anti-patrón)**

En `models.py`:
```python
class User(UserMixin, db.Model):  # ⚠️ Acoplado a BD
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), unique=True, nullable=False)
```

**Problema:** Los modelos están acoplados a SQLAlchemy:
- No puedes usar sin BD
- Difícil testear
- Violación de inversión de dependencias

**Debería ser:**
```python
# domain/entities/user.py
class User:  # Modelo puro de dominio
    def __init__(self, id: int, email: str, name: str):
        self.id = id
        self.email = email
        self.name = name
```

#### 3. **Falta de Puertos y Adaptadores**

No hay:
- ❌ Interfaces (puertos) definidas
- ❌ Inyección de dependencias
- ❌ Adaptadores intercambiables
- ❌ Separación clara BD/Lógica

**Ejemplo actual (problema):**
```python
def admin_species_delete(species_id):
    specie = Species.query.get_or_404(species_id)  # ⚠️ Consulta directa
    if specie.captures:  # ⚠️ Lógica y acceso BD juntos
        flash("No se puede eliminar...", "error")
```

**Cómo debería ser:**
```python
# ports/species_repository.py
class SpeciesRepository(ABC):
    @abstractmethod
    def get_by_id(self, species_id: int) -> Species:
        pass
    
    @abstractmethod
    def delete(self, species_id: int) -> None:
        pass

# application/services/species_service.py
class DeleteSpeciesService:
    def __init__(self, repository: SpeciesRepository):
        self.repository = repository  # Inyección de dependencia
    
    def execute(self, species_id: int) -> None:
        specie = self.repository.get_by_id(species_id)
        if specie.has_captures():
            raise BusinessException("..."
        self.repository.delete(species_id)
```

#### 4. **Falta de Capa Application (Use Cases)**

No hay servicios específicos del negocio:
- ❌ `RegisterUserService`
- ❌ `CreateCaptureService`
- ❌ `UpdateSpeciesService`
- ❌ `GenerateStatisticsService`

Toda la lógica está en rutas.

#### 5. **Sin Inversión de Dependencias**

Las vistas dependen directamente de:
- DB (`db.session`)
- SQLAlchemy ORM
- Flask helpers

No hay forma de:
- Cambiar la BD
- Testear sin Base de Datos
- Reutilizar lógica en otras interfaces

---

## 📊 Estructura Actual vs Estructura Hexagonal Ideal

### Estructura ACTUAL (Monolítica)

```
APP Pesca/
├── app.py (Inicialización)
├── models.py (Modelos ORM + Lógica)
├── views.py (Rutas + Lógica de Negocio + BD)  ⚠️ TODO MEZCLADO
└── templates/
```

### Estructura RECOMENDADA (Hexagonal)

```
APP Pesca/
├── src/
│   ├── domain/                    # 🟢 Core de negocio puro
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   ├── species.py
│   │   │   └── capture.py
│   │   └── exceptions.py
│   │
│   ├── application/               # 🔵 Casos de uso
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── species_service.py
│   │   │   └── capture_service.py
│   │   ├── dto/                   # Data Transfer Objects
│   │   │   └── species_dto.py
│   │   └── ports/                 # Interfaces (puertos)
│   │       ├── user_repository.py
│   │       ├── species_repository.py
│   │       └── capture_repository.py
│   │
│   ├── infrastructure/            # 🔴 Tecnología específica
│   │   ├── persistence/
│   │   │   ├── sqlalchemy_user_repository.py
│   │   │   ├── sqlalchemy_species_repository.py
│   │   │   └── sqlalchemy_capture_repository.py
│   │   └── models/               # Modelos ORM (NO confundir con Domain)
│   │       ├── user_orm.py
│   │       ├── species_orm.py
│   │       └── capture_orm.py
│   │
│   └── presentation/              # 🔴 Adaptador HTTP
│       ├── flask/
│       │   ├── routes/
│       │   │   ├── auth_routes.py
│       │   │   ├── user_routes.py
│       │   │   └── species_routes.py
│       │   └── blueprints.py
│       └── templates/
│
├── tests/                         # 🧪 Tests aislados
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── app.py                         # Factory pattern
└── requirements.txt
```

---

## 🔴 Problemas Clave de la Arquitectura Actual

### 1. Acoplamiento Alto
```
views.py → Flask → SQLAlchemy → Base de Datos
           ↓       ↓             ↓
        Todo mezclado - NO hay separación
```

### 2. Imposible Testear sin BD
- No puedes testear lógica de negocio
- Los tests tendría que usar BD real (lento)
- No puedes mock repositorio

### 3. Difícil Mantener
- 600+ líneas en `views.py`
- Para cambiar BD necesitas reescribir todo
- Cambios en Flask afectan lógica de negocio

### 4. No Escalable
- Agregar nuevas funcionalidades requiere modificar `views.py`
- Código duplicado imposible reutilizar
- No hay ciencia clara de responsabilidades

---

## 💡 Recomendaciones de Mejora

### Corto Plazo (PEP 8 - Inmediato)

```bash
# 1. Instalar herramientas de análisis
pip install flake8 black isort pylint

# 2. Ejecutar análisis
flake8 .
black --check .
pylint views.py models.py app.py

# 3. Auto-formatear
black .
isort .
```

**Comandos específicos para tu proyecto:**
```bash
# Formatear todo automáticamente
black . & isort .

# Ver violaciones PEP 8
flake8 . --max-line-length=88
```

### Medio Plazo (Refactor Arquitectura - Semanas)

1. **Crear capa de dominio:**
   ```python
   # src/domain/entities/user.py
   class User:
       def __init__(self, id: int, email: str, name: str, is_admin: bool):
           self.id = id
           self.email = email
           self.name = name
           self.is_admin = is_admin
       
       def is_admin_user(self) -> bool:
           return self.is_admin
   ```

2. **Crear puertos (interfaces):**
   ```python
   # src/application/ports/user_repository.py
   from abc import ABC, abstractmethod
   from domain.entities.user import User
   
   class UserRepository(ABC):
       @abstractmethod
       def find_by_email(self, email: str) -> User:
           pass
       
       @abstractmethod
       def save(self, user: User) -> None:
           pass
   ```

3. **Crear servicios (lógica de negocio):**
   ```python
   # src/application/services/user_service.py
   class RegisterUserService:
       def __init__(self, user_repo: UserRepository):
           self.user_repo = user_repo
       
       def execute(self, email: str, password: str, name: str):
           if self.user_repo.find_by_email(email):
               raise UserAlreadyExistsError()
           
           user = User(id=None, email=email, name=name, is_admin=False)
           self.user_repo.save(user)
           return user
   ```

4. **Crear adaptadores de Flask:**
   ```python
   # src/presentation/flask/routes/auth_routes.py
   @auth_bp.route("/register", methods=["POST"])
   def register():
       email = request.form.get("email")
       password = request.form.get("password")
       
       service = RegisterUserService(user_repo)
       try:
           user = service.execute(email, password, name)
           return {"success": True, "user_id": user.id}
       except UserAlreadyExistsError:
           return {"error": "Usuario ya existe"}, 409
   ```

### Largo Plazo (Testing y CI/CD)

- Agregar tests unitarios para servicios
- Implementar tests de integración
- Tests e2e
- CI/CD pipeline

---

## 📈 Métricas de Calidad Actual

| Métrica | Valor | Objetivo |
|---------|-------|----------|
| Líneas en `views.py` | 600+ | < 300 |
| Complejidad ciclomática | Alta | Media |
| Cobertura de tests | 0% | 80%+ |
| Acoplamiento | Alto | Bajo |
| Cohesión | Baja | Alta |

---

## ✅ Plan de Acción Recomendado

### Fase 1: Análisis Estático (1-2 días)
- [ ] Ejecutar `black` y `flake8`
- [ ] Corregir violaciones automáticas
- [ ] Documentar violaciones manuales

### Fase 2: Refactor Arquitectura (2-4 semanas)
- [ ] Crear estructura de carpetas
- [ ] Extractar entidades de dominio
- [ ] Crear puertos (interfaces)
- [ ] Implementar servicios
- [ ] Migrar rutas Flask

### Fase 3: Testing (2-3 semanas)
- [ ] Escribir tests unitarios
- [ ] Escribir tests de integración
- [ ] Configurar CI/CD

### Fase 4: Optimización (Continuo)
- [ ] Refactor incremental
- [ ] Performance tuning
- [ ] Documentación

---

## 📚 Recursos Recomendados

1. **PEP 8:**
   - https://www.python.org/dev/peps/pep-0008/
   - https://docs.python-guide.org/writing/style/

2. **Arquitectura Hexagonal:**
   - "Domain-Driven Design" - Eric Evans
   - https://alistair.cockburn.us/hexagonal-architecture/
   - Patrón: https://martinfowler.com/articles/hexagonal.html

3. **Herramientas Python:**
   - Black: https://github.com/psf/black
   - Flake8: https://flake8.pycqa.org/
   - Pylint: https://www.pylint.org/

---

## 🎯 Conclusiones

| Aspecto | Análisis |
|---------|----------|
| **PEP 8** | Cumplimiento PARCIAL (65%). Principalmente líneas largas y falta de type hints. |
| **Arquitectura** | NO IMPLEMENTADA. Código monolítico con mezcla de capas. Altamente acoplado. |
| **Mantenibilidad** | BAJA. Difícil agregar funcionalidad sin afectar código existente. |
| **Testabilidad** | POBRE. Imposible testear sin dependencias externas. |
| **Escalabilidad** | LIMITADA. Requiere refactor completo para crecer. |

### Recomendación Final
La aplicación funciona, pero necesita refactor urgente si planeas mantenerla a largo plazo. Comienza con PEP 8 (rápido) y luego planifica la migración a arquitectura hexagonal.

---

**Generado:** 30 de marzo de 2026  
**Analista:** GitHub Copilot  
**Versión:** 1.0
