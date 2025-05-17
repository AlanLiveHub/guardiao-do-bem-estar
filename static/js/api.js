// static/js/api.js

export async function sendMessageToServer(messageText) {
    console.log("[api.js] Enviando mensagem para o servidor:", messageText);
    try {
        const response = await fetch('/send_message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: new URLSearchParams({ 'message': messageText })
        });
        
        const data = await response.json(); // Tenta parsear JSON mesmo se não for OK

        if (!response.ok) {
            console.error("[api.js] Erro do servidor:", response.status, data.error || data.message);
            // Retorna um objeto de erro padronizado que inclui o 'data' se disponível
            return { 
                ok: false, 
                status: response.status, 
                error: data.error || data.message || `Erro ${response.status}.`,
                data: data // Inclui o payload completo do erro se houver (ex: full_history_for_template)
            };
        }
        console.log("[api.js] Resposta recebida do servidor:", data);
        return { ok: true, data: data }; // Retorna um objeto padronizado para sucesso

    } catch (error) {
        console.error("[api.js] Falha na requisição fetch:", error);
        return { 
            ok: false, 
            error: "Erro de conexão. Verifique sua rede.", 
            details: error 
        };
    }
}