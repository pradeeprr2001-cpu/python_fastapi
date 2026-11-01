
from fastapi import FastAPI

app = FastAPI()

@app.get("/display")
def display_data():
    return {"status": "success", "data": "Your content here"}