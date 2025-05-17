# chatbot_logic/flow_handler.py
from chatbot_logic import prompts, session_manager
from config import ( 
    RISKY_KEYWORDS, FICTION_CONTEXT_KEYWORDS, CVV_MESSAGE_TEXT_PARTS,
    CHECKIN_KEYWORDS, AFFIRMATIVE_KEYWORDS, MODEL_NAME, SYSTEM_INSTRUCTION_FOR_MODEL,
    BREATHING_EXERCISE_KEYWORDS, SOUNDS_EXERCISE_KEYWORDS, BODYSCAN_EXERCISE_KEYWORDS,
    COMPLETED_ACTION_KEYWORDS,
    POINTS_CHECKIN_COMPLETED, POINTS_THREE_GOOD_THINGS_COMPLETED, POINTS_GUIDED_EXERCISE_ACCEPTED,
    POINTS_MICRO_HABIT_REPORTED
)
import random
import traceback
import json # Para carregar os scripts JSON
import os   # Para construir caminhos de arquivo

# Define o caminho base para os scripts RAG
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # Diretório atual (chatbot_logic)
RAG_SCRIPT_DIR = os.path.join(BASE_DIR, "rag_scripts")

def load_rag_script(exercise_key):
    """Carrega um script de exercício do arquivo JSON."""
    filename = os.path.join(RAG_SCRIPT_DIR, f"{exercise_key}_exercise.json")
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            script_data = json.load(f)
            print(f"INFO (flow_handler): Script RAG '{filename}' carregado com sucesso.")
            return script_data
    except FileNotFoundError:
        print(f"ERRO (flow_handler): Script RAG não encontrado: {filename}")
    except json.JSONDecodeError:
        print(f"ERRO (flow_handler): Erro ao decodificar JSON do script RAG: {filename}")
    except Exception as e:
        print(f"ERRO (flow_handler): Erro inesperado ao carregar script RAG '{filename}': {e}")
    return None


def handle_user_message(user_input_text, sdk_chat_obj, flask_session_id):
    user_input_lower = user_input_text.lower()
    final_bot_response_parts = []
    send_to_gemini = True
    prompt_for_gemini = None 
    is_special_flow = False 

    # 1. Lógica de Risco (Prioridade Máxima)
    potentially_risky_word_found = False; fiction_context_found = False
    for r_keyword in RISKY_KEYWORDS:
        if r_keyword in user_input_lower: potentially_risky_word_found = True; break
    if potentially_risky_word_found:
        for f_keyword in FICTION_CONTEXT_KEYWORDS:
            if f_keyword in user_input_lower: fiction_context_found = True; break
        if not fiction_context_found:
            final_bot_response_parts = CVV_MESSAGE_TEXT_PARTS
            send_to_gemini = False; is_special_flow = True 
            print(f"AVISO (flow_handler): Risco detectado. Encaminhando para CVV.")

    # 2. Lógica de Fluxos Especiais
    if not is_special_flow:
        # Captura o estado das flags no início
        guidance_breathing_was_pending = session_manager.is_pending_guidance_breathing_offer()
        guidance_sounds_was_pending = session_manager.is_pending_guidance_sounds_offer()
        guidance_bodyscan_was_pending = session_manager.is_pending_guidance_bodyscan_offer()
        three_good_things_was_suggested = session_manager.was_three_good_things_suggested()
        asked_scale_was_pending = session_manager.has_asked_checkin_scale()
        asked_word_was_pending = session_manager.has_asked_checkin_word()
        
        current_flags_log = (
            f"3GT_SUG={three_good_things_was_suggested}, PEND_B={guidance_breathing_was_pending}, "
            f"PEND_S={guidance_sounds_was_pending}, PEND_BODY={guidance_bodyscan_was_pending}, "
            f"ASK_SCALE={asked_scale_was_pending}, ASK_WORD={asked_word_was_pending}"
        )
        print(f"DEBUG (flow_handler): Verificando fluxos. Flags: {current_flags_log}")

        num_pending_guidance_offers = sum([guidance_breathing_was_pending, guidance_sounds_was_pending, guidance_bodyscan_was_pending])

        # PRIORIDADE 1: Usuário está respondendo a uma oferta de guia
        if num_pending_guidance_offers > 0:
            is_special_flow = True 
            user_choice_input = user_input_text.strip()
            print(f"DEBUG (flow_handler): OFERTA DE GUIA(S) PENDENTE. Input: '{user_choice_input}'. Num offers: {num_pending_guidance_offers}")
            
            processed_choice_for_guide = False
            
            session_manager.clear_pending_guidance_breathing_offer()
            session_manager.clear_pending_guidance_sounds_offer()
            session_manager.clear_pending_guidance_bodyscan_offer()
            session_manager.clear_three_good_things_suggested()

            script_to_load_key = None
            exercise_chosen_name_log = "" # Para log

            if user_choice_input == "1" or (guidance_breathing_was_pending and any(kw in user_input_lower for kw in BREATHING_EXERCISE_KEYWORDS)):
                script_to_load_key = "breathing"
                exercise_chosen_name_log = "Respiração"
                processed_choice_for_guide = True
            elif user_choice_input == "2" or (guidance_sounds_was_pending and any(kw in user_input_lower for kw in SOUNDS_EXERCISE_KEYWORDS)):
                script_to_load_key = "sound_awareness"
                exercise_chosen_name_log = "Atenção aos Sons"
                processed_choice_for_guide = True
            elif user_choice_input == "3" or (guidance_bodyscan_was_pending and any(kw in user_input_lower for kw in BODYSCAN_EXERCISE_KEYWORDS)):
                script_to_load_key = "body_scan"
                exercise_chosen_name_log = "Escaneamento Corporal"
                processed_choice_for_guide = True
            
            if processed_choice_for_guide and script_to_load_key:
                exercise_script_data = load_rag_script(script_to_load_key)
                if exercise_script_data:
                    new_total_points = session_manager.add_user_points(POINTS_GUIDED_EXERCISE_ACCEPTED)
                    prompt_for_gemini = prompts.get_rag_guided_exercise_prompt(
                        exercise_script_data, 
                        POINTS_GUIDED_EXERCISE_ACCEPTED, 
                        new_total_points
                    )
                    print(f"DEBUG ... Usuário escolheu Guia RAG: {exercise_chosen_name_log}. +{POINTS_GUIDED_EXERCISE_ACCEPTED}pts, Total:{new_total_points}")
                else: 
                    final_bot_response_parts = [f"Desculpe, tive um problema ao preparar o exercício de {exercise_chosen_name_log}. Que tal tentarmos outra das opções ou algo diferente?"]
                    send_to_gemini = False
                    if guidance_breathing_was_pending: session_manager.set_pending_guidance_breathing_offer()
                    if guidance_sounds_was_pending: session_manager.set_pending_guidance_sounds_offer()
                    if guidance_bodyscan_was_pending: session_manager.set_pending_guidance_bodyscan_offer()
            elif not processed_choice_for_guide: 
                if any(word in user_input_lower for word in AFFIRMATIVE_KEYWORDS) and num_pending_guidance_offers > 0 :
                    if num_pending_guidance_offers >= 1: 
                        final_bot_response_parts = ["Ótimo! Qual deles você gostaria de tentar: 1. Respiração, 2. Sons, ou 3. Escaneamento Corporal? (Por favor, digite o número)"]
                        send_to_gemini = False
                        if guidance_breathing_was_pending: session_manager.set_pending_guidance_breathing_offer() 
                        if guidance_sounds_was_pending: session_manager.set_pending_guidance_sounds_offer()
                        if guidance_bodyscan_was_pending: session_manager.set_pending_guidance_bodyscan_offer()
                        print(f"DEBUG (flow_handler): Guia - Usuário disse 'sim' genericamente a oferta. Perguntando qual.")
                else: 
                    final_bot_response_parts = ["Entendido. Se mudar de ideia sobre os exercícios ou precisar de algo mais, é só me dizer."]
                    send_to_gemini = False
                    print(f"DEBUG (flow_handler): Guia - Usuário não escolheu exercício claramente ou recusou após oferta(s).")
        
        # PRIORIDADE 2: Usuário está listando Três Coisas Boas
        elif three_good_things_was_suggested:
            is_special_flow = True
            session_manager.clear_three_good_things_suggested()
            new_total_points = session_manager.add_user_points(POINTS_THREE_GOOD_THINGS_COMPLETED)
            prompt_for_gemini = prompts.get_acknowledge_three_good_things_prompt(user_input_text, new_total_points)
            print(f"DEBUG (flow_handler): Três Coisas Boas - Usuário supostamente listou. +{POINTS_THREE_GOOD_THINGS_COMPLETED}pts")
        
        # PRIORIDADE 3: Resposta a uma pergunta de check-in
        elif asked_scale_was_pending:
            is_special_flow = True; session_manager.clear_asked_checkin_scale()
            new_total_points = session_manager.add_user_points(POINTS_CHECKIN_COMPLETED)
            prompt_for_gemini = prompts.get_checkin_scale_response_prompt(user_input_text, new_total_points)
            session_manager.set_pending_guidance_breathing_offer() 
            session_manager.set_pending_guidance_sounds_offer()
            session_manager.set_pending_guidance_bodyscan_offer()
            session_manager.set_three_good_things_suggested()
            print(f"DEBUG (flow_handler): Check-in - Resposta à escala. +{POINTS_CHECKIN_COMPLETED}pts. Todas flags de sugestão pendente SET.")
        elif asked_word_was_pending:
            is_special_flow = True; session_manager.clear_asked_checkin_word()
            new_total_points = session_manager.add_user_points(POINTS_CHECKIN_COMPLETED)
            prompt_for_gemini = prompts.get_checkin_word_response_prompt(user_input_text, new_total_points)
            session_manager.set_pending_guidance_breathing_offer()
            session_manager.set_pending_guidance_sounds_offer()
            session_manager.set_pending_guidance_bodyscan_offer()
            session_manager.set_three_good_things_suggested()
            print(f"DEBUG (flow_handler): Check-in - Resposta à palavra. +{POINTS_CHECKIN_COMPLETED}pts. Todas flags de sugestão pendente SET.")
            
        # PRIORIDADE 4: Detecção explícita de conclusão de ação (micro-hábito)
        elif any(keyword in user_input_lower for keyword in COMPLETED_ACTION_KEYWORDS):
            is_not_in_other_active_flow = not (asked_scale_was_pending or asked_word_was_pending or guidance_breathing_was_pending or guidance_sounds_was_pending or guidance_bodyscan_was_pending or three_good_things_was_suggested)
            if is_not_in_other_active_flow:
                print(f"DEBUG (flow_handler): Possível conclusão de ação (micro-hábito): '{user_input_text}'")
                new_total_points = session_manager.add_user_points(POINTS_MICRO_HABIT_REPORTED)
                prompt_for_gemini = prompts.get_celebrate_achievement_prompt(user_input_text, POINTS_MICRO_HABIT_REPORTED, new_total_points)
                is_special_flow = True
                print(f"DEBUG (flow_handler): Micro-hábito reportado. +{POINTS_MICRO_HABIT_REPORTED}pts, Total:{new_total_points}")
            else:
                print(f"DEBUG (flow_handler): Keyword de conclusão detectada, mas outra flag de fluxo está ativa.")
            
        # PRIORIDADE 5: Usuário inicia um novo check-in
        elif any(keyword in user_input_lower for keyword in CHECKIN_KEYWORDS):
            if not (asked_scale_was_pending or asked_word_was_pending or guidance_breathing_was_pending or guidance_sounds_was_pending or guidance_bodyscan_was_pending or three_good_things_was_suggested):
                print(f"DEBUG (flow_handler): CASO E (Novo Check-in) ATIVADO.")
                is_special_flow = True; send_to_gemini = False 
                if random.choice([True, False]):
                    final_bot_response_parts = ["Claro! Vamos fazer um rápido check-in.", "Numa escala de 1 a 5 (1=muito mal, 5=muito bem), como você está se sentindo agora?"]
                    session_manager.set_asked_checkin_scale()
                else:
                    final_bot_response_parts = ["Ok, vamos lá com o check-in!", "Qual palavra descreve sua energia ou sentimento predominante hoje?"]
                    session_manager.set_asked_checkin_word()
                print(f"DEBUG (flow_handler): Intenção de Check-in. Perguntando. Resposta definida: {final_bot_response_parts}")
            else:
                print(f"DEBUG (flow_handler): Intenção de check-in, mas uma flag de estado está ativa. Deixando para fluxo normal/LLM.")

    # 3. Fluxo Normal (se nenhum fluxo especial foi ativado)
    if not is_special_flow:
        print("DEBUG (flow_handler): Entrando no Fluxo Normal.")
        prompt_for_gemini = user_input_text
        current_sdk_msg_count = session_manager.get_sdk_message_count(flask_session_id)
        if current_sdk_msg_count == 0 and not ("1.5" in MODEL_NAME and SYSTEM_INSTRUCTION_FOR_MODEL):
            pass # Confia no SYSTEM_INSTRUCTION para o tom da primeira resposta do LLM
    
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
            if hasattr(response_obj_from_sdk, 'text') and response_obj_from_sdk.text:
                if response_obj_from_sdk.text.strip(): extracted_texts.append(response_obj_from_sdk.text)
            elif hasattr(response_obj_from_sdk, 'parts') and response_obj_from_sdk.parts:
                for part in response_obj_from_sdk.parts:
                    part_text = getattr(part, 'text', None)
                    if part_text is not None and part_text.strip(): extracted_texts.append(part_text)
            elif hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                 candidate = response_obj_from_sdk.candidates[0]
                 if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts') and candidate.content.parts:
                    for part_comp in candidate.content.parts:
                        part_text = getattr(part_comp, 'text', None)
                        if part_text is not None and part_text.strip(): extracted_texts.append(part_comp.text)
            
            if extracted_texts:
                final_bot_response_parts = ["\n".join(extracted_texts)] # Junta em uma única string
                print(f"DEBUG (flow_handler): final_bot_response_parts APÓS join: {final_bot_response_parts}")
            else:
                final_bot_response_parts = []
                print(f"WARN (flow_handler): Nenhum texto útil extraído da resposta do Gemini.")

            if not final_bot_response_parts:
                finish_reason = "UNKNOWN"; safety_ratings_str = "N/A"
                if hasattr(response_obj_from_sdk, 'candidates') and response_obj_from_sdk.candidates:
                    candidate = response_obj_from_sdk.candidates[0]
                    finish_reason_obj = getattr(candidate, 'finish_reason', None)
                    if finish_reason_obj is not None: finish_reason = str(finish_reason_obj.name if hasattr(finish_reason_obj, 'name') else finish_reason_obj)
                    if hasattr(candidate, 'safety_ratings'): safety_ratings_str = str([f"{rating.category.name if hasattr(rating.category, 'name') else rating.category}: {rating.probability.name if hasattr(rating.probability, 'name') else rating.probability}" for rating in candidate.safety_ratings])
                print(f"WARN (flow_handler): Gemini respondeu sem texto útil final. FR: {finish_reason}. Safety: {safety_ratings_str}")
                if "SAFETY" in finish_reason.upper(): final_bot_response_parts = ["Minha política de segurança me impede de responder a isso."]
                else: final_bot_response_parts = ["Sinto muito, não tenho uma resposta para isso agora."]
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
        if session_manager.was_three_good_things_suggested(): session_manager.clear_three_good_things_suggested(); flags_cleared_log.append("3GT_sug")
        if session_manager.is_pending_guidance_breathing_offer(): session_manager.clear_pending_guidance_breathing_offer(); flags_cleared_log.append("pend_B")
        if session_manager.is_pending_guidance_sounds_offer(): session_manager.clear_pending_guidance_sounds_offer(); flags_cleared_log.append("pend_S")
        if session_manager.is_pending_guidance_bodyscan_offer(): session_manager.clear_pending_guidance_bodyscan_offer(); flags_cleared_log.append("pend_Body")
        if session_manager.has_asked_checkin_scale(): session_manager.clear_asked_checkin_scale(); flags_cleared_log.append("ask_S_norm")
        if session_manager.has_asked_checkin_word(): session_manager.clear_asked_checkin_word(); flags_cleared_log.append("ask_W_norm")
        if flags_cleared_log: print(f"DEBUG (flow_handler): Flags limpas (fluxo normal): {', '.join(flags_cleared_log)}")

    return final_bot_response_parts, send_to_gemini, prompt_for_gemini