from openai import OpenAI 
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key and model name from environment variables
api_key = os.getenv("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>")
client = OpenAI(api_key=api_key)

def get_response(role, prompt):
  response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
      {"role": "system", "content": f"{role}"},
      {"role": "user", "content": f"{prompt}"}
    ]
  )
  return response.choices[0].message.content
