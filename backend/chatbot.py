from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

# Cargar modelo y tokenizador
model_name = "facebook/blenderbot-1B-distill"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

def get_chatbot_response(query: str) -> str:
    """Genera respuestas conversacionales más detalladas con BlenderBot."""
    inputs = tokenizer(query, return_tensors="pt")
    response_ids = model.generate(**inputs, max_length=100)
    response = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response
