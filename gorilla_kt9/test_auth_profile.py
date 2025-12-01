import pytest
import httpx
import uuid

API_URL = "http://localhost:8000/api"


@pytest.fixture(scope="function")
def unique_user():
    suffix = str(uuid.uuid4())[:8]
    return {
        "username": f"testuser_{suffix}",
        "password": "SecurePass123!",
        "email": f"testuser_{suffix}@example.com",
        "name": f"Test User {suffix}"
    }

@pytest.mark.asyncio
async def test_register(unique_user):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{API_URL}/register", json=unique_user)
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["username"] == unique_user["username"]

@pytest.mark.asyncio
async def test_register_duplicate_username_fails(unique_user):

    async with httpx.AsyncClient() as client:

        resp1 = await client.post(f"{API_URL}/register", json=unique_user)
        assert resp1.status_code == 201
        resp2 = await client.post(f"{API_URL}/register", json=unique_user)
        assert resp2.status_code == 400  

@pytest.mark.asyncio
async def test_login(unique_user):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/register", json=unique_user)
        login_data = {"username": unique_user["username"], "password": unique_user["password"]}
        response = await client.post(f"{API_URL}/login", json=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_get_profile(unique_user):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/register", json=unique_user)
        login_resp = await client.post(f"{API_URL}/login", json={
            "username": unique_user["username"],
            "password": unique_user["password"]
        })
        token = login_resp.json()["access_token"]
        profile_resp = await client.get(
            f"{API_URL}/profile",
            headers={"Authorization": f"Bearer {token}"}
        )
    assert profile_resp.status_code == 200
    profile = profile_resp.json()
    assert profile["username"] == unique_user["username"]
    assert profile["email"] == unique_user["email"]
    assert profile["name"] == unique_user["name"]

@pytest.mark.asyncio
async def test_update_profile(unique_user):
    async with httpx.AsyncClient() as client:
        await client.post(f"{API_URL}/register", json=unique_user)
        login_resp = await client.post(f"{API_URL}/login", json={
            "username": unique_user["username"],
            "password": unique_user["password"]
        })
        token = login_resp.json()["access_token"]
        update_data = {
            "email": f"updated_{unique_user['email']}",
            "name": "Updated Test User"
        }
        update_resp = await client.put(
            f"{API_URL}/profile",
            headers={"Authorization": f"Bearer {token}"},
            json=update_data
        )
    assert update_resp.status_code == 200
    updated = update_resp.json()
    assert updated["email"] == update_data["email"]
    assert updated["name"] == update_data["name"]
    assert updated["username"] == unique_user["username"]  

@pytest.mark.asyncio
async def test_profile_access_without_token():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{API_URL}/profile")
    assert response.status_code == 401 