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
import json
from markitdown import MarkItDown


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
            sort = '-postedDate'

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

def get_document_details(document_id: str, include_attachments: Optional[bool] = True) -> Any:
    """
    Retrieves detailed information for a specific document.

    For detailed information about the input parameters and usage examples,
    refer to the documentation in `docs/tools/get_document_details.md`.

    Returns:
        Any: The JSON response from the API.
    """
    return rga_client.get_document_details(document_id, include_attachments)

##########################################################################################
# Tool: get_comments
#
# This tool wraps the `get_comments` method from the `RegulationsGovAPI` class.
# It takes user-provided filters as input, calls the API, and returns the full JSON
# response from the API.
##########################################################################################

def get_comments(
    agencyId: Optional[str] = None,
    searchTerm: Optional[str] = None,
    postedDate: Optional[str] = None,
    postedDateGe: Optional[str] = None,
    postedDateLe: Optional[str] = None,
    lastModifiedDate: Optional[str] = None,
    lastModifiedDateGe: Optional[str] = None,
    lastModifiedDateLe: Optional[str] = None,
    commentOnId: Optional[str] = None,
    sort: Optional[str] = None,
    pageNumber: Optional[int] = 1,
    pageSize: Optional[int] = 5,
) -> Any:
    """
    Tool: `get_comments`

    Retrieves a list of comments from Regulations.gov based on provided filters such as agency ID,
    search term, posted date, and more.

    For detailed information about the input parameters and usage examples, refer to the documentation
    in `docs/tools/get_comments.md`.

    Returns:
        Any: The JSON response from the API.
    """
    # Convert pageNumber and pageSize to integers
    try:
        pageNumber = int(pageNumber)
        pageSize = int(pageSize)
    except ValueError:
        raise ValueError("pageNumber and pageSize must be integers")

    # Ensure the pageNumber and pageSize are within the allowed range
    if pageNumber < 1:
        pageNumber = 1
    if pageSize < 5:
        pageSize = 5
    elif pageSize > 250:
        pageSize = 250

    # Ensure the sort field is valid
    if sort:
        if sort not in ['postedDate', '-postedDate', 'lastModifiedDate', '-lastModifiedDate']:
            sort = '-postedDate'

    return rga_client.get_comments(
        agencyId=agencyId,
        searchTerm=searchTerm,
        postedDate=postedDate,
        postedDateGe=postedDateGe,
        postedDateLe=postedDateLe,
        lastModifiedDate=lastModifiedDate,
        lastModifiedDateGe=lastModifiedDateGe,
        lastModifiedDateLe=lastModifiedDateLe,
        commentOnId=commentOnId,
        sort=sort,
        pageNumber=pageNumber,
        pageSize=pageSize,
    )


##########################################################################################
# Tool: get_comment_details
#
# This tool wraps the `get_comment_details` method from the `RegulationsGovAPI` class.
# It retrieves detailed information for a specific comment.
##########################################################################################

def get_comment_details(
    comment_id: str,
    include_attachments: Optional[bool] = False,
) -> Any:
    """
    Tool: `get_comment_details`

    Retrieves detailed information for a specific comment from Regulations.gov.

    For detailed information about the input parameters and usage examples, refer to the documentation
    in `docs/tools/get_comment_details.md`.

    Returns:
        Any: The JSON response from the API.
    """
    if not comment_id:
        raise ValueError("The 'comment_id' parameter is required and cannot be empty.")

    return rga_client.get_comment_details(
        comment_id=comment_id,
        include_attachments=include_attachments,
    )

##########################################################################################
# Tool: get_dockets
##########################################################################################

def get_dockets(
    agencyId: Optional[str] = None,
    searchTerm: Optional[str] = None,
    lastModifiedDate: Optional[str] = None,
    lastModifiedDateGe: Optional[str] = None,
    lastModifiedDateLe: Optional[str] = None,
    sort: Optional[str] = None,
    pageNumber: Optional[int] = 1,
    pageSize: Optional[int] = 5,
) -> Any:
    """
    Tool: `get_dockets`

    Retrieves a list of dockets from Regulations.gov based on provided filters such as agency ID,
    search term, last modified date, and more.

    For detailed information about the input parameters and usage examples, refer to the documentation
    in `docs/tools/get_dockets.md`.

    Returns:
        Any: The JSON response from the API.
    """
    # Convert pageNumber and pageSize to integers
    try:
        pageNumber = int(pageNumber)
        pageSize = int(pageSize)
    except ValueError:
        raise ValueError("pageNumber and pageSize must be integers")

    # Ensure the pageNumber and pageSize are within the allowed range
    if pageNumber < 1:
        pageNumber = 1
    if pageSize < 5:
        pageSize = 5
    elif pageSize > 250:
        pageSize = 250

    # Ensure the sort field is valid
    if sort:
        if sort not in ['docketId', '-docketId', 'title', '-title', 'lastModifiedDate', '-lastModifiedDate']:
            sort = '-lastModifiedDate'

    return rga_client.get_dockets(
        agencyId=agencyId,
        searchTerm=searchTerm,
        lastModifiedDate=lastModifiedDate,
        lastModifiedDateGe=lastModifiedDateGe,
        lastModifiedDateLe=lastModifiedDateLe,
        sort=sort,
        pageNumber=pageNumber,
        pageSize=pageSize,
    )


##########################################################################################
# Tool: get_docket_details
##########################################################################################

def get_docket_details(docketId: str) -> Any:
    """
    Tool: `get_docket_details`

    Retrieves detailed information for a specific docket.

    For detailed information about the input parameters and usage examples,
    refer to the documentation in `docs/tools/get_docket_details.md`.

    Returns:
        Any: The JSON response from the API.
    """
    if not docketId:
        raise ValueError("The 'docketId' parameter is required and cannot be empty.")

    return rga_client.get_docket_details(docketId)
