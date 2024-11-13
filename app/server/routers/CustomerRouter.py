from fastapi import APIRouter, HTTPException


from server.models import CustomerCreationRequestSchema
from server.services.CustomerService import customer_service
from server.services.UserService import user_service


router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    })
async def add_customer(customer: CustomerCreationRequestSchema):
    if await user_service.user_exists(customer.username):
        raise HTTPException(
            status_code=409,
            detail="Username already exists"
        ) 
    await customer_service.add_customer(customer)
    return 'Added'