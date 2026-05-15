from openai import OpenAI
import requests

# openai_client = OpenAI()
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

    return response.content

def openai_process_message(user_message, api_key):
    client = OpenAI(api_key=api_key)

    prompt = (
        "Act like a personal assistant. You can respond to questions, "
        "translate sentences, summarize news, and give recommendations. "
        "Keep responses concise - 2 to 3 sentences maximum."
    )

    openai_response = client.chat.completions.create(
        model="gpt-5-nano",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_completion_tokens=1000
    )

    print("openai response:", openai_response)

    response_text = openai_response.choices[0].message.content
    return response_text