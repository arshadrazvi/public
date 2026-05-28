from openai import OpenAI
import tempfile
from langchain_openai import ChatOpenAI


client = OpenAI()


def speech_to_text(audio_binary):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
        temp_audio.write(audio_binary)
        temp_audio.flush()

        with open(temp_audio.name, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

    return transcript.text


def text_to_speech(text, voice=""):
    return None


def openai_process_message(user_message):
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
    print ('user message', user_message)
    prompt = f"""
Translate the following English sentence into Spanish.
Reply ONLY with the translation.

English: {user_message}
Spanish:
"""

    response = model.invoke(prompt)

    print("openai response:", response.content)

    return response.content.strip()