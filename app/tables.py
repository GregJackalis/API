from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "Posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=True, server_default='TRUE')
    time_created = Column(TIMESTAMP(timezone=True), nullable=False , server_default=text('NOW()'))

    #making the foreign key with sqlalchemy, also the Users.id on the foreign key part refers ot the table name and not the class name
    owner_id = Column(Integer, ForeignKey("Users.id", ondelete= "CASCADE"), nullable=False)

    # owner_name = Column(String, ForeignKey("Users.email", ondelete= "CASCADE"), nullable=False)

    owner = relationship("Users")


class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False , server_default=text('NOW()'))
    

class Vote(Base):
    __tablename__ = "Votes"
    id = Column(Integer, primary_key=True, autoincrement=True)
    User_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    Post_id = Column(Integer, ForeignKey("Posts.id", ondelete="CASCADE"), nullable=False)

    # Define a unique constraint to ensure the combination of User_id and Post_id is unique
    __table_args__ = (UniqueConstraint("User_id", "Post_id"),)