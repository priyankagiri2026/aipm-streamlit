import streamlit as st

st.title("📱 Pokédex")
st.write("A minimal template for building a chat interface with Streamlit.")

# The message list has to survive reruns, so it lives in session_state.
if "messages" not in st.session_state:
    st.session_state.messages = []

if st.sidebar.button("Clear chat history"):
    st.session_state.messages = []

# Streamlit reruns the whole script on every interaction, so the past
# conversation has to be replayed from session_state on each run.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

prompt = st.chat_input("Ask me about a Pokémon")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Placeholder for a real model call: the reply just echoes the question.
    reply = f"You asked: {prompt}"
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)
