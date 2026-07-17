from dotenv import load_dotenv
from google import genai

load_dotenv()


client = genai.Client()

interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="Hey there!! "
)

print(interaction.output_text)