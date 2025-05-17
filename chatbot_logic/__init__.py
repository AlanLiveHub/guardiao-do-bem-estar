# meu_guardiao_do_bem_estar/chatbot_logic/__init__.py
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL

model_instance = None 

if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        if "1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL:
            model_instance = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_INSTRUCTION_FOR_MODEL)
            print(f"INFO (chatbot_logic): Modelo {MODEL_NAME} instanciado COM system_instruction.")
        else:
            model_instance = genai.GenerativeModel(MODEL_NAME)
            print(f"INFO (chatbot_logic): Modelo {MODEL_NAME} instanciado SEM system_instruction direto.")
    except Exception as e:
        print(f"FATAL (chatbot_logic): Falha ao instanciar modelo Gemini ({MODEL_NAME}): {e}")
else:
    print("FATAL (chatbot_logic): GEMINI_API_KEY não encontrada. Modelo não instanciado.")