# SchemaSense

SchemaSense is a web application that enables users to query databases (starting with PostgreSQL) using natural language.  
It automatically discovers schemas and columns, generates safe SQL queries via an agentic workflow, executes them, and summarizes results back to the user.

---

## 🚀 Features
- **Schema Discovery**: Connect to a database and automatically fetch tables, columns, and types.  
- **Agentic Workflow**:
  1. **LLM Generator** → Converts user questions into SQL (`SELECT` only).  
  2. **Evaluator Agent** → Validates query safety and correctness.  
  3. **Executor Agent** → Runs the query against the database.  
  4. **Summarizer Agent** → Translates raw results into human‑readable answers.  
- **Safe by Design**: Restricts queries to `SELECT` statements to prevent destructive operations.  
- **Extensible**: Future support for multiple databases and advanced summarization.

---

## 🛠️ Tech Stack
- **Backend**: Python / FastAPI  
- **Database**: PostgreSQL (initial target)  
- **LLM Integration**: OpenAI / HuggingFace / other pluggable models  
- **Frontend**: React (planned)  
- **Containerization**: Docker + Docker Compose  


Activate venv: conda activate Schemasense
python -m backend.api.agents.generator
python -m backend.api.graph.workflow
python -m uvicorn backend.main:fastapi_app --reload