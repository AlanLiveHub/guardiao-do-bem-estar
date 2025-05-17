# meu_guardiao_do_bem_estar/chatbot_logic/prompts.py
from config import DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE, COMPLETED_ACTION_KEYWORDS

def get_checkin_scale_response_prompt(user_scale_response):
    try:
        scale_value = int(user_scale_response)
        validation_text = f"Entendi, um {user_scale_response}."
    except ValueError:
        scale_value = None
        validation_text = f"Entendi que você disse '{user_scale_response}'."

    main_suggestion_for_llm = ""
    if scale_value is not None:
        if scale_value <= 2:
            main_suggestion_for_llm = ("Sinto muito que não esteja se sentindo tão bem. Para momentos assim, um exercício guiado pode ajudar. Tenho estas sugestões:\n1. Exercício de respiração profunda.\n2. Exercício de atenção aos sons.\n3. Um breve escaneamento corporal para relaxar.\nQual delas você gostaria de tentar? (Digite o número 1, 2 ou 3).")
        elif scale_value == 3:
            main_suggestion_for_llm = ("Um dia mais ou menos, entendo. Para se reconectar um pouco, que tal:\n1. Um breve exercício de atenção aos sons.\n2. Um curto escaneamento corporal.\n3. Listar três coisas boas do seu dia.\nO que te parece melhor? (Digite o número ou, para as três coisas, pode começar a listá-las). Ou, se preferir algo mais simples, que tal um rápido alongamento de 1 minuto agora mesmo?")
        else: # 4 ou 5
            main_suggestion_for_llm = ("Que ótimo! Para manter essa boa energia, o exercício de 'Três Coisas Boas' é excelente. Que tal me contar três coisas pelas quais você se sente grato(a) hoje? Ou, se preferir, podemos pensar em um pequeno micro-hábito para adicionar ao seu dia, como garantir que bebeu um copo d'água recentemente!")
    else: 
        main_suggestion_for_llm = ("Obrigado por compartilhar. Para te ajudar, tenho algumas sugestões:\n1. Exercício de respiração.\n2. Exercício de atenção aos sons.\n3. Um breve escaneamento corporal.\n4. O exercício das 'Três Coisas Boas'.\nAlguma dessas opções te interessa? (Digite o número ou comece a listar as três coisas).")

    return f"""INSTRUÇÃO ESPECIAL: O usuário respondeu a um check-in de escala com "{user_scale_response}".
Sua ÚNICA tarefa é gerar uma resposta de UMA ÚNICA PARTE DE TEXTO combinando EXATAMENTE:
Primeiro, esta validação: "{validation_text}"
Em seguida, APENAS esta sugestão/pergunta: "{main_suggestion_for_llm}"
NÃO adicione mais nada. Mantenha a empatia. Não dê conselhos médicos. Não repita o disclaimer.
"""

def get_checkin_word_response_prompt(user_word_response):
    user_word_lower = user_word_response.lower()
    validation_text = f"Entendo que você está se sentindo '{user_word_response}'."
    main_suggestion_for_llm = ""

    if any(kw in user_word_lower for kw in ["cansado", "exausto", "sobrecarregado", "sem energia"]):
        main_suggestion_for_llm = ("Isso pode ser desgastante. Um exercício guiado pode ajudar a recarregar. Sugiro:\n1. Exercício de respiração profunda.\n2. Exercício de atenção aos sons.\n3. Um breve escaneamento corporal.\nQual deles parece mais útil agora? (Digite 1, 2 ou 3). Ou talvez apenas um copo d'água e uma pausa de 2 minutos?")
    elif any(kw in user_word_lower for kw in ["ansioso", "estressado", "preocupado", "agitado"]):
        main_suggestion_for_llm = ("Quando nos sentimos assim, focar no presente pode ser calmante. Tenho estas opções:\n1. Exercício de atenção aos sons.\n2. Exercício de respirações conscientes.\n3. Um breve escaneamento corporal.\nGostaria de tentar um deles com minha orientação? (Digite 1, 2 ou 3).")
    elif any(kw in user_word_lower for kw in ["feliz", "bem", "ótimo", "grato", "animado"]):
        main_suggestion_for_llm = ("Que maravilha! Para cultivar ainda mais esse sentimento, que tal o exercício das 'Três Coisas Boas'? Você pode me contar três coisas que contribuíram para esse seu estado hoje. Ou, que tal um pequeno micro-hábito como enviar uma mensagem gentil para alguém?")
    else: 
        main_suggestion_for_llm = ("Obrigado por compartilhar. Que tal uma pequena ação como:\n1. Fazer 3 respirações profundas.\n2. Focar nos sons ao redor por um minuto.\n3. Fazer um rápido escaneamento corporal.\nAlguma dessas te atrai? (Digite 1, 2 ou 3). Ou simplesmente arrumar um cantinho da sua mesa?")

    return f"""INSTRUÇÃO ESPECIAL: O usuário respondeu a um check-in de palavra com "{user_word_response}".
Sua ÚNICA tarefa é gerar uma resposta de UMA ÚNICA PARTE DE TEXTO combinando EXATAMENTE:
Primeiro, esta validação: "{validation_text}"
Em seguida, APENAS esta sugestão/pergunta: "{main_suggestion_for_llm}"
NÃO adicione mais nada. Mantenha a empatia. Não dê conselhos médicos. Não repita o disclaimer.
"""

def get_acknowledge_three_good_things_prompt(user_listed_items): # Sem alterações significativas aqui
    return f"""INSTRUÇÃO ESPECIAL: O usuário listou três coisas pelas quais é grato: "{user_listed_items}"
Sua tarefa é gerar uma ÚNICA PARTE de texto que:
1. Reconheça positivamente de forma breve (ex: "Maravilha!", "Essas são ótimas coisas!").
2. Comente brevemente sobre o benefício da gratidão (ex: "Focar no positivo realmente eleva o espírito.").
3. Finalize com uma pergunta aberta para continuar (ex: "Como posso te ajudar a continuar seu dia bem?").
A resposta deve ter cerca de 2-3 frases no total, ser empática e positiva. Não repita o disclaimer.
"""

def get_breathing_guidance_prompt(): # Instruir para ÚNICA PARTE
    return f"""INSTRUÇÃO ESPECIAL: O usuário escolheu o exercício de 3 respirações profundas.
Sua tarefa é fornecer instruções CLARAS e CURTAS, passo a passo, em UMA ÚNICA PARTE DE TEXTO.
Use numeração (1., 2., 3.). Mantenha um tom calmo e encorajador.
Ao final, adicione uma frase positiva curta, como "Espero que isso tenha ajudado!".
Não repita o disclaimer.
"""

def get_sound_awareness_guidance_prompt(): # Instruir para ÚNICA PARTE
    return f"""INSTRUÇÃO ESPECIAL: O usuário escolheu o exercício de 1 minuto de atenção aos sons.
Sua tarefa é fornecer instruções CLARAS e CURTAS, passo a passo, para escuta atenta por aproximadamente 1 minuto, tudo em UMA ÚNICA PARTE DE TEXTO.
1. Sugira postura confortável e, opcionalmente, fechar os olhos.
2. Guie o usuário a notar diferentes tipos de sons (distantes, próximos, sutis) sem julgamento.
3. Inclua um lembrete para gentilmente trazer a atenção de volta se a mente divagar.
4. Após o período de escuta, guie o usuário a retornar a atenção ao ambiente.
5. Finalize com uma pergunta gentil, como "Como se sentiu após este momento de escuta?".
Mantenha um tom calmo e encorajador. Não repita o disclaimer inicial.
"""

def get_body_scan_guidance_prompt(): # Instruir para ÚNICA PARTE
    return f"""INSTRUÇÃO ESPECIAL: O usuário escolheu o breve exercício de escaneamento corporal.
Sua tarefa é fornecer instruções CLARAS e CURTAS, passo a passo, para um escaneamento corporal de aproximadamente 1-2 minutos, tudo em UMA ÚNICA PARTE DE TEXTO.
1. Sugira uma postura confortável (sentado ou deitado).
2. Guie a atenção do usuário através de algumas partes principais do corpo (ex: pés, pernas, abdômen, peito, ombros, rosto), pedindo para notar sensações sem julgamento.
3. Encoraje o relaxamento de tensões percebidas.
4. Após o escaneamento, guie o usuário a retornar a atenção ao ambiente.
5. Finalize com uma pergunta gentil, como "Como você se sente depois deste momento de atenção ao corpo?".
Mantenha um tom calmo e relaxante. Não repita o disclaimer inicial.
"""

def get_celebrate_achievement_prompt(user_action_description):
    return f"""INSTRUÇÃO ESPECIAL: O usuário acaba de relatar que completou uma ação ou hábito positivo.
Ação relatada pelo usuário: "{user_action_description}"

Sua tarefa:
1. CELEBRE a conquista do usuário com entusiasmo e encorajamento genuíno (ex: "Isso é fantástico!", "Parabéns por isso!", "Que maravilha, fico muito feliz por você!").
2. Reforce brevemente o benefício da ação ou o valor de dar pequenos passos (ex: "Cada pequena ação positiva conta muito para o nosso bem-estar.", "É ótimo ver você cuidando de si!").
3. Se apropriado e não repetitivo, você pode perguntar como ele se sentiu após a ação ou oferecer uma próxima sugestão leve. (ex: "Como você se sentiu depois disso?", ou "Que tal manter essa energia positiva com [outro micro-hábito]?"). Mas priorize a celebração.
Mantenha a resposta curta (2-3 frases), vibrante e positiva. Não repita o disclaimer.
"""

def get_initial_disclaimer_prompt(user_input_text):
    return user_input_text