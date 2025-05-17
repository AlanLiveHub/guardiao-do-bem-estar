// static/js/ui.js

let USER_AVATAR_URL = '';
let BOT_AVATAR_URL = '';

export function setAvatarUrls(userUrl, botUrl) {
    USER_AVATAR_URL = userUrl;
    BOT_AVATAR_URL = botUrl;
}

export function scrollToBottom(messagesContainerElement) {
    if (!messagesContainerElement) {
        console.warn("[ui.js] scrollToBottom: messagesContainerElement não encontrado.");
        return;
    }
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

function typeMessageEffect(messageContentDiv, textToType, callback, messagesContainerElementForScroll) {
    console.log("[typeMessageEffect] FUNÇÃO CHAMADA. Texto (inicio):", JSON.stringify(textToType.substring(0,50)+"..."));

    if (!messageContentDiv) {
        console.error("[typeMessageEffect] ERRO: messageContentDiv não é válido!");
        if (callback) callback();
        return;
    }
    messageContentDiv.innerHTML = ''; 

    if (typeof textToType !== 'string' || textToType.trim() === "") {
        console.warn("[typeMessageEffect] Texto inválido ou vazio. Exibindo placeholder.");
        messageContentDiv.innerHTML = " "; 
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
            if (messagesContainerElementForScroll) {
                scrollToBottom(messagesContainerElementForScroll); 
            }
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
        console.error("[appendMessageToUI] ERRO: messagesContainerElement não fornecido!");
        return;
    }
    const displayRole = (role === 'model') ? 'bot' : role;
    // Log detalhado do texto recebido
    console.log(`[appendMessageToUI] Role: ${displayRole}, Animar: ${animateTyping}, Erro: ${isError}, Texto COMPLETO: ${JSON.stringify(text)}`);


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
    let initialContent = finalText ? finalText.replace(/\n/g, '<br>') : " ";

    if (displayRole === 'user') {
        messageRowDiv.classList.add('user-message-row');
        avatarImg.src = USER_AVATAR_URL; 
        avatarImg.alt = "User Avatar";
        messageContentDiv.innerHTML = initialContent;
    } else { // bot
        messageRowDiv.classList.add('bot-message-row');
        avatarImg.src = BOT_AVATAR_URL; 
        avatarImg.alt = "Bot Avatar";

        if (isError) {
            messageContentDiv.classList.add('error-message-content');
            messageContentDiv.innerHTML = initialContent;
        } else if (animateTyping) {
            messageContentDiv.innerHTML = ''; 
        } else { 
            messageContentDiv.innerHTML = initialContent; 
        }
    }

    messageRowDiv.appendChild(avatarImg);
    messageRowDiv.appendChild(bubbleWrapperDiv);
    messagesContainerElement.appendChild(messageRowDiv);

    if (displayRole === 'bot' && !isError && animateTyping) {
        const canAnimate = finalText && finalText.trim() !== "";
        console.log(`[appendMessageToUI] Verificando condição para animar bot. 'finalText' é: ${JSON.stringify(finalText)}. Pode Animar: ${canAnimate}`);
        
        if (canAnimate) { 
            typeMessageEffect(messageContentDiv, finalText, () => {
                timestampDiv.style.visibility = 'visible';
                if (onTypingComplete) onTypingComplete();
            }, messagesContainerElement);
        } else { 
            console.warn("[appendMessageToUI] Animação pulada (texto vazio/inválido). 'finalText':", JSON.stringify(finalText));
            messageContentDiv.innerHTML = " "; 
            timestampDiv.style.visibility = 'visible';
            if (onTypingComplete) onTypingComplete();
            scrollToBottom(messagesContainerElement);
        }
    } else { 
        if (onTypingComplete) onTypingComplete();
        scrollToBottom(messagesContainerElement);
    }
}

export function renderFullHistory(messagesContainerElement, historyArray, animateLastBotMessage = false, enableInputCb) {
    if (!messagesContainerElement) { /* ... */ return; }
    console.log(`[renderFullHistory] Itens: ${historyArray ? historyArray.length : 0}, Animar último: ${animateLastBotMessage}`);
    messagesContainerElement.innerHTML = ''; 
    
    if (historyArray && Array.isArray(historyArray)) {
        historyArray.forEach((msg, index) => {
            const rawParts = msg.parts_for_template;
            // Log para verificar o parts_for_template original
            // console.log(`[renderFullHistory] Mensagem ${index} - parts_for_template original:`, JSON.stringify(rawParts));

            const messageContent = (rawParts && Array.isArray(rawParts) && rawParts.every(p => typeof p === 'string'))
                                   ? rawParts.join("\n")
                                   : ( (typeof rawParts === 'string') ? rawParts : "" ); // Aceita string única também
            
            // Log adicional para o messageContent após o join
            console.log(`[renderFullHistory] Mensagem ${index}: role=${msg.role}, parts_for_template=${JSON.stringify(rawParts)}, messageContentProcessado=${JSON.stringify(messageContent)}`);


            const isError = (msg.role === 'model' || msg.role === 'bot') && msg.is_error;
            const isBot = msg.role === 'model' || msg.role === 'bot';
            const displayRole = isBot ? 'bot' : msg.role;

            const shouldAnimateThisMessage = animateLastBotMessage && 
                                           isBot && 
                                           index === historyArray.length - 1 &&
                                           !isError;
            
            const currentMsgOnTypingComplete = (isBot && index === historyArray.length - 1 && !isError) 
                                             ? enableInputCb 
                                             : null;

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
    } else {
      scrollToBottom(messagesContainerElement);
    }
}

export function showTypingIndicator(messagesContainerElement) {
    if (!messagesContainerElement || !BOT_AVATAR_URL) { /* ... */ return; }
    removeTypingIndicator(); 
    const indicatorRow = document.createElement('div');
    indicatorRow.classList.add('message-row', 'bot-message-row', 'typing-indicator-row');
    const avatarImg = document.createElement('img');
    avatarImg.src = BOT_AVATAR_URL; 
    avatarImg.alt = "Bot Typing"; 
    avatarImg.classList.add('message-avatar');
    const bubbleWrapperDiv = document.createElement('div');
    bubbleWrapperDiv.classList.add('message-bubble-wrapper');
    const typingDotsDiv = document.createElement('div');
    typingDotsDiv.classList.add('typing-indicator'); 
    typingDotsDiv.innerHTML = `<span></span><span></span><span></span>`;
    bubbleWrapperDiv.appendChild(typingDotsDiv); 
    indicatorRow.appendChild(avatarImg);      
    indicatorRow.appendChild(bubbleWrapperDiv); 
    messagesContainerElement.appendChild(indicatorRow);
    scrollToBottom(messagesContainerElement);
}

export function removeTypingIndicator() { 
    const indicator = document.querySelector('.typing-indicator-row');
    if (indicator) { indicator.remove(); }
}