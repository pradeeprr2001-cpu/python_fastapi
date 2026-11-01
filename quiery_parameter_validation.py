
from fastapi import FastAPI, Query
from pydantic import BaseModel,Field
from typing import Optional

emp=[
      {'id':101, 'name':'ram', 'place':'chn'},
      {'id':102, 'name':'pradeep', 'place':'chn'}
    ]



app = FastAPI()



@app.get("/display/")
def view(id:int=Query(ge=100,le=200),
         name:str=Query(min_length=3,max_length=50, pattern="^[A-Za-z]")):
    for e in emp:
        if e['id']==id and e['name']== name:
            return e
 
         
    
