# meu_guardiao_do_bem_estar/chatbot_logic/utils.py
from datetime import datetime, timezone

def format_single_message_for_template(role, text_parts_list, timestamp_dt_object=None):
    """Formata uma ÚNICA mensagem para a estrutura esperada pelo template."""
    if timestamp_dt_object is None:
        timestamp_dt_object = datetime.now(timezone.utc)
    elif not isinstance(timestamp_dt_object, datetime):
        print(f"WARN (utils): format_single_message recebeu timestamp inválido: {timestamp_dt_object}. Usando now().")
        timestamp_dt_object = datetime.now(timezone.utc)
    
    # Garante que text_parts_list seja sempre uma lista de strings
    if not isinstance(text_parts_list, list):
        parts = [str(text_parts_list)]
    else:
        parts = [str(part) for part in text_parts_list if part is not None] # Filtra None e converte para str

    return {
        'role': role,
        'parts_for_template': parts,
        'timestamp': timestamp_dt_object.strftime("%d/%m/%Y %H:%M")
    }

def get_current_timestamp_str():
    """Retorna o timestamp atual formatado."""
    return datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M")

# Adicione outras funções utilitárias aqui conforme necessário