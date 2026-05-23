from flask import Flask, request
import whisper
import tempfile

app = Flask(__name__)
model = whisper.load_model("base")

@app.route("/transcribe", methods=["POST"])
def transcribe_audio():

    audio_file = request.files["file"]

    with tempfile.NamedTemporaryFile(suffix=".m4a") as tmp:
        audio_file.save(tmp.name)

        result = model.transcribe(tmp.name)

    return {
        "transcription": result["text"]
    }

if __name__ == "__main__":
    app.run(debug=True)