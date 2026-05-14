# db.py

from sqlalchemy import create_engine # create_engine is used to create a connection to the database
from sqlalchemy.orm import sessionmaker, declarative_base # sessionmaker is used to create a session factory, which will be used to create sessions for interacting with the database

DATABASE_URL = "sqlite:///./payroll.db" # DATABASE_URL is the URL for the database, in this case, it is a SQLite database located at ./payroll.db

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # create_engine is used to create a connection to the database, and connect_args is used to specify additional arguments for the connection, in this case, it is set to {"check_same_thread": False} to allow multiple threads to access the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # SessionLocal is a session factory that will be used to create sessions for interacting with the database, autocommit is set to False to disable autocommit mode, autoflush is set to False to disable autoflush mode, and bind is set to the engine created earlier to specify the database connection

Base = declarative_base() # Base is a base class for all the models in the database, it is created using declarative_base() which is a function that returns a new base class for declarative class definitions

# Dependency for FastAPI to get a database session 
def get_db():
    db = SessionLocal() # get_db is a function that creates a new session using the SessionLocal session factory
    try:
        yield db # yield is used to return the session, and it will be closed automatically when the function exits
    finally:
        db.close() # close the session when the function exits