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

## Setup

### 0. Start Postgres
Open cmd
wsl
cd ~
cd projects/postgres
docker compose up -d

### 1. Activate Virtual Environment
conda activate Schemasense

### 2. Run Application

Run Backend:
python -m uvicorn backend.main:fastapi_app --reload
http://127.0.0.1:8000/docs

Run Frontend:
1. React
cd frontend
npm run dev -- --port 3003
http://localhost:3003

2. Streamlit
streamlit run app.py

### 3. Testing Queries
Show me all employees in IT earning more than 70k