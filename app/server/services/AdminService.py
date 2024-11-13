import logging

logger = logging.getLogger(__name__)

from server.models import AdminCreationRequestSchema, AdminDetails, UserInDB, UserRole
from server.services.UserService import UserService
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class AdminService:
    def __init__(self):
        self._admin_details_crud: CommonCRUD = CommonCRUD(collection_name='admin_details')
        self._user_service: UserService = UserService()

    async def add_admin(self, admin: AdminCreationRequestSchema):
        logger.info('Adding admin')
        inserted_admin_details_id = await self._add_admin_details_for_admin(admin.admin_details)
        
        logger.info('Creating User Object from Admin')
        user: UserInDB = self._get_user_object(admin, inserted_admin_details_id)
        
        inserted_id = await self._user_service.add_user(user)
        return inserted_id
    
    async def _add_admin_details_for_admin(self, admin_details: AdminDetails) -> str:
        inserted_id = await self._admin_details_crud.add(admin_details.model_dump())
        return inserted_id
    
    def _get_user_object(self, admin: AdminCreationRequestSchema, admin_details_id) -> AdminDetails:
        user: UserInDB = UserInDB(username = admin.username,
                    hashed_password=hash_password(admin.password),
                    role=UserRole.CUSTOMER,
                    user_details_id=admin_details_id)
        return user


admin_service = AdminService()

