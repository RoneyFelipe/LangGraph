import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GEMINI_KEY')
TAVILY_API_KEY = os.getenv('TAVILY_KEY')