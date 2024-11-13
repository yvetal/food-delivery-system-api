import logging

logger = logging.getLogger(__name__)

from server.models import DeliveryPersonnelCreationRequestSchema, DeliveryPersonnelDetails, UserInDB, UserRole
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class DeliveryPersonnelService:
    def __init__(self):
        self._delivery_personnel_details_crud: CommonCRUD = CommonCRUD(collection_name='delivery_personnel_details')
        self._user_crud: CommonCRUD = CommonCRUD(collection_name='user')

    async def add_delivery_personnel(self, delivery_personnel: DeliveryPersonnelCreationRequestSchema):
        logger.info('Adding delivery_personnel')
        inserted_delivery_personnel_details_id = await self._add_delivery_personnel_details_for_delivery_personnel(delivery_personnel.delivery_personnel_details)
        
        logger.info('Creating User Object from DeliveryPersonnel')
        user: UserInDB = self._get_user_object(delivery_personnel, inserted_delivery_personnel_details_id)
        
        inserted_id = await self._add_user(user)
        return inserted_id
    
    async def _add_delivery_personnel_details_for_delivery_personnel(self, delivery_personnel_details: DeliveryPersonnelDetails) -> str:
        inserted_id = await self._delivery_personnel_details_crud.add(delivery_personnel_details.model_dump())
        return inserted_id
    
    async def _add_user(self, user: UserInDB) -> str:
        inserted_id = await self._user_crud.add(user.model_dump())
        return inserted_id
    
    def _get_user_object(self, delivery_personnel: DeliveryPersonnelCreationRequestSchema, delivery_personnel_details_id) -> DeliveryPersonnelDetails:
        user: UserInDB = UserInDB(username = delivery_personnel.username,
                    hashed_password=hash_password(delivery_personnel.password),
                    role=UserRole.CUSTOMER,
                    user_details_id=delivery_personnel_details_id)
        return user


delivery_personnel_service = DeliveryPersonnelService()

