import logging

logger = logging.getLogger(__name__)

from server.models import RestaurantCreationRequestSchema, RestaurantSchema, RestaurantUpdateRequestSchema, MenuItem, MenuItemCreationRequest
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class RestaurantService:
    def __init__(self):
        self._restaurant_crud: CommonCRUD = CommonCRUD(collection_name='restaurants')
        self._menu_item_crud: CommonCRUD = CommonCRUD(collection_name='menu_items')

    async def add_restaurant(self, restaurant_creation_request: RestaurantCreationRequestSchema):
        logger.info('Adding restaurant')
        restaurant = RestaurantSchema(name=restaurant_creation_request.name, restaurant_owner_username=restaurant_creation_request.restaurant_owner_username)
        inserted_id = await self._restaurant_crud.add(restaurant.model_dump())        
        return inserted_id
    
    async def get_all(self):
        logger.info('Getting restaurants')
        restaurants = await self._restaurant_crud.find_all()
        
        return restaurants

    async def get_by_id(self, id) -> RestaurantSchema:
        logger.info('Getting restaurants')
        restaurant = await self._restaurant_crud.find_by_id(id)
        
        return restaurant
    
    async def update_restaurant(self, id, restaurant: RestaurantUpdateRequestSchema):
        logger.info(f'Updating restaurant {id}')
        update_query = {}
        for key, value in restaurant.__dict__.items():
            if value != None:
                update_query[key] = value
        logger.info(f'Update query {update_query}')
        count = await self._restaurant_crud.update_by_id(id, update_query)
        logger.info(count)
    
    async def add_menu_item(self, id, menu_item_creation_request: MenuItemCreationRequest):
        menu_item = MenuItem(name=menu_item_creation_request.name,
                             availability=menu_item_creation_request.availability,
                             price=menu_item_creation_request.price,
                             restaurant_id=id,
        )
        logger.info(f'Adding Menu Item {menu_item}')
        inserted_id = await self._menu_item_crud.add(menu_item.__dict__)
        return inserted_id
    
    async def get_menu_items(self, id):
        menu_items = await self._menu_item_crud.find(query={'restaurant_id': id})
        return menu_items
    
    async def get_restaurants_by_owner(self, username):
        restaurants = await self._restaurant_crud.find(query={'restaurant_owner_username': username})
        return restaurants
    
restaurant_service = RestaurantService()

