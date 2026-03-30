import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "qwen/qwen3-32b"
TEMPERATURE = 0.7
MAX_TOKENS = 8192
MAX_CHAT_HISTORY = 20  # keeping this low to avoid token overflow

SYSTEM_MSG = """You are a helpful, knowledgeable, and concise AI assistant. 
Answer user questions clearly and accurately. 
If you don't know something, say so honestly rather than guessing.
Be conversational but informative."""