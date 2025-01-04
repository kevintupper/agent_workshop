# agent_workshop/app/auth_service.py

"""
auth_service.py

Handles user authentication via MSAL for Streamlit.
"""

import msal
import requests
import jwt
import streamlit as st
from typing import Optional, Dict, Any
from msal_config import MSALConfig


class AuthService:
    """
    AuthService manages the MSAL (Azure AD) authentication flow in a Streamlit context:
      - Build an authorization URL
      - Exchange auth code for token
      - Decode token to get tenant info
      - Optionally call Microsoft Graph for user profile
      - Enforce allowed tenants from MSALConfig
    """

    def __init__(self):
        # Create MSAL client app using credentials from msal_config
        self._app = msal.ConfidentialClientApplication(
            client_id=MSALConfig.APP_CLIENT_ID,
            authority=MSALConfig.AUTHORITY,
            client_credential=MSALConfig.APP_CLIENT_SECRET
        )

    def build_auth_url(self) -> str:
        """
        Create the authorization URL for user sign-in.
        """
        return self._app.get_authorization_request_url(
            scopes=MSALConfig.SCOPES,
            redirect_uri=MSALConfig.REDIRECT_URI
        )

    def exchange_code_for_token(self, code: str) -> Optional[str]:
        """
        Exchange the authorization code for an access token via MSAL.
        Returns the token or None if unsuccessful.
        """
        try:
            result = self._app.acquire_token_by_authorization_code(
                code=code,
                scopes=MSALConfig.SCOPES,
                redirect_uri=MSALConfig.REDIRECT_URI
            )
            if "access_token" in result:
                return result["access_token"]
            # If there's an error, MSAL sometimes puts an 'error_description' in result
            st.error(result.get("error_description", "MSAL code exchange failed."))
        except Exception as ex:
            st.error(f"Exception during token exchange: {ex}")
        return None

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decodes a JWT token (unverified). Returns the payload or None on error.
        """
        try:
            header = jwt.get_unverified_header(token)
            alg = header["alg"]
            decoded = jwt.decode(token, algorithms=[alg], options={"verify_signature": False})
            return decoded
        except Exception as ex:
            st.error(f"Error decoding token: {ex}")
            return None

    def get_tenant_id_from_token(self, access_token: str) -> Optional[str]:
        """
        Extract 'tid' (tenant id) from the unverified access token payload.
        """
        payload = self.decode_token(access_token)
        if payload:
            return payload.get("tid")
        return None

    def is_allowed_tenant(self, tenant_id: str) -> bool:
        """
        Check if tenant_id is in our MSALConfig.ALLOWED_TENANTS list.
        """
        return tenant_id in MSALConfig.ALLOWED_TENANTS

    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Fetch the user's profile from Microsoft Graph /me endpoint.
        Returns a dict with user data or None if error.
        """
        try:
            headers = {"Authorization": f"Bearer {access_token}"}
            resp = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
            if resp.status_code == 200:
                return resp.json()
            else:
                st.error(f"Failed to fetch user info: {resp.text}")
        except Exception as ex:
            st.error(f"Error requesting Graph /me: {ex}")
        return None
