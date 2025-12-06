from fastapi import APIRouter, HTTPException, status
from datetime import timedelta
from blog.JWT import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from .. import database, JWT
from .. import schemas, model
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(request:OAuth2PasswordRequestForm = Depends(),db: Session = Depends(database.get_db)):
    user = db.query(model.User).filter(model.User.email == request.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    if not CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto").verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    

    access_token = JWT.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


