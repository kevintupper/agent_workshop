##########################################################################################
# rga_tools.py
#
# This module provides a set of tools (functions) that wrap around the Regulations.gov
# API client (`RegulationsGovAPI`) to enable easy interaction with the API.
#
# These tools are designed to be used by agents or other systems, such as chatbots, to
# perform tasks like searching for documents, retrieving dockets, and more.
#
# Each tool is a standalone function that:
# - Accepts parameters for filtering, sorting, and pagination.
# - Calls the corresponding method in the `RegulationsGovAPI` client.
# - Returns a user-friendly response or the raw JSON data from the API.
#
# We also include some generic helper tools for common tasks like saving to file,
# printing to console, getting the current date, etc.
#
# ----------------------------------------
# Key Features:
# ----------------------------------------
# 1. Tools for:
#    - Searching and retrieving documents
#    - Retrieving details for a single document
#    - Searching and retrieving dockets
#    - Retrieving details for a single docket
#
# 2. Graceful error handling:
#    - Returns user-friendly error messages in case of API failures.
#
# 3. Extensible:
#    - New tools can be added easily by following the same pattern.
#
# ----------------------------------------
# Usage Example:
# ----------------------------------------
# from rga_wrapper import RegulationsGovAPI
# from rga_tools import find_documents
#
# api = RegulationsGovAPI(api_key="YOUR_API_KEY")
# response = find_documents(api, searchTerm="water")
# print(response)
#
##########################################################################################

from typing import Optional, Any
from rga_client_instance import rga_client  # Import the shared rga_client instance
import datetime
import json
import requests
from markitdown import MarkItDown
import os

##########################################################################################
# Helper tools
##########################################################################################

def get_current_date():
    """
    Get the current date in the format yyyy-MM-dd. 

    Use this tool when you need to get the current date for handling temporal filters.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")

def get_agency_id():
    """
    Retrieves a json array with each agencyID (ID) and the agency.

    Use this tool when you need to get the agency ID for filtering documents.
    """
    with open('data/agency.json', 'r') as file:
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




##########################################################################################
# Tool: get_documents
#
# This tool wraps the `get_documents` method from the `RegulationsGovAPI` class.
# It takes user-provided filters as input, calls the API, and returns the full JSON
# response from the API.
##########################################################################################

def get_documents(
    agencyId: Optional[str] = None,
    commentEndDate: Optional[str] = None,
    docketId: Optional[str] = None,
    documentType: Optional[str] = None,
    frDocNum: Optional[str] = None,
    searchTerm: Optional[str] = None,
    postedDate: Optional[str] = None,
    postedDateGe: Optional[str] = None,
    postedDateLe: Optional[str] = None,
    lastModifiedDate: Optional[str] = None,
    lastModifiedDateGe: Optional[str] = None,
    lastModifiedDateLe: Optional[str] = None,
    subtype: Optional[str] = None,
    withinCommentPeriod: Optional[bool] = None,
    sort: Optional[str] = None,
    pageNumber: Optional[int] = 1,
    pageSize: Optional[int] = 5,
) -> Any:
    """
    Tool: `get_documents`

    Find documents on Regulations.gov based on provided filter such as search term, agency, docket ID, 
    posted date, and more.

    It retrieves metadata and data about documents, including their titles, IDs, types, and posting dates.

    It also retrieves aggegated metadata about the full set of documents that match the filters, even 
    those not returned in the page.

    For detailed information about the input parameters and usage examples, refer to the documentation 
    in `docs/tools/get_documents.md`.

    Returns:
        Any: The JSON response from the API.
    """

    # Convert pageNumber and pageSize to integers
    try:
        pageNumber = int(pageNumber)
        pageSize = int(pageSize)
    except ValueError:
        raise ValueError("pageNumber and pageSize must be integers")
    
    # Ensure the pageNumber and pageSize are within the allowed range by adjusting them if necessary
    if pageNumber < 1:
        pageNumber = 1
    if pageNumber > 20:
        pageNumber = 20
    if pageSize < 5:
        pageSize = 5
    elif pageSize > 250:
        pageSize = 250


    # Ensure the sort field is valid (include descending sort)
    if sort:
        if sort not in ['documentId', '-documentId', 'title', '-title', 'postedDate', '-postedDate', 'lastModifiedDate', '-lastModifiedDate','commentEndDate', '-commentEndDate']:
            sort = 'postedDate'


    return rga_client.get_documents(
        agencyId=agencyId,
        commentEndDate=commentEndDate,
        docketId=docketId,
        documentType=documentType,
        frDocNum=frDocNum,
        searchTerm=searchTerm,
        postedDate=postedDate,
        postedDateGe=postedDateGe,
        postedDateLe=postedDateLe,
        lastModifiedDate=lastModifiedDate,
        lastModifiedDateGe=lastModifiedDateGe,
        lastModifiedDateLe=lastModifiedDateLe,
        subtype=subtype,
        withinCommentPeriod=withinCommentPeriod,
        sort=sort,
        pageNumber=pageNumber,
        pageSize=pageSize,
    )

##########################################################################################
# Tool: get_document_detailsw
##########################################################################################

def get_document_details(document_id: str, include_attachments: Optional[bool] = False) -> Any:
    """
    Retrieves detailed information for a specific document.

    For detailed information about the input parameters and usage examples,
    refer to the documentation in `docs/tools/get_document_details.md`.

    Returns:
        Any: The JSON response from the API.
    """
    return rga_client.get_document_details(document_id, include_attachments)
