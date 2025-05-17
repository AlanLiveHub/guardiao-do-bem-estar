# meu_guardiao_do_bem_estar/chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import ( 
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL,
    BREATHING_EXERCISE_KEYWORDS, SOUNDS_EXERCISE_KEYWORDS, BODYSCAN_EXERCISE_KEYWORDS
)
import random
import traceback

def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    user_input_lower = user_input_text.lower()
    final_bot_response_parts = []
    send_to_gemini = True
    prompt_for_gemini = None 
    is_special_flow = False # Flag para indicar se um fluxo especial foi tratado

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

        # PRIORIDADE 1: Usuário está respondendo a uma oferta de guia onde múltiplas opções podem ter sido dadas
        if session_manager.is_pending_guidance_breathing_offer(flask_session_id) or \
           session_manager.is_pending_guidance_sounds_offer(flask_session_id) or \
           session_manager.is_pending_guidance_bodyscan_offer(flask_session_id):
            
            is_special_flow = True 
            user_choice_input = user_input_text.strip()
            
            # Verifica se era uma oferta múltipla (pelo menos duas flags de guia estavam ativas ANTES desta interação)
            # Para isso, precisaríamos do estado ANTERIOR das flags, ou assumir que se QUALQUER uma está ativa, é uma resposta a ela.
            # A lógica abaixo tenta discernir a escolha.
            
            print(f"DEBUG (flow_handler): OFERTA DE GUIA PENDENTE. Input: '{user_choice_input}'")

            processed_choice_for_guide = False
            # Limpa TODAS as flags de oferta pendente de guia, pois o usuário está respondendo.
            # Se a resposta não for uma escolha válida, o bot pedirá para escolher novamente e setará as flags de novo.
            guidance_breathing_was_pending = session_manager.is_pending_guidance_breathing_offer(flask_session_id)
            guidance_sounds_was_pending = session_manager.is_pending_guidance_sounds_offer(flask_session_id)
            guidance_bodyscan_was_pending = session_manager.is_pending_guidance_bodyscan_offer(flask_session_id)

            session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
            session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
            session_manager.clear_pending_guidance_bodyscan_offer(flask_session_id)
            session_manager.clear_three_good_things_suggested(flask_session_id) # Limpa 3GT também

            if user_choice_input == "1" or any(kw in user_input_lower for kw in BREATHING_EXERCISE_KEYWORDS):
                prompt_for_gemini = prompts.get_breathing_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU/CONFIRMOU Respiração.")
                processed_choice_for_guide = True
            elif user_choice_input == "2" or any(kw in user_input_lower for kw in SOUNDS_EXERCISE_KEYWORDS):
                prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU/CONFIRMOU Atenção aos Sons.")
                processed_choice_for_guide = True
            elif user_choice_input == "3" or any(kw in user_input_lower for kw in BODYSCAN_EXERCISE_KEYWORDS):
                prompt_for_gemini = prompts.get_body_scan_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU/CONFIRMOU Escaneamento Corporal.")
                processed_choice_for_guide = True
            
            if not processed_choice_for_guide: 
                # Se não foi uma escolha clara de exercício (1,2,3 ou keyword específica),
                # mas o usuário disse algo afirmativo e múltiplas ofertas estavam ativas.
                num_pending_offers_before_clear = sum([
                    guidance_breathing_was_pending,
                    guidance_sounds_was_pending,
                    guidance_bodyscan_was_pending
                ])

                if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) and num_pending_offers_before_clear > 1:
                    final_bot_response_parts = ["Ótimo! Qual deles você gostaria de tentar: 1. Respiração, 2. Sons, ou 3. Escaneamento Corporal? (Digite o número)"]
                    send_to_gemini = False
                    # Recoloca as flags que estavam ativas para permitir nova tentativa de escolha
                    if guidance_breathing_was_pending: session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
                    if guidance_sounds_was_pending: session_manager.set_pending_guidance_sounds_offer(flask_session_id)
                    if guidance_bodyscan_was_pending: session_manager.set_pending_guidance_bodyscan_offer(flask_session_id)
                    print(f"DEBUG (flow_handler): Guia - Usuário disse 'sim' genericamente a multi-oferta. Perguntando qual.")
                else: # Recusa ou entrada não reconhecida (mesmo para oferta única)
                    final_bot_response_parts = ["Entendido. Se mudar de ideia sobre os exercícios, é só me dizer."]
                    send_to_gemini = False
                    print(f"DEBUG (flow_handler): Guia - Usuário não escolheu exercício claramente ou recusou.")
        
        # PRIORIDADE 2: Usuário está listando Três Coisas Boas
        # (Verifica DEPOIS de responder a ofertas de guia, pois a lista de 3GT pode ser uma resposta a uma sugestão)
        elif session_manager.was_three_good_things_suggested(flask_session_id):
            is_special_flow = True
            session_manager.clear_three_good_things_suggested(flask_session_id)
            prompt_for_gemini = prompts.get_acknowledge_three_good_things_prompt(user_input_text)
            print(f"DEBUG (flow_handler): Três Coisas Boas - Usuário supostamente listou.")
        
        # PRIORIDADE 3: Resposta a uma pergunta de check-in (escala ou palavra)
        elif session_manager.has_asked_checkin_scale(flask_session_id):
            is_special_flow = True
            session_manager.clear_asked_checkin_scale(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text)
            # O LLM será instruído a oferecer opções (respiração/sons/bodyscan) ou 3GT.
            # Setamos todas as flags relevantes de "oferta pendente"
            session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_pending_guidance_bodyscan_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id) # Se o LLM sugerir 3GT diretamente
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. Todas flags de sugestão pendente SET.")

        elif session_manager.has_asked_checkin_word(flask_session_id):
            is_special_flow = True
            session_manager.clear_asked_checkin_word(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text)
            session_manager.set_pending_guidance_breathing_offer(flask_session_id)
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_pending_guidance_bodyscan_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id)
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. Todas flags de sugestão pendente SET.")
            
        # PRIORIDADE 4: Usuário inicia um novo check-in
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            # Log para verificação ANTES da condição interna
            print(f"DEBUG (flow_handler): 'check-in' keyword detectada. Verificando flags de bloqueio...")
            # ... (logs de cada flag como antes) ...

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
                    print(f"DEBUG (flow_handler): Intenção. Perguntando ESCALA. Resposta definida: {final_bot_response_parts}")
                else:
                    final_bot_response_parts = ["Ok, vamos lá com o check-in!", "Qual palavra descreve sua energia ou sentimento predominante hoje?"]
                    session_manager.set_asked_checkin_word(flask_session_id)
                    print(f"DEBUG (flow_handler): Intenção. Perguntando PALAVRA. Resposta definida: {final_bot_response_parts}")
            else:
                print(f"DEBUG (flow_handler): Intenção de check-in, mas uma flag de estado está ativa. Deixando para fluxo normal/LLM.")

    # 3. Fluxo Normal (se nenhum fluxo especial foi ativado)
    if not is_special_flow:
        print("DEBUG (flow_handler): Entrando no Fluxo Normal.")
        prompt_for_gemini = user_input_text
        current_sdk_msg_count = session_manager.get_sdk_message_count(flask_session_id)
        if current_sdk_msg_count == 0 and not ("1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL):
            prompt_for_gemini = prompts.get_initial_disclaimer_prompt(user_input_text)
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

            if hasattr(response_obj_from_sdk, 'text') and response_obj_from_sdk.text is not None:
                raw_extracted_texts_debug.append(f"Direct .text: '{response_obj_from_sdk.text}'")
                if response_obj_from_sdk.text.strip(): # Adiciona apenas se não for só espaços
                    extracted_texts.append(response_obj_from_sdk.text)
            
            if hasattr(response_obj_from_sdk, 'parts') and response_obj_from_sdk.parts:
                for i, part in enumerate(response_obj_from_sdk.parts):
                    part_text = getattr(part, 'text', None)
                    raw_extracted_texts_debug.append(f"Part {i} .text: '{part_text}'")
                    if part_text is not None and part_text.strip(): 
                        extracted_texts.append(part_text)
            
            if hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                 candidate = response_obj_from_sdk.candidates[0]
                 if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for i, part_comp in enumerate(candidate.content.parts):
                        part_text = getattr(part_comp, 'text', None)
                        raw_extracted_texts_debug.append(f"Candidate Part {i} .text: '{part_text}'")
                        if part_text is not None and part_text.strip(): 
                            extracted_texts.append(part_comp.text)
            
            print(f"DEBUG (flow_handler): Textos extraídos BRUTOS (com conteúdo): {raw_extracted_texts_debug}")
            
            # Se extracted_texts ainda estiver vazio, mas raw_extracted_texts_debug não, pode ser que só havia espaços
            if not extracted_texts and any(s is not None for s in raw_extracted_texts_debug): # Verifica se algum texto foi extraído antes do strip
                 print(f"WARN (flow_handler): Textos extraídos eram apenas espaços ou None. raw_extracted: {raw_extracted_texts_debug}")


            # Desduplicação/Seleção (APENAS se houver textos após o strip inicial)
            if not extracted_texts: # Se extracted_texts ficou vazio após os strips individuais
                final_bot_response_parts = []
            elif len(extracted_texts) == 1:
                final_bot_response_parts = extracted_texts
            else: 
                first_part_for_check = extracted_texts[0]
                # Checagem mais simples para desduplicação: se todas as partes são iguais à primeira.
                if all(first_part_for_check == p for p in extracted_texts):
                    print(f"WARN (flow_handler): Múltiplas partes idênticas ({len(extracted_texts)}) detectadas após processamento. Usando apenas a primeira. Ex: '{first_part_for_check[:70]}...'")
                    final_bot_response_parts = [first_part_for_check]
                else:
                    # Se as partes são diferentes, junta todas (o LLM pode ter formatado a resposta em múltiplas partes intencionalmente)
                    print(f"INFO (flow_handler): Múltiplas partes diferentes detectadas ({len(extracted_texts)}). Usando todas. Ex primeira: '{extracted_texts[0][:70]}...'")
                    final_bot_response_parts = extracted_texts 
            
            print(f"DEBUG (flow_handler): final_bot_response_parts APÓS desduplicação/seleção: {final_bot_response_parts}")
            
            if not final_bot_response_parts: # Se ainda estiver vazio
                finish_reason = "UNKNOWN"; safety_ratings_str = "N/A"
                # ... (lógica de finish_reason e safety_ratings como antes) ...
                print(f"WARN (flow_handler): Gemini respondeu sem texto útil final. Finish Reason: {finish_reason}. Safety: {safety_ratings_str}")
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
        flags_cleared_log = []
        if session_manager.was_three_good_things_suggested(flask_session_id): session_manager.clear_three_good_things_suggested(flask_session_id); flags_cleared_log.append("3GT_sug")
        if session_manager.is_pending_guidance_breathing_offer(flask_session_id): session_manager.clear_pending_guidance_breathing_offer(flask_session_id); flags_cleared_log.append("pend_B")
        if session_manager.is_pending_guidance_sounds_offer(flask_session_id): session_manager.clear_pending_guidance_sounds_offer(flask_session_id); flags_cleared_log.append("pend_S")
        if session_manager.is_pending_guidance_bodyscan_offer(flask_session_id): session_manager.clear_pending_guidance_bodyscan_offer(flask_session_id); flags_cleared_log.append("pend_Body")
        if session_manager.has_asked_checkin_scale(flask_session_id): session_manager.clear_asked_checkin_scale(flask_session_id); flags_cleared_log.append("ask_S_norm")
        if session_manager.has_asked_checkin_word(flask_session_id): session_manager.clear_asked_checkin_word(flask_session_id); flags_cleared_log.append("ask_W_norm")
        if flags_cleared_log: print(f"DEBUG (flow_handler): Flags limpas (fluxo normal): {', '.join(flags_cleared_log)}")

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini