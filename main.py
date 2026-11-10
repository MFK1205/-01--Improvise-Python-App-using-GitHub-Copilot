from fastapi import FastAPI
from pydantic import BaseModel
import hashlib

app = FastAPI()


# Pydantic model for the text field
class TextData(BaseModel):
    """Request body for text-processing operations."""
    text: str


# Welcome Note
@app.get("/")
def read_root():
    """Return a welcome message for the API."""
    return {"message": "Welcome to the API, Leenasree!"}


# Generate tokens and checksum
@app.post("/generate/")
def generate(data: TextData):
    """Split submitted text into tokens and calculate its MD5 checksum."""

    # Generate tokens from the input text
    tokens = data.text.split()

    # Calculate checksum using UTF-8 encoding
    checksum = hashlib.md5(data.text.encode("utf-8")).hexdigest()

    return {
        "tokens": tokens,
        "checksum": checksum
    }
