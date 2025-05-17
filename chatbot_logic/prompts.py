# meu_guardiao_do_bem_estar/chatbot_logic/prompts.py
from config import DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE

def get_checkin_scale_response_prompt(user_scale_response):
    try:
        scale_value = int(user_scale_response)
    except ValueError:
        scale_value = None 

    # Lógica para construir a sugestão principal baseada na escala
    # Tornando as sugestões mais diretas e com menos variáveis para o LLM se perder.
    main_suggestion_llm = ""
    if scale_value is not None:
        if scale_value <= 2:
            main_suggestion_llm = (
                "Sinto muito que não esteja se sentindo tão bem. "
                "Para momentos assim, um exercício guiado pode ajudar a trazer um pouco de calma. "
                "Você gostaria de tentar um exercício de respiração ou de atenção aos sons? "
                "(Por favor, responda 'respiração' ou 'sons')."
            )
        elif scale_value == 3:
            main_suggestion_llm = (
                "Um dia mais ou menos, entendo. "
                "Para se reconectar um pouco, que tal um breve exercício de atenção aos sons ou talvez listar três coisas boas? "
                "O que te parece melhor para este momento?"
            )
        else: # 4 ou 5
            main_suggestion_llm = (
                "Que ótimo! Para manter essa boa energia, o exercício de 'Três Coisas Boas' é excelente. "
                "Que tal me contar três coisas pelas quais você se sente grato(a) hoje?"
            )
    else: # Se a entrada não for um número claro
        main_suggestion_llm = (
            "Obrigado por compartilhar. Para te ajudar a se sentir melhor ou manter o foco, "
            "sugiro um exercício de respiração, um de atenção aos sons, ou o exercício das 'Três Coisas Boas'. "
            "Alguma dessas opções te interessa?"
        )

    return f"""INSTRUÇÃO ESPECIAL: O usuário respondeu a um check-in de escala com "{user_scale_response}".

Sua tarefa:
1. Valide gentilmente o sentimento do usuário de forma concisa (ex: "Entendi, um {user_scale_response}.").
2. Em seguida, APRESENTE EXATAMENTE a seguinte sugestão ou pergunta, sem modificá-la: "{main_suggestion_llm}"
3. É crucial que sua resposta seja APENAS a validação seguida da sugestão/pergunta fornecida acima. Não adicione mais nada.
4. Mantenha a resposta curta, empática. Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

def get_checkin_word_response_prompt(user_word_response):
    user_word_lower = user_word_response.lower()
    main_suggestion_llm = ""

    if any(kw in user_word_lower for kw in ["cansado", "exausto", "sobrecarregado", "sem energia"]):
        main_suggestion_llm = (
            "Isso pode ser desgastante. Uma pequena pausa para algumas respirações profundas ou um momento de atenção aos sons pode ajudar a recarregar. "
            "Qual dos dois parece mais útil agora? (Responda 'respiração' ou 'sons')."
        )
    elif any(kw in user_word_lower for kw in ["ansioso", "estressado", "preocupado", "agitado"]):
        main_suggestion_llm = (
            "Quando nos sentimos assim, focar no presente pode ser calmante. Um exercício de atenção aos sons ou algumas respirações conscientes podem ajudar. "
            "Gostaria de tentar um deles com minha orientação? (Diga 'respiração' ou 'sons')."
        )
    elif any(kw in user_word_lower for kw in ["feliz", "bem", "ótimo", "grato", "animado"]):
        main_suggestion_llm = (
            "Que maravilha! Para cultivar ainda mais esse sentimento, que tal o exercício das 'Três Coisas Boas'? "
            "Você pode me contar três coisas que contribuíram para esse seu estado hoje."
        )
    else: 
        main_suggestion_llm = (
            "Obrigado por compartilhar. Que tal uma pequena ação como 3 respirações profundas, "
            "ou focar nos sons ao redor por um minuto? Alguma dessas te atrai?"
        )

    return f"""INSTRUÇÃO ESPECIAL: O usuário respondeu a um check-in de palavra com "{user_word_response}".

Sua tarefa:
1. Valide gentilmente o sentimento do usuário de forma concisa (ex: "Entendo que você está se sentindo '{user_word_response}'.")
2. Em seguida, APRESENTE EXATAMENTE a seguinte sugestão ou pergunta, sem modificá-la: "{main_suggestion_llm}"
3. É crucial que sua resposta seja APENAS a validação seguida da sugestão/pergunta fornecida acima. Não adicione mais nada.
4. Mantenha a resposta curta, empática. Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

def get_acknowledge_three_good_things_prompt(user_listed_items):
    return f"""INSTRUÇÃO ESPECIAL: O usuário listou três coisas pelas quais é grato: "{user_listed_items}"
Sua tarefa:
1. Reconheça positivamente (ex: "Maravilha!", "Essas são ótimas coisas!").
2. Comente brevemente sobre o benefício da gratidão (ex: "Focar no positivo realmente eleva o espírito.").
3. Finalize com uma pergunta aberta para continuar (ex: "Como posso te ajudar a continuar seu dia bem?").
Resposta curta (aprox. 3 frases), empática. Não repita o disclaimer.
"""

def get_breathing_guidance_prompt():
    return f"""INSTRUÇÃO ESPECIAL: O usuário aceitou ser guiado em 3 respirações profundas.
Forneça instruções CLARAS e CURTAS, passo a passo. Numere os passos. Tom calmo. Ao final, frase positiva. Não repita o disclaimer.
"""

def get_sound_awareness_guidance_prompt():
    return f"""INSTRUÇÃO ESPECIAL: O usuário aceitou ser guiado em 1 minuto de atenção aos sons.
Sua tarefa:
1. Instruções CLARAS e CURTAS, passo a passo, para escuta atenta por aprox. 1 minuto.
2. Sugira postura confortável, fechar os olhos (opcional).
3. Guie: notar sons distantes, próximos, sutis, sem julgamento.
4. Lembrete: trazer atenção de volta se mente divagar.
5. Guie retorno ao ambiente.
6. Finalize: "Como se sentiu após este momento de escuta atenta?".
Tom calmo. Não repita o disclaimer.
"""

def get_initial_disclaimer_prompt(user_input_text):
    # Este prompt só é usado se SYSTEM_INSTRUCTION_FOR_MODEL não for usada para o disclaimer inicial
    # e o bot não estiver em um fluxo especial na primeira mensagem.
    # Com a mensagem de boas-vindas na rota '/', este prompt para o LLM é menos provável de ser necessário
    # para o disclaimer, mas pode ser usado para garantir que a primeira resposta do LLM seja contextual.
    # Se o disclaimer já foi dado pela rota '/', então o LLM deve apenas responder ao user_input_text.
    return user_input_text