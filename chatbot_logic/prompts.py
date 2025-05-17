# chatbot_logic/prompts.py
from config import DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE # Se precisar do disclaimer aqui

# Prompts para o Check-in Emocional
def get_checkin_scale_response_prompt(user_scale_response):
    return f"""INSTRUÇÃO ESPECIAL: O usuário está respondendo a um check-in emocional.
A pergunta foi: "Como você está se sentindo hoje, numa escala de 1 a 5 (sendo 1 muito mal e 5 muito bem)?"
Resposta do usuário (um número de 1 a 5): "{user_scale_response}"

Sua tarefa:
1. Valide gentilmente o sentimento (ex: "Entendi, um {user_scale_response}.").
2. Interprete brevemente o número.
3. Sugira UMA micro-ação apropriada do "Kit de Primeiros Socorros Emocionais". Opções incluem:
    - Um exercício de respiração.
    - Um exercício simples de mindfulness.
    - O exercício "Três Coisas Boas".
    - Uma pequena pausa ou um copo d'água.
4. **Formulação da Sugestão:**
   - SE A SUGESTÃO FOR UM EXERCÍCIO GUIADO (respiração, mindfulness), PERGUNTE se o usuário gostaria de ser guiado (ex: "Que tal um exercício de respiração para se centrar? Posso te guiar. O que acha?").
   - SE A SUGESTÃO FOR O EXERCÍCIO "TRÊS COISAS BOAS", convide o usuário a listar diretamente. Exemplo: "Focar no positivo pode ser útil. Que tal me contar três pequenas coisas pelas quais você se sente grato(a) hoje?" ou "Um {user_scale_response} é um bom momento para praticar a gratidão. Quais são três coisas boas no seu dia de hoje?". **EVITE perguntar 'Você quer fazer o exercício das três coisas boas?' aqui; apenas convide a listar.**
   - Para outras sugestões (pausa, água), apenas sugira.
5. Mantenha a resposta curta (2-4 frases), empática. Não dê conselhos médicos. Não repita o disclaimer inicial (o usuário já o viu).
"""

def get_checkin_word_response_prompt(user_word_response):
    return f"""INSTRUÇÃO ESPECIAL: O usuário está respondendo a um check-in emocional.
A pergunta foi: "Qual palavra descreve sua energia ou sentimento predominante hoje?"
Resposta do usuário (uma ou poucas palavras): "{user_word_response}"

Sua tarefa:
1. Valide gentilmente o sentimento (ex: "Entendo que você está se sentindo '{user_word_response}'.").
2. Com base na palavra, sugira UMA micro-ação apropriada do "Kit de Primeiros Socorros Emocionais". Opções incluem:
    - Se 'cansado', 'sobrecarregado', 'estressado', 'ansioso': Sugira uma pausa, respiração ou mindfulness.
    - Se 'feliz', 'bem', 'grato': Sugira listar 3 coisas boas para reforçar, ou uma ação para manter a energia.
    - Se 'neutro', 'ok', 'normal': Sugira uma pequena pausa, um copo d'água, ou o exercício "Três Coisas Boas".
3. **Formulação da Sugestão:**
   - SE A SUGESTÃO FOR UM EXERCÍCIO GUIADO (respiração, mindfulness), PERGUNTE se o usuário gostaria de ser guiado (ex: "Sinto que um exercício de respiração poderia ajudar com isso. Posso te guiar. O que me diz?").
   - SE A SUGESTÃO FOR O EXERCÍCIO "TRÊS COISAS BOAS", convide o usuário a listar diretamente. Exemplo: "Já que está se sentindo '{user_word_response}', que tal dedicar um momento para pensar em três coisas boas do seu dia? Você pode me contar." ou "Para cultivar esse sentimento de '{user_word_response}', quais são três coisas que te trazem um sorriso hoje?". **EVITE perguntar 'Você quer fazer o exercício das três coisas boas?' aqui; apenas convide a listar.**
   - Para outras sugestões (pausa, água), apenas sugira.
4. Mantenha a resposta curta (2-4 frases), empática. Não dê conselhos médicos. Não repita o disclaimer inicial (o usuário já o viu).
"""

# Prompt para quando o usuário lista as Três Coisas Boas
def get_acknowledge_three_good_things_prompt(user_listed_items):
    return f"""INSTRUÇÃO ESPECIAL: O usuário acabou de listar três coisas pelas quais é grato, como parte do exercício "Três Coisas Boas".
Itens listados pelo usuário: "{user_listed_items}"

Sua tarefa:
1. Reconheça positivamente o esforço e os itens listados pelo usuário (ex: "Que ótimo que você tirou um momento para isso!", "Maravilha!", "Essas são ótimas coisas para se sentir grato(a)!").
2. Faça um breve comentário encorajador sobre o benefício de focar na gratidão (ex: "Focar nas coisas boas pode realmente ajudar a mudar nossa perspectiva e aumentar o bem-estar.").
3. **Para dar continuidade à conversa, finalize com uma pergunta aberta e encorajadora, convidando o usuário a explorar mais ou indicando que você está pronto para a próxima interação.** Exemplos:
    - "Como posso te ajudar a continuar cultivando seu bem-estar agora?"
    - "Há algo mais em que posso te apoiar hoje para manter essa sensação positiva?"
    - "O que você gostaria de fazer ou conversar em seguida?"
4. Mantenha a resposta geral curta (cerca de 3 frases no total), empática e positiva.
Não repita o disclaimer inicial.
"""

# Prompt para a primeira mensagem (se não usar system_instruction ou para modelos mais antigos)
# Este prompt pode ser desnecessário se a mensagem inicial é sempre gerenciada pelo app.py
def get_initial_disclaimer_prompt(user_input_text):
    # Se a mensagem inicial é gerenciada pelo app.py, este prompt pode não ser mais usado.
    # Mas se for, o disclaimer precisa ser removido se a system instruction já não o faz.
    # Assumindo que SYSTEM_INSTRUCTION_FOR_MODEL foi atualizada para NÃO dar o disclaimer inicial:
    return user_input_text # Simplesmente passa a mensagem do usuário para uma resposta direta
    
    # Se ainda precisasse do disclaimer aqui (improvável com a lógica atual):
    # disclaimer_blob = " ".join(DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE)
    # return (
    #     f"INSTRUÇÃO: Sua primeira resposta deve começar com: \"{disclaimer_blob}\". "
    #     f"Depois, responda à mensagem: \"{user_input_text}\"."
    # )

# Adicione outros prompts aqui conforme necessário, por exemplo, para guiar mindfulness.