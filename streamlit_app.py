nimport streamlit as st

# app title
st.title("Chatbot App v0.1")

# Setup a session state message variable
if 'messages' not in st.session_state:
	st.session_state.messages = []

# Display all the historical messages
for message in st.session_state.messages:
	st.chat_message(message['role']).markdown(message['content'])

# Build a prompt input template
prompt = st.chat_input('Pass your prompt here')


if prompt:
	# Display the prompt
	st.chat_message('user').markdown(prompt)
	# Store the user prompt in state
	st.session_state.messages.append({'role':'user', 'content':prompt})
