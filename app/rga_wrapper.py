"""
rga_wrapper.py

A Python wrapper for the Regulations.gov API (v4). This wrapper provides methods to interact with the API endpoints
for documents, comments, and dockets. It includes robust error handling, logging, and clear documentation for 
ease of use by developers of all levels.
"""

# Import necessary libraries
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
            Any: The JSON data from the response or error details.

        Notes:
            - For HTTP errors (e.g., 404, 500), this method returns a dictionary with error details
              instead of raising exceptions. This design choice ensures that the calling code can
              handle errors gracefully without needing to catch exceptions.
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

        For detailed information about the input parameters and usage examples
        refer to https://open.gsa.gov/api/regulationsgov/.

        The instructions for the documents agent are in the instructions folder.

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
            
        # Add pagination parameters
        params["page[number]"] = pageNumber
        params["page[size]"] = pageSize

        logger.info("Fetching documents with parameters: %s", params)
        response = requests.get(url, headers=self.headers, params=params)


        # Handle the response
        try:
            # Handle the response and return the result
            return self._handle_response(response)
        except Exception as e:
            logger.error("Error handling response: %s", e)
            raise


    def get_document_details(
        self,
        document_id: str,
        include_attachments: Optional[bool] = True,
    ) -> Any:
        """
        Retrieves detailed information for a specific document.

        For detailed information about the input parameters and usage examples
        refer to https://open.gsa.gov/api/regulationsgov/.

        The instructions for the documents agent are in the instructions folder.

        Args:
            document_id (str): The unique identifier of the document to retrieve.
            include_attachments (Optional[bool]): Whether to include attachments in the response. Defaults to False.

        Returns:
            Any: The JSON response from the API.

        Raises:
            ValueError: If the document_id is not provided or is empty.
        """
        if not document_id:
            raise ValueError("The 'document_id' parameter is required and cannot be empty.")

        # Construct the URL for the document details endpoint
        url = f"{self.base_url}/documents/{document_id}"

        # Query parameters
        params = {}
        if include_attachments:
            params["include"] = "attachments"

        # Log the request details
        self._log_request("GET", url, params)

        # Make the GET request to the API
        response = requests.get(url, headers=self.headers, params=params)

        # Handle the response
        try:
            return self._handle_response(response)
        except Exception as e:
            logger.error("Error handling response for document ID %s: %s", document_id, e)
            raise


    def get_comments(
        self,
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
        Retrieves a list of comments based on the provided filters.

        Args:
            agencyId (Optional[str]): Filters results for the agency acronym.
            searchTerm (Optional[str]): Filters results on the given term.
            postedDate (Optional[str]): Filters results relative to the posted date.
            postedDateGe (Optional[str]): Filters results with posted date >= this value.
            postedDateLe (Optional[str]): Filters results with posted date <= this value.
            lastModifiedDate (Optional[str]): Filters results relative to the last modified date.
            lastModifiedDateGe (Optional[str]): Filters results with last modified date >= this value.
            lastModifiedDateLe (Optional[str]): Filters results with last modified date <= this value.
            commentOnId (Optional[str]): Filters results on the supplied commentOnId.
            sort (Optional[str]): Sorts the results by the specified field.
            pageNumber (Optional[int]): Specifies the page number of results to return.
            pageSize (Optional[int]): Specifies the size of results per page.

        Returns:
            Any: The JSON response from the API.
        """
        # Construct the URL for the comments endpoint
        url = f"{self.base_url}/comments"

        # Query parameters
        params = {}
        if agencyId:
            params["filter[agencyId]"] = agencyId
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
        if commentOnId:
            params["filter[commentOnId]"] = commentOnId
        if sort:
            params["sort"] = sort
        if pageNumber:
            params["page[number]"] = pageNumber
        if pageSize:
            params["page[size]"] = pageSize

        # Log the request details
        self._log_request("GET", url, params)

        # Make the GET request to the API
        response = requests.get(url, headers=self.headers, params=params)

        # Handle the response
        try:
            return self._handle_response(response)
        except Exception as e:
            logger.error("Error handling response for comments: %s", e)
            raise
    

    def get_comment_details(
        self,
        comment_id: str,
        include_attachments: Optional[bool] = True,
    ) -> Any:
        """
        Retrieves detailed information for a specific comment.

        Args:
            comment_id (str): The ID of the comment to retrieve.
            include_attachments (Optional[bool]): Whether to include attachments in the response. Defaults to False.

        Returns:
            Any: The JSON response from the API.

        Raises:
            ValueError: If the comment_id is not provided or is empty.
        """
        if not comment_id:
            raise ValueError("The 'comment_id' parameter is required and cannot be empty.")

        # Construct the URL for the comment details endpoint
        url = f"{self.base_url}/comments/{comment_id}"

        # Query parameters
        params = {}
        if include_attachments:
            params["include"] = "attachments"

        # Log the request details
        self._log_request("GET", url, params)

        # Make the GET request to the API
        response = requests.get(url, headers=self.headers, params=params)

        # Handle the response
        try:
            return self._handle_response(response)
        except Exception as e:
            logger.error("Error handling response for comment ID %s: %s", comment_id, e)
            raise


    def get_dockets(
        self,
        agency_id: Optional[str] = None,
        search_term: Optional[str] = None,
        last_modified_date_ge: Optional[str] = None,
        last_modified_date_le: Optional[str] = None,
        sort: Optional[str] = None,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
    ) -> Any:
        """
        Retrieves a list of dockets based on the provided filters.

        Args:
            agency_id (Optional[str]): Filters results for the agency acronym (e.g., "EPA").
            search_term (Optional[str]): Filters results based on the given search term.
            last_modified_date_ge (Optional[str]): Filters results with last modified date >= this value.
            last_modified_date_le (Optional[str]): Filters results with last modified date <= this value.
            sort (Optional[str]): Sorts the results by fields like "title", "docketId", or "lastModifiedDate".
            page_number (Optional[int]): Specifies the page number of results to return (1-20).
            page_size (Optional[int]): Specifies the number of results per page (5-250).

        Returns:
            Any: The JSON response from the API.

        Raises:
            ValueError: If invalid parameters are provided.
        """
        url = f"{self.base_url}/dockets"
        params = {}

        # Map arguments to API parameters
        if agency_id:
            params["filter[agencyId]"] = agency_id
        if search_term:
            params["filter[searchTerm]"] = search_term
        if last_modified_date_ge:
            params["filter[lastModifiedDate][ge]"] = last_modified_date_ge
        if last_modified_date_le:
            params["filter[lastModifiedDate][le]"] = last_modified_date_le
        if sort:
            params["sort"] = sort
        if page_number:
            params["page[number]"] = page_number
        if page_size:
            params["page[size]"] = page_size

        # Log the request details
        self._log_request("GET", url, params)

        # Make the GET request to the API
        response = requests.get(url, headers=self.headers, params=params)

        # Handle the response
        try:
            return self._handle_response(response)
        except Exception as e:
            logger.error("Error handling response for dockets: %s", e)
            raise


    def get_docket_details(self, docket_id: str) -> Any:
        """
        Retrieves detailed information for a specific docket.

        Args:
            docket_id (str): The ID of the docket to retrieve.

        Returns:
            Any: The JSON response from the API.

        Raises:
            ValueError: If the docket_id is not provided or is empty.
        """
        if not docket_id:
            raise ValueError("The 'docket_id' parameter is required and cannot be empty.")

        # Construct the URL for the docket details endpoint
        url = f"{self.base_url}/dockets/{docket_id}"

        # Log the request details
        self._log_request("GET", url)

        # Make the GET request to the API
        response = requests.get(url, headers=self.headers)

        # Handle the response
        try:
            return self._handle_response(response)
        except Exception as e:
            logger.error("Error handling response for docket ID %s: %s", docket_id, e)
            raise
    

    def _log_request(self, method: str, url: str, params: Optional[Dict[str, Any]] = None):
        """
        Logs the details of an API request.

        Args:
            method (str): The HTTP method (e.g., GET, POST).
            url (str): The request URL.
            params (Optional[Dict[str, Any]]): The query parameters.

        Notes:
            - This method is used for debugging and monitoring API requests.
            - It logs the HTTP method, URL, and query parameters being sent to the API.
        """
        logger.info("API Request - Method: %s, URL: %s, Params: %s", method, url, params)

