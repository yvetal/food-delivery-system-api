import logging

logger = logging.getLogger(__name__)

from server.models import CustomerCreationRequestSchema, CustomerDetails, UserInDB, UserRole
from server.services.UserService import UserService
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class CustomerService:
    def __init__(self):
        self._customer_details_crud: CommonCRUD = CommonCRUD(collection_name='customer_details')
        self._user_service: UserService = UserService()

    async def add_customer(self, customer: CustomerCreationRequestSchema):
        logger.info('Adding customer')
        inserted_customer_details_id = await self._add_customer_details_for_customer(customer.customer_details)
        
        logger.info('Creating User Object from Customer')
        user: UserInDB = self._get_user_object(customer, inserted_customer_details_id)
        
        inserted_id = await self._user_service.add_user(user)
        return inserted_id
    
    async def _add_customer_details_for_customer(self, customer_details: CustomerDetails) -> str:
        inserted_id = await self._customer_details_crud.add(customer_details.model_dump())
        return inserted_id
    
    def _get_user_object(self, customer: CustomerCreationRequestSchema, customer_details_id) -> CustomerDetails:
        user: UserInDB = UserInDB(username = customer.username,
                    hashed_password=hash_password(customer.password),
                    role=UserRole.CUSTOMER,
                    user_details_id=customer_details_id)
        return user


customer_service = CustomerService()

