
from fastapi import FastAPI, Query, Path
from pydantic import BaseModel,Field
from typing import Optional

emp=[
      {'id':101, 'name':'ram', 'place':'chn'},
      {'id':102, 'name':'pradeep', 'place':'chn'}
    ]



app = FastAPI()



@app.get("/display/{id}/")   #retrive id alone is work
def view(id:int=Path(ge=100,le=200, multiple_of=2)):
        for e in emp:
             if e['id']==id:
                  return e
        

@app.get("/display/{id}/{name}")
def view(id:int=Path(ge=100,le=200, multiple_of=2),
         name:str=Path(min_length=3,max_length=50,pattern="^[A-Za-z]")):
    for e in emp:
        if e['id']==id and e['name']==name:
            return e
    
