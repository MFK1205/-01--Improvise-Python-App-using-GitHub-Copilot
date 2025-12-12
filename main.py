from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import hashlib

app = FastAPI()

# Pydantic model for the text field
class TextData(BaseModel):
    text: str

# Welcome Note
@app.get("/")
def read_root():
    return {"message": "Welcome to the API! Customized for [Siddi]"}

# FastAPI endpoint to accept POST request with a JSON body containing a single field "text"
@app.post("/generate/")
def generate(data: TextData):
    # Generate a checksum of the text
    checksum = hashlib.md5(data.text.encode()).hexdigest()
    return {"checksum": checksum}
