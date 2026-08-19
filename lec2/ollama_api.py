from fastapi import FastAPI    #import fastapi
from ollama import Client      #import ollama
from fastapi import Body       #import body part from fat api

app=FastAPI()                  #make app of fastapi

#made client for ollama 
client=Client(
  host='http://localhost:11434'
)

#pull this model before start the server
client.pull('gemma3:1b')

@app.post("/chat")             #make route of chat with post call
#so, if user post anything on /chat route,he/she can chat and need to run ollama on /chat route


# pass message parameter as string and write where it comes as an output (here, we have body and write description )
def chat(message: str = Body(...,description="Chat Message")):
  #now, let's take messages from the user and return whatever response come through model
  response = client.chat(model="gemma3:1b" , messages=[
    #and remove hardcoded part and make it dynamic as passing messgae to content
    {"role":"user","content":message}
  ])

  return response['message']['content']
