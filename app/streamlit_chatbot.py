# agent_workshop/app/streamlit_chatbot.py

"""
streamlit_chatbot.py

A Streamlit-based chatbot UI that enforces MSAL login, then uses the same multi-agent
chatbot logic as the console and Gradio examples, now with streaming support.
"""
import os
import sys


# Add the parent directory of 'app' and 'swarm' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from auth_service import AuthService
from swarm import Swarm
from msal_config import MSALConfig
import dotenv

# Import the main agent
from agents import triage_agent, documents_agent, comments_agent, dockets_agent

# Import for Azure OpenAI
from openai import AzureOpenAI

# Load the .env file
dotenv.load_dotenv()

# Add the parent directory of 'app' and 'swarm' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Initialize the Azure OpenAI client and Swarm client
aoai_client = AzureOpenAI(
    api_key=os.getenv("AOAI_KEY"),
    api_version="2024-10-01-preview",
    azure_endpoint=os.getenv("AOAI_ENDPOINT")
)

swarm_client = Swarm(client=aoai_client)

# Map agent names to agent objects
agent_map = {
    "Triage Agent": triage_agent,
    "Documents Agent": documents_agent,
    "Comments Agent": comments_agent,
    "Dockets Agent": dockets_agent,
}


def main():
    st.set_page_config(page_title="Agentic Chat with the Regulations.gov", layout="wide")
    st.markdown("### Agentic Chat with the Regulations.gov")

    # Check if user is authenticated
    if not is_user_authenticated():
        return  # If not, user sees sign-in link or error.

    # If we get here, user has a valid token + user info
    user_info = st.session_state.get("USER_INFO", {})
    st.write(f"Welcome, **{user_info.get('displayName', 'User')}**!")
    st.markdown("---")

    # Show a minimal text-based chat interface
    # or call your existing run_chatbot_loop / triage_agent code.
    display_chat_interface()

# Authentication check
def is_user_authenticated():
    """
    Checks if the user is authenticated using AuthService.
    If not authenticated, displays a sign-in button or warning.
    """
    service = AuthService()

    # 1. Do we already have token + user in session?
    if "ACCESS_TOKEN" in st.session_state and "USER_INFO" in st.session_state:
        return True

    # 2. Check if we have ?code= from MSAL redirect
    query_params = st.experimental_get_query_params()
    if "code" in query_params:
        code_value = query_params["code"][0]
        # Exchange code for token
        token = service.exchange_code_for_token(code_value)
        st.experimental_set_query_params()  # Clear the code param from the URL
        if token:
            # Check tenant
            tid = service.get_tenant_id_from_token(token)
            if tid and service.is_allowed_tenant(tid):
                # Grab user info from Graph
                info = service.get_user_info(token)
                if info:
                    st.session_state["ACCESS_TOKEN"] = token
                    st.session_state["USER_INFO"] = info
                    return True
                else:
                    st.error("Failed to retrieve user profile from Graph.")
            else:
                st.error("Tenant not allowed or not found in token.")
        else:
            st.error("Code exchange failed for unknown reasons.")
        return False

    # 3. If we have no token and no code => prompt sign-in
    st.info("Please sign in with your Azure AD account.")
    sign_in_url = service.build_auth_url()
    st.markdown(f"[Click here to Sign In]({sign_in_url})")
    return False


def display_chat_interface():
    """
    A Streamlit-based chat interface that uses the multi-agent chatbot logic.
    """

    # Initialize session state for chat
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "tools_called" not in st.session_state:
        st.session_state["tools_called"] = []
    if "internal_chatter" not in st.session_state:
        st.session_state["internal_chatter"] = []
    if "agent_name" not in st.session_state:
        st.session_state["agent_name"] = "Triage Agent"

    # Set the chat mode configuration
    streaming = True
    capture_tools_called = True
    capture_internal_chatter = True
    tool_and_chatter_holder = None

    # Chat interface
    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if user_input := st.chat_input("Type your message here..."):

        # Display user message
        st.session_state["messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get the current agent
        agent = agent_map.get(st.session_state["agent_name"], triage_agent)

        # Display assistant response (streaming)
        with st.chat_message("assistant"):

            # Call the Swarm API with streaming enabled
            response = swarm_client.run(
                agent=agent,
                messages=st.session_state["messages"],
                context_variables={},
                stream=streaming,  # Enable streaming
                debug=False,
                capture_tools_called=capture_tools_called,
                capture_internal_chatter=capture_internal_chatter,
            )

            # Create a container for the streaming response
            response_container = st.empty()

            # Handle streaming response
            if streaming:
                content = ""
                last_sender = ""

                # Process the streaming response
                for chunk in response:

                    # Update the last sender
                    if "sender" in chunk:
                        last_sender = chunk["sender"]

                    # Process the content
                    if "content" in chunk and chunk["content"] is not None:
                        # If the content is empty and there is a last sender, clear the last sender
                        if not content and last_sender:
                            last_sender = ""
                        # Append the content to the content variable
                        content += chunk["content"]
                        # Update the response container with the content
                        response_container.markdown(content)

                    # If the tool calls show the status of them being called.
                    if "tool_calls" in chunk and chunk["tool_calls"] is not None:
                        for tool_call in chunk["tool_calls"]:
                            f = tool_call["function"]
                            name = f["name"]
                            if not name:
                                continue
                            response_container.markdown(f"{last_sender}: {name}")

                    # If the delimiter is end and the content is not empty, add the content to the session state
                    if "delim" in chunk and chunk["delim"] == "end" and content:
                        st.session_state["messages"].append({"role": "assistant", "content": content})
                        content = ""

                    # If the response is in the chunk, hold it for later processing
                    if "response" in chunk:
                        tool_and_chatter_holder = chunk["response"]

            else:
                # If not streaming handle another way
                st.markdown(response.messages[-1]["content"])  
                st.session_state["messages"].extend(response.messages)

        # Process tools_called and internal_chatter after streaming is complete
        if capture_tools_called:
            st.session_state["tools_called"].extend(tool_and_chatter_holder.tools_called)
        if capture_internal_chatter:
            st.session_state["internal_chatter"].extend(tool_and_chatter_holder.internal_chatter)

    # Debug information
    with st.expander("Debug Information"):
        display_debug_info()

# Debug information display
def display_debug_info():
    """
    Displays debug information such as tools called and internal chatter.
    """
    st.subheader("Tools Called")
    if st.session_state.get("tools_called"):
        for tool in st.session_state["tools_called"]:
            st.write(f"- **Tool**: {tool['tool_name']}, **Arguments**: {tool['arguments']}")
    else:
        st.write("No tools called yet.")

    st.subheader("Internal Chatter")
    if st.session_state.get("internal_chatter"):
        for message in st.session_state["internal_chatter"]:
            st.write(f"- {message}")
    else:
        st.write("No internal chatter yet.")

if __name__ == "__main__":
    main()