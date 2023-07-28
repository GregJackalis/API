from fastapi import FastAPI, Response, status, HTTPException, Request, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from .. import schemas, oauth2, tables
from ..database import engine, get_db




router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# response_model=List[schemas.ReponseModel]

# @router.get("/", response_model=List[schemas.PostOut])
@router.get("/")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: Optional[int] = 10, Skip: Optional[int] = 0, Search: Optional[str] = ""):
    #THIS IS HOW TO WRITE QUERY AND SEND IT TO DATABASE
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    # posts = db.query(tables.Post).filter(tables.Post.title.contains(Search)).limit(Limit).offset(Skip).all()

    query = db.query(tables.Post, func.count(tables.Vote.Post_id)).outerjoin(tables.Vote, tables.Post.id == tables.Vote.Post_id).group_by(tables.Post.id).all()

    serializable_data = [
        {
            "owner": post.owner.email,
            "post_title": post.title,
            "post_content": post.content,
            "likes": votes
        }
        for post, votes in query
    ]

    return serializable_data




@router.get("/{id}")
def get_one_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    # post = cursor.fetchone()

    # post = db.query(tables.Post).filter(tables.Post.id == id).first()

    post, votes = db.query(tables.Post, func.count(tables.Vote.Post_id)).outerjoin(tables.Vote, tables.Post.id == tables.Vote.Post_id).group_by(tables.Post.id).filter(tables.Post.id == id).first()


    #checking if the entered id exists and if not then make the status code 404, meaning that it wasn't found
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Post with id {id} was not found!")
    
    serializable_data = {
        "owner": post.owner.email,
        "post_title": post.title,
        "post_content": post.content,
        "likes": votes  # The count of votes (likes) for the post
    }

    return serializable_data
    
    # THIS PART IS IN CASE WE WANT TO CHECK IF THE USER HAS THE SAME ID AS THE ID OF THE OWNER OF THE POST THAT THEY'RE TRYING TO INDIVIDUALLY GET
    # if post.owner_id == current_user:
    #     return post
    # else:
    #     return Response(content= "This user doesn't have authorization to view this post", status_code= status.HTTP_401_UNAUTHORIZED)





@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ReponseModel)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #THIS IS HOW TO WRITE QUERY AND SEND IT TO DATABASE
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES( %s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    new_post = tables.Post(**post.dict())
    new_post.owner_id = current_user

    # new_post.owner_name = db.query(tables.Users).filter(tables.Users.id == current_user).with_entities(tables.Users.email).scalar()

    # new_post.update("user": f"user {user} says:")
    db.add(new_post)
    db.commit()

    #this is the exact same as in writing RETURNING * in SQL
    db.refresh(new_post)
    
    return new_post
#title str, content str, published boolean



# @router.get("/posts/latest")
# def get_latest_post():
#     cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC""")
#     latest = cursor.fetchone()
#     return latest



@router.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deletedPost = cursor.fetchone()
    # conn.commit()

    deletedPost = db.query(tables.Post).filter(tables.Post.id == id)
    firstPost = deletedPost.first()
    

    if firstPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if firstPost.owner_id == current_user:
        deletedPost.delete(synchronize_session=False)
        db.commit()
        return Response(content= "post deleted successfully", status_code=status.HTTP_204_NO_CONTENT)

    else:
        return Response(content= "This user doesn't have authorization to delete this post", status_code= status.HTTP_401_UNAUTHORIZED)



@router.put("/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id),))

    # updated_Post = cursor.fetchone()
    # conn.commit()
    Post_Id = db.query(tables.Post).filter(tables.Post.id == id)
    updatedPost = Post_Id.first()

    if updatedPost == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist")
    
    if updatedPost.owner_id == current_user:
        Post_Id.update(post.dict(), synchronize_session=False)
        db.commit()
        return updatedPost
    else:
        return Response(content= "This user doesn't have authorization to edit this post", status_code= status.HTTP_401_UNAUTHORIZED)
