# assistant.py

import os
from openai import OpenAI
from dotenv import load_dotenv

# Load OpenAI key from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client only if API key is available
if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)
else:
    client = None

def load_prompt_template():
    with open("prompts/ai_qa_assistant.txt", "r") as f:
        return f.read()

def generate_qa_suggestions(project_description):
    template = load_prompt_template()
    prompt = template.format(project_description=project_description)

    response = client.chat.completions.create(
        model="gpt-4",  # Change to gpt-3.5-turbo if needed
        messages=[
            {"role": "system", "content": "You are a senior QA helping devs with test strategy."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip()
