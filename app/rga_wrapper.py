"""
rga_wrapper.py

A Python wrapper for the Regulations.gov API (v4). This wrapper provides methods to interact with the API endpoints
for documents, comments, dockets, and comment submissions. It includes robust error handling, logging, and clear
documentation for ease of use by developers of all levels.

Author: [Your Name]
Date: [Date]
"""

import logging
import requests
from typing import Optional, Dict, Any

# Create a module-specific logger
logger = logging.getLogger(__name__)


class RegulationsGovAPI:
    """
    A wrapper for the Regulations.gov API (v4).

    Attributes:
        api_key (str): The API key for authenticating requests.
        base_url (str): The base URL for the Regulations.gov API.
    """

    def __init__(self, api_key: str, base_url: str = "https://api.regulations.gov/v4"):
        """
        Initializes the RegulationsGovAPI instance.

        Args:
            api_key (str): The API key for authenticating requests.
            base_url (str): The base URL for the Regulations.gov API. Defaults to the production endpoint.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/vnd.api+json"
        }
        logger.info("RegulationsGovAPI initialized with base URL: %s", self.base_url)


    def _handle_response(self, response: requests.Response) -> Any:
        """
        Handles the HTTP response, checking for errors and returning the JSON data if successful.

        Args:
            response (requests.Response): The HTTP response object.

        Returns:
            Any: The JSON data from the response.

        Raises:
            Exception: If the response contains an HTTP error.
        """
        try:
            response.raise_for_status()
            logger.debug("Request successful: %s", response.url)
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                logger.warning("Resource not found: %s", response.url)
                return {"error": "Resource not found", "status_code": 404}
            elif response.status_code == 500:
                logger.error("Server error: %s", response.url)
                return {"error": "Server error", "status_code": 500}
            else:
                logger.error("HTTP error occurred: %s - %s", response.status_code, response.text)
                raise http_err
        except Exception as err:
            logger.exception("An unexpected error occurred: %s", err)
            raise err


    def get_documents(
        self,
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
        Retrieves a list of documents based on the provided filters.

        For detailed information about the input parameters and usage examples,
        refer to the documentation in `docs/tools/get_documents.md`.

        Returns:
            Any: The JSON response from the API.
        """
        url = f"{self.base_url}/documents"
        params = {}

        # Map parameters to API query filters
        if agencyId:
            params["filter[agencyId]"] = agencyId
        if commentEndDate:
            params["filter[commentEndDate]"] = commentEndDate
        if docketId:
            params["filter[docketId]"] = docketId
        if documentType:
            params["filter[documentType]"] = documentType
        if frDocNum:
            params["filter[frDocNum]"] = frDocNum
        if searchTerm:
            params["filter[searchTerm]"] = searchTerm
        if postedDate:
            params["filter[postedDate]"] = postedDate
        if postedDateGe:
            params["filter[postedDate][ge]"] = postedDateGe
        if postedDateLe:
            params["filter[postedDate][le]"] = postedDateLe
        if lastModifiedDate:
            params["filter[lastModifiedDate]"] = lastModifiedDate
        if lastModifiedDateGe:
            params["filter[lastModifiedDate][ge]"] = lastModifiedDateGe
        if lastModifiedDateLe:
            params["filter[lastModifiedDate][le]"] = lastModifiedDateLe
        if subtype:
            params["filter[subtype]"] = subtype
        if withinCommentPeriod:
            params["filter[withinCommentPeriod]"] = str(withinCommentPeriod).lower()
        if sort:
            params["sort"] = sort

        # Convert pageNumber and pageSize to integers
        try:
            pageNumber = int(pageNumber)
            pageSize = int(pageSize)
        except ValueError:
            raise ValueError("pageNumber and pageSize must be integers")

        # Make sure pageNumber and pageSize are within the allowed range
        if not 1 <= pageNumber <= 20:
            raise ValueError("pageNumber must be between 1 and 20")
        if pageSize < 5:
            pageSize = 5
        elif pageSize > 250:
            pageSize = 250

        # Add pagination parameters
        params["page[number]"] = pageNumber
        params["page[size]"] = pageSize


        logger.info("Fetching documents with parameters: %s", params)
        response = requests.get(url, headers=self.headers, params=params)

        # Handle the response
        return self._handle_response(response)


    def get_document_details(
        self,
        document_id: str,
        include_attachments: Optional[bool] = False,
    ) -> Any:
        """
        Retrieves detailed information for a specific document.

        Args:
            document_id (str): The unique identifier of the document to retrieve.
            include_attachments (Optional[bool]): Whether to include attachments in the response. Defaults to False.

        Returns:
            Any: The JSON response from the API.

        Raises:
            ValueError: If the document_id is not provided or is empty.
            HTTPError: If the API request fails (e.g., 404 for document not found, 403 for invalid API key).
        """
        if not document_id:
            raise ValueError("The 'document_id' parameter is required and cannot be empty.")

        # Construct the URL for the document details endpoint
        url = f"{self.base_url}/documents/{document_id}"

        # Query parameters
        params = {}
        if include_attachments:
            params["include"] = "attachments"

        logger.info("Fetching details for document ID: %s with parameters: %s", document_id, params)

        # Make the GET request to the API
        response = requests.get(url, headers=self.headers, params=params)

        # Handle the response
        return self._handle_response(response)


    def get_comments(self, filters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Retrieves a list of comments based on the provided filters.

        Args:
            filters (Optional[Dict[str, Any]]): A dictionary of query parameters for filtering the results.

        Returns:
            Any: The JSON response from the API.
        """
        url = f"{self.base_url}/comments"
        params = filters if filters else {}
        logger.info("Fetching comments with filters: %s", params)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)
    

    def get_comment_details(self, comment_id: str) -> Any:
        """
        Retrieves detailed information for a specific comment.

        Args:
            comment_id (str): The ID of the comment to retrieve.

        Returns:
            Any: The JSON response from the API.
        """
        url = f"{self.base_url}/comments/{comment_id}"
        logger.info("Fetching details for comment ID: %s", comment_id)
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)


    def get_dockets(self, filters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Retrieves a list of dockets based on the provided filters.

        Args:
            filters (Optional[Dict[str, Any]]): A dictionary of query parameters for filtering the results.

        Returns:
            Any: The JSON response from the API.
        """
        url = f"{self.base_url}/dockets"
        params = filters if filters else {}
        logger.info("Fetching dockets with filters: %s", params)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)


    def get_docket_details(self, docket_id: str) -> Any:
        """
        Retrieves detailed information for a specific docket.

        Args:
            docket_id (str): The ID of the docket to retrieve.

        Returns:
            Any: The JSON response from the API.
        """
        url = f"{self.base_url}/dockets/{docket_id}"
        logger.info("Fetching details for docket ID: %s", docket_id)
        response = requests.get(url, headers=self.headers)
        return self._handle_response(response)


    def get_agency_categories(self, acronym: str) -> Any:
        """
        Retrieves a list of agency categories filtered by the provided acronym.

        Args:
            acronym (str): The agency acronym to filter categories (e.g., 'EPA').

        Returns:
            Any: The JSON response from the API.
        """
        url = f"{self.base_url}/agency-categories"
        params = {"filter[acronym]": acronym}
        logger.info("Fetching agency categories for acronym: %s", acronym)
        response = requests.get(url, headers=self.headers, params=params)
        return self._handle_response(response)

