import streamlit as st
from backend import MultilingualChatbot
from voice import speak, listen, stop_speaking
from gesture_face import detect_gesture
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="LinguaBot",
    layout="wide"
)

# ---------------- SESSION ----------------
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "current_chat" not in st.session_state:

    chat_id = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    st.session_state.current_chat = chat_id

    st.session_state.all_chats[chat_id] = []

if "chatbot" not in st.session_state:
    st.session_state.chatbot = MultilingualChatbot()

# ---------------- SIDEBAR ----------------
with st.sidebar:

    st.title("💬 Chat History")

    # NEW CHAT
    if st.button("➕ New Chat"):

        chat_id = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        st.session_state.current_chat = chat_id

        st.session_state.all_chats[chat_id] = []

        st.rerun()

    st.markdown("---")

    # OLD CHATS
    for chat_id in reversed(
        list(st.session_state.all_chats.keys())
    ):

        if st.button(chat_id):

            st.session_state.current_chat = chat_id

            st.rerun()

# ---------------- CURRENT CHAT ----------------
chat_data = st.session_state.all_chats[
    st.session_state.current_chat
]

# ---------------- UI ----------------
st.title("🤖 LinguaBot")
st.caption("Multilingual AI Assistant")

col1, col2, col3, col4 = st.columns([2,1,1,1])

with col1:

    language = st.selectbox(
        "🌐 Select Language",
        ["English", "Hindi", "Kannada"]
    )

with col2:

    voice_btn = st.button(
        "🎤 Speak",
        use_container_width=True
    )

with col3:

    camera_btn = st.button(
        "📷 Camera",
        use_container_width=True
    )

with col4:

    stop_btn = st.button(
        "🛑 Stop",
        use_container_width=True
    )

# ---------------- STOP SPEECH ----------------
if stop_btn:
    stop_speaking()

# ---------------- CHAT DISPLAY ----------------
for msg in chat_data:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ---------------- TEXT INPUT ----------------
if prompt := st.chat_input("Type your message..."):

    # STOP CURRENT SPEECH
    stop_speaking()

    # SAVE USER MESSAGE
    chat_data.append({
        "role": "user",
        "content": prompt
    })

    # AI RESPONSE
    response = st.session_state.chatbot.chat(
        prompt,
        language,
        chat_data[-6:]
    )

    # SAVE AI RESPONSE
    chat_data.append({
        "role": "assistant",
        "content": response
    })

    # SPEAK RESPONSE
    speak(response, language)

    st.rerun()

# ---------------- VOICE INPUT ----------------
if voice_btn:

    stop_speaking()

    st.info("🎤 Listening... Speak now")

    user_voice = listen()

    # STOP COMMAND
    if user_voice.lower() == "stop":

        stop_speaking()

        st.warning("Voice stopped")

    else:

        # SAVE USER VOICE
        chat_data.append({
            "role": "user",
            "content": user_voice
        })

        # AI RESPONSE
        response = st.session_state.chatbot.chat(
            user_voice,
            language,
            chat_data[-6:]
        )

        # SAVE RESPONSE
        chat_data.append({
            "role": "assistant",
            "content": response
        })

        # SPEAK RESPONSE
        speak(response, language)

    st.rerun()

# ---------------- CAMERA / GESTURE ----------------
if camera_btn:

    stop_speaking()

    st.info(
        "📷 Opening Camera... Press ESC to capture"
    )

    gesture = detect_gesture()

    # SAVE GESTURE
    chat_data.append({
        "role": "user",
        "content": f"[Gesture: {gesture}]"
    })

    # AI RESPONSE
    response = st.session_state.chatbot.chat(
        f"I am showing {gesture}",
        language,
        chat_data[-6:]
    )

    # SAVE RESPONSE
    chat_data.append({
        "role": "assistant",
        "content": response
    })

    # SPEAK RESPONSE
    speak(response, language)

    st.rerun()