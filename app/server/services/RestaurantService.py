import logging

logger = logging.getLogger(__name__)

from server.models import RestaurantCreationRequestSchema, RestaurantSchema
from server.services.UserService import UserService
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class RestaurantService:
    def __init__(self):
        self._restaurant_crud: CommonCRUD = CommonCRUD(collection_name='restaurants')

    async def add_restaurant(self, restaurant_creation_request: RestaurantCreationRequestSchema):
        logger.info('Adding restaurant')
        restaurant = RestaurantSchema(name=restaurant_creation_request.name, restaurant_owner_id=restaurant_creation_request.restaurant_owner_id)
        inserted_id = await self._restaurant_crud.add(restaurant.model_dump())        
        return inserted_id
        
restaurant_service = RestaurantService()

