from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from server.models import AdminCreationRequestSchema
from server.services.AdminService import admin_service
from server.services.UserService import user_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_admin(admin: AdminCreationRequestSchema):
    if await user_service.user_exists(admin.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        ) 
    await admin_service.add_admin(admin)
    return 'Added'