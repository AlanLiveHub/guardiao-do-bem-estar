# meu_guardiao_do_bem_estar/chatbot_logic/prompts.py
from config import (
    DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE, 
    POINTS_CHECKIN_COMPLETED, 
    POINTS_THREE_GOOD_THINGS_COMPLETED, 
    POINTS_GUIDED_EXERCISE_ACCEPTED,
    POINTS_MICRO_HABIT_REPORTED 
)

# --- Prompts de Check-in ---
def get_checkin_scale_response_prompt(user_scale_response, new_total_points_after_checkin):
    try:
        scale_value = int(user_scale_response)
        validation_text = f"Entendi, um {user_scale_response}."
    except ValueError:
        scale_value = None
        validation_text = f"Entendi que você disse '{user_scale_response}'."

    # Sugestões de próximos passos
    options_text_guias = ( # Opções de exercícios guiados
        "Para momentos assim, um exercício guiado pode ajudar. Tenho estas sugestões:\n"
        "1. Exercício de respiração profunda (ótimo para acalmar o sistema nervoso e clarear a mente).\n"
        "2. Exercício de atenção aos sons (excelente para ancorar no presente e reduzir o ruído mental).\n"
        "3. Um breve escaneamento corporal para relaxar (ajuda a liberar tensões físicas e mentais).\n"
        "Qual delas você gostaria de tentar? (Por favor, digite o número 1, 2 ou 3)."
    )
    three_good_things_suggestion_text = ( # Sugestão de Três Coisas Boas
        "Que tal focar no positivo? Você pode me contar três pequenas coisas pelas quais se sente grato(a) hoje? Este exercício simples pode aumentar sentimentos de felicidade."
    )
    micro_habit_suggestion_text = ( # Sugestão de micro-hábito geral
        "Que tal escolhermos um pequeno micro-hábito para adicionar ao seu dia, como beber um copo d'água (que também ajuda na concentração!) ou fazer um alongamento rápido para despertar o corpo e a mente?"
    )

    main_suggestion_for_llm = "" 

    if scale_value is not None:
        if scale_value <= 2: 
            main_suggestion_for_llm = options_text_guias # Foco em guias para sentimentos mais desafiadores
        elif scale_value == 3: 
            main_suggestion_for_llm = ( # Oferece mix para humor neutro
                "Para se reconectar um pouco, tenho algumas ideias:\n"
                "1. Um breve exercício de atenção aos sons (para trazer mais presença).\n"
                "2. Um curto escaneamento corporal (para relaxar corpo e mente).\n"
                "3. Listar três coisas boas do seu dia (para um impulso de positividade).\n"
                "O que te parece melhor para este momento? (Digite o número ou, para as três coisas boas, pode começar a listá-las)."
            )
        else: # 4 ou 5 (Humor positivo)
            main_suggestion_for_llm = (
                f"{three_good_things_suggestion_text} {micro_habit_suggestion_text}" # Combina 3GT com sugestão de micro-hábito
            )
    else: # Se a entrada não for um número claro
        main_suggestion_for_llm = (
            "Obrigado por compartilhar. Para te ajudar, tenho algumas sugestões:\n"
            "1. Exercício de respiração (para calma e foco).\n"
            "2. Exercício de atenção aos sons (para ancorar no presente).\n"
            "3. Um breve escaneamento corporal (para relaxamento físico e mental).\n"
            "4. O exercício das 'Três Coisas Boas' (para cultivar gratidão).\n"
            "Alguma dessas opções te interessa? (Digite o número ou comece a listar as três coisas)."
        )
    
    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário respondeu a um check-in de escala com "{user_scale_response}".
Por este check-in, ele ganhou {POINTS_CHECKIN_COMPLETED} pontos! Seu novo total de pontos de bem-estar é {new_total_points_after_checkin}.

Sua resposta DEVE SER UMA ÚNICA STRING formatada assim:
"{validation_text} Ótimo! E por compartilhar, você ganhou +{POINTS_CHECKIN_COMPLETED} pontos, totalizando {new_total_points_after_checkin} pontos de bem-estar! {main_suggestion_for_llm}"

Lembre-se do princípio de CONEXÃO MENTE-CORPO: se a sugestão principal ({main_suggestion_for_llm}) mencionar uma ação física, reforce brevemente o benefício mental/emocional dela, como instruído na sua System Instruction.
NÃO adicione nenhum outro texto que não seja a validação, a mensagem de pontos e a sugestão principal (com a possível breve conexão mente-corpo).
Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

def get_checkin_word_response_prompt(user_word_response, new_total_points_after_checkin):
    user_word_lower = user_word_response.lower()
    validation_text = f"Entendo que você está se sentindo '{user_word_response}'."
    
    # Opções de texto com conexão mente-corpo implícita ou explícita
    options_text_guias = (
        f"Para lidar com o sentimento de '{user_word_response}', um exercício guiado pode ser muito útil para acalmar a mente e o corpo. Tenho estas sugestões:\n"
        "1. Exercício de respiração profunda (traz calma instantânea e clareza mental).\n"
        "2. Exercício de atenção aos sons (ajuda a focar no presente e reduzir a agitação interna).\n"
        "3. Um breve escaneamento corporal (ótimo para liberar tensões físicas que afetam o humor).\n"
        "Qual delas você gostaria de tentar? (Digite 1, 2 ou 3)."
    )
    three_good_things_suggestion_text = (
        "Que tal cultivar esse sentimento ou simplesmente focar no positivo com o exercício das 'Três Coisas Boas'? "
        "Lembrar das coisas boas ajuda a fortalecer nossa resiliência emocional. Você pode me contar três coisas que foram boas no seu dia."
    )
    micro_habit_water_suggestion = "Que tal um copo d'água agora? Manter-se hidratado(a) ajuda muito na clareza mental e disposição!"

    main_suggestion_for_llm = options_text_guias # Padrão
    if any(kw in user_word_lower for kw in ["feliz", "bem", "ótimo", "grato", "animado", "amor", "amando"]):
        main_suggestion_for_llm = f"{three_good_things_suggestion_text} Ou, para manter essa energia, {micro_habit_water_suggestion}"
    elif any(kw in user_word_lower for kw in ["cansado", "exausto", "sobrecarregado", "sem energia"]):
        main_suggestion_for_llm = f"{options_text_guias} Ou, se preferir algo mais imediato, {micro_habit_water_suggestion}"
    # Para "ansioso", "estressado", etc., o options_text_guias já é uma boa pedida.
    
    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário respondeu a um check-in de palavra com "{user_word_response}".
Por este check-in, ele ganhou {POINTS_CHECKIN_COMPLETED} pontos! Seu novo total de pontos de bem-estar é {new_total_points_after_checkin}.

Sua resposta DEVE SER UMA ÚNICA STRING formatada assim:
"{validation_text} Obrigado por compartilhar! Isso te rendeu +{POINTS_CHECKIN_COMPLETED} pontos, e agora você tem {new_total_points_after_checkin} pontos! {main_suggestion_for_llm}"

Lembre-se do princípio de CONEXÃO MENTE-CORPO: se a sugestão principal ({main_suggestion_for_llm}) mencionar uma ação física, reforce brevemente o benefício mental/emocional dela, como instruído na sua System Instruction.
NÃO adicione nenhum outro texto que não seja a validação, a mensagem de pontos e a sugestão principal (com a possível breve conexão mente-corpo).
Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

# --- Prompts para Ações Pontuáveis (LLM inclui feedback de pontos) ---
def get_acknowledge_three_good_things_prompt(user_listed_items, new_total_points):
    agradecimento = f"Maravilha! \"{user_listed_items}\" são ótimas coisas para se sentir grato(a)!"
    beneficio = "Focar no positivo e na gratidão realmente eleva o espírito e pode treinar nossa mente para notar mais coisas boas." # Conexão mente-corpo
    pontos_msg = f"E parabéns, você ganhou +{POINTS_THREE_GOOD_THINGS_COMPLETED} pontos por isso, acumulando {new_total_points} pontos de bem-estar!"
    continuacao = "Como posso te ajudar a continuar seu dia bem?"

    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário listou três coisas pelas quais é grato. Ele ganhou {POINTS_THREE_GOOD_THINGS_COMPLETED} pontos! Seu novo total de pontos é {new_total_points}.
Sua resposta DEVE SER UMA ÚNICA STRING formatada assim: "{agradecimento} {beneficio} {pontos_msg} {continuacao}"
NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

# --- NOVO PROMPT GENÉRICO PARA GUIAR EXERCÍCIO COM RAG ---
def get_rag_guided_exercise_prompt(exercise_data, points_earned, total_points):
    exercise_name = exercise_data.get("exercise_name_for_llm", "este exercício")
    
    introduction_text = exercise_data.get("introduction_template", "Vamos começar!").format(
        exercise_name=exercise_name,
        points_earned=points_earned, 
        total_points=total_points
    )
    # A introduction_template no JSON já pode incluir a conexão mente-corpo.
    # Exemplo para respiração no JSON: "Ótima escolha! ... Este exercício é excelente para acalmar o sistema nervoso e clarear a mente."
    
    steps_list = exercise_data.get("steps", ["Instrução de passo não encontrada."])
    formatted_steps = "\n".join(steps_list) 
    
    conclusion_text = exercise_data.get("conclusion_template", "Como se sentiu?")

    return f"""INSTRUÇÃO CRÍTICA: Sua tarefa é guiar o usuário através de um exercício de bem-estar.
Você deve apresentar o exercício usando EXATAMENTE os textos fornecidos, mantendo um tom calmo e encorajador.
Gere sua resposta como UMA ÚNICA PARTE DE TEXTO, usando quebras de linha (\n) para separar as seções e os passos.

Exercício a ser guiado: {exercise_name}

1.  **Introdução do Exercício:** Comece com esta frase:
    "{introduction_text}" 
    (Verifique se a 'introduction_template' no seu arquivo JSON já faz a conexão mente-corpo para este exercício específico).

2.  **Passos do Exercício:** Em seguida, apresente os seguintes passos. Mantenha a ordem e o conteúdo de cada passo:
{formatted_steps}

3.  **Conclusão do Exercício:** Após apresentar todos os passos, finalize com esta pergunta:
    "{conclusion_text}"

NÃO adicione nenhum comentário, passo ou texto adicional além dos fornecidos acima. Não repita o disclaimer inicial.
"""

# Prompt para celebração de micro-hábito (LLM informa os pontos)
def get_celebrate_achievement_prompt(user_action_description, points_earned, new_total_points):
    celebracao = f"Isso é fantástico, parabéns por '{user_action_description}'!"
    pontos_msg = f"Você ganhou +{points_earned} pontos por essa ótima iniciativa, e agora tem {new_total_points} pontos de bem-estar!"
    # Adiciona instrução para o LLM fazer a conexão mente-corpo aqui também
    beneficio_instrucao = "Explique brevemente como esta ação ('{user_action_description}') beneficia tanto o corpo quanto a mente/humor. Mantenha positivo e encorajador."

    return f"""INSTRUÇÃO CRÍTICA: Responda EXATAMENTE como instruído.
O usuário relatou que completou uma ação: "{user_action_description}".
Ele ganhou {points_earned} pontos! Seu novo total de pontos é {new_total_points}.

Sua resposta DEVE SER UMA ÚNICA STRING que inclua:
1. A celebração: "{celebracao}"
2. A mensagem de pontos: "{pontos_msg}"
3. Um breve reforço do benefício da ação, seguindo a instrução: "{beneficio_instrucao}" (Você preencherá esta parte).
Exemplo de benefício para 'beber água': "Manter-se hidratado ajuda seu corpo a funcionar bem e também melhora seu foco e humor!"

NÃO adicione nenhum outro texto. Não repita o disclaimer.
"""

def get_initial_disclaimer_prompt(user_input_text):
    return user_input_text