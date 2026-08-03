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

completion = client.chat.completions.create(
    model="gpt-5.5",
    messages=[
        {
            "role": "user",
            "content":"What is current weather of Michigan?",
        },
    ],
)

print(completion.choices[0].message.content)