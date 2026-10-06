from typing import Optional
from pydantic import BaseModel, Field


class PokemonBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, example="Pikachu")
    type1: str = Field(..., example="Electric")
    type2: Optional[str] = Field(None, example="")
    hp: int = Field(default=50, ge=1, le=500, example=35)
    attack: int = Field(default=50, ge=1, le=500, example=55)
    defense: int = Field(default=50, ge=1, le=500, example=40)
    speed: int = Field(default=50, ge=1, le=500, example=90)
    image_url: str = Field(
        default="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        example="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png"
    )
    description: Optional[str] = Field(
        default="Pokémon registrado en el sistema.",
        example="Cuando varios de estos Pokémon se juntan, su electricidad puede acumularse y causar tormentas."
    )


class PokemonCreate(PokemonBase):
    pass


class Pokemon(PokemonBase):
    id: int
    created_by: str = "system"
