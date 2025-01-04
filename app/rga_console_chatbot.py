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
import dotenv
from datetime import datetime

# Add the parent directory of 'app' and 'swarm' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import for Azure OpenAI
from openai import AzureOpenAI

# Import for SWARM 
from swarm import Swarm, Agent
from swarm.repl.repl import process_and_print_streaming_response, pretty_print_messages

# Import tools for the agents to use
from rga_tools import (
    get_documents,
    get_document_details,
    get_agency_id,
    get_pdf_content,
)

# Get Current Date for temporal context when filtering by date
current_date = datetime.now().strftime("%Y-%m-%d")

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

### Handling Date Parameters:
When the user asks for information that requires filtering by date (e.g., "Show me documents from the last 30 days"), follow these steps:
1. **Always use {current_date} as the current date when you need to calculate date ranges or offsets. 
2. **Calculate Date Ranges**: If the user specifies a relative date range (e.g., "last 30 days", "last year"), calculate the exact start and end dates using {current_date} as your point of reference for today.
   - Example: For "last 30 days", subtract 30 days from {current_date} to get the start date and use {current_date} as the end date.
   - Example: For "last year", calculate the start date as January 1 of the previous year and the end date as December 31 of the previous year.
3. **Pass the Calculated Dates to Tools**: Use the calculated start and end dates as parameters for tools like `get_documents`.
   - Example: Use `postedDateGe` for the start date and `postedDateLe` for the end date.
4. **Provide Clear Responses**: When responding to the user, clearly state the date range you used for filtering.
   - Example: "Here are the documents posted between 2023-09-15 and 2023-10-15."

### Available Tools:
You have access to the following tools to assist with user queries. Use them as needed to retrieve information or perform tasks.

{get_documents_instructions}

{get_document_details_instructions}

{get_agency_id_instructions}

{get_pdf_content_instructions}

Always strive to provide clear, user-friendly answers. If you're unsure about the user's intent, ask for clarification.
""",
    model="gpt-4o",
    functions=[
        get_documents,  # Use the shared tool
        get_document_details,  # Use the shared tool
        get_agency_id,  # Use the shared tool
        get_pdf_content,  # Use the shared tool
    ]
)

##########################################################################################
# Create chatbot loop
##########################################################################################
def run_chatbot_loop(
    starting_agent,
    context_variables=None,
    stream=False,
    debug=False,
    capture_tools_called=False,
    capture_internal_chatter=False,
) -> None:
    
    # Load the .env file
    dotenv.load_dotenv()

    # Initialize the Azure OpenAI client
    aoai_client = AzureOpenAI(
        api_key=os.getenv("AOAI_KEY"),
        api_version="2024-10-01-preview",
        azure_endpoint=os.getenv("AOAI_ENDPOINT")
    )

    # Initialize the SWARM client
    swarm_client = Swarm(client=aoai_client)

    print("\nStarting RGA Console Chatbot\n")

    messages = []
    agent = starting_agent

    try:
        while True:
            user_input = input("\033[90mUser\033[0m: ")
            messages.append({"role": "user", "content": user_input})

            # Run the agent
            response = swarm_client.run(
                agent=agent,
                messages=messages,
                stream=stream,
                debug=debug,
                capture_tools_called=capture_tools_called,
                capture_internal_chatter=capture_internal_chatter,
            )

            if stream:
                # Handle streaming response
                final_response = None
                for partial_response in response:  # Iterate over the generator
                    process_and_print_streaming_response(partial_response)
                    final_response = partial_response  # Keep track of the last response
            else:
                # Handle non-streaming response
                pretty_print_messages(response.messages)
                final_response = response

            # Show tools called and internal chatter if enabled
            if capture_tools_called and hasattr(final_response, "tools_called"):
                print("\n\033[93mTools Called:\033[0m")
                for tool in final_response.tools_called:
                    print(f"  - Tool: {tool['tool_name']}, Arguments: {tool['arguments']}")

            if capture_internal_chatter and hasattr(final_response, "internal_chatter"):
                print("\n\033[96mInternal Chatter:\033[0m")
                for message in final_response.internal_chatter:
                    print(f"  - {message}")

            # Extend messages and update the agent
            if hasattr(final_response, "messages"):
                messages.extend(final_response.messages)
            if hasattr(final_response, "agent"):
                agent = final_response.agent
                
    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == "__main__":
    # We run the demo loop. The user can now type queries in the console.
    # The agent can call the functions as needed and respond accordingly.
    run_chatbot_loop(agent, stream=True, debug=False, capture_tools_called=True, capture_internal_chatter=False)
