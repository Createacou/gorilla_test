import aiohttp
import asyncio

async def get_json(url: str) -> dict | None:
    """
    Асинхронная функция, которая делает GET-запрос к URL и возвращает JSON-ответ.
    В случае ошибки или статуса != 200 возвращает None.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    return None
    except Exception:
        return None