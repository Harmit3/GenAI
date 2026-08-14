import json
from dotenv import load_dotenv
from openai import OpenAI
import requests
import os

load_dotenv()

client = OpenAI()

# Tool means function. And this function is a tool.
def run_command(command):
    #execute command
    result=os.system(command=command)
    return result





#available_tools
available_tools={
    "run_command":{
        "fn":run_command,  #keep an instance of function itself
        "description":"Takes a command as input to execute on system and returns output."
    }
}


system_prompt=f"""
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
      - run_command: Takes a command as input to execute on system and returns output.

     Example:
     User Query: What is the weather of new york?
     Output: {{"step":"plan", "content":"The user is intrested in weather data of new york"}}
     Output: {{"step":"plan", "content":"From the available tools I should call get_weather"}}
     Output: {{"step":"action", "function":"get_weather", "input":"new york"}}
     Output: {{"step":"observe", "output":"12 degree Cel"}}
     Output: {{"step":"output", "content":"The weather for new york seems to be 12 degrees."}}



"""

messages = [
   {"role": "system","content":system_prompt},
]


while True:
 
  user_query=input('> ')
  messages.append({"role":"user","content":user_query})

  while True:
   completion = client.chat.completions.create(
       model="gpt-4o",
       response_format={"type":"json_object"},
       messages=messages,
   )

   parsed_output=json.loads(completion.choices[0].message.content)
   # loads convert json to object format, & dumps convert object to json format
   messages.append({"role":"assistant","content":json.dumps(parsed_output)})

   if parsed_output.get("step") == "plan":
         print(f"🧠: {parsed_output.get("content") }")
         continue


   # over here it needs to call function but it don't know which function to call so make available_tools and define there
   if parsed_output.get("step") == "action":
       tool_name=parsed_output.get("function")
       tool_input=parsed_output.get("input")

       # here, if u get tools then get tool_name and inside that get the function and finally call tool_input.
       #after that, asisgned that to output and go to to next step and continue it
       if available_tools.get(tool_name,False)!=False:
           output=available_tools[tool_name].get("fn")(tool_input)
           messages.append({"role": "assistant","content":json.dumps({"step":"observe", "output":output})})
           continue

   # if it's not plan,neither action then it would be output
   if parsed_output.get("step")=="output":
       print(f"🤖: {parsed_output.get('content')}")
       break