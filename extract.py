import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL="recursive/flint-v1.0:free"

messages=[]
system_prompt = """Ты извлекаешь данные из отзывов.
Отвечай ТОЛЬКО валидным JSON, без пояснений и без ```.
Формат:
{"sentiment": "positive" | "negative" | "neutral"| "unknowwn", "score": число от 1 до 5, "topics": [список тем]}"""

review="пусто"
while True:
    query=input("client")

    if query == "/exit":
        break

    messages.append({"role":'user',"content":query})

    resp=client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role":"system","content":system_prompt},
            {"role":"user","content":review},
        ],
    )

    
    raw = resp.choices[0].message.content 
    messages.append({"role":"assistant","content":raw})

    print("Сырой ответ: ",raw)


    try:
        data=json.loads(raw)
    except json.JSONDecodeError:
        print("model responsed data was not json: ",raw)
        exit()

    data=json.loads(raw)
    if data['sentiment'] not in ['positive','negative','neutral']:
        print("strange mood: ",data['sentiment'])

    if not isinstance(data['score'],int) or not 1<=data['score']<=5:
        print('strange score: ',data['score'])
