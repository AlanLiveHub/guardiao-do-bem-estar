# meu_guardiao_do_bem_estar/chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import ( 
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL,
    BREATHING_EXERCISE_KEYWORDS, SOUNDS_EXERCISE_KEYWORDS, BODYSCAN_EXERCISE_KEYWORDS,
    COMPLETED_ACTION_KEYWORDS # Importa a nova lista
)
import random
import traceback

def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    user_input_lower = user_input_text.lower()
    final_bot_response_parts = []
    send_to_gemini = True
    prompt_for_gemini = None 
    is_special_flow = False

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
            send_to_gemini = False 
            is_special_flow = True 
            print(f"AVISO (flow_handler): Risco detectado. Encaminhando para CVV.")

    # 2. Lógica de Fluxos Especiais (só executa se não houve risco)
    if not is_special_flow:
        print(f"DEBUG (flow_handler): Verificando fluxos. Flags: "
              f"3GT_SUG={session_manager.was_three_good_things_suggested(flask_session_id)}, "
              f"PEND_B={session_manager.is_pending_guidance_breathing_offer(flask_session_id)}, "
              f"PEND_S={session_manager.is_pending_guidance_sounds_offer(flask_session_id)}, "
              f"PEND_BODY={session_manager.is_pending_guidance_bodyscan_offer(flask_session_id)}, "
              f"ASK_SCALE={session_manager.has_asked_checkin_scale(flask_session_id)}, "
              f"ASK_WORD={session_manager.has_asked_checkin_word(flask_session_id)}")

        # PRIORIDADE 1: Usuário está respondendo a uma oferta de guia múltipla
        if (session_manager.is_pending_guidance_breathing_offer(flask_session_id) and
            session_manager.is_pending_guidance_sounds_offer(flask_session_id)) or \
           (session_manager.is_pending_guidance_breathing_offer(flask_session_id) and \
            session_manager.is_pending_guidance_bodyscan_offer(flask_session_id)) or \
           (session_manager.is_pending_guidance_sounds_offer(flask_session_id) and \
            session_manager.is_pending_guidance_bodyscan_offer(flask_session_id)) or \
           (session_manager.is_pending_guidance_breathing_offer(flask_session_id) and \
            session_manager.is_pending_guidance_sounds_offer(flask_session_id) and \
            session_manager.is_pending_guidance_bodyscan_offer(flask_session_id)):
            
            is_special_flow = True 
            # ... (Lógica completa do CASO B3 para oferta múltipla, como na última versão)
            # Exemplo resumido:
            user_choice_input = user_input_text.strip()
            session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
            session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
            session_manager.clear_pending_guidance_bodyscan_offer(flask_session_id)
            session_manager.clear_three_good_things_suggested(flask_session_id)
            if user_choice_input == "1": prompt_for_gemini = prompts.get_breathing_guidance_prompt()
            elif user_choice_input == "2": prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
            elif user_choice_input == "3": prompt_for_gemini = prompts.get_body_scan_guidance_prompt()
            else: # Opção inválida
                final_bot_response_parts = ["Por favor, escolha uma opção válida (1, 2 ou 3). Qual exercício gostaria?"]
                send_to_gemini = False
                session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
                session_manager.set_pending_guidance_sounds_offer(flask_session_id)
                session_manager.set_pending_guidance_bodyscan_offer(flask_session_id)
        
        # PRIORIDADE 2: Ofertas de guia ÚNICAS pendentes
        elif session_manager.is_pending_guidance_breathing_offer(flask_session_id):
            is_special_flow = True; session_manager.clear_three_good_things_suggested(flask_session_id) 
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in BREATHING_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
                prompt_for_gemini = prompts.get_breathing_guidance_prompt()
            else: 
                session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
                final_bot_response_parts = ["Entendido. Se mudar de ideia sobre a respiração, só dizer."]; send_to_gemini = False
        elif session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            is_special_flow = True; session_manager.clear_three_good_things_suggested(flask_session_id)
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in SOUNDS_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
                prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
            else:
                session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
                final_bot_response_parts = ["Tudo bem. Se quiser tentar atenção aos sons depois, me avise."]; send_to_gemini = False
        elif session_manager.is_pending_guidance_bodyscan_offer(flask_session_id):
            is_special_flow = True; session_manager.clear_three_good_things_suggested(flask_session_id)
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in BODYSCAN_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_bodyscan_offer(flask_session_id)
                prompt_for_gemini = prompts.get_body_scan_guidance_prompt()
            else:
                session_manager.clear_pending_guidance_bodyscan_offer(flask_session_id)
                final_bot_response_parts = ["Ok. Se quiser tentar o escaneamento corporal depois, me diga."]; send_to_gemini = False

        # PRIORIDADE 3: Usuário está listando Três Coisas Boas
        elif session_manager.was_three_good_things_suggested(flask_session_id):
            is_special_flow = True; session_manager.clear_three_good_things_suggested(flask_session_id)
            prompt_for_gemini = prompts.get_acknowledge_three_good_things_prompt(user_input_text)
            print(f"DEBUG (flow_handler): Três Coisas Boas - Usuário supostamente listou.")
        
        # PRIORIDADE 4: Resposta a uma pergunta de check-in
        elif session_manager.has_asked_checkin_scale(flask_session_id):
            is_special_flow = True; session_manager.clear_asked_checkin_scale(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text)
            session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_pending_guidance_bodyscan_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id)
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. Flags (B/S/Scan/3GT) SET.")
        elif session_manager.has_asked_checkin_word(flask_session_id):
            is_special_flow = True; session_manager.clear_asked_checkin_word(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text)
            session_manager.set_pending_guidance_breathing_offer(flask_session_id)
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_pending_guidance_bodyscan_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id)
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. Flags (B/S/Scan/3GT) SET.")

        # PRIORIDADE 5: Detecção explícita de conclusão de ação (NOVO BLOCO)
        # Verifica se não estamos em nenhum outro fluxo ativo antes de considerar uma celebração.
        elif any(keyword in user_input_lower for keyword in COMPLETED_ACTION_KEYWORDS):
            # Verifica se alguma flag de "espera de resposta" está ativa. Se estiver, não é uma celebração isolada.
            is_awaiting_specific_response = (
                session_manager.has_asked_checkin_scale(flask_session_id) or
                session_manager.has_asked_checkin_word(flask_session_id) or
                session_manager.is_pending_guidance_breathing_offer(flask_session_id) or
                session_manager.is_pending_guidance_sounds_offer(flask_session_id) or
                session_manager.is_pending_guidance_bodyscan_offer(flask_session_id) or
                session_manager.was_three_good_things_suggested(flask_session_id)
            )
            if not is_awaiting_specific_response:
                print(f"DEBUG (flow_handler): Possível conclusão de ação detectada: '{user_input_text}'")
                prompt_for_gemini = prompts.get_celebrate_achievement_prompt(user_input_text)
                is_special_flow = True # Marca como fluxo especial, pois tem um prompt dedicado
            else:
                print(f"DEBUG (flow_handler): Keyword de conclusão detectada, mas outra flag está ativa. Deixando para fluxo normal ou outro 'elif'.")
            
        # PRIORIDADE 6: Usuário inicia um novo check-in
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            # Log ANTES da condição interna
            print(f"DEBUG (flow_handler): 'check-in' keyword detectada. Verificando flags de bloqueio...")
            # ... (logs de cada flag como na sua última versão) ...
            if not (session_manager.has_asked_checkin_scale(flask_session_id) or \
                    session_manager.has_asked_checkin_word(flask_session_id) or \
                    session_manager.is_pending_guidance_breathing_offer(flask_session_id) or \
                    session_manager.is_pending_guidance_sounds_offer(flask_session_id) or \
                    session_manager.is_pending_guidance_bodyscan_offer(flask_session_id) or \
                    session_manager.was_three_good_things_suggested(flask_session_id)):
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
            else:
                print(f"DEBUG (flow_handler): Intenção de check-in, mas uma flag de estado está ativa. Deixando para fluxo normal/LLM.")

    # 3. Fluxo Normal (se nenhum fluxo especial foi ativado)
    if not is_special_flow:
        print("DEBUG (flow_handler): Entrando no Fluxo Normal.")
        prompt_for_gemini = user_input_text # O SYSTEM_INSTRUCTION_FOR_MODEL deve guiar celebração/micro-hábitos aqui
        current_sdk_msg_count = session_manager.get_sdk_message_count(flask_session_id)
        if current_sdk_msg_count == 0 and not ("1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL):
            prompt_for_gemini = prompts.get_initial_disclaimer_prompt(user_input_text) # Usado se a mensagem inicial do app.py não existir
            print("DEBUG (flow_handler): Usando prompt com disclaimer inicial (não-1.5).")
    
    # 4. Enviar para Gemini
    if send_to_gemini and prompt_for_gemini:
        try:
            print(f"----- (flow_handler) Enviando para Gemini (ID: {flask_session_id}) -----")
            print(f"Texto para API: '{prompt_for_gemini}'")
            
            if sdk_chat_obj is None:
                print("ERRO CRÍTICO (flow_handler): sdk_chat_obj é None antes de send_message.")
                raise Exception("Chat object is not initialized.")

            response_obj_from_sdk = sdk_chat_obj.send_message(prompt_for_gemini, stream=False)
            
            try:
                print(f"DEBUG (flow_handler): Resposta BRUTA do Gemini (vars): {vars(response_obj_from_sdk)}")
            except TypeError:
                print(f"DEBUG (flow_handler): Resposta BRUTA do Gemini (direto): {response_obj_from_sdk}")
            
            extracted_texts = []
            raw_extracted_texts_debug = [] 

            # Prioriza .text se for a única parte significativa
            if hasattr(response_obj_from_sdk, 'text') and response_obj_from_sdk.text and \
               (not hasattr(response_obj_from_sdk, 'parts') or not response_obj_from_sdk.parts):
                if response_obj_from_sdk.text.strip():
                    extracted_texts.append(response_obj_from_sdk.text)
                raw_extracted_texts_debug.append(f"Direct .text: '{response_obj_from_sdk.text}'")
            # Senão, processa .parts se existirem
            elif hasattr(response_obj_from_sdk, 'parts') and response_obj_from_sdk.parts:
                for i, part in enumerate(response_obj_from_sdk.parts):
                    part_text = getattr(part, 'text', None)
                    raw_extracted_texts_debug.append(f"Part {i} .text: '{part_text}'")
                    if part_text is not None and part_text.strip(): 
                        extracted_texts.append(part_text)
            # Senão, tenta candidates
            elif hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                 candidate = response_obj_from_sdk.candidates[0]
                 if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for i, part_comp in enumerate(candidate.content.parts):
                        part_text = getattr(part_comp, 'text', None)
                        raw_extracted_texts_debug.append(f"Candidate Part {i} .text: '{part_text}'")
                        if part_text is not None and part_comp.text.strip(): 
                            extracted_texts.append(part_comp.text)
            
            print(f"DEBUG (flow_handler): Textos extraídos BRUTOS (com conteúdo): {raw_extracted_texts_debug}")
            
            # Se extracted_texts está vazio mas raw_extracted_texts_debug não, pode ser que só havia espaços
            if not extracted_texts and any(s is not None for s in raw_extracted_texts_debug):
                 print(f"WARN (flow_handler): Textos extraídos eram apenas espaços ou None. raw_extracted: {raw_extracted_texts_debug}")

            # Desduplicação/Seleção
            if not extracted_texts:
                final_bot_response_parts = []
            elif len(extracted_texts) == 1:
                final_bot_response_parts = extracted_texts
            else: 
                first_part_for_check = extracted_texts[0]
                if len(first_part_for_check) > 20 and all(first_part_for_check == p for p in extracted_texts):
                    print(f"WARN (flow_handler): Múltiplas partes idênticas detectadas. Usando apenas a primeira.")
                    final_bot_response_parts = [first_part_for_check]
                else:
                    print(f"INFO (flow_handler): Múltiplas partes diferentes detectadas. Usando todas.")
                    final_bot_response_parts = extracted_texts 
            
            print(f"DEBUG (flow_handler): final_bot_response_parts APÓS desduplicação/seleção: {final_bot_response_parts}")
            
            if not final_bot_response_parts:
                # ... (lógica de finish_reason e safety_ratings como antes) ...
                finish_reason = "UNKNOWN"; safety_ratings_str = "N/A"
                # ... (código para obter finish_reason e safety_ratings)
                print(f"WARN (flow_handler): Gemini respondeu sem texto útil final. FR: {finish_reason}. Safety: {safety_ratings_str}")
                if "SAFETY" in finish_reason.upper(): final_bot_response_parts = ["Minha política de segurança me impede de responder a isso."]
                else: final_bot_response_parts = ["Sinto muito, não consegui gerar uma resposta clara desta vez."]
        except Exception as e:
            print(f"EXCEÇÃO API Gemini (flow_handler): {type(e).__name__}: {e}\n{traceback.format_exc()}")
            final_bot_response_parts = ["Algo deu errado com o assistente. Tente mais tarde."]
            send_to_gemini = False 
    
    elif not final_bot_response_parts and not send_to_gemini and is_special_flow:
        final_bot_response_parts = ["Ocorreu um erro interno. Poderia tentar de novo?"]
        print(f"ERRO LÓGICO (flow_handler): Fluxo especial, mas sem resposta definida. User input: '{user_input_text}'")

    # Limpeza de flags
    if not is_special_flow and send_to_gemini: 
        # ... (lógica de limpeza de flags como na última versão, incluindo _bodyscan e as _asked flags)
        pass

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini