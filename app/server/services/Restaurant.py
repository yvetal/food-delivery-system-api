from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..crud import Restaurant as restaurant_crud   
from ..crud import MenuItem as menu_item_crud   

from ..models.Restaurant import RestaurantSchema

router = APIRouter()

async def add(restaurant: dict):
    menu_items = restaurant['menu_items']
    del restaurant['menu_items']

    added_restaurant = await restaurant_crud.add(restaurant)
    menu_item_ids = []
    for menu_item in restaurant['menu_items']:
        added_menu_item = menu_item_crud.add(menu_item)
        menu_item_ids
    return added_restaurant

async def  retrieve_all():
    return await restaurant_crud.retrieve_all()