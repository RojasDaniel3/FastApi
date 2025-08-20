from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl="login")


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
        "password":"123456"
    },
        "daniel2":{
        "username":"daniel2",
        "full_name":"Daniel Rojas2",
        "email":"dani-rojas0206@hotmail.com2",
        "disabled": True,
        "password":"654321"
    }
}

def search_user(username: str):
    if username in users_db:
        return UserDB(users_db[username])
    
async def current_user(token: str =  Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales de autentificacion invalidas", headers={"WWW-Authenticate": "Bearer"}
        )
    
@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
            status_code=400, detail="El usuario no es correcto"
        )
    
    user = search_user(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=400, detail="La contraseña no es correcto"
        )
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user