# Introduction to Agentic AI with Regulations.gov

### DURATION
**8 hours** (plus breaks)

---

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

### SECTION-BY-SECTION DETAILS & LAB INSTRUCTIONS

**1. Welcome & Demo (9:00 – 9:20)**
- **Goal:** Show you the **end result** so you know what you’ll build & test today.
- **What You’ll Do**:
  1. **Console Chatbot**: Instructor or a volunteer runs `python app/chatbot.py` so you see how Triage/Agents respond to queries about dockets, documents, comments.
  2. **Streamlit UI**: Then run `streamlit run app/streamlit_chatbot.py`, quickly demonstrating the same multi-agent logic in a web interface.

**2. Environment Setup & Running the Demo (9:20 – 9:40)**
- **Hands-On**:
  1. **Clone** the `agent_workshop` and `swarm_azure` repositories.
  2. **Create**/Activate your Python 3.10+ environment.
  3. `pip install -r requirements.txt`.
  4. Copy `.env_sample` -> `.env`. Add your `RGA_API_KEY`.
  5. **Test** by running `python app/chatbot.py` and optionally the Streamlit UI.
- **Outcome**: Confirm you can run the console chatbot *and* the UI without error.

**3. Labs: Tools & Testing Notebook (9:40 – 10:30)**
- **Goal**: Gain confidence in how the code calls the Regulations.gov API and returns data.
- **Hands-On Steps**:
  1. Open **`tools_integration_testing.ipynb`** in Jupyter/VSCode.
  2. **Run** all cells to ensure each `get_documents`, `get_dockets`, `get_comments`, etc. works with your API key.
  3. **Experiment**: Tweak parameters like `agencyId="EPA"` or `searchTerm="air quality"`.  
  4. Discuss: Notice how date ranges (`postedDateGe`, `postedDateLe`) work.

**Morning Break (10:30 – 10:45)**

**4. Triage & Agents Walkthrough (10:45 – 11:15)**
- **Goal**: Understand how Triage selects the correct agent, how each agent calls “tools” for relevant tasks.
- **What You’ll See**:
  1. The `triage_agent` in `agents.py` calls `transfer_to_documents()`, `transfer_to_comments()`, or `transfer_to_dockets()` based on your input.
  2. Each specialized agent (Documents, Comments, Dockets) has *instructions* limiting it to that domain.
  3. Explore the `.md` instructions in `app/instructions/`.
- **Discussion**:  
  - Why do we keep agents separate? How does it differ from a single “everything” prompt?

**5. Workflows vs Agents & Instructions (11:15 – 12:00)**
- **Goal**: Realize how “instructions” shape agent responses. Understand difference between an “agent” and “a multi-step workflow.”
- **Hands-On**:
  1. Open **`dockets_agent_instructions.md`** (or any instructions file).  
  2. **Edit** one rule, e.g. allow the Dockets Agent to mention relevant documents (not recommended, but do it for the sake of testing!).  
  3. **Rerun** the console chatbot to see how the agent now responds differently.
- **Concept**:  
  - Agents have *dynamic instructions*. A “workflow” might just be a sequence of tasks, whereas an agent is an entity that can interpret queries and optionally call “tools.”

**Lunch Break (12:00 – 1:00)**

**6. Hands-On Exercises & Tweaks (1:00 – 2:00)**
- **Goal**: Let you try more advanced or creative changes:
  - E.g., modifying date intervals, trying out PDF extraction via `get_pdf_content`.
- **Exercises**:
  1. **Change** the Triage logic in `triage_agent_instructions.md` to handle a new keyword (like “policy” => Documents?).  
  2. **Try** date-based queries in the console: “Show me documents posted in the last 15 days.”  
  3. **Run** or re-run your tests in `tools_integration_testing.ipynb` after changes to confirm.

**7. Extending the System & Agentic Frameworks (2:00 – 3:00)**
- **Goals**:
  1. Compare **Swarm** with other frameworks like LangChain or Haystack.  
  2. Discuss what more is needed for a **real** production app (memory, concurrency, error handling).
- **Lecture/Discussion**:
  - Examples: how we might store user session data, or handle tens of thousands of calls, or integrate retrieval-augmented generation.
  - Q&A: “When do we prefer multiple specialized agents vs. a single large model approach?”

**Afternoon Break (3:00 – 3:15)**

**8. Deeper Integration & Q&A (3:15 – 4:15)** 
- **Goal**: Summarize, discuss next steps, open the floor to questions.
- **Talking Points**:
  1. Consider how you’d **log** or **monitor** the multi-agent calls.  
  2. Brainstorm advanced flows: e.g., hooking up user authentication or storing conversation context.
- **Wrap-Up**:
  - People can continue exploring the codebase.  
  - Coaches available for further help until ~5:00 or the workshop ends.

**(Optional Overflow / Extra Lab) (4:15 – 5:00)**
- For extra time or advanced participants to do deeper dives.  

---

### Participant Takeaways
1. You’ve **run** and **modified** a multi-agent chatbot for searching dockets, documents, and comments.  
2. You’ve learned how instructions, agent tools, and triage integrate to route queries.  
3. You’ve seen how agentic frameworks differ from monolithic prompt solutions, setting the stage for more advanced projects.
