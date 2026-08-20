from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)
MODEL = "openai/gpt-oss-120b"


def call_llm(messages, tools):
    return client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )
