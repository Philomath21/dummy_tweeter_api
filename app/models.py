# models represents tables in the database

from .database import Base       # .database is database.py file
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

# Always capitalize first letter of the name of the class in python
class Tweet(Base):
    __tablename__ = "tweets"    # define table name

    # defining columns
    # to understand parameters, pgadmin4 column parameters can be reffered
    id = Column(Integer, primary_key= True, nullable= False)
    user_id= Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"), nullable= False)
    tweet_content = Column(String, nullable= False)
    created_at= Column(TIMESTAMP(timezone=True),
                       nullable=False,
                       server_default= text('now()'))    # server_default = text('now()') to take the current time as input
    user_details = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True, nullable= False)
    email = Column(String, primary_key= False, unique= True, nullable= False)
    password = Column(String, nullable= False)
    created_at= Column(TIMESTAMP(timezone=True),
                       nullable=False,
                       server_default= text('now()'))
    

class Like(Base):
    __tablename__ = "likes"

    tweet_id = Column(Integer, ForeignKey("tweets.id", ondelete = "CASCADE"),
                      primary_key = True, nullable= False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete = "CASCADE"),
                     primary_key = True, nullable= False)
    created_at= Column(TIMESTAMP(timezone=True),
                       nullable=False,
                       server_default= text('now()'))