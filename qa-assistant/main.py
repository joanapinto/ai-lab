# main.py

from assistant import generate_qa_suggestions

# You can replace this with user input, or load from a file
project_description = """
I'm building a Next.js app with an authentication form (email/password) and a dashboard.
"""

response = generate_qa_suggestions(project_description)

print("=== AI QA Assistant Output ===\n")
print(response)
