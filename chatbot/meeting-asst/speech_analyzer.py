"""
Audio transcription + summary app using Whisper and IBM WatsonX.
"""

import gradio as gr
from transformers import pipeline

from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams


# -----------------------------
# WatsonX setup
# -----------------------------

credentials = {
    "url": "https://us-south.ml.cloud.ibm.com"
}

params = {
    GenParams.MAX_NEW_TOKENS: 800,
    GenParams.TEMPERATURE: 0.1,
}

model = Model(
    model_id="meta-llama/llama-3-2-11b-vision-instruct",
    credentials=credentials,
    params=params,
    project_id="skills-network",
)


# -----------------------------
# Whisper setup
# -----------------------------

speech_to_text = pipeline(
    "automatic-speech-recognition",
    model="openai/whisper-tiny.en",
    chunk_length_s=30,
)


# -----------------------------
# App function
# -----------------------------

def analyze_audio(audio_file):
    if audio_file is None:
        return "Please upload an audio file."

    transcript = speech_to_text(audio_file, batch_size=8)["text"]

    prompt = f"""
List the key points with details from the following transcript.

Transcript:
{transcript}
"""

    response = model.generate_text(prompt=prompt)

    return f"""TRANSCRIPT:

{transcript}


SUMMARY:

{response}
"""


# -----------------------------
# Gradio UI
# -----------------------------

app = gr.Interface(
    fn=analyze_audio,
    inputs=gr.Audio(sources=["upload"], type="filepath"),
    outputs=gr.Textbox(label="Transcript and Summary", lines=20),
    title="Audio Transcription and Summary App",
    description="Upload an audio file. The app transcribes it with Whisper and summarizes it with WatsonX.",
)

app.launch(server_name="0.0.0.0", server_port=7860)