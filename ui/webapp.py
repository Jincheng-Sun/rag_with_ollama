import streamlit as st
from ollama import chat

USER_ROLE_NAME = "user"
AGENT_ROLE_NAME = "assistant"
STREAM_OUTPUT = True
LLM_NAME = "phi3"
OLLAMA_BASE_URL = "localhost:11434"


# Streamed response emulator
def response_generator(messages):
    """Get response from a local Ollama model, in the future, change to API calls to remote models"""
    for chunk in chat(LLM_NAME, messages=messages, stream=True):
        yield chunk['message']['content']


st.title("FakeGPT")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": USER_ROLE_NAME, "content": prompt})
    # Display user message in chat message container
    with st.chat_message(USER_ROLE_NAME):
        st.markdown(prompt)
    # Display assistant response in chat message container
    with st.chat_message(AGENT_ROLE_NAME):
        if STREAM_OUTPUT is True:
            # Option 1: Streaming output
            response = st.write_stream(response_generator(st.session_state.messages))
        else:
            # Option 2: Dump the whole response
            response = "".join(response_generator(st.session_state.messages))
            # Display assistant response in chat message container
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": AGENT_ROLE_NAME, "content": response})
