# meu_guardiao_do_bem_estar/chatbot_logic/prompts.py
from config import DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE

def get_checkin_scale_response_prompt(user_scale_response):
    try:
        scale_value = int(user_scale_response)
        validation_text = f"Entendi, um {user_scale_response}."
    except ValueError:
        scale_value = None
        validation_text = f"Entendi que você disse '{user_scale_response}'."

    options_text = (
        "Para momentos assim, um exercício guiado pode ajudar. Tenho estas sugestões:\n"
        "1. Exercício de respiração profunda.\n"
        "2. Exercício de atenção aos sons.\n"
        "3. Um breve escaneamento corporal para relaxar.\n"
        "Qual delas você gostaria de tentar? (Por favor, digite o número 1, 2 ou 3)."
    )
    three_good_things_suggestion = (
        "Que tal focar no positivo? Você pode me contar três pequenas coisas pelas quais se sente grato(a) hoje?"
    )

    main_suggestion_for_llm = options_text
    if scale_value is not None and scale_value >= 4:
        main_suggestion_for_llm = three_good_things_suggestion
    
    return f"""INSTRUÇÃO ESPECIAL: O usuário respondeu a um check-in de escala com "{user_scale_response}".

Sua ÚNICA tarefa é gerar uma resposta contendo UMA ÚNICA PARTE DE TEXTO (um único bloco de texto, não uma lista de partes).
Esta única parte de texto deve combinar EXATAMENTE o seguinte:
Primeiro, esta validação: "{validation_text}"
Em seguida, APENAS esta sugestão/pergunta: "{main_suggestion_for_llm}"

Exemplo de como sua resposta DEVE SER (como uma única string/parte):
"{validation_text} {main_suggestion_for_llm}"

NÃO adicione nenhum outro texto, explicação, numeração própria, ou formatação além do que foi fornecido na sugestão.
NÃO divida sua resposta em múltiplas partes ou mensagens.
Mantenha a empatia implícita no tom da validação. Não dê conselhos médicos. Não repita o disclaimer inicial.
"""

def get_checkin_word_response_prompt(user_word_response):
    user_word_lower = user_word_response.lower()
    validation_text = f"Entendo que você está se sentindo '{user_word_response}'."
    
    options_text = (
        "Para lidar com isso, um exercício guiado pode ser útil. Tenho estas sugestões:\n"
        "1. Exercício de respiração profunda.\n"
        "2. Exercício de atenção aos sons.\n"
        "3. Um breve escaneamento corporal.\n"
        "Qual delas você gostaria de tentar? (Digite 1, 2 ou 3)."
    )
    three_good_things_suggestion = (
        "Que tal cultivar esse sentimento positivo com o exercício das 'Três Coisas Boas'? "
        "Você pode me contar três coisas que contribuíram para esse seu estado hoje."
    )

    main_suggestion_for_llm = options_text
    if any(kw in user_word_lower for kw in ["feliz", "bem", "ótimo", "grato", "animado"]):
        main_suggestion_for_llm = three_good_things_suggestion
    
    return f"""INSTRUÇÃO ESPECIAL: O usuário respondeu a um check-in de palavra com "{user_word_response}".

Sua ÚNICA tarefa é gerar uma resposta contendo UMA ÚNICA PARTE DE TEXTO (um único bloco de texto, não uma lista de partes).
Esta única parte de texto deve combinar EXATAMENTE o seguinte:
Primeiro, esta validação: "{validation_text}"
Em seguida, APENAS esta sugestão/pergunta: "{main_suggestion_for_llm}"

Exemplo de como sua resposta DEVE SER (como uma única string/parte):
"{validation_text} {main_suggestion_for_llm}"

NÃO adicione nenhum outro texto, explicação, numeração própria, ou formatação além do que foi fornecido na sugestão.
NÃO divida sua resposta em múltiplas partes ou mensagens.
Mantenha a empatia implícita no tom da validação. Não dê conselhos médicos. Não repita o disclaimer inicial.
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

def get_initial_disclaimer_prompt(user_input_text):
    return user_input_text