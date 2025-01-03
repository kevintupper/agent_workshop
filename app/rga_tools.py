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

    Searches for documents on Regulations.gov based on the provided criteria. This tool allows filtering by various
    parameters such as agency, docket, document type, date ranges, and keywords. It retrieves metadata and data
    about documents, including their titles, IDs, types, and posting dates.

    For detailed information about the input parameters and usage examples,
    refer to the documentation in `docs/tools/get_documents.md`.

    Returns:
        Any: The JSON response from the API.
    """
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
# Tool: get_document_details
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
