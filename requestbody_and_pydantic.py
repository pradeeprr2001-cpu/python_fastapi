
#REQUEST BODY ..
#used to send structured data to server



from fastapi import FastAPI
from pydantic import BaseModel

app= FastAPI()

class items(BaseModel):
    name : str
    price: float
    availability: bool
    
@app.post("/display/")
def view(data:items):
    return{"message":"items received","data":data}




#Pydantic model ..
#validation
#serialization
#documentation