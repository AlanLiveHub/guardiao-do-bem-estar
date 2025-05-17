# meu_guardiao_do_bem_estar/chatbot_logic/session_manager.py
from flask import session
from chatbot_logic import model_instance # Importa a instância do modelo
from config import (
    # Importa as chaves de sessão com o novo sufixo de config.py
    SESSION_KEY_SDK_HISTORY, SESSION_KEY_SDK_MSG_COUNT,
    SESSION_KEY_ASKED_SCALE, SESSION_KEY_ASKED_WORD, 
    SESSION_KEY_PENDING_GUIDANCE_BREATHING, SESSION_KEY_PENDING_GUIDANCE_SOUNDS, 
    SESSION_KEY_PENDING_GUIDANCE_BODYSCAN,
    SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS,
    SESSION_KEY_USER_POINTS # Importa a chave de pontos
)
import google.generativeai as genai # Para types.Content e types.Part

# Dicionário em memória para os objetos de chat ativos do SDK
active_sdk_chats = {}

def get_or_create_sdk_chat_data(flask_session_id):
    """Obtém ou cria/recarrega os dados do chat SDK para uma dada flask_session_id."""
    global active_sdk_chats

    if flask_session_id not in active_sdk_chats or \
       active_sdk_chats[flask_session_id].get('sdk_chat_obj') is None: # Verifica se o objeto é None também
        print(f"INFO (session_manager): Tentando criar/recarregar chat SDK para flask_session_id: {flask_session_id}")
        
        # Usa as chaves de sessão importadas de config.py (que já incluem o sufixo)
        # Não precisa mais formatar com f-string aqui se as chaves já vêm completas de config.py
        # No entanto, se você quiser manter a lógica de adicionar _flask_session_id às chaves de sessão
        # para isolar dados de diferentes usuários DENTRO da mesma instância de `session` global do Flask
        # (o que não é como a `session` do Flask normalmente funciona, ela já é por usuário/navegador),
        # você pode manter. Para a `session` do Flask, usar a chave direta de config é suficiente.
        # Vou simplificar para usar a chave direta de config, assumindo que `session` do Flask é por usuário.

        loaded_gemini_history_serializable = session.get(SESSION_KEY_SDK_HISTORY, [])
        loaded_sdk_message_count = session.get(SESSION_KEY_SDK_MSG_COUNT, 0)
        
        gemini_compatible_history = []
        if loaded_gemini_history_serializable:
            print(f"INFO (session_manager): Histórico SDK ({len(loaded_gemini_history_serializable)} msgs) da session Flask para {flask_session_id}.")
            for msg_data in loaded_gemini_history_serializable:
                content_parts = []
                if msg_data.get('parts'):
                    for part_data in msg_data['parts']:
                        if 'text' in part_data and part_data['text'] is not None:
                           content_parts.append(genai.types.Part(text=part_data['text']))
                if msg_data.get('role') and (content_parts or msg_data['role'] == 'user'): # Permite 'user' role sem parts
                     gemini_compatible_history.append(
                        genai.types.Content(role=msg_data['role'], parts=content_parts)
                    )
        else:
            print(f"INFO (session_manager): Nenhum histórico SDK na session Flask para {flask_session_id}.")

        try:
            if model_instance is None:
                print("ERRO CRÍTICO (session_manager): Instância do modelo Gemini (model_instance) não está disponível.")
                # Define um objeto de chat "dummy" ou None para evitar mais erros, mas o chat não funcionará
                active_sdk_chats[flask_session_id] = {'sdk_chat_obj': None, 'sdk_message_count': 0}
                return active_sdk_chats[flask_session_id] # Retorna o objeto "dummy"

            sdk_chat_obj = model_instance.start_chat(history=gemini_compatible_history)
            active_sdk_chats[flask_session_id] = {
                'sdk_chat_obj': sdk_chat_obj, 
                'sdk_message_count': loaded_sdk_message_count
            }
            print(f"INFO (session_manager): Chat SDK (re)criado para {flask_session_id}. Msgs: {loaded_sdk_message_count}. Histórico SDK: {len(sdk_chat_obj.history)}.")
        except Exception as e:
            print(f"ERRO (session_manager): Ao iniciar chat SDK com histórico para {flask_session_id}: {e}")
            if model_instance: # Tenta criar um novo chat se o modelo existe
                sdk_chat_obj = model_instance.start_chat(history=[])
                active_sdk_chats[flask_session_id] = {'sdk_chat_obj': sdk_chat_obj, 'sdk_message_count': 0}
                print(f"INFO (session_manager): Chat SDK iniciado SEM histórico para {flask_session_id} devido a falha no carregamento.")
            else:
                print(f"ERRO CRÍTICO (session_manager): Não foi possível criar chat SDK pois model_instance é None.")
                active_sdk_chats[flask_session_id] = {'sdk_chat_obj': None, 'sdk_message_count': 0}
            
    return active_sdk_chats[flask_session_id]

def get_sdk_message_count(flask_session_id):
    sdk_data = active_sdk_chats.get(flask_session_id, {})
    return sdk_data.get('sdk_message_count', 0)

def increment_sdk_message_count(flask_session_id):
    if flask_session_id in active_sdk_chats and active_sdk_chats[flask_session_id].get('sdk_chat_obj'):
        active_sdk_chats[flask_session_id]['sdk_message_count'] += 1
        print(f"INFO (session_manager): Contagem SDK para {flask_session_id} incrementada para {active_sdk_chats[flask_session_id]['sdk_message_count']}")

def save_sdk_state_to_flask_session(flask_session_id):
    """Salva o histórico e a contagem de mensagens do SDK na session Flask."""
    if flask_session_id in active_sdk_chats:
        sdk_data = active_sdk_chats[flask_session_id]
        sdk_chat_obj = sdk_data.get('sdk_chat_obj')
        
        if sdk_chat_obj and hasattr(sdk_chat_obj, 'history'):
            serializable_history = []
            for content_message in sdk_chat_obj.history:
                parts_data = []
                if content_message.parts: # Verifica se parts existe e não é None
                    for part in content_message.parts:
                        if hasattr(part, 'text') and part.text is not None:
                            parts_data.append({'text': part.text})
                
                # Adiciona apenas se tiver 'role' e (parts_data OU é um usuário, que pode ter entrada vazia)
                if content_message.role and (parts_data or content_message.role == 'user'):
                    serializable_history.append({
                        'role': content_message.role,
                        'parts': parts_data
                    })
            
            session[SESSION_KEY_SDK_HISTORY] = serializable_history # Usa chave de config
            session[SESSION_KEY_SDK_MSG_COUNT] = sdk_data.get('sdk_message_count', 0) # Usa chave de config
            session.modified = True 
            print(f"INFO (session_manager): Histórico SDK ({len(serializable_history)} msgs) e contagem ({session[SESSION_KEY_SDK_MSG_COUNT]}) salvos na session Flask para {flask_session_id}.")
        else:
            print(f"WARN (session_manager): Objeto de chat SDK não encontrado ou sem histórico para {flask_session_id} ao tentar salvar.")
    else:
        print(f"WARN (session_manager): Nenhum dado de chat SDK ativo para {flask_session_id} ao tentar salvar.")

# --- Gerenciamento de Flags Genérico ---
# Agora as funções de flag NÃO anexam flask_session_id, pois a chave de config JÁ é única por sessão (se for o caso)
# ou a 'session' do Flask já é por usuário. Se as chaves em config.py NÃO incluem o sufixo de versão,
# e você quer que cada flag seja realmente única por flask_session_id DENTRO do objeto session,
# então a lógica de f-string deve ser mantida aqui.
# Assumindo que as chaves em config.py SÃO as chaves finais da session:

def set_flag(flag_key, value=True): # Não precisa mais de flask_session_id se a chave já é única
    session[flag_key] = value
    print(f"INFO (session_manager): Flag '{flag_key}' SET para {value}.")

def get_flag(flag_key, default=None): # Não precisa mais de flask_session_id
    return session.get(flag_key, default)

def clear_flag(flag_key): # Não precisa mais de flask_session_id
    popped_value = session.pop(flag_key, None)
    if popped_value is not None:
        print(f"INFO (session_manager): Flag '{flag_key}' LIMPADA (valor era: {popped_value}).")

# --- Atalhos para Flags de Estado da Conversa ---
# Estas funções agora chamam set_flag/get_flag/clear_flag com a chave completa de config.py
# Não precisam mais do argumento flask_session_id (sid)

def has_asked_checkin_scale(): return get_flag(SESSION_KEY_ASKED_SCALE, False)
def set_asked_checkin_scale(): set_flag(SESSION_KEY_ASKED_SCALE)
def clear_asked_checkin_scale(): clear_flag(SESSION_KEY_ASKED_SCALE)

def has_asked_checkin_word(): return get_flag(SESSION_KEY_ASKED_WORD, False)
def set_asked_checkin_word(): set_flag(SESSION_KEY_ASKED_WORD)
def clear_asked_checkin_word(): clear_flag(SESSION_KEY_ASKED_WORD)

def is_pending_guidance_breathing_offer(): return get_flag(SESSION_KEY_PENDING_GUIDANCE_BREATHING, False)
def set_pending_guidance_breathing_offer(): set_flag(SESSION_KEY_PENDING_GUIDANCE_BREATHING)
def clear_pending_guidance_breathing_offer(): clear_flag(SESSION_KEY_PENDING_GUIDANCE_BREATHING)

def is_pending_guidance_sounds_offer(): return get_flag(SESSION_KEY_PENDING_GUIDANCE_SOUNDS, False)
def set_pending_guidance_sounds_offer(): set_flag(SESSION_KEY_PENDING_GUIDANCE_SOUNDS)
def clear_pending_guidance_sounds_offer(): clear_flag(SESSION_KEY_PENDING_GUIDANCE_SOUNDS)

def is_pending_guidance_bodyscan_offer(): return get_flag(SESSION_KEY_PENDING_GUIDANCE_BODYSCAN, False)
def set_pending_guidance_bodyscan_offer(): set_flag(SESSION_KEY_PENDING_GUIDANCE_BODYSCAN)
def clear_pending_guidance_bodyscan_offer(): clear_flag(SESSION_KEY_PENDING_GUIDANCE_BODYSCAN)

def was_three_good_things_suggested(): return get_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS, False)
def set_three_good_things_suggested(): set_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS)
def clear_three_good_things_suggested(): clear_flag(SESSION_KEY_SUGGESTED_THREE_GOOD_THINGS)


# --- Funções de Gamificação ---
def get_user_points(): # Não precisa mais de flask_session_id se a chave já é única
    return session.get(SESSION_KEY_USER_POINTS, 0) 

def add_user_points(points_to_add): # Não precisa mais de flask_session_id
    current_points = get_user_points()
    new_total_points = current_points + points_to_add
    session[SESSION_KEY_USER_POINTS] = new_total_points
    session.modified = True
    print(f"INFO (session_manager): Adicionado {points_to_add} pontos. Novo total: {new_total_points}")
    return new_total_points