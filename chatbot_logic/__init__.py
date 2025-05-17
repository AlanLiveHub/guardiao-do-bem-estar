# meu_guardiao_do_bem_estar/chatbot_logic/__init__.py
import google.generativeai as genai
from config import GEMINI_API_KEY, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL

# Configura a API globalmente para o pacote, se desejar
genai.configure(api_key=GEMINI_API_KEY)

# Cria a instância do modelo para ser importada por outros módulos dentro deste pacote
try:
    if "1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL:
        model_instance = genai.GenerativeModel(MODEL_NAME, system_instruction=SYSTEM_INSTRUCTION_FOR_MODEL)
        print(f"INFO (chatbot_logic): Modelo {MODEL_NAME} instanciado COM system_instruction.")
    else:
        model_instance = genai.GenerativeModel(MODEL_NAME)
        print(f"INFO (chatbot_logic): Modelo {MODEL_NAME} instanciado SEM system_instruction direto.")
except Exception as e:
    print(f"FATAL (chatbot_logic): Falha ao instanciar modelo Gemini ({MODEL_NAME}): {e}")
    model_instance = None # Ou levante a exceção para parar a aplicação
    # raise e

# Você pode importar 'model_instance' de 'chatbot_logic' em outros arquivos
# ex: from chatbot_logic import model_instance