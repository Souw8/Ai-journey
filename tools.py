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
                    "city":{"type":"string","description":"in time format"}
                },
                "required":["city"],
            },
        },
    }
]


messages=[{"role":"user","content":"Какая погода и время в Алматы"}]


response=client.chat.completions.create(
    model=MODEL,
    messages=messages,
    tools=tools,
)

message=response.choices[0].message

print("Model wants: ",message.tool_calls)

if message.tool_calls:
    messages.append(message)

    for call in message.tool_calls:
        args=json.loads(call.function.arguments)
        if call.function.name == "get_weather":
            result=get_weather(args["city"])
            print("result of function ",result)
        elif call.function.name == "get_time":
            result=get_time(args["city"])
            print("result of function ",result)

        messages.append({
            "role":"tool",
            "tool_call_id":call.id,
            "content":result,
        })

    response2=client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
    )
    print("response: ",response2.choices[0].message.content)
else:
    print("response_without tool: ",message.content)
