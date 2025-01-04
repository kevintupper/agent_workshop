##########################################################################################
# agents.py
#
# This script defines all the agents used in the regulations.gov chatbot.
#
# Agents:
#   1. **Triage Agent**: Routes user queries to the appropriate specialized agent.
#   2. **Documents Agent**: Handles queries related to searching and retrieving documents.
#   3. **Comments Agent**: Handles queries related to submitting and retrieving comments.
#   4. **Dockets Agent**: Handles queries related to retrieving docket details.
#
# Each agent is built using the SWARM framework and is designed to interact with the
# tools defined in `tools.py`. The Triage Agent acts as the central decision-maker,
# delegating tasks to the specialized agents as needed.
#
# Usage:
#   - Import the desired agent(s) into the main chatbot script (e.g., rga_console_chatbot.py).
#   - Use the Triage Agent to route user queries to the appropriate specialized agent.
#
##########################################################################################

# Standard imports
import os
from datetime import datetime
# SWARM imports
from swarm import Agent
    
# App imports
from app.tools import (
    get_agency_id,
    get_pdf_content,
    transfer_to_documents, 
    transfer_to_comments,
    transfer_to_dockets,    
    transfer_back_to_triage
)

from app.rga_tools import(
    get_documents,
    get_document_details,

)

# Default model for all agents
default_agent_model = "gpt-4o"

##########################################################################################
# Helper Function to Load Instructions
##########################################################################################

def load_instructions(file_name: str, **kwargs) -> str:
    """
    Load agent instructions from a markdown file in the 'instructions' folder and
    substitute placeholders with provided values.

    Args:
        file_name (str): The name of the markdown file (e.g., 'triage_agent_instructions.md').
        **kwargs: Key-value pairs for placeholder substitution (e.g., current_date="2023-10-01").

    Returns:
        str: The content of the markdown file with placeholders replaced.
    """
    instructions_dir = os.path.join(os.path.dirname(__file__), "instructions")
    file_path = os.path.join(instructions_dir, file_name)
    with open(file_path, "r") as file:
        instructions = file.read()

    # Perform placeholder substitution
    if kwargs:
        instructions = instructions.format(**kwargs)
    
    return instructions


##########################################################################################
# Get the current date for dynamic substitution in instructions for all agents
##########################################################################################
current_date = datetime.now().strftime("%Y-%m-%d")

##########################################################################################
# Triage Agent
##########################################################################################

# Load instructions for the Triage Agent with dynamic substitution
TRIAGE_AGENT_INSTRUCTIONS = load_instructions("triage_agent_instructions.md", current_date=current_date)

# Define the Triage Agent
triage_agent = Agent(
    name="Triage Agent",
    instructions=TRIAGE_AGENT_INSTRUCTIONS,
    model=default_agent_model,
    functions=[transfer_to_documents, transfer_to_comments, transfer_to_dockets]  
)


##########################################################################################
# Documents Agent
##########################################################################################

# Load instructions for the Documents Agent
DOCUMENTS_AGENT_INSTRUCTIONS = load_instructions("documents_agent_instructions.md", current_date=current_date)

# Define the Documents Agent
documents_agent = Agent(
    name="Documents Agent",
    instructions=DOCUMENTS_AGENT_INSTRUCTIONS,
    model=default_agent_model,
    functions=[get_documents, get_document_details, get_agency_id,get_pdf_content, transfer_back_to_triage]
)

##########################################################################################
# Comments Agent
##########################################################################################

# Load instructions for the Comments Agent
COMMENTS_AGENT_INSTRUCTIONS = load_instructions("comments_agent_instructions.md", current_date=current_date)

# Define the Comments Agent
comments_agent = Agent(
    name="Comments Agent",
    instructions=COMMENTS_AGENT_INSTRUCTIONS,
    functions=[]  # Add comment-related tools here when implemented
)

##########################################################################################
# Dockets Agent
##########################################################################################

# Load instructions for the Dockets Agent
DOCKETS_AGENT_INSTRUCTIONS = load_instructions("dockets_agent_instructions.md", current_date=current_date)

# Define the Dockets Agent
dockets_agent = Agent(
    name="Dockets Agent",
    instructions=DOCKETS_AGENT_INSTRUCTIONS,
    functions=[]  # Add docket-related tools here when implemented
)


##########################################################################################
# Export All Agents
##########################################################################################

# Export all agents for use in other scripts
__all__ = ["triage_agent", "documents_agent", "comments_agent", "dockets_agent"]
