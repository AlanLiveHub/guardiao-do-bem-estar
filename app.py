# meu_guardiao_do_bem_estar/app.py
import os
from flask import Flask, render_template, request, jsonify, session
import uuid
from datetime import datetime, timezone # utils.py também usa, mas pode ser bom aqui para timestamps de resposta

# Importações dos seus novos módulos
import config # Para APP_SECRET_KEY e outras configs se necessário diretamente aqui
from chatbot_logic import session_manager, flow_handler, utils
# A instância do modelo Gemini e a configuração da API são feitas em chatbot_logic/__init__.py

app = Flask(__name__)
app.secret_key = config.APP_SECRET_KEY # Usa a chave do config.py

@app.route('/')
def index_route():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session[config.SESSION_KEY_UI_HISTORY] = [] # Usa chave de config
        print(f"Flask session e ui_chat_history inicializados para {session['session_id']}")
    
    # Garante que a sessão do SDK (em memória) exista ou seja recarregada da session Flask
    _ = session_manager.get_or_create_sdk_chat_data(session['session_id'])
    
    ui_history_to_render = session.get(config.SESSION_KEY_UI_HISTORY, [])
    return render_template('index.html', chat_history_for_template=ui_history_to_render)

@app.route('/send_message', methods=['POST'])
def send_message_route_refactored():
    if 'session_id' not in session:
        print("ERRO (app.py): Sessão Flask não encontrada.")
        return jsonify({"error": "Sessão Flask não encontrada. Por favor, recarregue a página."}), 400
    
    current_flask_session_id = session['session_id']
    user_input_text = request.form.get('message', "").strip()

    if not user_input_text:
        print("WARN (app.py): Mensagem do usuário vazia recebida.")
        # Pode retornar um erro ou apenas uma resposta vazia para não quebrar o frontend
        return jsonify({
            "response_parts": ["Por favor, digite uma mensagem."],
            "full_history_for_template": session.get(config.SESSION_KEY_UI_HISTORY, [])
        }), 200 # Ou 400 se preferir tratar como erro de cliente


    sdk_data = session_manager.get_or_create_sdk_chat_data(current_flask_session_id)
    if not sdk_data or 'sdk_chat_obj' not in sdk_data: # Checagem extra de segurança
        print(f"ERRO CRÍTICO (app.py): Não foi possível obter sdk_chat_obj para {current_flask_session_id}")
        return jsonify({"error": "Erro interno ao configurar o chat do assistente."}), 500
    sdk_chat_obj = sdk_data['sdk_chat_obj']

    current_ui_history = session.get(config.SESSION_KEY_UI_HISTORY, [])

    # Adiciona mensagem do usuário à UI history
    user_msg_for_ui = utils.format_single_message_for_template(
        'user', [user_input_text] # timestamp é gerado dentro da função
    )
    current_ui_history.append(user_msg_for_ui)

    # Delega o processamento da lógica da mensagem
    bot_response_parts, did_send_to_gemini, _ = flow_handler.handle_user_message(
        user_input_text, 
        sdk_chat_obj, 
        current_flask_session_id
    )

    # Adiciona resposta do bot à UI history
    bot_response_timestamp = None # Será definido pelo SDK ou fallback
    if did_send_to_gemini and hasattr(sdk_chat_obj, 'history') and sdk_chat_obj.history and sdk_chat_obj.history[-1].role == 'model':
        sdk_msg_obj = sdk_chat_obj.history[-1]
        # Tenta obter create_time, depois update_time do objeto Content do SDK
        sdk_timestamp_dt = getattr(sdk_msg_obj, 'create_time', getattr(sdk_msg_obj, 'update_time', None))
        if isinstance(sdk_timestamp_dt, datetime):
            bot_response_timestamp = sdk_timestamp_dt
            
    bot_msg_for_ui = utils.format_single_message_for_template(
        'model', bot_response_parts, bot_response_timestamp # Passa o timestamp do SDK ou None (utils lida com None)
    )
    current_ui_history.append(bot_msg_for_ui)

    session[config.SESSION_KEY_UI_HISTORY] = current_ui_history # Salva histórico da UI
    
    if did_send_to_gemini: 
        session_manager.increment_sdk_message_count(current_flask_session_id)
        # Salva o estado do SDK (histórico e contagem) na session Flask
        session_manager.save_sdk_state_to_flask_session(current_flask_session_id)
    
    return jsonify({
        "response_parts": bot_response_parts, 
        "full_history_for_template": current_ui_history 
    })

if __name__ == '__main__':
    # Adicionar um check para GEMINI_API_KEY antes de rodar, usando config.GEMINI_API_KEY
    if not config.GEMINI_API_KEY:
        print("ERRO FATAL: GEMINI_API_KEY não configurada. Verifique seu arquivo .env e config.py")
    else:
        app.run(debug=True, port=5000)