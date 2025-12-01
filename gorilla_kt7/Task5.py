import asyncio
import pytest

def blocking_function(x: int, y: int) -> int:
    # Эмуляция CPU-bound или blocking I/O
    return x * y

async def run_in_thread(x: int, y: int) -> int:
    loop = asyncio.get_running_loop()
    # Для Python ≥3.9 можно использовать asyncio.to_thread
    result = await loop.run_in_executor(None, blocking_function, x, y)
    return result

@pytest.mark.asyncio
async def test_run_in_thread_returns_correct_result(event_loop):
    result = await run_in_thread(6, 7)
    assert result == 42