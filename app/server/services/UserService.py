import logging

logger = logging.getLogger(__name__)

from server.models import UserInDB
from server.crud.Common import CommonCRUD

class UserService:
    def __init__(self):
        self._user_crud: CommonCRUD = CommonCRUD(collection_name='user')

    async def user_exists(self, username: str):        
        logger.info(f'Checking user {username} existence')
        query = {'username': username}
        result = await self._user_crud.find_one(query)
        logger.info(result)
        if result:
            return True
        else:
            return False 
    
    async def get_user(self, username: str):        
        logger.info(f'Getting user {username}')
        query = {'username': username}
        result = await self._user_crud.find_one(query)
        return result
        
    async def add_user(self, user: UserInDB):        
        logger.info('Creating User Object from User')
        inserted_id = await self._add_user_to_db(user)
        return inserted_id
    
    async def _add_user_to_db(self, user: UserInDB) -> str:
        inserted_id = await self._user_crud.add(user.model_dump())
        return inserted_id


user_service = UserService()

