from openai import OpenAI       # import necessary dependencies
from dotenv import load_dotenv

load_dotenv()          # load your dotenv thruough this

client=OpenAI()       #make client of openAI via calling this

result = client.chat.completions.create(
    model="gpt-4",    
     temprature=0.5,
    max_tokens=200, 
    messages=[
       {  "role":"user", 
          "content": "Hey there !!"
       },
       
         {  "role":"user", 
          "content": "What is 2+2*0 ?"
       },
       
    ]
)

print(result.choices[0].message.content);       
 
# this will print what is mnodel's response is 