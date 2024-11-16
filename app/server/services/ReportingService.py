import logging

logger = logging.getLogger(__name__)

from server.models import RestaurantCreationRequestSchema, RestaurantSchema, RestaurantUpdateRequestSchema, MenuItem, MenuItemCreationRequest
from server.crud.Common import CommonCRUD

from server.hash import hash_password
from collections import defaultdict

class ReportingService:
    def __init__(self):
        self._order_crud: CommonCRUD = CommonCRUD(collection_name='orders')
    
    async def get_report(self):
        logger.info('Getting reports')
        orders = await self._order_crud.find_all()
        report = defaultdict(int)
        for order in orders:
            report[order['restaurant_id']] +=1
        return report

reporting_service = ReportingService()