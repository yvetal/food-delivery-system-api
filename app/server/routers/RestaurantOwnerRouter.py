from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.models import RestaurantOwnerCreationRequestSchema
from server.services.RestaurantOwnerService import restaurant_owner_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_restaurant_owner(restaurant_owner: RestaurantOwnerCreationRequestSchema):
    await restaurant_owner_service.add_restaurant_owner(restaurant_owner)
    return 