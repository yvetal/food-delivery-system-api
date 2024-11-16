from fastapi import APIRouter, HTTPException, Depends


from server.models import CustomerCreationRequestSchema
from server.services.CustomerService import customer_service
from server.services.OrderService import order_service
from server.services.UserService import user_service
from server.hash import role_required


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

@router.get("/orders")
async def get_orders_for_customer(current_user: dict = Depends(role_required("CUSTOMER"))):
    orders = await order_service.get_orders_for_customer_by_username(current_user['username'])
    return orders