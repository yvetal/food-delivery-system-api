from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.models import AdminCreationRequestSchema
from server.services.AdminService import admin_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_admin(admin: AdminCreationRequestSchema):
    await admin_service.add_admin(admin)
    return 'Added'