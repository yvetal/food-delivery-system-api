import requests

def test_restaurants():

    api_url = 'http://localhost:8000'

    restaurant_to_add = {
        'name': 'restaurant_1',
        'menu_items': [
            {
                'name': 'menu_items_1'
            }
        ]
    }
    restaurants_api_url = f'{api_url}/restaurants'
    response = requests.post(restaurants_api_url, json=restaurant_to_add)
    assert response.status_code == 200
    
    response = requests.get(restaurants_api_url)
    assert response.status_code == 200

    restaurant_names = [restaurant['name'] for restaurant in response.json()['data']]
    assert restaurant_to_add['name'] in restaurant_names