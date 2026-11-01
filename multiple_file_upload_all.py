
#multiple file
#read the file data (text) (pdf) (excel)
#size,file name


import io
from typing import List

import pandas as pd
from fastapi import FastAPI, File, UploadFile
from PyPDF2 import PdfReader

app = FastAPI()


@app.post("/read-file/")
async def read_file(files: List[UploadFile] = File(...)):
    results = []

    for file in files:
        name = file.filename.lower()
        content = await file.read()

        if name.endswith(".xls", ".xlsx"):
            df = pd.read_excel(io.BytesIO(content))
            results.append({
                "filename": file.filename,
                "type": "excel",
                "preview": df.head(3).to_dict()
            })

        elif name.endswith(".pdf"):
            reader = PdfReader(io.BytesIO(content))
            text = "".join([p.extract_text() or "" for p in reader.pages[:2]])
            results.append({
                "filename": file.filename,
                "type": "pdf",
                "preview": text.strip()[:500],
            })

        elif name.endswith(".txt"):
            words = content.decode("utf-8", errors="ignore").split()
            results.append({
                "filename": file.filename,
                "type": "txt",
                "word_count": len(words),
                "preview": " ".join(words[:50]),
            })

        else:
            results.append({
                "filename": file.filename,
                "error": "Unsupported file type.",
            })

    return results