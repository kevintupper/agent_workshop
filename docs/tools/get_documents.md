## Tool: `get_documents`

### Description
Searches for documents on Regulations.gov based on the provided criteria. This tool allows filtering by various parameters such as agency, docket, document type, date ranges, and keywords. It retrieves metadata and data about documents, including their titles, IDs, types, and posting dates.

### Input Parameters
- `agencyId` (Optional[str]): Filter by the agency ID (e.g., "EPA").
- `commentEndDate` (Optional[str]): Filter by the comment period end date (format: `YYYY-MM-DD`).
- `docketId` (Optional[str]): Filter by the docket ID.
- `documentType` (Optional[str]): Filters results on the specified document type. Available values : Notice, Rule, Proposed Rule, Supporting & Related Material, Other
- `frDocNum` (Optional[str]): Filter by the Federal Register document number.
- `searchTerm` (Optional[str]): Perform a full-text search for the specified term.
- `postedDate` (Optional[str]): Filter by a specific posted date (format: `YYYY-MM-DD`).
- `postedDateGe` (Optional[str]): Filter by posted dates greater than or equal to this date (format: `YYYY-MM-DD`).
- `postedDateLe` (Optional[str]): Filter by posted dates less than or equal to this date (format: `YYYY-MM-DD`).
- `lastModifiedDate` (Optional[str]): Filter by a specific last modified date (format: `YYYY-MM-DD`).
- `lastModifiedDateGe` (Optional[str]): Filter by last modified dates greater than or equal to this date (format: `YYYY-MM-DD`).
- `lastModifiedDateLe` (Optional[str]): Filter by last modified dates less than or equal to this date (format: `YYYY-MM-DD`).
- `subtype` (Optional[str]): Filter by the subtype of the document.
- `withinCommentPeriod` (Optional[bool]): Filters results for documents that are open for comment by setting the value to true.
- `sort` (Optional[str]): IMPORTANT: ONLY USE commentEndDate, postedDate, lastModifiedDate, documentId and title. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.
- `pageNumber` (Optional[int]): The page number to retrieve (default: 1, minimum: 1, maximum: 20).
- `pageSize` (Optional[int]): The number of results per page (default: 5, minimum: 5, maximum: 250).

### Output
#### Data
- `documentId` (str): The unique ID of the document.
- `title` (str): The title of the document.
- `documentType` (str): The type of the document (e.g., "Proposed Rule", "Rule").
- `postedDate` (str): The date the document was posted (format: `YYYY-MM-DD`).
- `lastModifiedDate` (str): The date the document was last modified (format: `YYYY-MM-DD`).
- `docketId` (str): The ID of the docket the document belongs to.
- `agencyId` (str): The ID of the agency that posted the document.
- `commentEndDate` (str): The end date of the comment period (if applicable).
- `subtype` (str): The subtype of the document (if available).

#### Metadata
- `totalElements` (int): The total number of documents matching the query.
- `pageNumber` (int): The current page number.
- `pageSize` (int): The number of results per page.
- `totalPages` (int): The total number of pages available.

#### Aggregate Outpout
The document counts are aggregated by agencyId and by documentType if you need totals.

### Usage Guidelines
1. Use only the parameters necessary to answer the user's query. Avoid overloading the request with unnecessary filters.
2. IMPORTANT: If the user is looking for specific metadata that includes aggregates of doctypes and agencies, or they only need a handful of documents use a small `pageSize` (e.g., 5 or 10).
3. For queries requiring a large number of documents, use a reasonable `pageSize` (e.g., 50 or 100) and handle pagination to aggregate results across multiple pages.
4. Adhere to the minimum and maximum for pageSize and pageNumber. NOTE: These are ints.
5. If the query involves date ranges, use `postedDateGe` and `postedDateLe` to filter documents efficiently.
6. Sort results by relevant fields (e.g., "-postedDate" for the most recent documents) to prioritize the most useful data for the user.
7. **Avoid including raw API links in responses**. Instead, summarize the document details in a user-friendly way. If the user needs access to the document, provide clear instructions on how to find it on Regulations.gov (e.g., "Search for the document by its title or ID on Regulations.gov").
8. If the user asks for specific content within a document, consider using the `get_document_details` and `get_pdf_content` tools to retrieve and summarize the content.

### Example Usage
1. **Search for documents with a specific term**:
   - Input: `searchTerm="climate change", page_size=5`
   - Output: A list of up to 5 documents matching the term "climate change".
2. **Retrieve documents posted in the last 30 days**:
   - Input: `postedDateGe="2023-09-15", postedDateLe="2023-10-15", sort="-postedDate", page_size=10`
   - Output: A list of up to 10 documents posted in the last 30 days, sorted by the most recent.
3. **Paginate through results for a large query**:
   - Input: `searchTerm="water", pageSize=50, pageNumber=1`
   - Output: The first 50 documents matching the term "water".
   - Follow-up Input: `searchTerm="water", pageSize=50, pageNumber=2`
   - Output: The next 50 documents matching the term "water". 