import os
import re
import uuid
from functools import wraps

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request

load_dotenv()

app = Flask(__name__)

AZURE_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
AZURE_LOCATION = os.getenv("AZURE_TRANSLATOR_LOCATION")
API_KEY = os.getenv("OPENAI_API_KEY")

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "No API key provided"}), 401
        
        # 从 Bearer token 中提取 API key
        try:
            api_key = auth_header.split('Bearer ')[-1]
        except:
            return jsonify({"error": "Invalid API key format"}), 401
        
        if api_key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401
            
        return f(*args, **kwargs)
    return decorated_function

@app.route("/v1/models", methods=["GET"])
def list_models():
    return jsonify(
        {
            "data": [
                {
                    "id": "azure-translator",
                    "object": "model",
                    "created": 1686935002,
                    "owned_by": "azure",
                }
            ]
        }
    )


@app.route("/v1/chat/completions", methods=["POST"])
@require_api_key
def chat_completions():
    try:
        data = request.json
        messages = data.get("messages", [])

        # Get the last message content
        last_message = messages[-1]["content"]
        print("--------------------------------")
        print(last_message)
        print("--------------------------------")

        pattern = re.compile(
            r"<translate_input>((?:(?!</?translate_input>).)*?)</translate_input>",
            re.DOTALL,
        )
        matches = pattern.findall(last_message)

        results = [match.strip() for match in matches]
        if results:
            last_message = results[0]

        # Translate to English using Azure Translator
        path = "/translate"
        match = re.search(
            r"<translate_input>\s*(.*?)\s*</translate_input>", last_message, re.DOTALL
        )
        if match:
            last_message = match.group(1).strip()
            print(last_message)  # 输出 "目标文字"

        # Translate to English using Azure Translator
        path = "/translate"
        constructed_url = AZURE_ENDPOINT + path

        params = {"api-version": "3.0", "to": "en"}

        headers = {
            "Ocp-Apim-Subscription-Key": AZURE_KEY,
            "Ocp-Apim-Subscription-Region": AZURE_LOCATION,
            "Content-type": "application/json",
            "X-ClientTraceId": str(uuid.uuid4()),
        }

        body = [{"text": last_message}]

        response = requests.post(
            constructed_url, params=params, headers=headers, json=body
        )
        translation_result = response.json()

        translated_text = translation_result[0]["translations"][0]["text"]

        return jsonify(
            {
                "id": str(uuid.uuid4()),
                "object": "chat.completion",
                "created": int(uuid.uuid1().time // 1e7),
                "model": "azure-translator",
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": translated_text},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": len(last_message),
                    "completion_tokens": len(translated_text),
                    "total_tokens": len(last_message) + len(translated_text),
                },
            }
        )

    except Exception as e:
        return jsonify(
            {"error": {"message": str(e), "type": "invalid_request_error", "code": 400}}
        ), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
