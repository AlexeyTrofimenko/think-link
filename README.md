# 🧠 Think-Link

Minimalist note-taking system with AI-powered enrichment.

---

## ✨ Features
- CRUD operations for **notes** and **tags** (FastAPI, async)
- Interactive UI for managing notes (Streamlit)
- Automatic tag generation via **Ollama** (gemma3:270M) and **n8n workflow**
- Persistent storage with **PostgreSQL** (Alembic migrations, SQLAlchemy ORM)
- Fully containerized with **Docker** and **Docker Compose**
- Continuous Integration with **GitHub Actions**
- Tested with **pytest**

---

## 🛠️ Tech Stack

| Layer                  | Tools |
|-------------------------|-------|
| **Language**           | Python 3.12 |
| **Package Manager**    | uv (modern Python packaging) |
| **Backend**            | FastAPI (async), SQLAlchemy ORM, Alembic |
| **Validation & Config**| Pydantic, Pydantic Settings |
| **Database**           | PostgreSQL |
| **Frontend**           | Streamlit |
| **AI/LLM**             | Ollama (gemma3:270M) |
| **Automation**         | n8n (self-hosted workflow engine) |
| **Infrastructure**     | Docker, Docker Compose |
| **CI/CD**              | GitHub Actions |
| **Testing**            | pytest |

---

## 📐 Architecture
- **FastAPI** exposes async CRUD routes for notes & tags.  
- **PostgreSQL** stores notes, tags, and relations.  
- **Alembic** manages schema migrations.  
- **Streamlit** provides a simple UI to view, create, and edit notes.  
- **n8n** subscribes to FastAPI events (webhooks) → sends note content into **Ollama** → receives suggested tags → updates DB.  

---
## 📸 Screenshots
- FastAPI docs (Swagger) → [screenshot](https://i.postimg.cc/htzph2q9/image.png)
- Streamlit UI → [screenshot](https://i.postimg.cc/HsfbvHfy/image.png)
- n8n workflow editor → [screenshot](https://i.postimg.cc/QdtvmgZt/image.png) 
## 🔀 API Routes

### Health

* `GET /health/` → `{ "ok": true }`
* `GET /health/db` → database connectivity check

### Notes

* `POST /notes/` → create a new note
* `GET /notes/` → list all notes
* `GET /notes/{note_id}` → get note by ID
* `PATCH /notes/{note_id}` → update note
* `DELETE /notes/{note_id}` → delete note

### Tags

* `POST /tags/` → create a new tag
* `GET /tags/` → list all tags
* `GET /tags/{tag_id}` → get tag by ID
* `DELETE /tags/{tag_id}` → delete tag

---


## 🚀 Getting Started

```bash
# clone repo
git clone https://github.com/AlexeyTrofimenko/think-link
cd think-link

# build & run services
docker compose up --build
