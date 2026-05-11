from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
'''
    Choosing the right model for your purposes is an 
    important part of building chatbots! You can read
    on the different types of models available on the
    Hugging Face website: https://huggingface.co/models.
'''

model_name = "facebook/blenderbot-400M-distill"

# Load model (download on first run and reference local installation for subsequent runs)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Create conversation history to refer back to.
# using list since it is a short one.

conversation_history = []
print("Chatbot ready! (type 'exit' to quit)\n")

while True:
    history_string = "\n".join(conversation_history)
    input_text = input("> ")

    prompt = history_string + f"\nUser: {input_text}\nBot:"

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    outputs = model.generate(
        **inputs,
        max_new_tokens=60,
        no_repeat_ngram_size=3,
        repetition_penalty=1.3,
        do_sample=True,
        temperature=0.6,
        top_p=0.85
    )
    ## Remove this print statement after testing
    # print(outputs)

    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    print(response)

    conversation_history.append(f"User: {input_text}")
    conversation_history.append(f"Bot: {response}")
    # print(conversation_history)

    # keep only last few exchanges (prevents confusion)
    conversation_history = conversation_history[-6:]


