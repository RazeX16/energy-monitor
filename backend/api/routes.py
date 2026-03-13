from fastapi import APIRouter, HTTPException
from backend.models.user_models import LoginRequest, LoginResponse
from backend.services.auth import verify_password, create_access_token

router = APIRouter()


# dummy user (for now)
fake_user = {
    "username": "admin",
    "password_hash": "$2b$12$5f7E2q9L8h4Z7U6sP0ZQfO2X4H8Qv6z0r3Qb0k2rV0M2g7Yk8WZ9S", 
    "role": "admin"
}


@router.post("/login", response_model=LoginResponse)
def login(data: LoginRequest):

    if data.username != fake_user["username"]:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(data.password, fake_user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token({"sub": data.username})

    return {
        "token": token,
        "username": data.username,
        "role": fake_user["role"]
    }