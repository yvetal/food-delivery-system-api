import logging

logger = logging.getLogger(__name__)

from fastapi import APIRouter, HTTPException, Depends

from server.services.MenuItemService import menu_item_service
from server.services.OrderService import order_service
from server.services.UserService import user_service
from server.hash import role_required
from server.models import MenuItemQuerySchema

router = APIRouter()

@router.post("/query")
async def fetch_menu_items(query: MenuItemQuerySchema, current_user: dict = Depends(role_required("CUSTOMER"))):
    menu_items = await menu_item_service.query(query)
    return menu_items