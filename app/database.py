from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os  # module for handling environment configurations
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()


# Safely fetch the value from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the DB Connection
engine = create_engine(DATABASE_URL)


# Allow us to interact with the DB (opening a session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define models (tables)
Base = declarative_base()

# THIS FILE READS FROM THE .env
