import os
from dotenv import load_dotenv
from openai import OpenAI

print(load_dotenv())

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"]
)

MODEL="recursive/flint-v1.0:free"

messagess=[{"role":"system","content":"Ты учитель по программированию,но можешь преподавать только программирование"}]


while True:
    client_request=input("Client")

    if client_request=="/exit":
        break
    messagess.append({"role":"user","content":client_request})

    response=client.chat.completions.create(
        model=MODEL,
        messages=messagess
    )

    answer=response.choices[0].message.content

    print('model', answer)

    messagess.append({"role":"user","content":answer})

