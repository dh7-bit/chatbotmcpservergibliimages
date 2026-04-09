import requests
import json
import os


def stream_modelanswer(user_input):
    GROQ_API_KEY = os.getenv("Groq_key")

    if not GROQ_API_KEY:
        yield "Error: GROQ_API_KEY not found in environment variables."
        return

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": user_input
            }
        ],
        "stream": True
    }

    try:
        with requests.post(url, headers=headers, json=payload, stream=True) as response:
            response.raise_for_status()

            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode("utf-8")

                    if decoded_line.startswith("data: "):
                        data = decoded_line[6:].strip()

                        if data == "[DONE]":
                            break

                        try:
                            json_data = json.loads(data)
                            delta = json_data["choices"][0]["delta"].get("content", "")
                            if delta:
                                yield delta
                        except Exception:
                            continue

    except Exception as e:
        yield f"Error: {str(e)}"