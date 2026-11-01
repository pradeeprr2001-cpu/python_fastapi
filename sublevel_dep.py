
#sublevel dependencies (multiple)

from fastapi import FastAPI, Depends

app= FastAPI()

def gp():
       return{"message":"from grand parent"}

def pa(a=Depends(gp)):
       return{f"message: from parent {a}"}

@app.get("/display")
def child(b:str=Depends(pa)):
       return{"message":b}