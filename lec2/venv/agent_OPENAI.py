import json
from dotenv import load_dotenv
from openai import OpenAI

client = OpenAI()


# Made this Tool which can fetch the real time weather data from the API. 
# Tool means function.
def get_weather(city: str):
   # TODO: NEED TO DO AN API CALL
   return "31 degree celcius"

system_prompt="""
     You are an helpful AI assistant who is specialized in resolving user query.
     You work on start, plan, action, observe mode.
     For the given user query and availble tools, plan the step by step execution, based on the planning,
     select the relevant tool from the availble tool, and based on the tool selection you perform an action to call the tool.
     Wait for the observation and based on the obeservation from the tool call resolve the user query.


     Rules:
     - Follow the Output JSON Format.
     - Always perform one step at a time and wait for next input.
     - Carefully analyse the user query.

     Output JSON Format:
     {{ 
          "step":"string",
          "content":"string",
          "function":"The name of function if the step is action.",
          "step":"The input parameter for the function",
     }}


     
     Availble Tools: 
       

     Example:
     User Query: What is the weather of new york?
     Output: {{"step":"plan", "content":"The user is intrested in weather data of new york"}}
     Output: {{"step":"plan", "content":"From the avaible tools I should call get_weather"}}
     Output: {{"step":"action", "function":"get_weather", "input":"new york"}}
     Output: {{"step":"observe", "output":"12 degree Cel"}}
     Output: {{"step":"output", "content":"The weather for new york seems to be 12 degrees."}}



"""

messages = [
   {"role": "system","content":system_prompt},
]

user_query=input('> ')

messages.append({"role":"user","content":user_query})

while True:
   completion = client.chat.completions.create(
       model="gpt-5.5",
          response_format={"type":"json_object"},
          messages=messages,
   )

   parsed_output=json.loads(completion.choices[0].message.content)
   # loads convert json to object format, & dumps convert object to json format
   messages.append({"role":"assistant","content":json.dumps(parsed_output)})

   if parsed_output.get("step")=="plan":
         print(f"🧠: {parsed_output.get("content") }")
         continue
   

completion = client.chat.completions.create(
    model="gpt-5.5",
    response_format={"type":"json_object"},
    messages=[
       {
           "role": "system",
           "content":system_prompt,
        },
        {
            "role": "user",
            "content":"What is current weather of Michigan?",
        },
        {
            "role": "assistant",
            "content":json.dump({{"step":"plan", "content":"The user is intrested in weather data of new york"}}),
       },
       # whatever input you get after run above code, put that output in next content |
       #                                                                              |    
       {
           "role": "assistant",
           "content":json.dump({{"step":"plan", "content":"From the available tools, I should call get_weather to obtain the weather information for new york."}}),
        },
        {
            "role": "assistant",
            "content":json.dump({{"step":"action","function":"get_weather", "input":"new york"}}),
        },
        {
            "role": "assistant",
            "content":json.dump({{"step":"observe", "output":"31 degree celcius"}}),
        },

    ],
)

print(completion.choices[0].message.content)