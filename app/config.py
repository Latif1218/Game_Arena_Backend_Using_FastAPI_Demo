import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")