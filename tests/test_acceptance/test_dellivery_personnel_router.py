import requests
api_url = 'http://localhost:8000'

valid_delivery_personnel = {
  "username": "string",
  "password": "string",
  "delivery_personnel_details": {}
}
invalid_delivery_personnel = {
  "username2": "string",
  "password": "string",
  "delivery_personnel_details": {}
}

def test_valid_delivery_personnel_creation():
    delivery_personnel_url = f'{api_url}/delivery-personnel'
    response = requests.post(delivery_personnel_url, json=valid_delivery_personnel)
    print(response.json())
    assert response.status_code == 200


def test_invalid_delivery_personnel_creation():
    delivery_personnel_url = f'{api_url}/delivery-personnel'
    response = requests.post(delivery_personnel_url, json=invalid_delivery_personnel)
    print(response.json())
    assert response.status_code == 422