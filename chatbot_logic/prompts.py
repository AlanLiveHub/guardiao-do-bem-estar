# meu_guardiao_do_bem_estar/chatbot_logic/prompts.py
from config import (
    DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE, 
    POINTS_CHECKIN_COMPLETED, 
    POINTS_THREE_GOOD_THINGS_COMPLETED, 
    POINTS_GUIDED_EXERCISE_ACCEPTED,
    POINTS_MICRO_HABIT_REPORTED 
)

def get_checkin_scale_response_prompt(user_scale_response, new_total_points_after_checkin):
    try:
        scale_value = int(user_scale_response)
        validation_text = f"Entendi, um {user_scale_response}."
    except ValueError:
        scale_value = None
        validation_text = f"Entendi que você disse '{user_scale_response}'."

    main_suggestion_for_llm = ""
    if scale_value is not None:
        if scale_value <= 2: # Sentimentos mais desafiadores
            main_suggestion_for_llm = (
                "Sinto muito que não esteja se sentindo tão bem. Para momentos assim, um exercício guiado pode ajudar a trazer um pouco de calma. Tenho estas sugestões:\n"
                "1. Exercício de respiração profunda.\n"
                "2. Exercício de atenção aos sons.\n"
                "3. Um breve escaneamento corporal para relaxar.\n"
                "Qual delas você gostaria de tentar? (Por favor, digite o número 1, 2 ou 3)."
            )
        elif scale_value == 3: # Humor neutro
            main_suggestion_for_llm = (
                "Um dia mais ou menos, entendo. Para se reconectar um pouco, tenho algumas ideias:\n"
                "1. Um breve exercício de atenção aos sons.\n"
                "2. Um curto escaneamento corporal.\n"
                "3. Listar três coisas boas do seu dia.\n"
                "O que te parece melhor para este momento? (Digite o número da opção ou, para as três coisas boas, pode começar a listá-las)."
            )
        else: # 4 ou 5 (Humor positivo)
            main_suggestion_for_llm = (
                "Que ótimo! Para manter essa boa energia, o exercício de 'Três Coisas Boas' é excelente. "
                "Que tal me contar três coisas pelas quais você se sente grato(a) hoje?"
            )
    else: # Se a entrada não for um número claro
        main_suggestion_for_llm = (
            "Obrigado por compartilhar. Para te ajudar, tenho algumas sugestões:\n"
            "1. Exercício de respiração.\n"
            "2. Exercício de atenção aos sons.\n"
            "3. Um breve escaneamento corporal.\n"
            "4. O exercício das 'Três Coisas Boas'.\n" # Adiciona 3GT como opção 4 aqui
            "Alguma dessas opções te interessa? (Digite o número ou comece a listar as três coisas)."
        )

    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário respondeu a um check-in de escala com "{user_scale_response}".
Por este check-in, ele ganhou {POINTS_CHECKIN_COMPLETED} pontos! Seu novo total de pontos de bem-estar é {new_total_points_after_checkin}.

Sua resposta DEVE SER UMA ÚNICA STRING formatada assim:
"{validation_text} Ótimo! E por compartilhar, você ganhou +{POINTS_CHECKIN_COMPLETED} pontos, totalizando {new_total_points_after_checkin} pontos de bem-estar! {main_suggestion_for_llm}"

NÃO adicione nenhum outro texto, explicação, ou formatação.
Apenas a validação, a mensagem de pontos, e a sugestão/pergunta fornecida.
Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

def get_checkin_word_response_prompt(user_word_response, new_total_points_after_checkin):
    user_word_lower = user_word_response.lower()
    validation_text = f"Entendo que você está se sentindo '{user_word_response}'."
    
    options_text_guias = ( # Opções de guia padrão
        "Para lidar com isso ou simplesmente para um momento de pausa, um exercício guiado pode ser útil. Tenho estas sugestões:\n"
        "1. Exercício de respiração profunda.\n"
        "2. Exercício de atenção aos sons.\n"
        "3. Um breve escaneamento corporal.\n"
        "Qual delas você gostaria de tentar? (Digite 1, 2 ou 3)."
    )
    three_good_things_suggestion = (
        "Que tal cultivar esse sentimento ou simplesmente focar no positivo com o exercício das 'Três Coisas Boas'? "
        "Você pode me contar três coisas que contribuíram para algo bom no seu dia hoje."
    )

    main_suggestion_for_llm = options_text_guias # Padrão é oferecer os guias
    if any(kw in user_word_lower for kw in ["feliz", "bem", "ótimo", "grato", "animado", "amor", "amando"]):
        main_suggestion_for_llm = three_good_things_suggestion
    elif any(kw in user_word_lower for kw in ["cansado", "exausto", "sobrecarregado", "sem energia", "triste", "pra baixo", "ansioso", "estressado", "preocupado", "agitado"]):
        # Para sentimentos mais desafiadores ou neutros que podem se beneficiar de guias
        main_suggestion_for_llm = options_text_guias 
    
    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário respondeu a um check-in de palavra com "{user_word_response}".
Por este check-in, ele ganhou {POINTS_CHECKIN_COMPLETED} pontos! Seu novo total de pontos de bem-estar é {new_total_points_after_checkin}.

Sua resposta DEVE SER UMA ÚNICA STRING formatada assim:
"{validation_text} Obrigado por compartilhar! Isso te rendeu +{POINTS_CHECKIN_COMPLETED} pontos, e agora você tem {new_total_points_after_checkin} pontos! {main_suggestion_for_llm}"

NÃO adicione nenhum outro texto, explicação, ou formatação.
Apenas a validação, a mensagem de pontos, e a sugestão/pergunta fornecida.
Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

def get_acknowledge_three_good_things_prompt(user_listed_items, new_total_points):
    agradecimento = f"Maravilha! \"{user_listed_items}\" são ótimas coisas para se sentir grato(a)!"
    beneficio = "Focar no positivo realmente eleva o espírito."
    pontos_msg = f"E parabéns, você ganhou +{POINTS_THREE_GOOD_THINGS_COMPLETED} pontos por isso, acumulando {new_total_points} pontos de bem-estar!"
    continuacao = "Como posso te ajudar a continuar seu dia bem?"

    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário listou três coisas pelas quais é grato.
Ele acabou de ganhar {POINTS_THREE_GOOD_THINGS_COMPLETED} pontos! Seu novo total de pontos é {new_total_points}.

Sua resposta DEVE SER UMA ÚNICA STRING formatada assim:
"{agradecimento} {beneficio} {pontos_msg} {continuacao}"

NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

def get_breathing_guidance_prompt(new_total_points):
    intro_guia = f"Ótima escolha! E você já ganhou +{POINTS_GUIDED_EXERCISE_ACCEPTED} pontos por iniciar este exercício! Seu total é {new_total_points}."
    passo1 = "1. Sente-se ou deite-se confortavelmente, relaxando os ombros."
    passo2 = "2. Inspire profundamente pelo nariz, sentindo o abdômen expandir, conte mentalmente até 4."
    passo3 = "3. Segure o ar por um instante, se for confortável para você."
    passo4 = "4. Expire lentamente pela boca, como se estivesse soprando uma vela, esvaziando completamente os pulmões, conte mentalmente até 6."
    passo5 = "Vamos repetir mais duas vezes: inspire... segure... expire..."
    passo6 = "Mais uma vez: inspire... segure... expire..." # Adicionando a terceira respiração explicitamente
    conclusao = "Muito bem! Espero que essas respirações tenham trazido um pouco de calma."
    
    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário escolheu o exercício de 3 respirações profundas.
Ele ganhou {POINTS_GUIDED_EXERCISE_ACCEPTED} pontos, totalizando {new_total_points}.

Sua resposta DEVE SER UMA ÚNICA STRING contendo EXATAMENTE o seguinte, nesta ordem, com quebras de linha (\n) entre cada linha:
{intro_guia}\n{passo1}\n{passo2}\n{passo3}\n{passo4}\n{passo5}\n{passo6}\n{conclusao}

NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

def get_sound_awareness_guidance_prompt(new_total_points):
    intro_guia = f"Excelente! Começar este exercício de atenção aos sons te rendeu +{POINTS_GUIDED_EXERCISE_ACCEPTED} pontos! Agora você tem {new_total_points}."
    passo1 = "1. Encontre uma posição confortável, sentado ou deitado. Se quiser, feche os olhos suavemente ou mantenha um olhar baixo e relaxado."
    passo2 = "2. Por um momento, apenas traga sua atenção para os sons ao seu redor. Não precisa identificá-los ou julgá-los, apenas perceba-os."
    passo3 = "3. Comece notando os sons mais distantes que consegue ouvir... depois os sons um pouco mais próximos..."
    passo4 = "4. Agora, foque nos sons bem pertinho de você, talvez até os sons do seu próprio corpo, como sua respiração."
    passo5 = "5. Se sua mente começar a divagar com pensamentos, gentilmente traga sua atenção de volta aos sons, sem críticas."
    passo6 = "6. Permaneça assim, apenas escutando, por mais alguns instantes..."
    conclusao = "Quando estiver pronto(a), lentamente traga sua atenção de volta para a sala e abra os olhos. Como se sentiu após este momento de escuta atenta?"
    
    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário escolheu o exercício de 1 minuto de atenção aos sons.
Ele ganhou {POINTS_GUIDED_EXERCISE_ACCEPTED} pontos, totalizando {new_total_points}.

Sua resposta DEVE SER UMA ÚNICA STRING contendo EXATAMENTE o seguinte, nesta ordem, com quebras de linha (\n) entre cada linha:
{intro_guia}\n{passo1}\n{passo2}\n{passo3}\n{passo4}\n{passo5}\n{passo6}\n{conclusao}

NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

# --- FUNÇÃO FALTANTE ADICIONADA AQUI ---
def get_body_scan_guidance_prompt(new_total_points):
    intro_guia = f"Ótima decisão! Por iniciar o escaneamento corporal, você ganhou +{POINTS_GUIDED_EXERCISE_ACCEPTED} pontos, chegando a {new_total_points} no total!"
    passo1 = "1. Encontre uma posição realmente confortável, deitado(a) se possível, ou bem relaxado(a) em uma cadeira."
    passo2 = "2. Feche os olhos suavemente e faça algumas respirações lentas e profundas para começar a relaxar."
    passo3 = "3. Agora, leve sua atenção para os dedos dos seus pés. Apenas sinta qualquer sensação neles... formigamento, calor, frio, dormência... sem julgamentos."
    passo4 = "4. Lentamente, permita que essa atenção suba pelos seus pés, tornozelos, panturrilhas, joelhos e coxas, notando as sensações em cada parte."
    passo5 = "5. Traga a atenção para o seu quadril, abdômen e a parte inferior das costas. Observe a subida e descida suave da sua respiração."
    passo6 = "6. Mova a atenção para o peito, ombros, braços e mãos. Se houver tensão nos ombros, tente soltá-la um pouco a cada expiração."
    passo7 = "7. Finalmente, leve a atenção para o pescoço, rosto e cabeça. Relaxe a mandíbula, a testa, os músculos ao redor dos olhos."
    passo8 = "8. Permaneça por um momento sentindo todo o seu corpo, respirando calmamente."
    conclusao = "Quando estiver pronto(a), mexa suavemente os dedos das mãos e dos pés, e abra os olhos. Como você se sente depois deste momento de atenção ao corpo?"

    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário escolheu o breve exercício de escaneamento corporal.
Ele ganhou {POINTS_GUIDED_EXERCISE_ACCEPTED} pontos, totalizando {new_total_points}.

Sua resposta DEVE SER UMA ÚNICA STRING contendo EXATAMENTE o seguinte, nesta ordem, com quebras de linha (\n) entre cada linha:
{intro_guia}\n{passo1}\n{passo2}\n{passo3}\n{passo4}\n{passo5}\n{passo6}\n{passo7}\n{passo8}\n{conclusao}

NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

def get_celebrate_achievement_prompt(user_action_description, points_earned, new_total_points):
    celebracao = f"Isso é fantástico, parabéns por '{user_action_description}'!"
    pontos_msg = f"Você ganhou +{points_earned} pontos por essa ótima iniciativa, e agora tem {new_total_points} pontos de bem-estar!"
    beneficio = "Cada pequena ação positiva conta muito para o nosso bem-estar. Continue assim!"

    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário relatou que completou uma ação.
Ele ganhou {points_earned} pontos! Seu novo total de pontos é {new_total_points}.

Sua resposta DEVE SER UMA ÚNICA STRING formatada assim:
"{celebracao} {pontos_msg} {beneficio}"

NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

def get_initial_disclaimer_prompt(user_input_text):
    # Com a mensagem de boas-vindas na rota '/', este prompt é menos provável de ser usado,
    # mas se for, deve apenas retornar o input do usuário para uma resposta direta do LLM.
    return user_input_text