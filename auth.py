from fastapi import Header, HTTPException
import config

def authenticate(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization format")
    
    token = authorization.split("Bearer ")[1]
    if token != config.API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token