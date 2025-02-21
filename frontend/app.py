import streamlit as st
import requests

# Configurar el backend
BACKEND_URL = "http://127.0.0.1:8001"


# Configurar la página con un diseño más atractivo y alegre
st.set_page_config(
    page_title="😊 Asistente de Bienestar",
    page_icon="💙",
    layout="wide",
)

# CSS para estilos mejorados con colores vivos y fuente moderna
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;700&display=swap');

        body {
            font-family: 'Nunito', sans-serif;
            background-color: #FDF8E6;
        }
        .chat-container {
            max-width: 700px;
            margin: auto;
            background: linear-gradient(to right, #FFB6C1, #FFD700);
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
            animation: fadeIn 1s ease-in-out;
        }
        .chat-box {
            max-height: 450px;
            overflow-y: auto;
            padding: 15px;
            background: #ffffff;
            border-radius: 15px;
            border: 2px solid #FF69B4;
        }
        .user-message {
            background: linear-gradient(135deg, #FF69B4, #FF1493);
            color: white;
            padding: 12px;
            border-radius: 15px;
            text-align: right;
            margin-bottom: 10px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.2);
            font-weight: 500;
        }
        .bot-message {
            background: linear-gradient(135deg, #FFD700, #FFA500);
            color: #333;
            padding: 12px;
            border-radius: 15px;
            text-align: left;
            margin-bottom: 10px;
            box-shadow: 0px 2px 8px rgba(0, 0, 0, 0.2);
            font-weight: 500;
        }
        .title {
            text-align: center;
            font-size: 32px;
            font-weight: bold;
            color: #FF4500;
            font-family: 'Nunito', sans-serif;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            color: #555;
        }
        .send-btn {
            background: linear-gradient(135deg, #32CD32, #00FF7F);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 18px;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: transform 0.2s ease-in-out;
            font-family: 'Nunito', sans-serif;
        }
        .send-btn:hover {
            transform: scale(1.1);
        }
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    </style>
""", unsafe_allow_html=True)

# Título y descripción con emojis animados
st.markdown("<h1 class='title'>😊 Asistente IA de Bienestar</h1>", unsafe_allow_html=True)
st.write("🌈 ¡Bienvenido! Escribe tu mensaje y nuestro asistente te ayudará con apoyo emocional. 💙")

# Inicializar historial de conversación en la sesión de Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Historial de conversación con estilo animado
chat_container = st.container()
with chat_container:
    st.markdown("<div class='chat-box'>", unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='chat-container user-message'>👤 {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-container bot-message'>🤖 {message['content']}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Campo de entrada del usuario con fondo animado
user_input = st.text_input("📝 Escribe tu mensaje aquí:")

# Botón con efecto de rebote
if st.button("💬 ¡Enviar Mensaje!", key="send_btn"):
    if user_input.strip():
        # Guardar mensaje del usuario en el historial
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            # Enviar la consulta al backend
            response = requests.post(f"{BACKEND_URL}/chat", params={"query": user_input})
            response.raise_for_status()
            data = response.json()

            chatbot_response = f"🤖 **Chatbot:** {data['response']} \n😊 **Emoción Detectada:** {data['emotion']}"

            # Guardar la respuesta del chatbot en el historial
            st.session_state.messages.append({"role": "bot", "content": chatbot_response})

        except requests.exceptions.RequestException as e:
            chatbot_response = f"❌ Error en la conexión con el backend: {e}"
            st.session_state.messages.append({"role": "bot", "content": chatbot_response})

        st.rerun()

# Pie de página 
st.markdown("<p class='footer'>🌟 Recuerda que siempre hay alguien para escucharte y que este chat no sustituye la ayuda psicológica profesional 💛</p>", unsafe_allow_html=True)
