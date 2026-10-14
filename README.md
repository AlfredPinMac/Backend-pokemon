# Pokémon Backend API (JWT Protected)

RESTful backend API developed with **FastAPI** for managing Pokémon data, secured using **Bearer Token (JWT)** authentication.

## Features

- **Secured REST Endpoints**:
  - `GET /api/pokemons`: Retrieves the Pokémon list (requires Bearer Token).
  - `POST /api/pokemons`: Creates a new Pokémon entry (requires Bearer Token).
  - `GET /api/pokemons/{id}`: Retrieves details for a specific Pokémon (requires Bearer Token).
  - `DELETE /api/pokemons/{id}`: Deletes a Pokémon by ID (requires Bearer Token).
  - `GET /health`: Public healthcheck endpoint.
- **Bearer Token Verification**: Middleware/dependency that ensures presence of `Authorization: Bearer <JWT>`, validating cryptographic signature and expiration.
- **Fail2Ban DDoS Mitigation**: Embedded rate logging and `fail2ban` jail monitoring on port 5000.
- **CORS Enabled**: Configured to interact seamlessly with Vue.js/Vite frontend clients.

## Requirements

- Python 3.10+ or Docker

## Local Setup and Execution

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows PowerShell
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   python run.py
   # Or directly with Uvicorn:
   uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
   ```

The server will be available at `http://localhost:5000`.
Interactive Swagger documentation: `http://localhost:5000/docs`

## Docker Execution

```bash
docker build -t pokemon-backend .
docker run --cap-add=NET_ADMIN --cap-add=NET_RAW -p 5000:5000 pokemon-backend
```
