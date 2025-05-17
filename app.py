# meu_guardiao_do_bem_estar/app.py
import os
from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime, timezone

import config 
from chatbot_logic import session_manager, flow_handler, utils

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY

@app.route('/')
def index_route():
    first_bot_message_sent_this_session_key = 'first_bot_message_sent_v3' # Nova chave para teste limpo

    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session[config.SESSION_KEY_UI_HISTORY] = [] 
        session[first_bot_message_sent_this_session_key] = False
        print(f"INFO (app.py): Flask session e ui_chat_history inicializados para {session['session_id']}")

    _ = session_manager.get_or_create_sdk_chat_data(session['session_id'])
    
    if not session.get(first_bot_message_sent_this_session_key, False):
        print(f"INFO (app.py): Adicionando primeira mensagem do bot para a sessão {session['session_id']}")
        
        welcome_message_parts = [
            config.DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE[0],
            config.DISCLAIMER_TEXT_FOR_FIRST_BOT_RESPONSE[1],
            "Como posso te ajudar a cultivar pequenos hábitos positivos hoje?"
        ]

        first_bot_msg_obj = utils.format_single_message_for_template(
            'model', 
            welcome_message_parts,
            datetime.now(timezone.utc)
        )
        
        current_ui_history_for_welcome = session.get(config.SESSION_KEY_UI_HISTORY, [])
        current_ui_history_for_welcome.append(first_bot_msg_obj)
        session[config.SESSION_KEY_UI_HISTORY] = current_ui_history_for_welcome
        
        session[first_bot_message_sent_this_session_key] = True
        session.modified = True
        print(f"INFO (app.py): Primeira mensagem do bot adicionada. Flag '{first_bot_message_sent_this_session_key}' SET.")

    ui_history_to_render = session.get(config.SESSION_KEY_UI_HISTORY, [])
    return render_template('index.html', chat_history_for_template=ui_history_to_render)

@app.route('/send_message', methods=['POST'])
def send_message_route_refactored():
    if 'session_id' not in session:
        print("ERRO (app.py): Sessão Flask não encontrada.")
        return jsonify({"error": "Sessão Flask não encontrada. Por favor, recarregue a página."}), 400
    
    current_flask_session_id = session['session_id']
    user_input_text = request.form.get('message', "").strip()

    current_ui_history = session.get(config.SESSION_KEY_UI_HISTORY, []) # Pega antes de adicionar msg do usuário

    if not user_input_text:
        print("WARN (app.py): Mensagem do usuário vazia recebida.")
        bot_empty_response_parts = ["Por favor, digite uma mensagem válida."]
        bot_empty_msg_obj = utils.format_single_message_for_template(
            'model', bot_empty_response_parts, datetime.now(timezone.utc)
        )
        current_ui_history.append(bot_empty_msg_obj) # Adiciona ao histórico da UI
        session[config.SESSION_KEY_UI_HISTORY] = current_ui_history
        session.modified = True
        return jsonify({
            "response_parts": bot_empty_response_parts,
            "full_history_for_template": current_ui_history
        }), 200

    sdk_data = session_manager.get_or_create_sdk_chat_data(current_flask_session_id)
    if not sdk_data or 'sdk_chat_obj' not in sdk_data: 
        print(f"ERRO CRÍTICO (app.py): Não foi possível obter sdk_chat_obj para {current_flask_session_id}")
        # Adiciona mensagem de erro ao histórico da UI também
        error_parts = ["Desculpe, estou com um problema técnico interno. Tente mais tarde."]
        error_msg_obj = utils.format_single_message_for_template('model', error_parts, datetime.now(timezone.utc))
        current_ui_history.append(error_msg_obj)
        session[config.SESSION_KEY_UI_HISTORY] = current_ui_history
        session.modified = True
        return jsonify({"error": "Erro interno ao configurar o chat do assistente.", "response_parts": error_parts, "full_history_for_template": current_ui_history}), 500
    sdk_chat_obj = sdk_data['sdk_chat_obj']

    # Adiciona mensagem do usuário à UI history ANTES de chamar flow_handler
    user_msg_for_ui = utils.format_single_message_for_template(
        'user', [user_input_text] 
    )
    current_ui_history.append(user_msg_for_ui)
    # Não salva na sessão ainda, pois a resposta do bot também será adicionada

    bot_response_parts, did_send_to_gemini, _ = flow_handler.handle_user_message(
        user_input_text, 
        sdk_chat_obj, 
        current_flask_session_id
    )
    print(f"DEBUG (app.py): Retorno do flow_handler - bot_response_parts: {bot_response_parts}, did_send_to_gemini: {did_send_to_gemini}")

    # Garante que bot_response_parts seja uma lista e não seja None
    if bot_response_parts is None:
        bot_response_parts = ["Ocorreu um erro inesperado e não recebi uma resposta."]
        print("ERRO (app.py): bot_response_parts retornou None do flow_handler.")
    elif not isinstance(bot_response_parts, list):
        bot_response_parts = [str(bot_response_parts)]
        print(f"WARN (app.py): bot_response_parts não era lista, convertido para: {bot_response_parts}")


    bot_response_timestamp = None 
    if did_send_to_gemini and hasattr(sdk_chat_obj, 'history') and sdk_chat_obj.history and sdk_chat_obj.history[-1].role == 'model':
        sdk_msg_obj = sdk_chat_obj.history[-1]
        sdk_timestamp_dt = getattr(sdk_msg_obj, 'create_time', getattr(sdk_msg_obj, 'update_time', None))
        if isinstance(sdk_timestamp_dt, datetime):
            bot_response_timestamp = sdk_timestamp_dt
            
    bot_msg_for_ui = utils.format_single_message_for_template(
        'model', bot_response_parts, bot_response_timestamp 
    )
    current_ui_history.append(bot_msg_for_ui)

    session[config.SESSION_KEY_UI_HISTORY] = current_ui_history 
    session.modified = True

    if did_send_to_gemini: 
        session_manager.increment_sdk_message_count(current_flask_session_id)
        session_manager.save_sdk_state_to_flask_session(current_flask_session_id)
    
    print(f"DEBUG (app.py): Enviando para frontend - response_parts: {bot_response_parts}")
    return jsonify({
        "response_parts": bot_response_parts, 
        "full_history_for_template": current_ui_history 
    })

if __name__ == '__main__':
    if not config.GEMINI_API_KEY:
        print("ERRO FATAL: GEMINI_API_KEY não configurada. Verifique seu arquivo .env e config.py")
    else:
        app.run(debug=True, port=5000)