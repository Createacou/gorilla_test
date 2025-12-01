import pytest
import aiohttp

async def fetch_json(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@pytest.mark.asyncio
async def test_http_request_returns_correct_response(event_loop):
    url = "https://httpbin.org/get"
    data = await fetch_json(url)
    assert "headers" in data
    assert "User-Agent" in data["headers"]