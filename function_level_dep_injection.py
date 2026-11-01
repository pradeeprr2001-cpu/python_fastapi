
#functional level

from fastapi import FastAPI, Depends

app= FastAPI()

def db():
    return{"db":"connected"}

@app.get("/display")
def dis(a:dict=Depends(db)):
    return {"message": "this is from display endpoint","db_status":a}