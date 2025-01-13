# Coaches Guide & Extended Notes

---

### Instructor’s Agenda Overview
1. **9:00 – 9:20** Demo final chatbot + environment overview.  
2. **9:20 – 9:40** Help them set up environment and run.  
3. **9:40 – 10:30** Tools & test notebook exploration.  
4. **(Break)**  
5. **10:45 – 11:15** Triage & agent code review.  
6. **11:15 – 12:00** Workflows vs agents, Agent Instructions, letting them tweak.  
7. **(Lunch)**  
9. **1:00 – 2:00** More advanced experimentation.  
8. **2:00 – 3:00** Discussion: other frameworks, real-app concerns.  
10. **(Break)**  
11. **3:15 – 4:15** Q&A, next steps.  
12. **4:15 – 5:00** Overflow time.

### WORKSHIP OUTLINE

| **Time**     | **Section**                                                  | **Description**                                                              |
|--------------|--------------------------------------------------------------|------------------------------------------------------------------------------|
| **9:00 – 9:20**  | 1. Welcome & Demo                                        | Quick intro & run the console+Streamlit chatbot to show final outcome.       |
| **9:20 – 9:40**  | 2. Environment Setup & Running the Demo                  | Clone repos, set up `.env`, run console & UI.                                |
| **9:40 – 10:30** | 3. Labs: Tools & Testing Notebook                        | Explore `tools_integration_testing.ipynb`, experiment with API queries.      |
| **10:30 – 10:45**| **Morning Break**                                        | 15-minute break.                                                             |
| **10:45 – 11:15**| 4. Triage & Agents Walkthrough                           | Understand Triage Agent, specialized agents & agent tools.                   |
| **11:15 – 12:00**| 5. Workflows vs Agents & Instructions                    | Discuss workflowa vs agents, agent instructions, practice changing them.     |
| **12:00 – 1:00** | **Lunch Break**                                          | 1 hour.                                                                      |
| **1:00 – 2:00**  | 6. Hands-On Exercises & Tweaks                           | Tweak instructions, test advanced date queries, check agent scoping.         |
| **2:00 – 3:00**  | 7. Extending the System & Agentic Frameworks             | Compare agentic frameworks, talk “real app” vs. PoC, advanced features.      |
| **3:00 – 3:15**  | **Afternoon Break**                                      | 15-minute break.                                                             |
| **3:15 – 4:15**  | 8. Deeper Integration & Q&A                              | Brainstorm production readiness, Q&A, final recap.                           |
| **4:15 – 5:00**  | (Optional Overflow / Extra Lab)                          | Extra time for expansions, coding experiments, or wrap-up.                   |

---

## **Key Instructor Notes:**

### Welcome & Demo
- **Prep**: Start your environment, confirm `chatbot.py` runs smoothly.  
- **Talking Points**:
  - Focus on showing how queries to the console or UI get triaged: “Show me dockets about air quality,” “Get me last 10 comments,” etc.

### Environment Setup & Running the Demo
- **Ensure** participants have a functional `.env` with `RGA_API_KEY`.
- **Optional**: Provide a shared test API key if some participants can’t get one.

### Labs: Tools & Testing Notebook
- **File**: `app/tools_integration_testing.ipynb`
- **Encourage** them to watch the requests/responses for `agencyId`, `searchTerm`, etc.
- **Possible Issues**: A 403 means invalid key. A 429 means rate-limited.

### Triage & Agents Walkthrough
- **Emphasize** how Triage Agent only routes, does not handle direct retrieval itself.
- **Check** if participants see the difference between Triage and specialized agents.

### Agents vs. Workflows and Instructions
- **Key Concept**: 
  - An *agent* has reasoning capacity and tool-calling capabilities within certain domain instructions.  
  - A *workflow* can just be a series of steps without that reasoning or adaptation to user input beyond a standard flow.
- **Exercise**: 
  - Have them add or remove certain disclaimers or step clarifications in `dockets_agent_instructions.md`. See how it changes the AI’s output.

### Hands-On Exercises & Tweaks
- **Ideas**:
  1. Show how to filter documents by date using a new parameter (like `postedDateGe="2024-01-01"`).  
  2. Let them adjust Triage so that if user says “I want to see pending documents,” it picks the Documents Agent.  
  3. Use `get_pdf_content` to retrieve PDF text from a known URL, verifying the content is converted to Markdown.

### Extending the System & Agentic Frameworks
- **Compare**: 
  - *AutoGen* / *Semantic Kernel* / *Swarm* / *LangChain* / *SmolAgents* / *PhiData*.  
  - Memory / state management / logging / concurrency concerns.
- **Q&A** on real-world production: 
  - Logging system, error handling, concurrency (multiple user sessions).

### **Deeper Integration & Q&A**
- **Instructor**: 
  - Potential advanced expansions (like storing conversation in a database, hooking to a front-end JS app, or hooking to another LLM for advanced summarization).  

### **Wrap-Up**
- Encourage them to revisit the code at home, maybe implement brand new “Search by RIN” or advanced date math.

---

## **Exercise & Notebook Suggestions**

1. **Test Notebook**: 
   - Already provided in `tools_integration_testing.ipynb`. Ask them to modify parameters (like `agencyId="DOS"`, `searchTerm="ITAR"`) to see how results change.

2. **Instruction Tweak**:
   - Provide a short textual snippet to insert into `comments_agent_instructions.md` that changes how it references document attachments. Let participants see how the agent’s behavior modifies.

3. **Agent vs. Workflow**:
   - Present a short scenario: “If user says ‘Find docket, then get me 2 documents from it, then fetch the PDF text’—would you treat that as a single agent or multiple steps in a workflow?” Let them discuss in small groups.

4. **Production Feasibility**:
   - Brainstorm how to handle 100K comments or a multi-tenant environment.  
   - Could they put these tools behind an API gateway or Docker container? Brainstorm solutions.

---

**End of Instructor Guide**  

These documents should set you up for a well-structured workshop. Good luck!