# File: app/ui/auth_ui.py

"""
Authentication UI Module

This module provides functions for handling the authentication user interface
in the AzureFed.com presentation system. It includes functions for enforcing
authentication, displaying the sign-in screen, and showing user credentials.

The module interacts with the AuthService for authentication logic and the
SessionManager for managing user session data.

Functions:
    enforce_auth_or_display_sign_in: Main authentication flow handler
    display_sign_in_screen: Renders the sign-in UI
    display_credentials_screen: Shows authenticated user information

Dependencies:
    - streamlit: Used for creating the user interface
    - app.core.session_manager: Manages user session data
"""

import streamlit as st
from app.core.session_manager import SessionManager


def enforce_auth_or_display_sign_in(services) -> bool:
    """
    Enforce authentication by checking for a valid access token in the session state.
    
    Args:
        services (ServiceContainer): The container with all services.

    Returns:
        bool: True if authenticated, False otherwise.
    """
    if SessionManager.is_authenticated():
        return True
    
    query_params = st.query_params.to_dict()
    if "code" in query_params:
        return _handle_auth_code(services, query_params["code"])
    else:
        display_sign_in_screen(services.auth_service)

    # We should never get here, but just in case.
    return False

def _handle_auth_code(services, auth_code: str) -> bool:
    """
    Handle the authentication code received from the identity provider.

    Args:
        service_container (ServiceContainer): The container with all services.
        auth_code (str): The authentication code received from the identity provider.

    Returns:
        bool: True if authentication is successful, False otherwise.
    """

    # Get the services we need
    auth_service = services.auth_service
    allowed_tenants = services.config.ALLOWED_TENANTS

    # Get the access token
    access_token = auth_service.get_token_from_code(auth_code)
    st.query_params.clear()
    
    # Check if we got an access token
    if not access_token:
        st.error("Authentication failed.")
        return False

    # Check the tenant ID and make sure it is in the list of allowed tenants
    tenant_id = auth_service.get_tenant_id_from_token(access_token)
    if tenant_id not in allowed_tenants:
        display_invalid_tenant_screen(auth_service)
        return False

    # Get the user's information
    user_info = auth_service.get_user_info(access_token)
    if not user_info:
        st.error("Failed to retrieve user information.")
        return False

    # Initialize the session we are now authenticated successfully.
    SessionManager.initialize_session(services, access_token, user_info)
    return True

def display_sign_in_screen(auth_service) -> None:
    """
    Display the sign-in screen to the user.

    This function renders the UI elements for the sign-in screen, including
    the title, welcome message, and sign-in button.

    Args:
        auth_service (AuthService): The authentication service.
    """
    st.title("Microsoft")
    st.subheader("Azure Fed Demo Platform")
    st.write("Welcome to the Microsoft Azure Fed Demo Platform. Please sign in with an authorized account.")
    
    auth_url = auth_service.get_auth_url()
    st.markdown(
        f"""
        <a href='{auth_url}' target='_self'>
            <button style='background-color: teal; color: white; border: none; border-radius: 4px; padding: 8px 16px; font-size: 18px; cursor: pointer;'>
                Sign In
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

def display_credentials_screen() -> None:
    """
    Display the welcome message and user credentials once the user is authenticated.

    This function shows the authenticated user's information, including their
    display name, user info, access token, and session log info.
    """
    user_info = SessionManager.get_user_info()
    
    st.markdown(f"Welcome, {user_info['displayName']}!")

    st.markdown("**User Info:**")
    st.write(user_info)

def display_invalid_tenant_screen(auth_service) -> None:
    """
    Display a screen for users who have logged in with an invalid tenant.
    """
    st.title("Access Denied")
    st.error("Your account is not authorized to access this application.")
    st.write("This application is only available to specific Microsoft tenants.")
    st.write("If you believe this is an error, please contact your administrator.")
    
    st.write("You can try signing in with a different account:")
    auth_url = auth_service.get_auth_url()
    st.markdown(
        f"""
        <a href='{auth_url}' target='_self'>
            <button style='background-color: teal; color: white; border: none; border-radius: 4px; padding: 8px 16px; font-size: 18px; cursor: pointer;'>
                Sign In with a Different Account
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )
