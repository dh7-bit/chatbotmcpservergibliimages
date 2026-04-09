import ollama
import json
import os



def stream_modelanswer(user_input):
  
    stream = ollama.chat(
        model="llama3.2:3b",
        stream=True,
        messages=[{"role": "user", "content": user_input}]
    )
    for chunk in stream:
        content = chunk["message"]["content"]
        if content:
            yield content

   