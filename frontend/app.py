import streamlit as st
import requests

# Configurar la página
st.set_page_config(page_title="Asistente IA de Bienestar Emocional", page_icon="💬", layout="centered")

# Aplicar estilo personalizado con CSS
st.markdown("""
    <style>
        body {
            background-color: #f5f5f5;
        }
        .chat-container {
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: #dcf8c6;
            padding: 10px;
            border-radius: 10px;
            text-align: right;
        }
        .bot-message {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
        }
        .chat-history {
            height: 400px;
            overflow-y: auto;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 10px;
            background-color: #fff;
        }
    </style>
""", unsafe_allow_html=True)

# Título con icono
st.markdown("<h1 style='text-align: center;'>💬 Asistente IA de Bienestar Emocional</h1>", unsafe_allow_html=True)

# Inicializar historial de conversación en la sesión de Streamlit
if "messages" not in st.session_state:
    st.session_state.messages = []

# Contenedor del historial de chat
st.markdown("### 🗨️ Historial de Conversación")
chat_container = st.container()

with chat_container:
    st.markdown("<div class='chat-history'>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='chat-container user-message'>👤 {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-container bot-message'>🤖 {message['content']}</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Campo de entrada del usuario
user_input = st.text_input("📝 Escribe tu mensaje aquí:")

# Botón para enviar la consulta
if st.button("Enviar"):
    if user_input.strip():
        # Guardar mensaje del usuario en el historial
        st.session_state.messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post("http://127.0.0.1:8000/chat", params={"query": user_input})
            response.raise_for_status()  # Verifica si hay errores HTTP
            data = response.json()

            chatbot_response = f"🤖 **Chatbot:** {data['response']} \n😊 **Emoción Detectada:** {data['emotion']}"
            
            # Guardar respuesta del chatbot en el historial
            st.session_state.messages.append({"role": "bot", "content": chatbot_response})

        except requests.exceptions.RequestException as e:
            chatbot_response = f"❌ Error en la conexión con el backend: {e}"
            st.session_state.messages.append({"role": "bot", "content": chatbot_response})

        # Recargar la página para mostrar la conversación
        st.experimental_rerun()

# Pie de página
st.markdown("---")
st.markdown("<p style='text-align: center;'>📌 <i>Este chatbot no sustituye ayuda profesional en salud mental.</i></p>", unsafe_allow_html=True)
