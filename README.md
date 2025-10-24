# Sistema de Profesores - Flask MVC

Una aplicación web desarrollada en Python Flask que implementa el patrón MVC (Model-View-Controller) para gestionar información de profesores con conexión a base de datos PostgreSQL.

## 🏗️ Arquitectura

La aplicación sigue el patrón MVC con las siguientes capas:

- **Models**: Entidades de base de datos (`app/models/`)
- **Views**: Templates HTML (`app/templates/`)
- **Controllers**: Controladores de rutas (`app/controllers/`)
- **Services**: Lógica de negocio (`app/services/`)
- **Repository**: Acceso a datos (`app/repositories/`)

## 📁 Estructura del Proyecto

```
lab-05/
├── app/
│   ├── __init__.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── profesor_controller.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── profesor.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── profesor_repository.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── profesor_service.py
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   └── templates/
│       ├── base.html
│       └── profesores/
│           ├── index.html
│           ├── create.html
│           ├── show.html
│           └── edit.html
├── config.py
├── requirements.txt
├── run.py
├── init_db.py
├── database.sql
├── .gitignore
└── README.md
```

## 🚀 Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd lab-05
```

### 2. Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar MySQL

1. Instalar MySQL Server
2. Crear la base de datos:

```bash
mysql -u root -p
```

```sql
CREATE DATABASE lab_05;
USE lab_05;
\q
```

3. Ejecutar el script SQL:

```bash
mysql -u root -p lab_05 < database.sql
```

### 5. Configurar variables de entorno

Crear archivo `.env` basado en `.env.example`:

```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:

```
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/lab_05
DB_USER=root
DB_PASSWORD=password
DB_PORT=3306
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True
```

### 6. Inicializar la base de datos

```bash
python init_mysql.py
```

### 7. Ejecutar la aplicación

```bash
python run.py
```

La aplicación estará disponible en: http://localhost:5000

## 📊 Funcionalidades

### CRUD de Profesores

- ✅ **Crear** nuevo profesor
- ✅ **Leer** lista de profesores
- ✅ **Actualizar** información de profesor
- ✅ **Eliminar** profesor (soft delete)

### Campos del Modelo Profesor

- ID (auto-incremento)
- Nombre
- Apellido
- DNI (único)
- Email (único)
- Teléfono
- Especialidad
- Título Académico
- Estado activo/inactivo
- Fecha de registro

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python 3.x, Flask 2.3.3
- **Base de datos**: MySQL
- **ORM**: SQLAlchemy
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Iconos**: Font Awesome

## 📝 API Endpoints

### Web Routes

- `GET /profesores/` - Lista de profesores
- `GET /profesores/create` - Formulario crear profesor
- `POST /profesores/create` - Crear profesor
- `GET /profesores/<id>` - Ver detalles profesor
- `GET /profesores/<id>/edit` - Formulario editar profesor
- `POST /profesores/<id>/edit` - Actualizar profesor
- `POST /profesores/<id>/delete` - Eliminar profesor

### API Routes (JSON)

- `GET /profesores/api` - Lista profesores (JSON)
- `GET /profesores/api/<id>` - Obtener profesor (JSON)
- `POST /profesores/api` - Crear profesor (JSON)
- `PUT /profesores/api/<id>` - Actualizar profesor (JSON)
- `DELETE /profesores/api/<id>` - Eliminar profesor (JSON)

## 🔧 Desarrollo

### Ejecutar en modo desarrollo

```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
python run.py
```

### Estructura de la Base de Datos

```sql
CREATE TABLE profesor (
    profesor_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    dni VARCHAR(20) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    telefono VARCHAR(20),
    especialidad VARCHAR(100),
    titulo_academico VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    activo BOOLEAN DEFAULT TRUE NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 📄 Licencia

Este proyecto es de uso educativo y está disponible bajo la licencia MIT.

## 👨‍💻 Autor

Desarrollado como parte del Laboratorio 05 - Patrón MVC con Flask y PostgreSQL.
