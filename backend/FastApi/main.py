from fastapi import FastAPI
from routers import products, users
from fastapi.staticfiles import StaticFiles

## RUN 
## fastapi dev main.py


## ACTIVATE
## source venv/bin/activate

## DESACTIVATE
## deactivate


app = FastAPI()



## Routers

app.include_router(products.router)
app.include_router(users.router)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return {"message": "Hola FastAPI"}

@app.get("/url")
async def url():
    return {"url": "Aca una url"}