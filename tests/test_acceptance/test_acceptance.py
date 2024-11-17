import requests
import pytest 

valid_admin = {
  "username": "admin",
  "password": "string",
  "admin_details": {}
}
valid_customer = {
  "username": "customer",
  "password": "string",
  "customer_details": {
    "delivery_address": "string",
    "payment_upi_id": "string@string"
  }
}
valid_delivery_personnel = {
  "username": "delivery_personnel",
  "password": "string",
  "delivery_personnel_details": {}
}
valid_restaurant_owner = {
  "username": "restaurant_owner",
  "password": "string",
  "restaurant_owner_details": {}
}

api_url = 'http://localhost:8000'

customers_url = f'{api_url}/customers'
admins_url = f'{api_url}/admins'
restaurant_owners_url = f'{api_url}/restaurant-owners'
delivery_personnels_url = f'{api_url}/delivery-personnel'

def test_create_users():
    response = requests.post(customers_url, json=valid_customer)
    assert response.status_code == 200

    response = requests.post(admins_url, json=valid_admin)
    assert response.status_code == 200

    response = requests.post(restaurant_owners_url, json=valid_restaurant_owner)
    assert response.status_code == 200

    response = requests.post(delivery_personnels_url, json=valid_delivery_personnel)
    assert response.status_code == 200

admin_token = ''
customer_token = ''
restaurant_owner_token = ''
delivery_personnel_token = ''


login_url = f'{api_url}/login'

@pytest.fixture(scope="module")
def login_get_admin_token():
    login_credentials = {'username': valid_admin['username'], 'password': valid_admin['password']}
    
    response = requests.post(login_url, json=login_credentials)
    assert response.status_code == 200
    admin_token = response.json()['access_token']
    return admin_token

@pytest.fixture(scope="module")
def login_get_customer_token():
    login_credentials = {'username': valid_customer['username'], 'password': valid_customer['password']}
    
    response = requests.post(login_url, json=login_credentials)
    assert response.status_code == 200
    customer_token = response.json()['access_token']
    return customer_token


@pytest.fixture(scope="module")
def login_get_restaurant_owner_token():
    login_credentials = {'username': valid_restaurant_owner['username'], 'password': valid_restaurant_owner['password']}
    
    response = requests.post(login_url, json=login_credentials)
    assert response.status_code == 200
    restaurant_owner_token = response.json()['access_token']
    return restaurant_owner_token

@pytest.fixture(scope="module")
def login_get_delivery_personnel_token():
    login_credentials = {'username': valid_delivery_personnel['username'], 'password': valid_delivery_personnel['password']}
    
    response = requests.post(login_url, json=login_credentials)
    assert response.status_code == 200
    delivery_personnel_token = response.json()['access_token']
    return delivery_personnel_token

def test_login_with_all_users(login_get_admin_token, login_get_customer_token, login_get_restaurant_owner_token, login_get_delivery_personnel_token):
    pass

restaurants_url = f'{api_url}/restaurants'
restaurant_creation_request = {
  "name": "string",
  "restaurant_owner_username": "restaurant_owner"
}

@pytest.fixture(scope="module")
def test_create_restaurant(login_get_admin_token):
    headers = {
        "Authorization": f"Bearer {login_get_admin_token}"
    }
    response = requests.post(restaurants_url, json=restaurant_creation_request, headers=headers)
    assert response.status_code == 200
    return response.json()

def test_unauthorized_create_restaurant(login_get_customer_token):
    headers = {
        "Authorization": f"Bearer {login_get_customer_token}"
    }
    response = requests.post(restaurants_url, json=restaurant_creation_request, headers=headers)
    assert response.status_code == 403

restaurant_update_details = {
    "name": "string",
    "opening_hours": "string",
    "delivery_zone": "string",
    "cuisine": "string",
    "vegetarian": False
}

@pytest.fixture(scope="module")
def test_add_restaurant_details(test_create_restaurant, login_get_restaurant_owner_token):
    headers = {
        "Authorization": f"Bearer {login_get_restaurant_owner_token}"
    }
    restaurant_id = test_create_restaurant
    restaurant_url = f'{restaurants_url}/{restaurant_id}'
    response = requests.put(restaurant_url, json=restaurant_update_details, headers=headers)
    assert response.status_code == 200

restaurant_query_details = {
    "name": "string",
    "delivery_zone": "string",
    "cuisine": "string",
    "vegetarian": False
}

def test_query_restaurants(test_add_restaurant_details, login_get_customer_token):
    headers = {
        "Authorization": f"Bearer {login_get_customer_token}"
    }
    query_url = f'{restaurants_url}/query'
    response = requests.post(query_url, json=restaurant_query_details, headers=headers)
    assert response.status_code == 200
    assert len(response.json())>0

menu_item = {
  "name": "string",
  "price": 10,
  "availability": True
}

@pytest.fixture(scope="module")
def test_add_menu_item(test_create_restaurant, login_get_restaurant_owner_token):
    headers = {
        "Authorization": f"Bearer {login_get_restaurant_owner_token}"
    }
    restaurant_id=test_create_restaurant
    menu_items_url = f'{restaurants_url}/{restaurant_id}/menu-items'
    response = requests.post(menu_items_url, json=menu_item, headers=headers)
    assert response.status_code == 200
    return response.json()

orders_url = f'{api_url}/orders'

@pytest.fixture(scope="module")
def test_create_order(test_create_restaurant, test_add_menu_item, login_get_customer_token):
    order = {
        'order_items': [
            {
                'menu_item_id': test_add_menu_item,
                'count': 5
            }
        ],
        'restaurant_id': test_create_restaurant
    }
    
    headers = {
        "Authorization": f"Bearer {login_get_customer_token}"
    }
    
    response = requests.post(orders_url, json=order, headers=headers)
    assert response.status_code == 200
    return(response.json())

def test_order_flow(test_create_order, login_get_delivery_personnel_token, login_get_restaurant_owner_token):
    order_url = f'{orders_url}/{test_create_order}'
    
    headers = {
        "Authorization": f"Bearer {login_get_restaurant_owner_token}"
    }
    response = requests.post(f'{order_url}/mark-prepared', headers=headers)
    assert response.status_code == 200

    
    headers = {
        "Authorization": f"Bearer {login_get_delivery_personnel_token}"
    }
    
    response = requests.post(f'{order_url}/mark-accepted-for-delivery', headers=headers)
    assert response.status_code == 200
    
    response = requests.post(f'{order_url}/mark-out-for-delivery', headers=headers)
    assert response.status_code == 200

    response = requests.post(f'{order_url}/mark-delivered', headers=headers)
    assert response.status_code == 200
