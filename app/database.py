from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv("DATABASE_URL")      

# Creates the DB Connection
engine = create_engine(DATABASE_URL) 

#allow us to interact with the DB (opening a sesssion)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define models(tables)
Base = declarative_base()

