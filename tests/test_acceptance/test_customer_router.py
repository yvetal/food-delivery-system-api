import requests
api_url = 'http://localhost:8000'

valid_customer = {
  "username": "customer",
  "password": "string",
  "customer_details": {}
}
invalid_customer = {
  "username2": "customer",
  "password": "string",
  "customer_details": {}
}

def test_valid_customer_creation_with_duplication():
    customers_url = f'{api_url}/customers'
    response = requests.post(customers_url, json=valid_customer)
    assert response.status_code == 200

    response = requests.post(customers_url, json=valid_customer)
    assert response.status_code == 409


def test_invalid_customer_creation():
    customers_url = f'{api_url}/customers'
    response = requests.post(customers_url, json=invalid_customer)
    print(response.json())
    assert response.status_code == 422