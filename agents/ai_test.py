from app.openai_client import OpenAIClient

ai = OpenAIClient()

answer = ai.ask(
    "Give me 5 trending YouTube AI video ideas for 2026."
)

print(answer)