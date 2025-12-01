import asyncio
import pytest

class CustomError(Exception):
    pass

async def async_function_fails():
    await asyncio.sleep(0.01)
    raise CustomError("Something went wrong")

@pytest.mark.asyncio
async def test_async_function_raises_expected_exception(event_loop):
    with pytest.raises(CustomError, match="Something went wrong"):
        await async_function_fails()