
### **Workshop Title**:  
*Introduction to Agentic AI: Building a Chatbot for Regulations.gov*

### **Duration**:  
8 hours (including breaks)

---

### **Detailed Schedule**

#### **1. Welcome and Introduction** *(30 minutes)*  
- **Goals**:  
  - Set expectations and introduce the workshop objectives.  
  - Show the **end-to-end demo of the chatbot** to give participants a clear vision of what they’ll build.
- **Topics**:  
  - What is agentic AI? Why is it important?  
  - Overview of the chatbot functionality and Regulations.gov API.  
  - Hands-on goals for the day.  

---

#### **2. Foundations of Agentic AI** *(1 hour)*  
- **Goals**:  
  - Teach participants the basics of agentic AI and the Swarm framework.  
- **Topics**:  
  - What are agents? How do they communicate and delegate tasks?  
  - Overview of Swarm: orchestrator + agent model, and handoffs.  
  - Other frameworks in brief (e.g., LangChain, Phidata).  
- **Hands-On Activity**:  
  - Participants set up their environment:
    - Install Python, Swarm, and dependencies.  
    - Clone the pre-prepared GitHub repository.  
  - Explore the project structure to understand components.  

---

#### **3. Regulations.gov API Overview** *(45 minutes)*  
- **Goals**:  
  - Understand the API and its entities.  
- **Topics**:  
  - Key entities: Dockets, Documents, Comments.  
  - How search and retrieve calls work.  
  - Authentication and rate limits.  
- **Hands-On Activity**:  
  - Run example API calls using cURL or Postman.  
  - Write a basic Python script to make API requests.  

---

#### **4. Building the Console Chatbot (Part 1: Orchestrator and First Agent)** *(1.5 hours)*  
- **Goals**:  
  - Set up the orchestrator and the first agent for searching dockets.  
- **Topics**:  
  - Define the orchestrator’s role.  
  - Build an agent for **searching dockets** using the API.  
  - Handle user queries and return results.  
- **Hands-On Activity**:  
  - Implement the orchestrator and the first agent.  
  - Test the chatbot for basic queries (e.g., "Find dockets about climate policy").  

---

#### **Lunch Break** *(1 hour)*  

---

#### **5. Building the Console Chatbot (Part 2: Additional Agents)** *(1.5 hours)*  
- **Goals**:  
  - Expand the chatbot by adding agents for documents and comments.  
- **Topics**:  
  - Add agents for:
    - **Searching documents** related to dockets.  
    - **Retrieving comments** for specific documents.  
  - Implement agent handoffs for multi-step workflows.  
- **Hands-On Activity**:  
  - Code and integrate the new agents.  
  - Test the chatbot with multi-agent workflows.  

---

#### **6. Transition to Streamlit: Building the UI** *(1 hour)*  
- **Goals**:  
  - Build a basic user interface for the chatbot using Streamlit.  
- **Topics**:  
  - Introduction to Streamlit.  
  - Connect the chatbot logic to a simple UI.  
  - Add input fields and display results interactively.  
- **Hands-On Activity**:  
  - Set up Streamlit and build the UI.  
  - Run the chatbot with the UI and test it.  

---

#### **7. What’s Missing: PoC vs. Production** *(45 minutes)*  
- **Goals**:  
  - Discuss the limitations of the current implementation and what’s needed for production readiness.  
- **Topics**:  
  - **Chatbot Limitations**:
    - Statelessness, lack of persistence, error handling, scalability, and security.  
  - **Framework Limitations**:
    - Swarm’s experimental nature, debugging tools, and lack of built-in memory.  
  - **Production Features**:
    - Adding state management, advanced UX, and robust monitoring.  
- **Interactive Discussion**:  
  - Group brainstorm: What would participants add/change to scale this chatbot to production?  

---

#### **8. Wrap-Up and Q&A** *(30 minutes)*  
- **Goals**:  
  - Reflect on what was learned and discuss next steps.  
- **Topics**:  
  - Recap of agentic AI principles and chatbot architecture.  
  - Resources for further learning (e.g., docs, tutorials, other frameworks).  
- **Activity**:  
  - Participants share takeaways and ask final questions.

---

### **Break Times**
- **Morning Break**: 15 minutes  
- **Afternoon Break**: 15 minutes  

---

### **Final Notes**
- **GitHub Repo**: Ensure the repo includes a clear `README` with step-by-step instructions and starter code for each session.  
- **Facilitator Tips**:
  - Keep sessions interactive and guide participants through debugging.  
  - Allocate extra time to help slower participants catch up without delaying the group.  
- **Outcomes**:
  - By the end of the workshop, participants will have a working chatbot in both console and Streamlit versions, with a clear understanding of its architecture, limitations, and future potential.  
