
from dotenv import load_dotenv
import json
import os
import requests
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

# Made this Tool which can fetch the real time weather data from the API. 
# Tool means function.
def get_weather(city: str):
   # TODO: NEED TO DO AN API CALL
   print("🛠️ Tool called:get_weather",city)
   url=f"https://wttr.in/{city}?format=%c+%t"
   response=requests.get(url)


   if response.status_code==200:
       return f"The weather in {city} is {response.text}."
   
   return "Something went wrong."



#available_tools
available_tools={
    "get_weather":{
        "fn":get_weather,         #keep an instance of function itself
        "description":"Takes a city name as an input and returns the current weather for the city"
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
         "step": "plan | action | output",
    "content": "Description of thought/output (required for plan/output)",
          "function":"The name of function if the step is action.",
          "step":"The input parameter for the function",
     }}


     
     Availble Tools: 
      - get_weather : Takes a city name as an input and returns the current weather for the city

     Example:
     User Query: What is the weather of new york?
     Output: {{"step":"plan", "content":"The user is intrested in weather data of new york"}}
     Output: {{"step":"plan", "content":"From the available tools I should call get_weather"}}
     Output: {{"step":"action", "function":"get_weather", "input":"new york"}}
     Output: {{"step":"observe", "output":"12 degree Cel"}}
     Output: {{"step":"output", "content":"The weather for new york seems to be 12 degrees."}}



"""

contents=[]

while True:
 
  user_query=input('> ')
  if user_query.lower() in ['exit', 'quit']:
        break
  contents.append(types.Content(role="user", parts=[types.Part.from_text(text=user_query)]))

  while True:
    response = client.models.generate_content(
       model="gemini-3.5-flash",
        contents=contents,
       config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json"

            )
      
    ) 


    try:
        parsed_output = json.loads(response.text)
    except json.JSONDecodeError:
        contents.append(types.Content(role="user", parts=[
            types.Part.from_text(text="Your last output was not valid JSON. Please repeat the step using valid raw JSON format.")
        ]))
        continue

   
       # loads convert json to object format, & dumps convert object to json format
    contents.append(types.Content(role="model", parts=[types.Part.from_text(text=response.text)]))

    
    if parsed_output.get("step")=="plan":
             print(f"🧠: {parsed_output.get("content") }")
             continue
    
          # over here it needs to call function but it don't know which function to call so make available_tools and define there
    if parsed_output.get("step")=="action":
           tool_name=parsed_output.get("function")
           tool_input=parsed_output.get("input")
    
    
           # here, if u get tools then get tool_name and inside that get the function and finally call tool_input.
           #after that, asisgned that to output and go to to next step and continue it
           if tool_name in available_tools:
               output=available_tools[tool_name].get("fn")(tool_input)
               observation_json = json.dumps({"step": "observe", "output": output})
               contents.append(types.Content(role="user", parts=[types.Part.from_text(text=observation_json)]))
               continue
    
        # if it's not plan,neither action then it would be output
    
    if parsed_output.get("step")=="output":
           print(f"🤖: {parsed_output.get("content") }")
           break
    
    
    