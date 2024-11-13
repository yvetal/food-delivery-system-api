from fastapi import APIRouter, HTTPException

from server.models import DeliveryPersonnelCreationRequestSchema
from server.services.DeliveryPersonnelService import delivery_personnel_service
from server.services.UserService import user_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_delivery_personnel(delivery_personnel: DeliveryPersonnelCreationRequestSchema):
    if await user_service.user_exists(delivery_personnel.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        ) 
    await delivery_personnel_service.add_delivery_personnel(delivery_personnel)
    return 'Added'