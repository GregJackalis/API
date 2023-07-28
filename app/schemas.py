from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

#use this to pass the most necessary attributes so that the other classes can inherit them and furthermore 
#expand them with more attributes depending on the class
class PostBase(BaseModel):
      title: str
      content: str
      published: bool = True  #this is a default schema value in case the client/user doesn't give any

#inheritance in python
class PostCreate(PostBase):
      pass


class UserResponse(BaseModel):
      email: EmailStr
      id: int


      class Config:
            orm_mode = True

class ReponseModel(PostBase):
      pass
      id: int
      time_created: datetime
      # owner_name: str
      owner : UserResponse

      class Config:
            orm_mode = True

class PostOut(PostBase):
      Post: ReponseModel
      votes:int

      class Config:
            orm_mode = True
      

class UserModel(BaseModel):
      email: EmailStr
      password: str


class UserLogin(BaseModel):
      email: EmailStr
      password: str

class Token(BaseModel):
      access_token: str
      token_type: str

class Token_Data(BaseModel):
      id: Optional[str]


class VoteSchema(BaseModel):
      post_id: int
      dir: conint(le=1)