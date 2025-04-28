from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os #module for handling environments configurations
from dotenv import load_dotenv


#dotenv best practices
load_dotenv() #load variables from .env


# Creates the DB Connection
engine = create_engine("DATABASE_URL") 


#safely fetches the value from .env
DATABASE_URL = os.getenv("DATABASE_URL")

#allow us to interact with the DB (opening a sesssion)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define models(tables)
Base = declarative_base()



#THIS FILE READS FROM THE .env