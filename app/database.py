from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql://nashon:23456@localhost/muchai"

# Creates the DB Connection
engine = create_engine(DATABASE_URL) 

#allow us to interact with the DB (opening a sesssion)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#define models(tables)
Base = declarative_base()

