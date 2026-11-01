
from fastapi import FastAPI, Response, Cookie, HTTPException
from typing import Optional
import uuid


app = FastAPI()

couname="admin"
copass="1234"

sessions={}


@app.post("/login")
def login(uname: str, pa:str, res:Response):
    if couname == uname and copass == pa:
        sid=str(uuid.uuid4())
        sessions[sid]={"username":uname}
        res.set_cookie(key="sid",value=sid,httponly=True)
        return{"message":"Login success"}
    else:
        raise HTTPException(status_code=401,detail="Invalid credential")

@app.get("/home")
def home(sid:Optional[str]=Cookie(None)):
    if sid is None or sid not in sessions:
        raise HTTPException(status_code=401,detail="Not Aunthenticated")
    return {"user":sessions[sid]}

    