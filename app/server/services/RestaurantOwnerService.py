import logging

logger = logging.getLogger(__name__)

from server.models import RestaurantOwnerCreationRequestSchema, RestaurantOwnerDetails, UserInDB, UserRole
from server.services.UserService import UserService
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class RestaurantOwnerService:
    def __init__(self):
        self._restaurant_owner_details_crud: CommonCRUD = CommonCRUD(collection_name='restaurant_owner_details')
        self._user_service: UserService = UserService()

    async def add_restaurant_owner(self, restaurant_owner: RestaurantOwnerCreationRequestSchema):
        logger.info('Adding restaurant_owner')
        inserted_restaurant_owner_details_id = await self._add_restaurant_owner_details_for_restaurant_owner(restaurant_owner.restaurant_owner_details)
        
        logger.info('Creating User Object from RestaurantOwner')
        user: UserInDB = self._get_user_object(restaurant_owner, inserted_restaurant_owner_details_id)
        
        inserted_id = await self._user_service.add_user(user)
        return inserted_id
    
    async def _add_restaurant_owner_details_for_restaurant_owner(self, restaurant_owner_details: RestaurantOwnerDetails) -> str:
        inserted_id = await self._restaurant_owner_details_crud.add(restaurant_owner_details.model_dump())
        return inserted_id
    
    def _get_user_object(self, restaurant_owner: RestaurantOwnerCreationRequestSchema, restaurant_owner_details_id) -> RestaurantOwnerDetails:
        user: UserInDB = UserInDB(username = restaurant_owner.username,
                    hashed_password=hash_password(restaurant_owner.password),
                    role=UserRole.RESTAURANT_OWNER,
                    user_details_id=restaurant_owner_details_id)
        return user


restaurant_owner_service = RestaurantOwnerService()

