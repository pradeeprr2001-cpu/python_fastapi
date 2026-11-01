
from fastapi import FastAPI

app= FastAPI()

emp=[
    {'id':101, 'name':'ram', 'place':'chn'},
    {'id':102, 'name':'pradeep', 'place':'chn'}
]



@app.get("/display/{id}")
def viewforpath(id:int):
    for e in emp:
        if e['id']==id:
            return e

