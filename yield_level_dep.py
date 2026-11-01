
#yield level 

from fastapi import FastAPI, Depends
from datetime import datetime

app= FastAPI()

def bookstore():
    print("book taken from shelf",datetime.now())
    book="Fastapi book"
    yield book
    print("book returned to shelf",datetime.now())

@app.get("/read")   
def readbook(a:str=Depends(bookstore)):
    return {f"message {datetime.now()}" :f"reading {a}"} 