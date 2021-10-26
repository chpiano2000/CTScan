from fastapi.security import HTTPBearer
from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from pydantic import ValidationError
from typing import Union, Any, Optional
import jwt
from .config import SECRET_KEY

ALGORITHM = "HS256"
access_token_jwt_subject = "access"

reusable_oauth2 = HTTPBearer(scheme_name='Authorization')

def generate_token(data: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode = {
        "exp": expire, "email": data
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def validate_token(http_authorization_credentials=Depends(reusable_oauth2)) -> str:
    try:
        payload = jwt.decode(http_authorization_credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get('username') < datetime.now():
            raise HTTPException(status_code=403, detail="Token expired")
        return payload.get('username')
    except(jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=403,
            detail=f"Could not validate credentials",
        )
