
#multiple file
#read the file data (text)
#size,file name

from typing import List
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/read-file/")
async def read_file(files: List[UploadFile] = File(...)):
    result = []
    for file in files:
        content = await file.read()
        text = content.decode("utf-8")
        
        result.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": len(content),
            "content_preview": text[:200],
        })

    return result