# chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import ( 
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL,
    BREATHING_EXERCISE_KEYWORDS, SOUNDS_EXERCISE_KEYWORDS
)
import random
import traceback

def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    user_input_lower = user_input_text.lower()
    final_bot_response_parts = []
    send_to_gemini = True
    prompt_for_gemini = None 
    is_special_flow = False

    # 1. Lógica de Risco (COMO ANTES)
    # ... (seu código de risco aqui, se risco, define final_bot_response_parts, send_to_gemini=False, is_special_flow=True)

    # 2. Lógica de Fluxos Especiais (Ordem de Prioridade Ajustada)
    if not is_special_flow:
        # ... (TODA A LÓGICA DOS CASOS A, B3, B1, B2, C, D, E COMO NA ÚLTIMA RESPOSTA COMPLETA QUE TE DEI) ...
        # Certifique-se de que as chamadas ao session_manager usam (flask_session_id)
        # Exemplo do início dos fluxos:
        print(f"DEBUG (flow_handler): Verificando fluxos. Flags: 3GT_SUGGESTED={session_manager.was_three_good_things_suggested(flask_session_id)}, PENDING_BREATHING={session_manager.is_pending_guidance_breathing_offer(flask_session_id)}, PENDING_SOUNDS={session_manager.is_pending_guidance_sounds_offer(flask_session_id)}, SCALE_ASKED={session_manager.has_asked_checkin_scale(flask_session_id)}, WORD_ASKED={session_manager.has_asked_checkin_word(flask_session_id)}")

        if session_manager.was_three_good_things_suggested(flask_session_id) and \
           not session_manager.is_pending_guidance_breathing_offer(flask_session_id) and \
           not session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            session_manager.clear_three_good_things_suggested(flask_session_id)
            prompt_for_gemini = prompts.get_acknowledge_three_good_things_prompt(user_input_text)
            is_special_flow = True; print(f"DEBUG (flow_handler): Três Coisas Boas - Usuário listou.")
        
        elif session_manager.is_pending_guidance_breathing_offer(flask_session_id) and \
             session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            is_special_flow = True
            print(f"DEBUG (flow_handler): CASO B3 - Ambas ofertas (B/S) pendentes. Analisando: '{user_input_lower}'")
            chose_breathing = any(kw in user_input_lower for kw in BREATHING_EXERCISE_KEYWORDS)
            chose_sounds = any(kw in user_input_lower for kw in SOUNDS_EXERCISE_KEYWORDS)
            session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
            session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
            session_manager.clear_three_good_things_suggested(flask_session_id)
            if chose_breathing and not chose_sounds:
                prompt_for_gemini = prompts.get_breathing_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU respiração.")
            elif chose_sounds and not chose_breathing:
                prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário ESCOLHEU atenção aos sons.")
            elif any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS): 
                final_bot_response_parts = ["Ótimo! Qual deles você gostaria de tentar: o de respiração ou o de atenção aos sons? (Por favor, diga 'respiração' ou 'sons')"]
                send_to_gemini = False
                session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
                session_manager.set_pending_guidance_sounds_offer(flask_session_id)
                print(f"DEBUG (flow_handler): Guia - Usuário disse 'sim' genericamente. Perguntando qual.")
            else: 
                final_bot_response_parts = ["Entendido. Se quiser tentar um dos exercícios mais tarde, é só me dizer."]
                send_to_gemini = False
                print(f"DEBUG (flow_handler): Guia - Usuário não escolheu ou recusou após oferta múltipla.")
        
        elif session_manager.is_pending_guidance_breathing_offer(flask_session_id):
            is_special_flow = True; session_manager.clear_three_good_things_suggested(flask_session_id) 
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in BREATHING_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
                prompt_for_gemini = prompts.get_breathing_guidance_prompt() 
                print(f"DEBUG (flow_handler): Guia - Usuário confirmou GUIA DE RESPIRAÇÃO (oferta única).")
            else: 
                session_manager.clear_pending_guidance_breathing_offer(flask_session_id)
                final_bot_response_parts = ["Entendido. Se mudar de ideia sobre o exercício de respiração, é só dizer."]
                send_to_gemini = False
            
        elif session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            is_special_flow = True; session_manager.clear_three_good_things_suggested(flask_session_id)
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) or any(kw in user_input_lower for kw in SOUNDS_EXERCISE_KEYWORDS):
                session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
                prompt_for_gemini = prompts.get_sound_awareness_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário confirmou GUIA DE ATENÇÃO AOS SONS (oferta única).")
            else:
                session_manager.clear_pending_guidance_sounds_offer(flask_session_id)
                final_bot_response_parts = ["Tudo bem. Se quiser tentar o de atenção aos sons em outro momento, me avise."]
                send_to_gemini = False

        elif session_manager.has_asked_checkin_scale(flask_session_id):
            is_special_flow = True; session_manager.clear_asked_checkin_scale(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text)
            session_manager.set_pending_guidance_breathing_offer(flask_session_id) 
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id)
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. Flags (B/S/3GT) SET.")

        elif session_manager.has_asked_checkin_word(flask_session_id):
            is_special_flow = True; session_manager.clear_asked_checkin_word(flask_session_id)
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text)
            session_manager.set_pending_guidance_breathing_offer(flask_session_id)
            session_manager.set_pending_guidance_sounds_offer(flask_session_id)
            session_manager.set_three_good_things_suggested(flask_session_id)
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. Flags (B/S/3GT) SET.")
            
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            if not (session_manager.has_asked_checkin_scale(flask_session_id) or \
                    session_manager.has_asked_checkin_word(flask_session_id) or \
                    session_manager.is_pending_guidance_breathing_offer(flask_session_id) or \
                    session_manager.is_pending_guidance_sounds_offer(flask_session_id) or \
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
                print(f"DEBUG (flow_handler): Intenção de check-in, mas flag de estado ativa. Fluxo normal.")


    # 3. Fluxo Normal
    if not is_special_flow:
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
            print(f"DEBUG (flow_handler): Resposta BRUTA do Gemini: {response_obj_from_sdk}")
            
            extracted_texts = []
            raw_extracted_texts_debug = [] # Para log

            if hasattr(response_obj_from_sdk, 'text') and response_obj_from_sdk.text is not None:
                raw_extracted_texts_debug.append(f"Direct .text: '{response_obj_from_sdk.text}'")
                extracted_texts.append(response_obj_from_sdk.text)
            elif hasattr(response_obj_from_sdk, 'parts') and response_obj_from_sdk.parts:
                for i, part in enumerate(response_obj_from_sdk.parts):
                    if hasattr(part, 'text') and part.text is not None:
                        raw_extracted_texts_debug.append(f"Part {i} .text: '{part.text}'")
                        extracted_texts.append(part.text)
                    else:
                         raw_extracted_texts_debug.append(f"Part {i} .text: None ou Vazio")
            elif hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                 candidate = response_obj_from_sdk.candidates[0]
                 if candidate.content and candidate.content.parts:
                    for i, part_comp in enumerate(candidate.content.parts):
                        if hasattr(part_comp, 'text') and part_comp.text is not None:
                            raw_extracted_texts_debug.append(f"Candidate Part {i} .text: '{part_comp.text}'")
                            extracted_texts.append(part_comp.text)
                        else:
                            raw_extracted_texts_debug.append(f"Candidate Part {i} .text: None ou Vazio")
            
            print(f"DEBUG (flow_handler): Textos extraídos BRUTOS: {raw_extracted_texts_debug}")
            final_bot_response_parts = [text for text in extracted_texts if text and text.strip()]
            
            if not final_bot_response_parts:
                finish_reason = "UNKNOWN"
                safety_ratings_str = "N/A"
                if hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                    candidate = response_obj_from_sdk.candidates[0]
                    finish_reason_obj = getattr(candidate, 'finish_reason', None)
                    if finish_reason_obj is not None: finish_reason = str(finish_reason_obj)
                    # Log safety ratings
                    if hasattr(candidate, 'safety_ratings'):
                        safety_ratings_str = str([f"{rating.category}: {rating.probability}" for rating in candidate.safety_ratings])


                print(f"WARN (flow_handler): Gemini respondeu sem texto útil. Finish Reason: {finish_reason}. Safety Ratings: {safety_ratings_str}")
                if "SAFETY" in finish_reason.upper():
                    final_bot_response_parts = ["Minha política de segurança me impede de responder a isso. Podemos falar sobre outra coisa?"]
                else:
                    final_bot_response_parts = ["Sinto muito, não consegui gerar uma resposta clara desta vez."]
        except Exception as e:
            print(f"EXCEÇÃO API Gemini (flow_handler): {type(e).__name__}: {e}\n{traceback.format_exc()}")
            final_bot_response_parts = ["Algo deu errado com o assistente. Tente mais tarde."]
            send_to_gemini = False 
    
    elif not final_bot_response_parts and not send_to_gemini and is_special_flow:
        final_bot_response_parts = ["Algo deu errado internamente. Poderia tentar novamente?"]
        print(f"ERRO LÓGICO (flow_handler): Fluxo especial, mas sem resposta definida. User input: '{user_input_text}'")

    # Limpeza de flags
    if not is_special_flow and send_to_gemini: 
        flags_cleared_log = []
        if session_manager.was_three_good_things_suggested(flask_session_id):
            session_manager.clear_three_good_things_suggested(flask_session_id); flags_cleared_log.append("3GT_sug")
        if session_manager.is_pending_guidance_breathing_offer(flask_session_id):
            session_manager.clear_pending_guidance_breathing_offer(flask_session_id); flags_cleared_log.append("pend_breath")
        if session_manager.is_pending_guidance_sounds_offer(flask_session_id):
            session_manager.clear_pending_guidance_sounds_offer(flask_session_id); flags_cleared_log.append("pend_sound")
        if session_manager.has_asked_checkin_scale(flask_session_id) :
            session_manager.clear_asked_checkin_scale(flask_session_id); flags_cleared_log.append("ask_scale")
        if session_manager.has_asked_checkin_word(flask_session_id):
            session_manager.clear_asked_checkin_word(flask_session_id); flags_cleared_log.append("ask_word")
        if flags_cleared_log:
            print(f"DEBUG (flow_handler): Flags de estado limpas (fluxo normal): {', '.join(flags_cleared_log)}")

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini