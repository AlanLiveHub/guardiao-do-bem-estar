# chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import (
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL
)
import random
import traceback

def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    user_input_lower = user_input_text.lower()
    final_bot_response_parts = []
    send_to_gemini = True
    prompt_for_gemini = None 
    is_special_flow = False

    # 1. Lógica de Risco
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

    # 2. Lógica de Fluxos Especiais
    if not is_special_flow:
        print(f"DEBUG (flow_handler): Verificando fluxos. Flags: 3GT_SUGGESTED={session_manager.was_three_good_things_suggested()}, PENDING_GUIDANCE={session_manager.is_pending_guidance_offer()}, SCALE_ASKED={session_manager.has_asked_checkin_scale()}, WORD_ASKED={session_manager.has_asked_checkin_word()}")

        if session_manager.was_three_good_things_suggested():
            session_manager.clear_three_good_things_suggested()
            prompt_for_gemini = prompts.get_acknowledge_three_good_things_prompt(user_input_text)
            print(f"DEBUG (flow_handler): Três Coisas Boas - Usuário listou. Prompt de reconhecimento.")
            is_special_flow = True
        
        elif session_manager.is_pending_guidance_offer():
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS):
                session_manager.clear_pending_guidance_offer()
                prompt_for_gemini = prompts.get_breathing_guidance_prompt() 
                print(f"DEBUG (flow_handler): Guia - Usuário confirmou. Iniciando guia.")
            else:
                session_manager.clear_pending_guidance_offer()
                final_bot_response_parts = ["Entendido. Se mudar de ideia ou precisar de algo mais, é só dizer."]
                send_to_gemini = False
            is_special_flow = True

        elif session_manager.has_asked_checkin_scale():
            session_manager.clear_asked_checkin_scale()
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text)
            session_manager.set_pending_guidance_offer()
            session_manager.set_three_good_things_suggested()
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. Flags pending_guidance e 3_coisas_boas SET.")
            is_special_flow = True

        elif session_manager.has_asked_checkin_word():
            session_manager.clear_asked_checkin_word()
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text)
            session_manager.set_pending_guidance_offer()
            session_manager.set_three_good_things_suggested()
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. Flags pending_guidance e 3_coisas_boas SET.")
            is_special_flow = True
            
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            # Condição para iniciar novo check-in
            if not session_manager.has_asked_checkin_scale() and \
               not session_manager.has_asked_checkin_word() and \
               not session_manager.is_pending_guidance_offer() and \
               not session_manager.was_three_good_things_suggested():
                
                print(f"DEBUG (flow_handler): CASO E (Novo Check-in) ATIVADO.")
                is_special_flow = True
                send_to_gemini = False 

                if random.choice([True, False]):
                    final_bot_response_parts = [
                        "Claro! Vamos fazer um rápido check-in.",
                        "Numa escala de 1 a 5 (1=muito mal, 5=muito bem), como você está se sentindo agora?"
                    ]
                    session_manager.set_asked_checkin_scale()
                    print(f"DEBUG (flow_handler): Check-in - Intenção. Perguntando ESCALA (Aleatório). final_bot_response_parts: {final_bot_response_parts}")
                else:
                    final_bot_response_parts = [
                        "Ok, vamos lá com o check-in!",
                        "Qual palavra descreve sua energia ou sentimento predominante hoje?"
                    ]
                    session_manager.set_asked_checkin_word()
                    print(f"DEBUG (flow_handler): Check-in - Intenção. Perguntando PALAVRA (Aleatório). final_bot_response_parts: {final_bot_response_parts}")
            else:
                print(f"DEBUG (flow_handler): Intenção de check-in, mas uma flag de estado está ativa. Deixando para fluxo normal.")


    # 3. Fluxo Normal
    if not is_special_flow: # Se NENHUM fluxo especial (incluindo risco) foi tratado
        prompt_for_gemini = user_input_text
        current_sdk_msg_count = session_manager.get_sdk_message_count(flask_session_id)
        if current_sdk_msg_count == 0 and not ("1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL):
            prompt_for_gemini = prompts.get_initial_disclaimer_prompt(user_input_text)
            print("DEBUG (flow_handler): Usando prompt com disclaimer inicial (não-1.5).")
    
    # 4. Enviar para Gemini se send_to_gemini é True E um prompt foi preparado
    if send_to_gemini and prompt_for_gemini:
        try:
            print(f"----- (flow_handler) Enviando para Gemini (ID: {flask_session_id}) -----")
            print(f"Texto para API: '{prompt_for_gemini}'")
            response_obj_from_sdk = sdk_chat_obj.send_message(prompt_for_gemini, stream=False)
            
            extracted_texts = []
            # Adapte esta extração para ser robusta com a estrutura de resposta do seu modelo
            if hasattr(response_obj_from_sdk, 'text') and response_obj_from_sdk.text:
                extracted_texts.append(response_obj_from_sdk.text)
            elif hasattr(response_obj_from_sdk, 'parts') and response_obj_from_sdk.parts:
                for part in response_obj_from_sdk.parts:
                    if hasattr(part, 'text') and part.text:
                        extracted_texts.append(part.text)
            elif hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                 candidate = response_obj_from_sdk.candidates[0]
                 if candidate.content and candidate.content.parts:
                    for part in candidate.content.parts:
                        if hasattr(part, 'text') and part.text:
                            extracted_texts.append(part.text)
            
            final_bot_response_parts = [text for text in extracted_texts if text and text.strip()]
            if not final_bot_response_parts:
                final_bot_response_parts = ["Sinto muito, não consegui gerar uma resposta clara agora."]
                print("WARN (flow_handler): Gemini respondeu, mas sem texto útil.")

        except Exception as e:
            print(f"EXCEÇÃO API Gemini (flow_handler): {type(e).__name__}: {e}\n{traceback.format_exc()}")
            final_bot_response_parts = ["Algo deu errado ao tentar falar com o assistente. Tente novamente mais tarde."]
            send_to_gemini = False
    
    # Fallback final se nenhuma resposta foi definida (deveria ser raro)
    elif not final_bot_response_parts and not send_to_gemini:
        # Isso pode acontecer se send_to_gemini foi setado para False em um fluxo
        # mas final_bot_response_parts não foi preenchido.
        final_bot_response_parts = ["Hmm, parece que me perdi um pouco. Pode tentar de novo?"]
        print("ERRO (flow_handler): send_to_gemini é False, mas nenhuma resposta foi definida explicitamente.")
    
    # Limpeza de flags se o usuário mudou de assunto
    if not is_special_flow and send_to_gemini: 
        flags_were_cleared = False
        if session_manager.was_three_good_things_suggested():
            print("DEBUG (flow_handler): Fluxo normal, limpando flag 3GT.")
            session_manager.clear_three_good_things_suggested(); flags_were_cleared = True
        if session_manager.is_pending_guidance_offer():
            print("DEBUG (flow_handler): Fluxo normal, limpando flag pending_guidance.")
            session_manager.clear_pending_guidance_offer(); flags_were_cleared = True
        if session_manager.has_asked_checkin_scale() :
            print("DEBUG (flow_handler): Fluxo normal, limpando flag asked_scale.")
            session_manager.clear_asked_checkin_scale(); flags_were_cleared = True
        if session_manager.has_asked_checkin_word():
            print("DEBUG (flow_handler): Fluxo normal, limpando flag asked_word.")
            session_manager.clear_asked_checkin_word(); flags_were_cleared = True
        if flags_were_cleared:
            print("DEBUG (flow_handler): Algumas flags de estado foram limpas.")

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini