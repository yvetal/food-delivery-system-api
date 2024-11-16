import requests
api_url = 'http://localhost:8000'

valid_admin = {
  "username": "admin",
  "password": "string",
  "admin_details": {}
}
invalid_admin = {
  "username2": "admin",
  "password": "string",
  "admin_details": {}
}

def test_valid_admin_creation_with_duplication():
    admins_url = f'{api_url}/admins'
    response = requests.post(admins_url, json=valid_admin)
    assert response.status_code == 200

    response = requests.post(admins_url, json=valid_admin)
    assert response.status_code == 409


def test_invalid_admin_creation():
    admins_url = f'{api_url}/admins'
    response = requests.post(admins_url, json=invalid_admin)
    print(response.json())
    assert response.status_code == 422