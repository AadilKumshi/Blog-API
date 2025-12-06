from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import database
from ..Oauth2 import get_current_user
from .. import schemas, model
from passlib.context import CryptContext

get_db = database.get_db
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

@router.post("/", status_code=201)
def create_user(user: schemas.createUser, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = model.User(name=user.name, email=user.email, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user 

@router.get("/{id}", response_model=schemas.ShowUser, dependencies=[Depends(get_current_user)])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user




