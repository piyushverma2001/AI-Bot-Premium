import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

@app.route("/chat", methods=["POST"])
def handle_chat():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        logging.error("No JSON data or 'message' field provided in request")
        return jsonify({"error": "JSON data with a 'message' field is required"}), 400

    prompt = data.get("message", "")
    logging.info(f"Received message: {prompt}")

    if not prompt:
        return jsonify({"error": "Message cannot be empty"}), 400

    system_prompt = (
        "You are a highly skilled coding assistant. Provide direct, code-focused answers "
        "to the user's queries. Keep your responses concise and to the point, including only the necessary "
        "code or explanation required to solve the problem. Do not provide extra commentary or unrelated details unless the user specifically asks for further explanation."
    )

    try:
        api_response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",  # Options: gpt-4o || o1 || o1-mini || gpt-4o-mini
            temperature=0.7
        )
        bot_reply = api_response.choices[0].message.content
        logging.info(f"API response: {bot_reply}")
        return jsonify({"reply": bot_reply})
    except Exception as e:
        logging.exception("Error during OpenAI API call")
        return jsonify({"error": f"Open AI Error: {e}"}), 500

if __name__ == "__main__":
    app.run(debug=os.getenv("FLASK_DEBUG", "False") == "True", port=8080)
