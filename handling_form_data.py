
from fastapi import FastAPI, Form

app=FastAPI()

@app.post("/feedback/")
def feed (name:str= Form(),
          email:str=Form(),
          rat:int=Form()):
    return{
        "Status":"feedback received",
        "Name":name,
        "Rating":rat
    }
