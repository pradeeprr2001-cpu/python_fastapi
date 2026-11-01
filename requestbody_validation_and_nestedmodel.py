
from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional





app = FastAPI()

class Manf(BaseModel):
    company: str
    country: str

class Item(BaseModel):  
    name: str = Field(min_length=3, max_length=50, pattern="^[a-zA-Z]")
    price: float = Field(gt=1, lt=10000)
    availability: Optional[bool] = None
    manufacturer: Manf

@app.post("/display/")
def view(data: Item):
    return {"message": "item received", "data": data}
