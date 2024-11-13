from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.models import CustomerCreationRequestSchema
from server.services.CustomerService import customer_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_customer(customer: CustomerCreationRequestSchema):
    await customer_service.add_customer(customer)
    return 