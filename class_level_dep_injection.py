
#class level dependency injection

from fastapi import FastAPI, Depends

app= FastAPI()

class user:
    def __init__(self):
        self.name="code solve exicute"
        self.age=22


def getuser():
    return user()   

@app.get("/user_data")  
def dis(a:user=Depends(getuser)):
    return {"name":a.name,"age":a.age}