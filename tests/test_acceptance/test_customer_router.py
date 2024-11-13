import requests
api_url = 'http://localhost:8000'

valid_customer = {
  "username": "string",
  "password": "string",
  "customer_details": {
    "delivery_address": "string",
    "payment_upi_id": "string"
  }
}
invalid_customer = {
  "username2": "string",
  "password": "string",
  "customer_details": {
    "delivery_address": "string",
    "payment_upi_id": "string"
  }
}

def test_valid_customer_creation():
    customers_url = f'{api_url}/customers'
    response = requests.post(customers_url, json=valid_customer)
    print(response.json())
    assert response.status_code == 200


def test_invalid_customer_creation():
    customers_url = f'{api_url}/customers'
    response = requests.post(customers_url, json=invalid_customer)
    print(response.json())
    assert response.status_code == 422