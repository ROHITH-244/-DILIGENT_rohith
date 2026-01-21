import streamlit as st
import requests
import json

# Set up the Streamlit app
st.set_page_config(page_title="Jarvis AI Assistant", page_icon="🤖")
st.title("🤖 Jarvis AI Assistant")
st.caption("Powered by LLaMA, Pinecone, and RAG Technology")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Function to send request to backend API
def send_to_backend(query: str) -> str:
    """
    Send query to the backend API and return the response.
    
    Args:
        query (str): User query
        
    Returns:
        str: AI-generated response
    """
    try:
        response = requests.post(
            "http://localhost:8000/chat",
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "Sorry, I couldn't process that request.")
    except requests.exceptions.RequestException as e:
        return f"Error connecting to backend: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Chat input
if prompt := st.chat_input("Ask me anything..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking...")
        
        # Get response from backend
        response = send_to_backend(prompt)
        
        # Display final response
        message_placeholder.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})