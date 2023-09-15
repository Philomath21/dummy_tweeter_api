# This files establishes connection of API with the database through sqlAlchemy (ORM) 
### Copied from fastapi website to connect to SQLAlchemy
# https://fastapi.tiangolo.com/tutorial/sql-databases/  ######################

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Following is the format of the SQL string to be passed, to connect to the database.
# SQLALCHEMY_DATABASE_URL = "postgresql://<user>:<password>@<postgresserver>/<db_name>"
# Add your parameters to it
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Trim0.5@localhost/API proj database"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#############################################################################################

# Dependency (SQLAlchemy)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#############################################################################################


