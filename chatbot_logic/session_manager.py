# meu_guardiao_do_bem_estar/chatbot_logic/session_manager.py
from flask import session
from chatbot_logic import model_instance 
from config import (
    SESSION_KEY_SDK_HISTORY, SESSION_KEY_SDK_MSG_COUNT,
    SESSION_KEY_ASKED_SCALE, SESSION_KEY_ASKED_WORD, 
    SESSION_KEY_PENDING_GUIDANCE_BREATHING, SESSION_KEY_PENDING_GUIDANCE_SOUNDS, SESSION_KEY_PENDING_GUIDANCE_BODYSCAN,
    SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS
)
import google.generativeai as genai

active_sdk_chats = {}

# ... (get_or_create_sdk_chat_data, get_sdk_message_count, increment_sdk_message_count, save_sdk_state_to_flask_session como antes) ...
# (funções set_flag, get_flag, clear_flag como antes)
# (helpers para asked_scale, asked_word, pending_breathing, pending_sounds, three_good_things como antes)

def get_or_create_sdk_chat_data(flask_session_id): # Mantendo a versão completa anterior
    global active_sdk_chats
    if flask_session_id not in active_sdk_chats or not active_sdk_chats[flask_session_id].get('sdk_chat_obj'):
        print(f"INFO (session_manager): Tentando criar/recarregar chat SDK para flask_session_id: {flask_session_id}")
        sdk_history_key = f"{SESSION_KEY_SDK_HISTORY}_{flask_session_id}"
        sdk_msg_count_key = f"{SESSION_KEY_SDK_MSG_COUNT}_{flask_session_id}"
        loaded_gemini_history_serializable = session.get(sdk_history_key, [])
        loaded_sdk_message_count = session.get(sdk_msg_count_key, 0)
        gemini_compatible_history = []
        if loaded_gemini_history_serializable:
            print(f"INFO (session_manager): Histórico SDK ({len(loaded_gemini_history_serializable)} msgs) da session Flask para {flask_session_id}.")
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
            if model_instance is None: raise Exception("Instância do modelo Gemini não disponível.")
            sdk_chat_obj = model_instance.start_chat(history=gemini_compatible_history)
            active_sdk_chats[flask_session_id] = {'sdk_chat_obj': sdk_chat_obj, 'sdk_message_count': loaded_sdk_message_count}
            print(f"INFO (session_manager): Chat SDK (re)criado para {flask_session_id}. Msgs: {loaded_sdk_message_count}. Histórico SDK: {len(sdk_chat_obj.history)}.")
        except Exception as e:
            print(f"ERRO (session_manager): Ao iniciar chat SDK para {flask_session_id}: {e}")
            if model_instance:
                sdk_chat_obj = model_instance.start_chat(history=[])
                active_sdk_chats[flask_session_id] = {'sdk_chat_obj': sdk_chat_obj, 'sdk_message_count': 0}
                print(f"INFO (session_manager): Chat SDK iniciado SEM histórico para {flask_session_id} devido a falha.")
            else:
                active_sdk_chats[flask_session_id] = {'sdk_chat_obj': None, 'sdk_message_count': 0}
    return active_sdk_chats[flask_session_id]

def get_sdk_message_count(flask_session_id):
    return active_sdk_chats.get(flask_session_id, {}).get('sdk_message_count', 0)

def increment_sdk_message_count(flask_session_id):
    if flask_session_id in active_sdk_chats and active_sdk_chats[flask_session_id].get('sdk_chat_obj'):
        active_sdk_chats[flask_session_id]['sdk_message_count'] += 1
        print(f"INFO (session_manager): Contagem SDK para {flask_session_id} incrementada para {active_sdk_chats[flask_session_id]['sdk_message_count']}")

def save_sdk_state_to_flask_session(flask_session_id):
    if flask_session_id in active_sdk_chats:
        sdk_data = active_sdk_chats[flask_session_id]
        sdk_chat_obj = sdk_data.get('sdk_chat_obj')
        if sdk_chat_obj and hasattr(sdk_chat_obj, 'history'):
            serializable_history = [{'role': cm.role, 'parts': [{'text': p.text} for p in cm.parts if hasattr(p, 'text') and p.text is not None]} for cm in sdk_chat_obj.history if cm.role and (any(hasattr(p, 'text') and p.text is not None for p in cm.parts) or cm.role == 'user')]
            sdk_history_key = f"{SESSION_KEY_SDK_HISTORY}_{flask_session_id}"
            sdk_msg_count_key = f"{SESSION_KEY_SDK_MSG_COUNT}_{flask_session_id}"
            session[sdk_history_key] = serializable_history
            session[sdk_msg_count_key] = sdk_data.get('sdk_message_count', 0)
            session.modified = True
            print(f"INFO (session_manager): Histórico SDK ({len(serializable_history)} msgs) e contagem ({session[sdk_msg_count_key]}) salvos para {flask_session_id}.")

def set_flag(flag_key_template, flask_session_id, value=True):
    session[f"{flag_key_template}_{flask_session_id}"] = value
    print(f"INFO (session_manager): Flag '{flag_key_template}_{flask_session_id}' SET para {value}.")

def get_flag(flag_key_template, flask_session_id, default=None):
    return session.get(f"{flag_key_template}_{flask_session_id}", default)

def clear_flag(flag_key_template, flask_session_id):
    full_key = f"{flag_key_template}_{flask_session_id}"
    popped_value = session.pop(full_key, None)
    if popped_value is not None: print(f"INFO (session_manager): Flag '{full_key}' LIMPADA (valor era: {popped_value}).")

def has_asked_checkin_scale(sid): return get_flag(SESSION_KEY_ASKED_SCALE, sid, False)
def set_asked_checkin_scale(sid): set_flag(SESSION_KEY_ASKED_SCALE, sid)
def clear_asked_checkin_scale(sid): clear_flag(SESSION_KEY_ASKED_SCALE, sid)

def has_asked_checkin_word(sid): return get_flag(SESSION_KEY_ASKED_WORD, sid, False)
def set_asked_checkin_word(sid): set_flag(SESSION_KEY_ASKED_WORD, sid)
def clear_asked_checkin_word(sid): clear_flag(SESSION_KEY_ASKED_WORD, sid)

def is_pending_guidance_breathing_offer(sid): return get_flag(SESSION_KEY_PENDING_GUIDANCE_BREATHING, sid, False)
def set_pending_guidance_breathing_offer(sid): set_flag(SESSION_KEY_PENDING_GUIDANCE_BREATHING, sid)
def clear_pending_guidance_breathing_offer(sid): clear_flag(SESSION_KEY_PENDING_GUIDANCE_BREATHING, sid)

def is_pending_guidance_sounds_offer(sid): return get_flag(SESSION_KEY_PENDING_GUIDANCE_SOUNDS, sid, False)
def set_pending_guidance_sounds_offer(sid): set_flag(SESSION_KEY_PENDING_GUIDANCE_SOUNDS, sid)
def clear_pending_guidance_sounds_offer(sid): clear_flag(SESSION_KEY_PENDING_GUIDANCE_SOUNDS, sid)

# --- Funções para Guia de Escaneamento Corporal --- (NOVO)
def is_pending_guidance_bodyscan_offer(sid):
    return get_flag(SESSION_KEY_PENDING_GUIDANCE_BODYSCAN, sid, False)

def set_pending_guidance_bodyscan_offer(sid):
    set_flag(SESSION_KEY_PENDING_GUIDANCE_BODYSCAN, sid)

def clear_pending_guidance_bodyscan_offer(sid):
    clear_flag(SESSION_KEY_PENDING_GUIDANCE_BODYSCAN, sid)

def was_three_good_things_suggested(sid): return get_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS, sid, False)
def set_three_good_things_suggested(sid): set_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS, sid)
def clear_three_good_things_suggested(sid): clear_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS, sid)