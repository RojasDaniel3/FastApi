from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()






@app.get("/usersjson")
async def usersjson():
    return [{"name": "Daniel", "surname": "rojas"},
            {"name": "Kevin", "surname": "Echeverria"},
            {"name": "Cristian", "surname": "ricardo"}]