# Sistema de Inventario - DevOps

**Equipo: 2** 

Proyecto desarrollado para el **Primer Parcial – DevOps (Electiva)**.

---

## 2. Integrantes

- [Maria del Mar Perez Montenegro]
- [Edi Santiago Monzon]
- [David Segundo Giron Acosta]
- [Ana Judith Velasquez Cañaveral]

---

## 3. Descripción

El proyecto consiste en una aplicación web para la gestión de un inventario de productos.

La aplicación permite realizar las operaciones principales de un CRUD:

- Crear productos.
- Consultar productos.
- Editar productos.
- Eliminar productos.

Cada producto contiene la siguiente información:

- ID
- Nombre
- Categoría
- Precio
- Cantidad

La aplicación fue desarrollada utilizando Flask como framework web, PostgreSQL como sistema de gestión de base de datos y Docker y Docker Compose para la ejecución de los servicios mediante contenedores.

---

## 4. Tecnologías utilizadas

Las principales tecnologías utilizadas en el proyecto son:

- **Python 3.12**
- **Flask**
- **PostgreSQL 18**
- **HTML5**
- **CSS3**
- **Docker**
- **Docker Compose**
- **Git**
- **GitHub**

---

## 5. Arquitectura

La solución está compuesta principalmente por dos servicios:

1. **Web:** Contenedor encargado de ejecutar la aplicación desarrollada con Flask.
2. **Base de datos:** Contenedor encargado de ejecutar PostgreSQL.

Los dos servicios se comunican mediante la red creada por Docker Compose.

La base de datos utiliza un volumen Docker para mantener la información almacenada aunque los contenedores sean detenidos y posteriormente iniciados nuevamente.

### Diagrama de arquitectura

```text
                  ┌──────────────────────┐
                  │      Navegador       │
                  │                      │
                  │   localhost:8080     │
                  └──────────┬───────────┘
                             │
                             │ HTTP
                             ▼
                  ┌──────────────────────┐
                  │    Contenedor Web    │
                  │                      │
                  │    Python + Flask    │
                  │      Puerto 5000     │
                  └──────────┬───────────┘
                             │
                             │ Red Docker
                             ▼
                  ┌──────────────────────┐
                  │ Contenedor PostgreSQL│
                  │                      │
                  │    PostgreSQL 18     │
                  │      Puerto 5432     │
                  └──────────┬───────────┘
                             │
                             ▼
                  ┌──────────────────────┐
                  │    Docker Volume     │
                  │                      │
                  │    postgres_data     │
                  └──────────────────────┘

## 6. Estructura del proyecto

La estructura principal del proyecto es:

```text
inventario-devops/
│
├── app.py
├── database.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── init.sql
├── .dockerignore
├── .gitignore
├── README.md
│
├── templates/
│   ├── index.html
│   └── editar.html
│
└── static/
    ├── style.css
    └── logo.png
```

### Principales archivos y carpetas

| Archivo / Carpeta | Descripción |
|---|---|
| `app.py` | Contiene la aplicación Flask, sus rutas y las operaciones CRUD. |
| `database.py` | Contiene la configuración de conexión y consultas a PostgreSQL. |
| `requirements.txt` | Contiene las dependencias necesarias para ejecutar la aplicación Python. |
| `Dockerfile` | Define la imagen utilizada para ejecutar la aplicación Flask. |
| `docker-compose.yml` | Define los servicios de Flask y PostgreSQL, además de la configuración del volumen. |
| `init.sql` | Contiene la estructura inicial de la tabla `productos`. |
| `.dockerignore` | Define los archivos que no deben copiarse a la imagen Docker. |
| `.gitignore` | Define los archivos que no deben ser enviados al repositorio Git. |
| `templates/` | Contiene las plantillas HTML utilizadas por Flask. |
| `static/` | Contiene los archivos CSS e imágenes de la aplicación. |
| `README.md` | Contiene la documentación oficial del proyecto. |

---

## 7. Configuración

La aplicación utiliza variables de entorno para establecer la conexión entre Flask y PostgreSQL.

En el entorno de Docker Compose se utilizan las siguientes variables:

```env
DB_HOST=db
DB_NAME=inventario
DB_USER=postgres
DB_PASSWORD=postgres
```

### Descripción de las variables

| Variable | Descripción |
|---|---|
| `DB_HOST` | Nombre del servicio de PostgreSQL dentro de Docker Compose. |
| `DB_NAME` | Nombre de la base de datos utilizada por la aplicación. |
| `DB_USER` | Usuario utilizado para conectarse a PostgreSQL. |
| `DB_PASSWORD` | Contraseña del usuario de PostgreSQL. |

> **Importante:** El archivo `.env` utilizado para configuraciones locales no debe incluirse en el repositorio, ya que puede contener información sensible.

---

## 8. ¿Cómo ejecutar el proyecto?

Para ejecutar el proyecto desde cero, una persona que tenga acceso al repositorio puede seguir los siguientes pasos.

### 8.1 Clonar el repositorio

Ejecutar:

```bash
git clone https://github.com/Santi104/Parcial-1-DevOps.git
```

Ingresar a la carpeta del proyecto:

```bash
cd Parcial-1-DevOps
```

### 8.2 Verificar Docker

Es necesario tener Docker instalado y ejecutándose.

Comprobar la instalación con:

```bash
docker --version
```

Y:

```bash
docker compose version
```

### 8.3 Construir y ejecutar el proyecto

Para construir la imagen de la aplicación y levantar los servicios:

```bash
docker compose up --build
```

También se puede ejecutar en segundo plano:

```bash
docker compose up -d --build
```

Docker Compose iniciará los siguientes servicios:

- Aplicación web desarrollada con Flask.
- Base de datos PostgreSQL.

### 8.4 Acceder a la aplicación

Una vez iniciados los contenedores, abrir un navegador y acceder a:

```text
http://localhost:8080
```

Desde allí se podrá utilizar el sistema de inventario.

### 8.5 Detener los contenedores

Para detener los servicios:

```bash
docker compose down
```

Este comando detiene y elimina los contenedores, pero conserva el volumen de PostgreSQL.

### 8.6 Volver a iniciar el proyecto

Para iniciar nuevamente los servicios:

```bash
docker compose up -d
```

Los datos previamente almacenados permanecerán disponibles gracias al volumen `postgres_data`.

---

## 9. Git y trabajo colaborativo

El proyecto utiliza **Git** para el control de versiones y **GitHub** como plataforma para alojar el repositorio y facilitar el trabajo colaborativo.

El desarrollo se organizó utilizando diferentes *branches* para separar las principales partes del proyecto.

La estructura de trabajo definida es:

```text
main
│
├── feature-aplicacion
├── feature-base-datos
├── feature-docker
└── feature-compose
```

### `feature-aplicacion`

Branch destinada al desarrollo de la aplicación web, incluyendo:

- Aplicación Flask.
- Rutas.
- Operaciones CRUD.
- Plantillas HTML.
- Estilos CSS.
- Interfaz del sistema.

### `feature-base-datos`

Branch destinada al desarrollo relacionado con PostgreSQL, incluyendo:

- Configuración de la conexión.
- Archivo `database.py`.
- Archivo `init.sql`.
- Estructura de la tabla `productos`.

### `feature-docker`

Branch destinada a la configuración de Docker, incluyendo:

- `Dockerfile`.
- Imagen de la aplicación.
- Instalación de dependencias.
- Configuración del contenedor de la aplicación.

### `feature-compose`

Branch destinada a la configuración de Docker Compose, incluyendo:

- Servicio de Flask.
- Servicio de PostgreSQL.
- Comunicación entre los servicios.
- Variables de entorno.
- Volumen de PostgreSQL.

Los cambios desarrollados en las diferentes branches se integran posteriormente a `main` mediante **Pull Requests**.

### Repositorio

Repositorio oficial del proyecto:

https://github.com/Santi104/Parcial-1-DevOps

---

## 10. Persistencia

Para garantizar la persistencia de los datos de PostgreSQL se implementó un volumen Docker denominado:

```text
postgres_data
```

El volumen se declara en `docker-compose.yml`:

```yaml
volumes:
  postgres_data:
```

Y se utiliza en el servicio de PostgreSQL:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql
```

De esta forma, los datos de PostgreSQL se almacenan en el volumen y no dependen directamente del ciclo de vida del contenedor.

### Comprobación de persistencia

La persistencia se comprobó mediante el siguiente procedimiento:

1. Se iniciaron los servicios:

```bash
docker compose up -d
```

2. Se ingresó a la aplicación:

```text
http://localhost:8080
```

3. Se agregó un producto al inventario.

4. Se verificó que el producto apareciera correctamente en la aplicación.

5. Se detuvieron los contenedores:

```bash
docker compose down
```

6. Se iniciaron nuevamente los servicios:

```bash
docker compose up -d
```

7. Se ingresó nuevamente a:

```text
http://localhost:8080
```

8. Se comprobó que el producto continuaba registrado.

Con esta prueba se verificó que los datos permanecen almacenados después de detener y volver a iniciar los contenedores.

> **Importante:** No se debe utilizar `docker compose down -v` si se desea conservar la información almacenada, ya que este comando también elimina los volúmenes asociados al proyecto.

---

## 11. Estado del proyecto

El proyecto cuenta con las siguientes funcionalidades y componentes:

- [x] Aplicación web desarrollada con Flask.
- [x] Registro de productos.
- [x] Consulta de productos.
- [x] Edición de productos.
- [x] Eliminación de productos.
- [x] Base de datos PostgreSQL.
- [x] Dockerfile.
- [x] Docker Compose.
- [x] Comunicación entre Flask y PostgreSQL.
- [x] Variables de entorno.
- [x] Volumen para persistencia.
- [x] Control de versiones con Git.
- [x] Repositorio en GitHub.
- [x] Organización mediante branches.
- [x] Documentación mediante `README.md`.

---

## 12. Información académica

| Información | Detalle |
|---|---|
| **Asignatura** | Electiva DevOps |
| **Evaluación** | Primer Parcial – Mini Proyecto |
| **Docente** | Ph.D. Angela María Vargas Arcila |

---

## 13. Integrantes

| Integrante | Rol / Trabajo realizado |
|---|---|
| [Ana Judith Velasquez] | Desarrollo de la aplicación |
| [Maria del Mar Perez] | Base de datos |
| [Edi Santiago Monzon] | Docker |
| [David Giron] | Docker Compose |