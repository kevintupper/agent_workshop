import os
from dotenv import load_dotenv
from rga_wrapper import RegulationsGovAPI

# Load environment variables
load_dotenv()

# Initialize the Regulations.gov API client
api_key = os.getenv("RGA_API_KEY")
if not api_key:
    raise ValueError("Error: RGA_API_KEY not found in .env. Please set it before running.")

rga_client = RegulationsGovAPI(api_key=api_key)
