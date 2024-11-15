from fastapi import APIRouter, HTTPException

from server.models import Token, LoginCredentials
from server.services.UserService import user_service
from server.hash import verify_password, create_access_token

router = APIRouter()

@router.post(
    "/",
    responses={
        200: {"description": "Successful Response", "model": str},
    },
    response_model=Token
)
async def login(user: LoginCredentials):
    user_in_db = await user_service.get_user(user.username)
    if not user_in_db or not verify_password(user.password, user_in_db['hashed_password']):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user_in_db['username'], "role": user_in_db['role']})
    return {"access_token": access_token, "token_type": "bearer"}
