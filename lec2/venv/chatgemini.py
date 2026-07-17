from dotenv import load_dotenv
import os
from google import genai

load_dotenv()


client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Hey there!! Who are you?"
)

print(interaction.output_text)