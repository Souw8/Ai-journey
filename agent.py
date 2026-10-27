import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    max_retries=5,
)

MODEL="recursive/flint-v1.0:free"


def get_weather(city):
    fake_data={"Almaty":"+5 C ,cloudy","Astana":"-3 C,snow"}
    return fake_data.get(city,"no data")



def get_time(city):
    actual_data={"Almaty":"18:42","Astana":"18:42"}
    return actual_data.get(city,"no data")
tools=[
    {
        "type":"function",
        "function":{
            "name":"get_weather",
            "description":"Узнать текущую погоду в городе",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{"type":"string","description":"in english"}
                },
                "required":["city"],
            },
        },
    },
    {
        "type":"function",
        "function":{
            "name":"get_time",
            "description":"Узнать время города",
            "parameters":{
                "type":"object",
                "properties":{
                    "city":{"type":"string","description":"in english"}
                },
                "required":["city"],
            },
        },
    }
]


messages=[{"role":"user","content":"Где сейчас теплее: в Алматы или в Астане"}]


max_steps=5
for step in range(max_steps):
    response=client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
    extra_body={
        "models": [
            "recursive/flint-v1.0:free",
            "thinkingmachines/inkling:free",
            "openrouter/free",
        ]
    },
)
    message=response.choices[0].message
    model_want=message.tool_calls

    if not model_want:
        print(message.content)
        break

    messages.append(message)

    for call in model_want:
        args=json.loads(call.function.arguments)
        if call.function.name == "get_weather":
            result=get_weather(args["city"])
        elif call.function.name == "get_time":
            result=get_time(args["city"])
        else:
            result="unknown function"

        messages.append({
                "role":"tool",
                "tool_call_id":call.id,
                "content":result,
            })
        print(f"Шаг {step}: {call.function.name}({args}) -> {result}")
else:
     print("Агент не справился за", max_steps, "шагов")
