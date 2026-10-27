import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

resp = client.chat.completions.create(
    model="recursive/flint-v1.0:free",
    messages=[{"role": "user", "content": "Объясни, что такое токен, в двух предложениях"}],
)

print(resp.choices[0].message.content)
print(resp.usage)