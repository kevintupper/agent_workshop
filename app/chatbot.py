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
import json

# Add the parent directory of 'app' and 'swarm' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import for Azure OpenAI
from openai import AzureOpenAI

# Import for SWARM 
from swarm import Swarm
from swarm.repl.repl import process_and_print_streaming_response, pretty_print_messages

# Import the main agent
from app.agents import triage_agent


# Load the .env file
dotenv.load_dotenv()

# Initialize the Azure OpenAI client
aoai_client = AzureOpenAI(
    api_key=os.getenv("AOAI_KEY"),
    api_version="2024-10-01-preview",
    azure_endpoint=os.getenv("AOAI_ENDPOINT")
)



##########################################################################################
# Create chatbot loop
##########################################################################################
def run_chatbot_loop(
    starting_agent=triage_agent,  # Use the Triage Agent as the starting agent
    stream=False,
    debug=False,
    capture_tools_called=False,
    capture_internal_chatter=False,
) -> None:
    
    # Initialize the SWARM client
    print("\nStarting RGA Console Chatbot\n")
    swarm_client = Swarm(client=aoai_client)

    # Initialize the messages list
    messages = []

    while True:
        user_input = input("\033[90mUser\033[0m: ")
        messages.append({"role": "user", "content": user_input})

        response = swarm_client.run(
            agent=starting_agent,
            messages=messages,
            stream=stream,
            debug=debug,
            capture_tools_called=capture_tools_called,
            capture_internal_chatter=capture_internal_chatter,
        )

        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        if capture_tools_called and response.tools_called:
            print("\n\033[93mTools Called:\033[0m")
            for tool in response.tools_called:
                print(f"  - Tool: {tool['tool_name']}, Arguments: {tool['arguments']}")

        if capture_internal_chatter and response.internal_chatter:
            print("\n\033[96mInternal Chatter:\033[0m")
            for message in response.internal_chatter:
                print(f"  - {message}")

        messages.extend(response.messages)
        starting_agent = response.agent
        print(f"Starting agent: {starting_agent.name}")
                
if __name__ == "__main__":
    # Start the chatbot loop with the Triage Agent
    run_chatbot_loop(stream=True, debug=False, capture_tools_called=True, capture_internal_chatter=False)
