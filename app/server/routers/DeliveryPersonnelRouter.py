from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.models import DeliveryPersonnelCreationRequestSchema
from server.services.DeliveryPersonnelService import delivery_personnel_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_delivery_personnel(delivery_personnel: DeliveryPersonnelCreationRequestSchema):
    await delivery_personnel_service.add_delivery_personnel(delivery_personnel)
    return 