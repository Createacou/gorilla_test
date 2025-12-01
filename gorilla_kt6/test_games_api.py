import asyncio
import aiohttp
import pytest
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, ValidationError


class Game(BaseModel):
    id: int
    name: str
    description: str
    price: float
    imageUrl: str
    genre: str
    rating: float


async def fetch_games_data(url: str) -> Optional[List[Dict[str, Any]]]:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def validate_games_structure(data: List[Dict[str, Any]]) -> List[Game]:
    games = []
    for item in data:
        game = Game(**item)
        games.append(game)
    return games


async def get_games_by_genre(genre: str, games: List[Game]) -> List[Game]:
    return [g for g in games if g.genre.lower() == genre.lower()]


async def get_game_by_id(game_id: int, games: List[Game]) -> Optional[Game]:
    for game in games:
        if game.id == game_id:
            return game
    return None
API_URL = "https://gist.githubusercontent.com/LordHarmadon/642f2230d551adb06ae38e0a26d818c3/raw/efab18f16a5cca19294b175bdce39b7f91471a02/games.json"


@pytest.mark.asyncio
async def test_fetch_games_data():
    data = await fetch_games_data(API_URL)
    assert data is not None
    assert isinstance(data, list)
    assert len(data) > 0


@pytest.mark.asyncio
async def test_validate_games_structure():
    data = await fetch_games_data(API_URL)
    assert data is not None

    games = await validate_games_structure(data)
    assert len(games) == len(data)
    assert all(isinstance(g, Game) for g in games)  # Проверяем, что это объекты Pydantic


@pytest.mark.asyncio
async def test_get_games_by_genre():
    data = await fetch_games_data(API_URL)
    assert data is not None

    games = await validate_games_structure(data)
    action_games = await get_games_by_genre("Action", games)
    assert len(action_games) > 0
    assert all(g.genre.lower() == "action" for g in action_games)


@pytest.mark.asyncio
async def test_get_game_by_id():
    data = await fetch_games_data(API_URL)
    assert data is not None

    games = await validate_games_structure(data)
    game = await get_game_by_id(1, games)
    assert game is not None
    assert game.id == 1
    assert game.name == "Grand Theft Auto 5"


@pytest.mark.asyncio
async def test_get_nonexistent_game_by_id():
    data = await fetch_games_data(API_URL)
    assert data is not None

    games = await validate_games_structure(data)
    game = await get_game_by_id(999, games)
    assert game is None

if __name__ == "__main__":
    asyncio.run(fetch_games_data(API_URL))