import httpx

from app.services.settings_n8n import n8n_settings


async def note_created_webhook(note_id: int, title: str, content: str | None) -> None:
    if n8n_settings.N8N_DISABLED or not n8n_settings.N8N_URL:
        return

    async with httpx.AsyncClient(timeout=5) as client:
        await client.post(
            n8n_settings.N8N_URL,
            json={"note_id": note_id, "title": title, "content": content},
        )
