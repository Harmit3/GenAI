from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

client = genai.Client()

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


response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[
       types.Content(
                   role="system", parts=[types.Part.from_text()]
               ),
        types.Content(
            role="user", parts=[types.Part.from_text(text="What is current weather of Michigan?")]
        ),

    ],
)
print(response.text)