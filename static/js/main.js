// static/js/main.js
import { setAvatarUrls, appendMessageToUI, renderFullHistory, showTypingIndicator, removeTypingIndicator, getCurrentTimestamp, scrollToBottom } from './ui.js';
import { sendMessageToServer } from './api.js';

// Seletores de DOM Globais para este módulo
const messageForm = document.getElementById('messageForm');
const userInputElement = document.getElementById('userInput');
const messagesContainer = document.getElementById('messages');
const sendButton = document.getElementById('sendButton');

// Configura as URLs dos avatares para o módulo ui.js
// Estas variáveis globais USER_AVATAR_URL_FROM_TEMPLATE e BOT_AVATAR_URL_FROM_TEMPLATE
// devem ser definidas no index.html em uma tag <script> ANTES de carregar main.js
// Ex: <script> const USER_AVATAR_URL_FROM_TEMPLATE = "{{...}}"; </script>
if (typeof USER_AVATAR_URL_FROM_TEMPLATE !== 'undefined' && typeof BOT_AVATAR_URL_FROM_TEMPLATE !== 'undefined') {
    setAvatarUrls(USER_AVATAR_URL_FROM_TEMPLATE, BOT_AVATAR_URL_FROM_TEMPLATE);
} else {
    console.error("URLs de avatar não definidas no template HTML para main.js!");
    // Defina fallbacks ou trate o erro
    setAvatarUrls('path/to/default_user_avatar.png', 'path/to/default_bot_avatar.png');
}


// Event listener principal
if (messageForm) {
    messageForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (!userInputElement || !sendButton || !messagesContainer) return;

        const messageText = userInputElement.value.trim();
        if (messageText === '') return;

        appendMessageToUI(messagesContainer, messageText, 'user', getCurrentTimestamp(), false, false, null);
        const sentMessageText = messageText; 
        userInputElement.value = ''; 

        const originalButtonText = sendButton.textContent;
        sendButton.disabled = true; 
        sendButton.textContent = 'Enviando...';
        userInputElement.disabled = true;
        showTypingIndicator(messagesContainer);

        const result = await sendMessageToServer(sentMessageText);
        removeTypingIndicator(); 

        if (!result.ok) {
            // Se 'result.data' existir e tiver 'full_history_for_template', usa-o.
            // Isso pode acontecer se o servidor responder com um erro mas ainda fornecer o histórico.
            if (result.data && result.data.full_history_for_template) {
                renderFullHistory(messagesContainer, result.data.full_history_for_template, false, () => userInputElement.focus());
            } else {
                // Caso contrário, mostra a mensagem de erro diretamente.
                appendMessageToUI(messagesContainer, result.error || "Erro desconhecido.", 'bot', getCurrentTimestamp(), true, false, () => userInputElement.focus());
            }
        } else {
            // Resposta OK
            const serverData = result.data;
            if (serverData && serverData.full_history_for_template) {
                renderFullHistory(messagesContainer, serverData.full_history_for_template, true, () => userInputElement.focus()); 
            } else { 
                console.warn("[main.js] Resposta OK, mas estrutura de dados inesperada.");
                appendMessageToUI(messagesContainer, "Resposta inesperada do servidor.", 'bot', getCurrentTimestamp(), false, false, () => userInputElement.focus());
            }
        }
        
        sendButton.textContent = originalButtonText;
        sendButton.disabled = false;
        userInputElement.disabled = false;
        if (!document.querySelector('.typing-indicator-row') && document.activeElement !== userInputElement) {
            // userInputElement.focus(); // O foco é melhor tratado no callback de renderFullHistory
        }
    });
} else {
    console.error("Formulário de mensagem não encontrado!");
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    if (messagesContainer) {
        scrollToBottom(messagesContainer);
    }
});