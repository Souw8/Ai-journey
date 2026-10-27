import os
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

MODEL = "recursive/flint-v1.0:free"

messages = [] 

while True:
    user_input = input("Ты: ")

    if user_input=='/exit':
        break

    messages.append({'role':'user','content':user_input})

    resp = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    answer = resp.choices[0].message.content

    print("Модель:", answer)

    messages.append({'role':'assistant','content':answer})
