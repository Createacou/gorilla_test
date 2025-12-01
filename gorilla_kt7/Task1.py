import asyncio
import pytest

async def async_function_success():
    await asyncio.sleep(0.01)
    return "expected_value"

@pytest.mark.asyncio
async def test_async_function_resolves_correctly():
    result = await async_function_success()
    assert result == "expected_value"