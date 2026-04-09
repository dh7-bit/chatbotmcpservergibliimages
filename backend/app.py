from flask import Flask, request, Response, stream_with_context, json, jsonify
from flask_cors import CORS
from modelanswers import stream_modelanswer
from mcptesting import mcptesting
import re
import asyncio
import requests
import base64
import os
app = Flask(__name__)
CORS(app)

# -------------------------------
# IMAGE CONFIG
# -------------------------------
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# -------------------------------
# HOME
# -------------------------------
@app.route("/")
def home():
    return "Flask backend running!"

# -------------------------------
# IMAGE PROMPT ENHANCER
# -------------------------------
def enhance_prompt(user_prompt):
    return f"""
A beautiful Studio Ghibli inspired anime illustration of {user_prompt},
soft cinematic lighting, dreamy atmosphere, lush detailed background,
whimsical fantasy environment, expressive character design,
highly detailed, pastel colors, magical storytelling composition
""".strip()

# -------------------------------
# GENERATE IMAGE AS BASE64
# -------------------------------
def generate_image_base64(prompt):
    final_prompt = enhance_prompt(prompt)

    payload = {
        "inputs": final_prompt
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        image_bytes = response.content

        # convert bytes -> base64 string
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # return browser-friendly data URL
        return f"data:image/jpeg;base64,{image_base64}"
    else:
        raise Exception(f"Error: {response.status_code} - {response.text}")

# -------------------------------
# CHAT ROUTE (STREAMING)
# -------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    print(data)

    user_message = data.get("message", "").strip()

    def generate():
        matches = re.findall(r'[\d\.\(\)]+(?:\s*[\+\-\*/]\s*[\d\.\(\)]+)+', user_message)

        if matches:
            for i, expr in enumerate(matches):
                if i >= 1:
                    yield f"data: {json.dumps({'chunk': ' and '})}\n\n"

                expr = expr.strip()
                result = asyncio.run(mcptesting(expr))
                text = result.content[0].text

                yield f"data: {json.dumps({'chunk': f'{expr} = {text}'})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

        else:
            for chunk in stream_modelanswer(user_message):
                yield f"data: {json.dumps({'chunk': chunk})}\n\n"

            yield f"data: {json.dumps({'done': True})}\n\n"

    return Response(
        stream_with_context(generate()),
        content_type="text/event-stream"
    )

# -------------------------------
# IMAGE GENERATION ROUTE
# -------------------------------
@app.route("/generate-image", methods=["POST"])
def generate_image_route():
    prompt = request.form.get("message", "").strip()
    request_type = request.form.get("type", "").strip()

    print("Image prompt:", prompt)

    if request_type != "image":
        return jsonify({"error": "Invalid request type"}), 400

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        image_base64 = generate_image_base64(prompt)

        return jsonify({
            "caption": "Here is your generated image ✨",
            "image_url": image_base64   # frontend can use this directly
        })

    except Exception as e:
        print("Image generation error:", str(e))
        return jsonify({"error": str(e)}), 500

# -------------------------------
# RUN APP
# -------------------------------


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)