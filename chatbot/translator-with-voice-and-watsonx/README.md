                    ┌──────────────────────────────┐
                    │         Browser UI           │
                    │       (index.html)           │
                    └──────────────┬───────────────┘
                                   │
                                   │ GET /
                                   ▼
                    ┌──────────────────────────────┐
                    │         server.py            │
                    │         index()              │
                    └──────────────┬───────────────┘
                                   │
                                   ▼
                         Render HTML page

User enters English text
        │
        ▼
┌─────────────────────────────────────────────┐
│ Frontend JavaScript (fetch request)         │
│ POST /process-message                       │
│ { "userMessage": "Hello" }                  │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                server.py                    │
│       process_message_route()               │
│                                             │
│ data = request.get_json()                   │
│ user_message = data["userMessage"]          │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                worker.py                    │
│    openai_process_message(user_message)     │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│             ChatOpenAI API                  │
│                                             │
│ Prompt: Translate English → Spanish         │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│      Returns translated Spanish text        │
│          e.g. "Hola, ¿cómo estás?"          │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│                server.py                    │
│ return jsonify({                            │
│   "response": translated_text               │
│ })                                          │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────┐
│          Frontend JavaScript                │
│ data.response                               │
│ Display translated message                  │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
                Browser shows:
             "Hola, ¿cómo estás?"
