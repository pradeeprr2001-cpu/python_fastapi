#global level

from fastapi import FastAPI, Depends



def ver_tok(tok:str="123"):
    if tok != "123":
        raise Exception("invalid token")
    return True

app= FastAPI(dependencies=[Depends(ver_tok)])

@app.get("/display")
def dis():
    return {"message":"hello"}

