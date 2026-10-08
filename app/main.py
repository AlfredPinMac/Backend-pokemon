import os
import logging
from typing import List, Optional

import jwt
from fastapi import FastAPI, HTTPException, Depends, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.models import Pokemon, PokemonCreate

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("pokemon-api")

app = FastAPI(
    title="Pokémon Backend API",
    description="Backend para gestión de Pokémon protegido por autenticación Bearer JWT",
    version="1.0.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Access log middleware for Fail2Ban HTTP Flood detection
@app.middleware("http")
async def fail2ban_access_log_middleware(request: Request, call_next):
    client_ip = request.client.host if request.client else "127.0.0.1"
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        client_ip = forwarded.split(",")[0].strip()

    response = await call_next(request)

    # Standard Apache/Nginx combined log format
    log_line = f'{client_ip} - - [{datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0000")}] "{request.method} {request.url.path} HTTP/1.1" {response.status_code}\n'
    try:
        os.makedirs("/var/log/backend", exist_ok=True)
        with open("/var/log/backend/access.log", "a") as f:
            f.write(log_line)
    except Exception:
        pass

    return response

# JWT Secret & Algorithm (must match the LDAP Auth API secret)
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-jwt-key-for-ldap-cybersecurity-lab-2026")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

security = HTTPBearer(auto_error=False)

# Seed Pokémons Database (In-memory storage)
POKEMONS_DB: List[dict] = [
    {
        "id": 1,
        "name": "Pikachu",
        "type1": "Electric",
        "type2": None,
        "hp": 35,
        "attack": 55,
        "defense": 40,
        "speed": 90,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "description": "Cuando se enfada, este Pokémon descarga de golpe la energía que almacena en el interior de sus mejillas.",
        "created_by": "admin"
    },
    {
        "id": 2,
        "name": "Charizard",
        "type1": "Fire",
        "type2": "Flying",
        "hp": 78,
        "attack": 84,
        "defense": 78,
        "speed": 100,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "description": "Escupe fuego tan caliente que es capaz de fundir rocas. Se sabe que puede causar incendios forestales involuntarios.",
        "created_by": "admin"
    },
    {
        "id": 3,
        "name": "Blastoise",
        "type1": "Water",
        "type2": None,
        "hp": 79,
        "attack": 83,
        "defense": 100,
        "speed": 78,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "description": "Dispara chorros de agua a gran presión desde los cañones de su caparazón con una precisión asombrosa.",
        "created_by": "admin"
    },
    {
        "id": 4,
        "name": "Venusaur",
        "type1": "Grass",
        "type2": "Poison",
        "hp": 80,
        "attack": 82,
        "defense": 83,
        "speed": 80,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png",
        "description": "La flor de su lomo absorbe la luz del sol y la transforma en energía, llenando el aire de un aroma agradable.",
        "created_by": "admin"
    },
    {
        "id": 5,
        "name": "Gengar",
        "type1": "Ghost",
        "type2": "Poison",
        "hp": 60,
        "attack": 65,
        "defense": 60,
        "speed": 110,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "description": "Se oculta en las sombras de las personas. En plena noche puede hacer que la temperatura baje varios grados.",
        "created_by": "admin"
    },
    {
        "id": 6,
        "name": "Mewtwo",
        "type1": "Psychic",
        "type2": None,
        "hp": 106,
        "attack": 110,
        "defense": 90,
        "speed": 130,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "description": "Fue creado por recombinación genética de Mew. Sus habilidades en combate han sido llevadas al extremo.",
        "created_by": "admin"
    },
    {
        "id": 7,
        "name": "Lucario",
        "type1": "Fighting",
        "type2": "Steel",
        "hp": 70,
        "attack": 110,
        "defense": 70,
        "speed": 90,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/448.png",
        "description": "Tiene la habilidad de detectar y manipular los auras de todas las cosas vivientes a su alrededor.",
        "created_by": "admin"
    },
    {
        "id": 8,
        "name": "Eevee",
        "type1": "Normal",
        "type2": None,
        "hp": 55,
        "attack": 55,
        "defense": 50,
        "speed": 55,
        "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "description": "Posee una estructura genética inestable que le permite evolucionar en múltiples formas diferentes.",
        "created_by": "admin"
    }
]

# Track highest ID
current_id_counter = len(POKEMONS_DB)


def get_current_user_from_jwt(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> dict:
    """
    Middleware/Dependency to validate the presence and authenticity of the Bearer Token (JWT).
    """
    if not credentials or not credentials.credentials:
        logger.warning("[AUTH] Request rejected: Bearer Token is missing in Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso no autorizado: Bearer Token ausente en encabezado Authorization.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    logger.info(f"[AUTH] Validating Bearer Token: {token[:15]}...{token[-10:] if len(token) > 25 else ''}")

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username = payload.get("sub") or payload.get("username")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token JWT inválido: no contiene información de usuario (sub/username).",
                headers={"WWW-Authenticate": "Bearer"},
            )
        logger.info(f"[AUTH] Token valid for user: {username}")
        return payload

    except jwt.ExpiredSignatureError:
        logger.warning("[AUTH] Token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token JWT ha expirado. Inicie sesión nuevamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"[AUTH] Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token JWT inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.get("/")
def root():
    return {
        "message": "Pokemon Backend API activa y funcionando",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "GET_pokemons": "/api/pokemons (Requiere Bearer JWT)",
            "POST_pokemons": "/api/pokemons (Requiere Bearer JWT)"
        }
    }


@app.get("/health")
def health():
    return {"status": "ok", "service": "pokemon-backend-api"}


@app.get("/api/pokemons", response_model=List[Pokemon])
def get_pokemons(
    user: dict = Depends(get_current_user_from_jwt)
):
    """
    GET: Devuelve la lista completa de Pokémones.
    Requiere Bearer Token (JWT) válido.
    """
    logger.info(f"[GET /api/pokemons] Solicitud autorizada para usuario: {user.get('sub')}")
    return POKEMONS_DB


@app.post("/api/pokemons", response_model=Pokemon, status_code=status.HTTP_201_CREATED)
def create_pokemon(
    pokemon_in: PokemonCreate,
    user: dict = Depends(get_current_user_from_jwt)
):
    """
    POST: Agrega un nuevo Pokémon al listado.
    Requiere Bearer Token (JWT) válido.
    """
    global current_id_counter
    current_id_counter += 1

    username = user.get("sub") or user.get("username", "anonymous")
    new_pokemon = {
        "id": current_id_counter,
        "name": pokemon_in.name,
        "type1": pokemon_in.type1,
        "type2": pokemon_in.type2 if pokemon_in.type2 else None,
        "hp": pokemon_in.hp,
        "attack": pokemon_in.attack,
        "defense": pokemon_in.defense,
        "speed": pokemon_in.speed,
        "image_url": pokemon_in.image_url,
        "description": pokemon_in.description or f"Pokémon registrado por {username}",
        "created_by": username
    }

    POKEMONS_DB.append(new_pokemon)
    logger.info(f"[POST /api/pokemons] Pokémon '{new_pokemon['name']}' registrado con ID {new_pokemon['id']} por {username}")
    return new_pokemon


@app.get("/api/pokemons/{pokemon_id}", response_model=Pokemon)
def get_pokemon_by_id(
    pokemon_id: int,
    user: dict = Depends(get_current_user_from_jwt)
):
    for p in POKEMONS_DB:
        if p["id"] == pokemon_id:
            return p
    raise HTTPException(status_code=404, detail=f"Pokémon con ID {pokemon_id} no encontrado")


@app.delete("/api/pokemons/{pokemon_id}", status_code=status.HTTP_200_OK)
def delete_pokemon(
    pokemon_id: int,
    user: dict = Depends(get_current_user_from_jwt)
):
    global POKEMONS_DB
    pokemon_to_remove = None
    for p in POKEMONS_DB:
        if p["id"] == pokemon_id:
            pokemon_to_remove = p
            break

    if not pokemon_to_remove:
        raise HTTPException(status_code=404, detail=f"Pokémon con ID {pokemon_id} no encontrado")

    POKEMONS_DB = [p for p in POKEMONS_DB if p["id"] != pokemon_id]
    logger.info(f"[DELETE /api/pokemons/{pokemon_id}] Pokémon eliminado por {user.get('sub')}")
    return {"message": f"Pokémon '{pokemon_to_remove['name']}' eliminado exitosamente", "id": pokemon_id}
