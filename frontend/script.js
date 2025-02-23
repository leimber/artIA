document.addEventListener('DOMContentLoaded', () => {
    const messagesContainer = document.getElementById('chat-messages');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Función para añadir un mensaje al chat
    function addMessage(text, isUser, emotion = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        let messageContent = `<div class="message-text">${text}</div>`;
        
        if (emotion) {
            messageContent += `
                <div class="emotion-tag">
                    Emoción detectada: ${Object.keys(emotion).join(', ')}
                </div>
            `;
        }
        
        messageDiv.innerHTML = messageContent;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Función para manejar el envío de mensajes
    async function handleSendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Deshabilitar input mientras se procesa
        messageInput.disabled = true;
        sendButton.disabled = true;

        // Mostrar el mensaje del usuario
        addMessage(message, true);
        messageInput.value = '';

        try {
            const response = await fetch('http://localhost:8001/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query: message })
            });

            const data = await response.json();
            
            // Añadir pequeña pausa para que parezca más natural
            setTimeout(() => {
                addMessage(data.response, false, data.emotions);
            }, 500);

        } catch (error) {
            console.error('Error:', error);
            addMessage('Lo siento, ha ocurrido un error. ¿Podrías intentarlo de nuevo?', false);
        } finally {
            // Rehabilitar input
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', handleSendMessage);
    
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            handleSendMessage();
        }
    });

    // Mensaje de bienvenida
    setTimeout(() => {
        addMessage('¡Hola! Soy ArtIA, tu asistente de bienestar. ¿Cómo te sientes hoy? 🌟', false);
    }, 500);
});