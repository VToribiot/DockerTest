from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json

app = FastAPI()


class Temperature(BaseModel):
    amount: float
    measurement: str

    def __init__(self, amount: str, measurement: int):
        super().__init__(amount=amount, measurement=measurement)


def f_to_c(t):
    return (t - 32) * 5/9

def c_to_f(t):
    return (t * 9/5) + 32


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/ftoc")
async def fahrenheit_to_celsius(temp : Temperature):    
    result = Temperature(f_to_c(temp.amount), 'C')
    return result

@app.post("/ctof")
async def celsius_to_fahrenheit(temp : Temperature):    
    result = Temperature(c_to_f(temp.amount), 'F')
    return result