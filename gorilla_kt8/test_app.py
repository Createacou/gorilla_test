import pytest
import allure
from app import get_json

@pytest.mark.asyncio
@allure.feature("HTTP Requests")
@allure.story("Successful Response")
@allure.title("Test get_json returns correct data from httpbin")
@allure.description("Проверяет, что функция возвращает корректный JSON при успешном ответе.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("json", "http", "success")
async def test_get_json_success():
    url = "https://httpbin.org/get"
    result = await get_json(url)
    assert result is not None
    assert isinstance(result, dict)
    assert "headers" in result
    assert "User-Agent" in result["headers"]



@pytest.mark.asyncio
@allure.feature("HTTP Requests")
@allure.story("Error Handling")
@allure.title("Test get_json returns None on invalid URL")
@allure.description("Проверяет, что функция возвращает None при ошибке или неудачном запросе.")
@allure.severity(allure.severity_level.CRITICAL)
@allure.tag("error", "network", "failure")
async def test_get_json_invalid_url():
    url = "https://nonexistent-domain-123456789.com/api"
    result = await get_json(url)
    assert result is None


@pytest.mark.asyncio
@allure.feature("HTTP Requests")
@allure.story("Error Handling")
@allure.title("Test get_json returns None on 404 status")
@allure.description("Проверяет, что функция возвращает None при получении статуса 404.")
@allure.severity(allure.severity_level.NORMAL)
@allure.tag("http", "404", "error")
async def test_get_json_404():
    url = "https://httpbin.org/status/404"
    result = await get_json(url)
    assert result is None
