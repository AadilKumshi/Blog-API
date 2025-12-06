from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from ..Oauth2 import get_current_user
from ..database import get_db
from typing import List
from .. import schemas, model, database

get_db = database.get_db

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)

@router.get("/", response_model=List[schemas.Blog], dependencies=[Depends(get_current_user)])
def get_blogs(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

@router.post("/", dependencies=[Depends(get_current_user)])
def create_blog(blog: schemas.Blog, db: Session = Depends(get_db),):
    new_blog = model.Blog(title=blog.title, body=blog.body, user_id=1)  # Assuming user_id=1 for simplicity
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return {"data": f"Blog titled '{new_blog.title}' has been created with ID {new_blog.id}."}

@router.get("/{id}", dependencies=[Depends(get_current_user)])
def get_blog(id: int, db: Session = Depends(get_db), response_model=schemas.Blog):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog

@router.delete("/{id}", dependencies=[Depends(get_current_user)])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return {"data": f"Blog with ID {id} has been deleted."}

@router.put("/{id}", dependencies=[Depends(get_current_user)])
def update_blog(id: int, updated_blog: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = updated_blog.title
    blog.body = updated_blog.body
    db.commit()
    return {"data": f"Blog with ID {id} has been updated."}