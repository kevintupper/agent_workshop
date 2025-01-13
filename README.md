# Agent Workshop: Regulations.gov Chatbot

Welcome to the **Agent Workshop** repository! This project demonstrates how to build a **multi-agent chatbot** that interacts with the [Regulations.gov v4 API](https://open.gsa.gov/api/regulationsgov/) to handle data for **dockets**, **documents**, and **comments**. The chatbot uses the [Swarm framework](https://github.com/kevintupper/swarm_azure) to orchestrate specialized agents, each equipped with the proper tools for querying and retrieving data.

---

## Table of Contents
1. [Project Overview](#project-overview)  
2. [Key Features](#key-features)  
3. [Prerequisites](#prerequisites)  
4. [Installation](#installation)  
5. [Configuration](#configuration)  
6. [Usage](#usage)  
7. [Repository Structure](#repository-structure)  
8. [License](#license)  

---

## Project Overview

In this workshop, you will:
- Learn to set up **Triage**, **Dockets**, **Documents**, and **Comments** agents that only respond to relevant user requests.  
- Integrate Python tooling to process PDF content, handle date calculations, and manage user queries.  
- Deploy the chatbot in two ways: **console** (`python app/chatbot.py`) and **Streamlit UI** (`streamlit run app/streamlit_chatbot.py`).  

---

## Key Features

- **Multi-Agent Orchestration**: A Triage Agent routes questions to Dockets, Documents, or Comments Agents.  
- **Regulations.gov Data Integration**: Tools call the official v4 API to fetch details on documents, dockets, and comments.  
- **Date & Pagination Helpers**: Allows queries like “last 30 days” or “posted this year.”  
- **PDF Extraction**: Converts PDF attachments to Markdown for summarization or direct review.  
- **Streaming Support**: Returns content to the user incrementally in the console or Streamlit UI.  

---

## Prerequisites

1. **Python 3.10+**  
2. **Git** (for cloning this repository)  
3. **Pip** or **pipenv** for package installations  
4. (Optional) **Virtual Environment** tool (e.g., `venv` or `conda`) to isolate dependencies  

---

## Installation

1. **Clone** this repository:
   ```bash
   git clone https://github.com/YourUsername/agent_workshop.git
   cd agent_workshop
   ```

2. **Clone the Swarm Framework**:
    As part of this workshop, we will also be working with the [Swarm framework](https://github.com/kevintupper/swarm_azure). You are encouraged to fork the repository and clone your own version to allow for customization of the agentic code:
    ```bash
    git clone https://github.com/YourUsername/swarm_azure.git
    cd swarm_azure
    ```

    After cloning, you can make adjustments to the Swarm framework as needed for your agents.

3. **Create & activate** a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```
4. **Install** Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Obtain** an API key for [Regulations.gov](https://open.gsa.gov/api/regulationsgov/).  
2. **Copy** `.env_sample` to `.env` in the project root:
   ```bash
   cp .env_sample .env
   ```
3. **Fill** in your `.env` with:
   - `RGA_API_KEY` for the Regulations.gov API  
   - `AOAI_KEY` and `AOAI_ENDPOINT` if you plan to use Azure OpenAI for the language model.

Your `.env` file should look like:
```
RGA_API_KEY="YOUR_API_KEY"
AOAI_ENDPOINT="YOUR_AZURE_OPENAI_ENDPOINT"
AOAI_KEY="YOUR_AZURE_OPENAI_KEY"
```
*(If you’re not using Azure OpenAI, you can still use the local Swarm or any other OpenAI key—just ensure code references are updated.)*

---

## Usage

### 1. **Notebook Testing** (optional)
Run the integration tests to confirm everything works:
```bash
jupyter notebook app/tools_integration_testing.ipynb
```
Open and run each cell to see if the API calls succeed.

### 2. **Console Chatbot**
To launch the CLI-based chatbot:
```bash
python app/chatbot.py
```
Enter queries at the prompt (e.g., “Find me the dockets related to air pollution from EPA”).

### 3. **Streamlit UI**
For a friendly web interface:
```bash
streamlit run app/streamlit_chatbot.py --server.port=8501
```
Open the provided link (usually `http://localhost:8501`) in your browser and chat away.

---

## Repository Structure

```
/agent_workshop
├── app
│   ├── instructions
│   │   ├── dockets_agent_instructions.md
│   │   ├── triage_agent_instructions.md
│   │   ├── documents_agent_instructions.md
│   │   └── comments_agent_instructions.md
│   ├── rga_tools.py
│   ├── streamlit_chatbot.py
│   ├── tools_integration_testing.ipynb
│   ├── rga_types.py
│   ├── tools.py
│   ├── __init__.py
│   ├── agents.py
│   ├── rga_client_instance.py
│   ├── chatbot.py
│   └── rga_wrapper.py
├── LICENSE
├── guide_participants.md
├── guide_coaches.md
├── requirements.txt
├── docs
│   ├── tools
│   │   ├── get_documents.md
│   │   ├── get_pdf_content.md
│   │   ├── get_document_details.md
│   │   └── get_agency_id.md
│   └── api
│       ├── rga_openapi.yaml
│       ├── rga_examples.txt
│       ├── get_xxx.txt - copy/paste of regulations.gov docs
├── README.md
├── agent_patterns.jpeg
├── .env_sample
└── data
    └── agency.json
```

---

## License

This project is licensed under the [MIT License](LICENSE). Feel free to modify, distribute, or enhance this codebase for your own use.  

Enjoy building your **Regulations.gov** multi-agent chatbot! If you have questions or run into issues, feel free to open an issue or submit a pull request. Good luck!