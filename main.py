from openai import OpenAI
from dotenv import load_dotenv
import os
from crewai_tools import SerperDevTool
load_dotenv()
search_tool = SerperDevTool()
client = OpenAI(
    api_key=os.getenv("Grok_api_key"),
    base_url="https://api.groq.com/openai/v1"
)
response = client.chat.completions.create(
   model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "Explain what an AI agent is in 2 sentences."}
    ]
)
print(response.choices[0].message.content)
