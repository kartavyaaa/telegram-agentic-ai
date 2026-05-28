from openai import OpenAI
import sys
print(sys.executable)
from app.core.config import settings

client = OpenAI(
    api_key=
)

response = client.chat.completions.create(
    model="gpt-5.4-mini",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)