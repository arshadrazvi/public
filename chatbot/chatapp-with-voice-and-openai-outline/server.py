'''
    Flask server voice chatbot
'''
import base64
import json
import yaml
import os

from flask_cors import CORS
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

KEY_PATH = "/Users/arshad/github.com/"
KEY_FILE = "config.yaml"
SECRET_FILE = KEY_PATH + KEY_FILE

print("SERVER.PY STARTED", SECRET_FILE)

with open(SECRET_FILE, "r") as file:
    config = yaml.safe_load(file)
api_key = config["openai"]["api_key"] # paste your key here if you have one
print('****KEY****',api_key[:7])

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech-to-text")
    audio_binary = request.data # Get the user's speech from their request
<<<<<<< HEAD
    text = speech_to_text(audio_binary, api_key) # Call speech_to_text function to transcribe the speech
=======
    text = speech_to_text(audio_binary) # Call speech_to_text function to transcribe the speech
>>>>>>> 7a6f470 (not processing audio - base url issue)

	# Return the response back to the user in JSON format
    response = app.response_class(
        response=json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    print(response.data)
    return response


@app.route('/process-message', methods=['POST'])
def process_message_route():
    '''
        message route
    '''
    user_message = request.json['userMessage'] # Get user's message from their request
    print('user_message', user_message)

    voice = request.json['voice'] # Get user's preferred voice from their request
    print('voice', voice)

	# Call openai_process_message function to process the user's message and get a response back
    openai_response_text = openai_process_message(user_message, api_key)

	# Clean the response to remove any emptylines
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])

	# Call our text_to_speech function to convert OpenAI Api's reponse to speech
<<<<<<< HEAD
    openai_response_speech = text_to_speech(
    text=openai_response_text,
    api_key=api_key,
    voice="nova"
    )
=======
    openai_response_speech = text_to_speech(openai_response_text, voice)
>>>>>>> 7a6f470 (not processing audio - base url issue)

    # convert openai_response_speech to base64 string so it can be sent back in the JSON response
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')

	# Send a JSON response back to the user containing their message's response both
    # # in text and speech formats

    response = app.response_class(
        response=json.dumps(
            {"openaiResponseText": openai_response_text,
            "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )

    print(response)
    return response



if __name__ == "__main__":
    app.run(port=8000, host='0.0.0.0')
