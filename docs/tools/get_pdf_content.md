## Tool: `get_pdf_content`

### Description
Retrieves the content of a PDF file from a given URL, converts it to Markdown using the `MarkItDown` library, and returns the Markdown content. This tool is useful for analyzing or reviewing the textual content of PDF documents in a structured format.

### Input Parameters
- `pdf_url` (str): The URL of the PDF file to be downloaded and converted to Markdown.

### Output
- `markdown_content` (str): The Markdown representation of the PDF content.

### Example Scenarios
1. **Analyze a PDF Document**:
    - User: "Can you summarize the content of this PDF?"
    - Agent:
        1. Calls `get_pdf_content` with the provided `pdf_url`.
        2. Converts the PDF to Markdown.
        3. Returns the Markdown content to the user for further analysis or summarization.

2. **Extract Text for Review**:
    - User: "I need the text from this PDF to review it."
    - Agent:
        1. Calls `get_pdf_content` with the provided `pdf_url`.
        2. Converts the PDF to Markdown.
        3. Returns the Markdown content to the user for review.

3. **Prepare Content for Further Processing**:
    - User: "Extract the text from this PDF so I can use it in my report."
    - Agent:
        1. Calls `get_pdf_content` with the provided `pdf_url`.
        2. Converts the PDF to Markdown.
        3. Returns the Markdown content for the user to include in their report.

### Usage Guidelines
1. Ensure the `pdf_url` is valid and accessible. If the URL is invalid or the file cannot be downloaded, the tool will raise an error.
2. Use this tool when the user needs the textual content of a PDF in a structured format (Markdown) for analysis, review, or further processing.
3. If the user query suggests they are looking for specific details likely contained in a PDF attachment (e.g., names, descriptions, or other content), use this tool automatically after retrieving the document details with `get_document_details`.
4. If the PDF is large or complex, the conversion may take some time. Inform the user if there is a delay.
5. The tool automatically cleans up temporary files used during the conversion process.
6. Consider using this tool in conjunction with the `get_document_details` tool when the user requires both detailed metadata and the actual content of the document in the PDF.

### Important Notes
- The tool uses the `MarkItDown` library to convert the PDF to Markdown. Ensure the library is installed and properly configured.
- If the PDF content cannot be converted (e.g., due to unsupported formats or errors), the tool will raise an exception with a descriptive error message.
- This tool is designed for extracting text-based content. It may not work well with PDFs that are primarily images or contain non-textual elements.

### Example Usage
1. **Extract Markdown from a PDF**:
    - Input: `pdf_url="https://example.com/sample.pdf"`
    - Output: The Markdown content of the PDF file.

2. **Handle Conversion Errors**:
    - Input: `pdf_url="https://example.com/invalid.pdf"`
    - Output: An error message indicating the PDF could not be downloaded or converted.

3. **Use in a Workflow**:
    - Input: `pdf_url="https://example.com/document.pdf"`
    - Output: The Markdown content, which can then be summarized, analyzed, or included in a report.
