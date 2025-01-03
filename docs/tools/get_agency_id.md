## Tool: `get_agency_id`
- **Description**: Retrieves a json array with each agencyID (ID) and the agency.

- **Input Parameters**: None.

- **Output**:
    - `agencyList` (list): A list of particpating agencies by Id.


### Example Scenarios:
1. **Regulations.gov Query**:
    - User: "Find documents about climate change issued by the state dept."
    - Agent:
        1. Calls `get_agency_id` to retrieve the list of agencies.
        2. Determines
        3. Calls `get_documents` with `searchTerm="climate change", agencyId="DOS".
        4. Returns the list of documents to the user.

### Important Note:

Only use this if you want to lookup an agencyID to use as a parameter for retrieving data with get_documents.