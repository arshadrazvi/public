                         ┌──────────────────────────┐
                         │        Browser UI        │
                         │       index.html         │
                         └────────────┬─────────────┘
                                      │
                                      │ loads
                                      ▼
                         ┌──────────────────────────┐
                         │     static/script.js     │
                         │       FRONTEND           │
                         └────────────┬─────────────┘
                                      │
        ┌─────────────────────────────┴─────────────────────────────┐
        │                                                           │
        ▼                                                           ▼
User types text                                           User clicks mic
        │                                                           │
        ▼                                                           ▼
cleanTextInput()                                      recordAudio()
        │                                                           │
        ▼                                                           ▼
populateUserMessage()                              MediaRecorder starts
        │                                                           │
        ▼                                                           ▼
populateBotResponse()                              User clicks mic again
        │                                                           │
        │                                                           ▼
        │                                                 MediaRecorder stops
        │                                                           │
        │                                                           ▼
        │                                                 audioBlob created
        │                                                           │
        │                                                           ▼
        │                                      fetch("/speech-to-text")
        │                                      body: userRecording.audioBlob
        │                                                           │
        │                                                           ▼
        │                                      ┌──────────────────────────┐
        │                                      │        server.py         │
        │                                      │      BACKEND API         │
        │                                      └────────────┬─────────────┘
        │                                                   │
        │                                                   ▼
        │                                      speech_to_text_route()
        │                                                   │
        │                                                   ▼
        │                                      audio_binary = request.get_data()
        │                                                   │
        │                                                   ▼
        │                                      worker.py speech_to_text()
        │                                                   │
        │                                                   ▼
        │                                      OpenAI Whisper transcription
        │                                                   │
        │                                                   ▼
        │                                      returns text, example:
        │                                      "Hello, how are you?"
        │                                                   │
        │                                                   ▼
        │                                      server.py returns JSON:
        │                                      { "text": "Hello, how are you?" }
        │                                                   │
        │                                                   ▼
        │                                      script.js receives response.text
        │                                                   │
        │                                                   ▼
        │                                      populateUserMessage(text)
        │                                                   │
        └─────────────────────────────┬─────────────────────────────┘
                                      ▼
                         populateBotResponse(userMessage)
                                      │
                                      ▼
                         fetch("/process-message")
                         body:
                         {
                           "userMessage": userMessage,
                           "voice": voiceOption
                         }
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │        server.py         │
                         │    process_message_route │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         data = request.get_json()
                                      │
                                      ▼
                         user_message = data.get("userMessage", "")
                                      │
                                      ▼
                         openai_process_message(user_message)
                                      │
                                      ▼
                         ┌──────────────────────────┐
                         │        worker.py         │
                         │  openai_process_message  │
                         └────────────┬─────────────┘
                                      │
                                      ▼
                         ChatOpenAI / OpenAI API
                         Translate English → Spanish
                                      │
                                      ▼
                         response_text = "Hola, ¿cómo estás?"
                                      │
                                      ▼
                         server.py returns JSON:
                         {
                           "openaiResponseText": "Hola, ¿cómo estás?"
                         }
                                      │
                                      ▼
                         script.js receives response
                                      │
                                      ▼
                         Display:
                         response.openaiResponseText
                                      │
                                      ▼
                         Browser shows Spanish translation





KEY FILES
index.html
  ↓ loads

static/script.js
  ↓ frontend logic

server.py
  ↓ Flask backend routes

worker.py
  ↓ OpenAI / speech / translation logic

MAIN PATH
Text path:
User text → script.js → /process-message → server.py → worker.py → OpenAI → server.py → script.js → UI

Voice path:
Mic audio → script.js → /speech-to-text → server.py → worker.py → Whisper → server.py → script.js
           → /process-message → server.py → worker.py → OpenAI → script.js → UI
