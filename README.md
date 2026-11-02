# Sistema de Inventario — Segundo Parcial DevOps

**Asignatura:** Electiva DevOps  
**Evaluación:** Segundo parcial — Evolución del proyecto DevOps  
**Docente:** Ph.D. Angela María Vargas Arcila  
**Equipo:** 2  
**Repositorio:** https://github.com/Santi104/Parcial-1-DevOps

## Integrantes

- Maria del Mar Perez Montenegro
- Edi Santiago Monzon
- David Segundo Giron Acosta
- Ana Judith Velasquez Cañaveral

## 1. Descripción y funcionalidades

Aplicación web de gestión de inventario desarrollada con **Flask** y **PostgreSQL**. Conserva las operaciones CRUD del primer parcial y añade dos funcionalidades para el segundo parcial.

**Operaciones existentes:** registrar, consultar, editar y eliminar productos. Cada registro contiene ID, nombre, categoría, precio y cantidad.

**Nuevas funcionalidades:**

1. **Filtrado por categoría:** muestra únicamente los productos de la categoría seleccionada.
2. **Consulta de productos agotados:** muestra productos cuya cantidad es cero.

Ambos filtros pueden utilizarse conjuntamente y se aplican desde la interfaz web.

## 2. Tecnologías y arquitectura

| Componente | Tecnología |
|---|---|
| Aplicación web | Python 3.12, Flask, HTML5 y CSS3 |
| Base de datos | PostgreSQL 18 |
| Contenedores | Docker y Docker Compose |
| Pruebas | pytest |
| Versionamiento | Git y GitHub |
| Automatización | GitHub Actions |
| Registro de imágenes | GitHub Container Registry (GHCR) |

La aplicación se ejecuta en un contenedor `web` (Flask, puerto interno 5000), conectado mediante la red de Docker Compose a un contenedor `db` (PostgreSQL, puerto interno 5432). El navegador accede por **http://localhost:8080**. Los datos se conservan en el volumen `postgres_data`.

```text
Navegador (localhost:8080)
            |
            v
     web: Flask (5000)
            |
       Red Docker
            |
            v
   db: PostgreSQL (5432)
            |
            v
   Volumen postgres_data
```

## 3. Estructura del repositorio

```text
Parcial-1-DevOps/
├── .github/workflows/
│   ├── ci.yml
│   └── cd.yml
├── tests/
│   ├── test_filtros.py
│   ├── test_integracion.py
│   └── test_postgresql.py
├── templates/
│   ├── index.html
│   └── editar.html
├── static/
│   ├── style.css
│   └── logo.png
├── app.py
├── database.py
├── filtros.py
├── init.sql
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
└── README.md
```

`app.py` contiene las rutas y operaciones CRUD; `database.py` gestiona las conexiones y consultas a PostgreSQL; `filtros.py` implementa los filtros; `init.sql` define la tabla inicial; y los archivos de `.github/workflows/` automatizan las pruebas y la publicación de la imagen.

## 4. Instalación y ejecución local

**Requisito:** Docker con Docker Compose disponible y en ejecución.

Clonar el repositorio:

```bash
git clone https://github.com/Santi104/Parcial-1-DevOps.git
cd Parcial-1-DevOps
```

Construir e iniciar los servicios:

```bash
docker compose up -d --build
```

Comprobar los contenedores:

```bash
docker compose ps
```

Abrir **http://localhost:8080** y utilizar el formulario de registro, la tabla de productos y los filtros.

Detener los servicios sin eliminar el volumen de datos:

```bash
docker compose down
```

Volver a iniciarlos:

```bash
docker compose up -d
```

**Persistencia:** el volumen `postgres_data` conserva los registros entre reinicios. No ejecutar `docker compose down -v` si se desea mantener la información.

### Variables de conexión

El archivo `docker-compose.yml` configura los siguientes valores para el entorno académico:

| Variable | Valor |
|---|---|
| `DB_HOST` | `db` |
| `DB_NAME` | `inventario` |
| `DB_USER` | `postgres` |
| `DB_PASSWORD` | `postgres` |

Estas credenciales son únicamente para desarrollo y demostración; no deben reutilizarse en producción.

## 5. Pruebas automatizadas

El proyecto cuenta con **12 pruebas** distribuidas así:

| Archivo | Cantidad | Comprobaciones |
|---|---:|---|
| `tests/test_filtros.py` | 7 | Filtros por categoría y agotados, combinación, ausencia de coincidencias y conservación de datos originales |
| `tests/test_integracion.py` | 4 | Respuestas HTTP de Flask y representación HTML con filtros; emplean datos simulados |
| `tests/test_postgresql.py` | 1 | Integración real de Flask con PostgreSQL: registrar, consultar, editar y eliminar un producto |
| **Total** | **12** | |

Las pruebas de filtros y HTTP también permiten comprobar que las nuevas modificaciones no alteran los comportamientos esperados (regresión). La prueba de CRUD verifica las operaciones originales contra una base PostgreSQL real.

### Ejecutar las pruebas con PostgreSQL en Docker

La prueba real utiliza una base **separada** llamada `inventario_test`; no debe ejecutarse contra `inventario`.

Con los servicios iniciados, crear la base de pruebas **una sola vez**:

```bash
docker compose exec db psql -U postgres -d postgres -c "CREATE DATABASE inventario_test;"
```

Si la base ya existe, omitir ese comando. Crear la tabla de pruebas (puede ejecutarse más de una vez):

```bash
docker compose exec db psql -U postgres -d inventario_test -c "CREATE TABLE IF NOT EXISTS productos (id SERIAL PRIMARY KEY, nombre VARCHAR(100) NOT NULL, categoria VARCHAR(100) NOT NULL, precio NUMERIC(10,2) NOT NULL, cantidad INTEGER NOT NULL);"
```

La imagen de aplicación se orienta a ejecutar Flask. Para realizar una prueba puntual dentro del contenedor, instalar pytest en ese contenedor:

```bash
docker compose exec web python -m pip install "pytest>=8,<10"
```

Como el `Dockerfile` copia los archivos al construir la imagen, **reconstruir `web` después de añadir o actualizar pruebas** para que el contenedor contenga los archivos más recientes:

```bash
docker compose up -d --build web
```

Si se reconstruye `web`, reinstalar pytest en el contenedor nuevo:

```bash
docker compose exec web python -m pip install "pytest>=8,<10"
```

Ejecutar las 12 pruebas con la base aislada:

```bash
docker compose exec -e DB_NAME=inventario_test -e TEST_DB_NAME=inventario_test web python -m pytest -v
```

**Resultado verificado:** `12 passed`. La instalación de pytest dentro del contenedor es temporal; la ejecución automatizada de CI instala las dependencias desde `requirements.txt`.

## 6. Integración continua en GitHub Actions

**Archivo:** `.github/workflows/ci.yml`  
**Workflow:** `Pruebas automaticas`

Se ejecuta al abrir o actualizar un Pull Request dirigido a `main` y al hacer `push` a `main`. El flujo implementado:

1. Descarga el repositorio.
2. Configura Python 3.11 e instala `requirements.txt`.
3. Inicia PostgreSQL 18 como servicio con la base `inventario_test`.
4. Prepara la tabla `productos` y las variables de conexión de pruebas.
5. Ejecuta `python -m pytest -v` y muestra los resultados.

Se verificaron **12 pruebas aprobadas** tanto en el Pull Request de integración como después de fusionarlo a `main`.

### Demostración de fallo y corrección

Se creó una rama temporal `prueba-fallo-ci` y un Pull Request de demostración. Se modificó intencionalmente una afirmación de `tests/test_filtros.py`, sin alterar el código de la aplicación.

| Momento | Commit | Resultado de CI |
|---|---|---|
| Prueba intencionalmente incorrecta | `283f676` | **1 failed, 11 passed** |
| Afirmación corregida | `43d9ed4` | **12 passed** |

La demostración quedó registrada en el historial de GitHub Actions. El Pull Request de demostración se cerró **sin fusionarlo**; el código correcto permaneció en `main`.

**Evidencia:** [Ejecuciones de GitHub Actions](https://github.com/Santi104/Parcial-1-DevOps/actions).

## 7. Entrega continua y publicación de la imagen

**Archivo:** `.github/workflows/cd.yml`  
**Workflow:** `Entrega continua - Docker y GHCR`

Después de un CI exitoso correspondiente a un `push` a `main`, el workflow construye la imagen a partir del `Dockerfile` y la publica en GHCR, con la etiqueta `latest` y otra asociada al commit.

**Imagen publicada:**

```text
ghcr.io/santi104/parcial-1-devops:latest
```

Tras la integración de las pruebas PostgreSQL en `main`, se verificó que tanto CI como CD finalizaron correctamente.

### Descargar y ejecutar la imagen de GHCR

Con los servicios de Docker Compose en funcionamiento, descargar la imagen:

```bash
docker pull ghcr.io/santi104/parcial-1-devops:latest
```

Comprobar su presencia:

```bash
docker image ls ghcr.io/santi104/parcial-1-devops
```

Iniciar una segunda instancia de la aplicación usando la imagen **descargada**, en el puerto `8081`:

```bash
docker run -d --name inventario-ghcr-prueba \
  --network parcial-1-devops_default \
  -p 8081:5000 \
  -e DB_HOST=db \
  -e DB_NAME=inventario \
  -e DB_USER=postgres \
  -e DB_PASSWORD=postgres \
  ghcr.io/santi104/parcial-1-devops:latest
```

> El nombre de red `parcial-1-devops_default` corresponde al nombre de proyecto Docker Compose utilizado en esta demostración; puede variar si la carpeta o el nombre del proyecto cambian. La segunda instancia comparte la base de datos del entorno local, por lo que cualquier modificación de productos afecta a ese inventario.

Verificar el contenedor y abrir **http://localhost:8081**:

```bash
docker ps --filter name=inventario-ghcr-prueba
```

Se comprobó que la página cargaba correctamente, mostraba los productos y presentaba los filtros nuevos.

Detener y eliminar **solo** el contenedor de demostración:

```bash
docker stop inventario-ghcr-prueba
docker rm inventario-ghcr-prueba
```

Esto no elimina la imagen descargada ni detiene los servicios de Docker Compose.

## 8. Archivos de configuración y trabajo colaborativo

El entorno reproducible del proyecto se configura con `Dockerfile`, `docker-compose.yml` y `init.sql`: imagen de Flask, servicios web y PostgreSQL, variables de entorno, red interna, inicialización de la tabla y volumen persistente. **No se implementó Terraform.**

El equipo trabajó con ramas de funcionalidades y Pull Requests hacia `main`, incluyendo `feature-aplicacion`, `feature-base-datos`, `feature-docker`, `feature-compose` y `feature-pruebas-postgresql`. Los cambios se integraron después de comprobar los resultados de GitHub Actions.

## 9. Distribución del trabajo

| Integrante | Trabajo registrado en la organización inicial |
|---|---|
| Ana Judith Velasquez Cañaveral | Aplicación |
| Maria del Mar Perez Montenegro | Base de datos |
| Edi Santiago Monzon | Docker |
| David Segundo Giron Acosta | Docker Compose |

El segundo parcial incorporó adicionalmente filtros, pruebas, automatización CI/CD y publicación de la imagen en GHCR como trabajo del equipo.
