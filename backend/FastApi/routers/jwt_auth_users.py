from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt

ALGORITHM = "HS256" 
ACCESS_TOKEN_DURATION = 1
SECRET = "190a926de1c728a08f1cb33336e4a96ee72258108c37ac2584406a6548bf42ae"

router = APIRouter()


oauth2 = OAuth2PasswordBearer(tokenUrl="login")


crypt = CryptContext(schemes=["bcrypt"], deprecated="auto",)


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str


users_db = {
    "daniel":{
        "username":"daniel",
        "full_name":"Daniel Rojas",
        "email":"dani-rojas0206@hotmail.com",
        "disabled": False,
        "password":"$2y$10$jna54rbbNeD.mRsiBUR8H.jkrptu0lSiZv/7t.Ku6j2GCtJCIcZl."
    },
        "daniel2":{
        "username":"daniel2",
        "full_name":"Daniel Rojas2",
        "email":"dani-rojas0206@hotmail.com2",
        "disabled": True,
        "password":"$2a$12$aRZR.M5kJ7AahBYUpK284u9Fv2cvBqEjf5g.UFV8wpUFF8yI43Fly"
    }
}



def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    


async def auth_user(token: str = Depends(oauth2)):
    
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autentificacion invalidas", headers={"WWW-Authenticate": "Bearer"}
        )
        
    
    
    
    try:
    
        username =  jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
            
        
        
        
        
    except PyJWTError:
    
        raise exception
        
    return search_user(username)


async def current_user(user: User =  Depends(auth_user)):

        
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario inactivo"
        )
    
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto"
        )
    
    user = search_user_db(form.username)
    
    # crypt.verify(form.password, user.password)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcto"
        )
        
        
    
    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION)
    
    expire = datetime.utcnow() + access_token_expiration
    
    access_token = {"sub":user.username, "exp":expire}
    
    return {"access_token": jwt.encode(access_token,SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user