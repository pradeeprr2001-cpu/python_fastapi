from fastapi import FastAPI, HTTPException, Request
app= FastAPI()


req_counter={}
max_req=5

@app.get("/data")
def get_data(request:Request):
    client_ip= request.client.host
    req_counter[client_ip]=req_counter.get(client_ip,0)+1

    print(req_counter)


    if req_counter[client_ip]>max_req:
        raise HTTPException(status_code=424,detail="Too many req.. your req limit is reached...!")
    return{"message":f"Request{req_counter[client_ip]} succesful"}
