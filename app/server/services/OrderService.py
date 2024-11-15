import logging

logger = logging.getLogger(__name__)

from server.models import OrderCreationRequestSchema, OrderSchema, DeliveryStatus
from server.crud.Common import CommonCRUD

from server.hash import hash_password

class OrderService:
    def __init__(self):
        self._order_crud: CommonCRUD = CommonCRUD(collection_name='orders')
        self._order_item_crud: CommonCRUD = CommonCRUD(collection_name='order_items')

    async def add_order(self, order_creation_request: OrderCreationRequestSchema, customer_username:str):
        logger.info('Adding order')
        order_item_ids = []
        for order_item in order_creation_request.order_items:
            inserted_id = await self._order_item_crud.add(order_item.model_dump())
            order_item_ids.append(inserted_id)
        order = OrderSchema(customer_username=customer_username, order_item_ids=order_item_ids)
        inserted_id = await self._order_crud.add(order.model_dump())        
        return inserted_id
    
    async def get_all(self):
        logger.info('Getting orders')
        orders = await self._order_crud.find_all()
        
        return orders
    
    async def assign_delivery(self, id, username):
        logger.info('Getting orders')
        update_count = await self._order_crud.update_by_id(id, update_query={'delivery_status': DeliveryStatus.ASSIGNED, 'delivery_personnel_username': username})
        return update_count
    
order_service = OrderService()

