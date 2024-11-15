import logging

logger = logging.getLogger(__name__)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from server.routers.CustomerRouter import router as CustomerRouter
from server.routers.RestaurantOwnerRouter import router as RestaurantOwnerRouter
from server.routers.DeliveryPersonnelRouter import router as DeliveryPersonnelRouter
from server.routers.AdminRouter import router as AdminRouter
from server.routers.LoginRouter import router as LoginRouter

app = FastAPI()
app.include_router(CustomerRouter, tags=["Customer"], prefix="/customers")
app.include_router(RestaurantOwnerRouter, tags=["RestaurantOwner"], prefix="/restaurant-owners")
app.include_router(DeliveryPersonnelRouter, tags=["DeliveryPersonnel"], prefix="/delivery-personnel")
app.include_router(AdminRouter, tags=["Admin"], prefix="/admins")
app.include_router(LoginRouter, tags=["Login"], prefix="/login")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this phantastic app!"}
