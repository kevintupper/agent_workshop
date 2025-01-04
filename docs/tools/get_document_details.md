1| ## Tool: `get_document_details`
2| 
3| ### Description
4| Retrieves detailed information about a single document on Regulations.gov using its unique `documentId`. This tool provides metadata and data about the document, including its title, type, posting date, last modified date, and other relevant details.
5| 
6| ### Input Parameters
7| - `documentId` (Required[str]): The unique identifier of the document to retrieve details for.
8| - `includeAttachments` (Optional[bool]): If set to `true`, includes attachments in the response. Defaults to `false`.
9| 
10| ### Output
11| #### Data
12| - `documentId` (str): The unique ID of the document.
13| - `title` (str): The title of the document.
14| - `documentType` (str): The type of the document (e.g., "Proposed Rule", "Rule").
15| - `postedDate` (str): The date the document was posted (format: `YYYY-MM-DD`).
16| - `lastModifiedDate` (str): The date the document was last modified (format: `YYYY-MM-DD`).
17| - `docketId` (str): The ID of the docket the document belongs to.
18| - `agencyId` (str): The ID of the agency that posted the document.
19| - `commentStartDate` (str): The date the comment period started (if applicable).
20| - `commentEndDate` (str): The date the comment period ends (if applicable).
21| - `subtype` (str): The subtype of the document (if available).
22| - `withdrawn` (bool): Indicates if the document has been withdrawn.
23| - `attachments` (list[dict]): A list of attachments associated with the document (if `includeAttachments` is `true`).
24| 
25| #### Metadata
26| - `highlightedContent` (str): Content highlighted by the search engine for the `searchTerm` (if applicable).
27| - `keywords` (list[str]): Agency-selected keywords associated with the document to improve searchability.
28| - `ombApproval` (str): The control number assigned by the Office of Management and Budget (OMB) under the Paperwork Reduction Act (if applicable).
29| - `paperLength` (int): The length of the document in paper format (if applicable).
30| - `paperWidth` (int): The width of the document in paper format (if applicable).
31| 
32| ### Usage Guidelines
33| 1. Use this tool when detailed information about a specific document is required.
34| 2. Always provide a valid `documentId` to retrieve the document details.
35| 3. If attachments are needed, set `includeAttachments` to `true`. Note that attachments are not included by default.
36| 4. Ensure the `documentId` is valid and corresponds to an existing document on Regulations.gov.
37| 5. If the document includes a PDF attachment and the user's query suggests they are looking for specific content within the document, consider using the `get_pdf_content` tool to retrieve and process the PDF content automatically.
38| 6. If the user prompt would benefit from the actual content of the document in the PDF, consider using the `get_pdf_content` tool in conjunction with this tool.
39| 
40| ### Example Usage
41| 1. **Retrieve details for a specific document**:
42|    - Input: `documentId="EPA-HQ-OAR-2003-0129-0001"`
43|    - Output: Detailed information about the document with ID `EPA-HQ-OAR-2003-0129-0001`.
44| 
45| 2. **Retrieve details for a document with attachments**:
46|    - Input: `documentId="EPA-HQ-OAR-2003-0129-0001", includeAttachments=true`
47|    - Output: Detailed information about the document, including its attachments.
