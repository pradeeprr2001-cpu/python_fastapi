
#login 
#sec data
#jwt
#verify
#header.payload.singnature

from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from jose import JWTError, jwt

app=FastAPI()

#conf
ALGORITHM ="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=10
SECRET_KEY="mysecretkey_1234"

def create_token(uname:str):
    expire = datetime.now()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload= {"username":uname,"expire":expire.timestamp()}
    return jwt.encode(payload,SECRET_KEY,ALGORITHM)

def verify_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms={ALGORITHM})
        return payload["username"]
    except JWTError:
        raise HTTPException(status_code=400,detail="invalid token")

@app.post("/login")
def login(uname:str,password:str):
    if uname=="admin" and password=="1234":
        token=create_token(uname)
        return {"access token":token}
    return HTTPException(status_code=400,detail="invalid Uname or password")

@app.get("/secret_data")
def sec_data(token:str):
    uname= verify_token(token)
    return{"message": f"hello {uname}, this is secret endpoint"}
