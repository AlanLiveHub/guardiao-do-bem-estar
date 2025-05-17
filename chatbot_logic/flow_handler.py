# meu_guardiao_do_bem_estar/chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import ( 
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL,
    BREATHING_EXERCISE_KEYWORDS, SOUNDS_EXERCISE_KEYWORDS # Importa as keywords de exercício
)
import random
import traceback

def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    user_input_lower = user_input_text.lower()
    final_bot_response_parts = []
    send_to_gemini = True
    prompt_for_gemini = None 
    is_special_flow = False # Flag para indicar se um fluxo especial foi tratado e se devemos pular o fluxo normal

    # 1. Lógica de Risco (Prioridade Máxima)
    potentially_risky_word_found = False
    fiction_context_found = False
    for r_keyword in RISKY_KEYWORDS:
        if r_keyword in user_input_lower:
            potentially_risky_word_found = True; break
    if potentially_risky_word_found:
        for f_keyword in FICTION_CONTEXT_KEYWORDS:
            if f_keyword in user_input_lower:
                fiction_context_found = True; break
        if not fiction_context_found:
            final_bot_response_parts = CVV_MESSAGE_TEXT_PARTS
            send_to_gemini = False # Não envia para o Gemini
            is_special_flow = True # Marca como fluxo especial para pular o resto
            print(f"AVISO (flow_handler): Risco detectado. Encaminhando para CVV.")

    # 2. Lógica de Fluxos Especiais (só executa se não houve risco)
    if not is_special_flow:
        print(f"DEBUG (flow_handler): Verificando fluxos. Flags: 3GT_SUGGESTED={session_manager.was_three_good_things_suggested(flask_session_id)}, PENDING_BREATHING={session_manager.is_pending_guidance_breathing_offer(flask_session_id)}, PENDING_SOUNDS={session_manager.is_pending_guidance_sounds_offer(flask_session_id)}, SCALE_ASKED={session_manager.has_asked_checkin_scale(flask_session_id)}, WORD_ASKED={session_manager.has_asked_checkin_word(flask_session_id)}")

        # PRIORIDADE 1: Usuário está respondendo a uma oferta de guia múltipla (Respiração OU Sons)
        if session_manager.is_pending_guidance_breathing_offer(flask_session_id) and \
           session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            print(f"DEBUG (flow_handler): CASO B3 - Ambas ofertas (B/S) pendentes. Analisando input: '{user_input_text.strip()}'")
            is_special_flow = True 
            
            # Limpa ambas as flags de oferta imediatamente, pois o usuário está respondendo à escolha
            session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
            session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
            session_manager.clear_three_good_things_suggested(flask_session_id) # Limpa 3GT também

            user_choice = user_input_text.strip()
            if user_choice == "1": # Usuário escolheu Respiração
                prompt_for_gemini = prompts.get_breathing_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU 1 (Respiração).")
            elif user_choice == "2": # Usuário escolheu Atenção aos Sons
                prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU 2 (Atenção aos Sons).")
            else: # Opção inválida ou o usuário não digitou um número esperado
                final_bot_response_parts = ["Por favor, escolha uma opção válida digitando o número (por exemplo, 1 ou 2). Qual exercício gostaria de tentar?"]
                send_to_gemini = False
                # Recoloca as flags para permitir nova tentativa de escolha
                session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
                session_manager.set_pending_guidance_sounds_offer(flask_session_id)
                print(f"DEBUG (flow_handler): Guia - Usuário não digitou 1 ou 2. Perguntando novamente.")
        
        # PRIORIDADE 2: Oferta de guia de RESPIRAÇÃO PENDENTE (única)
        elif session_manager.is_pending_guidance_breathing_offer(flask_session_id):
            is_special_flow = True
            session_manager.clear_three_good_things_suggested(flask_session_id) 
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in BREATHING_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
                prompt_for_gemini = prompts.get_breathing_guidance_prompt() 
                print(f"DEBUG (flow_handler): Guia - Usuário confirmou GUIA DE RESPIRAÇÃO (oferta única).")
            else: 
                session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
                final_bot_response_parts = ["Entendido. Se mudar de ideia sobre o exercício de respiração, é só dizer."]
                send_to_gemini = False
            
        # PRIORIDADE 3: Oferta de guia de ATENÇÃO AOS SONS PENDENTE (única)
        elif session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            is_special_flow = True
            session_manager.clear_three_good_things_suggested(flask_session_id)
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in SOUNDS_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
                prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário confirmou GUIA DE ATENÇÃO AOS SONS (oferta única).")
            else:
                session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
                final_bot_response_parts = ["Tudo bem. Se quiser tentar o de atenção aos sons em outro momento, me avise."]
                send_to_gemini = False

        # PRIORIDADE 4: Usuário está listando Três Coisas Boas
        elif session_manager.was_three_good_things_suggested(flask_session_id):
            is_special_flow = True
            # Não limpamos flags de guia aqui, pois o fluxo de 3GT é independente e pode ter sido
            # sugerido mesmo que uma oferta de guia também tenha sido feita (e ignorada).
            # O LLM no prompt de acknowledge_three_good_things foi instruído a finalizar com pergunta aberta.
            session_manager.clear_three_good_things_suggested(flask_session_id)
            prompt_for_gemini = prompts.get_acknowledge_three_good_things_prompt(user_input_text)
            print(f"DEBUG (flow_handler): Três Coisas Boas - Usuário supostamente listou.")
        
        # PRIORIDADE 5: Resposta a uma pergunta de check-in
        elif session_manager.has_asked_checkin_scale(flask_session_id):
            is_special_flow = True
            session_manager.clear_asked_checkin_scale(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text)
            # O LLM será instruído a oferecer opções (respiração/sons) ou 3GT.
            # Setamos todas as flags relevantes de "oferta pendente"
            session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id) # Se o LLM sugerir 3GT diretamente
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. Flags (B_offer/S_offer/3GT_sug) SET.")

        elif session_manager.has_asked_checkin_word(flask_session_id):
            is_special_flow = True
            session_manager.clear_asked_checkin_word(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text)
            session_manager.set_pending_guidance_breathing_offer(flask_session_id)
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id)
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. Flags (B_offer/S_offer/3GT_sug) SET.")
            
        # PRIORIDADE 6: Usuário inicia um novo check-in
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            # Esta condição só é verdadeira se NENHUMA das flags anteriores estava ativa.
            print(f"DEBUG (flow_handler): CASO E (Novo Check-in) ATIVADO.")
            is_special_flow = True; send_to_gemini = False 
            if random.choice([True, False]):
                final_bot_response_parts = ["Claro! Vamos fazer um rápido check-in.", "Numa escala de 1 a 5 (1=muito mal, 5=muito bem), como você está se sentindo agora?"]
                session_manager.set_asked_checkin_scale(flask_session_id)
                print(f"DEBUG (flow_handler): Intenção. Perguntando ESCALA. Resposta: {final_bot_response_parts}")
            else:
                final_bot_response_parts = ["Ok, vamos lá com o check-in!", "Qual palavra descreve sua energia ou sentimento predominante hoje?"]
                session_manager.set_asked_checkin_word(flask_session_id)
                print(f"DEBUG (flow_handler): Intenção. Perguntando PALAVRA. Resposta: {final_bot_response_parts}")

    # 3. Fluxo Normal (se nenhum fluxo especial foi ativado e não houve risco)
    if not is_special_flow:
        print("DEBUG (flow_handler): Entrando no Fluxo Normal.")
        prompt_for_gemini = user_input_text
        current_sdk_msg_count = session_manager.get_sdk_message_count(flask_session_id)
        # Lógica para adicionar disclaimer na primeira mensagem real ao LLM (se SYSTEM_INSTRUCTION não o faz)
        if current_sdk_msg_count == 0 and not ("1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL):
            prompt_for_gemini = prompts.get_initial_disclaimer_prompt(user_input_text)
            print("DEBUG (flow_handler): Usando prompt com disclaimer inicial (não-1.5 ou System Instruction diferente).")
    
    # 4. Enviar para Gemini se 'send_to_gemini' é True E um 'prompt_for_gemini' foi preparado
    if send_to_gemini and prompt_for_gemini:
        try:
            print(f"----- (flow_handler) Enviando para Gemini (ID: {flask_session_id}) -----")
            print(f"Texto para API: '{prompt_for_gemini}'")
            
            if sdk_chat_obj is None:
                print("ERRO CRÍTICO (flow_handler): sdk_chat_obj é None antes de send_message.")
                raise Exception("Chat object is not initialized.")

            response_obj_from_sdk = sdk_chat_obj.send_message(prompt_for_gemini, stream=False)
            print(f"DEBUG (flow_handler): Resposta BRUTA do Gemini: {response_obj_from_sdk}")
            
            extracted_texts = []
            raw_extracted_texts_debug = [] 

            if hasattr(response_obj_from_sdk, 'text') and response_obj_from_sdk.text is not None:
                raw_extracted_texts_debug.append(f"Direct .text: '{response_obj_from_sdk.text}'")
                extracted_texts.append(response_obj_from_sdk.text)
            elif hasattr(response_obj_from_sdk, 'parts') and response_obj_from_sdk.parts:
                for i, part in enumerate(response_obj_from_sdk.parts):
                    part_text = getattr(part, 'text', None)
                    raw_extracted_texts_debug.append(f"Part {i} .text: '{part_text}'")
                    if part_text is not None: extracted_texts.append(part_text)
            elif hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                 candidate = response_obj_from_sdk.candidates[0]
                 if candidate.content and candidate.content.parts:
                    for i, part_comp in enumerate(candidate.content.parts):
                        part_text = getattr(part_comp, 'text', None)
                        raw_extracted_texts_debug.append(f"Candidate Part {i} .text: '{part_text}'")
                        if part_text is not None: extracted_texts.append(part_comp.text)
            
            print(f"DEBUG (flow_handler): Textos extraídos BRUTOS: {raw_extracted_texts_debug}")
            final_bot_response_parts = [text for text in extracted_texts if text and text.strip()]
            
            if not final_bot_response_parts:
                finish_reason = "UNKNOWN"
                safety_ratings_str = "N/A"
                if hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                    candidate = response_obj_from_sdk.candidates[0]
                    finish_reason_obj = getattr(candidate, 'finish_reason', None)
                    if finish_reason_obj is not None: finish_reason = str(finish_reason_obj)
                    if hasattr(candidate, 'safety_ratings'):
                        safety_ratings_str = str([f"{rating.category.name}: {rating.probability.name}" for rating in candidate.safety_ratings]) # Usar .name para enums

                print(f"WARN (flow_handler): Gemini respondeu sem texto útil. Finish Reason: {finish_reason}. Safety Ratings: {safety_ratings_str}")
                if "SAFETY" in finish_reason.upper():
                    final_bot_response_parts = ["Minha política de segurança me impede de responder a isso. Podemos falar sobre outra coisa?"]
                else:
                    final_bot_response_parts = ["Sinto muito, não consegui gerar uma resposta clara desta vez. (Motivo: " + finish_reason + ")"]
        except Exception as e:
            print(f"EXCEÇÃO API Gemini (flow_handler): {type(e).__name__}: {e}\n{traceback.format_exc()}")
            final_bot_response_parts = ["Algo deu errado ao tentar falar com o assistente. Tente novamente mais tarde."]
            send_to_gemini = False 
    
    # Se é um fluxo especial que NÃO envia para o Gemini, e final_bot_response_parts não foi preenchido
    elif not final_bot_response_parts and not send_to_gemini and is_special_flow:
        final_bot_response_parts = ["Ocorreu um erro interno no meu fluxo de pensamento. Poderia tentar de novo?"]
        print(f"ERRO LÓGICO (flow_handler): Fluxo especial, mas sem resposta definida. User input: '{user_input_text}'")


    # Limpeza de flags se o usuário mudou de assunto E não é um fluxo especial já tratado E a mensagem foi para o Gemini (fluxo normal)
    if not is_special_flow and send_to_gemini: 
        flags_cleared_log = []
        # Limpa todas as flags de "espera" ou "sugestão"
        if session_manager.was_three_good_things_suggested(flask_session_id):
            session_manager.clear_three_good_things_suggested(flask_session_id); flags_cleared_log.append("3GT_sug")
        if session_manager.is_pending_guidance_breathing_offer(flask_session_id):
            session_manager.clear_pending_guidance_breathing_offer(flask_session_id); flags_cleared_log.append("pend_breath")
        if session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            session_manager.clear_pending_guidance_sounds_offer(flask_session_id); flags_cleared_log.append("pend_sound")
        # Não limpamos ASKED_SCALE/WORD aqui automaticamente, pois se o usuário não respondeu à pergunta de check-in
        # e mudou de assunto, o próximo "check-in" deveria continuar o ciclo.
        # Mas se uma pergunta foi feita e ignorada, e a conversa seguiu normalmente, pode ser útil limpar.
        # Para agora, vamos deixar que sejam limpas apenas quando respondidas.
        if flags_cleared_log:
            print(f"DEBUG (flow_handler): Flags de estado (sugestão/guia) foram limpas (fluxo normal após possível sugestão ignorada): {', '.join(flags_cleared_log)}")

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini