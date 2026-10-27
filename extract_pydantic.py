import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from typing import Literal
from pydantic import BaseModel,Field,ValidationError


load_dotenv()


client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)

class Review(BaseModel):
    sentiment: Literal["positive","negative","neutral"]=Field(
        description="общее настроение отзыва"
    )
    score: int = Field(ge=1,le=5,
                       description="оценка пользователя:1-очень плохо,5-отлично")
    topics: list[str]=Field(
        description="конкретные аспекты,о которых говорится; доставка качесство цена и т.д."
    )



MODEL="recursive/flint-v1.0:free"

messages=[]

system_prompt = "извлеки данные из отзыва"

review_text = "all of this was so good"

resp = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": review_text},
    ],
    response_format={
        "type":"json_schema",
        "json_schema":{
            "name":"review",
            "strict":True,
            "schema":Review.model_json_schema()
        },
    },
)

raw = resp.choices[0].message.content
print("Сырой ответ:", raw)


try:
    result=Review.model_validate_json(raw)
except ValidationError as e:
    print("Model response was wrong")
    print(e)
    exit()

print(result.sentiment)
print(result.score)
print(result.topics)