from fastapi import FastAPI, Response, status, HTTPException, Request, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import schemas, tables, utils, oauth2
from ..database import engine, get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model= schemas.UserResponse)
def create_user(newUser: schemas.UserModel ,db: Session = Depends(get_db)):

    #hash password
    hashed_Password = utils.hashing(newUser.password)
    newUser.password = hashed_Password

    new_user = tables.Users(**newUser.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model= schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    user_found = db.query(tables.Users).filter(tables.Users.id == id).first()

    if user_found == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} does not exist")
    
    return user_found
