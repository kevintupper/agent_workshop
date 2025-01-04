# agent_workshop/app/streamlit_chatbot.py

"""
streamlit_chatbot.py

A Streamlit-based chatbot UI that enforces MSAL login, then uses the same agent
that chatbot.py references.
"""

import streamlit as st
from auth_service import AuthService
from msal_config import MSALConfig

# Example: If your console chatbot is in "chatbot.py" with a function run_chatbot_loop,
# you might import it like:
#
# from .chatbot import run_chatbot_loop
#   or if your agent code is in a different file:
# from .agents import triage_agent

def main():
    st.title("Secure Streamlit Chatbot Demo (MSAL Login)")

    # Check if user is authenticated
    if not is_user_authenticated():
        return  # If not, user sees sign-in link or error.

    # If we get here, user has a valid token + user info
    user_info = st.session_state.get("USER_INFO", {})
    st.write(f"Welcome, **{user_info.get('displayName', 'User')}**!")
    st.markdown("---")

    # Show a minimal text-based chat interface
    # or call your existing run_chatbot_loop / triage_agent code.
    display_simple_chat()


def is_user_authenticated() -> bool:
    """
    Orchestrates the MSAL sign-in flow in Streamlit.
    Checks st.session_state for tokens, or attempts code exchange.
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


def display_simple_chat():
    """
    A minimal chat interface. In a real scenario, you might run your same agent logic 
    that the console-based chatbot uses. This is just a placeholder.
    """
    user_input = st.text_input("Enter your question:")
    if st.button("Send"):
        if user_input.strip():
            st.write(f"**User**: {user_input}")
            # Here you'd call triage_agent or run_chatbot_loop or similar:
            # response = triage_agent(user_input)
            # st.write(f"**Agent**: {response}")
            st.write("**Agent**: [Placeholder response from your agent here]")
        else:
            st.warning("Please enter something first.")


if __name__ == "__main__":
    main()
