import os
import yaml
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from worker import openai_process_message

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Load API key
KEY_PATH = "/Users/arshad/github.com/"
KEY_FILE = "config.yaml"
SECRET_FILE = KEY_PATH + KEY_FILE

print("SERVER.PY STARTED", SECRET_FILE)

with open(SECRET_FILE, "r") as file:
    config = yaml.safe_load(file)

api_key = config["openai"]["api_key"]
os.environ["OPENAI_API_KEY"] = api_key

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# @app.route("/speech-to-text", methods=["POST"])
# def speech_to_text_route():
#     return jsonify({
#         "error": "speech-to-text not implemented yet"
#     }), 501

@app.route("/speech-to-text", methods=["POST"])
def speech_to_text_route():
    try:
        print("MIC ROUTE HIT")
        print("content-type:", request.content_type)
        print("content-length:", request.content_length)

        audio_binary = request.get_data()
        print("audio bytes received:", len(audio_binary))
        return jsonify({
            "text": "hello"
    })
    except:
        return jsonify({
        "error": "speech-to-text not implemented yet"
    }), 501


@app.route("/process-message", methods=["POST"])
def process_message_route():
    data = request.get_json()

    user_message = data.get("userMessage", "")
    print("user_message check", user_message)

    response_text = openai_process_message(user_message)

    return jsonify({
        "openaiResponseText": response_text
    })


if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0")