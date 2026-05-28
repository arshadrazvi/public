from langchain_openai import ChatOpenAI


def speech_to_text(audio_binary):
    return None


def text_to_speech(text, voice=""):
    return None


def openai_process_message(user_message):
    model = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
Translate the following English sentence into Spanish.
Reply ONLY with the translation.

English: {user_message}
Spanish:
"""

    response = model.invoke(prompt)

    print("openai response:", response.content)

    return response.content.strip()