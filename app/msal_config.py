# agent_workshop/app/msal_config.py

"""
msal_config.py

Simple container for environment-based MSAL settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


class MSALConfig:
    """
    MSALConfig reads environment variables for Azure AD auth flow.
    """

    AUTHORITY = os.getenv("MSAL_AUTHORITY", "https://login.microsoftonline.com/organizations")
    SCOPES = os.getenv("MSAL_SCOPES", "User.Read").split(",")
    REDIRECT_URI = os.getenv("MSAL_REDIRECT_URI", "http://localhost:8501")
    APP_CLIENT_ID = os.getenv("APP_CLIENT_ID", "")
    APP_CLIENT_SECRET = os.getenv("APP_CLIENT_SECRET", "")

    # Allowed tenants can be comma-separated in .env, e.g. "72f988bf-...,123..."
    ALLOWED_TENANTS = [t.strip() for t in os.getenv("ALLOWED_TENANTS", "").split(",") if t.strip()]
