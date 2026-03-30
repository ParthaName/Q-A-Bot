import streamlit as st
from qa_chain import init_llm, build_chain, convert_history, ask_stream
from config import MAX_CHAT_HISTORY, GROQ_API_KEY


st.set_page_config(page_title="AI Q&A", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    #MainMenu, footer {visibility: hidden;}
    .block-container {max-width: 720px; padding-top: 1.5rem;}
</style>
""", unsafe_allow_html=True)

# init session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chain" not in st.session_state:
    if not GROQ_API_KEY:
        st.error("GROQ_API_KEY not found. Please add it to your .env file.")
        st.stop()
    llm = init_llm()
    st.session_state.chain = build_chain(llm)


# sidebar
with st.sidebar:
    st.header("Settings")
    st.caption(f"Model: qwen3-32b")
    st.caption(f"Messages: {len(st.session_state.messages)}")
    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


# main chat area
st.title("AI Q&A Assistant")
st.caption("Ask me anything — I remember the conversation context.")
st.divider()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    past = st.session_state.messages[:-1][-MAX_CHAT_HISTORY:]
    history = convert_history(past)

    with st.chat_message("assistant"):
        try:
            reply = st.write_stream(ask_stream(st.session_state.chain, user_input, history))
            st.session_state.messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            st.error(f"Something went wrong: {e}")