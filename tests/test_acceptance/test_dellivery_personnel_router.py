import requests
api_url = 'http://localhost:8000'

valid_delivery_personnel = {
  "username": "delivery_personnel",
  "password": "string",
  "delivery_personnel_details": {}
}
invalid_delivery_personnel = {
  "username2": "delivery_personnel",
  "password": "string",
  "delivery_personnel_details": {}
}

def test_valid_delivery_personnel_creation_with_duplication():
    delivery_personnel_url = f'{api_url}/delivery-personnel'
    response = requests.post(delivery_personnel_url, json=valid_delivery_personnel)
    assert response.status_code == 200

    response = requests.post(delivery_personnel_url, json=valid_delivery_personnel)
    assert response.status_code == 409


def test_invalid_delivery_personnel_creation():
    delivery_personnel_url = f'{api_url}/delivery-personnel'
    response = requests.post(delivery_personnel_url, json=invalid_delivery_personnel)
    print(response.json())
    assert response.status_code == 422