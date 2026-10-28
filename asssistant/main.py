import os
import json
import openai
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
    max_retries=5,
)

model="recursive/flint-v1.0:free"

def calculate(a,operation,b):
    if operation == "+":
        return str(a+b)
    elif operation == "-":
        return str(a-b)
    elif operation == "*":
        return str(a*b)
    elif operation == "/":
        if b==0:
            return "div/0"
        return str(a/b) 
    elif operation == "%":
        return str(a%b) 
    else:
        return "unknown operation"

def  save_note(text):
    with open("note.txt","a",encoding="utf-8") as file:
        file.write(text + "\n")
    return "Note was saved"

def read_notes():
    with open("note.txt","r",encoding="utf-8") as file:
        content=file.read()
    if not content.strip():
        return "No notes"
    else:
        return content


tools=[
    {
    "type":"function",
    "function":{
        "name":"calculate",
        "description":"Узнать результат выражение",
        "parameters":{
            "type":"object",
            "properties":{
                "a":{"type":"number","description":"Первое число"},
                "operation":{"type":"string","enum":["+","-","/","*","%"]},
                "b":{"type":"number","description":"Второе число"},           
        },
        "required":["a","operation","b"],
            },
        },
    },
{
    "type":"function",
    "function":{
        "name":"save_note",
        "description":"Сохранить содержимое файла",
        "parameters":{
            "type":"object",
            "properties":{
                "text":{"type":"string","description":"заметки"}         
        },
        "required":["text"],
        },
    },
},
{
    "type":"function",
    "function":{
        "name":"read_notes",
        "description":"Узнать содержимое файла",
        "parameters":{
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
}

]

system_prompt="""Ты личный помощник в терминале.Четкость,отвечаешь коротко но со смыслом.Для любых вычислений используй функцию calculate,считать самому не надо
Если пользователь хочеть сохранить что то из разговора или попросить запомнить что то,сохраняй через save_note.
ЕСЛИ спрашивает о заметках используй read_notes,не придумывай сам текст"""

messages=[{"role":"system","content":system_prompt}]

max_steps=15
while True:
    user_input=input("User: ")
    if user_input == "/exit":
        break
    messages.append({"role":"user","content":user_input})

    for step in range(max_steps):
        try:
            response=client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                extra_body={
                    "models":[
                        "recursive/flint-v1.0:free",
                        "thinkingmachines/inkling:free",
                        "openrouter/free",
                    ]
                },
            )
        except openai.APIError as e:
            print("For now our product has issues")
            break

        message=response.choices[0].message
        model_want=message.tool_calls

        if not model_want:
            print(message.content)
            break
        messages.append(message)

        for call in model_want:
            try:
                args = json.loads(call.function.arguments)
            except json.JSONDecodeError:
                args = None
                result = "Ошибка: аргументы не в формате JSON, попробуй снова"
            if call.function.name == "calculate":
                result=calculate(args["a"],args["operation"],args["b"])
            elif call.function.name == "save_note":
                result=save_note(args["text"])
            elif call.function.name == "read_notes":
                result=read_notes()
            else:
                result="unknown function"

            messages.append({
                "role":"tool",
                "tool_call_id":call.id,
                "content":result,
            })
            print(f"Step {step} : {call.function.name}({args}) ->{result}")
    else:
        print("Agent cant do this",max_steps," steps")