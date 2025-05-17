// static/js/ui.js

// URLs dos avatares (serão passadas do HTML ou definidas globalmente)
let USER_AVATAR_URL = '';
let BOT_AVATAR_URL = '';

// Função para configurar as URLs dos avatares (chamada de main.js)
export function setAvatarUrls(userUrl, botUrl) {
    USER_AVATAR_URL = userUrl;
    BOT_AVATAR_URL = botUrl;
}

// Elementos do DOM (serão selecionados em main.js e possivelmente passados ou acessados globalmente)
// Para simplificar, vamos assumir que são acessíveis globalmente após serem definidos em main.js
// ou passamos messagesContainer como argumento onde necessário.
// Melhor prática: passar os elementos como argumentos para as funções.

export function scrollToBottom(messagesContainerElement) {
    if (!messagesContainerElement) return;
    setTimeout(() => {
        messagesContainerElement.scrollTop = messagesContainerElement.scrollHeight;
    }, 60);
}

export function getCurrentTimestamp() {
    const now = new Date();
    const day = String(now.getDate()).padStart(2, '0');
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const year = now.getFullYear();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    return `${day}/${month}/${year} ${hours}:${minutes}`;
}

function typeMessageEffect(messageContentDiv, textToType, callback) {
    console.log("[typeMessageEffect] FUNÇÃO CHAMADA. Texto:", JSON.stringify(textToType.substring(0,50)+"..."));

    messageContentDiv.innerHTML = ''; // Limpa o conteúdo antes de iniciar

    if (typeof textToType !== 'string' || textToType.trim() === "") {
        console.warn("[typeMessageEffect] Texto inválido ou vazio.");
        messageContentDiv.innerHTML = " ";
        if (callback) callback();
        return;
    }

    let i = 0;
    const speed = 35;
    let builtString = "";

    function typeCharacter() {
        if (i < textToType.length) {
            const char = textToType.charAt(i);
            if (char === '\n') {
                builtString += "<br>";
            } else {
                builtString += char;
            }
            messageContentDiv.innerHTML = builtString;
            i++;
            // Acessando messagesContainer globalmente ou passado como argumento
            scrollToBottom(document.getElementById('messages')); 
            setTimeout(typeCharacter, speed);
        } else {
            console.log("[typeMessageEffect] Digitação concluída.");
            if (callback) callback(); 
        }
    }
    console.log("[typeMessageEffect] Iniciando loop de digitação...");
    typeCharacter();
}

export function appendMessageToUI(messagesContainerElement, text, role, timestampStr, isError = false, animateTyping = false, onTypingComplete = null) {
    if (!messagesContainerElement) {
        console.error("appendMessageToUI: messagesContainerElement não fornecido!");
        return;
    }
    const displayRole = (role === 'model') ? 'bot' : role;
    console.log(`[appendMessageToUI] Role: ${displayRole}, Animar: ${animateTyping}, Erro: ${isError}, Texto (inicio): ${JSON.stringify(String(text).substring(0,50))}...`);

    const messageRowDiv = document.createElement('div');
    messageRowDiv.classList.add('message-row');
    const avatarImg = document.createElement('img');
    avatarImg.classList.add('message-avatar');
    const bubbleWrapperDiv = document.createElement('div');
    bubbleWrapperDiv.classList.add('message-bubble-wrapper');
    const messageContentDiv = document.createElement('div');
    messageContentDiv.classList.add('message-content');
    const timestampDiv = document.createElement('div');
    timestampDiv.classList.add('message-timestamp');
    timestampDiv.textContent = timestampStr;
    
    if (displayRole === 'bot' && animateTyping && !isError) {
        timestampDiv.style.visibility = 'hidden';
    }

    bubbleWrapperDiv.appendChild(messageContentDiv);
    bubbleWrapperDiv.appendChild(timestampDiv);

    let finalText = (typeof text === 'string') ? text : ""; 

    if (displayRole === 'user') {
        messageRowDiv.classList.add('user-message-row');
        avatarImg.src = USER_AVATAR_URL; // Usa a variável global/módulo
        avatarImg.alt = "User Avatar";
        messageContentDiv.innerHTML = finalText.replace(/\n/g, '<br>');
    } else { // bot
        messageRowDiv.classList.add('bot-message-row');
        avatarImg.src = BOT_AVATAR_URL; // Usa a variável global/módulo
        avatarImg.alt = "Bot Avatar";

        if (isError) {
            messageContentDiv.classList.add('error-message-content');
            messageContentDiv.innerHTML = finalText ? finalText.replace(/\n/g, '<br>') : "Ocorreu um erro.";
        } else if (animateTyping) {
            // Preenchido por typeMessageEffect.
        } else { 
            messageContentDiv.innerHTML = finalText ? finalText.replace(/\n/g, '<br>') : " "; 
        }
    }

    messageRowDiv.appendChild(avatarImg);
    messageRowDiv.appendChild(bubbleWrapperDiv);
    messagesContainerElement.appendChild(messageRowDiv);
    // scrollToBottom(messagesContainerElement); // Chamado após animação ou diretamente

    if (displayRole === 'bot' && !isError && animateTyping) {
        const canAnimate = finalText && typeof finalText === 'string' && finalText.trim() !== "";
        
        if (canAnimate) { 
            typeMessageEffect(messageContentDiv, finalText, () => {
                timestampDiv.style.visibility = 'visible';
                if (onTypingComplete) onTypingComplete();
                scrollToBottom(messagesContainerElement);
            });
        } else { 
            messageContentDiv.innerHTML = " "; 
            timestampDiv.style.visibility = 'visible';
            if (onTypingComplete) onTypingComplete();
            scrollToBottom(messagesContainerElement);
        }
    } else {
        if (onTypingComplete) onTypingComplete();
        scrollToBottom(messagesContainerElement);
    }
}

export function renderFullHistory(messagesContainerElement, historyArray, animateLastBotMessage = false, focusCallback) {
    if (!messagesContainerElement) {
        console.error("renderFullHistory: messagesContainerElement não fornecido!");
        return;
    }
    console.log(`[renderFullHistory] Itens: ${historyArray ? historyArray.length : 0}, Animar último: ${animateLastBotMessage}`);
    messagesContainerElement.innerHTML = ''; 
    
    if (historyArray && Array.isArray(historyArray)) {
        historyArray.forEach((msg, index) => {
            const messageContent = (msg.parts_for_template && Array.isArray(msg.parts_for_template))
                                   ? msg.parts_for_template.join("\n")
                                   : ""; 
            
            const isError = (msg.role === 'model' || msg.role === 'bot') && msg.is_error; // Supondo que backend envie msg.is_error
            const isBot = msg.role === 'model' || msg.role === 'bot';
            const displayRole = isBot ? 'bot' : msg.role;

            const shouldAnimateThisMessage = animateLastBotMessage && 
                                           isBot && 
                                           index === historyArray.length - 1 &&
                                           !isError;
            
            const currentMsgOnTypingComplete = (isBot && index === historyArray.length - 1 && !isError && focusCallback) ? focusCallback : null;

            appendMessageToUI(
                messagesContainerElement,
                messageContent, 
                displayRole, 
                msg.timestamp || getCurrentTimestamp(), 
                isError,
                shouldAnimateThisMessage,
                currentMsgOnTypingComplete
            );
        });
    }
}

export function showTypingIndicator(messagesContainerElement) {
    if (!messagesContainerElement || !BOT_AVATAR_URL) return;
    if (document.querySelector('.typing-indicator-row')) return;

    const indicatorRow = document.createElement('div');
    indicatorRow.classList.add('typing-indicator-row', 'bot-message-row'); 
    const avatarImg = document.createElement('img');
    avatarImg.src = BOT_AVATAR_URL; 
    avatarImg.alt = "Bot Typing"; 
    avatarImg.classList.add('message-avatar');
    const typingDotsDiv = document.createElement('div');
    typingDotsDiv.classList.add('typing-indicator'); 
    typingDotsDiv.innerHTML = `<span></span><span></span><span></span>`;

    indicatorRow.appendChild(avatarImg); 
    indicatorRow.appendChild(typingDotsDiv);
    messagesContainerElement.appendChild(indicatorRow);
    scrollToBottom(messagesContainerElement);
}

export function removeTypingIndicator() { 
    const indicator = document.querySelector('.typing-indicator-row');
    if (indicator) indicator.remove();
}