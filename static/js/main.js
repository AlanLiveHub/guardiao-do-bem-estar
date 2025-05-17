// static/js/main.js
import { 
    setAvatarUrls, 
    appendMessageToUI,
    renderFullHistory, 
    showTypingIndicator, 
    removeTypingIndicator, 
    getCurrentTimestamp, 
    scrollToBottom 
} from './ui.js';
import { sendMessageToServer } from './api.js';

const messageForm = document.getElementById('messageForm');
const userInputElement = document.getElementById('userInput');
const messagesContainer = document.getElementById('messages');
const sendButton = document.getElementById('sendButton');

if (typeof USER_AVATAR_URL_FROM_TEMPLATE !== 'undefined' && typeof BOT_AVATAR_URL_FROM_TEMPLATE !== 'undefined') {
    setAvatarUrls(USER_AVATAR_URL_FROM_TEMPLATE, BOT_AVATAR_URL_FROM_TEMPLATE);
} else {
    console.error("ERRO: URLs de avatar não definidas no template HTML!");
}

function enableInputControls(focusInput = true) {
    if (userInputElement) userInputElement.disabled = false;
    if (sendButton) {
        sendButton.disabled = false;
        sendButton.textContent = "Enviar"; 
    }
    if (focusInput && userInputElement && document.activeElement !== userInputElement) {
        userInputElement.focus();
    }
    console.log("[main.js] Controles de input HABILITADOS.");
}

function disableInputControls(buttonText = 'Enviando...') {
    if (userInputElement) userInputElement.disabled = true;
    if (sendButton) {
        sendButton.disabled = true;
        sendButton.textContent = buttonText; 
    }
    console.log("[main.js] Controles de input DESABILITADOS com texto:", buttonText);
}

if (messageForm && userInputElement && messagesContainer && sendButton) {
    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const messageText = userInputElement.value.trim();
        if (messageText === '') return;

        appendMessageToUI(messagesContainer, messageText, 'user', getCurrentTimestamp(), false, false, null);
        const sentMessageText = messageText; 
        userInputElement.value = ''; 

        disableInputControls('Enviando...'); 
        showTypingIndicator(messagesContainer);

        const result = await sendMessageToServer(sentMessageText);
        removeTypingIndicator(); 

        if (!result.ok) {
            console.error("[main.js] Erro da API recebido:", result.error);
            if (result.data && result.data.full_history_for_template) {
                renderFullHistory(messagesContainer, result.data.full_history_for_template, false, enableInputControls);
            } else {
                appendMessageToUI(messagesContainer, result.error || "Erro desconhecido.", 'bot', getCurrentTimestamp(), true, false, enableInputControls);
            }
        } else {
            const serverData = result.data;
            if (serverData && serverData.full_history_for_template) {
                const history = serverData.full_history_for_template;
                const lastMsg = history[history.length - 1];
                const willAnimate = lastMsg && (lastMsg.role === 'model' || lastMsg.role === 'bot') && !lastMsg.is_error;

                if (willAnimate) {
                    if(sendButton) sendButton.textContent = "Aguarde..."; 
                    console.log("[main.js] Botão atualizado para 'Aguarde...' durante a animação do bot.");
                }
                renderFullHistory(messagesContainer, serverData.full_history_for_template, true, enableInputControls); 
            } else { 
                console.warn("[main.js] Resposta OK, mas estrutura de dados do servidor inesperada.");
                appendMessageToUI(messagesContainer, "Resposta inesperada do servidor.", 'bot', getCurrentTimestamp(), false, false, enableInputControls);
            }
        }
    });
} else {
    console.error("ERRO: Um ou mais elementos essenciais do DOM não foram encontrados!");
}

document.addEventListener('DOMContentLoaded', () => {
    if (messagesContainer) {
        scrollToBottom(messagesContainer); 
    }
    enableInputControls(false); 
});