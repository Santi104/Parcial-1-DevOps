# Sistema de Inventario — Proyecto Final DevOps

**Asignatura:** Electiva DevOps  
**Evaluación:** Proyecto final — Integración, seguridad y observabilidad DevOps
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

| Componente                     | Tecnología                             |
| ------------------------------ | -------------------------------------- |
| Aplicación web                 | Python 3.12, Flask 3.1.3, HTML5 y CSS3 |
| Base de datos                  | PostgreSQL 18                          |
| Contenedores                   | Docker y Docker Compose                |
| Pruebas automatizadas          | pytest                                 |
| Versionamiento y colaboración  | Git y GitHub                           |
| Integración y entrega continua | GitHub Actions                         |
| Registro de imágenes           | GitHub Container Registry (GHCR)       |
| Construcción multiplataforma   | Docker Buildx y QEMU (AMD64 y ARM64)   |
| Análisis de secretos           | Gitleaks                               |
| Análisis de vulnerabilidades   | Trivy                                  |
| Métricas de aplicación         | prometheus-client                      |
| Recolección de métricas        | Prometheus                             |
| Visualización y monitoreo      | Grafana                                |
| Registros de aplicación        | logging de Python                      |

La aplicación se ejecuta mediante **Docker Compose**, utilizando cuatro servicios conectados a través de una red interna:

- **`web`:** aplicación Flask, disponible en `http://localhost:8080` y con puerto interno `5000`.
- **`db`:** base de datos PostgreSQL 18, con puerto interno `5432` y persistencia mediante el volumen `postgres_data`.
- **`prometheus`:** recolecta las métricas HTTP de Flask desde `http://web:5000/metrics`, con un intervalo de 5 segundos. Su interfaz está disponible en `http://localhost:9090`.
- **`grafana`:** permite visualizar las métricas recolectadas por Prometheus mediante un dashboard de cuatro paneles. Está disponible en `http://localhost:3000` y conserva su configuración mediante el volumen `grafana_data`.

**Diagrama de arquitectura:**

```text
                  Navegador
                      |
             +--------+--------+
             |                 |
             v                 v
      localhost:8080     localhost:3000
             |                 |
             v                 v
       web: Flask          Grafana
        (5000)             (3000)
             |                 |
       +-----+-----+           |
       |           |           v
       v           v       Prometheus
  PostgreSQL    /metrics      (9090)
    (5432)         ^             |
       |           |             |
       v           +-------------+
 postgres_data      Recoleccion
                    cada 5 s

Grafana almacena su configuracion en grafana_data.
```

Los servicios se comunican mediante la red interna de Docker Compose. Los volúmenes permiten conservar los datos de PostgreSQL y la configuración de Grafana entre reinicios y recreaciones de los contenedores.

## 3. Estructura del repositorio

```text
Parcial-1-DevOps/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── cd.yml
├── tests/
│   ├── test_filtros.py
│   ├── test_integracion.py
│   └── test_postgresql.py
├── templates/
│   ├── index.html
│   └── editar.html
├── static/
│   ├── style.css
│   └── logo-devops.png
├── app.py
├── database.py
├── filtros.py
├── init.sql
├── Dockerfile
├── docker-compose.yml
├── prometheus.yml
├── grafana-dashboard.json
├── requirements.txt
├── pytest.ini
├── .gitignore
└── README.md
```

`app.py` contiene las rutas CRUD, la instrumentación de métricas HTTP y los registros de eventos de la aplicación. `database.py` gestiona la conexión y las consultas a PostgreSQL; `filtros.py` implementa los filtros; e `init.sql` define la tabla inicial.

El `Dockerfile` construye la imagen de Flask y `docker-compose.yml` configura los cuatro servicios. `prometheus.yml` define la recolección de métricas y `grafana-dashboard.json` contiene el dashboard exportado con cuatro paneles.

Los archivos de `.github/workflows/` automatizan las pruebas, el análisis de seguridad y la publicación de la imagen multiplataforma en GHCR. El directorio `tests/` contiene las pruebas automatizadas del proyecto.

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

Una vez iniciados los contenedores con `docker compose up -d --build`, comprobar que los cuatro servicios estén en ejecución mediante `docker compose ps`.

**Acceso a los servicios:**

| Servicio          | Dirección                     | Función                                                                    |
| ----------------- | ----------------------------- | -------------------------------------------------------------------------- |
| Inventario Flask  | http://localhost:8080         | Registrar, consultar, editar, eliminar y filtrar productos                 |
| Métricas de Flask | http://localhost:8080/metrics | Consultar las métricas HTTP expuestas por la aplicación                    |
| Prometheus        | http://localhost:9090         | Consultar las métricas recolectadas y verificar los objetivos de monitoreo |
| Grafana           | http://localhost:3000         | Visualizar el dashboard de observabilidad                                  |

Para comprobar la comunicación entre Flask y Prometheus, abrir `http://localhost:9090/targets` y verificar que el objetivo `flask-app` aparezca con estado **UP**.

En una instalación nueva, Grafana requiere configurar Prometheus como fuente de datos e importar el dashboard incluido en el repositorio. Este procedimiento se explica en la sección de observabilidad.

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

| Variable      | Valor        |
| ------------- | ------------ |
| `DB_HOST`     | `db`         |
| `DB_NAME`     | `inventario` |
| `DB_USER`     | `postgres`   |
| `DB_PASSWORD` | `postgres`   |

Estas credenciales son únicamente para desarrollo y demostración; no deben reutilizarse en producción.

### Configuración de Grafana e importación del dashboard

Después de iniciar los cuatro servicios con Docker Compose, realizar la configuración inicial de Grafana:

1. Abrir `http://localhost:3000`.
2. Iniciar sesión con las credenciales iniciales de Grafana (`admin` / `admin`) si se trata de una instalación nueva. Grafana puede solicitar cambiar la contraseña.
3. Ir a **Connections → Data sources → Add data source**.
4. Seleccionar **Prometheus**.
5. En la dirección del servidor Prometheus, ingresar `http://prometheus:9090`.
6. Seleccionar **Save & test** y comprobar que la conexión sea exitosa.
7. Ir a **Dashboards → New → Import** (la ubicación puede variar según la versión de Grafana).
8. Seleccionar el archivo `grafana-dashboard.json` incluido en la raíz del repositorio.
9. Si Grafana solicita seleccionar una fuente de datos, elegir la fuente **Prometheus** configurada anteriormente.
10. Completar la importación y abrir el dashboard **Monitoreo de Inventario DevOps**.

El dashboard contiene cuatro paneles: solicitudes HTTP por segundo, errores HTTP por segundo, solicitudes HTTP en curso y duración promedio de las solicitudes.

**Verificación:** abrir `http://localhost:8080`, navegar por el inventario y actualizar la página varias veces. Después, comprobar en Grafana que el panel de solicitudes HTTP registra actividad.

Para generar errores HTTP de prueba, visitar `http://localhost:8080/ruta-inexistente` varias veces y comprobar que aumenta el indicador de errores.

**Persistencia:** Grafana utiliza el volumen `grafana_data` para conservar su configuración, fuentes de datos y dashboards entre reinicios y recreaciones de contenedores. No ejecutar `docker compose down -v` si se desea conservar estos datos.

## 5. Pruebas automatizadas

El proyecto cuenta con **12 pruebas** distribuidas así:

| Archivo                     | Cantidad | Comprobaciones                                                                                              |
| --------------------------- | -------: | ----------------------------------------------------------------------------------------------------------- |
| `tests/test_filtros.py`     |        7 | Filtros por categoría y agotados, combinación, ausencia de coincidencias y conservación de datos originales |
| `tests/test_integracion.py` |        4 | Respuestas HTTP de Flask y representación HTML con filtros; emplean datos simulados                         |
| `tests/test_postgresql.py`  |        1 | Integración real de Flask con PostgreSQL: registrar, consultar, editar y eliminar un producto               |
| **Total**                   |   **12** |                                                                                                             |

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

El workflow `Pruebas automaticas`, definido en `.github/workflows/ci.yml`, se ejecuta automáticamente cuando se realiza un `push` a `main` o se abre o actualiza un Pull Request dirigido a `main`.

La integración continua incluye dos trabajos independientes:

**1. Pruebas automatizadas (`pruebas`)**

1. Descarga el código del repositorio.
2. Configura Python 3.11 e instala las dependencias de `requirements.txt`.
3. Inicia PostgreSQL 18 con una base de pruebas aislada llamada `inventario_test`.
4. Prepara la tabla `productos` y las variables de conexión.
5. Ejecuta `python -m pytest -v` para comprobar el funcionamiento de la aplicación.

**2. Análisis de secretos (`gitleaks`)**

1. Descarga el código del repositorio.
2. Ejecuta Gitleaks mediante un contenedor Docker.
3. Analiza los archivos del proyecto para detectar posibles secretos expuestos.
4. Utiliza `--redact` para ocultar los valores sensibles en los resultados y `--exit-code=1` para hacer fallar el trabajo cuando se detectan hallazgos.

Ambos trabajos forman parte de la integración continua. Sus resultados pueden consultarse en la pestaña **Actions** del repositorio de GitHub.

El análisis de Gitleaks utiliza la opción `--no-git`, por lo que examina los archivos del repositorio descargado y no todo su historial de commits.

Se verificaron **12 pruebas aprobadas** tanto en el Pull Request de integración como después de fusionarlo a `main`.

### Demostración de fallo y corrección

Se creó una rama temporal `prueba-fallo-ci` y un Pull Request de demostración. Se modificó intencionalmente una afirmación de `tests/test_filtros.py`, sin alterar el código de la aplicación.

| Momento                            | Commit    | Resultado de CI         |
| ---------------------------------- | --------- | ----------------------- |
| Prueba intencionalmente incorrecta | `283f676` | **1 failed, 11 passed** |
| Afirmación corregida               | `43d9ed4` | **12 passed**           |

La demostración quedó registrada en el historial de GitHub Actions. El Pull Request de demostración se cerró **sin fusionarlo**; el código correcto permaneció en `main`.

**Evidencia:** [Ejecuciones de GitHub Actions](https://github.com/Santi104/Parcial-1-DevOps/actions).

## 7. Entrega continua y publicación de la imagen

**Archivo:** `.github/workflows/cd.yml`  
**Workflow:** `Entrega continua - Docker y GHCR`

El workflow `Entrega continua - Docker y GHCR`, definido en `.github/workflows/cd.yml`, se activa cuando finaliza el workflow `Pruebas automaticas` de la rama `main`.

La entrega continua solamente continúa si la ejecución de CI terminó correctamente y fue originada por un `push` a `main`.

El proceso se divide en dos trabajos:

**1. Verificación de seguridad de las imágenes (`verificar-imagen`)**

1. Descarga el código correspondiente al commit que activó el proceso.
2. Configura Docker Buildx y QEMU para trabajar con diferentes arquitecturas.
3. Construye imágenes de análisis para `linux/amd64` y `linux/arm64`.
4. Ejecuta Trivy sobre cada imagen para detectar vulnerabilidades del sistema operativo y las bibliotecas.
5. Analiza vulnerabilidades de severidad `HIGH` y `CRITICAL`, utilizando `ignore-unfixed: true` para excluir aquellas que no tienen una corrección disponible.
6. Hace fallar el trabajo cuando Trivy detecta vulnerabilidades que cumplen las condiciones configuradas.

**2. Publicación de la imagen (`publicar-imagen`)**

Este trabajo depende de que `verificar-imagen` finalice correctamente. Si falla el análisis de seguridad de alguna arquitectura, no se ejecuta la publicación.

Cuando las verificaciones son satisfactorias:

1. Descarga el código del commit correspondiente.
2. Configura QEMU y Docker Buildx.
3. Inicia sesión en GitHub Container Registry mediante `GITHUB_TOKEN`.
4. Construye y publica una imagen multiplataforma compatible con `linux/amd64` y `linux/arm64`.
5. Publica dos etiquetas: `latest` y otra identificada con el SHA del commit.

De esta manera, el flujo de entrega continua integra la construcción multiplataforma, el análisis de vulnerabilidades con Trivy y la publicación de imágenes en GHCR.

**Evidencias:** los resultados de las verificaciones y de la publicación pueden consultarse en [GitHub Actions](https://github.com/Santi104/Parcial-1-DevOps/actions). Durante la revisión final se comprobará la ejecución correspondiente a la versión entregada.

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

| Integrante                     | Trabajo registrado en la organización inicial |
| ------------------------------ | --------------------------------------------- |
| Ana Judith Velasquez Cañaveral | Aplicación                                    |
| Maria del Mar Perez Montenegro | Base de datos                                 |
| Edi Santiago Monzon            | Docker                                        |
| David Segundo Giron Acosta     | Docker Compose                                |

El segundo parcial incorporó adicionalmente filtros, pruebas, automatización CI/CD y publicación de la imagen en GHCR como trabajo del equipo.

## 10. Observabilidad: logs y métricas HTTP

La aplicación Flask incorpora mecanismos de observabilidad para registrar operaciones importantes, medir el comportamiento de las solicitudes HTTP y facilitar el monitoreo mediante Prometheus y Grafana.

### 10.1. Logs de la aplicación

Se utiliza el módulo `logging` de Python con nivel `INFO` y un formato que incluye:

- Fecha y hora del evento.
- Nivel de severidad.
- Nombre del componente que genera el registro.
- Mensaje con información contextual de la operación.

El formato configurado es:

```python
"%(asctime)s %(levelname)s [%(name)s] %(message)s"
```

La aplicación genera registros informativos durante las operaciones de inventario, lo que permite consultar su actividad desde los logs del contenedor.

Para visualizar los registros en tiempo real:

```bash
docker compose logs -f web
```

Para salir de la visualización, presionar `Ctrl + C`. Esto no detiene el contenedor.

### 10.2. Métricas HTTP de Flask

La aplicación utiliza la biblioteca `prometheus-client` y expone sus métricas en:

`http://localhost:8080/metrics`

Se implementaron cuatro instrumentos:

| Métrica                         | Tipo      | Descripción                                                                  |
| ------------------------------- | --------- | ---------------------------------------------------------------------------- |
| `http_requests_total`           | Counter   | Cuenta las solicitudes HTTP recibidas.                                       |
| `http_errors_total`             | Counter   | Cuenta las respuestas HTTP con códigos de estado iguales o superiores a 400. |
| `http_requests_in_progress`     | Gauge     | Mide las solicitudes HTTP que se encuentran en procesamiento.                |
| `http_request_duration_seconds` | Histogram | Registra la duración de las solicitudes HTTP en segundos.                    |

Los contadores de solicitudes y errores utilizan las etiquetas `method`, `endpoint` y `http_status`. El indicador de solicitudes en curso y el histograma utilizan `method` y `endpoint`.

La instrumentación se realiza mediante los mecanismos `before_request` y `after_request` de Flask, que permiten registrar el inicio y la finalización de las solicitudes.

La ruta `/metrics` se excluye de estas mediciones HTTP para evitar que las consultas periódicas de Prometheus alteren los indicadores de actividad de la aplicación.

### 10.3. Recolección de métricas con Prometheus

El servicio `prometheus` se configura mediante el archivo `prometheus.yml`, ubicado en la raíz del repositorio.

La configuración define:

- Intervalo de recolección: 5 segundos.
- Nombre del trabajo: `flask-app`.
- Objetivo interno: `web:5000`.
- Ruta de métricas: `/metrics`.

Para verificar su funcionamiento:

1. Iniciar los servicios con `docker compose up -d --build`.
2. Abrir `http://localhost:9090/targets`.
3. Confirmar que el objetivo `flask-app` aparece con estado `UP`.
4. Abrir la interfaz de consultas de Prometheus y ejecutar `http_requests_total`.
5. Comprobar que se muestran series de métricas después de generar solicitudes a la aplicación.

### 10.4. Visualización con Grafana

Grafana se conecta a Prometheus mediante la dirección interna:

`http://prometheus:9090`

El dashboard **Monitoreo de Inventario DevOps** contiene cuatro paneles:

| Panel                                 | Consulta PromQL                                                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------- |
| Solicitudes HTTP por segundo          | `sum(rate(http_requests_total[1m]))`                                                |
| Errores HTTP por segundo              | `sum(rate(http_errors_total[1m]))`                                                  |
| Solicitudes HTTP en curso             | `sum(http_requests_in_progress)`                                                    |
| Duración promedio de solicitudes HTTP | `sum(http_request_duration_seconds_sum) / sum(http_request_duration_seconds_count)` |

El último panel muestra el promedio acumulado de duración de las solicitudes observadas, expresado en segundos.

El dashboard se encuentra exportado en `grafana-dashboard.json`. Las instrucciones para importarlo en otra instancia de Grafana están documentadas en la sección 4.

### 10.5. Demostración del monitoreo

Para comprobar que las métricas responden a la actividad real:

1. Abrir el inventario en `http://localhost:8080`.
2. Actualizar la página varias veces y realizar operaciones de consulta.
3. Abrir Grafana en `http://localhost:3000` y observar el panel **Solicitudes HTTP por segundo**.
4. Visitar varias veces `http://localhost:8080/ruta-inexistente` para generar respuestas HTTP `404`.
5. Comprobar que el panel **Errores HTTP por segundo** registra actividad.
6. Revisar los demás paneles para observar las solicitudes en curso y la duración promedio.
7. Consultar los logs mediante `docker compose logs web`.

Las métricas de tasa utilizan una ventana de un minuto, por lo que sus valores pueden disminuir cuando deja de generarse tráfico.

La configuración del dashboard se conserva mediante el volumen `grafana_data` de Docker Compose.

## 11. Flujo DevOps integrado

El proyecto integra desarrollo, pruebas, seguridad, entrega continua y observabilidad mediante el siguiente flujo:

1. Un integrante desarrolla una funcionalidad en una rama de trabajo y realiza un commit.
2. Los cambios se integran a la rama `main` mediante GitHub.
3. GitHub Actions ejecuta el workflow de integración continua (`ci.yml`), que prepara PostgreSQL, instala las dependencias, ejecuta las pruebas automatizadas y analiza posibles secretos expuestos mediante Gitleaks.
4. Cuando la ejecución de CI finaliza correctamente después de un `push` a `main`, se activa el workflow de entrega continua (`cd.yml`).
5. El workflow de CD construye imágenes para las arquitecturas `linux/amd64` y `linux/arm64` y las analiza con Trivy. Si el análisis detecta vulnerabilidades que incumplen los criterios configurados, se detiene la publicación.
6. Si las verificaciones son satisfactorias, GitHub Actions publica la imagen en GitHub Container Registry (GHCR), utilizando las etiquetas `latest` y el SHA del commit.
7. La aplicación puede ejecutarse mediante Docker. Durante su funcionamiento genera logs estructurados y expone métricas HTTP en `/metrics`.
8. Prometheus recopila las métricas y Grafana permite visualizar solicitudes, errores, concurrencia y duración de las peticiones.

Este flujo permite relacionar los cambios de código con las pruebas, los controles de seguridad, la versión publicada de la imagen y el comportamiento observable de la aplicación.

## 12. Evidencias y demostración del proyecto

Las evidencias se organizan en la carpeta `evidencias/` del repositorio. Las capturas corresponden a ejecuciones reales de las herramientas utilizadas.

| Evidencia                                               | Archivo                                                             |
| ------------------------------------------------------- | ------------------------------------------------------------------- |
| Aplicación funcionando                                  | `evidencias/01-aplicacion.png`                                      |
| Pruebas automatizadas satisfactorias                    | `evidencias/02-pruebas.png`                                         |
| Integración continua en GitHub Actions                  | `evidencias/03-ci.png`                                              |
| Análisis de secretos con Gitleaks                       | `evidencias/04-gitleaks.png`                                        |
| Análisis de vulnerabilidades con Trivy                  | `evidencias/05-trivy-parte1.png`, `evidencias/05-trivy-parte2.png` y `evidencias/05-trivy-parte3.png`|
| Entrega continua y publicación automática | `evidencias/06-cd-parte1.png` y `evidencias/06-cd-parte2.png`                     |
| Imagen publicada en GHCR con sus etiquetas              | `evidencias/07-ghcr.png`                                            |
| Logs de operaciones y errores de Flask                  | `evidencias/08-logs.png`                                            |
| Endpoint de métricas de Prometheus                      | `evidencias/09-metrics.png`                                         |
| Objetivo de Prometheus en estado UP                     | `evidencias/10-prometheus.png`                                      |
| Dashboard de Grafana con los cuatro paneles             | `evidencias/11-grafana.png`                                         |
| Dashboard mostrando actividad por solicitudes y errores | `evidencias/12-grafana-trafico.png`                                 |

### Demostración en vivo

Durante la sustentación se mostrará la aplicación funcionando, la ejecución de pruebas, los workflows de GitHub Actions, la imagen publicada en GHCR, los resultados de seguridad, la consulta de logs y el dashboard de Grafana.

Para demostrar la observabilidad se realizarán solicitudes a la aplicación y se generarán respuestas HTTP `404`, comprobando que los registros y las métricas reflejan esa actividad.

Las capturas complementan la demostración, pero no sustituyen la ejecución en vivo de los componentes.

**Nota:** los nombres de las capturas deben coincidir con los archivos que realmente se incorporen a `evidencias/`. Las evidencias de la ejecución final de CI/CD y GHCR se obtendrán después de integrar los cambios en `main`.
