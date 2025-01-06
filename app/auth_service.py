# File: app/services/auth_service.py

"""
AuthService Module

This module provides authentication and authorization functionality for the application.
It handles user authentication via Microsoft Azure AD, token management, and tenant-based access control.

Key Features:
- User authentication with Microsoft Azure AD
- Token management and decoding
- Tenant-based access control
- User information retrieval from Microsoft Graph API

Classes:
    AuthService: Manages authentication and authorization processes.

Dependencies:
    - msal: Microsoft Authentication Library for Python
    - requests: HTTP library for making API calls
    - jwt: JSON Web Token implementation
    - app.utils.debug_logger: Custom debug logging utility
"""

# Imports for authentication
import msal
import requests
import jwt
from typing import Dict, Any, Optional

# Import debug logger
from app.utils.debug_logger import debug_logger



#***********************************************************************************************
# AuthService Class
#***********************************************************************************************
class AuthService:
    """
    AuthService class for managing authentication and authorization.

    This service handles user authentication, token management, and tenant-based access control.
    It interacts with Microsoft Azure AD for authentication and Microsoft Graph API for user information.

    Attributes:
        _app (msal.ConfidentialClientApplication): MSAL client application instance.
        _current_user (dict): Information about the currently authenticated user.
    """

    def __init__(self, config):
        """
        Initialize the AuthService.

        Args:
            config (ConfigModel): The application configuration.
        """
        self._logger = debug_logger
        self._config = config
        self._app = msal.ConfidentialClientApplication(
            client_id=self._config.APP_CLIENT_ID,
            authority=self._config.MSAL_AUTHORITY,
            client_credential=self._config.APP_CLIENT_SECRET
        )
        self._current_user = None
        self._logger.debug("AuthService initialized with MSAL client application")

    def get_auth_url(self) -> str:
        """
        Generate the authorization URL for user sign-in.

        Returns:
            str: The authorization URL for the user to initiate the sign-in process.
        """
        auth_url = self._app.get_authorization_request_url(
            scopes=self._config.MSAL_SCOPES,
            redirect_uri=self._config.MSAL_REDIRECT_URI
        )
        self._logger.debug(f"Generated auth URL: {auth_url}")
        return auth_url

    def authenticate_user(self, auth_code: str) -> bool:
        """
        Authenticate a user with the given authorization code.

        This method performs the following steps:
        1. Obtains an access token using the authorization code.
        2. Extracts the tenant ID from the token.
        3. Checks if the tenant is allowed.
        4. If allowed, retrieves the user information.

        Args:
            auth_code (str): The authorization code received after user sign-in.

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        token = self.get_token_from_code(auth_code)
        if token:
            tenant_id = self.get_tenant_id_from_token(token)
            if self.is_allowed_tenant(tenant_id):
                user_info = self.get_user_info(token)
                if user_info:
                    self._current_user = user_info
                    self._current_user['tenant_id'] = tenant_id
                    return True
            else:
                self._logger.warning(f"User from tenant {tenant_id} attempted to log in. Access denied.")
        return False

    def get_token_from_code(self, auth_code: str) -> Optional[str]:
        """
        Retrieve an access token using the authorization code.

        Args:
            auth_code (str): The authorization code received after user sign-in.

        Returns:
            str: The access token if successful, None otherwise.
        """
        try:
            result = self._app.acquire_token_by_authorization_code(
                auth_code,
                scopes=self._config.MSAL_SCOPES,
                redirect_uri=self._config.MSAL_REDIRECT_URI
            )
            return result.get("access_token")
        except Exception as err:
            self._logger.error(f"Error getting token from code: {err}")
            return None

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Decode a JWT token without verifying the signature.

        Args:
            token (str): The JWT token to decode.

        Returns:
            dict: The decoded token claims if successful, None otherwise.
        """
        try:
            algorithm = jwt.get_unverified_header(token)['alg']
            decoded_token = jwt.decode(
                token,
                algorithms=[algorithm],
                options={"verify_signature": False}
            )
            return decoded_token
        except Exception as e:
            self._logger.error(f"Error decoding token: {e}")
            return None

    def get_tenant_id_from_token(self, access_token: str) -> Optional[str]:
        """
        Extract the tenant ID from an access token.

        Args:
            access_token (str): The access token to extract the tenant ID from.

        Returns:
            str: The tenant ID if successful, None otherwise.
        """
        try:
            decoded_token = self.decode_token(access_token)
            return decoded_token['tid']
        except Exception as e:
            self._logger.error(f"Error extracting tenant ID from token: {e}")
            return None

    def is_allowed_tenant(self, tenant_id: str) -> bool:
        """
        Check if a given tenant ID is in the list of allowed tenants.

        Args:
            tenant_id (str): The tenant ID to check.

        Returns:
            bool: True if the tenant is allowed, False otherwise.
        """
        allowed_tenants = self._config.ALLOWED_TENANTS
        return tenant_id in allowed_tenants

    def get_user_info(self, access_token: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve user information from the Microsoft Graph API.

        Args:
            access_token (str): The access token to use for authentication.

        Returns:
            dict: User information if successful, None otherwise.
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            self._logger.error(f"Error fetching user info: {response.text}")
            return None

    def is_authenticated(self) -> bool:
        """
        Check if a user is currently authenticated.

        Returns:
            bool: True if a user is authenticated, False otherwise.
        """
        return self._current_user is not None

    def get_current_user(self) -> Dict[str, Any]:
        """
        Get the current authenticated user's information.

        Returns:
            dict: The current user's information if authenticated, None otherwise.
        """
        return self._current_user

    def logout(self) -> None:
        """
        Log out the current user by clearing the user information.
        """
        self._current_user = None
