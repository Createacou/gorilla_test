import requests
import pytest
import json
from time import sleep

BASE_URL = "https://dog.ceo/api"

def get_random_breed():
    """Helper to get a random breed for testing."""
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    response.raise_for_status()
    breeds = response.json().get("message", {})
    if breeds:
        for breed, sub_breeds in breeds.items():
            if sub_breeds:
                return breed, sub_breeds[0] if sub_breeds else None
        first_breed = next(iter(breeds))
        return first_breed, None
    return "affenpinscher", None

def test_get_all_breeds():
    """Test 1: Get all breeds list."""
    response = requests.get(f"{BASE_URL}/breeds/list/all")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "success"
    assert isinstance(data["message"], dict)

def test_get_images_by_breed():
    """Test 2: Get images for a specific breed."""
    breed, _ = get_random_breed()
    response = requests.get(f"{BASE_URL}/breed/{breed}/images")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "success"
    assert isinstance(data["message"], list)
    assert len(data["message"]) > 0
    assert data["message"][0].startswith("https://images.dog.ceo/breeds/")

def test_get_random_image_by_breed():
    """Test 3: Get a random image for a specific breed."""
    breed, _ = get_random_breed()
    response = requests.get(f"{BASE_URL}/breed/{breed}/images/random")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "success"
    assert isinstance(data["message"], str)
    assert data["message"].startswith("https://images.dog.ceo/breeds/")

def test_get_random_image_any_breed():
    """Test 4: Get a random dog image (any breed)."""
    response = requests.get(f"{BASE_URL}/breeds/image/random")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "success"
    assert isinstance(data["message"], str)
    assert data["message"].startswith("https://images.dog.ceo/")

def test_get_sub_breeds():
    """Test 5: Get sub-breeds for a specific breed."""
    breed, sub_breed = get_random_breed()
    response = requests.get(f"{BASE_URL}/breed/{breed}/list")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data
    assert data["status"] == "success"
    assert isinstance(data["message"], list)
    # The list can be empty if the breed has no sub-breeds
    if sub_breed:
        assert sub_breed in data["message"]


if __name__ == "__main__":
    import subprocess
    import sys

    print("--- Dog CEO API Тестирование ---")
    print("Цель: Проверить основные эндпоинты API и обеспечить покрытие сущностей.")
    print("-" * 80)

    try:
        pytest_functions = [
            test_get_all_breeds,
            test_get_images_by_breed,
            test_get_random_image_by_breed,
            test_get_random_image_any_breed,
            test_get_sub_breeds
        ]
        print("\n--- Запуск тестов pytest ---")
        if len(sys.argv) > 1 and sys.argv[1] == "run_tests":
            for test_func in pytest_functions:
                try:
                    test_func()
                    print(f"OK: {test_func.__name__}")
                except Exception as e:
                    print(f"FAIL: {test_func.__name__} - {e}")
        else:
            subprocess.run([sys.executable, __file__, "run_tests"])

    except Exception as e:
        print(f"Ошибка при запуске тестов: {e}")

    print("-" * 80)
    print("--- Отчет о тестировании ---")
    print("Проверенные эндпоинты:")
    print("  - /breeds/list/all")
    print("  - /breed/{breed}/images")
    print("  - /breed/{breed}/images/random")
    print("  - /breeds/image/random")
    print("  - /breed/{breed}/list")
    print("\nПроверенные аспекты:")
    print("  - Статус-код 200 OK")
    print("  - Структура ответа (наличие 'message', 'status')")
    print("  - Статус ответа ('success')")
    print("  - Типы данных в ответе (dict, list, str)")
    print("  - Формат URL изображений")
    print("-" * 80)
