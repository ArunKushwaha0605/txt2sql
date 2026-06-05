import streamlit as st

st.set_page_config(
    page_title="Text-to-SQL Chatbot", 
    layout="centered")
st.title("🗄️ Text-to-SQL AI Assistant")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! Ask me anything about your database."}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# React to user input
if user_query := st.chat_input("Ask a question about the data..."):
    
    # 1. Display user message in chat message container (Appears on the RIGHT)
    with st.chat_message("user"):
        st.write(user_query)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # 2. Generate placeholder/response for the assistant
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        
        # --- Logic for Text-to-SQL will go here ---
        # 1. Generate SQL from user_query
        # 2. Run SQL against database
        # 3. Format result
        assistant_response = "This is a placeholder response. Soon, I will display your SQL query results here."
        
        response_placeholder.write(assistant_response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})