from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

app = FastAPI()

# JWT and password hashing configurations
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# In-memory 'database' for simplicity
users_db = {}

# Define Pydantic models
class User(BaseModel):
    username: str
    password: str
    role: str

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None



def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user(username: str):
    user = users_db.get(username)
    if user:
        return UserInDB(**user)

@app.post("/register", status_code=201)
async def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = hash_password(user.password)
    users_db[user.username] = {"username": user.username, "hashed_password": hashed_password, "role": user.role}
    return {"msg": "User registered successfully"}

@app.post("/login", response_model=Token)
async def login(user: User):
    user_in_db = get_user(user.username)
    if not user_in_db or not verify_password(user.password, user_in_db.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username, "role": user_in_db.role})
    return {"access_token": access_token, "token_type": "bearer"}



from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: str = payload.get("role")
        if username is None or role is None:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
        return {"username": username, "role": role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def role_required(role: str):
    async def role_checker(current_user: dict = Depends(get_current_user)):
        if current_user["role"] != role:
            raise HTTPException(status_code=403, detail="Access forbidden")
        return current_user
    return role_checker




@app.get("/customer/dashboard")
async def customer_dashboard(current_user: dict = Depends(role_required("customer"))):
    return {"msg": f"Welcome, {current_user['username']}! This is your customer dashboard."}

@app.get("/restaurant/dashboard")
async def restaurant_dashboard(current_user: dict = Depends(role_required("restaurant_owner"))):
    return {"msg": f"Welcome, {current_user['username']}! This is your restaurant dashboard."}

@app.get("/admin/dashboard")
async def admin_dashboard(current_user: dict = Depends(role_required("administrator"))):
    return {"msg": f"Welcome, {current_user['username']}! This is your admin dashboard."}
