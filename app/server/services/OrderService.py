import logging

logger = logging.getLogger(__name__)

from server.models import OrderCreationRequestSchema, OrderSchema, DeliveryStatus, PreparationStatus
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
        order = OrderSchema(customer_username=customer_username, order_item_ids=order_item_ids, restaurant_id=order_creation_request.restaurant_id)
        inserted_id = await self._order_crud.add(order.model_dump())        
        return inserted_id
    
    async def get_all(self):
        logger.info('Getting orders')
        orders = await self._order_crud.find_all()
        
        return orders
    
    async def assign_delivery(self, id, username):
        logger.info(f'Assigning order {id} for delivery to {username}')
        update_count = await self._order_crud.update_by_id(id, update_query={'delivery_status': DeliveryStatus.ASSIGNED, 'delivery_personnel_username': username})
        return update_count
    
    async def get_orders_for_customer_by_username(self, username):
        logger.info(f'Getting orders for {username}')
        orders = await self._order_crud.find({'customer_username': username})
        return orders

    async def get_orders_for_delivery_personnel_by_username(self, username):
        logger.info(f'Getting orders for {username}')
        orders = await self._order_crud.find({'delivery_personnel_username': username})
        return orders
    
    async def get_orders_for_restaurant_by_id(self, id):
        logger.info(f'Getting orders for {id}')
        orders = await self._order_crud.find({'restaurant_id': id})
        return orders
    
    async def get_by_id(self, id):
        logger.info(f'Getting order by id {id}')
        order = await self._order_crud.find_by_id(id)
        return order
    
    async def mark_prepared(self, id):
        logger.info(f'Marking order {id} prepared')
        update_count = await self._order_crud.update_by_id(id, update_query={'preparation_status': PreparationStatus.PREPARED})
        return update_count
    
    async def mark_out_for_delivery(self, id):
        logger.info(f'Marking order {id} out for delivery')
        update_count = await self._order_crud.update_by_id(id, update_query={'delivery_status': DeliveryStatus.OUT_FOR_DELIVERY})
        return update_count
        
    async def mark_delivered(self, id):
        logger.info(f'Marking order {id} delivered')
        update_count = await self._order_crud.update_by_id(id, update_query={'delivery_status': DeliveryStatus.DELIVERED})
        return update_count
        
order_service = OrderService()

