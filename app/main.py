from fastapi import FastAPI

#python communicator with sql library

#libraries for orm to work
from . import tables
from .database import engine

from .routers import post, user, auth, vote
from .config import settings

from fastapi.middleware.cors import CORSMiddleware


# tables.Base.metadata.create_all(bind=engine)



api = FastAPI()

# origins = ["https://www.google.com", "https://www.youtube.com"]
origins = ["*"]

api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    

@api.get("/")
def default():
    return{"message": "HELLO WORLD!"}
# def findPost(id):
#     for p in myPosts:
#         if p['id'] == id:
#             return p
    
# def find_index_post(id):
#     for i, p in enumerate(myPosts):
#         if p['id'] == id:
#             return i


api.include_router(post.router)
api.include_router(user.router)
api.include_router(auth.router)
api.include_router(vote.router)