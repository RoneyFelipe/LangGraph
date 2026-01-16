# 🤖 Intelligent Assistant with LangGraph - AI Engineer Challenge

This repository contains the solution for the AI Engineer Technical Challenge. The project consists of a conversational agent capable of autonomously deciding when to respond using its internal knowledge, when to perform precise mathematical calculations, and when to search for real-time information on the web.

## 🚀 Features

- **Intelligent Routing:** The model semantically decides whether to respond with text, perform a calculation, or search the web.
- **Robustness (Retries):** Implemented retry logic using the `stamina` library to handle transient API errors in both LLM calls and mathematical operations.
- **Persistent Memory:** The conversation context is saved in a local SQLite database, allowing continuity across messages.
- **Integrated Tools:**
  - 🧮 **Calculator:** For exact mathematical operations with internal error handling.
  - 🌐 **Web Search (Tavily):** For up-to-date information (e.g., "What is the date today?", "Weather forecast").
  - 🗑️ **Context Management:** A dedicated tool to clear the agent's memory directly from the database.

## 🛠️ Tech Stack

- **Language:** Python 3.12
- **Orchestration:** [LangGraph](https://langchain-ai.github.io/langgraph/) (State graph and execution flow).
- **LLM:** Google Gemini 2.5 Flash (via `langchain-google-genai`).
- **Resilience:** [Stamina](https://stamina.hynek.me/) (For automatic retries on failures).
- **Search Engine:** Tavily AI.
- **Database:** SQLite (via LangGraph's `SqliteSaver`).

---

## 📂 Project Structure

The code is modularized to ensure scalability and maintainability:

```text
├── src/
│   ├── graph.py     # Agent class definition, retry logic, and graph compilation
│   ├── tools.py     # Calculator, Tavily Search, and Memory Reset tools
│   ├── state.py     # AgentState definition and SQLite persistence setup
│   ├── prompts.py   # Dynamic System Prompt (injects current date)
│   └── configs.py   # Environment variable management
├── main.py          # Entry point (Interactive chat loop)
├── requirements.txt # Project dependencies
└── .env.example     # Template for required environment variables
```

---

## ⚙️ How to Run

### 1. Prerequisites
Ensure Python is installed. The use of a virtual environment is highly recommended.

### 2. Installation

Clone the repository and install dependencies using the `requirements.txt` file located in the root directory:

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd <FOLDER_NAME>

# Create and activate virtual environment (Optional but recommended)
python -m venv venv

# On Windows:
# venv\Scripts\activate

# On Linux/Mac:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configuration (.env)

Create a `.env` file in the project root and add your API keys. Make sure they match the names expected by `src/configs.py`:

```env
GEMINI_API_KEY="your_google_ai_studio_key"
TAVILY_API_KEY="your_tavily_key"
```

### 4. Running the Assistant

Execute the main file to start the chat loop:

```bash
python main.py
```

---

## 🧠 Implementation Logic

The solution was built using a custom `Agent` class that wraps the **LangGraph** state machine.

1.  **Dynamic Context:** The system prompt in `prompts.py` automatically injects the current date, ensuring the model knows "today's" date when performing searches.
2.  **Resilient Execution:**
    - The `call_gemini` method in `graph.py` is decorated with `@retry`, allowing up to 3 attempts if the API fails or times out.
    - The internal calculator logic in `tools.py` also implements retry logic to ensure stability.
3.  **Graph Flow:**
    - **Node `llm`**: Invokes the Gemini model with the bound tools.
    - **Conditional Edge**: Checks if the model output contains `tool_calls`.
    - **Node `action`**: Executes the requested tool (Math, Search, or Memory Reset) and returns the result to the graph.
4.  **Transaction Management:**
    - The `reset_memory` tool implements a dedicated SQLite connection to safely delete `checkpoints` and `writes` tables without conflicting with the main LangGraph thread.

---

## 💡 Learnings and Next Steps

### What I learned
* **LangGraph Architecture:** Gained hands-on experience in utilizing LangGraph to structure agent workflows using its graph-based system (nodes and edges).
* **Tool Construction:** Learned how to build custom tools and effectively bind them to the model to extend its capabilities.
* **Model Interaction:** Understood how to manage the interaction loop between the LLM, the state, and tool execution to create a cohesive assistant.

### Future Development
* **Code Quality:** Enforce strict type hints following PEP 8 and integrate tools like `mypy` and linters for code quality control.
* **Model Fallback:** Integrate OpenAI as a fallback provider to ensure system reliability in case of Gemini instability.
* **Advanced Context Control:** Implement tools to manage multiple conversation threads, allowing users to switch between, exit, and resume specific sessions while preserving their full context.
* **Dockerization:** Create a `Dockerfile` for consistent deployment.
* **Streaming:** Implement token streaming to improve the perceived latency for the user.
* **User Interface:** Implement a graphical frontend using Streamlit or Chainlit.

---
