import time

import streamlit as st

USER_ROLE_NAME = "User"
AGENT_ROLE_NAME = "Assistant"
STREAM_OUTPUT = True


# Streamed response emulator
def response_generator():
    """A meaningless response generator, counting from 0 to 9."""
    for i in range(10):
        yield f"{i}" + " "
        time.sleep(0.05)


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
            # Option 1: Stream output
            stream = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            response = st.write_stream(response_generator())
        else:
            # Option 2: Dump the whole response
            response = "".join(response_generator())
            # Display assistant response in chat message container
            st.markdown(response)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": AGENT_ROLE_NAME, "content": response})
