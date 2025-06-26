from fastapi import Header, HTTPException
from typing import Optional
import os

API_KEY = os.getenv("API_KEY", "srijaykey123")  # load from env or default

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key