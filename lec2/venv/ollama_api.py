from fastapi import FastAPI    #import fastapi
from ollama import Client      #import ollama

app=FastAPI()                  #make app of fastapi

#made client for ollama 
client=Client(
  host='http://localhost:11434'
)

#pull this model before start the server
client.pull('gemma3:1b')

@app.post("/chat")             #make route of chat with post call
#so, if user post anything on /chat route,he/she can chat and need to run ollama on /chat route

def chat():
  #now, let's take messages from the user and return whatever response come through model
  response = client.chat(model="gemma3:1b" , messages=[
    {"role":"user","content":"Hey there!!"}
  ])

  return response['messages']['content']
