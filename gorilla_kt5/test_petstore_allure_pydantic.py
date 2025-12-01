import requests
import pytest
import allure
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any


BASE_URL = "https://petstore.swagger.io/v2"

class User(BaseModel):
    id: int
    username: str
    firstName: str
    lastName: str
    email: str
    password: str
    phone: str
    userStatus: int = Field(..., alias="userStatus")

    class Config:
        allow_population_by_field_name = True


class Order(BaseModel):
    id: int
    petId: int
    quantity: int
    shipDate: str
    status: str
    complete: bool


class InventoryResponse(BaseModel):
    __root__: Dict[str, int]


class BaseRequest:
    def __init__(self, base_url: str):
        self.base_url = base_url

    @allure.step("GET {url}")
    def get(self, endpoint: str, endpoint_id: Optional[str] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        if endpoint_id:
            url += f"/{endpoint_id}"
        response = requests.get(url)
        self._attach_response(response)
        return response

    @allure.step("POST {url}")
    def post(self, endpoint: str, data: dict, endpoint_id: Optional[str] = None) -> requests.Response:
        url = f"{self.base_url}/{endpoint}"
        if endpoint_id:
            url += f"/{endpoint_id}"
        response = requests.post(url, json=data)
        self._attach_response(response)
        return response

    @allure.step("PUT {url}")
    def put(self, endpoint: str, endpoint_id: str, data: dict) -> requests.Response:
        url = f"{self.base_url}/{endpoint}/{endpoint_id}"
        response = requests.put(url, json=data)
        self._attach_response(response)
        return response

    @allure.step("DELETE {url}")
    def delete(self, endpoint: str, endpoint_id: str) -> requests.Response:
        url = f"{self.base_url}/{endpoint}/{endpoint_id}"
        response = requests.delete(url)
        self._attach_response(response)
        return response

    @staticmethod
    def _attach_response(response: requests.Response):
        allure.attach(
            str(response.request.headers),
            name="Request Headers",
            attachment_type=allure.attachment_type.TEXT,
        )
        if response.request.body:
            allure.attach(
                response.request.body.decode() if isinstance(response.request.body, bytes) else str(response.request.body),
                name="Request Body",
                attachment_type=allure.attachment_type.JSON,
            )
        allure.attach(
            str(response.status_code),
            name="Response Status Code",
            attachment_type=allure.attachment_type.TEXT,
        )
        if response.text:
            allure.attach(
                response.text,
                name="Response Body",
                attachment_type=allure.attachment_type.JSON,
            )



@pytest.fixture(scope="module")
def base_request():
    return BaseRequest(BASE_URL)


@pytest.fixture
def user_data() -> dict:
    return {
        "id": 1001,
        "username": "NAGUFmuiier1945",
        "firstName": "Klaus",
        "lastName": "Halzeth",
        "email": "Sp#$a2281488pozvoniImyPodbrosim@gmail.com",
        "password": "12341234",
        "phone": "+7234567890",
        "userStatus": 1
    }


@pytest.fixture
def order_data() -> dict:
    return {
        "id": 10,
        "petId": 1,
        "quantity": 1,
        "shipDate": "3035-10-20T09:00:00.000+00:00",
        "status": "placed",
        "complete": True
    }



@allure.epic("Petstore API")
@allure.feature("User Management")
class TestUserAPI:

    @allure.title("Create, retrieve, update and delete user")
    def test_full_user_lifecycle(self, base_request, user_data):

        resp_create = base_request.post("user", user_data)
        assert resp_create.status_code == 200
        User(**resp_create.json())  

        resp_get = base_request.get("user", user_data["username"])
        assert resp_get.status_code == 200
        retrieved = User(**resp_get.json())
        assert retrieved.username == user_data["username"]

        updated_data = {**user_data, "firstName": "KlausUpdated"}
        resp_put = base_request.put("user", user_data["username"], updated_data)
        assert resp_put.status_code == 200

        resp_del = base_request.delete("user", user_data["username"])
        assert resp_del.status_code == 200

    @allure.title("Get non-existent user returns 404")
    def test_get_nonexistent_user(self, base_request):
        resp = base_request.get("user", "nonexistent_user_999999")
        assert resp.status_code == 404


@allure.epic("Petstore API")
@allure.feature("Store Management")
class TestStoreAPI:

    @allure.title("Place order, retrieve it, then delete")
    def test_order_lifecycle(self, base_request, order_data):

        resp_place = base_request.post("store/order", order_data)
        assert resp_place.status_code == 200
        placed = Order(**resp_place.json())
        assert placed.id == order_data["id"]

       
        resp_get = base_request.get("store/order", str(order_data["id"]))
        assert resp_get.status_code == 200
        retrieved = Order(**resp_get.json())
        assert retrieved.id == order_data["id"]

        
        resp_del = base_request.delete("store/order", str(order_data["id"]))
        assert resp_del.status_code == 200

    @allure.title("Get inventory returns valid structure")
    def test_get_inventory(self, base_request):
        resp = base_request.get("store/inventory")
        assert resp.status_code == 200
        inv = InventoryResponse(__root__=resp.json())
        assert isinstance(inv.__root__, dict)
        assert len(inv.__root__) > 0
        for key, value in inv.__root__.items():
            assert isinstance(key, str)
            assert isinstance(value, int)

    @allure.title("Delete non-existent order returns 404")
    def test_delete_nonexistent_order(self, base_request):
        resp = base_request.delete("store/order", "999999999")
        assert resp.status_code == 404