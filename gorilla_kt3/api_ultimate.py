import requests
import pprint


class BaseRequest:
    def __init__(self, base_url):
        self.base_url = base_url

    def _request(self, url, request_type, data=None, expected_error=False):
        stop_flag = False
        while not stop_flag:
            if request_type == 'GET':
                response = requests.get(url)
            elif request_type == 'POST':
                response = requests.post(url, json=data) 
            elif request_type == 'PUT':
                response = requests.put(url, json=data) 
            else:  
                response = requests.delete(url)

            if not expected_error and 200 <= response.status_code < 300:
                stop_flag = True
            elif expected_error:
                stop_flag = True

        pprint.pprint(f'{request_type} request to: {response.url}')
        pprint.pprint(f'Status Code: {response.status_code}')
        pprint.pprint(f'Reason: {response.reason}')
        try:
            json_response = response.json()
        except ValueError:
            json_response = None
        pprint.pprint(f'Response Text: {response.text}')
        pprint.pprint(f'Response JSON: {json_response}')
        pprint.pprint('**********')
        return response

    def get(self, endpoint, endpoint_id=None, expected_error=False):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id is not None:
            url += f'/{endpoint_id}'
        response = self._request(url, 'GET', expected_error=expected_error)
        try:
            return response.json()
        except ValueError:
            return response.text

    def post(self, endpoint, data, endpoint_id=None):
        url = f'{self.base_url}/{endpoint}'
        if endpoint_id is not None:
            url += f'/{endpoint_id}'
        response = self._request(url, 'POST', data=data)
        try:
            return response.json()
        except ValueError:
            return response.text

    def put(self, endpoint, endpoint_id, data):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'PUT', data=data)
        try:
            return response.json()
        except ValueError:
            return response.text

    def delete(self, endpoint, endpoint_id):
        url = f'{self.base_url}/{endpoint}/{endpoint_id}'
        response = self._request(url, 'DELETE')
        try:
            return response.json()
        except ValueError:
            return response.text


class UserAPI:
    def __init__(self, base_request):
        self.base_request = base_request
        self.endpoint = 'user'

    def create_user(self, user_data):
        return self.base_request.post(self.endpoint, user_data)

    def get_user_by_username(self, username):
        return self.base_request.get(self.endpoint, endpoint_id=username)

    def update_user(self, username, user_data):
        return self.base_request.put(self.endpoint, username, user_data)

    def delete_user(self, username):
        return self.base_request.delete(self.endpoint, endpoint_id=username)


class StoreAPI:
    def __init__(self, base_request):
        self.base_request = base_request
        self.endpoint = 'store'

    def get_inventory(self):
        return self.base_request.get(f'{self.endpoint}/inventory')

    def place_order(self, order_data):
        return self.base_request.post(f'{self.endpoint}/order', order_data)

    def get_order_by_id(self, order_id):
        return self.base_request.get(f'{self.endpoint}/order', endpoint_id=order_id)

    def delete_order(self, order_id):
        return self.base_request.delete(f'{self.endpoint}/order', endpoint_id=order_id)


if __name__ == "__main__":
    BASE_URL_PETSTORE = 'https://petstore.swagger.io/v2'
    base_request = BaseRequest(BASE_URL_PETSTORE)

    user_api = UserAPI(base_request)
    store_api = StoreAPI(base_request)

    print(" User API ")
    user_data = {
        "id": 1001,
        "username": "NAGUFmuiier1945",
        "firstName": "Klaus",
        "lastName": "Halzeth",
        "email": "Sp#$a2281488pozvoniImyPodbrosim@gmail.com",
        "password": "12341234",
        "phone": "+7234567890",
        "userStatus": 1
    }
    created_user = user_api.create_user(user_data)
    pprint.pprint("Created User Response:")
    pprint.pprint(created_user)


    retrieved_user = user_api.get_user_by_username("NAGUFmuiier1945")
    pprint.pprint("Retrieved User:")
    pprint.pprint(retrieved_user)

    updated_data = {
        "id": 1001,
        "username": "NAGUFmuiier1945",
        "firstName": "Klaus",
        "lastName": "Halzeth",
        "email": "Sp#$a2281488pozvoniImyPodbrosim@gmail.com",
        "password": "12341234",
        "phone": "+7234567890",
        "userStatus": 1
    }
    updated_user = user_api.update_user("NAGUFmuiier1945", updated_data)
    pprint.pprint("Updated User Response:")
    pprint.pprint(updated_user)


    deleted_user = user_api.delete_user("NAGUFmuiier1945")
    pprint.pprint("Deleted User Response:")
    pprint.pprint(deleted_user)

 
    print("\n--- Store API ---")
  
    inventory = store_api.get_inventory()
    pprint.pprint("Inventory:")
    pprint.pprint(inventory)

 
    order_data = {
        "id": 10,
        "petId": 1,
        "quantity": 1,
        "shipDate": "3035-10-20T09:00:00.000+00:00",
        "status": "placed",
        "complete": True
    }
    placed_order = store_api.place_order(order_data)
    pprint.pprint("Placed Order Response:")
    pprint.pprint(placed_order)


    retrieved_order = store_api.get_order_by_id(10)
    pprint.pprint("Retrieved Order:")
    pprint.pprint(retrieved_order)

    deleted_order = store_api.delete_order(10)
    pprint.pprint("Deleted Order Response:")
    pprint.pprint(deleted_order)
