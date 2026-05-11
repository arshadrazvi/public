from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import warnings

'''
    onenote:https://d.docs.live.net/7D5C3D29B2E9AA62/Documents/Viper/Knowledge%20Base/AI/IBM%20Applied%20AI%20Professional%20Certificate.one%23Creating%20chatbot&section-id=%7BAB1526B2-CC3E-6A4D-A7D1-0E34CA57B56F%7D&page-id=%7BBB17F9DC-2FDB-9C49-B4DB-6CCB44C28F09%7D&end
'''

warnings.filterwarnings("ignore")
model_name = "HuggingFaceTB/SmolLM2-360M-Instruct"

print("Loading model...")

tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token = tokenizer.unk_token

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="cpu",
    torch_dtype=torch.float32
)

messages = [{
    "role": "system",
    "content": "You are a very friendly and cheerful assistant. Always respond in a warm, casual, and encouraging tone."
}]

print("Chatbot started. Type 'exit' to quit.\n")
while True:
    user_input = input("> ")

    if user_input.lower() == "exit":
        break

    messages.append({"role": "user", "content": user_input})
    messages = [messages[0]] + messages[-10:]

    tokenized = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
        return_dict=True,
        max_length=512
    )

    with torch.inference_mode():
        outputs = model.generate(
            tokenized["input_ids"],
            attention_mask=tokenized["attention_mask"],
            max_new_tokens=60,
            temperature=0.5,
            top_p=0.8,
            do_sample=True,
            repetition_penalty=1.3,
            no_repeat_ngram_size=3,
            pad_token_id=tokenizer.pad_token_id
        )


    response = tokenizer.decode(
        outputs[0][tokenized["input_ids"].shape[-1]:],
        skip_special_tokens=True
    )
    print(f"Bot: {response}\n")

    messages.append({"role": "assistant", "content": response})


