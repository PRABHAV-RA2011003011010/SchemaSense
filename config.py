import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Hugging Face
HF_TOKEN = os.getenv("HF_TOKEN")