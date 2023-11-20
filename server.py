import pandas as pd
import uvicorn
from typing import Annotated, Optional
from io import BytesIO
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field

class Person(BaseModel):
    fname : str = Field(title="FName")
    lname : str = Field(title="Lname")
    age : int = Field(title="Age")
    gender : Optional[str] = Field(title="Gender")
    last_grade : Optional[str] = Field(title="Last sem grade A|B|C|D|E")

app = FastAPI()

def try_wrapper(func, **args):
    try:
        out = func(**args)
        return {
            "status" : True,
            "data" : out,
            "message" : "Task completed !"
        }
    except Exception as exp:
        return {
            "status" : False,
            "data" : str(exp),
            "message" : "Task failed !"
        }
        

# @app.post("/files")
# async def create_file(file : Annotated[bytes, File()]):
#     frame = pd.read_excel(file)
#     return {"file_size" : frame.head()}

@app.post("/upload-file")
async def create_upload_file(file : UploadFile = File(...)):
    data = await file.read()
    frame = pd.read_excel(BytesIO(data))
    frame.columns = frame.columns.str.lower()
    removed = frame[frame.isna().any(axis=1)]
    frame = frame.dropna()
    docs = frame.to_dict(orient="records")
    removed = removed.to_dict()
    try:
        print(docs)
        docs = [Person(**doc) for doc in docs]
        print([doc.__dict__ for doc in docs])
        if len(removed):
            return {"message" : "Parsed all docs"}
        return {"message" : f'Parsed all docs except {str(removed)}'}
    except Exception as ex:
        return {"message" : str(ex)}
        


if __name__ == "__main__":
    uvicorn.run("server:app", port=8000, log_level="info", reload=True)