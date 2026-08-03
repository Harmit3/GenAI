from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[
        types.Content(
            role="user", parts=[types.Part.from_text(text="What is current weather of Michigan?")]
        )
    ],
)
print(response.text)