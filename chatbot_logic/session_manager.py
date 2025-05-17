# meu_guardiao_do_bem_estar/chatbot_logic/session_manager.py
from flask import session
from chatbot_logic import model_instance # Importa a instância do modelo

from config import (
    SESSION_KEY_SDK_HISTORY, SESSION_KEY_SDK_MSG_COUNT,
    SESSION_KEY_ASKED_SCALE, SESSION_KEY_ASKED_WORD, SESSION_KEY_PENDING_GUIDANCE,
    SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS
)
import google.generativeai as genai # Para types.Content e types.Part

# Dicionário em memória para os objetos de chat ativos do SDK
active_sdk_chats = {}

def get_or_create_sdk_chat_data(flask_session_id):
    """Obtém ou cria/recarrega os dados do chat SDK para uma dada flask_session_id."""
    global active_sdk_chats # Para modificar o dicionário global

    if flask_session_id not in active_sdk_chats or not active_sdk_chats[flask_session_id].get('sdk_chat_obj'):
        print(f"INFO (session_manager): Tentando criar/recarregar chat SDK para flask_session_id: {flask_session_id}")
        
        sdk_history_key = f"{SESSION_KEY_SDK_HISTORY}_{flask_session_id}"
        sdk_msg_count_key = f"{SESSION_KEY_SDK_MSG_COUNT}_{flask_session_id}"

        loaded_gemini_history_serializable = session.get(sdk_history_key, [])
        loaded_sdk_message_count = session.get(sdk_msg_count_key, 0)
        
        gemini_compatible_history = []
        if loaded_gemini_history_serializable:
            print(f"INFO (session_manager): Histórico SDK ({len(loaded_gemini_history_serializable)} msgs) encontrado na session Flask para {flask_session_id}.")
            for msg_data in loaded_gemini_history_serializable:
                content_parts = []
                if msg_data.get('parts'):
                    for part_data in msg_data['parts']:
                        if 'text' in part_data and part_data['text'] is not None:
                           content_parts.append(genai.types.Part(text=part_data['text']))
                
                if msg_data.get('role') and (content_parts or msg_data['role'] == 'user'):
                     gemini_compatible_history.append(
                        genai.types.Content(role=msg_data['role'], parts=content_parts)
                    )
        else:
            print(f"INFO (session_manager): Nenhum histórico SDK na session Flask para {flask_session_id}.")

        try:
            if model_instance is None:
                raise Exception("Instância do modelo Gemini não está disponível em chatbot_logic.")
            sdk_chat_obj = model_instance.start_chat(history=gemini_compatible_history)
            active_sdk_chats[flask_session_id] = {
                'sdk_chat_obj': sdk_chat_obj, 
                'sdk_message_count': loaded_sdk_message_count
            }
            print(f"INFO (session_manager): Chat SDK (re)criado para {flask_session_id}. Msgs: {loaded_sdk_message_count}. Histórico SDK: {len(sdk_chat_obj.history)} msgs.")
        except Exception as e:
            print(f"ERRO (session_manager): Ao iniciar chat SDK com histórico para {flask_session_id}: {e}")
            sdk_chat_obj = model_instance.start_chat(history=[]) # Fallback
            active_sdk_chats[flask_session_id] = {'sdk_chat_obj': sdk_chat_obj, 'sdk_message_count': 0}
            print(f"ERRO (session_manager): Chat SDK iniciado SEM histórico para {flask_session_id}.")
            
    return active_sdk_chats[flask_session_id]

def get_sdk_message_count(flask_session_id):
    sdk_data = active_sdk_chats.get(flask_session_id, {})
    return sdk_data.get('sdk_message_count', 0)

def increment_sdk_message_count(flask_session_id):
    if flask_session_id in active_sdk_chats:
        active_sdk_chats[flask_session_id]['sdk_message_count'] += 1
        print(f"INFO (session_manager): Contagem de mensagens SDK para {flask_session_id} incrementada para {active_sdk_chats[flask_session_id]['sdk_message_count']}")
        # A contagem será salva na session Flask pela rota principal após a chamada do Gemini

def save_sdk_state_to_flask_session(flask_session_id):
    """Salva o histórico e a contagem de mensagens do SDK na session Flask."""
    if flask_session_id in active_sdk_chats:
        sdk_data = active_sdk_chats[flask_session_id]
        sdk_chat_obj = sdk_data.get('sdk_chat_obj')
        
        if sdk_chat_obj and hasattr(sdk_chat_obj, 'history'):
            serializable_history = []
            for content_message in sdk_chat_obj.history:
                parts_data = []
                if content_message.parts:
                    for part in content_message.parts:
                        if hasattr(part, 'text') and part.text is not None:
                            parts_data.append({'text': part.text})
                
                if content_message.role and (parts_data or content_message.role == 'user'):
                    serializable_history.append({
                        'role': content_message.role,
                        'parts': parts_data
                    })
            
            sdk_history_key = f"{SESSION_KEY_SDK_HISTORY}_{flask_session_id}"
            sdk_msg_count_key = f"{SESSION_KEY_SDK_MSG_COUNT}_{flask_session_id}"

            session[sdk_history_key] = serializable_history
            session[sdk_msg_count_key] = sdk_data.get('sdk_message_count', 0)
            session.modified = True # Importante
            print(f"INFO (session_manager): Histórico SDK ({len(serializable_history)} msgs) e contagem ({session[sdk_msg_count_key]}) salvos na session Flask para {flask_session_id}.")
        else:
            print(f"WARN (session_manager): Objeto de chat SDK não encontrado ou sem histórico para {flask_session_id} ao tentar salvar.")
    else:
        print(f"WARN (session_manager): Nenhum dado de chat SDK ativo para {flask_session_id} ao tentar salvar.")


# Funções para gerenciar flags de estado da conversa na session Flask
def set_flag(flag_key, value=True):
    session[flag_key] = value
    print(f"INFO (session_manager): Flag '{flag_key}' SET para {value}.")

def get_flag(flag_key, default=None):
    return session.get(flag_key, default)

def clear_flag(flag_key):
    popped_value = session.pop(flag_key, None)
    if popped_value is not None:
        print(f"INFO (session_manager): Flag '{flag_key}' LIMPADA (valor era: {popped_value}).")
    return popped_value

# Atalhos para flags comuns
def has_asked_checkin_scale(): return get_flag(SESSION_KEY_ASKED_SCALE, False)
def set_asked_checkin_scale(): set_flag(SESSION_KEY_ASKED_SCALE)
def clear_asked_checkin_scale(): clear_flag(SESSION_KEY_ASKED_SCALE)

def has_asked_checkin_word(): return get_flag(SESSION_KEY_ASKED_WORD, False)
def set_asked_checkin_word(): set_flag(SESSION_KEY_ASKED_WORD)
def clear_asked_checkin_word(): clear_flag(SESSION_KEY_ASKED_WORD)

def is_pending_guidance_offer(): return get_flag(SESSION_KEY_PENDING_GUIDANCE, False)
def set_pending_guidance_offer(): set_flag(SESSION_KEY_PENDING_GUIDANCE)
def clear_pending_guidance_offer(): clear_flag(SESSION_KEY_PENDING_GUIDANCE)

# --- Funções para Três Coisas Boas ---
def was_three_good_things_suggested():
    return get_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS, False)

def set_three_good_things_suggested():
    set_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS)

def clear_three_good_things_suggested():
    clear_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS)