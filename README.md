# Pokémon Backend API (JWT Protected)

Backend REST API desarrollado con **FastAPI** para la gestión de un listado de Pokémones, protegido mediante autenticación con **Bearer Token (JWT)**.

## Características

- **Endpoints REST protegidos**:
  - `GET /api/pokemons`: Obtiene el listado de Pokémones (requiere Bearer Token).
  - `POST /api/pokemons`: Da de alta un nuevo Pokémon (requiere Bearer Token).
  - `GET /api/pokemons/{id}`: Obtiene el detalle de un Pokémon específico (requiere Bearer Token).
  - `DELETE /api/pokemons/{id}`: Elimina un Pokémon por su ID (requiere Bearer Token).
  - `GET /health`: Healthcheck público.
- **Validación de Bearer Token**: Middleware/dependencia que valida la existencia del encabezado `Authorization: Bearer <JWT>` y verifica su firma y expiración.
- **CORS Habilitado**: Permite la interacción con el cliente Frontend (Vue.js / Vite).

## Requisitos

- Python 3.10+ o Docker

## Instalación y Ejecución Local

1. Crear entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # En Windows PowerShell
   ```

2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Ejecutar servidor de desarrollo:
   ```bash
   python run.py
   # O directamente con uvicorn:
   uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
   ```

El servidor estará disponible en `http://localhost:5000`.
Documentación interactiva Swagger: `http://localhost:5000/docs`

## Ejecución con Docker

```bash
docker build -t pokemon-backend .
docker run -p 5000:5000 pokemon-backend
```
