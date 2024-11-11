from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..services import Restaurant as service   
from ..models.Restaurant import RestaurantSchema

router = APIRouter()

@router.post("/", response_description="Restaurant added")
async def add_data(data: RestaurantSchema = Body(...)):
    data = jsonable_encoder(data)
    new_item = await service.add(data)
    return ResponseModel(new_item, "Restaurant added successfully.")

@router.get("/", response_description="Restaurants retrieved")
async def get():    
    items = await service.retrieve_all()
    if items:
        return ResponseModel(items, "Restaurant data retrieved successfully")
    return ResponseModel(items, "Empty list returned")

def ResponseModel(data, message):
    return {
        "data": data,
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}