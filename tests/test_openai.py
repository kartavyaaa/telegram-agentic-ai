import sys
print(sys.executable)
from app.core.config import settings

from app.core.openai_client import (
    create_chat_completion
)

response = create_chat_completion(
    model="gpt-5.4-mini",
    messages=[
        {
            "role": "user",
            "content": "Hello"
        }
    ]
)

print(response.choices[0].message.content)