## Finalized 8-Hour Workshop Plan

Below is a refined agenda designed for **15 participants** and **3 coaches**, maximizing hands-on practice and collaboration. The goal: by the end, each attendee has a functional chatbot (`chatbot.py` and a Streamlit UI) integrated with the regulations.gov API, plus a solid understanding of Agentic AI principles.

---

### **1. Welcome & Overview (30 minutes)**
- **Goals**: 
  - Introduce instructors, coaches, and participants.
  - Outline workshop objectives and final deliverables.
- **Activities**:
  - Quick round of intros from participants.
  - Short demonstration of the final chatbot capabilities.
  - Overview of the provided repo (structure, key files).

---

### **2. Fundamentals of Agentic AI & Swarm (45 minutes)**
- **Goals**:
  - Teach basic concepts: agentic AI, how Swarm orchestrates agents, and why this approach is powerful.
  - Show how multiple agents can collaborate.
- **Activities**:
  - Diagram of the agent→tool→agent loop.
  - Discussion: advantages over single large model prompting.
  - Brief Q&A to clarify conceptual points.

---

### **3. Regulations.gov API Overview (30 minutes)**
- **Goals**:
  - Ensure everyone understands the API entities: dockets, documents, comments.
  - Show common endpoints, filtering, date ranges, pagination.
- **Activities**:
  - Quick look at example endpoints with cURL/Postman or simple Python requests.
  - Group Q&A: clarify how we’ll use these endpoints in the chatbot.

---

### **4. Build the Console Chatbot – Triage & Dockets (1 hour 30 minutes)**
- **Goals**:
  - Set up the base console chatbot loop.
  - Implement Triage Agent + Dockets Agent to handle simple queries.
- **Activities**:
  - Walk through `chatbot.py` structure.
  - Add Triage Agent logic (decides if a query goes to Dockets).
  - Implement Dockets Agent with the `get_dockets` and `get_docket_detail` tools.
  - Test queries (e.g., “Find me dockets from EPA in the last 7 days”).
- **Hands-On**:
  - Participants code in pairs, coaches circulate to help.
  - By end, a working console chatbot that can route basic docket queries.

**_15-Minute Morning Break_**

---

### **5. Documents & Comments Agents (1 hour)**
- **Goals**:
  - Expand the chatbot with two more agents: Documents and Comments.
  - Show how Triage routes queries to these new agents.
- **Activities**:
  - Implement Documents Agent with `get_documents`, `get_document_details`, and PDF content retrieval.
  - Implement Comments Agent with `get_comments`, `get_comment_details`.
  - Test queries across all three specialized agents.
- **Hands-On**:
  - Pair programming; each pair codes both agents.
  - Validate with sample queries like “Search for documents about water in the last month.”

---

### **6. Lunch Break (45 minutes)**

---

### **7. Enhancing & Testing the Agents (45 minutes)**
- **Goals**:
  - Ensure robust responses, pagination, date calculations, and error handling.
  - Refine Triage logic if the user’s question doesn’t fit any agent.
- **Activities**:
  - Add date math for “last 30 days” or “this year” queries (using dynamic `current_date`).
  - Discuss edge cases (invalid agency ID, zero results).
  - Small group debugging: participants swap code and test each other’s chatbot.
  
**_15-Minute Afternoon Break_**

---

### **8. Streamlit UI – Building a Friendly Frontend (1 hour)**
- **Goals**:
  - Wrap the console chatbot in a clean, interactive UI.
  - Demonstrate how to integrate Streamlit with the Swarm agents.
- **Activities**:
  - Review `streamlit_chatbot.py`.
  - Link up the existing logic from `chatbot.py`.
  - Run local server and test the UI flow.
- **Hands-On**:
  - Pair up again, ensure the UI can handle agent handoffs seamlessly.
  - Check PDF retrieval and text display in the UI.

---

### **9. Q&A, Next Steps & Wrap-Up (45 minutes)**
- **Goals**:
  - Address final questions and discuss productionizing or scaling.
  - Summarize lessons learned and highlight next steps.
- **Topics**:
  - Potential improvements: memory/persistence, advanced authentication, UI polish.
  - Compare with alternative frameworks (LangChain, etc.).
- **Conclusion**:
  - Participants share takeaways.
  - Provide a link or instructions for “answer key” solutions in the repo.

---

## Timing Recap

| Section                                  | Time     |
|------------------------------------------|----------|
| **1. Welcome & Overview**                | 30 min   |
| **2. Fundamentals of Agentic AI & Swarm**| 45 min   |
| **3. Regulations.gov API Overview**      | 30 min   |
| **4. Build Console Chatbot (Triage+Dockets)**| 90 min |
| **Break**                                | 15 min   |
| **5. Docs & Comments Agents**            | 60 min   |
| **6. Lunch**                             | 45 min   |
| **7. Enhancing & Testing**               | 45 min   |
| **Break**                                | 15 min   |
| **8. Streamlit UI**                     | 60 min   |
| **9. Q&A / Wrap-Up**                     | 45 min   |
| **Total**                                | 8 hours  |

