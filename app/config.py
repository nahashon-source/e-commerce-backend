from dotenv import load_dotenv
import os

#Load environment variables from .env
load_dotenv()


#safely fetches the value from .env
DATABASE_URL = os.getenv("DATABASE_URL")