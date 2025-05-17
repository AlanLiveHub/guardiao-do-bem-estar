# meu_guardiao_do_bem_estar/config.py
import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API key GEMINI_API_KEY not found in .env file.")

MODEL_NAME = "gemini-1.5-flash-latest"
SYSTEM_INSTRUCTION_FOR_MODEL = f"""Você é 'Meu Guardião do Bem-Estar'. Mantenha um tom positivo, conciso e empático. Seu objetivo é auxiliar usuários a construir e manter hábitos que promovam o bem-estar físico e mental.
O usuário já recebeu uma mensagem de boas-vindas com o disclaimer principal (sobre não substituir ajuda profissional e o contato do CVV) ao abrir o chat.
Portanto, em suas respostas subsequentes, NÃO repita esse disclaimer inicial completo, a menos que seja estritamente relevante para uma pergunta específica sobre limites ou o usuário peça conselhos que você claramente não pode dar (nesse caso, reforce a busca por ajuda profissional e o CVV).
Concentre-se em responder diretamente à pergunta ou comentário do usuário de forma útil e encorajadora.
"""

DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE = [
    "Olá! Sou seu Guardião do Bem-Estar. 👋",
    "Lembre-se, NÃO substituo ajuda profissional. Se precisar de ajuda IMEDIATA, contate o CVV (Centro de Valorização da Vida) no 188 ou cvv.org.br."
]
RISKY_KEYWORDS = [
    "suicídio", "quero morrer", "não quero viver", "não vejo saída", "não vejo futuro", 
    "não vejo esperança", "sumir", "não aguento mais", "desisto da vida", "me matar", 
    "sem esperança", "acabar com tudo", "morte", "depressão profunda", "ansiedade incapacitante", 
    "tristeza extrema", "solidão absoluta", "desespero total", "desamparo completo", 
    "pânico constante", "medo paralisante", "angústia insuportável", "estresse esmagador", 
    "crise de ansiedade severa", "crise de pânico recorrente", "crise existencial profunda"
]
FICTION_CONTEXT_KEYWORDS = [
    "anime", "mangá", "manga", "filme", "série", "seriado", "livro", "personagem", 
    "história", "conto", "jogo", "game", "ficção", "enredo", "trama", "autor", 
    "one piece", "naruto", "luffy", "ace", "dragon ball", "harry potter", "goku"
]
CVV_MESSAGE_TEXT_PARTS = [
    "Percebi que você pode estar precisando de apoio imediato.",
    "Por favor, entre em contato com o CVV (Centro de Valorização da Vida) ligando para 188 (ligação gratuita) ou acesse cvv.org.br.",
    "Sua vida é importante e há ajuda disponível. Você não está sozinho(a)."
]

CHECKIN_KEYWORDS = ["check-in", "checkin", "como estou", "me sinto", "sentimento", "energia"]
AFFIRMATIVE_KEYWORDS = ["sim", "quero", "pode ser", "aceito", "ok", "s", "claro", "sim por favor", "gostaria", "manda", "isso", "por favor", "aceitar"]

BREATHING_EXERCISE_KEYWORDS = ["respira", "respiração", "respirar", "1", "um", "primeira", "opcao 1", "opção 1"]
SOUNDS_EXERCISE_KEYWORDS = ["som", "sons", "escuta", "ouvir", "2", "dois", "segunda", "opcao 2", "opção 2"]
BODYSCAN_EXERCISE_KEYWORDS = ["corpo", "corporal", "escaneamento", "scan", "3", "tres", "terceira", "opcao 3", "opção 3"]


SESSION_KEY_UI_HISTORY = 'ui_chat_history_v4' 
SESSION_KEY_SDK_HISTORY = 'sdk_gemini_history_v4'
SESSION_KEY_SDK_MSG_COUNT = 'sdk_message_count_v4'
SESSION_KEY_ASKED_SCALE = "asked_checkin_scale_v4"
SESSION_KEY_ASKED_WORD = "asked_checkin_word_v4"
SESSION_KEY_PENDING_GUIDANCE_BREATHING = "pending_guidance_offer_breathing_v4"
SESSION_KEY_PENDING_GUIDANCE_SOUNDS = "pending_guidance_offer_sounds_v4"
SESSION_KEY_PENDING_GUIDANCE_BODYSCAN = "pending_guidance_offer_bodyscan_v4"
SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS = "suggested_three_good_things_v4"

APP_SECRET_KEY = os.urandom(24)