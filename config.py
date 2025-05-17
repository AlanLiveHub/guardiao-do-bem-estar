# meu_guardiao_do_bem_estar/config.py
import os
from dotenv import load_dotenv

load_dotenv() # Carrega variáveis do .env para este módulo também, se necessário

# Chave da API Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API key GEMINI_API_KEY not found in .env file.")

# Configurações do Modelo
MODEL_NAME = "gemini-1.5-flash-latest" # Ou o modelo que você estiver usando

# Instrução de Sistema para o Modelo (se aplicável)
SYSTEM_INSTRUCTION_FOR_MODEL = f"""Você é 'Meu Guardião do Bem-Estar'. Sua primeira resposta DEVE incluir o seguinte disclaimer e depois responder à pergunta do usuário: "Olá! Sou seu Guardião do Bem-Estar. 👋 Lembre-se, NÃO substituo ajuda profissional. Se precisar de ajuda IMEDIATA, contate o CVV (Centro de Valorização da Vida) no 188 ou cvv.org.br. " Após esta primeira introdução, NÃO repita o disclaimer, a menos que seja estritamente relevante ou o usuário peça conselhos que você não pode dar. Mantenha um tom positivo, conciso e empático."""

# Constantes de Texto e Palavras-chave
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
] # Revise e ajuste conforme necessário

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

# Palavras-chave para Check-in
CHECKIN_KEYWORDS = ["check-in", "checkin", "como estou", "me sinto", "sentimento", "energia"]

# Palavras-chave afirmativas para confirmação de guia
AFFIRMATIVE_KEYWORDS = ["sim", "quero", "pode ser", "aceito", "ok", "s", "claro", "sim por favor", "gostaria", "manda", "isso"]

# Chaves de Sessão (para consistência)
SESSION_KEY_UI_HISTORY = 'ui_chat_history'
SESSION_KEY_SDK_HISTORY = 'sdk_gemini_history' # Para persistência do histórico do SDK
SESSION_KEY_SDK_MSG_COUNT = 'sdk_message_count' # Para persistência da contagem de msgs do SDK

SESSION_KEY_ASKED_SCALE = "asked_checkin_scale"
SESSION_KEY_ASKED_WORD = "asked_checkin_word"
SESSION_KEY_PENDING_GUIDANCE = "pending_guidance_offer_breathing" # Pode generalizar depois
# SESSION_KEY_LAST_CHECKIN_TYPE = 'last_checkin_type' # Não mais usado com random.choice

# Outras configurações
APP_SECRET_KEY = os.urandom(24) # Para a app Flask