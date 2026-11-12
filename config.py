
import os
from dotenv import load_dotenv

from agents import (
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    set_tracing_export_api_key
)

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configure OpenAI tracing separately
set_tracing_export_api_key(OPENAI_API_KEY)

# Gemini client
gemini_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Gemini model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash-lite",
    openai_client=gemini_client
)
