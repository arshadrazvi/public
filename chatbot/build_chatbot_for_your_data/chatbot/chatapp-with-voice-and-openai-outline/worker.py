from openai import OpenAI
import requests

# openai_client = OpenAI()
<<<<<<< HEAD
import tempfile


def speech_to_text(audio_binary, api_key):
    client = OpenAI(api_key=api_key)

    with tempfile.NamedTemporaryFile(suffix=".wav") as temp_audio:
        temp_audio.write(audio_binary)
        temp_audio.flush()

        with open(temp_audio.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

    return transcript.text

# def speech_to_text(audio_binary):
#     base_url = "https://sn-watson-stt.labs.skills.network"
#     api_url = base_url+'/speech-to-text/api/v1/recognize'

# 	# Set up parameters for our HTTP request
#     params = {
# 		'model': 'en-US_Multimedia',
# 	}

# 	# Set up the body of our HTTP request
#     body = audio_binary

# 	# Send a HTTP Post request
#     response = requests.post(api_url, 
#                params=params, 
#                data=audio_binary,
#                timeout = 10).json()

# 	# Parse the response to get our transcribed text
#     text = 'null'
#     while bool(response.get('results')):
#         print('speech to text response:', response)
#         text = response.get('results').pop().get('alternatives').pop().get('transcript')
#         print('recognised text: ', text)
#         return text

def text_to_speech(text, api_key, voice="alloy"):
    client = OpenAI(api_key=api_key)

    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text
    )

    print("OpenAI text-to-speech response:", response)

=======


def speech_to_text(audio_binary):
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'

	# Set up parameters for our HTTP request
    params = {
		'model': 'en-US_Multimedia',
	}

	# Set up the body of our HTTP request
    body = audio_binary

	# Send a HTTP Post request
    response = requests.post(api_url, 
               params=params, 
               data=audio_binary,
               timeout = 10).json()

	# Parse the response to get our transcribed text
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text

def text_to_speech(text, voice=""):
	# Set up Watson Text-to-Speech HTTP Api url
    base_url = 'https://sn-watson-stt.labs.skills.network'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'

	# Adding voice parameter in api_url if the user has selected a preferred voice
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice

	# Set the headers for our HTTP request
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }

	# Set the body of our HTTP request
    json_data = {
        'text': text,
    }

	# Send a HTTP Post request to Watson Text-to-Speech Service
    response = requests.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
>>>>>>> 7a6f470 (not processing audio - base url issue)
    return response.content

def openai_process_message(user_message, api_key):
    client = OpenAI(api_key=api_key)
<<<<<<< HEAD

    prompt = (
        "Act like a personal assistant. You can respond to questions, "
        "translate sentences, summarize news, and give recommendations. "
        "Keep responses concise - 2 to 3 sentences maximum."
    )

    openai_response = client.chat.completions.create(
=======
    print('client', client)

# def openai_process_message(user_message):
    # Set the prompt for OpenAI Api
    prompt = "Act like a personal assistant. You can respond to questions, \
        translate sentences, summarize news, and give recommendations. \
            Keep responses concise - 2 to 3 sentences maximum."
    # Call the OpenAI Api to process our prompt
    openai_response = openai_client.chat.completions.create(
>>>>>>> 7a6f470 (not processing audio - base url issue)
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_completion_tokens=1000
    )
<<<<<<< HEAD

    print("openai response:", openai_response)

    response_text = openai_response.choices[0].message.content
    return response_text
=======
    print("openai response:", openai_response)
    # Parse the response to get the response message for our prompt
    response_text = openai_response.choices[0].message.content
    return response_text
>>>>>>> 7a6f470 (not processing audio - base url issue)
