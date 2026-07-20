from fastapi import APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from security.authentication import authenticate_admin, create_access_token
from config import get_settings

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    principal = authenticate_admin(form.username, form.password)
    if not principal: raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_access_token(principal.username, principal.roles), "token_type": "bearer", "expires_in": get_settings().access_token_minutes * 60}
