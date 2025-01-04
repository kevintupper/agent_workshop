##########################################################################################
# rga_console_chatbot.py
#
# This script creates a console chatbot using the SWARM framework and the regulations.gov
# API client that we previously built.
#
# The idea:
# - We load the RGA_KEY (Regulations.gov API Key) from a .env file using python_dotenv.
# - We instantiate our RegulationsGovAPI client with this key.
# - We create an Agent that has access to a set of functions that wrap around the
#   RegulationsGovAPI client methods, allowing the Agent to search documents, dockets,
#   comments, and even post comments via the console.
#
# The user can interact with the agent by typing queries in the console. The agent will use
# the provided functions (tools) to get data from the regulations.gov API and respond with
# relevant information.
#
# The code heavily leverages the SWARM example patterns, but is adapted to our use case.
#
# Usage:
#   1. Ensure you have a .env file with: RGA_KEY=YOUR_REGULATIONS_GOV_API_KEY
#   2. pip install -r requirements.txt (should include requests, openai, python-dotenv, swarm)
#   3. Run: python rga_console_chatbot.py
#
##########################################################################################

import os
import sys

# Add the parent directory of 'app' and 'swarm' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import for SWARM (adjusted to use AzureOpenAI)
from swarm import Agent
from swarm.repl import run_demo_loop

# Tools for the agent to use
from rga_tools import (
    get_documents,
    get_document_details,
    get_current_date,
    get_agency_id,
    get_pdf_content,
)


##########################################################################################
# Create our SWARM Agent
#
# The instructions tell the agent what it is and what it can do. We tell it that it can
# help the user interact with the regulations.gov API. The agent can call the functions
# we defined above to fulfill user requests.
##########################################################################################

# Read the instructions for each tool from the tool's documentation files.
with open('docs/tools/get_documents.md', 'r') as file:
    get_documents_instructions = file.read()

with open('docs/tools/get_document_details.md', 'r') as file:
    get_document_details_instructions = file.read()

with open('docs/tools/get_current_date.md', 'r') as file:
    get_current_date_instructions = file.read()

with open('docs/tools/get_agency_id.md', 'r') as file:
    get_agency_id_instructions = file.read()

with open('docs/tools/get_pdf_content.md', 'r') as file:
    get_pdf_content_instructions = file.read()


# Create the agent
agent = Agent(
    name="RegulationsGovAgent",
    instructions=f"""
You are a helpful agent that can search and retrieve information from the Regulations.gov API. Your primary role is to assist the user in finding information related to regulations, documents, dockets, and comments available on Regulations.gov. You can also engage in general conversation when the user is not discussing Regulations.gov topics, but you should qualify your responses when appropriate to ensure clarity.

### General Guidelines:
1. **Primary Focus**: Your main focus is to assist the user with queries related to Regulations.gov. Use the provided tools to retrieve accurate and relevant information.
2. **Non-Regulations.gov Topics**: IMPORTANT: Decline to participate in conversations that are not related to Regulations.gov and the type of subjects found on there, i.e., rules/regulations/etc. If the user asks about something completely unrelated, based on your judgment, respond by saying that you are not able to help with that and that you are primarily focused on discussing content found on Regulations.gov.
   - Example: "I apologize, but my expertise is in Regulations.gov and related topics."
3. **Clarify Ambiguity**: If the user's query is unclear, ask follow-up questions to better understand their intent.

### Handling Document Content:
1. If the user asks for specific details that are likely contained in a document's content (e.g., names, descriptions, or other specific information), follow these steps:
   - Use the `get_document_details` tool to retrieve the document metadata and check for any attachments (e.g., a PDF).
   - If a PDF attachment is available, use the `get_pdf_content` tool to retrieve and process the content.
   - Extract the relevant information from the PDF content and provide a clear, concise response to the user.
2. If the document does not have a PDF attachment or the content is not relevant to the user's query, provide the metadata details instead.
3. **Avoid including raw API links in responses**.
4. **Avoid responses like this:  You can find more details about this document by searching for its title or Document ID on [Regulations.gov](https://www.regulations.gov).**


### Handling Date Parameters:
When the user asks for information that requires filtering by date (e.g., "Show me documents from the last 30 days"), follow these steps:
1. Use the `get_current_date` tool to retrieve the current date.
2. Use the current date to calculate the appropriate date range for filtering.
3. Pass the calculated date range as parameters to the relevant Regulations.gov tools.

### Available Tools:
You have access to the following tools to assist with user queries. Use them as needed to retrieve information or perform tasks.

{get_documents_instructions}

{get_document_details_instructions}

{get_current_date_instructions}

{get_agency_id_instructions}

{get_pdf_content_instructions}

Always strive to provide clear, user-friendly answers. If you're unsure about the user's intent, ask for clarification.
""",
    model="gpt-4o",
    functions=[
        get_documents,  # Use the shared tool
        get_document_details,  # Use the shared tool
        get_current_date,  # Use the shared tool
        get_agency_id,  # Use the shared tool
        get_pdf_content,  # Use the shared tool
    ]
)

##########################################################################################
# Run the interactive console loop using run_demo_loop provided by SWARM
#
# The user can type queries, and the agent will respond.
##########################################################################################

if __name__ == "__main__":
    # We run the demo loop. The user can now type queries in the console.
    # The agent can call the functions as needed and respond accordingly.
    run_demo_loop(agent, stream=True, debug=False, listToolCalls=False)
