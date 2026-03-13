import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
PAGEINDEX_API_KEY = os.getenv("PAGEINDEX_API_KEY")
DEFAULT_LLM_MODEL = "llama-3.3-70b-versatile"
DEFAULT_TEMPERATURE = 0
