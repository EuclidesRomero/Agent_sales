const API_URL = 'http://localhost:8000/chat';
const BUSINESS_ID = 1;
const PHONE_NUMBER = '+1234567890';

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

function addMessage(content, type = 'system', isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    if (isError) {
        messageDiv.classList.add('error');
    }
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function setLoading(isLoading) {
    sendButton.disabled = isLoading;
    sendButton.textContent = isLoading ? 'Enviando...' : 'Enviar';
    messageInput.disabled = isLoading;
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    messageInput.value = '';
    setLoading(true);

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                business_id: BUSINESS_ID,
                phone_number: PHONE_NUMBER
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        if (data.response) {
            let messageText = data.response;
            
            // Agregar información de debug
            if (data.intent) {
                messageText += `\n\n[Intent: ${data.intent.name || data.intent}]`;
            }
            if (data.last_product_discussed) {
                messageText += `\n[Producto: ${data.last_product_discussed.name || data.last_product_discussed}]`;
            }
            
            addMessage(messageText, 'system');
        } else {
            addMessage('No se recibió respuesta del servidor', 'system', true);
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage(`Error: ${error.message}`, 'system', true);
    } finally {
        setLoading(false);
        messageInput.focus();
    }
}

sendButton.addEventListener('click', sendMessage);

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

messageInput.focus();