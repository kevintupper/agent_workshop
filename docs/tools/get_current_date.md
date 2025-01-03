## Tool: `get_current_date`
- **Description**: Retrieves the current date.

- **Input Parameters**: None.

- **Output**:
    - `currentDate` (string): The current date in `YYYY-MM-DD` format.

- **Example Usage**:
    - Input: None
    - Output: `currentDate="2023-10-15"`

### Example Scenarios:
1. **Regulations.gov Query**:
    - User: "Find documents about climate change from the last 7 days."
    - Agent:
        1. Calls `get_current_date` to retrieve the current date (e.g., "2023-10-15").
        2. Calculates the start date as "2023-10-08" (7 days before the current date).
        3. Calls `get_documents` with `searchTerm="climate change", postedDateGe="2023-10-08", postedDateLe="2023-10-15"`.
        4. Returns the list of documents to the user.
