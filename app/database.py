from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os  # module for handling environment configurations
from dotenv import load_dotenv


# Load variables from .env
load_dotenv()

#Fetch DATBASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

#Validate DATABASE_URL
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set in your .env file")
    
# Safely fetch the value from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the DB Connection
engine = create_engine(DATABASE_URL)


# Allow us to interact with the DB (opening a session)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define models (tables)
Base = declarative_base()

#Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# THIS FILE READS FROM THE .env
