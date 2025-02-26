import os
from openai import OpenAI
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key = os.getenv("OPENAI_API_KEY"))

# Make a pre-prompt for the query.
@app.route("/chat", methods=["POST"])
def response():
    data = request.json
    prompt = data.get("message", "")

    print(f"Received message: {prompt}")

    if not prompt:
        return jsonify({"error": "Message cannot be empty"}), 400

    try:
        response = client.chat.completions.create(
           messages=[
               {"role": "user", "content": prompt}
               ],
           model="gpt-4o",     #gpt-4o || o1 || o1-mini || gpt-4o-mini
           temperature=0.7
        )
        botReply = response.choices[0].message.content
        print(response.choices[0].message.content)
        return jsonify({"reply": botReply})

    except Exception as e:
        return f"Open AI Error: {e}"

if __name__ == "__main__":
    app.run(debug=True, port=8080)