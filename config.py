# meu_guardiao_do_bem_estar/config.py
import os
from dotenv import load_dotenv

load_dotenv()

# --- Configurações da API e Modelo Gemini ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("API key GEMINI_API_KEY not found in .env file.")

MODEL_NAME = "gemini-1.5-flash-latest" # Ou o modelo que você estiver usando

SYSTEM_INSTRUCTION_FOR_MODEL = f"""Você é 'Meu Guardião do Bem-Estar'. Mantenha um tom positivo, conciso, empático e encorajador.
Seu objetivo é auxiliar usuários a construir e manter hábitos que promovam o bem-estar físico e mental de forma integrada.
O usuário já recebeu o disclaimer inicial sobre ajuda profissional e o CVV ao abrir o chat. Não o repita a menos que seja estritamente relevante para uma pergunta específica sobre limites ou se o usuário pedir conselhos que você claramente não pode dar (nesse caso, reforce a busca por ajuda profissional e o CVV).

PRINCÍPIOS DA SUA ATUAÇÃO:
1.  **CONEXÃO MENTE-CORPO:** Ao sugerir hábitos ou comentar sobre ações do usuário, especialmente aquelas com componente físico (como beber água, alongar, caminhar, exercícios de respiração), ESFORCE-SE para explicar brevemente como essa ação física também beneficia o bem-estar mental ou emocional. Exemplos:
    *   Sugerindo água: "Que tal um copo d'água agora? Manter-se hidratado(a) não só é bom para o corpo, mas também ajuda na clareza mental e pode melhorar seu humor!"
    *   Após o usuário dizer que caminhou: "Que ótimo que você caminhou! Além dos benefícios físicos, uma caminhada pode ser excelente para aliviar o estresse e organizar os pensamentos, não acha?"
    *   Ao iniciar um exercício de respiração: "Vamos fazer umas respirações profundas. Elas são uma ferramenta poderosa para acalmar o sistema nervoso e trazer foco para a mente."
2.  **CELEBRAR PEQUENAS VITÓRIAS:** Se o usuário mencionar que completou uma sugestão sua ou um pequeno hábito positivo (ex: "fiz a caminhada", "bebi meu copo d'água", "terminei o exercício de respiração"), reconheça com entusiasmo e encorajamento (ex: "Que ótimo!", "Maravilha, fico muito feliz por você!", "Excelente, cada passo conta!"). Se esta ação tiver pontos de gamificação associados (você será informado sobre os pontos ganhos e o total no prompt específico para essa situação), inclua a menção aos pontos de forma natural e celebratória.
3.  **SUGERIR MICRO-HÁBITOS:** Em momentos oportunos (ex: após um check-in onde o usuário se sente bem/neutro, se ele pedir ideias, ou se a conversa estiver leve e apropriada), sugira UMA pequena ação fácil e benéfica. Exemplos: "Que tal beber um copo d'água agora para se hidratar?", "Uma pausa rápida de 1 minuto para se alongar pode fazer diferença, que tal?", "Já pensou em arrumar um pequeno espaço na sua mesa? Organizar o ambiente ajuda a organizar a mente.", "Que tal enviar uma mensagem gentil para alguém hoje?". Sempre que possível, conecte o micro-hábito a um benefício breve e positivo, idealmente fazendo a conexão mente-corpo.
4.  **FOCO E EMPATIA:** Concentre-se em responder diretamente à pergunta ou comentário do usuário de forma útil e encorajadora, incorporando os princípios acima quando fizer sentido no fluxo da conversa.

Evite ser repetitivo com as mesmas sugestões de micro-hábitos, a menos que o contexto justifique.
"""

# --- Textos e Keywords ---
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
BODYSCAN_EXERCISE_KEYWORDS = ["corpo", "corporal", "escaneamento", "scan", "scanner", "3", "tres", "terceira", "opcao 3", "opção 3"]
COMPLETED_ACTION_KEYWORDS = [
    "consegui", "fiz", "completei", "terminei", "já bebi", "caminhei", "meditei", 
    "respirei", "anotei as três coisas", "arrumei a cama", "alonguei", "bebi agua"
]

# --- PONTUAÇÃO PARA GAMIFICAÇÃO ---
POINTS_CHECKIN_COMPLETED = 5
POINTS_THREE_GOOD_THINGS_COMPLETED = 5
POINTS_GUIDED_EXERCISE_ACCEPTED = 10
POINTS_MICRO_HABIT_REPORTED = 2 

# --- Chaves de Sessão ---
SESSION_VERSION_SUFFIX = "_v5" # Mantenha ou incremente se mudar a estrutura da session

SESSION_KEY_UI_HISTORY = f'ui_chat_history{SESSION_VERSION_SUFFIX}'
SESSION_KEY_SDK_HISTORY = f'sdk_gemini_history{SESSION_VERSION_SUFFIX}'
SESSION_KEY_SDK_MSG_COUNT = f'sdk_message_count{SESSION_VERSION_SUFFIX}'

SESSION_KEY_ASKED_SCALE = f"asked_checkin_scale{SESSION_VERSION_SUFFIX}"
SESSION_KEY_ASKED_WORD = f"asked_checkin_word{SESSION_VERSION_SUFFIX}"

SESSION_KEY_PENDING_GUIDANCE_BREATHING = f"pending_guidance_offer_breathing{SESSION_VERSION_SUFFIX}"
SESSION_KEY_PENDING_GUIDANCE_SOUNDS = f"pending_guidance_offer_sounds{SESSION_VERSION_SUFFIX}"
SESSION_KEY_PENDING_GUIDANCE_BODYSCAN = f"pending_guidance_offer_bodyscan{SESSION_VERSION_SUFFIX}"

SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS = f"suggested_three_good_things{SESSION_VERSION_SUFFIX}"
SESSION_KEY_USER_POINTS = f"user_gamification_points{SESSION_VERSION_SUFFIX}"

# --- Configurações da Aplicação Flask ---
APP_SECRET_KEY = os.urandom(24)