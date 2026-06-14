import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")