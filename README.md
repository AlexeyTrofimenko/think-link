# 🧠 Think-Link
<img src="https://i.ibb.co/mV668D0p/image.png">

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/FastAPI-async-success?style=for-the-badge&logo=fastapi">
  <img src="https://img.shields.io/badge/Pydantic AI-agents-ef4444?style=for-the-badge&logo=pydantic">
  <img src="https://img.shields.io/badge/Streamlit-frontend-ff4b4b?style=for-the-badge&logo=streamlit">
  <img src="https://img.shields.io/badge/Docker-compose-0db7ed?style=for-the-badge&logo=docker">
</p>

---

<p align="center">
✨ A minimalist note-taking system where you can talk to your notes naturally using AI ✨
</p>

---

## ⚙️ Tech Stack

| Layer | Tools |
|-------|-------|
| **Language** | Python 3.12 |
| **Package Manager** | uv |
| **Backend** | FastAPI (async), SQLAlchemy ORM, Alembic |
| **AI / LLM** | Pydantic AI (agents), Ollama (gemma3:270M), nomic-embed-text, OpenAI API |
| **Database** | PostgreSQL + pgvector |
| **Frontend** | Streamlit |
| **Automation** | n8n (self-hosted workflows) |
| **Infrastructure** | Docker / Docker Compose |
| **Code Quality** | Ruff, mypy |
| **CI/CD** | GitHub Actions |
| **Testing** | pytest |

---

## 🧩 AI Agents

| Agent | Purpose | Abilities |
|--------|----------|-----------|
| **Notes Agent** | Focused on a database | • Creates new notes from natural text<br>• Answers questions using RAG search |
| **Note Agent**  | Focused on a single note | • Answers questions about that note<br>• Edits or extends content<br>• Uses DuckDuckGo Search for real-time context |

---

## 🔀 Routes

### 🩵 Health
| Method | Route | Description |
|--------:|:------|:-------------|
| `GET` | `/health/` | Service heartbeat |
| `GET` | `/health/db` | Database connectivity check |

### 📝 Notes
| Method | Route | Description |
|--------:|:------|:-------------|
| `POST` | `/notes/` | Create a note |
| `GET` | `/notes/` | List all notes |
| `GET` | `/notes/{note_id}` | Retrieve a note |
| `PATCH` | `/notes/{note_id}` | Update note |
| `DELETE` | `/notes/{note_id}` | Delete note |

### 🏷️ Tags
| Method | Route | Description |
|--------:|:------|:-------------|
| `POST` | `/tags/` | Create tag |
| `GET` | `/tags/` | List tags |
| `GET` | `/tags/{tag_id}` | Get tag |
| `DELETE` | `/tags/{tag_id}` | Delete tag |

### 🤖 Agents
| Method | Route | Description |
|--------:|:------|:-------------|
| `POST` | `/ask` | Create or query via RAG |
| `POST` | `/do` | Answer, edit, or extend note |

---

## 🚀 Getting Started

```bash
# clone repo
git clone https://github.com/AlexeyTrofimenko/think-link
cd think-link

# ensure required env keys and secrets

# pull LLM models
ollama pull gemma3:270m
ollama pull nomic-embed-text

# build & run
docker compose up --build

# import n8n workflow
```

<p align="center"><i>Feel free to contribute</i></p>
