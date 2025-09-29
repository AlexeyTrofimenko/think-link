import requests
from models import NoteAgentResponse

API_BASE = "http://api:8000"


def do_agent(note_id: str, message: str | None = None) -> NoteAgentResponse:
    payload = {"note_id": note_id, "message": message}
    r = requests.post(f"{API_BASE}/ai/do", json=payload)
    r.raise_for_status()
    return NoteAgentResponse.model_validate(r.json())


def ask_agent(message: str) -> NoteAgentResponse:
    payload = {"message": message}
    r = requests.post(f"{API_BASE}/ai/ask", json=payload)
    r.raise_for_status()
    return NoteAgentResponse.model_validate(r.json())
