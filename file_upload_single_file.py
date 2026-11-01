
#single file
#read the file data (text)
#size,file name

from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/read-file/")
async def read_file(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
    }