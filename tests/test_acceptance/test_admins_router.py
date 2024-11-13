import requests
api_url = 'http://localhost:8000'

valid_admin = {
  "username": "string",
  "password": "string",
  "admin_details": {}
}
invalid_admin = {
  "username2": "string",
  "password": "string",
  "admin_details": {}
}

def test_valid_admin_creation():
    admins_url = f'{api_url}/admins'
    response = requests.post(admins_url, json=valid_admin)
    print(response.json())
    assert response.status_code == 200


def test_invalid_admin_creation():
    admins_url = f'{api_url}/admins'
    response = requests.post(admins_url, json=invalid_admin)
    print(response.json())
    assert response.status_code == 422