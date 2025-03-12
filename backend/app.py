import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import openai

# Load environment variables from .env file
load_dotenv()

# Setup logging configuration with timestamps and log levels
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Create Flask app and configure CORS
app = Flask(__name__)
# You can set ALLOWED_ORIGINS in your .env file as comma separated values, e.g., "http://localhost,http://example.com"
allowed_origins = os.getenv("ALLOWED_ORIGINS", "*").split(',')
CORS(app, resources={r"/*": {"origins": allowed_origins}})

# Retrieve the OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    logging.error("OpenAI API key is not set. Please set the OPENAI_API_KEY environment variable.")
    raise ValueError("Missing OpenAI API key")
openai.api_key = openai_api_key

# Define a system prompt that instructs the AI how to respond
SYSTEM_PROMPT = (
    "You are a highly skilled coding assistant. Provide direct, code-focused answers "
    "to the user's queries. Keep your responses concise and to the point, including only the necessary "
    "code or explanation required to solve the problem. Do not provide extra commentary or unrelated details unless the user specifically asks for further explanation."
)

def generate_response(prompt: str, temperature: float = 0.7, model: str = "gpt-4o-mini") -> str:
    """
    Generates a response from the OpenAI Chat API based on the provided prompt.
    
    Args:
        prompt (str): The user's message to the chatbot.
        temperature (float): Sampling temperature.
        model (str): The OpenAI model to use.
    
    Returns:
        str: The chatbot's reply.
    
    Raises:
        Exception: If the API call fails.
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        reply = response.choices[0].message.content
        return reply
    except Exception as e:
        logging.exception("Failed to generate response from OpenAI API")
        raise e

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint to handle chat requests. Expects a JSON payload with a 'message' key.
    Returns the AI generated reply as JSON.
    """
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        logging.error("Invalid request: No JSON data or missing 'message' field.")
        return jsonify({"error": "JSON data with a 'message' field is required"}), 400

    # Trim whitespace from the message
    prompt = data.get("message", "").strip()
    if not prompt:
        return jsonify({"error": "Message cannot be empty"}), 400

    logging.info(f"Received prompt: {prompt}")

    try:
        bot_reply = generate_response(prompt)
        logging.info(f"Bot reply: {bot_reply}")
        return jsonify({"reply": bot_reply})
    except Exception:
        # Return a generic error message without exposing internal details
        return jsonify({"error": "Failed to process the request. Please try again later."}), 500

@app.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint to ensure the application is running.
    """
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    logging.info(f"Starting app on port {port}")
    # In production, consider using a WSGI server like Gunicorn
    app.run(host="0.0.0.0", port=port)
