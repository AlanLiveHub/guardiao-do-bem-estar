# meu_guardiao_do_bem_estar/chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import (
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL # Importe o que for necessário
)
import random
import traceback # Para logar exceções da API Gemini

def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    """
    Processa a mensagem do usuário, decide o fluxo e retorna a resposta do bot.
    Retorna: (list_of_response_parts, did_send_to_gemini_flag, prepared_prompt_for_gemini)
    O último item (prepared_prompt_for_gemini) é mais para debug/log.
    """
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
            potentially_risky_word_found = True
            break
    if potentially_risky_word_found:
        for f_keyword in FICTION_CONTEXT_KEYWORDS:
            if f_keyword in user_input_lower:
                fiction_context_found = True
                break
        if not fiction_context_found:
            final_bot_response_parts = CVV_MESSAGE_TEXT_PARTS
            send_to_gemini = False
            print(f"AVISO (flow_handler): Risco detectado. Encaminhando para CVV.")
            is_special_flow = True # Considera isso um fluxo especial que não vai pro Gemini

    # 2. Lógica de Fluxos Especiais (Check-in, Guias) - Só executa se não houver risco
    if not is_special_flow: # Equivalente ao seu 'if send_to_gemini_flag:' anterior
        if session_manager.is_pending_guidance_offer():
            if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS):
                session_manager.clear_pending_guidance_offer()
                prompt_for_gemini = prompts.get_breathing_guidance_prompt()
                print(f"DEBUG (flow_handler): Guia - Usuário confirmou respiração.")
            else:
                session_manager.clear_pending_guidance_offer()
                final_bot_response_parts = ["Entendido. Se mudar de ideia ou precisar de algo mais, é só dizer."]
                send_to_gemini = False
            is_special_flow = True

        elif session_manager.has_asked_checkin_scale():
            session_manager.clear_asked_checkin_scale()
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text)
            session_manager.set_pending_guidance_offer()
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. Flag pending_guidance SET.")
            is_special_flow = True

        elif session_manager.has_asked_checkin_word():
            session_manager.clear_asked_checkin_word()
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text)
            session_manager.set_pending_guidance_offer()
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. Flag pending_guidance SET.")
            is_special_flow = True
            
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            if random.choice([True, False]):
                final_bot_response_parts = [
                    "Claro! Vamos fazer um rápido check-in.",
                    "Numa escala de 1 a 5 (1=muito mal, 5=muito bem), como você está se sentindo agora?"
                ]
                session_manager.set_asked_checkin_scale()
                print(f"DEBUG (flow_handler): Check-in - Intenção. Perguntando ESCALA (Aleatório).")
            else:
                final_bot_response_parts = [
                    "Ok, vamos lá com o check-in!",
                    "Qual palavra descreve sua energia ou sentimento predominante hoje?"
                ]
                session_manager.set_asked_checkin_word()
                print(f"DEBUG (flow_handler): Check-in - Intenção. Perguntando PALAVRA (Aleatório).")
            send_to_gemini = False
            is_special_flow = True

    # 3. Fluxo Normal (se nenhum fluxo especial foi ativado e não houve risco)
    if not is_special_flow:
        prompt_for_gemini = user_input_text
        # Lógica para adicionar disclaimer na primeira mensagem (se necessário)
        current_sdk_msg_count = session_manager.get_sdk_message_count(flask_session_id)
        if current_sdk_msg_count == 0 and not ("1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL):
            prompt_for_gemini = prompts.get_initial_disclaimer_prompt(user_input_text)
            print("DEBUG (flow_handler): Usando prompt com disclaimer inicial (não-1.5).")
    
    # 4. Enviar para Gemini se necessário
    if send_to_gemini and prompt_for_gemini:
        try:
            print(f"----- (flow_handler) Enviando para Gemini (ID: {flask_session_id}) -----")
            print(f"Texto para API: '{prompt_for_gemini}'")
            response_obj_from_sdk = sdk_chat_obj.send_message(prompt_for_gemini, stream=False)
            
            extracted_texts = []
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
            
            final_bot_response_parts = [text for text in extracted_texts if text.strip()]
            if not final_bot_response_parts:
                final_bot_response_parts = ["Sinto muito, não consegui gerar uma resposta clara agora."]
                print("WARN (flow_handler): Gemini respondeu, mas sem texto útil.")

        except Exception as e:
            print(f"EXCEÇÃO API Gemini (flow_handler): {type(e).__name__}: {e}\n{traceback.format_exc()}")
            final_bot_response_parts = ["Algo deu errado ao tentar falar com o assistente. Tente novamente mais tarde."]
            send_to_gemini = False # Indica que a comunicação falhou
    
    elif not send_to_gemini and not final_bot_response_parts:
        # Fallback se send_to_gemini era False mas final_bot_response_parts não foi preenchido (erro de lógica)
        final_bot_response_parts = ["Hmm, algo não saiu como esperado internamente."]
        print("ERRO (flow_handler): send_to_gemini é False, mas nenhuma resposta foi definida.")

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini