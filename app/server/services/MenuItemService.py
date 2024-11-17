import logging

logger = logging.getLogger(__name__)

from server.models import MenuItemQuerySchema
from server.crud.Common import CommonCRUD

class MenuItemService:
    def __init__(self):
        self._menu_item_crud: CommonCRUD = CommonCRUD(collection_name='menu_items')

    async def query(self, query: MenuItemQuerySchema):
        logger.info('Getting menu_items')
        get_query = {}
        for key, value in query.__dict__.items():
            if value != None:
                get_query[key] = value
        menu_items = await self._menu_item_crud.find(get_query)
        return menu_items

menu_item_service = MenuItemService()

