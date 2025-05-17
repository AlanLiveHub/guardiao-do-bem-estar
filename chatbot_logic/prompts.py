# meu_guardiao_do_bem_estar/chatbot_logic/prompts.py
from config import DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE # Se precisar do disclaimer aqui

# Prompts para o Check-in Emocional
def get_checkin_scale_response_prompt(user_scale_response):
    return f"""INSTRUÇÃO ESPECIAL: O usuário está respondendo a um check-in emocional.
A pergunta foi: "Como você está se sentindo hoje, numa escala de 1 a 5 (sendo 1 muito mal e 5 muito bem)?"
Resposta do usuário (um número de 1 a 5): "{user_scale_response}"

Sua tarefa:
1. Valide gentilmente o sentimento (ex: "Entendi, um {user_scale_response}.").
2. Interprete brevemente o número.
3. Sugira UMA micro-ação apropriada do "Kit de Primeiros Socorros Emocionais" (respiração, mindfulness simples, listar 3 coisas boas, pequena pausa).
4. SE A SUGESTÃO FOR UM EXERCÍCIO GUIADO (respiração, mindfulness), PERGUNTE se o usuário gostaria de ser guiado (ex: "Posso te guiar. O que acha?").
5. Mantenha a resposta curta (2-4 frases), empática. Não dê conselhos médicos. Não repita o disclaimer.
"""

def get_checkin_word_response_prompt(user_word_response):
    return f"""INSTRUÇÃO ESPECIAL: O usuário está respondendo a um check-in emocional.
A pergunta foi: "Qual palavra descreve sua energia ou sentimento predominante hoje?"
Resposta do usuário (uma ou poucas palavras): "{user_word_response}"

Sua tarefa:
1. Valide gentilmente o sentimento (ex: "Entendo que você está se sentindo '{user_word_response}'.").
2. Com base na palavra (ex: 'cansado', 'ansioso', 'feliz', 'neutro'), sugira UMA micro-ação apropriada do "Kit de Primeiros Socorros Emocionais" (respiração, mindfulness simples, listar 3 coisas boas, pequena pausa).
   - Se 'cansado' ou 'sobrecarregado': Sugira uma pausa ou respiração.
   - Se 'ansioso' ou 'estressado': Sugira respiração ou mindfulness.
   - Se 'feliz' ou 'bem': Sugira listar 3 coisas boas para reforçar.
   - Se 'neutro' ou 'ok': Sugira uma pequena pausa ou um copo d'água.
3. SE A SUGESTÃO FOR UM EXERCÍCIO GUIADO (respiração, mindfulness), PERGUNTE se o usuário gostaria de ser guiado (ex: "Posso te guiar. O que acha?").
4. Mantenha a resposta curta (2-4 frases), empática. Não dê conselhos médicos. Não repita o disclaimer.
"""

# Prompt para Guia de Respiração
def get_breathing_guidance_prompt():
    return f"""INSTRUÇÃO ESPECIAL: O usuário aceitou ser guiado em um exercício de 3 respirações profundas.
Forneça instruções CLARAS e CURTAS, passo a passo, para o usuário fazer 3 respirações profundas. Numere os passos. Mantenha um tom calmo. Ao final, adicione uma frase positiva. Não repita o disclaimer inicial.
"""

# Prompt para a primeira mensagem (se não usar system_instruction ou para modelos mais antigos)
def get_initial_disclaimer_prompt(user_input_text):
    disclaimer_blob = " ".join(DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE)
    return (
        f"INSTRUÇÃO: Sua primeira resposta deve começar com: \"{disclaimer_blob}\". "
        f"Depois, responda à mensagem: \"{user_input_text}\"."
    )

# Adicione outros prompts aqui conforme necessário