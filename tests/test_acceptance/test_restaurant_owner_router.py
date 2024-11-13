import requests
api_url = 'http://localhost:8000'

valid_restaurant_owner = {
  "username": "restaurant_owner",
  "password": "string",
  "restaurant_owner_details": {}
}
invalid_restaurant_owner = {
  "username2": "restaurant_owner",
  "password": "string",
  "restaurant_owner_details": {}
}

def test_valid_restaurant_owner_creation_with_duplication():
    restaurant_owners_url = f'{api_url}/restaurant-owners'
    response = requests.post(restaurant_owners_url, json=valid_restaurant_owner)
    assert response.status_code == 200

    response = requests.post(restaurant_owners_url, json=valid_restaurant_owner)
    assert response.status_code == 409


def test_invalid_restaurant_owner_creation():
    restaurant_owners_url = f'{api_url}/restaurant-owners'
    response = requests.post(restaurant_owners_url, json=invalid_restaurant_owner)
    print(response.json())
    assert response.status_code == 422