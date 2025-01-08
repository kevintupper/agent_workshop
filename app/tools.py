##########################################################################################
# tools.py
#
# This script contains all the tools and utility functions used by the agents in the
# regulations.gov chatbot. These tools include API wrappers, helper functions,
# and transfer functions for routing queries between agents.
#
# Tools:
#   1. **Transfer Functions**: Functions to transfer queries to specialized agents.
#   2. **Utility Functions**: Functions to get agency ID and PDF content.
#
# Usage:
#   - Import the desired tools into the agents or chatbot scripts as needed.
#   - Use the transfer functions to route queries between agents.
#
##########################################################################################

# Import necessary libraries
import json
import os
import requests
from markitdown import MarkItDown

##########################################################################################
# Transfer Functions
##########################################################################################

def transfer_to_documents():
    """
    Transfer the conversation to the Documents Agent.
    """
    from agents import documents_agent  # Local import to avoid circular dependency
    return documents_agent


def transfer_to_comments():
    """
    Transfer the conversation to the Comments Agent.
    """
    from agents import comments_agent  # Local import to avoid circular dependency
    return comments_agent


def transfer_to_dockets():
    """
    Transfer the conversation to the Dockets Agent.
    """
    from agents import dockets_agent  # Local import to avoid circular dependency
    return dockets_agent


def transfer_back_to_triage():
    """
    Transfer the conversation back to the Triage Agent.
    """
    from agents import triage_agent  # Local import to avoid circular dependency
    return triage_agent

##########################################################################################
# Utility Functions / Tools
##########################################################################################


def get_agency_id():
    """
    Retrieves a json array with each agencyID (ID) and the agency.

    Use this tool when you need to get the agency ID for filtering documents.
    """
    with open('data/agency.json', 'r', encoding='utf-8') as file:
        agency_list = json.load(file)
    return agency_list


def get_pdf_content(pdf_url: str) -> str:
    """
    Retrieves the content of a PDF file from a given URL, converts it to Markdown using the MarkItDown library,
    and returns the Markdown content.

    Args:
        pdf_url (str): The URL of the PDF file to be converted.

    Returns:
        str: The Markdown content of the PDF file.
    """
    # Step 1: Download the PDF file from the provided URL
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download PDF from {pdf_url}. Status code: {response.status_code}")

    # Save the PDF temporarily
    temp_pdf_path = "temp_downloaded_file.pdf"
    with open(temp_pdf_path, "wb") as pdf_file:
        pdf_file.write(response.content)

    # Step 2: Convert the PDF to Markdown using MarkItDown
    try:
        md = MarkItDown()
        result = md.convert(temp_pdf_path)
        markdown_content = result.text_content
    except Exception as e:
        raise Exception(f"Failed to convert PDF to Markdown: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_pdf_path):
            os.remove(temp_pdf_path)

    # Step 3: Return the Markdown content
    return markdown_content
